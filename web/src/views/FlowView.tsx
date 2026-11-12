import { useState } from 'react';
import { D, ECON_KO, STATUS_SHORT, byId, evidenceCount, flowById, type Bridge, type Flow, type FlowLink, type FlowStep, type Indicator, type LinkKind } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine } from '../ui/Chart';
import { Claims } from '../ui/WhyPanel';
import { SBadge, StepNoteView } from '../ui/Story';
import { ConclusionView, FuturesView, TurnCard } from './TopicView';

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
  return (
    <button className="flowcard" onClick={() => nav({ tab: 'flow', flow: f.id, why: undefined, path: [] })}>
      <span className="fc-meta"><span className="fc-dom">{domainLabel(f.domain)} · {f.topic}</span><span className={`econ e-${f.econ.status}`}>{f.econ.status === 'linked' ? '경제 연결' : f.econ.status === 'partial' ? '일부 연결' : '맥락'}</span></span>
      <b className="fc-q">{f.question}</b>
      {!compact && <span className="fc-shape">{f.shape}</span>}
      <span className="fc-go">시대별로 읽기 →</span>
    </button>
  );
}

const domainLabel = (id: string) => D.domains.find((d) => d.id === id)?.label ?? id;
export const KIND_SHORT: Record<LinkKind, string> = { causal: '인과', condition: '조건', correlation: '상관', sequence: '순서·추론', interpretation: '해석', hypothesis: '가설', similar: '비교' };

/** 변화 흐름 지도 — 대분류(8) → 세부 흐름. 한 줄 = 한 주제의 일곱 시대. 칸 사이 표시 = 다음 시대로 넘어간 연결의 성격. */
function FlowList({ nav }: { nav: (p: Partial<Route>) => void }) {
  const [open, setOpen] = useState<string | null>(null);
  return (
    <div className="view">
      <section className="panel hero">
        <h2>변화 흐름 — 한 주제를 시대별로 끝까지</h2>
        <p className="lead">한 줄은 <b>같은 대상</b>을 1960년대부터 2020년대까지 따라갑니다. 칸 사이의 표시는 다음 시대로 <b>왜 넘어갔는지</b>의 성격입니다(인과·조건·상관·순서·해석). ‘순서’는 근거가 없어 시간 순서로만 이어 놓은 곳입니다.</p>
        <p className="small muted">분야를 누르면 그 안의 흐름이 펼쳐집니다. 줄을 누르면 시대별 근거와 연결고리를 읽습니다.</p>
      </section>
      <section className="panel">
        <div className="fmap-head"><span /> {D.eras.map((e) => <span key={e.id}>{e.label.replace('~현재', '')}</span>)}</div>
        {D.domains.map((d) => {
          const fs = D.flows.filter((f) => f.domain === d.id);
          const on = open === d.id || open === 'all';
          return (
            <div key={d.id} className={`fdom${on ? ' on' : ''}`}>
              <button className="fdom-h" aria-expanded={on} onClick={() => setOpen(on ? null : d.id)}><b>{d.label}</b> <span className="muted small">흐름 {fs.length}개 {on ? '▴' : '▾'}</span></button>
              {on && fs.map((f) => <FlowRow key={f.id} f={f} nav={nav} />)}
            </div>
          );
        })}
        <p><button className="link" onClick={() => setOpen(open === 'all' ? null : 'all')}>{open === 'all' ? '모두 접기' : '모든 분야 펼치기'}</button></p>
      </section>
      <HowToRead />
    </div>
  );
}

