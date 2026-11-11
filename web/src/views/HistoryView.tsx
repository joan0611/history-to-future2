import { useState } from 'react';
import { CATS, CAT_KO, CAT_SHORT, D, MAX_Y, byId, eraEnd, eraOf, inc, isKR, lead, nodesIn, out, pickKey, type Cat, type Node } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart } from '../ui/Chart';

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
      {r.z === 'all' && <Overview r={r} nav={nav} why={why} />}
      {r.z === 'decade' && <Decade r={r} nav={nav} why={why} />}
      {r.z === 'year' && <Year r={r} nav={nav} why={why} />}
    </div>
  );
}

function Overview({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const gdp = D.indicators.find((i) => i.id === 'gdp-growth')!;
  const kr = gdp.series.find((s) => s.country === 'KR')!;
  const cpi = D.indicators.find((i) => i.id === 'cpi-kr')!;
  const a = D.analyses.find((x) => x.key === 'gdp-growth:KR');
  const pc = D.analyses.find((x) => x.key === 'cpi-kr:KR');
  const [issueCat, setIssueCat] = useState<Cat | 'all'>('all');
  return (
    <>
      <section className="panel hero">
        <div className="hero-text">
          <h2>고속 성장에서 저성장으로 — 한 줄로 본 65년</h2>
          <p>{a?.changePoint ? <>성장률은 {a.changePoint.year}년 전후로 평균 {a.changePoint.before}%에서 {a.changePoint.after}%로 한 단계 내려앉았습니다(데이터에서 자동 계산한 변화점). </> : null}
            {pc?.highEpisodes?.length ? <>물가가 추세보다 크게 뛴 시기는 {pc.highEpisodes.map(([x, y]) => (x === y ? `${x}` : `${x}~${y}`)).join(', ')}년입니다. </> : null}
            그래프를 누르면 그 해로 갑니다.</p>
        </div>
        <Chart ariaLabel="한국 경제성장률과 물가상승률 1960~2025" unit="%" year={r.y} height={260}
          onPick={(y) => nav({ y, z: 'year' })}
          series={[
            { key: 'g', label: '경제성장률', color: 'var(--c-economy)', points: kr.points.map(([t, v]) => [Number(t), v]) },
            { key: 'p', label: '물가상승률', color: 'var(--c-politics)', points: cpi.series[0].points.map(([t, v]) => [Number(t), v]) },
          ]} />
        <div className="legend"><span><i className="lg-line" style={{ background: 'var(--c-economy)' }} />실질 경제성장률</span><span><i className="lg-line" style={{ background: 'var(--c-politics)' }} />소비자물가 상승률</span><span><i className="lg-sel" />선택 연도</span></div>
        <p className="src-line">출처: FRED(원자료 OECD·세계은행) — 실질 GDP 성장률, 소비자물가 상승률. 같은 단위(%)라 한 축에 그렸습니다.</p>
      </section>

      <section className="panel">
        <h2>변화의 지도 <span className="sub">분야마다 시대를 대표하는 변화 하나 — 누르면 원인과 결과</span></h2>
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
        <h2>시대별 주요 사건 <span className="sub">시대마다 중요한 5개 먼저</span></h2>
        <div className="chips">
          <button className={`chip${issueCat === 'all' ? ' on' : ''}`} onClick={() => setIssueCat('all')}>전체 분야</button>
          {CATS.map((c) => <button key={c} className={`chip${issueCat === c ? ' on' : ''}`} onClick={() => setIssueCat(c)}><span className={`cdot c-${c}`} />{CAT_SHORT[c]}</button>)}
        </div>
        <div className="issues">
          {D.eras.map((e) => <EraIssues key={e.id} eraId={e.id} cat={issueCat} why={why} nav={nav} />)}
        </div>
      </section>
    </>
  );
}

function Row({ c, why }: { c: Cat; why: (id: string) => void }) {
  return (
    <>
      <span className={`cmap-c c-${c}`}><span className={`cdot c-${c}`} />{CAT_SHORT[c]}</span>
      {D.eras.map((e) => {
        const [n] = pickKey(D.nodes.filter((x) => x.eraId === e.id && x.lane === c), 1);
        return n
          ? <button key={e.id} className={`cmap-cell c-${c}`} onClick={() => why(n.id)} title={`${n.year} ${n.label}`}><span className="y">{n.year}</span>{n.label}</button>
          : <span key={e.id} className="cmap-cell empty">자료 없음</span>;
      })}
    </>
  );
}

function EraIssues({ eraId, cat, why, nav }: { eraId: string; cat: Cat | 'all'; why: (id: string) => void; nav: (p: Partial<Route>) => void }) {
  const e = D.eras.find((x) => x.id === eraId)!;
  const [more, setMore] = useState(false);
  const pool = D.nodes.filter((n) => n.eraId === eraId && n.yearPrecision === 'year' && isKR(n) && (cat === 'all' || n.lane === cat));
  const top = pickKey(pool, 5);
  const rest = pool.filter((n) => !top.includes(n)).sort((a, b) => a.year - b.year);
  const list = more ? [...top, ...rest].sort((a, b) => a.year - b.year) : top;
  return (
    <div className="era-issues">
      <button className="era-issues-h" onClick={() => nav({ y: e.id === '1970s' ? 1973 : e.startYear, z: 'decade' })}><b>{e.label}</b> <span>{e.title.split('—')[0].trim()}</span></button>
      {list.length ? <ol>{list.map((n) => <IssueLine key={n.id} n={n} why={why} strong={top.includes(n)} />)}</ol> : <p className="muted empty">해당 분야 자료 없음</p>}
      {rest.length > 0 && <button className="link" onClick={() => setMore(!more)}>{more ? '주요 사건만' : `+${rest.length}개 더 보기`}</button>}
    </div>
  );
}

function IssueLine({ n, why, strong }: { n: Node; why: (id: string) => void; strong?: boolean }) {
  return (
    <li className={`issue c-${n.lane}${strong ? ' strong' : ''}`}>
      <button onClick={() => why(n.id)}><span className="y">{n.year}</span><span className={`cdot c-${n.lane}`} /><span className="t">{n.label}</span></button>
    </li>
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
