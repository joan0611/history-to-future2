import { SpecStatus } from '../ui/SpecStatus';
import { D, MODE_KO, topicById, type Topic, type TLine, type TTurn, type TWorld, type TFuture } from '../lib/data';
import type { Route } from '../lib/route';
import { SLineView, SBadge, LayerLegend, SharedEvents, goTo } from '../ui/Story';

/**
 * 주제 이야기 — 같은 대상을 끝까지 따라가는 본문(R-Q3, R-Q7).
 * 순서(R-FU3): 질문·장면 → 시간축 → 전환점 이야기(세계 연결 포함) → 갈래 → 다른 흐름과 만나는 곳 → 핵심 추론 → 반복 → 미래 → 결론.
 * 11개 질문은 본문 목록이 아니라 데이터 점검표로만 쓴다(R-Q6).
 */
type Nav = (p: Partial<Route>) => void;
const T = D.topics;

const Lines = ({ xs }: { xs: TLine[] }) => <>{xs.map((x, i) => <SLineView key={i} x={x} />)}</>;
const scrollTo = (id: string) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });

export function TopicView({ r, nav }: { r: Route; nav: Nav }) {
  const t = r.topic ? topicById[r.topic] : undefined;
  if (t) return <TopicDetail t={t} nav={nav} />;
  return <TopicMap nav={nav} />;
}

/* ── 분야 지도: 읽을 수 있는 주제만 활성, 다룰 예정은 다른 모양(R-Q16). 작업 현황은 저장소 문서에만 둔다. ── */
type MapItem = { kind: 'topic' | 'taste' | 'flow' | 'industry'; id: string };
const IND = (D.industries as { industries: { id: string; label: string; question: string; span: [number, number] }[] }).industries;
function itemInfo(it: MapItem): { title: string; q: string; span?: string; kindKo: string } | undefined {
  if (it.kind === 'topic') { const t = topicById[it.id]; return t && { title: t.label, q: t.question, span: `${t.span[0]}~${t.span[1]}`, kindKo: '이야기' }; }
  if (it.kind === 'taste') { const f = D.tastes.flows.find((x) => x.id === it.id); return f && { title: f.title, q: f.question, span: `${f.span[0]}~${f.span[1]}`, kindKo: '취향 흐름' }; }
  if (it.kind === 'flow') { const f = D.flows.find((x) => x.id === it.id); return f && { title: f.topic, q: f.question, kindKo: '시대 흐름' }; }
  const i = IND.find((x) => x.id === it.id); return i && { title: i.label, q: i.question, span: `${i.span[0]}~${i.span[1]}`, kindKo: '산업 일대기' };
}
function openItem(nav: Nav, it: MapItem) {
  if (it.kind === 'topic') nav({ tab: 'topic', topic: it.id });
  else if (it.kind === 'taste') nav({ tab: 'taste', taste: it.id, topic: undefined });
  else if (it.kind === 'flow') nav({ tab: 'flow', flow: it.id, topic: undefined });
  else nav({ tab: 'field', cat: 'industry', ind: it.id, topic: undefined });
  window.setTimeout(() => window.scrollTo({ top: 0 }), 30);
}

