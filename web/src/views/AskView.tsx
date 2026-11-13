import { useMemo, useState } from 'react';
import { ask, ALAYER_KO, type ALine } from '../lib/ask';
import { D } from '../lib/data';
import type { Route } from '../lib/route';

const EXAMPLES = [
  '한국의 자동차 산업과 반도체 산업은 성장 과정에서 어떤 공통점과 차이가 있었을까?',
  '물가와 실업률은 함께 움직였을까? 인과관계가 있을까?',
  '경제적 불확실성이 높아질 때 소비구조에는 어떤 변화가 반복되었을까?',
  '1990년대 출산율 하락의 원인은 무엇일까?',
  '앞으로 보험은 어떻게 바뀔 가능성이 있을까?',
];

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
