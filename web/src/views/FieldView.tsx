import { useState } from 'react';
import { CATS, CAT_KO, CAT_SHORT, D, eraEnd, isKR, lead, nodesIn, pickKey, type Cat, type Indicator } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine, type Band, type Marker } from '../ui/Chart';
import { Lifecycle } from '../ui/Lifecycle';

/**
 * ② 분야별 변화 — 분야를 고르면 1960~현재 장기 동향이 먼저(대표 시각화 하나를 크게).
 * 상단: 대표 그래프(또는 흐름도) + 요약 / 중단: 전환점·시대별 단계·선택 시기 사건 / 하단: 자동 발견 패턴·없는 자료
 * 연도를 골라도 전체 기간은 그대로, 선택 연도만 강조.
 */
// 여러 항목 한 그래프: 분야 색 + 회색조를 섞어 9개까지 구분(범례·툴팁에 이름이 함께 나온다)
const MULTI_COLOR = ['#c2410c', '#1d4ed8', '#047857', '#a21caf', '#b45309', '#0e7490', '#4d7c0f', '#6b7280', '#be123c'];
const SERIES_COLOR: Record<string, string> = { KR: 'var(--c-economy)', US: 'var(--ink-3)', JP: 'var(--c-industry)' };
const MISSING: Record<Cat, string[]> = {
  economy: ['금리: 재할인율(1964~1998)·콜금리(1991~)·기준금리(1999~)를 따로 표시(정책금리 체계가 바뀌어 하나의 선으로 잇지 않음). 1960~63년 금리 자료 없음', '1989년 이전 실업률', '에너지 소비량 연속 자료 — 석유의존도는 1973·2010년 두 시점만'],
  industry: ['1983년 이전 산업별 취업자 비중(제조업은 1989년 이전)', '직업구조(직업별 취업자) 통계', '1975년 이전 유선전화 연도별 값'],
  society: ['1992년 이전 임금', '자동차 보급률(1,000명당 보유 대수) — 신규 등록 대수(1993~2022)만 있음', '가계 소비 구성은 1970년부터(그 이전 자료 없음)', '1인 가구 2015년 이전 연속 자료'],
  politics: ['정치는 수치 지표 대신 시대별 흐름도로 표시합니다. 정권·제도를 숫자로 바꾼 지표는 만들지 않습니다.'],
  culture: ['음악 차트·음반 판매·방송 통계 — 아직 수집하지 않음(지금은 기록으로 확인된 단계만)', '패션 자료 없음'],
  flow: ['재등장 사례가 아직 적어 반복 간격을 계산할 수 없습니다.'],
};
const NUMERIC: Record<Cat, string[]> = {
  economy: ['gdp-growth', 'gdppc-kr', 'cpi-kr', 'fx-kr', 'unemp-kr', 'emprate-kr', 'disc-kr', 'call-kr', 'baserate-kr', 'oil-dep-kr'],
  industry: ['exports-kr', 'exp-gdp-kr', 'va-agr-kr', 'va-mfg-kr', 'va-srv-kr', 'emp-ag-kr', 'emp-mfg-kr', 'emp-svc-kr', 'tel-kr', 'mobile-kr', 'internet-kr', 'pcbang-kr'],
  society: ['tfr-kr', 'aged-kr', 'life-kr', 'urban-kr', 'house-kr', 'wage-kr', 'realwage-kr', 'carreg-kr', 'hhcons-kr', 'cons-mix-kr', 'engel-kr', 'cons-house-kr', 'hsupply-kr', 'one-person-kr', 'online-kr'], politics: [], culture: ['cons-culture-kr'], flow: [] };
const SIGNALS: Record<Cat, string[]> = { economy: ['ch-sg-debt'], industry: ['ch-sg-chip', 'ch-sg-connect'], society: ['ch-sg-household'], politics: ['ch-sg-china'], culture: ['ch-sg-folk', 'ch-sg-kculture'], flow: [] };

