import { useState } from 'react';
import { D, ECON_KO, ERA_LABEL, STATUS_SHORT, flowById, studyById, type LinkKind, type Study, type Synth } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine } from '../ui/Chart';
import { Claims } from '../ui/WhyPanel';
import { LINK_DESC } from './FlowView';

/**
 * 지금 판단하기 — 사이트의 출발점.
 *   1 판단 질문 → 2 관련 과거 흐름 → 3 조건과 연결 근거 → 4 현재와 과거 비교 → 5 조건별 시나리오 → 6 관찰 지표
 * 완성한 분석만 '분석'으로 연다. 아직 끝까지 가지 못한 질문은 '준비 중'으로만 보여주고 완성된 것처럼 꾸미지 않는다.
 */
export function NowView({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const s = r.study ? studyById[r.study] : undefined;
  if (s) return <StudyDetail s={s} r={r} nav={nav} why={why} />;
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
      <span className="sc-meta"><span className="tag-done">분석 완성</span> 자료 기준일 {s.asOf}</span>
      <b className="sc-q">{s.question}</b>
      <span className="sc-find"><b>확인된 것</b> {s.findings[0].text}</span>
      <span className="sc-now"><b>지금 중요한 이유</b> {s.whyNow.text}</span>
      <span className="fc-go">읽기 →</span>
    </button>
  );
}

function SynthLine({ y }: { y: Synth }) {
  const [open, setOpen] = useState(false);
  return (
    <li className="synth">
      <p>{y.text} <span className="ct t-synthesis" title="사이트가 근거 문장을 묶어 쓴 해석">자료 종합</span> <button className="link small" onClick={() => setOpen(!open)}>{open ? '근거 접기' : `근거 ${y.claimIds.length}`}</button></p>
      {open && <Claims ids={y.claimIds} all />}
    </li>
  );
}

const KIND_KO: Record<LinkKind, string> = { causal: '인과', condition: '배경·조건', correlation: '상관', sequence: '시간 순서', interpretation: '해석', hypothesis: '가설', similar: '비교' };

