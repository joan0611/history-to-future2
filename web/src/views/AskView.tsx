import { useEffect, useMemo, useState } from 'react';
import { ask, ALAYER_KO, type ALine } from '../lib/ask';
import { D } from '../lib/data';
import { pairTest, testable } from '../lib/pairtest';
import type { Route } from '../lib/route';

const EXAMPLES = [
  '한국의 자동차 산업과 반도체 산업은 성장 과정에서 어떤 공통점과 차이가 있었을까?',
  '물가와 실업률은 함께 움직였을까? 인과관계가 있을까?',
  '경제적 불확실성이 높아질 때 소비구조에는 어떤 변화가 반복되었을까?',
  '1990년대 출산율 하락의 원인은 무엇일까?',
  '앞으로 보험은 어떻게 바뀔 가능성이 있을까?',
];

const HKEY = 'htf2-ask-history';
function loadHist(): string[] { try { const v = JSON.parse(localStorage.getItem(HKEY) ?? '[]'); return Array.isArray(v) ? v.filter((x) => typeof x === 'string').slice(0, 10) : []; } catch { return []; } }
function saveHist(q: string): string[] { const h = [q, ...loadHist().filter((x) => x !== q)].slice(0, 10); try { localStorage.setItem(HKEY, JSON.stringify(h)); } catch { /* 저장 불가 환경 */ } return h; }
const PERIODS: [string, string][] = [['1960~1979년', '1960~1979년'], ['1980~1999년', '1980~1999년'], ['2000년 이후', '2000~2025년']];
const stripYears = (q: string) => q.replace(/\s*\((19|20)\d\d~(19|20)\d\d년\)\s*$/, '');

const fx = (x: number | null) => (x === null ? '계산 불가' : x.toFixed(2));
function PairPanel({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void }) {
  const opts = useMemo(() => testable(), []);
  const [a, setA] = useState(r.ta ?? 'cpi-kr'), [b, setB] = useState(r.tb ?? 'unemp-kr'), [c, setC] = useState(r.tc ?? ''), [f, setF] = useState(r.tf ? String(r.tf) : ''), [t, setT] = useState(r.tt ? String(r.tt) : '');
  const res = useMemo(() => (r.ta && r.tb ? pairTest(r.ta, r.tb, r.tc, r.tf, r.tt) : null), [r.ta, r.tb, r.tc, r.tf, r.tt]);
  const sel = (v: string, set: (x: string) => void, id: string, none?: string) => (
    <select id={id} value={v} onChange={(e) => set(e.target.value)}>{none !== undefined && <option value="">{none}</option>}{opts.map((i) => <option key={i.id} value={i.id}>{i.title}</option>)}</select>);
  return (
    <details className="ak-pair" id="ak-pair" open={!!r.ta}>
      <summary>두 지표를 직접 골라 검정하기 — 가설 만들기·반증하기</summary>
      <p className="muted small">내가 의심하는 두 현상이 함께 움직이는지, 공통 원인 때문은 아닌지 실제 연도별 자료로 계산합니다. 계산은 이 화면에서 바로 하며 결과는 주소에 남아 공유할 수 있습니다.</p>
      <form className="ak-pform" onSubmit={(e) => { e.preventDefault(); nav({ tab: 'ask', ta: a, tb: b, tc: c || undefined, tf: Number(f) || undefined, tt: Number(t) || undefined }); }}>
        <label>지표 A {sel(a, setA, 'ak-a')}</label>
        <label>지표 B {sel(b, setB, 'ak-b')}</label>
        <label>공통 원인 후보(통제) {sel(c, setC, 'ak-c', '통제하지 않음')}</label>
        <label>기간 <input id="ak-f" inputMode="numeric" size={5} placeholder="시작" value={f} onChange={(e) => setF(e.target.value)} />~<input id="ak-t" inputMode="numeric" size={5} placeholder="끝" value={t} onChange={(e) => setT(e.target.value)} /></label>
        <button type="submit" className="chip on">계산하기</button>
      </form>
      {res && 'error' in res && <p className="ak-warn">{res.error}</p>}
      {res && !('error' in res) && (
        <div className="ak-pres">
          <table className="ak-calc"><caption>{res.a.title} ↔ {res.b.title} <span className="muted">— 실제 연도별 자료, {res.years[0]}~{res.years[1]}년</span></caption><tbody>
            <tr><th>겹치는 해 / 변화 짝</th><td>{res.n}개 / {res.nd}개</td></tr>
            <tr><th>수준 상관</th><td>{fx(res.rLevel)}</td></tr>
            <tr><th>해마다 변화끼리 상관</th><td>{fx(res.rDiff)}{res.ci && ` (95% 신뢰구간 ${fx(res.ci[0])}~${fx(res.ci[1])})`}</td></tr>
            <tr><th>순열 검정 p값(2,000번)</th><td className="ak-p">{res.p === null ? '계산 불가' : res.p.toFixed(3)}</td></tr>
            <tr><th>시차별 변화 상관</th><td>{res.lags.map((l) => `${l.lag > 0 ? '+' : ''}${l.lag}년 ${fx(l.r)}`).join(' · ')}</td></tr>
            {res.c && <tr><th>{res.c.title} 통제 후(부분상관)</th><td className="ak-partial">{fx(res.rPartial)}{res.ciPartial && ` (95% ${fx(res.ciPartial[0])}~${fx(res.ciPartial[1])})`} · A↔통제 {fx(res.rAC)}, B↔통제 {fx(res.rBC)}</td></tr>}
            <tr><th>앞 절반 / 뒤 절반</th><td>{fx(res.first)} / {fx(res.second)}{res.split && ` (${res.split}년 기준)`}</td></tr>
          </tbody></table>
          <ul>{res.verdict.map((v, k) => <li key={k} className={`ak-line ak-${v.layer}`}><span className="ak-tag">{ALAYER_KO[v.layer]}</span> {v.text}</li>)}</ul>
          <p className="small muted">출처: {[res.a, res.b, res.c].filter(Boolean).map((i) => `${i!.title} — ${i!.series.flatMap((x) => x.sourceIds).map((sid) => D.sources[sid]?.publisher).filter(Boolean).filter((x, k, arr) => arr.indexOf(x) === k).join(', ')}`).join(' / ')}</p>
        </div>
      )}
    </details>
  );
}

