import { useState } from 'react';
import { D, flowById, type Layer, type TasteFlow, type TR } from '../lib/data';
import type { Route } from '../lib/route';
import { Claims } from '../ui/WhyPanel';
import { ConclusionView, FuturesView, TurnCard } from './TopicView';
import { LayerLegend } from '../ui/Story';

/**
 * 취향·생활 흐름 — 사람들이 무엇을 좋아하고 사다가, 어떤 조건·불편을 만나 다른 선택으로 옮겨 갔는지.
 * 문장마다 층위(확인된 사실 / 출처의 해석 / AI 종합 추론 / 탐색·전망 가설)를 붙이고,
 * 갈래(선택지)를 공통 시간축 위에 놓아 교체·공존·분화·재등장이 보이게 한다.
 */
const T = D.tastes;
type Eff = 'fact' | 'source' | 'mixed' | 'inference' | 'hypothesis';
const EFF_KO: Record<Eff, string> = { fact: '사실', source: '출처 해석', mixed: '사실·해석', inference: 'AI 추론', hypothesis: '가설' };
const EFF_HELP: Record<Eff, string> = {
  fact: '자료에서 직접 확인한 사실', source: '연구자·기관·업계·기자의 해석(출처가 한 말)', mixed: '사실과 출처의 해석이 섞인 문장',
  inference: 'AI 종합 추론 — 이 사이트가 여러 사실을 이어 제안하는 설명(출처의 주장이 아님)', hypothesis: '탐색·전망 가설 — 추가 확인이 필요',
};
const STATE_KO: Record<string, string> = { deep: '깊게 구현', scoped: '범위를 좁혀 구현', eras: '시대 흐름만 있음', candidate: '후보(조사 전)' };

/** claim 층위는 근거 문장의 종류(사실/해석)로 표시를 정한다 */
export function effLayer(layer: Layer, ids: string[]): Eff {
  if (layer === 'inference' || layer === 'hypothesis') return layer;
  if (layer === 'fact') return 'fact';
  if (layer === 'source') return 'source';
  const types = new Set(ids.map((i) => D.claims[i]?.claimType).filter(Boolean));
  if (types.size === 1 && types.has('interpretation')) return 'source';
  if (types.has('interpretation')) return 'mixed';
  return 'fact';
}

export function LayerBadge({ l }: { l: Eff }) {
  return <span className={`lyr l-${l}`} title={EFF_HELP[l]}>{EFF_KO[l]}</span>;
}

function Reason({ x }: { x: TR }) {
  return (
    <dl className="reason">
      {x.logic && <><dt>연결 논리</dt><dd>{x.logic}</dd></>}
      {x.alt && <><dt>다른 설명</dt><dd>{x.alt}</dd></>}
      {x.scope && <><dt>적용 범위</dt><dd>{x.scope}</dd></>}
      {x.test && <><dt>강해지거나 약해지는 신호</dt><dd>{x.test}</dd></>}
    </dl>
  );
}

/** 한 문장 + 층위 표시 + (펼치면) 근거와 다른 설명 */
function Line({ x, tag = 'p' }: { x: TR; tag?: 'p' | 'li' }) {
  const [open, setOpen] = useState(false);
  const l = effLayer(x.layer, x.basis);
  const reasoned = l === 'inference' || l === 'hypothesis';
  const body = (
    <>
      <span className="tl-t"><LayerBadge l={l} /> {x.text} <button className="link small" onClick={() => setOpen(!open)}>{open ? '접기' : reasoned ? '근거·다른 설명' : `근거 ${x.basis.length}`}</button></span>
      {open && reasoned && <Reason x={x} />}
      {open && <Claims ids={x.basis} all />}
    </>
  );
  return tag === 'li' ? <li className={`tl l-${l}`}>{body}</li> : <div className={`tl l-${l}`}>{body}</div>;
}

function Ids({ ids, label }: { ids: string[]; label?: string }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button className="link small" onClick={() => setOpen(!open)}>{open ? '접기' : label ?? `근거 ${ids.length}`}</button>
      {open && <Claims ids={ids} all />}
    </>
  );
}

function Legend() {
  return (
    <div className="lyr-legend">
      {(['fact', 'source', 'inference', 'hypothesis'] as Eff[]).map((l) => <span key={l}><LayerBadge l={l} /> {EFF_HELP[l]}</span>)}
    </div>
  );
}

export function TasteView({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void }) {
  const f = r.taste ? T.flows.find((x) => x.id === r.taste) : undefined;
  return f ? <TasteDetail f={f} nav={nav} /> : <TasteLanding nav={nav} />;
}