export function TopicMap({ nav }: { nav: Nav }) {
  return (
    <div className="view topics">
      <section className="panel hero">
        <h2>한 가지를 끝까지 따라가는 이야기</h2>
        <p className="lead">분야를 고르고, 그 안의 주제 하나를 고르세요. 한 주제 안에서는 같은 대상만 따라갑니다 — 처음엔 어땠는지, 무엇이 언제 왜 바뀌었는지, 옛 선택은 어떻게 남았는지, 지금 어디에 있고 앞으로 어떤 방향이 가능한지.</p>
      </section>
      <SpecStatus />
      {T.fieldMap.map((fd) => {
        const items = fd.items.map((it) => ({ it, info: itemInfo(it as MapItem) })).filter((x) => x.info);
        const dom = T.domains.find((d) => d.id === 'shop' && fd.id === 'buying');
        return (
          <section key={fd.id} className="panel tp-dom" id={`fd-${fd.id}`}>
            <h2>{fd.label}</h2>
            {dom && <p className="muted">{dom.desc}</p>}
            {items.length > 0 ? (
              <div className="tp-cards">
                {items.map(({ it, info }) => (
                  <button key={it.id} className="tp-card" onClick={() => openItem(nav, it as MapItem)}>
                    <span className="tp-kindko">{info!.kindKo}</span>
                    <b>{info!.title}</b>
                    <span className="tp-q">{info!.q}</span>
                    {info!.span && <span className="muted small">{info!.span}</span>}
                    <span className="fc-go">읽기 →</span>
                  </button>
                ))}
              </div>
            ) : <p className="muted small">아직 읽을 수 있는 주제가 없습니다.</p>}
            {fd.id === 'buying' && <Interplay domain="shop" nav={nav} />}
            {fd.planned.length > 0 && (
              <div className="tp-planned">
                <span className="muted small">다룰 예정 — 아직 읽을 내용 없음</span>
                <ul>{fd.planned.map((p) => <li key={p}>{p}</li>)}</ul>
              </div>
            )}
          </section>
        );
      })}
      <Needs nav={nav} />
    </div>
  );
}

/* ── 분야를 가로지르는 욕구(R-Q17): 사례의 시기·과정을 먼저, 그다음 공통점·차이 ── */
function Needs({ nav }: { nav: Nav }) {
  return (
    <section className="panel" id="needs">
      <h2>분야를 가로지르는 욕구</h2>
      <p className="muted">같은 이름의 욕구가 여러 분야에서 보일 때, 먼저 각 사례가 <b>언제 · 누구에게서 · 무엇에서 무엇으로</b> 바뀌었는지 보고, 그다음 공통점과 차이를 읽습니다. 사례끼리 원인-결과 관계라는 뜻은 아닙니다.</p>
      {T.needs.map((n) => (
        <article key={n.id} className="tp-need">
          <h3>{n.label} <span className="tp-rel">{T.relKo[n.rel]}</span></h3>
          <p className="small">{n.intro}</p>
          <div className="tz-tlwrap"><table className="tp-cases"><thead><tr><th>사례</th><th>언제 · 누가</th><th>그전 선택</th><th>계기</th><th>달라진 선택</th><th>원한 것</th></tr></thead><tbody>
            {n.cases.map((c) => (
              <tr key={c.kind + c.id + c.label}>
                <th><button className="link" onClick={() => openItem(nav, { kind: c.kind as MapItem['kind'], id: c.id })}>{c.label} →</button></th>
                <td><b>{c.when}</b><br /><span className="small muted">{c.who}</span></td>
                <td><SLineView x={c.before} /></td><td><SLineView x={c.trigger} /></td><td><SLineView x={c.after} /></td><td><SLineView x={c.motive} /></td>
              </tr>
            ))}
          </tbody></table></div>
          <dl className="tp-needread">
            <dt>왜 그때, 그 모양으로</dt><dd><SLineView x={n.whyNow} /></dd>
            <dt>공통점</dt><dd><SLineView x={n.common} /></dd>
            <dt>차이</dt><dd><SLineView x={n.differ} /></dd>
            <dt>이 설명이 안 맞는 곳</dt><dd><SLineView x={n.counter} /></dd>
          </dl>
        </article>
      ))}
    </section>
  );
}

