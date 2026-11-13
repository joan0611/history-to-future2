import { D, flowById, topicById, type Indicator, type TFuture, type TLine } from '../lib/data';
import { pairTest } from '../lib/pairtest';
import type { Route } from '../lib/route';
import { SBadge, SLineView, LayerLegend } from '../ui/Story';

/**
 * 근거를 모아 구성한 판단 질문(지시서 1~14 질문 → 6단계 읽는 순서).
 * 새 사실을 쓰지 않는다. 앱 안의 흐름·주제·지표·미래를 질문에 맞춰 모으고, 지표는 실제 시계열에서 계산한다.
 * 1 질문 → 2 과거 흐름 → 3 조건과 연결 근거 → 4 현재와 과거 비교(수치·유사 국면) → 5 조건별 시나리오 → 6 관찰 지표·판단 수정
 */
type Nav = (p: Partial<Route>) => void;
export interface QStudy { id: string; q: string; short: string; flows: string[]; topics: string[]; inds: string[]; pair: [string, string]; limits: string[] }

export const QSTUDIES: QStudy[] = [
  { id: 'q-jobs', q: '기술 변화는 산업·직업·고용구조를 어떻게 바꿨고, AI는 어디까지 같은 길을 갈까?', short: '농업 → 제조업 → 서비스업으로 일자리가 옮겨 간 길과, 그 길이 AI에서 되풀이될지',
    flows: ['flow-jobs', 'flow-tech'], topics: ['work-style', 'work-learn', 'work-cert'], inds: ['emp-ag-kr', 'emp-mfg-kr', 'emp-svc-kr', 'wage-share-kr', 'internet-kr'], pair: ['internet-kr', 'emp-svc-kr'],
    limits: ['직업별 고용은 2013년 이후만 있고, AI 도입 이후의 직업별 고용 자료는 아직 연결하지 않았다.', '기술 보급과 고용 비중이 함께 움직여도 경기·인구 변화가 둘을 함께 움직였을 수 있어 인과로 보지 않는다.'] },
  { id: 'q-shop', q: '유통과 결제 방식의 변화는 소비와 사업 구조를 어떻게 바꿨나?', short: '매장 → 온라인·모바일, 현금 → 간편결제로 바뀌며 누가 얻고 누가 잃었나',
    flows: ['flow-shop'], topics: ['shop-channel', 'shop-pay', 'shop-own'], inds: ['online-kr', 'hhcons-kr', 'cons-mix-kr'], pair: ['online-kr', 'hhcons-kr'],
    limits: ['업태별 매출 비중의 연속 통계(1993년 이전)는 없다.', '온라인쇼핑 거래액 계열은 2001년부터라 그 이전은 사건으로만 본다.'] },
  { id: 'q-family', q: '인구·가구 구성의 변화는 주거와 소비 수요에 어떻게 이어지나?', short: '출산 감소·고령화·1인 가구 증가가 집과 지출을 어떻게 바꾸나',
    flows: ['flow-family', 'flow-city'], topics: ['city-home', 'life-alone', 'family-care'], inds: ['tfr-kr', 'aged-kr', 'one-person-kr', 'hsupply-kr', 'house-kr', 'cons-house-kr'], pair: ['one-person-kr', 'cons-house-kr'],
    limits: ['가구 구성별(1인·부부·자녀 가구) 소비 지출의 장기 계열은 연결하지 않았다.', '1인 가구 비율은 5년 단위 조사에서 온 해가 많아 해마다의 변화 계산은 표본이 작다.'] },
  { id: 'q-time', q: '노동시간과 생활시간의 변화는 여가·서비스 수요와 어떤 관계가 있었나?', short: '주 48시간 → 주5일 → 52시간 상한으로 줄어든 시간이 어디로 갔나',
    flows: ['flow-time', 'flow-leisure'], topics: ['life-rest', 'hobby-place', 'travel-abroad'], inds: ['cons-culture-kr', 'emp-svc-kr', 'gdppc-kr', 'carreg-kr'], pair: ['gdppc-kr', 'cons-culture-kr'],
    limits: ['생활시간조사의 여가 시간 연속 자료는 연결하지 않았다.', '여가 지출 비중은 소득이 늘어서인지 시간이 늘어서인지 이 자료만으로 나눌 수 없다.'] },
];
export const qById: Record<string, QStudy> = Object.fromEntries(QSTUDIES.map((q) => [q.id, q]));

