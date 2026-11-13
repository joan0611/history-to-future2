import { useEffect, useRef, useState } from 'react';
import { CATS, CAT_SHORT, D, isKR, nodesIn, type Analysis, type Finding, type Node } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine, type Band } from '../ui/Chart';
import { TYPE_SHORT } from './FieldView';
import { SLineView } from '../ui/Story';
import type { TLine, TRepeat } from '../lib/data';

/**
 * ④ 반복·비교 — 엔진(data/build/cycles.py)이 사람의 지정 없이 모든 연간 지표를 분석한 결과.
 * 흥미도 순으로 정렬하되 신뢰도는 따로 표시(둘을 섞지 않음). 반복이 없다는 결과도 그대로 보여준다.
 */
const TYPE_DESC: Record<string, string> = {
  A: '여러 시차·주파수를 함께 본 두 검정(적색잡음 대조)을 모두 통과하고 관측 기간 안에 3번 이상 반복된 경우만',
  W: '검정 하나만 통과했거나 추정 주기가 관측 기간 안에 3번 미만 — 주기로 판정하지 않고 보류',
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
        <p>이 화면은 두 종류의 반복을 따로 봅니다. 위쪽은 <b>이야기 속에서 찾은 반복</b>(재등장·반작용·반복되는 긴장 같은 문화·생활의 되풀이)이고, 아래쪽은 <b>숫자 모양의 반복</b>(통계 검정)입니다. 문화적 재등장을 통계적 주기로 읽지 않도록 섞지 않았습니다.</p>
        <p className="lead">두 가지를 구분해 보여줍니다. <b>데이터 모양의 유사성</b>은 엔진이 연간 지표 {analyzed}개를 사람이 비교 대상을 정하지 않은 채 계산한 결과이고({usable}개는 계산 가능), <b>역사적 상황의 유사성</b>은 사람이 근거 문장을 대조해 정리한 비교입니다. 숫자의 모양이 닮았다고 원인이 같거나, 일정한 주기로 되풀이되거나, 다음 일을 예측할 수 있다는 뜻은 아닙니다.</p>
        <p className="small muted">‘판정 안정성’은 통계 판단이 자료 길이·검정 결과로 볼 때 얼마나 흔들리지 않는지를 뜻합니다(사건의 확실성이 아님). 검정 일부만 통과한 결과는 ‘판정 보류’로만 표시합니다. 그 결과가 역사적으로 얼마나 중요한지를 뜻하지 않습니다.</p>
        <div className="chips" role="group" aria-label="유형">
          <button className={`chip${type === 'all' ? ' on' : ''}`} onClick={() => setType('all')}>전체 {D.findings.length}</button>
          {Object.keys(TYPE_SHORT).filter((t) => D.findings.some((x) => x.type === t)).map((t) => (
            <button key={t} className={`chip${type === t ? ' on' : ''}`} onClick={() => setType(t)}><span className={`ftype t-${t}`}>{t}</span>{TYPE_SHORT[t]} {D.findings.filter((x) => x.type === t).length}</button>
          ))}
          {!D.findings.some((x) => x.type === 'A') && <span className="note">통계적 주기(A): 0건 — 이 자료에서는 확인되지 않았습니다</span>}
        </div>
      </section>

      <RepeatIndex nav={nav} />

      <h2 className="cyc-h2" id="cyc-stats">숫자 모양의 반복 — 연간 지표 통계 검정</h2>
      <div className="cyc">
        <ol className="cyc-list" aria-label="발견 목록">
          {list.map((x, i) => (
            <li key={x.id}>
              <button className={x.id === f?.id ? 'on' : ''} onClick={() => nav({ f: x.id })}>
                <span className="rank">{i + 1}</span>
                <span className={`ftype t-${x.type}`}>{TYPE_SHORT[x.type]}</span>
                <b>{x.title}</b>
                <span className="cmeta"><span className={`conf k-${x.confidence.level}`}>{x.type === 'W' ? '판정 보류' : `판정 안정성 ${x.confidence.level}`}</span><span className={`cdot c-${x.category}`} />{CAT_SHORT[x.category]}{x.current && <span className="now">지금과 관련</span>}</span>
              </button>
            </li>
          ))}
        </ol>
        <div className="cyc-detail" ref={detail}>{f && <Detail f={f} r={r} nav={nav} why={why} />}</div>
      </div>

      <section className="panel">
        <h2>역사적 상황 비교 <span className="sub">같은 측면으로 여러 과거 사례를 대조 — 닮음·다름 판정은 처음 두 사례에 대해서만</span></h2>
        <p className="small muted">두 사례만 맞대면 ‘닮았다’는 판단이 쉽게 과장됩니다. 그래서 같은 측면으로 다른 사례(예: 2차 석유파동, 2026년 중동 사태)를 함께 놓았습니다. 빈칸은 자료를 연결하지 않은 곳입니다. 가계 소비를 기준으로 여섯 국면을 비교한 분석은 <a href="#/now/an-consumption">지금 판단하기</a>에 있습니다.</p>
        {D.parallels.map((p) => (
          <details key={p.id} className="par">
            <summary><b>{p.title}</b> — {p.a.label}({p.a.years}) ↔ {p.b.label}({p.b.years}) <span className="muted">· 닮음 {p.rows.filter((x) => x.verdict === 'similar' || x.verdict === 'same').length} · 일부 {p.rows.filter((x) => x.verdict === 'partial').length} · 다름 {p.rows.filter((x) => x.verdict === 'different').length}</span></summary>
            <div className="tbl-wrap"><table className="tbl">
              <thead><tr><th>측면</th><th>{p.a.label}<br /><span className="muted small">{p.a.years}</span></th><th>{p.b.label}<br /><span className="muted small">{p.b.years}</span></th><th>판단(앞 두 사례)</th>{(p.more ?? []).map((m) => <th key={m.label} className="more">{m.label}<br /><span className="muted small">{m.years} · 추가 사례</span></th>)}</tr></thead>
              <tbody>{p.rows.map((x) => (
                <tr key={x.aspect}><td>{x.aspect}</td><td>{x.a.text}</td><td>{x.b.text}</td><td><b>{PV[x.verdict] ?? x.verdict}</b><br /><span className="muted small">{x.note}</span></td>
                  {(p.more ?? []).map((m) => { const c = m.cells[x.aspect]; return <td key={m.label} className="more">{c && c[0] ? c[0] : <span className="muted small">자료 연결 안 함</span>}</td>; })}</tr>
              ))}</tbody>
            </table></div>
          </details>
        ))}
      </section>

      <section className="panel">
        <details className="aux"><summary><b>보조 자료 — 엔진이 본 모든 지표</b> <span className="sub">반복이 없거나 계산할 수 없는 결과도 숨기지 않습니다</span></summary>
        <div className="tbl-wrap"><table className="tbl">
          <thead><tr><th>지표</th><th>기간</th><th>관측</th><th>판정</th><th>근거</th></tr></thead>
          <tbody>{D.analyses.map((a) => (
            <tr key={a.key}><td>{a.title} ({a.country})</td><td>{a.from}–{a.to}</td><td>{a.n}</td><td>{VERDICT[a.verdict]}</td><td className="muted">{a.why}</td></tr>
          ))}</tbody>
        </table></div>
        <p className="small muted">방법: 직선 추세를 먼저 분리 → 시차 2~20년 자기상관과 주기도(푸리에)를 ‘같은 1차 자기상관을 가진 적색잡음’ 대조 {String(D.cycleParams.permutations)}개와 비교(시드 {String(D.cycleParams.seed)}, 여러 시차를 한꺼번에 본 검정, p=(넘은 수+1)/(대조 수+1)) → 두 검정을 모두 통과하고 관측 기간 안에 3회 이상 반복될 때만 ‘주기 후보’ → 하나만 통과하거나 반복이 3회 미만이면 ‘판정 보류’ → 급변 구간({String(D.cycleParams.episodeRule)}) → 간격의 변동계수 → 5년 구간 궤적 비교. 인공 사인파·흰잡음·적색잡음·직선 추세로 엔진 자체를 검사합니다(tests/test_cycles.py).</p>
        <p className="small muted">고친 점(2026-11-12): 이전에는 자료 순서를 무작위로 섞은 대조를 써서, 서서히 움직이는 수준 지표(예: 1975~2025 실질 주택가격 지수)가 p≈0으로 나오는데도 ‘우연 범위’라고 적히는 모순이 있었습니다. 대조를 적색잡음으로 바꾸고, 판정과 설명 문구가 어긋나지 않는지 자동 검사를 추가했습니다.</p>
        </details>
      </section>
      <CrossStructures why={why} />
    </div>
  );
}