/* ── 주제 본문 ── */
function TopicDetail({ t, nav }: { t: Topic; nav: Nav }) {
  const dom = T.domains.find((d) => d.id === t.domain);
  return (
    <div className="view topic">
      <p><button className="link" onClick={() => nav({ tab: 'topic', topic: undefined })}>← {dom?.label ?? '주제'} 전체</button></p>
      <section className="panel" id="tp-q">
        <p className="muted small">{dom?.label}</p>
        <h2 className="tp-title">{t.label}</h2>
        <p className="tp-question">{t.question} <a className="ak-ask" href={`#/ask?q=${encodeURIComponent(t.question)}`}>이 질문으로 분석하기</a></p>
        <div className="tp-scene"><SLineView x={t.scene} /></div>
        <p className="tp-tracks"><b>이 이야기가 계속 따라가는 것</b> {t.tracks}</p>
        <LayerLegend />
        {t.scope && t.scope.length > 0 && <details className="tp-scope"><summary>시작 시점과 자료가 비는 곳</summary><Lines xs={t.scope} /></details>}
        <nav className="tp-toc" aria-label="이 주제의 순서">
          {[['tp-time', '시간 흐름'], ['tp-turns', '전환점 이야기'], ['tp-branch', '옛 선택은 어떻게 남았나'], ...(t.compare ? [['tp-compare', '도구별 비교']] : []), ['tp-reason', '왜 그렇게 봤나'], ...(t.repeats?.length ? [['tp-repeat', '되풀이되는 것']] : []), ['tp-future', '앞으로 가능한 방향'], ['tp-end', '결론']].map(([id, l]) => <button key={id} className="chip" onClick={() => scrollTo(id)}>{l}</button>)}
        </nav>
      </section>

      <TimeAxis t={t} />

      <section className="panel" id="tp-turns">
        <h2>전환점 이야기</h2>
        <p className="muted">각 전환점은 <b>그전 상태 → 새로 생긴 조건 → 사람·기업의 반응 → 구체적인 변화 → 다음에 남긴 것</b> 순서로 읽습니다. 앞 전환점이 남긴 것이 다음 전환점의 조건이 됩니다.</p>
        {t.turns.map((tu, i) => <TurnCard key={tu.id} tu={tu} n={i + 1} />)}
      </section>

      <Branches t={t} />
      {t.compare && <CompareTable t={t} />}
      {t.links && t.links.length > 0 && <Links t={t} nav={nav} />}

      <section className="panel" id="tp-reason">
        <h2>왜 그렇게 봤나 — 핵심 추론</h2>
        <p className="muted">이야기에서 가장 중요한 연결을 어떤 사실에서 출발해 어떻게 이었는지, 다른 설명은 무엇이고 무엇으로 확인·반박할 수 있는지 보여 줍니다.</p>
        {t.reasons.map((x) => (
          <article key={x.title} className="tp-reason">
            <h3>{x.title}</h3>
            <h4>출발한 사실</h4><Lines xs={x.facts} />
            <h4>이어 붙인 논리</h4><SLineView x={x.logic} />
            <h4>제안하는 설명</h4><SLineView x={x.proposal} />
            <h4>경쟁하는 다른 설명</h4><Lines xs={x.rivals} />
            <h4>어느 시기·누구에게 해당하나</h4><SLineView x={x.scope} />
            <h4>확인하거나 반박할 자료</h4><Lines xs={x.check} />
          </article>
        ))}
      </section>

      {t.repeats && t.repeats.length > 0 && (
        <section className="panel" id="tp-repeat">
          <h2>되풀이되는 것 — 그리고 달라진 것</h2>
          <p className="muted">같은 모양이 다시 나타났다고 같은 이유인지는 따로 따져야 합니다. 과거와 지금을 같은 질문으로 나란히 놓았습니다.</p>
          {t.repeats.map((rp) => (
            <article key={rp.title} className="tp-repeat">
              <h3><span className="tp-kind">{rp.type}</span> {rp.title}</h3>
              <table className="tp-cmp"><tbody>
                <tr><th>그때 누가·왜</th><td><SLineView x={rp.past} /></td></tr>
                <tr><th>지금 누가·왜</th><td><SLineView x={rp.now} /></td></tr>
                <tr><th>겉모양만 같나, 이유도 같나</th><td><SLineView x={rp.alike} /></td></tr>
                <tr><th>달라진 것(가격·기술·매체·의미, 과거 불편)</th><td><SLineView x={rp.changed} /></td></tr>
                <tr><th>다른 설명</th><td><Lines xs={rp.alternatives} /></td></tr>
                <tr><th>반대 사례·안 맞는 조건</th><td><Lines xs={rp.counter} /></td></tr>
              </tbody></table>
              {rp.at.length > 0 && <p className="small">해당 구간으로: {rp.at.map((a) => { const tu = t.turns.find((x) => x.id === a); return <button key={a} className="chip" onClick={() => scrollTo(`turn-${a}`)}>{tu?.years} {tu?.title}</button>; })}</p>}
            </article>
          ))}
        </section>
      )}

      <FuturesView id="tp-future" f={t.futures} />
      <ConclusionView id="tp-end" c={t.conclusion} />
    </div>
  );
}

