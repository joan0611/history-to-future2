import { D, ERA_LABEL, studyById, type Study } from '../lib/data';
import type { Route } from '../lib/route';
import { StatusChips, StudyDetail } from './StudyView';
import { SpecCards } from '../ui/SpecStatus';
import { QSTUDIES, QuickStudy, qById } from './QuickStudy';

/**
 * 지금 판단하기 — 사이트의 출발점.
 *   1 판단 질문 → 2 관련 과거 흐름 → 3 조건과 연결 근거 → 4 현재와 과거 비교 → 5 조건별 시나리오 → 6 관찰 지표
 * 완성한 분석만 '분석'으로 연다. 아직 끝까지 가지 못한 질문은 '준비 중'으로만 보여주고 완성된 것처럼 꾸미지 않는다.
 */
export function NowView({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const s = r.study ? studyById[r.study] : undefined;
  if (s) return <StudyDetail s={s} nav={nav} />;
  const q = r.study ? qById[r.study] : undefined;
  if (q) return <QuickStudy s={q} nav={nav} />;
  return <Landing nav={nav} />;
}

const STEPS = ['지금 판단하고 싶은 질문', '관련된 과거의 변화 흐름', '변화를 움직인 조건과 연결 근거', '현재와 과거의 비교', '조건별 향후 시나리오', '앞으로 관찰할 지표'];



function Landing({ nav }: { nav: (p: Partial<Route>) => void }) {
  return (
    <div className="view now">
      <section className="panel hero">
        <h2>과거의 변화 원리로 지금의 경제를 읽는다</h2>
        <p className="lead">이 사이트는 사건과 유행을 모아 두는 곳이 아닙니다. 과거에 사회와 경제가 <b>어떤 조건에서, 어떤 경로로</b> 변했는지 근거로 확인하고, 그 원리가 <b>지금도 작동하는지</b> 비교해 <b>앞으로 무엇을 지켜봐야 하는지</b> 찾는 데 씁니다.</p>
        <ol className="readorder">{STEPS.map((x, i) => <li key={x}><b>{i + 1}</b>{x}</li>)}</ol>
      </section>

      <section className="doors" id="doors" aria-label="어디서부터 볼까">
        <button className="door d-hist" onClick={() => nav({ tab: 'history' })}><i aria-hidden>⟶</i><b>전체 역사</b><span>1960년부터 지금까지, 시대마다 무엇이 달라졌나</span></button>
        <button className="door d-field" onClick={() => nav({ tab: 'topic' })}><i aria-hidden>▦</i><b>분야별 변화</b><span>10개 분야에서 한 가지를 끝까지 따라가기</span></button>
        <button className="door d-cycle" onClick={() => nav({ tab: 'cycle' })}><i aria-hidden>↻</i><b>사이클 발견</b><span>되풀이된 것과 이번엔 다른 것</span></button>
        <button className="door d-ask" onClick={() => nav({ tab: 'ask' })}><i aria-hidden>?</i><b>직접 물어보기</b><span>질문을 자료로 분석하고 두 지표를 검정</span></button>
      </section>

      <section className="panel">
        <h2>10개 분야 한눈에 <span className="sub">링이 꽉 찰수록 근거·추론·미래·화면 시험까지 갖춘 분야</span></h2>
        <SpecCards compact />
      </section>

      <section className="panel">
        <h2>지금 판단하고 싶은 질문</h2>
        {D.studies.map((s) => <StudyCard key={s.id} s={s} nav={nav} />)}
        <h3 className="pending-h">근거를 모아 구성한 판단 질문 <span className="muted small">흐름·주제·지표·미래를 6단계 순서로 모았습니다 — 수치는 실제 시계열에서 계산</span></h3>
        <div className="qs-cards">
          {QSTUDIES.map((q) => (
            <button key={q.id} className="studycard qs-card" onClick={() => nav({ tab: 'now', study: q.id })}>
              <b className="sc-q">{q.q}</b>
              <span className="sc-find">{q.short}</span>
              <span className="muted small">흐름 {q.flows.length} · 주제 {q.topics.length} · 지표 {q.inds.length}</span>
              <span className="fc-go">읽기 →</span>
            </button>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>근거가 되는 변화 흐름 <span className="sub">8개 분야 — 한 줄은 한 주제를 1960년대부터 2020년대까지 따라갑니다</span></h2>
        <div className="domgrid">
          {D.domains.map((d) => {
            const fs = D.flows.filter((f) => f.domain === d.id);
            return (
              <div key={d.id} className="domcard">
                <b>{d.label}</b>
                {fs.length ? fs.map((f) => (
                  <button key={f.id} className="link" onClick={() => nav({ tab: 'flow', flow: f.id })}>{f.topic} <span className={`econ e-${f.econ.status}`}>{f.econ.status === 'linked' ? '경제 연결' : f.econ.status === 'partial' ? '일부 연결' : '맥락'}</span></button>
                )) : <span className="muted small">아직 흐름 없음</span>}
              </div>
            );
          })}
        </div>
        <p className="small muted">‘경제 연결’은 이 흐름의 변화가 소비·산업·일자리로 이어진 경로를 근거로 확인했다는 뜻입니다. ‘맥락’ 흐름은 역사·문화적 배경으로만 쓰고 경제 전망의 근거로 넓히지 않습니다.</p>
        <p><button className="btn" onClick={() => nav({ tab: 'flow' })}>변화 흐름 전체 보기 →</button> <button className="btn ghost" onClick={() => nav({ tab: 'history' })}>시대별 사건 둘러보기 →</button></p>
      </section>
    </div>
  );
}

function StudyCard({ s, nav }: { s: Study; nav: (p: Partial<Route>) => void }) {
  return (
    <button className="studycard" onClick={() => nav({ tab: 'now', study: s.id })}>
      <span className="sc-meta"><StatusChips s={s} /> 자료 기준일 {s.asOf}</span>
      <b className="sc-q">{s.explainer ? s.explainer.question : s.title}</b>
      <span className="sc-find">{s.explainer ? s.explainer.short : s.summary.state.text}</span>
      <span className="sc-now muted small">{s.title} — {s.subtitle}</span>
      <span className="fc-go">읽기 →</span>
    </button>
  );
}

export { ERA_LABEL };