/** 분야를 넘는 구조(지시서 7장·8-E): 원인 지도 연결에서 빌드 때 계산한 공통 원인·피드백. 새 연결을 만들지 않는다. */
function CrossStructures({ why }: { why: (id: string) => void }) {
  const G = (D as unknown as { graphX: { commonCauses: { cause: string; label: string; year: number; lanes: string[]; effects: { id: string; label: string; year: number; lane: string }[] }[]; feedbacks: { loop: string[]; labels: string[] }[]; kind7Counts: Record<string, number> } }).graphX;
  if (!G) return null;
  const LANE: Record<string, string> = { economy: '경제', industry: '산업', society: '사회', politics: '정치', culture: '문화', flow: '흐름' };
  return (
    <section className="panel" id="cyc-cross">
      <h2>분야를 넘는 구조 <span className="sub">원인 지도의 연결에서 자동 계산 — 공통 원인에 의한 동시 변화 · 서로 되먹이는 고리</span></h2>
      <p className="small muted">계산 규칙: 한 사건에서 2년 안에 서로 다른 분야의 사건 둘 이상으로 이어진 경우를 '공통 원인 후보'로, A→B와 B→A(또는 세 사건의 고리)가 함께 있는 경우를 '피드백'으로 셉니다. 연결 자체의 근거 수준은 사건 상세에서 확인하세요. 관계 유형 분포: {Object.entries(G.kind7Counts).map(([k, v]) => `${k} ${v}`).join(' · ')}</p>
      <h3>공통 원인 후보 {G.commonCauses.length}개</h3>
      <ul className="cyc-common">{G.commonCauses.map((c) => (
        <li key={c.cause}><button className="link" onClick={() => why(c.cause)}>{c.label} ({c.year})</button> → {c.effects.map((e, k) => <span key={e.id}>{k ? ', ' : ''}<button className="link" onClick={() => why(e.id)}>{e.label}</button> <span className="muted">[{LANE[e.lane] ?? e.lane} {e.year}]</span></span>)}</li>))}</ul>
      <h3>피드백 고리 {G.feedbacks.length}개</h3>
      <ul className="cyc-fb">{G.feedbacks.map((f) => <li key={f.loop.join()}>{f.labels.join(' ⇄ ')}</li>)}</ul>
    </section>
  );
}