/* 시간축: 전환점이 언제 시작했는지(칸 = 다음 전환점까지) */
function TimeAxis({ t }: { t: Topic }) {
  const [a, b] = t.span;
  const W = 900, L = 20, R = 20, H = 70;
  const x = (y: number) => L + ((y - a) / Math.max(1, b - a)) * (W - L - R);
  const ticks = Array.from({ length: Math.floor((b - a) / 10) + 2 }, (_, i) => Math.ceil(a / 10) * 10 + i * 10).filter((y) => y <= b);
  return (
    <section className="panel" id="tp-time">
      <h2>시간 흐름</h2>
      <p className="muted">무엇을 보나: 전환점이 시작된 해입니다. 칸 하나는 다음 전환점이 시작될 때까지이고, 겹쳐 있는 칸은 두 변화가 같은 시기에 함께 진행됐다는 뜻입니다. 누르면 그 이야기로 갑니다.</p>
      <div className="tz-tlwrap"><svg className="tp-axis" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="전환점 시간축">
        {ticks.map((y) => <g key={y}><line x1={x(y)} x2={x(y)} y1={8} y2={H - 18} className="tick" /><text x={x(y)} y={H - 4} className="tickl" textAnchor="middle">{y}</text></g>)}
        {t.turns.map((tu, i) => {
          const nx = i + 1 < t.turns.length ? Math.max(t.turns[i + 1].start, tu.start + 1) : b;
          const row = i % 2;
          return (
            <g key={tu.id} className="tp-seg" onClick={() => scrollTo(`turn-${tu.id}`)} role="button" tabIndex={0} onKeyDown={(e) => { if (e.key === 'Enter') scrollTo(`turn-${tu.id}`); }}>
              <rect x={x(tu.start)} y={12 + row * 20} width={Math.max(x(nx) - x(tu.start) - 2, 6)} height={16} rx={4} className={`tpk k${i % 6}`}><title>{`${tu.years} ${tu.title}`}</title></rect>
              <text x={x(tu.start) + 4} y={24 + row * 20} className="tp-segl">{i + 1}</text>
            </g>
          );
        })}
      </svg></div>
      <ol className="tp-axis-list">{t.turns.map((tu) => <li key={tu.id}><button className="link" onClick={() => scrollTo(`turn-${tu.id}`)}><b>{tu.years}</b> {tu.title}</button></li>)}</ol>
      <p className="small">읽어낼 것: 변화가 고르게 퍼져 있지 않고 몇몇 시기에 몰려 있습니다. 몰린 시기가 왜 몰렸는지가 아래 전환점 이야기의 질문입니다.</p>
    </section>
  );
}

export function TurnCard({ tu, n }: { tu: TTurn; n: number }) {
  const rows: [string, TLine[]][] = [['그전 상태', tu.before], ['새로 생긴 조건', tu.condition], ['사람·기업의 반응', tu.response], ['구체적인 변화', tu.change], ['다음에 남긴 것', tu.legacy]];
  return (
    <article className="tp-turn" id={`turn-${tu.id}`}>
      <h3><span className="tp-n">{n}</span> <span className="tp-yr">{tu.years}</span> {tu.title}</h3>
      <div className="tp-why"><b>왜 이 시점인가</b> <SLineView x={tu.why} /></div>
      <ol className="tp-chain">{rows.map(([h, xs]) => <li key={h}><h4>{h}</h4><div><Lines xs={xs} /></div></li>)}</ol>
      {tu.world && <WorldBox w={tu.world} />}
      <SharedEvents evs={tu.events} />
      {tu.gap && <p className="tp-gap small"><SBadge l="unknown" /> 자료 공백: {tu.gap}</p>}
    </article>
  );
}