const kr = (i: Indicator) => i.series.filter((s) => s.country === 'KR' || s.country.startsWith('KR-') || i.series.length === 1);
const at = (pts: [string, number][], y: number) => pts.find(([d]) => Number(String(d).slice(0, 4)) === y)?.[1];
const fmt = (v: number | undefined, u: string) => (v === undefined ? '자료 없음' : `${Math.abs(v) >= 100 ? Math.round(v).toLocaleString() : v.toFixed(1)}${u.length <= 2 ? u : ''}`);
const YS = [1980, 1990, 2000, 2010];

export function QuickStudy({ s, nav }: { s: QStudy; nav: Nav }) {
  const flows = s.flows.map((f) => flowById[f]).filter(Boolean);
  const topics = s.topics.map((t) => topicById[t]).filter(Boolean);
  const inds = s.inds.map((id) => D.indicators.find((i) => i.id === id)).filter((x): x is Indicator => !!x);
  const pr = pairTest(s.pair[0], s.pair[1]);
  const futs: { from: string; go: string; f: TFuture }[] = [
    ...topics.flatMap((t) => t.futures.items.map((f) => ({ from: t.label.split(' — ')[0], go: `#/topic/${t.id}`, f }))),
    ...flows.flatMap((fl) => (fl.futures?.items ?? []).map((f) => ({ from: fl.topic, go: `#/flow/${fl.id}`, f }))),
  ];
  const repeats = topics.flatMap((t) => (t.repeats ?? []).map((r) => ({ t, r })));
  const watch = [...new Set(futs.flatMap((x) => x.f.watch))];
  const revise = futs.flatMap((x) => x.f.against.map((a) => ({ a, from: x.f.name })));
  const keys: { from: string; go: string; x: TLine }[] = [
    ...flows.filter((f) => f.conclusion).map((f) => ({ from: f.topic, go: `#/flow/${f.id}`, x: f.conclusion!.key })),
    ...topics.map((t) => ({ from: t.label.split(' — ')[0], go: `#/topic/${t.id}`, x: t.conclusion.key })),
  ];
  return (
    <div className="view now qs" id={`qs-${s.id}`}>
      <p><button className="link" onClick={() => nav({ tab: 'now', study: undefined })}>← 지금 판단하기</button></p>
      <section className="panel" id="qs-1">
        <div className="eyebrow">판단 질문 · 앱 안의 근거를 모아 구성한 분석</div>
        <h2>{s.q}</h2>
        <p className="lead">{s.short}</p>
        <p className="muted small">이 분석은 새 문장을 쓰지 않고, 이미 출처가 붙은 흐름·주제·지표·미래 문장을 이 질문에 맞춰 모은 것입니다. 수치는 앱에 있는 실제 시계열에서 그 자리에서 계산합니다.</p>
        <LayerLegend />
        <ol className="readorder qs-steps">{['질문', '과거 흐름', '조건과 연결 근거', '현재와 과거 비교', '조건별 시나리오', '관찰 지표·판단 수정'].map((x, i) => <li key={x}><a href={`#qs-${i + 1}`} onClick={(e) => { e.preventDefault(); document.getElementById(`qs-${i + 1}`)?.scrollIntoView({ behavior: 'smooth' }); }}><b>{i + 1}</b>{x}</a></li>)}</ol>
      </section>

      <section className="panel" id="qs-2">
        <h2>② 관련된 과거의 변화 흐름</h2>
        <ul className="qs-list">{keys.map((k) => <li key={k.go}><a className="chip" href={k.go}>{k.from}</a> <SLineView x={k.x} /></li>)}</ul>
      </section>

      <section className="panel" id="qs-3">
        <h2>③ 변화를 움직인 조건과 연결 근거</h2>
        {topics.flatMap((t) => t.reasons.slice(0, 1).map((r) => (
          <article key={t.id} className="qs-reason">
            <h3>{r.title} <a className="small" href={`#/topic/${t.id}`}>({t.label.split(' — ')[0]})</a></h3>
            <div className="qs-r"><b>근거</b>{r.facts.map((f, k) => <SLineView key={k} x={f} />)}</div>
            <div className="qs-r"><b>연결 논리</b><SLineView x={r.logic} /></div>
            <div className="qs-r"><b>다른 설명</b>{r.rivals.map((f, k) => <SLineView key={k} x={f} />)}</div>
          </article>
        )))}
      </section>

      <section className="panel" id="qs-4">
        <h2>④ 현재와 과거의 비교</h2>
        <div className="tablewrap"><table className="tz-table qs-num">
          <thead><tr><th>지표</th>{YS.map((y) => <th key={y}>{y}</th>)}<th className="cur">가장 최근</th></tr></thead>
          <tbody>{inds.flatMap((i) => kr(i).map((se) => {
            const last = se.points[se.points.length - 1];
            return (
              <tr key={i.id + se.label}>
                <th><a href={`#/field/${i.category ?? 'economy'}?ind=${i.id}`}>{i.title}{kr(i).length > 1 ? ` — ${se.label}` : ''}</a> <span className="muted small">({i.unit})</span></th>
                {YS.map((y) => <td key={y}>{fmt(at(se.points, y), i.unit)}</td>)}
                <td className="cur">{last ? `${fmt(last[1], i.unit)} (${String(last[0]).slice(0, 4)})` : '자료 없음'}</td>
              </tr>
            );
          }))}</tbody>
        </table></div>
        {'error' in pr ? <p className="muted">{pr.error}</p> : (
          <div className="qs-pair">
            <p><SBadge l="observed" /> {pr.a.title}와 {pr.b.title}: 같은 해끼리 수준 상관 {pr.rLevel?.toFixed(2) ?? '계산 불가'}, 해마다 변화끼리 상관 {pr.rDiff?.toFixed(2) ?? '계산 불가'} ({pr.years[0]}~{pr.years[1]}년, {pr.n}개 해){pr.pBlock !== null ? `, 3년 묶음 순열 p=${pr.pBlock.toFixed(3)}` : ''}.</p>
            <p className="small muted"><SBadge l="unknown" /> 상관은 인과가 아니다. 두 지표 모두 긴 추세를 가지면 수준 상관이 커 보이므로 변화끼리의 상관을 함께 본다. <a href={`#/ask?ta=${s.pair[0]}&tb=${s.pair[1]}`}>통제 지표를 넣어 직접 검정하기 →</a></p>
          </div>
        )}
        {repeats.length > 0 && <>
          <h3>과거의 닮은 국면</h3>
          <div className="qs-rep">{repeats.map(({ t, r }) => (
            <article key={t.id + r.title}>
              <b>{r.title}</b> <span className="muted small">{r.type}{r.likeness ? ` · ${r.likeness}` : ''}</span>
              <div className="qs-r"><b>그때</b><SLineView x={r.past} /></div>
              <div className="qs-r"><b>지금</b><SLineView x={r.now} /></div>
              <div className="qs-r"><b>달라진 것</b><SLineView x={r.changed} /></div>
            </article>
          ))}</div>
        </>}
      </section>

      <section className="panel" id="qs-5">
        <h2>⑤ 조건별 향후 시나리오</h2>
        <p className="muted small">확률은 붙이지 않았습니다. 각 가능성의 기회와 위험을 함께 적었습니다.</p>
        <div className="qs-futs">{futs.map(({ from, go, f }) => (
          <article key={go + f.name} className="qs-fut">
            <h3><span className="tp-kind">{f.kind}</span> {f.name}{f.term && <span className={`tp-term ${f.term === '장기 구조' ? 'long' : 'short'}`}>{f.term}</span>}</h3>
            <p className="small muted"><a href={go}>{from}</a></p>
            <SLineView x={f.change} as="scenario" />
            <div className="qs-r"><b>기회</b><SLineView x={f.demand} /></div>
            {f.risk && <div className="qs-r tp-risk"><b>위험</b><SLineView x={f.risk} as="scenario" /></div>}
          </article>
        ))}</div>
      </section>

      <section className="panel" id="qs-6">
        <h2>⑥ 앞으로 관찰할 지표와 판단을 바꿀 신호</h2>
        <div className="qs-watch"><div><h3>볼 지표</h3><ul>{watch.map((w) => <li key={w}>{w}</li>)}</ul></div>
          <div><h3>이것이 보이면 판단을 고친다</h3><ul>{revise.map((r, k) => <li key={k}>{r.a} <span className="muted small">({r.from})</span></li>)}</ul></div></div>
        <h3>이 분석의 한계</h3>
        <ul>{s.limits.map((l) => <li key={l}><SBadge l="unknown" /> {l}</li>)}</ul>
      </section>
    </div>
  );
}