const PV: Record<string, string> = { similar: '닮음', same: '닮음', partial: '일부 닮음', different: '다름', unknown: '확인 안 됨' };
const VERDICT: Record<string, string> = { A: '통계적 주기 후보', E: '장기 구조 변화', none: '주기 없음', weak: '주기 후보 — 판정 보류', insufficient: '자료 부족 — 계산 안 함' };

function Detail({ f, r, nav, why }: { f: Finding; r: Route; nav: (p: Partial<Route>) => void; why: (id: string) => void }) {
  const ser = f.series.map((k) => D.analyses.find((a) => a.key === k)).filter(Boolean) as Analysis[];
  const main = ser[0];
  const tone = f.title.includes('급락') ? 'lo' : 'hi';
  const bands: Band[] = f.periods.map(([a, b], i) => ({ from: a, to: b, tone: f.type === 'C' || f.type === 'D' ? 'cmp' : tone, label: f.type === 'C' ? (i ? 'B' : 'A') : undefined }));
  const ind = main ? D.indicators.find((i) => i.id === main.indicator) : undefined;
  return (
    <article className="panel">
      <div className="eyebrow"><span className={`ftype t-${f.type}`}>{f.type} · {TYPE_SHORT[f.type]}</span> <span className={`conf k-${f.confidence.level}`}>{f.type === 'W' ? '판정 보류' : `판정 안정성 ${f.confidence.level}`}</span></div>
      <h2>{f.title}</h2>
      <p className="lead">{f.summary}</p>
      <p className="note">이 유형의 뜻: {TYPE_DESC[f.type]}. 판정 근거: {f.confidence.why}.</p>
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
          <tr key={i}><td>{s.range[0]}–{s.range[1]}</td><td>{s.method ?? '직선 추세 제거'}</td><td>{s.n}</td><td>{VERDICT[s.verdict] ?? s.verdict}</td><td>{fmtP(s.pAcf)}</td><td>{fmtP(s.pSpectral)}</td></tr>
        ))}</tbody>
      </table></div>
      {a.periodicity && <p className="small muted">전체 기간: 가장 강한 시차 {a.periodicity.bestLag}년(|r|={a.periodicity.maxAbsAcf}, 기준선 ±{a.periodicity.band}), 주기도 최대 봉우리 약 {a.periodicity.spectralPeriod}년.</p>}
    </details>
  );
}