/* 갈래 구조: 한 줄 = 한 선택지, 언제 생겨 지금 어떤 상태인가 */
function Branches({ t }: { t: Topic }) {
  const [a, b] = t.span;
  const pct = (y: number) => ((Math.max(y, a) - a) / Math.max(1, b - a)) * 100;
  return (
    <section className="panel" id="tp-branch">
      <h2>옛 선택은 어떻게 남았나</h2>
      <p className="muted">무엇을 보나: {t.branches.intro} 막대는 그 선택지가 있던 기간입니다.</p>
      <ul className="tp-lanes">
        {t.branches.lanes.map((l) => (
          <li key={l.label}>
            <span className="tp-lane-name">{l.label}</span>
            <span className="tp-lane-bar"><i style={{ left: `${pct(l.start)}%`, width: `${pct(l.end ?? b) - pct(l.start)}%` }} /></span>
            <span className={`tp-state s-${l.state}`}>{l.state}</span>
            <span className="tp-lane-note"><SLineView x={l.note} /></span>
          </li>
        ))}
      </ul>
      <div className="tp-read"><b>읽어낼 것</b> <SLineView x={t.branches.read} /></div>
    </section>
  );
}

function Links({ t, nav }: { t: Topic; nav: Nav }) {
  return (
    <section className="panel" id="tp-links">
      <h2>다른 이야기와 만나는 곳</h2>
      <p className="muted">아래는 이 주제의 다음 단계가 아니라, 같은 시기에 영향을 주고받은 다른 대상입니다. 새로운 설명이 있는 곳만 연결했습니다.</p>
      <ul className="tp-links">
        {t.links!.map((l) => {
          const planned = l.kind === 'topic' && !topicById[l.target];
          const name = l.kind === 'topic' ? (topicById[l.target]?.label ?? T.planned.find((p) => p.id === l.target)?.label) : l.kind === 'flow' ? (D.flows.find((f) => f.id === l.target)?.topic ?? D.tastes.flows.find((f) => f.id === l.target)?.title) : l.target;
          return (
            <li key={l.target + l.at}>
              <span className="tp-at">{l.at}</span> {l.why}{' '}
              {planned ? <span className="chip off" aria-disabled="true">{name} — 준비 중</span>
                : <button className="chip go" onClick={() => (l.kind === 'topic' ? nav({ tab: 'topic', topic: l.target }) : goTo(nav, l.target))}>{name} →</button>}
            </li>
          );
        })}
      </ul>
    </section>
  );
}

/* 같은 분야 안의 주제들이 서로 영향을 준 지점(R-Q18) — 각 주제의 '만나는 곳'에서 모은다 */
function Interplay({ domain, nav }: { domain: string; nav: Nav }) {
  const ts = T.topics.filter((t) => t.domain === domain);
  const rows = ts.flatMap((t) => (t.links ?? []).filter((l) => l.kind === 'topic' && topicById[l.target]?.domain === domain).map((l) => ({ from: t, to: topicById[l.target], at: l.at, why: l.why })));
  if (!rows.length) return null;
  return (
    <div className="tp-inter">
      <h3>이 분야의 이야기들이 서로 영향을 준 곳</h3>
      <p className="muted small">각 이야기는 한 가지 대상만 따라갑니다. 대신 서로 맞물린 시점을 여기 모았습니다.</p>
      <ul>{rows.map((r, i) => (
        <li key={i}><span className="tp-at">{r.at}</span> <button className="link" onClick={() => nav({ tab: 'topic', topic: r.from.id })}>{r.from.label.split(' — ')[0]}</button> ↔ <button className="link" onClick={() => nav({ tab: 'topic', topic: r.to.id })}>{r.to.label.split(' — ')[0]}</button> — {r.why}</li>
      ))}</ul>
    </div>
  );
}

/** 세계 → 들어온 경로 → 국내 대응 → 결과(R-W2). 주제 이야기와 산업 일대기가 같이 쓴다. */
export function WorldBox({ w, at }: { w: TWorld; at?: string }) {
  return (
    <div className="tp-world">
      <b>세계와 이어진 지점{at ? ` · ${at}` : ''}</b> <span className="tp-mode">{MODE_KO[w.mode]}</span>
      <ol className="tp-wsteps">
        <li><h4>세계에서 달라진 것</h4><SLineView x={w.what} /></li>
        <li><h4>들어온 경로</h4><SLineView x={w.route} /></li>
        <li><h4>국내의 대응</h4><SLineView x={w.response} /></li>
        <li><h4>결과</h4><SLineView x={w.result} /></li>
      </ol>
    </div>
  );
}

