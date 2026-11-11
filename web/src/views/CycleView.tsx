import { useEffect, useRef, useState } from 'react';
import { CATS, CAT_SHORT, D, isKR, nodesIn, type Analysis, type Finding, type Node } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine, type Band } from '../ui/Chart';
import { TYPE_SHORT } from './FieldView';

/**
 * ④ 반복·비교 — 엔진(data/build/cycles.py)이 사람의 지정 없이 모든 연간 지표를 분석한 결과.
 * 흥미도 순으로 정렬하되 신뢰도는 따로 표시(둘을 섞지 않음). 반복이 없다는 결과도 그대로 보여준다.
 */
const TYPE_DESC: Record<string, string> = {
  A: '여러 시차·주파수를 함께 본 순열 검정을 통과하고 관측 기간 안에 3번 이상 반복된 경우만',
  B: '같은 종류의 급변이 3번 이상 나타났지만 간격이 일정하지 않음 — 주기가 아님',
  C: '서로 다른 시기의 지표 궤적이 숫자상 닮음 — 원인이 같다는 뜻은 아님',
  D: '등장·확산·쇠퇴·재등장이 기록으로 확인됨 — 수치가 부족해 정성적 유사성',
  E: '순환이 아니라 한 방향으로 움직이는 장기 변화',
  N: '검정 결과 일정한 주기가 보이지 않음',
  R: '두 지표가 함께 움직이는 정도 — 인과가 아님',
};
const COLORS = ['var(--c-economy)', 'var(--c-politics)', 'var(--c-industry)', 'var(--c-society)', 'var(--c-culture)', 'var(--ink-3)', 'var(--c-flow)'];