const fmtP = (p?: number) => p == null ? '—' : p < 0.001 ? '<0.001' : p < 0.1 ? String(Number(p.toFixed(3))) : p.toFixed(2);

/* ── 이야기 속 반복(R-CY1~CY6) ─────────────────────────────── */
const R_TYPES: { type: string; desc: string }[] = [
  { type: '재등장', desc: '사라졌던 선택이 다시 나타남 — 겉모양만인지 기능·동기도 같은지 따로 봅니다.' },
  { type: '반작용', desc: '앞의 유행·방식이 만든 불편에 맞서는 움직임.' },
  { type: '반복되는 긴장', desc: '같은 두 가치(예: 편리함과 비용)가 수단만 바꿔 계속 부딪힘.' },
  { type: '결합·변형', desc: '옛 형식이 새 기술·서비스와 섞여 다른 것이 됨.' },
  { type: '경제·산업 순환', desc: '수요·공급·가격·재고·인력이 늘었다 줄었다 함 — 간격이 일정하다는 뜻은 아님.' },
  { type: '장기 구조 변화', desc: '되풀이가 아니라 한 방향으로 움직이는 변화 — 반복처럼 보이는 착시를 막기 위해 함께 둡니다.' },
];
interface RCase { where: string; whereKind: 'topic' | 'industry' | 'flow'; whereId: string; rp: TRepeat }
function gatherRepeats(): RCase[] {
  const out: RCase[] = [];
  for (const t of D.topics.topics) for (const rp of t.repeats ?? []) out.push({ where: t.label, whereKind: 'topic', whereId: t.id, rp });
  const inds = (D.industries as { industries: { id: string; label: string; repeats?: TRepeat[] }[] }).industries ?? [];
  for (const i of inds) for (const rp of i.repeats ?? []) out.push({ where: `${i.label} 산업 일대기`, whereKind: 'industry', whereId: i.id, rp });
  for (const f of D.flows) for (const rp of (f as { repeats?: TRepeat[] }).repeats ?? []) out.push({ where: `${f.topic} 시대 흐름`, whereKind: 'flow', whereId: f.id, rp });
  return out;
}
/** 취향 흐름에서 재등장·변형으로 표시만 된 후보(비교표는 아직 없음) */
function gatherCandidates() {
  const lane = (f: { lanes: { id: string; label: string }[] }, id: string) => f.lanes.find((l) => l.id === id)?.label ?? id;
  return D.tastes.flows.flatMap((f) => f.moves.filter((m) => m.rel === 'revive' || m.rel === 'transform').map((m) => ({ flow: f.id, title: f.title, text: `${lane(f, m.from)} → ${lane(f, m.to)}`, rel: m.rel === 'revive' ? '재등장' : '결합·변형', year: m.year })));
}