function FlowRow({ f, nav }: { f: Flow; nav: (p: Partial<Route>) => void }) {
  return (
    <div className="frow">
      <button className="frow-q" onClick={() => nav({ tab: 'flow', flow: f.id })}><b>{f.topic}</b><span>{f.question}</span><span className={`econ e-${f.econ.status}`}>{f.econ.status === 'linked' ? '경제 연결' : f.econ.status === 'partial' ? '일부 연결' : '맥락'}</span></button>
      <div className="frow-cells">
        {D.eras.map((e, i) => {
          const b = f.bridges[i - 1];
          return (
            <div key={e.id} className="frow-cell">
              {b ? <span className={`fbr k-${b.kind}`} title={`${D.linkKo[b.kind]} — ${b.note}`}>← {KIND_SHORT[b.kind]}</span> : <span className="fbr none" aria-hidden>시작</span>}
              <button className="fcell" onClick={() => nav({ tab: 'flow', flow: f.id, y: e.startYear })}><span className="fcell-e">{e.label.replace('~현재', '')}</span>{f.eraStates[e.id]}</button>
            </div>
          );
        })}
      </div>
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
  sequence: '앞뒤 순서는 자료로 확인, 이어진 이유는 이 사이트의 추론(출처의 주장 아님)',
  interpretation: '연구자·기관·작성자의 해석',
  hypothesis: '아직 검증되지 않은 설명',
  similar: '다른 시기의 닮은 일과 비교 — 영향 관계가 아님',
};

function FlowDetail({ f, r, nav, why }: { f: Flow; r: Route; nav: (p: Partial<Route>) => void; why: (id: string, from?: string) => void }) {
  const inds = f.indicators.map((id) => D.indicators.find((i) => i.id === id)).filter(Boolean) as Indicator[];
  const claimIds = [...new Set(f.steps.flatMap((s) => s.claimIds).concat(f.bridges.flatMap((b) => b.claimIds)))];
  const ev = evidenceCount(claimIds);
  const kinds = f.bridges.reduce((a, b) => ({ ...a, [b.kind]: (a[b.kind] ?? 0) + 1 }), {} as Record<string, number>);
  const go = (id: string) => { const el = document.getElementById(id); el?.closest('details')?.setAttribute('open', ''); el?.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
  const startEra = D.eras.find((e) => r.y >= e.startYear && r.y <= (e.endYear ?? 2026))?.id;
  return (
    <div className="view flow">
      <nav className="crumbline"><button className="link" onClick={() => nav({ flow: undefined })}>← 모든 흐름</button></nav>
      <section className="panel hero">
        <div className="eyebrow">{domainLabel(f.domain)} · {f.topic} <span className={`econ e-${f.econ.status}`}>{ECON_KO[f.econ.status]}</span></div>
        <h2>{f.question}</h2>
        {f.tracks && <p className="tp-tracks"><b>이 흐름이 계속 따라가는 것</b> {f.tracks}</p>}
        <p className="shape"><b>확인된 변화의 모양</b> {f.shape} <span className="muted small">(근거 문장을 묶은 작성자 정리)</span></p>
        {f.note && <p className="small muted">{f.note}</p>}
        <ol className="erabar" aria-label="시대별 모습">
          {D.eras.map((e, i) => {
            const b = f.bridges[i - 1];
            return (
              <li key={e.id} className={startEra === e.id ? 'on' : ''}>
                {b ? <span className={`fbr k-${b.kind}`} title={D.linkKo[b.kind]}>← {KIND_SHORT[b.kind]}</span> : <span className="fbr none" aria-hidden>시작</span>}
                <a href={`#era-${e.id}`} onClick={(ev2) => { ev2.preventDefault(); go(`era-${e.id}`); }}><span className="pb-ph">{e.label.replace('~현재', '')}</span><span className="pb-t">{f.eraStates[e.id]}</span></a>
              </li>
            );
          })}
        </ol>
        <p className="small muted">연결 {f.bridges.length}개: {Object.entries(kinds).map(([k, n]) => `${D.linkKo[k as LinkKind]} ${n}`).join(' · ')}. 근거 문장 {ev.total}개(두 곳 이상 확인 {ev.verified} · 한 곳 확인 {ev.sourced}).</p>
      </section>

      {f.turns && f.turns.length > 0 && (
        <section className="panel" id="fl-turns">
          <h2>전환점 이야기</h2>
          <p className="muted">각 전환점은 <b>그전 상태 → 새로 생긴 조건 → 사람·기업의 반응 → 구체적인 변화 → 다음에 남긴 것</b> 순서로 읽습니다. 앞 전환점이 남긴 것이 다음 전환점의 조건이 됩니다. 시대를 똑같이 나누지 않고, 실제로 방향이 바뀐 시점만 골랐습니다.</p>
          <ol className="tp-axis-list">{f.turns.map((tu) => <li key={tu.id}><button className="link" onClick={() => document.getElementById(`turn-${tu.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })}><b>{tu.years}</b> {tu.title}</button></li>)}</ol>
          {f.turns.map((tu, i) => <TurnCard key={tu.id} tu={tu} n={i + 1} />)}
        </section>
      )}

      {inds.length > 0 && (
        <section className="panel">
          <h2>숫자로 보는 장기 흐름</h2>
          {inds.map((ind) => <MiniIndicator key={ind.id} ind={ind} r={r} nav={nav} />)}
        </section>
      )}

      <details className="panel fl-evidence" id="fl-evidence" open={!f.turns?.length}>
        <summary><h2>근거 자료 — 시대별 단계와 연결 <span className="sub">위 이야기가 기댄 근거 문장과 시대 사이 연결의 성격(인과·조건·해석·순서)</span></h2></summary>
        <p className="muted small">앞 시대가 남긴 것이 다음 시대의 '새로 생긴 조건'이 됩니다. 조건 칸의 연결 성격은 연결 상자에 표시했습니다.</p>
        <ol className="eras-flow">
          {D.eras.map((e, i) => {
            const all = f.steps.filter((s) => s.era === e.id);
            const steps = all.filter((s) => !s.side);
            const sides = all.filter((s) => s.side);
            const b = f.bridges[i];
            return (
              <li key={e.id} id={`era-${e.id}`} className="era-sec">
                <h3><span className="era-tag">{e.label.replace('~현재', '')}</span> {f.eraStates[e.id]}</h3>
                <dl className="era-chain">
                  <dt>그전 상태</dt><dd>{i === 0 ? '이 흐름의 출발점입니다.' : f.eraStates[D.eras[i - 1].id]}</dd>
                </dl>
                {i > 0 && f.bridges[i - 1] && <BridgeBox b={f.bridges[i - 1]} />}
                <p className="era-ch-h">사람·기업의 반응과 구체적 변화</p>
                <ol className="steps">{steps.map((s, k) => <Step key={s.id} s={s} prev={steps[k - 1]} links={f.links.filter((l) => l.to === s.id)} f={f} why={why} nav={nav} />)}</ol>
                {sides.map((s) => <SideStep key={s.id} s={s} nav={nav} />)}
                {b && <p className="era-next small">다음에 남긴 것 → <a href={`#era-${b.to}`} onClick={(ev2) => { ev2.preventDefault(); go(`era-${b.to}`); }}>{D.eras.find((x) => x.id === b.to)?.label.replace('~현재', '')}의 '새로 생긴 조건'으로 이어집니다 ↓</a></p>}
              </li>
            );
          })}
        </ol>
      </details>

      <section className="panel econbox">
        <h2>경제 판단과의 관계</h2>
        <p><span className={`econ e-${f.econ.status}`}>{ECON_KO[f.econ.status]}</span> {f.econ.note}</p>
        {f.econ.analysis && <p><button className="btn" onClick={() => nav({ tab: 'now', study: f.econ.analysis, flow: undefined })}>이 흐름을 쓰는 분석: {D.studies.find((x) => x.id === f.econ.analysis)?.short} — 현재 비교·시나리오·지표 →</button></p>}
      </section>

      {f.futures && <FuturesView id="fl-future" f={f.futures} />}
      {f.conclusion && <ConclusionView id="fl-end" c={f.conclusion} />}

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
            <h2>다른 흐름과 만나는 곳</h2>
            <ul className="plain">{f.cross.map((x) => <li key={x.flow}><button className="link" onClick={() => nav({ flow: x.flow })}>{flowById[x.flow].question}</button> <span className="muted">— {x.note}</span></li>)}</ul>
          </div>
        </div>
      </section>
      <HowToRead />
    </div>
  );
}

const IND_LABEL: Record<string, string> = Object.fromEntries(((D.industries as { industries: { id: string; label: string }[] }).industries ?? []).map((i) => [i.id, i.label]));

/** 같은 시기에 있었지만 이 흐름의 추적 대상이 아닌 일 — 단계로 넣지 않고 연결만 둔다(R-Q3·R-Q5). */
function SideStep({ s, nav }: { s: FlowStep; nav: (p: Partial<Route>) => void }) {
  if (!s.side) return null;
  return (
    <aside className="side-step" id={`step-${s.id}`}>
      <p className="small"><b>같은 시기, 다른 대상</b> {s.period} {s.title}</p>
      <p className="small muted">{s.side.why}</p>
      <p>{s.side.go.map(([k, id]) => k === 'industry' && <button key={id} className="chip go" onClick={() => nav({ tab: 'field', cat: 'industry', ind: id, flow: undefined })}>{IND_LABEL[id] ?? id} 산업 일대기 →</button>)}</p>
    </aside>
  );
}

/** 직접 근거가 없는 연결의 이유 — 이 사이트의 추론임을 밝히고 다른 설명을 함께 둔다(R-A6). */
function InferBox({ t, alt }: { t: string; alt?: string }) {
  return (
    <div className="infer-box">
      <p><SBadge l="inference" /> <b>왜 이어졌다고 보나</b> {t}</p>
      {alt && <p className="small muted"><b>다른 설명</b> {alt}</p>}
    </div>
  );
}

function BridgeBox({ b }: { b: Bridge }) {
  const nextLabel = D.eras.find((e) => e.id === b.to)?.label.replace('~현재', '');
  return (
    <div className={`ebridge k-${b.kind}`}>
      <span className="conn-arrow" aria-hidden>↓</span>
      <div>
        <p className="bridge-h">새로 생긴 조건 — 앞 시대에서 {nextLabel}로 넘어온 연결 <span className={`lk k-${b.kind}`}>{D.linkKo[b.kind]}</span>{b.change && <span className="chg">앞뒤 관계: {b.change}</span>}</p>
        <p>{b.note}</p>
        {b.infer && <InferBox t={b.infer} alt={b.inferAlt} />}
        {b.claimIds.length > 0 && <details className="conn-ev"><summary>앞뒤 사실의 근거 {b.claimIds.length}</summary><Claims ids={b.claimIds} all /></details>}
      </div>
    </div>
  );
}

function Step({ s, prev, links, f, why, nav }: { s: FlowStep; prev?: FlowStep; links: FlowLink[]; f: Flow; why: (id: string, from?: string) => void; nav: (p: Partial<Route>) => void }) {
  return (
    <li id={`step-${s.id}`} className={`step ph-${s.phase}`}>
      {links.filter((l) => prev && l.from === prev.id).map((l) => (
        <div key={l.from + l.to} className={`conn k-${l.kind}`}>
          <span className="conn-arrow" aria-hidden>↓</span>
          <span><span className={`lk k-${l.kind}`}>{D.linkKo[l.kind]}</span> {l.note}</span>
          {l.infer && <InferBox t={l.infer} alt={l.inferAlt} />}
          {l.claimIds.length > 0 && <details className="conn-ev"><summary>이 연결의 근거 {l.claimIds.length}</summary><Claims ids={l.claimIds} all /></details>}
        </div>
      ))}
      <div className="step-card">
        <div className="step-h"><span className={`phase ph-${s.phase}`}>{D.phaseKo[s.phase]}</span><span className="step-y">{s.period}</span>{s.measure && <span className="measure" title="이 자료가 실제로 재는 것">자료가 재는 것: {s.measure}</span>}</div>
        <h4>{s.title}</h4>
        {s.claimIds.length ? <Claims ids={s.claimIds} all /> : <p className="empty">자료 없음 — {s.empty}</p>}
        {s.nodeIds.length > 0 && (
          <p className="step-ev">사건 상세: {s.nodeIds.map((id) => byId[id] && <button key={id} className="chip" onClick={() => why(id, f.id)}>{byId[id].year} {byId[id].label} →</button>)}</p>
        )}
        <StepNoteView flow={f.id} step={s.id} nav={nav} />
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