export function CycleView({ r, nav, why }: { r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const [type, setType] = useState<string>('all');
  const list = D.findings.filter((f) => type === 'all' || f.type === type);
  const f = D.findings.find((x) => x.id === r.f) ?? list[0];
  const detail = useRef<HTMLDivElement>(null);
  useEffect(() => { if (r.f && window.innerWidth < 900) detail.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, [r.f]);
  const analyzed = D.analyses.length, usable = D.analyses.filter((a) => a.verdict !== 'insufficient').length;
  return (
    <div className="view">
      <section className="panel hero">
        <h2>반복과 비교 — 닮은 점, 다른 점, 그리고 한계</h2>
        <p className="lead">두 가지를 구분해 보여줍니다. <b>데이터 모양의 유사성</b>은 엔진이 연간 지표 {analyzed}개를 사람이 비교 대상을 정하지 않은 채 계산한 결과이고({usable}개는 계산 가능), <b>역사적 상황의 유사성</b>은 사람이 근거 문장을 대조해 정리한 비교입니다. 숫자의 모양이 닮았다고 원인이 같거나, 일정한 주기로 되풀이되거나, 다음 일을 예측할 수 있다는 뜻은 아닙니다.</p>
        <p className="small muted">신뢰도는 통계 판단이 얼마나 안정적인지를 뜻합니다. 그 결과가 역사적으로 얼마나 중요한지를 뜻하지 않습니다.</p>
        <div className="chips" role="group" aria-label="유형">
          <button className={`chip${type === 'all' ? ' on' : ''}`} onClick={() => setType('all')}>전체 {D.findings.length}</button>
          {Object.keys(TYPE_SHORT).filter((t) => D.findings.some((x) => x.type === t)).map((t) => (
            <button key={t} className={`chip${type === t ? ' on' : ''}`} onClick={() => setType(t)}><span className={`ftype t-${t}`}>{t}</span>{TYPE_SHORT[t]} {D.findings.filter((x) => x.type === t).length}</button>
          ))}
          {!D.findings.some((x) => x.type === 'A') && <span className="note">통계적 주기(A): 0건 — 이 자료에서는 확인되지 않았습니다</span>}
        </div>
      </section>

      <div className="cyc">
        <ol className="cyc-list" aria-label="발견 목록">
          {list.map((x, i) => (
            <li key={x.id}>
              <button className={x.id === f?.id ? 'on' : ''} onClick={() => nav({ f: x.id })}>
                <span className="rank">{i + 1}</span>
                <span className={`ftype t-${x.type}`}>{TYPE_SHORT[x.type]}</span>
                <b>{x.title}</b>
                <span className="cmeta"><span className={`conf k-${x.confidence.level}`}>신뢰도 {x.confidence.level}</span><span className={`cdot c-${x.category}`} />{CAT_SHORT[x.category]}{x.current && <span className="now">지금과 관련</span>}</span>
              </button>
            </li>
          ))}
        </ol>
        <div className="cyc-detail" ref={detail}>{f && <Detail f={f} r={r} nav={nav} why={why} />}</div>
      </div>

      <section className="panel">
        <h2>역사적 상황 비교 <span className="sub">사람이 근거 문장을 대조해 정리 — 측면마다 닮음·일부 닮음·다름</span></h2>
        {D.parallels.map((p) => (
          <details key={p.id} className="par">
            <summary><b>{p.title}</b> — {p.a.label}({p.a.years}) ↔ {p.b.label}({p.b.years}) <span className="muted">· 닮음 {p.rows.filter((x) => x.verdict === 'similar' || x.verdict === 'same').length} · 일부 {p.rows.filter((x) => x.verdict === 'partial').length} · 다름 {p.rows.filter((x) => x.verdict === 'different').length}</span></summary>
            <div className="tbl-wrap"><table className="tbl">
              <thead><tr><th>측면</th><th>{p.a.label}</th><th>{p.b.label}</th><th>판단</th></tr></thead>
              <tbody>{p.rows.map((x) => (
                <tr key={x.aspect}><td>{x.aspect}</td><td>{x.a.text}</td><td>{x.b.text}</td><td><b>{PV[x.verdict] ?? x.verdict}</b><br /><span className="muted small">{x.note}</span></td></tr>
              ))}</tbody>
            </table></div>
          </details>
        ))}
      </section>

      <section className="panel">
        <h2>엔진이 본 모든 지표 <span className="sub">반복이 없거나 계산할 수 없는 결과도 숨기지 않습니다</span></h2>
        <div className="tbl-wrap"><table className="tbl">
          <thead><tr><th>지표</th><th>기간</th><th>관측</th><th>판정</th><th>근거</th></tr></thead>
          <tbody>{D.analyses.map((a) => (
            <tr key={a.key}><td>{a.title} ({a.country})</td><td>{a.from}–{a.to}</td><td>{a.n}</td><td>{VERDICT[a.verdict]}</td><td className="muted">{a.why}</td></tr>
          ))}</tbody>
        </table></div>
        <p className="small muted">방법: 직선 추세를 먼저 분리 → 시차 1~20년 자기상관과 주기도(푸리에)를 무작위로 섞은 자료 {String(D.cycleParams.permutations)}개와 비교(시드 {String(D.cycleParams.seed)}, 여러 시차를 한꺼번에 본 검정) → 급변 구간({String(D.cycleParams.episodeRule)}) → 간격의 변동계수 → 5년 구간 궤적 비교. 인공 사인파·흰잡음·직선 추세로 엔진 자체를 검사합니다(tests/test_cycles.py).</p>
      </section>
    </div>
  );
}

const PV: Record<string, string> = { similar: '닮음', same: '닮음', partial: '일부 닮음', different: '다름', unknown: '확인 안 됨' };
const VERDICT: Record<string, string> = { A: '통계적 주기 후보', E: '장기 구조 변화', none: '주기 없음', insufficient: '자료 부족 — 계산 안 함' };

function Detail({ f, r, nav, why }: { f: Finding; r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const ser = f.series.map((k) => D.analyses.find((a) => a.key === k)).filter(Boolean) as Analysis[];
  const main = ser[0];
  const tone = f.title.includes('급락') ? 'lo' : 'hi';
  const bands: Band[] = f.periods.map(([a, b], i) => ({ from: a, to: b, tone: f.type === 'C' || f.type === 'D' ? 'cmp' : tone, label: f.type === 'C' ? (i ? 'B' : 'A') : undefined }));
  const ind = main ? D.indicators.find((i) => i.id === main.indicator) : undefined;
  return (
    <article className="panel">
      <div className="eyebrow"><span className={`ftype t-${f.type}`}>{f.type} · {TYPE_SHORT[f.type]}</span> <span className={`conf k-${f.confidence.level}`}>신뢰도 {f.confidence.level}</span></div>
      <h2>{f.title}</h2>
      <p className="lead">{f.summary}</p>
      <p className="note">이 유형의 뜻: {TYPE_DESC[f.type]}. 신뢰도 근거: {f.confidence.why}.</p>
      <Guide f={f} main={main} />

      {ser.map((a, i) => a.points && (
        <div key={a.key} className="cyc-chart">
          <h3>{a.title} ({a.country === 'KR' ? '한국' : a.country === 'US' ? '미국' : '일본'}) — 원본 자료{f.type === 'C' ? ' (비교 구간 A·B 강조)' : f.periods.length ? ' (해당 구간 강조)' : ''}</h3>
          <Chart ariaLabel={`${a.title} 원본`} unit={a.unit} year={r.y} onPick={(y) => nav({ y })} height={240} zero
            series={[{ key: a.key, label: a.title, color: COLORS[i], points: a.points }]} bands={bands}
            markers={(a.turningPoints ?? []).map((p) => ({ year: p.year, kind: p.kind }))} trend={a.verdict === 'E' ? a.trend : undefined} />
        </div>
      ))}
      {ind && <SourceLine ids={ind.series.flatMap((s) => s.sourceIds)} />}

      {f.periods.length >= 2 && (f.type === 'B' || f.type === 'D') && <Intervals f={f} />}
      {f.periods.length >= 2 && main?.points && (f.type === 'B' || f.type === 'C') && <Overlay f={f} ser={ser} />}
      {f.periods.length >= 2 && <Conditions f={f} why={why} />}
      {f.type === 'C' && f.current && <Current f={f} main={main} />}
      {main?.sensitivity && <Sensitivity a={main} />}
      {f.type === 'D' && <p className="note">문화 재유행은 차트·판매량 같은 연속 수치가 아직 없어 기록으로 확인된 단계만 비교합니다. 한 번의 재등장으로 '몇 년 주기'를 말하지 않습니다.</p>}
    </article>
  );
}

/** 읽는 법 — 무엇을 비교했고, 무엇이 닮았고, 무엇은 확인하지 않았으며, 이 결과로 말할 수 없는 것은 무엇인가 */
function Guide({ f, main }: { f: Finding; main?: Analysis }) {
  const ev = f.evidence as Record<string, unknown>;
  const what: Record<string, string> = {
    A: '추세를 뺀 값에서 같은 간격의 오르내림이 우연보다 강한지(순열 검정).',
    B: `${main?.title ?? '지표'}가 ${String(ev.basis ?? main?.episodeBasis ?? '기준')}보다 크게 벗어난 해를 ‘급변’으로 정하고, 그런 구간의 횟수와 간격.`,
    C: `두 5년 구간의 경제성장률·물가상승률 궤적(숫자 모양)을 표준화해 잰 거리. 사건·제도·국제 정세는 계산에 들어가지 않았습니다.`,
    D: '기록으로 확인된 단계(등장·확산·쇠퇴·재등장)의 순서. 수치는 비교하지 않았습니다.',
    E: '직선 추세가 변동을 얼마나 설명하는지와 평균이 바뀐 해.',
    N: '여러 시차·주기를 무작위로 섞은 자료와 비교한 주기 검정.',
    R: '추세를 뺀 두 지표가 몇 년 차이를 두고 함께 움직이는지(상관).',
  };
  const cannot: Record<string, string> = {
    A: '왜 그런 간격이 생기는지, 앞으로도 같은 간격일지.',
    B: `일정한 주기(간격이 들쭉날쭉${ev.cv != null ? `, 변동계수 ${String(ev.cv)}` : ''})나 다음 급변 시점. 급변 횟수가 적어 판단이 흔들릴 수 있습니다.`,
    C: '두 시기의 원인이 같다거나, 지금 이후가 과거처럼 흘러갈 것이라는 예측.',
    D: '재등장이 몇 년마다 온다는 주기 — 재등장 사례가 하나뿐입니다.',
    E: '이 흐름이 앞으로도 같은 기울기로 이어진다는 예측.',
    N: '이 지표에 반복이 전혀 없다는 단정(관측 기간 안에서 검정한 결과일 뿐).',
    R: '한 지표가 다른 지표를 움직였다는 인과.',
  };
  return (
    <dl className="guide">
      <dt>무엇을 비교했나</dt><dd>{what[f.type]}</dd>
      <dt>닮은 점(데이터)</dt><dd>{f.summary}</dd>
      <dt>확인하지 않은 것</dt><dd>그 시기를 만든 원인·제도·사람들의 생활이 같았는지는 계산하지 않았습니다.{f.periods.length >= 2 ? ' 아래 ‘조건 비교’에서 구간마다 정리된 사건을 직접 비교할 수 있습니다.' : ''}</dd>
      <dt>이 결과로 말할 수 없는 것</dt><dd>{cannot[f.type]}</dd>
    </dl>
  );
}

/** 반복 간격 — 구간 사이 거리를 막대로 */
function Intervals({ f }: { f: Finding }) {
  const ps = [...f.periods].sort((a, b) => a[0] - b[0]);
  const lo = ps[0][0], hi = ps[ps.length - 1][1];
  const X = (y: number) => ((y - lo) / Math.max(1, hi - lo)) * 100;
  return (
    <div className="intervals">
      <h3>반복 간격</h3>
      <div className="iv-bar">
        {ps.map(([a, b], i) => <span key={i} className="iv-ep" style={{ left: `${X(a)}%`, width: `${Math.max(1.2, X(b + 1) - X(a))}%` }} title={`${a}~${b}`} />)}
        {ps.slice(1).map(([a], i) => {
          const gap = a - ps[i][0];
          return <span key={i} className="iv-gap" style={{ left: `${X(ps[i][0])}%`, width: `${X(a) - X(ps[i][0])}%` }}>{gap}년</span>;
        })}
      </div>
      <div className="iv-years">{ps.map(([a, b], i) => <span key={i}>{a === b ? a : `${a}~${b}`}</span>)}</div>
    </div>
  );
}

/** 겹쳐 보기 — 각 구간의 시작 해를 0으로 맞춰 같은 축에. 단위가 같으면 원값, 다르면 표준화 값임을 표시 */
function Overlay({ f, ser }: { f: Finding; ser: Analysis[] }) {
  const pre = 2, post = 5;
  const lines: { label: string; pts: [number, number][] }[] = [];
  let normalized = false;
  if (f.type === 'B') {
    const a = ser[0];
    for (const [s] of f.periods) lines.push({ label: `${s}년 시작`, pts: (a.points ?? []).filter(([y]) => y >= s - pre && y <= s + post).map(([y, v]) => [y - s, v]) });
  } else {
    normalized = true;
    for (const a of ser) {
      const vs = (a.points ?? []).map((p) => p[1]);
      const mu = vs.reduce((x, y) => x + y, 0) / vs.length, sd = Math.sqrt(vs.reduce((x, y) => x + (y - mu) ** 2, 0) / vs.length);
      for (const [s, e] of f.periods) lines.push({ label: `${a.title.replace('한국 ', '').replace('실질 ', '')} ${s}~${e}`, pts: (a.points ?? []).filter(([y]) => y >= s && y <= e).map(([y, v]) => [y - s, Math.round(((v - mu) / sd) * 100) / 100]) });
    }
  }
  const x0 = f.type === 'B' ? -pre : 0, x1 = f.type === 'B' ? post : 4;
  return (
    <div className="cyc-chart">
      <h3>겹쳐 보기 <span className="sub">{f.type === 'B' ? '각 구간 시작 해 = 0, 원래 단위 그대로' : '구간 시작 = 0, 지표마다 평균 0·표준편차 1로 표준화한 값(단위 없음)'}</span></h3>
      <Chart ariaLabel="구간 겹쳐 보기" unit={normalized ? '' : ser[0].unit} height={220} x0={x0} x1={x1} eraBands={false} zero
        series={lines.map((l, i) => ({ key: l.label, label: l.label, color: COLORS[i % COLORS.length], points: l.pts }))} />
      <div className="legend">{lines.map((l, i) => <span key={l.label}><i className="lg-line" style={{ background: COLORS[i % COLORS.length] }} />{l.label}</span>)}</div>
    </div>
  );
}

/** 조건 비교 — 각 구간에 관계망에 정리된 사건을 분야별로 놓고, 모든 구간에 공통인 분야와 일부에만 있는 분야를 구분 */
function Conditions({ f, why }: { f: Finding; why: (id: string) => void }) {
  const cols = f.periods.map(([a, b]) => ({ p: [a, b] as [number, number], ns: nodesIn(a - 1, b + 1) }));
  const lanesOf = (ns: Node[]) => new Set(ns.map((n) => n.lane));
  const common = CATS.filter((c) => cols.every((x) => lanesOf(x.ns).has(c)));
  const intlCommon = cols.every((x) => x.ns.some((n) => !isKR(n)));
  const par = D.parallels.find((p) => f.periods.some(([a]) => p.a.years.includes(String(a)) || p.b.years.includes(String(a))));
  return (
    <div className="conds">
      <h3>결과뿐 아니라 조건도 반복됐나 <span className="sub">각 구간 ±1년에 정리된 사건 기준</span></h3>
      <p className="small">{common.length ? <>모든 구간에 함께 있는 분야: <b>{common.map((c) => CAT_SHORT[c]).join(', ')}</b>{intlCommon ? ' · 모든 구간에 국제 사건이 함께 있음' : ''}. </> : '모든 구간에 공통인 분야가 없습니다. '}
        분야가 같다고 원인이 같다는 뜻은 아닙니다 — 항목을 눌러 각각의 원인을 확인하세요.</p>
      <div className="conds-grid" style={{ gridTemplateColumns: `repeat(${Math.min(cols.length, 4)}, minmax(0, 1fr))` }}>
        {cols.slice(0, 8).map(({ p, ns }) => (
          <div key={p.join()}>
            <h4>{p[0] === p[1] ? p[0] : `${p[0]}~${p[1]}`}</h4>
            {ns.length ? <ul>{ns.sort((a, b) => a.importance - b.importance).slice(0, 5).map((n) => (
              <li key={n.id}><button className={`c-${n.lane}`} onClick={() => why(n.id)}><span className={`cdot c-${n.lane}`} />{n.label}{!isKR(n) && <em> (국제)</em>}</button></li>
            ))}</ul> : <p className="muted">이 구간에 정리된 사건이 아직 없음 — 조건 비교 불가</p>}
          </div>
        ))}
      </div>
      {par && <p className="small">사람이 정리한 비교 사례(근거 문장 대조)도 있습니다: <b>{par.title}</b> — {par.a.label} ↔ {par.b.label}. 자동 발견과는 별개입니다.</p>}
    </div>
  );
}

/** 현재와 비교 — 가장 닮은 과거 구간 '이후'에 실제로 일어난 일(사실)만 보여주고, 예측은 하지 않는다 */
function Current({ f, main }: { f: Finding; main?: Analysis }) {
  const past = f.periods[0];
  if (!main?.points) return null;
  const after = main.points.filter(([y]) => y > past[1] && y <= past[1] + 3);
  return (
    <div className="note current">
      <b>지금과 닮은 과거 다음에는 무슨 일이 있었나 (사실, 예측 아님)</b>
      <p>{past[0]}~{past[1]}년 다음 3년의 {main.title}: {after.map(([y, v]) => `${y}년 ${v}${main.unit}`).join(', ') || '자료 없음'}.</p>
      <p className="small">닮은 정도는 성장률·물가 두 지표의 5년 모양만 본 것입니다. 국제 정세·정책·산업구조가 다르면 다음 흐름도 다를 수 있습니다. 시나리오는 조건부로만 읽어 주세요.</p>
    </div>
  );
}

/** 분석 구간·방법을 바꾸면 결과가 어떻게 달라지나 */
function Sensitivity({ a }: { a: Analysis }) {
  return (
    <details className="sens">
      <summary>분석 구간·방법을 바꾸면? (민감도 {a.sensitivity!.length}가지)</summary>
      <div className="tbl-wrap"><table className="tbl">
        <thead><tr><th>구간</th><th>방법</th><th>관측</th><th>판정</th><th>p(시차)</th><th>p(주기도)</th></tr></thead>
        <tbody>{a.sensitivity!.map((s, i) => (
          <tr key={i}><td>{s.range[0]}–{s.range[1]}</td><td>{s.method ?? '직선 추세 제거'}</td><td>{s.n}</td><td>{VERDICT[s.verdict] ?? s.verdict}</td><td>{s.pAcf ?? '—'}</td><td>{s.pSpectral ?? '—'}</td></tr>
        ))}</tbody>
      </table></div>
      {a.periodicity && <p className="small muted">전체 기간: 가장 강한 시차 {a.periodicity.bestLag}년(|r|={a.periodicity.maxAbsAcf}, 기준선 ±{a.periodicity.band}), 주기도 최대 봉우리 약 {a.periodicity.spectralPeriod}년.</p>}
    </details>
  );
}