function Line({ l }: { l: ALine }) {
  const srcs = l.ids.flatMap((id) => D.claims[id]?.sourceIds ?? (D.sources[id] ? [id] : [])).slice(0, 3).map((s) => D.sources[s]).filter(Boolean);
  return (
    <li className={`ak-line ak-${l.layer}`}>
      <span className="ak-tag">{ALAYER_KO[l.layer]}</span> {l.text}
      {l.go && <> <a href={l.go} className="ak-go">자세히</a></>}
      {srcs.length > 0 && <span className="ak-src"> — 출처: {srcs.map((s, k) => <a key={k} href={s.url} target="_blank" rel="noreferrer">{s.publisher}</a>).reduce<React.ReactNode[]>((a, x, k) => (k ? [...a, ', ', x] : [x]), [])}</span>}
    </li>
  );
}

export function AskView({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void }) {
  const [text, setText] = useState(r.q ?? '');
  const a = useMemo(() => (r.q ? ask(r.q) : null), [r.q]);
  const [hist, setHist] = useState<string[]>(() => loadHist());
  useEffect(() => { if (r.q) setHist(saveHist(r.q)); }, [r.q]);
  const go = (q: string) => { setText(q); nav({ tab: 'ask', q, why: undefined, path: [] }); };
  return (
    <section className="panel ak" id="ask">
      <h1>질문 분석</h1>
      <p className="muted">질문을 쓰면 앱 안의 근거 문장·사건·주제·산업·지표를 찾고, 지표가 있으면 실제로 계산해(요약, 두 지표의 상관·시차·기간별 안정성) 사실·관찰·해석·추론·가설을 나눠 보여 줍니다. <b>언어모델은 연결돼 있지 않습니다</b> — 규칙으로 근거를 모으고 계산하는 엔진이며, 근거가 모자라면 답 대신 필요한 자료를 알려 줍니다.</p>
      <form className="ak-form" onSubmit={(e) => { e.preventDefault(); if (text.trim()) go(text.trim()); }}>
        <textarea id="ak-q" rows={2} value={text} onChange={(e) => setText(e.target.value)} placeholder="예: 경제 위기 때 소비는 어떻게 바뀌었을까?" aria-label="질문" />
        <button type="submit" className="chip on">분석하기</button>
      </form>
      {!a && <div className="ak-ex"><p>예시 질문</p>{EXAMPLES.map((q) => <button key={q} className="chip" onClick={() => go(q)}>{q}</button>)}</div>}
      {hist.length > 0 && <details className="ak-hist" open={!a}><summary>최근 질문 ({hist.length}) — 이 브라우저에만 저장</summary><ul>{hist.map((q) => <li key={q}><button className="link" onClick={() => go(q)}>{q}</button></li>)}</ul></details>}
      {a && <p className="ak-again small">같은 질문을 기간을 좁혀 다시 묻기: {PERIODS.map(([lab, yy]) => <button key={lab} className="chip" onClick={() => go(`${stripYears(a.q)} (${yy})`)}>{lab}</button>)}</p>}
      <PairPanel r={r} nav={nav} />
      {a && (
        <div className="ak-res" data-enough={a.enough ? '1' : '0'}>
          <details className="ak-trace" open>
            <summary>엔진이 한 일</summary>
            <ol>{a.trace.map((t, k) => <li key={k}>{t}</li>)}</ol>
          </details>
          {!a.enough && <p className="ak-warn">근거 부족 — 이 질문에 답할 자료가 앱 안에 충분하지 않습니다. 아래 '추가 검증에 필요한 자료'를 확인하세요.</p>}
          {a.sections.map((s) => (
            <div key={s.key} className={`ak-sec ak-sec-${s.key}`}>
              <h3>{s.title}</h3>
              {s.key === 'data' && a.calcs.length > 0 && (
                <div className="ak-calcs">
                  {a.calcs.map((c, k) => (
                    <table key={k} className="ak-calc"><caption>{c.title} <span className="muted">— 방법: {c.method}</span></caption>
                      <tbody>{c.rows.map(([x, y]) => <tr key={x}><th>{x}</th><td>{y}</td></tr>)}</tbody></table>
                  ))}
                </div>
              )}
              {s.lines.length ? <ul>{s.lines.map((l, k) => <Line key={k} l={l} />)}</ul> : <p className="muted">{a.enough ? '이 항목에 해당하는 근거를 찾지 못했습니다.' : '근거가 부족해 쓰지 않았습니다.'}</p>}
            </div>
          ))}
          <details className="ak-hits"><summary>찾은 근거 목록 ({a.hits.length})</summary>
            <ul>{a.hits.map((h) => <li key={h.kind + h.id}><span className="ak-tag">{({ claim: '문장', topic: '주제', industry: '산업', event: '사건', indicator: '지표' } as const)[h.kind]}</span> {h.go ? <a href={h.go}>{h.label.slice(0, 80)}</a> : h.label.slice(0, 80)} <span className="muted">(일치 점수 {h.score})</span></li>)}</ul>
          </details>
        </div>
      )}
    </section>
  );
}
