import { CAT_SHORT, D, STATUS_SHORT, byId, evidenceCount, flowById, type Flow, type FlowLink, type FlowStep, type Indicator, type LinkKind } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine } from '../ui/Chart';
import { Claims } from '../ui/WhyPanel';

/**
 * 변화 흐름 — 질문 하나를 중심으로 '이전 → 조건 → 전환점 → 확산 → 생활 변화 → 지금'을 잇는다.
 * 핵심 설명(근거 문장)은 클릭 없이 바로 보이고, 사건을 누르면 사건 상세(근거·원인·결과)로 간다.
 * 단계 사이 연결은 인과·조건·상관·시간 순서·해석·가설 중 무엇인지 글자로 적는다.
 */
const MULTI = ['#c2410c', '#1d4ed8', '#047857', '#a21caf', '#b45309', '#0e7490'];

export function FlowView({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const f = r.flow ? flowById[r.flow] : undefined;
  if (!f) return <FlowList nav={nav} />;
  return <FlowDetail f={f} r={r} nav={nav} why={why} />;
}

export function FlowCard({ f, nav, compact }: { f: Flow; nav: (p: Partial<Route>) => void; compact?: boolean }) {
  const claimIds = [...new Set(f.steps.flatMap((s) => s.claimIds))];
  const ev = evidenceCount(claimIds);
  return (
    <button className="flowcard" onClick={() => nav({ tab: 'flow', flow: f.id, why: undefined, path: [] })}>
      <span className="fc-meta">{f.cats.map((c) => <span key={c} className={`fc-cat c-${c}`}><span className={`cdot c-${c}`} />{CAT_SHORT[c]}</span>)}<span>{f.span[0]}–{f.span[1]}</span></span>
      <b className="fc-q">{f.question}</b>
      {!compact && <span className="fc-shape">{f.shape}</span>}
      <span className="fc-foot">단계 {f.steps.length}개 · 근거 문장 {ev.total}개(두 곳 이상 확인 {ev.verified}) · 미확인 {f.gaps.length}건 <span className="fc-go">읽기 →</span></span>
    </button>
  );
}

function FlowList({ nav }: { nav: (p: Partial<Route>) => void }) {
  return (
    <div className="view">
      <section className="panel hero">
        <h2>질문으로 읽는 변화</h2>
        <p className="lead">사건을 시간순으로 늘어놓는 대신, 질문 하나를 놓고 <b>이전에는 어땠고 → 어떤 조건에서 → 무엇이 계기가 되어 → 누구에게 퍼졌고 → 생활이 어떻게 달라졌으며 → 지금 무엇이 이어지는지</b>를 근거와 함께 따라갑니다.</p>
        <div className="flowgrid">{D.flows.map((f) => <FlowCard key={f.id} f={f} nav={nav} />)}</div>
      </section>
      <HowToRead />
    </div>
  );
}

export function HowToRead() {
  return (
    <section className="panel howto">
      <h2>표시를 읽는 법</h2>
      <div className="two">
        <div>
          <h3>문장 하나의 확인 수준</h3>
          <ul className="plain">
            <li><span className="st s-verified">{STATUS_SHORT.verified}</span> 서로 다른 발행처·원자료 두 곳 이상이 같은 내용을 담고 있음. 같은 발표를 옮긴 기사 여러 개는 한 곳으로 셉니다.</li>
            <li><span className="st s-sourced">{STATUS_SHORT.sourced}</span> 출처 한 곳(공식 통계 원자료 포함)에서 확인.</li>
            <li><span className="st s-needs_source">{STATUS_SHORT.needs_source}</span> 아직 근거를 찾지 못한 가설. 사실로 쓰지 않습니다.</li>
          </ul>
          <p className="small muted">확인 수준은 문장의 내용에 대한 것입니다. 그 문장이 다른 변화의 '원인'이라는 뜻은 아닙니다.</p>
        </div>
        <div>
          <h3>단계 사이 연결의 성격</h3>
          <ul className="plain">
            {(Object.keys(D.linkKo) as LinkKind[]).map((k) => <li key={k}><span className={`lk k-${k}`}>{D.linkKo[k]}</span> {LINK_DESC[k]}</li>)}
          </ul>
        </div>
      </div>
    </section>
  );
}

export const LINK_DESC: Record<LinkKind, string> = {
  causal: '앞의 일이 뒤의 일을 낳았다는 것을 자료가 직접 보여줌',
  condition: '앞의 일이 뒤의 일이 가능해진 배경·조건이었음(유일한 원인은 아님)',
  correlation: '두 흐름이 함께 움직였지만 원인 관계는 확인하지 않음',
  sequence: '앞뒤 순서만 맞음 — 인과를 주장하지 않음',
  interpretation: '연구자·기관·작성자의 해석',
  hypothesis: '아직 검증되지 않은 설명',
};

function FlowDetail({ f, r, nav, why }: { f: Flow; r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const stepById = Object.fromEntries(f.steps.map((s) => [s.id, s]));
  const inds = f.indicators.map((id) => D.indicators.find((i) => i.id === id)).filter(Boolean) as Indicator[];
  const phases = [...new Set(f.steps.map((s) => s.phase))];
  return (
    <div className="view flow">
      <nav className="crumbline"><button className="link" onClick={() => nav({ flow: undefined })}>← 모든 질문</button></nav>
      <section className="panel hero">
        <div className="eyebrow">{f.cats.map((c) => <span key={c} className={`fc-cat c-${c}`}><span className={`cdot c-${c}`} />{CAT_SHORT[c]}</span>)} {f.span[0]}–{f.span[1]}</div>
        <h2>{f.question}</h2>
        <p className="shape"><b>변화의 모양</b> {f.shape} <span className="muted small">(여러 근거를 묶은 작성자 정리)</span></p>
        <div className="lede"><h3>먼저 보는 근거</h3><Claims ids={f.lede} all /></div>
        <ol className="phasebar" aria-label="이 흐름의 단계">
          {f.steps.map((s) => (
            <li key={s.id} className={`ph-${s.phase}`}><a href={`#step-${s.id}`} onClick={(e) => { e.preventDefault(); document.getElementById(`step-${s.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }}>
              <span className="pb-ph">{D.phaseKo[s.phase]}</span><span className="pb-y">{s.period}</span><span className="pb-t">{s.title}</span></a></li>
          ))}
        </ol>
        <p className="small muted">이 흐름에 있는 단계: {phases.map((p) => D.phaseKo[p]).join(' · ')}. 모든 흐름에 같은 단계를 억지로 채우지 않습니다.</p>
      </section>

      {inds.length > 0 && (
        <section className="panel">
          <h2>숫자로 보는 장기 흐름</h2>
          {inds.map((ind) => <MiniIndicator key={ind.id} ind={ind} r={r} nav={nav} />)}
        </section>
      )}

      <section className="panel">
        <h2>단계별로 따라가기</h2>
        <ol className="steps">
          {f.steps.map((s, i) => <Step key={s.id} s={s} prev={f.steps[i - 1]} links={f.links.filter((l) => l.to === s.id)} stepById={stepById} f={f} why={why} />)}
        </ol>
      </section>

      <section className="panel">
        <div className="two">
          <div>
            <h2>확인되지 않은 부분</h2>
            <p className="small muted">자료를 찾지 못했다는 뜻이며, 그런 일이 없었다는 뜻이 아닙니다.</p>
            <ul className="plain gaps">{f.gaps.map((g) => <li key={g}>{g}</li>)}</ul>
          </div>
          <div>
            <h2>다른 설명 가능성</h2>
            <ul className="plain">{f.alternatives.map((a) => <li key={a}>{a}</li>)}</ul>
            <h2>다른 흐름과의 연결</h2>
            <ul className="plain">{f.cross.map((x) => <li key={x.flow}><button className="link" onClick={() => nav({ flow: x.flow })}>{flowById[x.flow].question}</button> <span className="muted">— {x.note}</span></li>)}</ul>
          </div>
        </div>
      </section>
      <HowToRead />
    </div>
  );
}

function Step({ s, prev, links, stepById, f, why }: { s: FlowStep; prev?: FlowStep; links: FlowLink[]; stepById: Record<string, FlowStep>; f: Flow; why: (id: string, from?: string) => void }) {
  const fromPrev = links.some((l) => prev && l.from === prev.id);
  return (
    <li id={`step-${s.id}`} className={`step ph-${s.phase}`}>
      {links.map((l) => (
        <div key={l.from + l.to} className={`conn k-${l.kind}`}>
          <span className="conn-arrow" aria-hidden>↓</span>
          <span><span className={`lk k-${l.kind}`}>{D.linkKo[l.kind]}</span>{prev && l.from !== prev.id && <span className="muted"> ‘{stepById[l.from].title}’에서</span>} {l.note}</span>
          {l.claimIds.length > 0 && <details className="conn-ev"><summary>이 연결의 근거 {l.claimIds.length}</summary><Claims ids={l.claimIds} all /></details>}
        </div>
      ))}
      {prev && !fromPrev && links.length === 0 && (
        <div className="conn k-none"><span className="conn-arrow" aria-hidden>↓</span><span className="muted small">앞 단계와의 연결은 확인된 근거가 없어 시간 순서로만 놓았습니다.</span></div>
      )}
      <div className="step-card">
        <div className="step-h"><span className={`phase ph-${s.phase}`}>{D.phaseKo[s.phase]}</span><span className="step-y">{s.period}</span></div>
        <h3>{s.title}</h3>
        {s.claimIds.length ? <Claims ids={s.claimIds} all /> : <p className="empty">자료 없음 — {s.empty}</p>}
        {s.nodeIds.length > 0 && (
          <p className="step-ev">사건 상세: {s.nodeIds.map((id) => byId[id] && <button key={id} className="chip" onClick={() => why(id, f.id)}>{byId[id].year} {byId[id].label} →</button>)}</p>
        )}
      </div>
    </li>
  );
}

function MiniIndicator({ ind, r, nav }: { ind: Indicator; r: Route; nav: (p: Partial<Route>) => void }) {
  const ser = ind.series.filter((s) => ind.multi || s.country === 'KR').map((s, i) => ({
    key: s.label, label: s.label, color: ind.multi ? MULTI[i % MULTI.length] : 'var(--c-economy)',
    points: s.points.map(([t, v]) => [Number(t.slice(0, 4)), v] as [number, number]),
  }));
  return (
    <div className="mini-ind">
      <h3>{ind.title} <span className="sub">{ind.unit}</span></h3>
      <Chart ariaLabel={`${ind.title} 장기 추이`} unit={ind.unit} year={r.y} onPick={(y) => nav({ y })} series={ser} height={220} log={!!ind.log} />
      <div className="legend">{ser.map((x) => <span key={x.key}><i className="lg-line" style={{ background: x.color }} />{x.label}</span>)}</div>
      <SourceLine ids={ind.series.flatMap((s) => s.sourceIds)} extra={ind.note} />
    </div>
  );
}