/** 여러 갈래의 미래 가능성 — 가능성마다 7항목, 확률 없음(R-Q12·R-Q13·R-FU1). */
export function FuturesView({ id, f, title = '앞으로 가능한 방향' }: { id: string; f: { split: TLine; items: TFuture[] }; title?: string }) {
  return (
    <section className="panel" id={id}>
      <h2>{title}</h2>
      <div className="tp-split"><b>왜 방향이 갈라지나</b> <SLineView x={f.split} as="scenario" /></div>
      <p className="muted small">확률은 붙이지 않았습니다. 시점도 근거가 있을 때만 적었습니다. 각 가능성마다 무엇을 보면 판단을 고쳐야 하는지 함께 적었습니다.</p>
      <div className="tp-futs">
        {f.items.map((x) => (
          <article key={x.name} className="tp-fut">
            <h3><span className="tp-kind">{x.kind}</span> {x.name}</h3>
            <table className="tp-cmp"><tbody>
              <tr><th>예상 변화</th><td><SLineView x={x.change} as="scenario" /></td></tr>
              <tr><th>근거</th><td><Lines xs={x.basis} /></td></tr>
              <tr><th>연결 논리</th><td><SLineView x={x.logic} /></td></tr>
              <tr><th>성립 조건</th><td><SLineView x={x.conditions} as="scenario" /></td></tr>
              <tr><th>필요해질 상품·서비스</th><td><SLineView x={x.demand} /></td></tr>
              <tr><th>볼 신호</th><td><ul>{x.watch.map((w) => <li key={w}>{w}</li>)}</ul></td></tr>
              <tr><th>판단을 바꿀 신호</th><td><ul>{x.against.map((w) => <li key={w}>{w}</li>)}</ul></td></tr>
              {x.horizon && <tr><th>시간 범위</th><td>{x.horizon}</td></tr>}
            </tbody></table>
          </article>
        ))}
      </div>
    </section>
  );
}

/** 결론 5요소(R-Q14). */
export function ConclusionView({ id, c }: { id: string; c: { key: TLine; favored: TLine; undecided: TLine; next: TLine; change: TLine } }) {
  return (
    <section className="panel tp-end" id={id}>
      <h2>결론</h2>
      <dl>
        <dt>가장 중요하게 읽은 것</dt><dd><SLineView x={c.key} /></dd>
        <dt>지금 더 지지하는 해석과 이유</dt><dd><SLineView x={c.favored} /></dd>
        <dt>아직 판단할 수 없는 것</dt><dd><SLineView x={c.undecided} as="unknown" /></dd>
        <dt>다음에 주목할 가능성</dt><dd><SLineView x={c.next} /></dd>
        <dt>이것이 보이면 판단을 바꾼다</dt><dd><SLineView x={c.change} /></dd>
      </dl>
    </section>
  );
}

/** 작은 비교표(R-Q21·R-DA1) — 앞: 무엇을 보나, 뒤: 무엇을 읽나. 이어서 질문별 답(R-DA2). */
function CompareTable({ t }: { t: Topic }) {
  const c = t.compare!;
  return (
    <section className="panel" id="tp-compare">
      <h2>도구별로 나란히 보기</h2>
      <p className="muted">무엇을 보나: {c.intro}</p>
      <div className="tablewrap"><table className="tz-table tp-cmpt">
        <thead><tr><th></th>{c.cols.map((x) => <th key={x}>{x}</th>)}</tr></thead>
        <tbody>{c.rows.map((r) => <tr key={r.label}><th>{r.label}</th>{r.cells.map((x, i) => <td key={i}>{x}</td>)}</tr>)}</tbody>
      </table></div>
      <div className="tp-split"><b>읽어낼 것</b> <SLineView x={c.read} /></div>
      {t.probes && t.probes.length > 0 && (
        <div className="tp-probes">
          <h3>서로의 불편이 서로를 불렀나</h3>
          <dl>{t.probes.map((p) => <div key={p.q}><dt>{p.q}</dt><dd><Lines xs={p.a} /></dd></div>)}</dl>
        </div>
      )}
    </section>
  );
}