function StudyDetail({ s, r, nav }: { s: Study; r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const [edge, setEdge] = useState<number | null>(null);
  const [cell, setCell] = useState<string | null>(null);
  const inds = s.indicators.map((id) => D.indicators.find((i) => i.id === id)).filter((i) => i && i.unit === '%'); // 단위가 같은 지표만 한 축에 그린다(지수는 제외)
  const COLORS = ['var(--c-economy)', 'var(--c-politics)', 'var(--c-industry)', 'var(--c-culture)'];
  const series = inds.map((ind, i) => ({ key: ind!.id, label: `${ind!.title} (${ind!.unit})`, color: COLORS[i % 4], points: ind!.series.find((x) => x.country === 'KR')!.points.map(([t, v]) => [Number(t.slice(0, 4)), v] as [number, number]).filter(([y]) => y >= 1988) }));
  const ends = inds.map((ind) => ind!.series.find((x) => x.country === 'KR')!.points.at(-1)![0]);
  const allClaims = [...new Set([...s.findings, ...s.same, ...s.different, s.whyNow].flatMap((y) => y.claimIds).concat(s.rows.flatMap((x) => Object.values(x.cells).flatMap((c) => c[1]))).concat(s.mechanism.edges.flatMap((e) => e.claimIds)))];
  const st = { verified: 0, sourced: 0 } as Record<string, number>;
  allClaims.forEach((id) => { const c = D.claims[id]; if (c) st[c.status] = (st[c.status] ?? 0) + 1; });
  const nodeOf = Object.fromEntries(s.mechanism.nodes.map((n) => [n.id, n]));
  return (
    <div className="view study">
      <nav className="crumbline"><button className="link" onClick={() => nav({ study: undefined })}>← 지금 판단하기</button></nav>
      <section className="panel hero">
        <div className="eyebrow"><span className="tag-done">분석 완성</span> 자료 기준일 <b>{s.asOf}</b> · 근거 문장 {allClaims.length}개(두 곳 이상 확인 {st.verified ?? 0} · 한 곳 확인 {st.sourced ?? 0})</div>
        <h2>{s.question}</h2>
        <ol className="readorder mini">{STEPS.map((x, i) => <li key={x}><a href={`#st-${i}`} onClick={(e) => { e.preventDefault(); document.getElementById(`st-${i}`)?.scrollIntoView({ behavior: 'smooth' }); }}><b>{i + 1}</b>{x}</a></li>)}</ol>
        <h3>확인된 핵심</h3>
        <ul className="plain synths">{s.findings.map((y) => <SynthLine key={y.text} y={y} />)}</ul>
        <div className="whynow"><h3>지금 중요한 이유</h3><ul className="plain synths"><SynthLine y={s.whyNow} /></ul></div>
        <details className="scope"><summary>분석 범위와 추적하는 변수</summary>
          <dl><dt>대상</dt><dd>{s.scope.target}</dd><dt>기간</dt><dd>{s.scope.period}</dd><dt>변수</dt><dd>{s.scope.variable}</dd><dt>다루지 않는 것</dt><dd>{s.scope.notIncluded}</dd></dl>
        </details>
      </section>

      <section className="panel" id="st-1">
        <h2><span className="stepno">2</span> 과거에 관찰된 변화 <span className="sub">위기 국면마다 소비가 어떻게 줄고 회복했나</span></h2>
        <Chart ariaLabel="기준금리·물가·실업률 추이와 주요 국면" unit="%" year={r.y} height={240} x0={1988} onPick={(y) => nav({ y })}
          series={series} bands={s.chartNotes.map((n) => ({ from: n.year, to: n.year, tone: 'cmp' as const, label: n.label }))} />
        <div className="legend">{series.map((x) => <span key={x.key}><i className="lg-line" style={{ background: x.color }} />{x.label}</span>)}<span><i className="lg-band cmp" />사건 주석(원인 표시 아님)</span></div>
        <SourceLine ids={inds.flatMap((i) => i!.series.find((x) => x.country === 'KR')!.sourceIds)} extra={`각 지표의 마지막 자료 연도: ${inds.map((i, k) => `${i!.title} ${ends[k]}`).join(' · ')}. 그래프의 수치 움직임만으로 원인을 정하지 않습니다 — 원인은 아래 전달 과정과 근거 문장으로 봅니다.`} />
        <p className="small muted">민간소비 연간 증가율은 원자료 시계열을 직접 받지 못해 그래프로 그리지 않고 아래 비교표에 공표 값을 적었습니다.</p>
      </section>

      <section className="panel" id="st-2">
        <h2><span className="stepno">3</span> 소비 여력에 영향을 준 조건과 전달 과정 <span className="sub">화살표를 누르면 연결의 성격과 근거</span></h2>
        <div className="mech">
          {s.mechanism.edges.map((e, i) => (
            <button key={i} className={`mech-row k-${e.kind}${edge === i ? ' on' : ''}`} onClick={() => setEdge(edge === i ? null : i)}>
              <span className="mech-n">{nodeOf[e.from].label}<small>{nodeOf[e.from].sub}</small></span>
              <span className={`mech-a k-${e.kind}`}><span className={`lk k-${e.kind}`}>{KIND_KO[e.kind]}</span>→</span>
              <span className="mech-n">{nodeOf[e.to].label}<small>{nodeOf[e.to].sub}</small></span>
              <span className="mech-note">{e.note}</span>
            </button>
          ))}
        </div>
        {edge !== null && <div className="mech-ev"><p className="small"><span className={`lk k-${s.mechanism.edges[edge].kind}`}>{D.linkKo[s.mechanism.edges[edge].kind]}</span> {LINK_DESC[s.mechanism.edges[edge].kind]}</p><Claims ids={s.mechanism.edges[edge].claimIds} all /></div>}
        <p className="small muted">여러 조건이 동시에 소비에 작용합니다. 각 연결의 크기(얼마나 줄였나)는 인용한 연구가 있는 경우에만 적었습니다.</p>
      </section>

      <section className="panel" id="st-3">
        <h2><span className="stepno">4</span> 과거 여러 국면과 지금 — 같은 항목으로 비교 <span className="sub">칸을 누르면 근거 · 빈칸은 자료를 연결하지 않은 곳</span></h2>
        <div className="tbl-wrap"><table className="tbl cmp">
          <thead><tr><th>항목</th>{s.episodes.map((e) => <th key={e.id} className={e.current ? 'cur' : ''}>{e.label}<br /><span className="muted small">{e.years}</span></th>)}</tr></thead>
          <tbody>{s.rows.map((row) => (
            <tr key={row.item}><td><b>{row.item}</b></td>{s.episodes.map((e) => {
              const [txt] = row.cells[e.id] ?? [""];
              const k = `${row.item}|${e.id}`;
              return <td key={e.id} className={e.current ? 'cur' : ''}>{txt ? <button className="cellbtn" onClick={() => setCell(cell === k ? null : k)}>{txt}</button> : <span className="muted small">자료 연결 안 함</span>}</td>;
            })}</tr>
          ))}</tbody>
        </table></div>
        {cell && (() => { const [item, ep] = cell.split('|'); const row = s.rows.find((x) => x.item === item)!; return <div className="mech-ev"><p className="small"><b>{item} · {s.episodes.find((e) => e.id === ep)!.label}</b></p><Claims ids={row.cells[ep][1]} all /></div>; })()}
        <div className="two">
          <div><h3>지금과 같은 점</h3><ul className="plain synths">{s.same.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
          <div><h3>지금과 다른 점 — 비교 결과를 바꿀 수 있는 조건</h3><ul className="plain synths">{s.different.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
        </div>
        <p className="small muted">국면이 닮았다는 것은 원인과 이후 경로가 같다는 뜻이 아닙니다. 그래프 모양이 비슷한지가 아니라 같은 항목(원인·소득·물가·금리·부채·정책)으로 맞대어 봅니다.</p>
      </section>

      <section className="panel" id="st-4">
        <h2><span className="stepno">5</span> 조건별로 가능한 경로 <span className="sub">예측이 아닙니다 — 어떤 조건이면 어떤 과정이 작동하는지</span></h2>
        <div className="scen">
          {s.scenarios.map((x) => (
            <div key={x.id} className="scen-card">
              <h3>{x.name}</h3>
              <dl>
                <dt>성립 조건</dt><dd>{x.conditions}</dd>
                <dt>작동 과정</dt><dd>{x.path}</dd>
                <dt>영향받을 영역</dt><dd>{x.affected}</dd>
                <dt>시차·불확실성</dt><dd>{x.timing}</dd>
                <dt>성립하지 않게 되는 조건</dt><dd>{x.breaks}</dd>
              </dl>
              <details><summary className="small">이 시나리오의 근거 {x.basis.length}</summary><Claims ids={x.basis} all /></details>
            </div>
          ))}
        </div>
        <p className="small muted">시나리오마다 발생 확률을 붙이지 않았습니다. 확률을 계산할 근거가 없기 때문입니다. 실제로는 여러 경로가 동시에 작동할 수 있습니다.</p>
      </section>

      <section className="panel" id="st-5">
        <h2><span className="stepno">6</span> 앞으로 확인할 지표</h2>
        <div className="tbl-wrap"><table className="tbl">
          <thead><tr><th>지표</th><th>어디서·얼마나 자주</th><th>이렇게 움직이면 지지</th><th>이렇게 움직이면 약화</th><th>지금 값</th></tr></thead>
          <tbody>{s.watch.map((w) => (
            <tr key={w.name}><td><b>{w.name}</b></td><td className="small">{w.source}</td><td className="small">{w.supports}</td><td className="small">{w.weakens}</td>
              <td className="small">{w.claimIds.map((id) => D.claims[id]).filter(Boolean).map((c) => <span key={c.id} className="nowval">{c.support ?? c.period} <span className={`st s-${c.status}`}>{STATUS_SHORT[c.status]}</span></span>)}</td></tr>
          ))}</tbody>
        </table></div>
        <p className="small muted">수치 기준(몇 % 이상이면 위험 등)은 검증된 기준이 없어 정하지 않았습니다. 방향과 함께 다른 지표와 어긋나는지를 봅니다.</p>
        <h3>판단을 고쳐야 하는 신호</h3>
        <ul className="plain revise">{s.revise.map((x) => <li key={x}>{x}</li>)}</ul>
      </section>

      <section className="panel">
        <div className="two">
          <div><h2>다른 설명 가능성</h2><ul className="plain">{s.alternatives.map((x) => <li key={x}>{x}</li>)}</ul></div>
          <div><h2>이 분석의 한계</h2><ul className="plain gaps">{s.limits.map((x) => <li key={x}>{x}</li>)}</ul></div>
        </div>
        <h2>관련 변화 흐름</h2>
        <ul className="plain">{s.flows.map((f) => <li key={f}><button className="link" onClick={() => nav({ tab: 'flow', flow: f })}>{flowById[f].question}</button> <span className={`econ e-${flowById[f].econ.status}`}>{ECON_KO[flowById[f].econ.status]}</span></li>)}</ul>
      </section>

      <section className="panel">
        <h2>근거 문장 전체 <span className="sub">출처·원문 위치·적용 기간과 한계</span></h2>
        <details><summary>{allClaims.length}개 펼치기</summary><Claims ids={allClaims} all /></details>
      </section>
    </div>
  );
}

export { ERA_LABEL };