function RepeatIndex({ nav }: { nav: (p: Partial<Route>) => void }) {
  const cases = gatherRepeats();
  const cands = gatherCandidates();
  const go = (c: RCase, at?: string) => {
    if (c.whereKind === 'topic') {
      nav({ tab: 'topic', topic: c.whereId, f: undefined });
      if (at) window.setTimeout(() => document.getElementById(`turn-${at}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 500);
    } else if (c.whereKind === 'flow') {
      nav({ tab: 'flow', flow: c.whereId, f: undefined });
      if (at) window.setTimeout(() => document.getElementById(`step-${at}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }), 600);
    } else nav({ tab: 'field', cat: 'industry', ind: c.whereId, f: undefined });
  };
  const atLabel = (c: RCase, a: string) => {
    if (c.whereKind === 'topic') { const tu = D.topics.topics.find((t) => t.id === c.whereId)?.turns.find((x) => x.id === a); return tu ? `${tu.years} ${tu.title}` : a; }
    if (c.whereKind === 'flow') { const st = D.flows.find((f) => f.id === c.whereId)?.steps.find((x) => x.id === a); return st ? `${st.period} ${st.title}` : a; }
    return a;
  };
  const Row = ({ h, x }: { h: string; x: TLine | TLine[] }) => <tr><th>{h}</th><td>{(Array.isArray(x) ? x : [x]).map((y, i) => <SLineView key={i} x={y} />)}</td></tr>;
  return (
    <section className="panel" id="cyc-story">
      <h2>이야기 속에서 찾은 반복 — 여섯 유형</h2>
      <p className="muted">무엇을 보나: 각 주제·산업 이야기를 쓰면서 발견한 되풀이를 유형별로 모았습니다. 사례마다 과거와 지금 <b>누가 왜</b> 골랐는지, 겉모양만 닮았는지 동기까지 같은지, 무엇이 바뀌었는지, '싫증 나서 반대가 유행'이 아닌 다른 설명, 그리고 반례를 함께 둡니다. 구간 버튼을 누르면 그 이야기의 해당 전환점으로 갑니다.</p>
      {R_TYPES.map(({ type, desc }) => {
        const xs = cases.filter((c) => c.rp.type === type);
        return (
          <div key={type} className="rp-type" id={`rp-${type}`}>
            <h3>{type} <span className="sub">{desc}</span></h3>
            {xs.length === 0 && <p className="small muted">이 유형으로 비교까지 정리한 사례는 아직 없습니다. 찾은 자료에서 이 유형이 확인되지 않았다는 뜻이며, 없다고 단정하는 것은 아닙니다.</p>}
            {xs.map((c) => (
              <details key={c.whereId + c.rp.title} className="rp-case">
                <summary><b>{c.rp.title}</b> <span className="muted small">· {c.where}{c.rp.interval ? ` · 간격 ${c.rp.interval}` : ''}</span></summary>
                <p className="rp-go">{c.rp.at.map((a, i) => <button key={a} className="chip go" onClick={() => go(c, a)}>{c.rp.at.length > 1 ? (i === 0 ? '과거 구간: ' : '지금 구간: ') : '해당 구간: '}{atLabel(c, a)} →</button>)}</p>
                <table className="tp-cmp"><tbody>
                  <Row h="과거 — 누가 왜" x={c.rp.past} />
                  <Row h="지금 — 누가 왜" x={c.rp.now} />
                  <Row h="겉모양만인가, 동기도 같은가" x={c.rp.alike} />
                  <Row h="무엇이 바뀌었나(가격·기술·매체·의미, 과거 불편의 해결)" x={c.rp.changed} />
                  <Row h="다른 설명" x={c.rp.alternatives} />
                  <Row h="반례·설명이 안 맞는 곳" x={c.rp.counter} />
                </tbody></table>
              </details>
            ))}
          </div>
        );
      })}
      {cands.length > 0 && (
        <details className="rp-cands">
          <summary>탐색 중인 후보 {cands.length}개 — 취향 흐름에서 재등장·변형으로 표시만 하고 아직 비교표를 만들지 않은 것</summary>
          <ul>{cands.map((c, i) => <li key={i}><span className="il-stat">{c.rel}</span> {c.title}: {c.text} <span className="muted small">{c.year}년 무렵</span> <button className="link small" onClick={() => nav({ tab: 'taste', taste: c.flow, f: undefined })}>그 흐름 보기 →</button></li>)}</ul>
        </details>
      )}
    </section>
  );
}
