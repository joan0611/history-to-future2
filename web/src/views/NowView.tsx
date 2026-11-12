import { D, ERA_LABEL, flowById, studyById, type Study } from '../lib/data';
import type { Route } from '../lib/route';
import { StatusChips, StudyDetail } from './StudyView';

/**
 * 지금 판단하기 — 사이트의 출발점.
 *   1 판단 질문 → 2 관련 과거 흐름 → 3 조건과 연결 근거 → 4 현재와 과거 비교 → 5 조건별 시나리오 → 6 관찰 지표
 * 완성한 분석만 '분석'으로 연다. 아직 끝까지 가지 못한 질문은 '준비 중'으로만 보여주고 완성된 것처럼 꾸미지 않는다.
 */
export function NowView({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const s = r.study ? studyById[r.study] : undefined;
  if (s) return <StudyDetail s={s} nav={nav} />;
  return <Landing nav={nav} />;
}

const STEPS = ['지금 판단하고 싶은 질문', '관련된 과거의 변화 흐름', '변화를 움직인 조건과 연결 근거', '현재와 과거의 비교', '조건별 향후 시나리오', '앞으로 관찰할 지표'];

/** 근거는 있지만 아직 '현재 비교 → 시나리오 → 지표'까지 완성하지 못한 질문. 흐름(과거 부분)만 연결한다. */
const PENDING: { q: string; flows: string[]; missing: string }[] = [
  { q: '기술 변화는 산업·직업·고용구조를 어떻게 바꿨고, AI는 어디까지 같은 길을 갈까?', flows: ['flow-jobs', 'flow-tech'], missing: '직업별 고용 시계열과 AI 이후 고용 자료를 아직 연결하지 못했다.' },
  { q: '유통과 결제 방식의 변화는 소비와 사업 구조를 어떻게 바꿨나?', flows: ['flow-shop'], missing: '업태별 매출 비중의 연속 통계(1993년 이전)와 현재 플랫폼 거래 자료가 부족하다.' },
  { q: '인구·가구 구성의 변화는 주거와 소비 수요에 어떻게 이어지나?', flows: ['flow-family', 'flow-city'], missing: '가구 구성별 소비 지출 자료를 아직 연결하지 못했다.' },
  { q: '노동시간과 생활시간의 변화는 여가·서비스 수요와 어떤 관계가 있었나?', flows: ['flow-time', 'flow-leisure'], missing: '여가 시간(생활시간조사)과 여가 지출의 연속 자료가 없다.' },
];

function Landing({ nav }: { nav: (p: Partial<Route>) => void }) {
  return (
    <div className="view now">
      <section className="panel hero">
        <h2>과거의 변화 원리로 지금의 경제를 읽는다</h2>
        <p className="lead">이 사이트는 사건과 유행을 모아 두는 곳이 아닙니다. 과거에 사회와 경제가 <b>어떤 조건에서, 어떤 경로로</b> 변했는지 근거로 확인하고, 그 원리가 <b>지금도 작동하는지</b> 비교해 <b>앞으로 무엇을 지켜봐야 하는지</b> 찾는 데 씁니다.</p>
        <ol className="readorder">{STEPS.map((x, i) => <li key={x}><b>{i + 1}</b>{x}</li>)}</ol>
      </section>

      <section className="panel">
        <h2>지금 판단하고 싶은 질문</h2>
        {D.studies.map((s) => <StudyCard key={s.id} s={s} nav={nav} />)}
        <h3 className="pending-h">준비 중인 질문 <span className="muted small">과거 흐름은 있지만 현재 비교·시나리오·지표까지 완성하지 못했습니다</span></h3>
        <ul className="pending">
          {PENDING.map((p) => (
            <li key={p.q}><span className="tag-pending">미완성</span> <b>{p.q}</b>
              <span className="muted small"> 빠진 것: {p.missing}</span>
              <span className="pend-flows">과거 흐름만 보기: {p.flows.map((f) => <button key={f} className="chip" onClick={() => nav({ tab: 'flow', flow: f })}>{flowById[f].topic}</button>)}</span>
            </li>
          ))}
        </ul>
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