const flowTitle = (id: string) => T.flows.find((f) => f.id === id)?.title ?? id;

function TasteLanding({ nav }: { nav: (p: Partial<Route>) => void }) {
  const cnt = (s: string) => T.fields.filter((f) => f.state === s).length;
  return (
    <div className="view taste">
      <section className="panel hero" id="tz-hero">
        <h2>무엇을 좋아하고 사다가, 왜 다른 것을 고르게 됐나</h2>
        <p className="lead">연도와 사건보다 <b>선택이 옮겨 가는 과정</b>을 봅니다. 무엇이 인기였고 어떤 만족을 줬는지 → 무엇이 달라졌는지 → 왜 다른 선택이 매력적이었는지 → 기존 선택과 어떻게 함께 남았는지 → 지금 남은 불편이 어떤 다음 수요로 이어질 수 있는지.</p>
        <Legend />
        <p className="muted small">'AI 추론'과 '가설'은 출처가 직접 주장한 내용이 아닙니다. 펼치면 근거 문장, 연결 논리, 다른 설명, 적용 범위, 확인할 신호가 나옵니다.</p>
      </section>

      <section className="panel" id="tz-flows">
        <h2>분석한 흐름 <span className="sub">{T.flows.length}개 — 모두 같은 구조(갈래·단계·연결·조건 사슬·집단·공존·미래)</span></h2>
        <div className="tz-cards">
          {T.flows.map((f) => (
            <button key={f.id} className="tz-card" onClick={() => nav({ taste: f.id })}>
              <span className="tz-field">{T.fields.find((x) => x.id === f.field)?.label} · {f.status}</span>
              <b>{f.title}</b>
              <span className="tz-q">{f.question}</span>
              {f.scene && <span className="tz-scene">{f.scene.text}</span>}
              <span className="muted small">{f.span[0]}~{f.span[1]} · 갈래 {f.lanes.length} · 연결 {f.moves.length}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="panel" id="tz-fields">
        <h2>12개 분야 지도 <span className="sub">진행 상태를 숨기지 않습니다 — 깊게 {cnt('deep')} · 범위 좁혀 {cnt('scoped')} · 시대 흐름만 {cnt('eras')} · 후보 {cnt('candidate')}</span></h2>
        <p className="muted small">'시대 흐름만 있음'은 시대별 탐색의 흐름(연도·사건 중심)만 있고, 이 화면의 취향 구조(무엇이 인기→왜 바뀌었나)는 아직 적용하지 않았다는 뜻입니다. 이 지도 자체도 완성된 틀이 아니라 작업 목록입니다.</p>
        <div className="tz-fieldgrid">
          {T.fields.map((fd) => (
            <div key={fd.id} className={`tz-fd st-${fd.state}`}>
              <p><b>{fd.label}</b> <span className={`tz-state st-${fd.state}`}>{STATE_KO[fd.state]}</span></p>
              <p className="small">{fd.topics.join(' · ')}</p>
              <p className="small muted">{fd.note}</p>
              <p className="small">
                {fd.flows.map((id) => <button key={id} className="link" onClick={() => nav({ taste: id })}>{flowTitle(id)} →</button>)}
                {(fd.eraFlows ?? []).filter((id) => flowById[id]).map((id) => <button key={id} className="link muted" onClick={() => nav({ tab: 'flow', flow: id, taste: undefined })}>시대 흐름: {flowById[id].topic || flowById[id].question}</button>)}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="panel" id="tz-needs">
        <h2>분야를 가로지르는 욕구 <span className="sub">같은 이름의 욕구라도 분야마다 다른 물건·행동으로 나타난다</span></h2>
        {T.needs.map((n) => (
          <div key={n.id} className="tz-need">
            <h3>{n.label}</h3>
            <ul className="tz-cases">
              {n.cases.map((c, i) => (
                <li key={i}><button className="link" onClick={() => nav({ taste: c.flow })}>{flowTitle(c.flow)}</button> — {c.how} <Ids ids={c.claims} /></li>
              ))}
            </ul>
            <Line x={n.compare} />
          </div>
        ))}
        <p className="muted small">편의성·가성비 같은 욕구는 각 흐름 안에 흩어져 있고 아직 따로 비교하지 않았습니다.</p>
      </section>
    </div>
  );
}

const SECTIONS = [
  ['tz-1', '갈래와 시간축'], ['tz-2', '무엇이 인기였나'], ['tz-3', '무엇이 달라졌나'], ['tz-4', '조건 사슬'],
  ['tz-5', '비교'], ['tz-6', '누가 무엇을'], ['tz-7', '다음 수요'], ['tz-end', '결론'], ['tz-8', '조사 기록'],
] as const;

function TasteDetail({ f, nav }: { f: TasteFlow; nav: (p: Partial<Route>) => void }) {
  const [sel, setSel] = useState<number | null>(null);
  const laneName = (id: string) => f.lanes.find((l) => l.id === id)?.label ?? id;
  return (
    <div className="view taste">
      <section className="panel hero" id="tz-0">
        <button className="link small" onClick={() => nav({ taste: undefined })}>← 취향·생활 흐름 전체</button>
        <LayerLegend />
        <p className="tz-field">{T.fields.find((x) => x.id === f.field)?.label} · {f.status} · {f.span[0]}~{f.span[1]}</p>
        <h2 className="st-title">{f.title}</h2>
        <p className="st-sub">{f.subtitle}</p>
        <p className="tz-question">{f.question}</p>
        {f.scene && <Line x={f.scene} />}
        <nav className="tz-nav">{SECTIONS.filter(([id]) => id !== 'tz-5' || f.contrast || f.outfits).map(([id, t]) => <a key={id} href={`#${id}`} onClick={(e) => { e.preventDefault(); document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' }); }}>{t}</a>)}</nav>
        <Legend />
      </section>

      {f.turns && f.turns.length > 0 && (
        <section className="panel" id="tz-turns">
          <h2>전환점 이야기</h2>
          <p className="muted">각 전환점은 <b>그전 상태 → 새로 생긴 조건 → 사람·기업의 반응 → 구체적인 변화 → 다음에 남긴 것</b> 순서로 읽습니다. 아래 갈래 시간축·조건 사슬·비교는 이 이야기의 근거를 다른 모양으로 보여 줍니다.</p>
          {f.turns.map((tu, i) => <TurnCard key={tu.id} tu={tu} n={i + 1} />)}
        </section>
      )}

      <section className="panel" id="tz-1">
        <h2>갈래와 시간축 <span className="sub">같은 시기에 여러 선택이 함께 있다 — 화살표는 선택이 옮겨 가거나 갈라진 지점</span></h2>
        <Timeline f={f} sel={sel} setSel={setSel} />
        <PhaseLegend />
        <ol className="tz-moves">
          {f.moves.map((m, i) => (
            <li key={i} className={sel === i ? 'on' : ''}>
              <p><span className="mvn">{i + 1}</span> <b>{laneName(m.from)} → {laneName(m.to)}</b> <span className={`rel r-${m.rel}`}>{T.rels[m.rel]}</span> <span className="muted small">{m.year}년 무렵</span></p>
              <p className="tz-why">{m.why}</p>
              <button className="link small" onClick={() => setSel(sel === i ? null : i)}>{sel === i ? '접기' : '왜 그렇게 보나 — 근거와 다른 설명'}</button>
              {sel === i && <div className="tz-reason"><Line x={m.reason} /><Reason x={m.reason} /></div>}
            </li>
          ))}
        </ol>
      </section>

      <section className="panel" id="tz-2">
        <h2>무엇이 인기였고, 왜 좋아했나 <span className="sub">대표 상품·쓰는 모습·인기 신호(신호 종류를 나눠 표시)</span></h2>
        <div className="tz-stages">
          {f.stages.map((s, i) => (
            <article key={i} className="tz-stage">
              <p className="tz-field">{laneName(s.lane)} · {s.period}</p>
              <h3>{s.title}</h3>
              <ul className="tz-items">{s.items.map((it) => <li key={it}>{it}</li>)}</ul>
              <p className="small"><b>왜 좋아했나</b></p>
              <Line x={s.appeal} />
              <p className="small"><b>누가</b> {s.who} · <b>어디서</b> {s.where}</p>
              <ul className="tz-sigs">
                {s.signals.map(([k, t, ids], j) => <li key={j}><span className={`sig g-${k}`}>{T.signals[k] ?? k}</span> {t} <Ids ids={ids} label="출처" /></li>)}
              </ul>
            </article>
          ))}
        </div>
        <p className="muted small">검색·SNS·보도는 관심의 신호이지 판매가 아닙니다. 판매·거래액 신호가 없는 단계는 '많이 팔렸다'고 쓰지 않았습니다.</p>
      </section>

      <section className="panel" id="tz-3">
        <h2>무엇이 달라졌고, 왜 다른 선택이 매력적이었나</h2>
        <ul className="tz-lanes">
          {f.lanes.map((l) => (
            <li key={l.id}><b>{l.label}</b> <span className="muted small">{l.desc}</span> — {l.segs.map((s) => `${s[0]}~${s[1]} ${T.phases[s[2]]}${s[3] ? `(${s[3]})` : ''}`).join(' → ')} <Ids ids={l.claims} /></li>
          ))}
        </ul>
        {f.coexist.length > 0 && <>
          <h3>함께 남은 선택 — 공존 질문</h3>
          {f.coexist.map((c, i) => <div key={i} className="tz-co"><p className="tz-question small">{c.q}</p><Line x={c.a} /></div>)}
        </>}
      </section>

      <section className="panel" id="tz-4">
        <h2>조건 사슬 <span className="sub">조건 → 제약·기회 → 욕구·기준 → 행동 → 공급 대응 → 새 불편</span></h2>
        {f.chains.map((ch, i) => (
          <div key={i} className="tz-chain">
            <h3>{ch.title}</h3>
            <ol>
              {ch.steps.map(([lv, t, layer, ids], j) => (
                <li key={j}><span className="lv">{lv}</span> <LayerBadge l={effLayer(layer, ids)} /> {t} <Ids ids={ids} /></li>
              ))}
            </ol>
          </div>
        ))}
      </section>

      {(f.contrast || f.outfits) && (
        <section className="panel" id="tz-5">
          {f.contrast && <>
            <h2>{f.contrast.title}</h2>
            <div className="tablewrap"><table className="tz-table">
              <thead><tr><th>기준</th><th>{f.contrast.a}</th><th>{f.contrast.b}</th><th>층위</th></tr></thead>
              <tbody>{f.contrast.rows.map((r) => (
                <tr key={r.dim}><th>{r.dim}</th><Cell v={r.a} ai={r.aiCells?.includes('a')} /><Cell v={r.b} ai={r.aiCells?.includes('b')} /><td><LayerBadge l={effLayer(r.layer, r.basis)} /> <Ids ids={r.basis} />{r.aiWhy && <AiWhy t={r.aiWhy} />}</td></tr>
              ))}</tbody>
            </table></div>
            <p className="muted small">{f.contrast.note}</p>
          </>}
          {f.outfits && <>
            <h2>바지와 함께 입은 것 <span className="sub">자료가 없는 칸은 AI 추론으로 채우고 표시함</span></h2>
            <div className="tablewrap"><table className="tz-table">
              <thead><tr><th>시기</th><th>바지</th><th>상의</th><th>신발</th><th>근거</th></tr></thead>
              <tbody>{f.outfits.map((o) => (
                <tr key={o.period}><th>{o.period}</th><Cell v={o.pants} ai={o.aiCells?.includes('pants')} /><Cell v={o.top} ai={o.aiCells?.includes('top')} /><Cell v={o.shoes} ai={o.aiCells?.includes('shoes')} /><td><Ids ids={o.basis} />{o.aiWhy && <AiWhy t={o.aiWhy} />}</td></tr>
              ))}</tbody>
            </table></div>
          </>}
        </section>
      )}

      <section className="panel" id="tz-6">
        <h2>누가 무엇을 골랐나 <span className="sub">같은 시기, 집단마다 다른 선택</span></h2>
        <ul className="tz-segs">
          {f.segments.map((s, i) => <li key={i}><b>{s.group}</b> — {s.choice} <LayerBadge l={effLayer(s.layer, s.claims)} /> <Ids ids={s.claims} /></li>)}
        </ul>
      </section>

      <section className="panel" id="tz-7">
        <h2>남은 불편과 다음 수요 <span className="sub">하나의 예측이 아니라 조건별 여러 방향</span></h2>
        <div className="tz-future">
          <div><h3>채워진 욕구</h3>{f.future.satisfied.map((x, i) => <Line key={i} x={x} />)}</div>
          <div><h3>남은 불편</h3>{f.future.discomforts.map((x, i) => <Line key={i} x={x} />)}</div>
          <div><h3>채워지지 않은 욕구</h3>{f.future.unmet.map((x, i) => <Line key={i} x={x} />)}</div>
        </div>
        {f.futures && <FuturesView id="tz-7f" f={f.futures} title="조건별로 갈라지는 다음 수요" />}
      </section>

      {f.conclusion && <ConclusionView id="tz-end" c={f.conclusion} />}

      <section className="panel" id="tz-8">
        <h2>조사 기록</h2>
        <dl className="reason">
          <dt>찾아본 것</dt><dd>{f.research.searched}</dd>
          <dt>찾지 못한 것</dt><dd>{f.research.missing}</dd>
          <dt>확인할 곳</dt><dd>{f.research.check}</dd>
        </dl>
      </section>
    </div>
  );
}

function Cell({ v, ai }: { v: string; ai?: boolean }) {
  return <td className={ai ? 'ai-cell' : ''}>{ai && <LayerBadge l="inference" />} {v}</td>;
}
function AiWhy({ t }: { t: string }) {
  const [open, setOpen] = useState(false);
  return <><br /><button className="link small" onClick={() => setOpen(!open)}>{open ? '접기' : 'AI 추론의 근거'}</button>{open && <p className="small muted">{t}</p>}</>;
}

const PH = ['emerge', 'spread', 'main', 'saturate', 'transform', 'revive', 'niche'];
function PhaseLegend() {
  return <p className="ph-legend">{PH.map((p) => <span key={p}><i className={`ph ph-${p}`} /> {T.phases[p]}</span>)} <span className="muted small">빈 칸은 '없었다'가 아니라 그 시기 자료를 연결하지 못했다는 뜻</span></p>;
}

function Timeline({ f, sel, setSel }: { f: TasteFlow; sel: number | null; setSel: (i: number | null) => void }) {
  const W = 920, L = 150, R = 12, top = 22, rowH = 34;
  const [a, b] = f.span;
  const x = (y: number) => L + ((y - a) / (b - a)) * (W - L - R);
  const H = top + f.lanes.length * rowH + 8;
  const row = (id: string) => f.lanes.findIndex((l) => l.id === id);
  const cy = (i: number) => top + i * rowH + rowH / 2;
  const step = b - a > 20 ? 5 : b - a > 10 ? 2 : 1;
  const ticks: number[] = [];
  for (let y = Math.ceil(a / step) * step; y <= b; y += step) ticks.push(y);
  return (
    <div className="tz-tlwrap">
      <svg className="tz-tl" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${f.title} 갈래별 국면과 이동`}>
        <defs>
          <marker id={`ar-${f.id}`} viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" className="ar" /></marker>
        </defs>
        {ticks.map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={top - 4} y2={H - 6} className="tick" /><text x={x(t)} y={12} className="tickl" textAnchor="middle">{t}</text></g>)}
        {f.lanes.map((l, i) => (
          <g key={l.id}>
            <text x={L - 8} y={cy(i) + 4} textAnchor="end" className="lanel">{l.label.length > 11 ? l.label.slice(0, 11) + '…' : l.label}<title>{l.label} — {l.desc}</title></text>
            <line x1={L} x2={W - R} y1={cy(i)} y2={cy(i)} className="laneline" />
            {l.segs.map(([s, e, ph, lab], j) => {
              const w = x(e) - x(s);
              return (
                <g key={j}>
                  <rect x={x(s) + 1} y={cy(i) - 11} width={Math.max(w - 2, 3)} height={22} rx={4} className={`ph ph-${ph}`}><title>{`${l.label} ${s}~${e}: ${T.phases[ph]}${lab ? ` — ${lab}` : ''}`}</title></rect>
                  {w > 54 && <text x={x(s) + 6} y={cy(i) + 4} className="segl">{T.phases[ph]}</text>}
                </g>
              );
            })}
          </g>
        ))}
        {f.moves.map((m, i) => {
          const r1 = row(m.from), r2 = row(m.to);
          if (r1 < 0 || r2 < 0) return null;
          const xx = x(Math.min(Math.max(m.year, a), b));
          const y1 = cy(r1) + (r2 > r1 ? 11 : -11), y2 = cy(r2) + (r2 > r1 ? -11 : 11);
          const d = `M${xx},${y1} C${xx + 26},${(y1 + y2) / 2} ${xx + 26},${(y1 + y2) / 2} ${xx},${y2}`;
          return (
            <g key={i} className={`mv r-${m.rel}${sel === i ? ' on' : ''}`} onClick={() => setSel(sel === i ? null : i)} role="button" aria-label={`${i + 1}번 연결: ${m.why}`}>
              <path d={d} className="mvp" markerEnd={`url(#ar-${f.id})`} />
              <path d={d} className="mvhit" />
              <circle cx={xx + 20} cy={(y1 + y2) / 2} r={9} className="mvc" />
              <text x={xx + 20} y={(y1 + y2) / 2 + 4} textAnchor="middle" className="mvt">{i + 1}</text>
              <title>{`${i + 1}. ${T.rels[m.rel]}: ${m.why}`}</title>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