export function FieldView({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const c = r.cat;
  const inds = NUMERIC[c].map((id) => D.indicators.find((i) => i.id === id)).filter(Boolean) as Indicator[];
  const ind = inds.find((i) => i.id === r.ind) ?? inds[0];
  const lifeChains = (c === 'flow' ? D.chains.filter((x) => x.kind === 'signal') : D.chains.filter((x) => SIGNALS[c].includes(x.id)));
  const findings = D.findings.filter((f) => f.category === c || (c === 'flow' && f.type === 'D'));
  const near = nodesIn(r.y - 1, r.y + 1, (n) => isKR(n));
  const nearCat = near.filter((n) => n.lane === c);

  return (
    <div className="view">
      <nav className="cats" role="tablist" aria-label="분야">
        {CATS.map((x) => (
          <button key={x} role="tab" aria-selected={x === c} className={`cat c-${x}${x === c ? ' on' : ''}`} onClick={() => nav({ cat: x, ind: undefined })}>
            <span className={`cdot c-${x}`} />{CAT_KO[x]}
          </button>
        ))}
      </nav>

      <section className="panel hero">
        <h2>{CAT_KO[c]} — 1960년부터 지금까지</h2>
        {ind ? <NumericMain ind={ind} inds={inds} r={r} nav={nav} /> : lifeChains.length > 0 ? (
          <><p className="lead">{c === 'politics' ? '정치·외교는 수치 대신 시대별 흐름과 국제 관계의 변화로 봅니다.' : '확인된 기록으로 등장 → 확산 → 쇠퇴 → 재등장 단계를 이었습니다. 점이나 이름을 누르면 원인과 결과로 갑니다.'}</p>
            <Lifecycle chains={lifeChains} year={r.y} why={why} /></>
        ) : <p className="empty">이 분야의 장기 수치 자료가 아직 없습니다.</p>}
        {ind && lifeChains.length > 0 && <><h3>함께 보는 흐름</h3><Lifecycle chains={lifeChains} year={r.y} why={why} /></>}
      </section>

      <section className="panel">
        <h2>시대별 변화 단계 <span className="sub">{CAT_SHORT[c]} 분야에서 시대마다 가장 중요한 변화</span></h2>
        <ol className="stages">
          {D.eras.map((e) => {
            const ns = pickKey(D.nodes.filter((n) => n.eraId === e.id && n.lane === c), 2);
            return (
              <li key={e.id} className={r.y >= e.startYear && r.y <= eraEnd(e) ? 'on' : ''}>
                <button className="stage-h" onClick={() => nav({ y: e.id === '1970s' ? 1973 : e.startYear })}>{e.label.replace('~현재', '')}</button>
                {ns.length ? ns.map((n) => <button key={n.id} className={`stage-i c-${c}`} onClick={() => why(n.id)}><span className="y">{n.year}</span>{n.label}</button>)
                  : <span className="muted empty">자료 없음</span>}
              </li>
            );
          })}
        </ol>
      </section>

      <section className="panel">
        <h2>{r.y - 1}~{r.y + 1}년 무슨 일이 있었나 <span className="sub">그래프나 시간축에서 연도를 바꾸면 함께 바뀝니다</span></h2>
        {near.length === 0 ? <p className="empty">이 기간에 날짜가 확인된 항목이 없습니다.</p> : (
          <ul className="nearlist">
            {[...nearCat, ...near.filter((n) => n.lane !== c)].slice(0, 10).map((n) => (
              <li key={n.id} className={n.lane === c ? 'mine' : ''}>
                <button onClick={() => why(n.id)}><span className="y">{n.year}</span><span className={`cdot c-${n.lane}`} /><b>{n.label}</b><span className="l">{lead(n, 80)}</span></button>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="panel">
        <h2>이 분야에서 자동으로 찾은 반복·변화 <span className="sub">사이클 발견 엔진 결과</span></h2>
        {findings.length ? (
          <ul className="flist">
            {findings.map((f) => (
              <li key={f.id}><a href={`#/cycle?f=${f.id}&y=${r.y}`}><span className={`ftype t-${f.type}`}>{TYPE_SHORT[f.type]}</span><b>{f.title}</b><span className="muted">신뢰도 {f.confidence.level}</span></a></li>
            ))}
          </ul>
        ) : <p className="empty">이 분야는 연속된 수치 자료가 부족해 엔진이 분석할 대상이 아직 없습니다.</p>}
        <h3>아직 없는 자료</h3>
        <ul className="plain muted">{MISSING[c].map((m) => <li key={m}>{m}</li>)}</ul>
      </section>
    </div>
  );
}

export const TYPE_SHORT: Record<string, string> = { A: '통계적 주기', B: '불규칙 반복', C: '구조적 유사', D: '문화 재유행', E: '장기 구조 변화', N: '주기 없음', R: '지표 간 관계' };

function NumericMain({ ind, inds, r, nav }: { ind: Indicator; inds: Indicator[]; r: Route; nav: (p: Partial<Route>) => void }) {
  const [showEp, setShowEp] = useState(true);
  const [others, setOthers] = useState(false);
  const a = D.analyses.find((x) => x.key === `${ind.id}:KR`);
  const series = ind.series.filter((s) => ind.multi || s.country === 'KR' || others).map((s, i) => ({
    key: s.country, label: s.label, color: ind.multi ? MULTI_COLOR[i % MULTI_COLOR.length] : (SERIES_COLOR[s.country] ?? 'var(--c-economy)'),
    points: s.points.map(([t, v]) => [Number(t.slice(0, 4)), v] as [number, number]),
  }));
  const bands: Band[] = showEp && a ? [
    ...(a.highEpisodes ?? []).map(([f, t]) => ({ from: f, to: t, tone: 'hi' as const })),
    ...(a.lowEpisodes ?? []).map(([f, t]) => ({ from: f, to: t, tone: 'lo' as const })),
  ] : [];
  const markers: Marker[] = (a?.turningPoints ?? []).map((p) => ({ year: p.year, kind: p.kind }));
  return (
    <>
      {inds.length > 1 && (
        <div className="subtabs" role="tablist" aria-label="세부 지표">
          {inds.map((i) => <button key={i.id} role="tab" aria-selected={i.id === ind.id} className={i.id === ind.id ? 'on' : ''} onClick={() => nav({ ind: i.id })}>{i.title}</button>)}
        </div>
      )}
      <p className="lead"><b>{ind.title}</b> ({ind.unit}) — {ind.description}</p>
      {a && a.verdict !== 'insufficient' && (
        <p className="auto">자동 분석: {a.verdict === 'E' ? '장기 구조 변화(주기 아님)' : a.verdict === 'A' ? '통계적 주기 후보' : '일정한 주기 없음'} — {a.why}.
          {a.changePoint && ` 평균이 바뀐 해: ${a.changePoint.year}년(${a.changePoint.before}→${a.changePoint.after}${ind.unit}).`}</p>
      )}
      {a?.verdict === 'insufficient' && <p className="auto muted">자동 분석: {a.why}</p>}
      <div className="toggles">
        {a && (a.highEpisodes?.length || a.lowEpisodes?.length) ? <label><input type="checkbox" checked={showEp} onChange={(e) => setShowEp(e.target.checked)} /> 급변 구간 표시({a.episodeBasis})</label> : null}
        {ind.series.length > 1 && !ind.multi && <label><input type="checkbox" checked={others} onChange={(e) => setOthers(e.target.checked)} /> 미국·일본 함께 보기</label>}
      </div>
      <Chart ariaLabel={`${ind.title} 장기 추이`} unit={ind.unit} year={r.y} onPick={(y) => nav({ y })} series={series} bands={bands} markers={markers}
        trend={a?.verdict === 'E' && !ind.log ? a.trend : undefined} height={320} zero={!!ind.zeroLine} log={!!ind.log} />
      <div className="legend">
        {ind.multi ? series.map((x) => <span key={x.key}><i className="lg-line" style={{ background: x.color }} />{x.label}</span>) : <span><i className="lg-line" />{ind.title}</span>}
        {bands.length > 0 && <><span><i className="lg-hi" />{a?.episodeBasis} 크게 높았던 구간</span><span><i className="lg-lo" />{a?.episodeBasis} 크게 낮았던 구간</span></>}
        {markers.length > 0 && <span>▼▲ 자동 탐지한 고점·저점(누르면 그 해로)</span>}
        {a?.verdict === 'E' && !ind.log && <span><i className="lg-trend" />장기 추세선</span>}
        {ind.log && <span>세로축: 배수(로그) 눈금</span>}
        <span><i className="lg-sel" />선택 연도</span>
      </div>
      <SourceLine ids={ind.series.flatMap((s) => s.sourceIds)} extra={ind.note} />
      {markers.length > 0 && (
        <div className="tp">
          <b>전환점</b> {markers.map((m) => <button key={m.year + m.kind} className={`chip${m.year === r.y ? ' on' : ''}`} onClick={() => nav({ y: m.year })}>{m.year} {m.kind === 'peak' ? '고점' : '저점'}</button>)}
        </div>
      )}
    </>
  );
}


