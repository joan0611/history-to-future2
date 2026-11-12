import { CATS, CAT_KO, CAT_SHORT, D, MAX_Y, byId, eraEnd, eraOf, inc, isKR, lead, nodesIn, out, pickKey, type Cat } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart } from '../ui/Chart';
import type { Era, Flow } from '../lib/data';

/**
 * ① 전체 역사 — 전체(1960~현재) → 10년 → 1년.
 *   전체: 장기 흐름 그래프 + '변화 지도'(분야 × 시대, 칸마다 대표 변화 1개) + 시대별 주요 사건(먼저 5개)
 *   10년: 그 시대의 해마다 무엇이 있었나(연도 칸) + 핵심 변화와 그 연결 + 앞뒤 시대
 *   1년: 분야별 핵심 변화와 한 줄 설명, 국제 정세, 앞뒤 해와의 연결
 */
export function HistoryView({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  return (
    <div className="view">
      <div className="zoom" role="tablist" aria-label="보기 단위">
        {([['all', '전체 1960–현재'], ['decade', '10년'], ['year', '1년']] as const).map(([z, t]) => (
          <button key={z} role="tab" aria-selected={r.z === z} className={r.z === z ? 'on' : ''} onClick={() => nav({ z })}>{t}</button>
        ))}
      </div>
      <p className="zoom-help">{ZOOM_HELP[r.z]}</p>
      {r.z === 'all' && <Overview r={r} nav={nav} why={why} />}
      {r.z === 'decade' && <Decade r={r} nav={nav} why={why} />}
      {r.z === 'year' && <Year r={r} nav={nav} why={why} />}
    </div>
  );
}

const ZOOM_HELP = {
  all: '전체: 1960년부터 지금까지를 한눈에. 선택한 연도는 표시만 되고 내용을 거르지 않습니다.',
  decade: '10년: 선택한 연도가 속한 시대 하나를 봅니다. 시간축에서 다른 연도를 누르면 그 시대로 바뀝니다.',
  year: '1년: 선택한 연도 한 해에 날짜가 확인된 항목만 봅니다. 다른 해의 내용을 끌어와 채우지 않습니다.',
} as const;

/** 흐름의 단계가 어느 해에 걸리는지(기간 글자에서 첫 연도) */
const stepYear = (p: string) => { const m = p.match(/(19|20)\d{2}/); return m ? Number(m[0]) : NaN; };
export function flowStepsIn(e: Era) {
  const end = eraEnd(e);
  const out: { f: Flow; id: string; title: string; period: string }[] = [];
  for (const f of D.flows) for (const s of f.steps) { if (s.period.includes('이전')) continue; const y = stepYear(s.period); if (y >= e.startYear && y <= end) out.push({ f, id: s.id, title: s.title, period: s.period }); }
  return out;
}

function Overview({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const gdp = D.indicators.find((i) => i.id === 'gdp-growth')!;
  const kr = gdp.series.find((s) => s.country === 'KR')!;
  const cpi = D.indicators.find((i) => i.id === 'cpi-kr')!;
  const a = D.analyses.find((x) => x.key === 'gdp-growth:KR');
  return (
    <>
      <section className="panel hero">
        <div className="hero-text">
          <h2>시대별 사건 찾기</h2>
          <p>사건을 찾는 보조 자료입니다. 사건을 누르면 그 사건이 들어 있는 <b>이야기</b>(같은 주제를 시간 순서로 따라가는 글)로 바로 갈 수 있습니다.</p>
        </div>
      </section>

      <section className="panel">
        <h2>시대마다 무엇이 달라졌나 <span className="sub">이전에서 이어진 것 → 이 시대에 달라진 것 → 다음 시대로 넘긴 것</span></h2>
        <ol className="eras">
          {D.eras.map((e, i) => <EraCard key={e.id} e={e} prevSummary={D.transitions.find((t) => t.toEra === e.id)?.summary} first={i === 0} on={eraOf(r.y).id === e.id} nav={nav} />)}
        </ol>
        <p className="small muted">시대 요약은 근거 문장을 묶어 작성자가 정리한 것입니다. 문장별 근거와 해마다의 사건은 각 시대의 ‘10년 보기’에서 확인할 수 있습니다.</p>
      </section>

      <section className="panel">
        <h2>분야별 대표 사건 <span className="sub">칸을 누르면 사건 상세와 그 사건이 들어 있는 이야기</span></h2>
        <p className="small muted">해외 사례에는 ‘해외’ 표시를 붙였습니다.</p>
        <div className="cmap" style={{ gridTemplateColumns: `6.5rem ${D.eras.map((e) => `${eraEnd(e) - e.startYear + 1}fr`).join(' ')}` }}>
          <span />
          {D.eras.map((e) => (
            <button key={e.id} className={`cmap-h${eraOf(r.y).id === e.id ? ' on' : ''}`} onClick={() => nav({ y: e.id === '1970s' ? 1973 : e.startYear, z: 'decade' })}>
              <b>{e.label.replace('~현재', '')}</b><span>{e.title.split('—')[0].trim()}</span>
            </button>
          ))}
          {CATS.map((c) => (
            <Row key={c} c={c} why={why} />
          ))}
        </div>
        {/* 좁은 화면: 시대마다 한 묶음(시대 → 분야별 대표 변화) */}
        <div className="cmap-m">
          {D.eras.map((e) => (
            <div key={e.id} className={eraOf(r.y).id === e.id ? 'on' : ''}>
              <button className="cmap-h" onClick={() => nav({ y: e.id === '1970s' ? 1973 : e.startYear, z: 'decade' })}><b>{e.label.replace('~현재', '')}</b><span>{e.title.split('—')[0].trim()}</span></button>
              {CATS.map((c) => {
                const [n] = pickKey(D.nodes.filter((x) => x.eraId === e.id && x.lane === c), 1);
                return n ? <button key={c} className={`cmap-cell c-${c}`} onClick={() => why(n.id)}><span className="y">{CAT_SHORT[c]} · {n.year}</span>{n.label}</button> : null;
              })}
            </div>
          ))}
        </div>
      </section>

      <section className="panel">
        <h2>경제 지표 한 줄로 보기 <span className="sub">경제는 변화의 한 부분일 뿐 — 다른 분야는 ‘분야별 변화’에서</span></h2>
        <p className="small">{a?.changePoint ? <>성장률은 {a.changePoint.year}년 전후로 평균 {a.changePoint.before}%에서 {a.changePoint.after}%로 한 단계 내려앉았습니다(데이터에서 자동 계산한 변화점). </> : null}그래프를 누르면 그 해로 갑니다.</p>
        <Chart ariaLabel="한국 경제성장률과 물가상승률 1960~2025" unit="%" year={r.y} height={200}
          onPick={(y) => nav({ y, z: 'year' })}
          series={[
            { key: 'g', label: '경제성장률', color: 'var(--c-economy)', points: kr.points.map(([t, v]) => [Number(t), v]) },
            { key: 'p', label: '물가상승률', color: 'var(--c-politics)', points: cpi.series[0].points.map(([t, v]) => [Number(t), v]) },
          ]} />
        <div className="legend"><span><i className="lg-line" style={{ background: 'var(--c-economy)' }} />실질 경제성장률</span><span><i className="lg-line" style={{ background: 'var(--c-politics)' }} />소비자물가 상승률</span><span><i className="lg-sel" />선택 연도</span></div>
        <p className="src-line">출처: FRED(원자료 OECD·세계은행) — 실질 GDP 성장률, 소비자물가 상승률. 같은 단위(%)라 한 축에 그렸습니다.</p>
      </section>
    </>
  );
}

const turnsIn = (e: Era) => D.topics.topics.flatMap((t) => t.turns.filter((tu) => tu.start >= e.startYear && tu.start <= eraEnd(e)).map((tu) => ({ t, tu })));

function EraCard({ e, prevSummary, first, on, nav }: { e: Era; prevSummary?: string; first: boolean; on: boolean; nav: (p: Partial<Route>) => void }) {
  const go = () => nav({ y: e.id === '1970s' ? 1973 : e.startYear, z: 'decade' });
  return (
    <li className={`era-card${on ? ' on' : ''}`}>
      <button className="era-h" onClick={go}><b>{e.label}</b> <span>{e.title}</span></button>
      <dl>
        <dt>이전에서</dt><dd>{prevSummary ?? (first ? '이 사이트는 1960년부터 다룹니다. 1960년 이전 배경은 사건 상세의 ‘1960년 이전’ 항목에서 볼 수 있습니다.' : '자료 없음')}</dd>
        <dt>달라진 것</dt><dd>{e.glance.keyCause ?? '자료 없음'}</dd>
        {e.glance.legacy && <><dt>다음으로</dt><dd>{e.glance.legacy}</dd></>}
      </dl>
      {turnsIn(e).length > 0 && (
        <p className="era-flows"><span className="muted">이 시대에 전환점이 있는 이야기</span> {turnsIn(e).map((x) => (
          <a key={x.t.id + x.tu.id} className="chip" href={`#/topic/${x.t.id}`}>{x.t.label.split(' — ')[0]} · {x.tu.title}</a>
        ))}</p>
      )}
      <button className="link" onClick={go}>10년 보기 — 해마다의 사건과 근거 →</button>
    </li>
  );
}

function Row({ c, why }: { c: Cat; why: (id: string) => void }) {
  return (
    <>
      <span className={`cmap-c c-${c}`}><span className={`cdot c-${c}`} />{c === 'flow' ? '여러 분야' : CAT_SHORT[c]}</span>
      {D.eras.map((e) => {
        const [n] = pickKey(D.nodes.filter((x) => x.eraId === e.id && x.lane === c), 1);
        return n
          ? <button key={e.id} className={`cmap-cell c-${c}`} onClick={() => why(n.id)} title={`${n.year} ${n.label}`}><span className="y">{n.year}{!isKR(n) && <span className="abroad">해외</span>}</span>{n.label}</button>
          : <span key={e.id} className="cmap-cell empty">자료 없음</span>;
      })}
    </>
  );
}

function Decade({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const e = eraOf(r.y);
  const end = eraEnd(e);
  const idx = D.eras.indexOf(e);
  const prev = D.eras[idx - 1], next = D.eras[idx + 1];
  const pool = D.nodes.filter((n) => n.eraId === e.id && isKR(n));
  const key = pickKey(pool, 5);
  const keyIds = new Set(key.map((n) => n.id));
  const links = D.edges.filter((x) => keyIds.has(x.from) && keyIds.has(x.to));
  const tIn = D.transitions.find((t) => t.toEra === e.id), tOut = D.transitions.find((t) => t.fromEra === e.id);
  const years = Array.from({ length: end - e.startYear + 1 }, (_, i) => e.startYear + i);
  const fromBefore = key.flatMap((k) => inc[k.id].map((x) => byId[x.from]).filter((o) => o && o.year < e.startYear).map((o) => ({ o, k })));
  const toAfter = key.flatMap((k) => out[k.id].map((x) => byId[x.to]).filter((o) => o && o.year > end).map((o) => ({ o, k })));
  return (
    <>
      <section className="panel">
        <div className="dec-head">
          {prev && <button className="btn ghost sm" onClick={() => nav({ y: prev.startYear })}>← {prev.label}</button>}
          <div><div className="eyebrow">{e.startYear}–{e.endYear ?? '현재'}</div><h2>{e.label} — {e.title}</h2></div>
          {next && <button className="btn ghost sm" onClick={() => nav({ y: next.startYear })}>{next.label} →</button>}
        </div>
        {e.glance.keyCause && <p className="lead">{e.glance.keyCause}</p>}
        {tIn && <p className="bridge"><b>앞 시대에서 이어진 흐름</b> {tIn.summary}</p>}

        <h3>이 시대의 핵심 변화 {key.length}가지</h3>
        <ol className="keyrail">
          {key.map((n, i) => {
            const linkOut = links.filter((x) => x.from === n.id);
            return (
              <li key={n.id} className={`c-${n.lane}`}>
                <button className="keycard" onClick={() => why(n.id)}>
                  <span className="kc-meta"><span className={`cdot c-${n.lane}`} />{n.year} · {CAT_KO[n.lane]}</span>
                  <b>{n.label}</b>
                  <span className="kc-lead">{lead(n, 90)}</span>
                  <span className="kc-why">원인·결과 보기 →</span>
                </button>
                {linkOut.map((x) => <span key={x.id} className="kc-link">↳ {D.relKo[x.rel]} → {byId[x.to].label}</span>)}
                {i < key.length - 1 && !linkOut.length && <span className="kc-gap" aria-hidden />}
              </li>
            );
          })}
        </ol>
        {(fromBefore.length > 0 || toAfter.length > 0) && (
          <div className="two">
            <div><h4>이전 시대에서 온 원인</h4><ul className="plain">{fromBefore.slice(0, 4).map(({ o, k }) => <li key={o.id + k.id}><button className="link" onClick={() => why(o.id)}>{o.year < 1960 ? '1960 이전' : o.year} {o.label}</button> <span className="muted">→ {k.label}</span></li>)}</ul></div>
            <div><h4>다음 시대로 이어진 결과</h4><ul className="plain">{toAfter.slice(0, 4).map(({ o, k }) => <li key={o.id + k.id}><span className="muted">{k.label} →</span> <button className="link" onClick={() => why(o.id)}>{o.year} {o.label}</button></li>)}</ul></div>
          </div>
        )}
        {tOut && <p className="bridge out"><b>다음 시대로</b> {tOut.summary}</p>}
      </section>

      {flowStepsIn(e).length > 0 && (
        <section className="panel">
          <h3>이 시대를 지나는 변화 흐름 <span className="sub">질문별로 이 시대가 어떤 단계였나</span></h3>
          <ul className="plain era-steps">
            {flowStepsIn(e).map((x) => (
              <li key={x.f.id + x.id}><a href={`#/flow/${x.f.id}?y=${r.y}`}><b>{x.f.question}</b></a> <span className="muted">— {x.period}: {x.title}</span></li>
            ))}
          </ul>
        </section>
      )}

      <section className="panel">
        <h3>해마다 무엇이 있었나 <span className="sub">연도를 누르면 1년 보기</span></h3>
        <div className="yeargrid">
          {years.map((y) => {
            const ns = pool.filter((n) => n.yearPrecision === 'year' && n.year === y).sort((a, b) => a.importance - b.importance);
            return (
              <div key={y} className={`yg${y === r.y ? ' on' : ''}${ns.length ? '' : ' empty'}`}>
                <button className="yg-h" onClick={() => nav({ y, z: 'year' })}>{y}</button>
                {ns.length ? <ul>{ns.slice(0, 3).map((n) => <li key={n.id}><button className={`c-${n.lane}`} onClick={() => why(n.id)}><span className={`cdot c-${n.lane}`} />{n.label}</button></li>)}
                  {ns.length > 3 && <li><button className="link" onClick={() => nav({ y, z: 'year' })}>+{ns.length - 3}</button></li>}</ul> : <p className="muted">자료 없음</p>}
              </div>
            );
          })}
        </div>
      </section>
    </>
  );
}

function Year({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const y = r.y;
  const all = nodesIn(y, y);
  const kr = all.filter(isKR);
  const intl = all.filter((n) => !isKR(n));
  const ids = new Set(all.map((n) => n.id));
  const before = D.edges.filter((e) => ids.has(e.to) && byId[e.from]?.year < y);
  const after = D.edges.filter((e) => ids.has(e.from) && byId[e.to]?.year > y);
  const byCat = CATS.map((c) => ({ c, ns: pickKey(kr.filter((n) => n.lane === c), 6) })).filter((x) => x.ns.length)
    .sort((a, b) => a.ns.reduce((s, n) => s + n.importance, 0) / a.ns.length - b.ns.reduce((s, n) => s + n.importance, 0) / b.ns.length);
  const empty = CATS.filter((c) => !byCat.some((x) => x.c === c));
  return (
    <section className="panel">
      <div className="dec-head">
        <button className="btn ghost sm" onClick={() => nav({ y: Math.max(1960, y - 1) })} disabled={y <= 1960}>← {y - 1}</button>
        <div><div className="eyebrow">{eraOf(y).label}</div><h2>{y}년 대한민국</h2></div>
        <button className="btn ghost sm" onClick={() => nav({ y: Math.min(MAX_Y, y + 1) })} disabled={y >= MAX_Y}>{y + 1} →</button>
      </div>
      <p className={`complete${kr.length ? '' : ' none'}`}>
        {kr.length ? <>이 해로 날짜가 확인된 항목 <b>{kr.length}</b>개{empty.length ? ` · 자료 없음: ${empty.map((c) => CAT_SHORT[c]).join(', ')}` : ''}</>
          : <>{y}년으로 날짜가 확인된 자료가 아직 없습니다. 다른 해의 내용을 가져와 채우지 않습니다.</>}
      </p>
      <div className="ycats">
        {byCat.map(({ c, ns }) => (
          <div key={c} className={`ycat c-${c}`}>
            <h3><span className={`cdot c-${c}`} />{CAT_KO[c]}</h3>
            <ul>{ns.map((n) => <li key={n.id}><button onClick={() => why(n.id)}><b>{n.label}</b><span>{lead(n, 100)}</span></button></li>)}</ul>
          </div>
        ))}
        {intl.length > 0 && (
          <div className="ycat intl">
            <h3>국제 정세</h3>
            <ul>{intl.map((n) => {
              const toKr = out[n.id].map((e) => byId[e.to]).filter((m) => m && m.countries.includes('KR'));
              return <li key={n.id}><button onClick={() => why(n.id)}><b>{n.label}</b><span>{toKr.length ? `한국으로: ${toKr[0].label}` : '한국과 직접 연결된 근거는 아직 없음'}</span></button></li>;
            })}</ul>
          </div>
        )}
      </div>
      {(before.length > 0 || after.length > 0) && (
        <div className="two">
          <div><h4>이전 해에서 이어진 것</h4><ul className="plain">{before.slice(0, 6).map((e) => <li key={e.id}><button className="link" onClick={() => why(e.from)}>{byId[e.from].year < 1960 ? '1960 이전' : byId[e.from].year} {byId[e.from].label}</button> <span className="muted">→ {byId[e.to].label}</span></li>)}</ul></div>
          <div><h4>이후로 이어진 것</h4><ul className="plain">{after.slice(0, 6).map((e) => <li key={e.id}><span className="muted">{byId[e.from].label} →</span> <button className="link" onClick={() => why(e.to)}>{byId[e.to].year} {byId[e.to].label}</button></li>)}</ul></div>
        </div>
      )}
    </section>
  );
}
