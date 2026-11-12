import { useState } from 'react';
import { D, ECON_KO, flowById, type MechKind, type Study, type Synth } from '../lib/data';
import type { Route } from '../lib/route';
import { Chart, SourceLine } from '../ui/Chart';
import { Claims } from '../ui/WhyPanel';
import { SLineView } from '../ui/Story';

/**
 * 대표 경제 분석 화면.
 *   요약(지금 상태·근거·불확실·볼 지표) → 소비 자체의 추이 → 설명 변수(하나씩) → 핵심 주장 점검
 *   → 전달 과정(충격 종류별·근거 수준별) → 국면 비교(항목별 기준) → 시나리오 → 관찰 지표 → 원문 근거
 */

export function StatusChips({ s }: { s: Study }) {
  return (
    <span className="stchips">
      <span className="stc c-content" title="콘텐츠 작성 상태">작성 · {s.status.content}</span>
      <span className="stc c-evidence" title="근거 확인 상태">근거 · {s.status.evidence}</span>
      <span className="stc c-data" title="원자료 확보 상태">자료 · {s.status.data}</span>
      <span className="stc c-back" title="이후 자료로 판단을 대조했는지">사후 검증 · {s.status.backtest}</span>
    </span>
  );
}

export function SynthLine({ y }: { y: Synth }) {
  const [open, setOpen] = useState(false);
  return (
    <li className="synth">
      <p>{y.text} <span className="ct t-synthesis" title="사이트가 근거 문장을 묶어 쓴 해석">자료 종합</span> <button className="link small" onClick={() => setOpen(!open)}>{open ? '근거 접기' : `근거 ${y.claimIds.length}`}</button></p>
      {open && <Claims ids={y.claimIds} all />}
    </li>
  );
}

const MK_SHORT: Record<MechKind, string> = { effect: '연구 추정 효과', channel: '전달 경로', condition: '배경·조건', correlation: '상관', sequence: '시간 순서', interpretation: '해석', hypothesis: '가설' };
const SEC = ['요약', '소비 추이', '핵심 주장 점검', '전달 과정', '국면 비교', '시나리오', '관찰 지표', '근거'];

export function StudyDetail({ s, nav }: { s: Study; nav: (p: Partial<Route>) => void }) {
  const [ep, setEp] = useState<string>('all');
  const [edge, setEdge] = useState<number | null>(null);
  const [cell, setCell] = useState<string | null>(null);
  const [ex, setEx] = useState(s.explain[0]);
  const [pc, setPc] = useState(false);
  const scenName = Object.fromEntries(s.scenarios.map((x) => [x.id, x.name]));
  const watchById = Object.fromEntries(s.watch.map((w) => [w.id, w]));
  const allClaims = [...new Set([...s.findings, ...s.same, ...s.different, s.whyNow, s.summary.state, ...s.summary.basis, ...s.summary.uncertain].flatMap((y) => y.claimIds)
    .concat(s.rows.flatMap((x) => Object.values(x.cells).flatMap((c) => c[1]))).concat(s.mechanism.edges.flatMap((e) => e.claimIds)).concat(s.watch.flatMap((w) => w.claimIds)))];

  // 소비 자체의 추이(주 그래프) — 구간 평균은 같은 지표의 계단선으로만 겹친다
  const cs = pc ? s.consSeries.perCapita : s.consSeries.total;
  const steps: [number, number][] = s.consSeries.periods.flatMap(([a, b]) => {
    const v = cs.filter(([y]) => y >= a && y <= b).map(([, x]) => x);
    const m = v.reduce((p, q) => p + q, 0) / v.length;
    return [[a, m], [b, m]] as [number, number][];
  });
  const bands = s.chartNotes.map((n) => ({ from: n.year, to: n.year, tone: 'cmp' as const, label: n.label }));
  const exInd = D.indicators.find((i) => i.id === ex);
  const exSer = exInd?.series.find((x) => x.country === 'KR');

  // 전달 과정 그림 배치
  const W = 900, colX = [20, 340, 690], bw = 210, bh = 40;
  const cols = [0, 1, 2].map((c) => s.mechanism.nodes.filter((n) => n.col === c));
  const pos: Record<string, { x: number; y: number }> = {};
  cols.forEach((list, c) => {
    let y = 14;
    list.forEach((n, i) => {
      if (c === 0 && n.bg && !list[i - 1]?.bg) y += 26;
      pos[n.id] = { x: colX[c], y: c === 2 ? 210 : y };
      y += bh + 10;
    });
  });
  const H = Math.max(...Object.values(pos).map((p) => p.y)) + bh + 16;
  const on = (eps: string[]) => ep === 'all' || eps.includes(ep);
  const nodeOf = Object.fromEntries(s.mechanism.nodes.map((n) => [n.id, n]));

  return (
    <div className="view study">
      <nav className="crumbline"><button className="link" onClick={() => nav({ study: undefined })}>← 지금 판단하기</button></nav>

      {s.explainer && <ExplainerView e={s.explainer} asOf={s.asOf} />}

      <p className="ex-divider">아래부터는 위 설명의 근거를 자세히 보는 상세 분석입니다 — 소비 추이 그래프, 과거 위기와의 비교, 전달 과정, 시나리오, 지표.</p>

      <section className="panel hero" id="st-0">
        <div className="eyebrow"><StatusChips s={s} /> 최종 검토일 <b>{s.status.reviewed}</b></div>
        <h2 className="st-title">{s.title}</h2>
        <p className="st-sub">{s.subtitle}</p>
        <dl className="timeframe">
          <dt>자료 기준일</dt><dd>{s.timeframe.asOf}</dd>
          <dt>현재 관측 기간</dt><dd>{s.timeframe.observed}</dd>
          <dt>비교하는 과거</dt><dd>{s.timeframe.past}</dd>
          <dt>역사 연도 선택</dt><dd>{s.timeframe.history}</dd>
        </dl>
        <div className="sum4">
          <div className="sum-b"><h3>1 지금의 핵심 상태</h3><ul className="plain synths"><SynthLine y={s.summary.state} /></ul></div>
          <div className="sum-b"><h3>2 그 판단의 주요 근거</h3><ul className="plain synths">{s.summary.basis.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
          <div className="sum-b"><h3>3 아직 확실하지 않은 점</h3><ul className="plain synths">{s.summary.uncertain.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
          <div className="sum-b"><h3>4 앞으로 볼 지표</h3><ul className="plain">{s.summary.watchFirst.map((id) => <li key={id}><a href="#st-6" onClick={(e) => { e.preventDefault(); document.getElementById('st-6')?.scrollIntoView({ behavior: 'smooth' }); }}><b>{watchById[id].name}</b></a><br /><span className="small muted">{watchById[id].latest}</span></li>)}</ul></div>
        </div>
        <ol className="readorder mini">{SEC.slice(1).map((x, i) => <li key={x}><a href={`#st-${i + 1}`} onClick={(e) => { e.preventDefault(); document.getElementById(`st-${i + 1}`)?.scrollIntoView({ behavior: 'smooth' }); }}><b>{i + 1}</b>{x}</a></li>)}</ol>
        <details className="scope"><summary>분석 범위·상태 기준</summary>
          <dl><dt>대상</dt><dd>{s.scope.target}</dd><dt>기간</dt><dd>{s.scope.period}</dd><dt>변수</dt><dd>{s.scope.variable}</dd><dt>다루지 않는 것</dt><dd>{s.scope.notIncluded}</dd></dl>
          <table className="tbl small"><thead><tr><th>상태 축</th><th>단계</th><th>바뀌는 기준</th></tr></thead><tbody>{s.statusRules.map((x) => <tr key={x.axis}><td>{x.axis}</td><td>{x.levels}</td><td>{x.rule}</td></tr>)}</tbody></table>
        </details>
      </section>

      <section className="panel" id="st-1">
        <h2><span className="stepno">1</span> 소비 자체의 추이 <span className="sub">실질 민간소비, 연간 증가율(%)</span></h2>
        <p className="small"><label><input type="checkbox" checked={pc} onChange={(e) => setPc(e.target.checked)} /> 1인당으로 보기(인구 증가 효과 제외)</label></p>
        <Chart ariaLabel="실질 민간소비 증가율" unit="%" height={260} x0={1961} x1={2026}
          series={[{ key: 'cons', label: pc ? '1인당 실질 민간소비 증가율' : '실질 민간소비 증가율', color: 'var(--c-economy)', points: cs },
            { key: 'avg', label: '대한상의 구간 평균(같은 계열로 재계산)', color: 'var(--ink-3)', points: steps }]} bands={bands} />
        <div className="legend"><span><i className="lg-line" style={{ background: 'var(--c-economy)' }} />{pc ? '1인당 실질 민간소비 증가율' : '실질 민간소비 증가율'}</span><span><i className="lg-line" style={{ background: 'var(--ink-3)' }} />구간 평균(1988~96, 97~2002, 03~07, 08~19, 20~24)</span><span><i className="lg-band cmp" />위기 연도 표시(원인 표시 아님)</span></div>
        <SourceLine ids={s.consSeries.sourceIds} extra="1961~2025년 연간. 분기·월 값은 이 그래프에 넣지 않았습니다(아래 비교표에 기준을 붙여 따로 표시)." />
        <h3>설명 변수 — 하나씩 보기 <span className="sub">소비와 다른 지표라 같은 그래프에 겹치지 않습니다</span></h3>
        <div className="seg">{s.explain.map((id) => { const i = D.indicators.find((x) => x.id === id); return i ? <button key={id} className={`chip${ex === id ? ' on' : ''}`} onClick={() => setEx(id)}>{i.title.replace(/\(.*\)/, '')}</button> : null; })}</div>
        {exInd && exSer && <>
          <Chart ariaLabel={exInd.title} unit={exInd.unit} height={170} x0={1961} x1={2026} zero={exInd.unit === '%'}
            series={[{ key: ex, label: exInd.title, color: 'var(--c-politics)', points: exSer.points.map(([t, v]) => [Number(String(t).slice(0, 4)), v] as [number, number]) }]} bands={bands} />
          <SourceLine ids={exSer.sourceIds} extra={`${exInd.title} (${exInd.unit})`} />
        </>}
      </section>

      <section className="panel" id="st-2">
        <h2><span className="stepno">2</span> 핵심 주장 점검 <span className="sub">'충격 이후 소비 증가율이 매번 낮아졌다'는 말은 어디까지 맞나</span></h2>
        <div className="tbl-wrap"><table className="tbl">
          <thead><tr><th>구간</th><th>대한상의 보도</th><th>재계산(연평균, 기하)</th><th>단순 평균</th><th>위기·반등 연도 제외</th><th>1인당</th><th>같은 구간 GDP 성장률</th></tr></thead>
          <tbody>{s.periodTest.rows.map((x) => <tr key={x.period}><td>{x.period}</td><td>{x.reported}</td><td><b>{x.geo}</b></td><td>{x.arith}</td><td>{x.exCrisis}</td><td>{x.perCapita}</td><td>{x.gdp ?? '-'}</td></tr>)}</tbody>
        </table></div>
        <p className="small muted">위기 고정이 아닌 10년 단위: {s.periodTest.fixed.map((x) => `${x.period} ${x.arith}%(GDP ${x.gdp}%)`).join(' · ')}</p>
        <ul className="plain notes">{s.periodTestNote.map((x) => <li key={x}>{x}</li>)}</ul>
        <h3>확인된 핵심</h3>
        <ul className="plain synths">{s.findings.map((y) => <SynthLine key={y.text} y={y} />)}</ul>
        <details><summary>이번 점검에서 다시 확인한 주장 {s.audit.length}개</summary>
          <div className="tbl-wrap"><table className="tbl small audit"><thead><tr><th>주장</th><th>확인한 내용</th><th>결과</th><th>바꾼 것</th></tr></thead>
            <tbody>{s.audit.map((a) => <tr key={a.claim}><td>{a.claim}</td><td>{a.check}</td><td><span className={`au au-${a.result}`}>{a.result}</span></td><td>{a.change}</td></tr>)}</tbody></table></div>
        </details>
      </section>

      <section className="panel" id="st-3">
        <h2><span className="stepno">3</span> 전달 과정 <span className="sub">충격(왼쪽) → 경로(가운데) → 소비. 선의 모양 = 근거 수준</span></h2>
        <div className="seg">
          <button className={`chip${ep === 'all' ? ' on' : ''}`} onClick={() => setEp('all')}>모든 국면</button>
          {s.episodes.map((e) => <button key={e.id} className={`chip${ep === e.id ? ' on' : ''}`} onClick={() => setEp(e.id)}>{e.label}</button>)}
        </div>
        <div className="mechfig">
          <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label="소비에 이르는 전달 경로">
            <text x={colX[0]} y={10} className="mf-h">충격·배경</text><text x={colX[1]} y={10} className="mf-h">전달 경로</text><text x={colX[2]} y={200} className="mf-h">결과</text>
            {s.mechanism.edges.map((e, i) => {
              const a = pos[e.from], b = pos[e.to];
              const x1 = a.x + bw, y1 = a.y + bh / 2, x2 = b.x, y2 = b.y + bh / 2, mx = (x1 + x2) / 2;
              return <path key={i} d={`M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`} className={`mf-e k-${e.kind}${on(e.eps) ? '' : ' off'}${edge === i ? ' sel' : ''}`} onClick={() => setEdge(i)} />;
            })}
            {s.mechanism.nodes.map((n) => {
              const p = pos[n.id];
              const act = ep === 'all' || s.mechanism.edges.some((e) => on(e.eps) && (e.from === n.id || e.to === n.id));
              return <g key={n.id} className={`mf-n${n.bg ? ' bg' : ''}${n.col === 2 ? ' out' : ''}${act ? '' : ' off'}`} transform={`translate(${p.x},${p.y})`}>
                <rect width={bw} height={bh} rx={8} /><text x={10} y={17}>{n.label}</text><text x={10} y={32} className="mf-sub">{n.sub}</text></g>;
            })}
          </svg>
        </div>
        <div className="legend mk">{(Object.keys(MK_SHORT) as MechKind[]).filter((k) => s.mechanism.edges.some((e) => e.kind === k)).map((k) => <span key={k}><i className={`mk-l k-${k}`} />{MK_SHORT[k]} — <span className="muted">{s.mechanism.kinds[k]}</span></span>)}</div>
        <ul className="plain mech-list">
          {s.mechanism.edges.map((e, i) => on(e.eps) && (
            <li key={i} className={edge === i ? 'on' : ''}>
              <button className="link" onClick={() => setEdge(edge === i ? null : i)}><span className={`mkb k-${e.kind}`}>{MK_SHORT[e.kind]}</span> <b>{nodeOf[e.from].label} → {nodeOf[e.to].label}</b></button>
              <p className="small">{e.note}</p>
              {edge === i && <Claims ids={e.claimIds} all />}
            </li>
          ))}
        </ul>
      </section>

      <section className="panel" id="st-4">
        <h2><span className="stepno">4</span> 과거 국면과 지금 — 항목마다 같은 기준으로 <span className="sub">칸을 누르면 근거</span></h2>
        <div className="tbl-wrap"><table className="tbl cmp">
          <thead><tr><th>항목 · 기준</th>{s.episodes.map((e) => <th key={e.id} className={e.current ? 'cur' : ''}>{e.label}<br /><span className="muted small">{e.years}</span></th>)}</tr></thead>
          <tbody>{s.rows.map((row) => (
            <tr key={row.item}><td><b>{row.item}</b><br /><span className="small muted">{row.basis}</span>{row.gap && <><br /><span className="small gapnote">공백: {row.gap}</span></>}</td>{s.episodes.map((e) => {
              const [txt] = row.cells[e.id] ?? [''];
              const k = `${row.item}|${e.id}`;
              return <td key={e.id} className={e.current ? 'cur' : ''}>{txt ? <button className="cellbtn" onClick={() => setCell(cell === k ? null : k)}>{txt}</button> : <span className="muted small">확보 못 함</span>}</td>;
            })}</tr>
          ))}</tbody>
        </table></div>
        {cell && (() => { const [item, e2] = cell.split('|'); const row = s.rows.find((x) => x.item === item)!; return <div className="mech-ev"><p className="small"><b>{item} · {s.episodes.find((e) => e.id === e2)!.label}</b></p><Claims ids={row.cells[e2][1]} all /></div>; })()}
        <p className="small muted">연간 값과 분기·월 값은 같은 칸에서 순위로 비교하지 않습니다. 색은 '지금' 열 표시에만 씁니다.</p>
        <div className="two">
          <div><h3>지금과 같은 점</h3><ul className="plain synths">{s.same.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
          <div><h3>지금과 다른 점</h3><ul className="plain synths">{s.different.map((y) => <SynthLine key={y.text} y={y} />)}</ul></div>
        </div>
        <div className="whynow"><h3>그래서 지금 먼저 볼 것</h3><ul className="plain synths"><SynthLine y={s.whyNow} /></ul></div>
      </section>

      <section className="panel" id="st-5">
        <h2><span className="stepno">5</span> 조건별로 가능한 경로 <span className="sub">예측이 아닙니다 — 확률을 붙이지 않았습니다</span></h2>
        <div className="scen">
          {s.scenarios.map((x) => (
            <div key={x.id} className="scen-card">
              <h3>{x.name}</h3>
              <dl>
                <dt>성립 조건</dt><dd>{x.conditions}</dd>
                <dt>작동 과정</dt><dd>{x.path}</dd>
                <dt>영향받을 영역</dt><dd>{x.affected}</dd>
                <dt>시차·불확실성</dt><dd>{x.timing}</dd>
                <dt>성립하지 않게 되는 조건</dt><dd>{x.breaks}</dd>
                <dt>확인할 지표</dt><dd>{s.watch.filter((w) => w.supports.some(([id]) => id === x.id) || w.weakens.some(([id]) => id === x.id)).map((w) => w.name).join(' · ')}</dd>
              </dl>
              <details><summary className="small">이 시나리오의 근거 {x.basis.length}</summary><Claims ids={x.basis} all /></details>
            </div>
          ))}
        </div>
      </section>

      <section className="panel" id="st-6">
        <h2><span className="stepno">6</span> 앞으로 확인할 지표</h2>
        <div className="watchlist">
          {s.watch.map((w) => (
            <div key={w.id} className="wcard">
              <h3>{w.name}</h3>
              <p className="wlatest"><b>최신</b> {w.latest}</p>
              <dl>
                <dt>정의</dt><dd>{w.def}</dd>
                <dt>단위·비교 기준</dt><dd>{w.unit}</dd>
                <dt>출처·주기</dt><dd>{w.source}</dd>
                {w.threshold && <><dt>사용한 기준</dt><dd>{w.threshold}</dd></>}
                <dt>지지</dt><dd>{w.supports.map(([id, t]) => <span key={id + t} className="wsup"><b>{scenName[id]}</b> — {t}<br /></span>)}</dd>
                <dt>약화</dt><dd>{w.weakens.map(([id, t]) => <span key={id + t} className="wweak"><b>{scenName[id]}</b> — {t}<br /></span>)}</dd>
                <dt>단독 해석 주의</dt><dd>{w.caution}</dd>
              </dl>
              <details><summary className="small">근거</summary><Claims ids={w.claimIds} all /></details>
            </div>
          ))}
        </div>
        <h3>판단을 고쳐야 하는 신호</h3>
        <ul className="plain revise">{s.revise.map((x) => <li key={x}>{x}</li>)}</ul>
      </section>

      <section className="panel" id="st-7">
        <div className="two">
          <div><h2>다른 설명 가능성</h2><ul className="plain">{s.alternatives.map((x) => <li key={x}>{x}</li>)}</ul></div>
          <div><h2>이 분석의 한계</h2><ul className="plain gaps">{s.limits.map((x) => <li key={x}>{x}</li>)}</ul></div>
        </div>
        <h2>관련 변화 흐름</h2>
        <ul className="plain">{s.flows.map((f) => flowById[f] && <li key={f}><button className="link" onClick={() => nav({ tab: 'flow', flow: f })}>{flowById[f].question}</button> <span className={`econ e-${flowById[f].econ.status}`}>{ECON_KO[flowById[f].econ.status]}</span></li>)}</ul>
        <h2>근거 문장 전체 <span className="sub">출처·원문 위치·적용 기간과 한계</span></h2>
        <details><summary>{allClaims.length}개 펼치기</summary><Claims ids={allClaims} all /></details>
      </section>
    </div>
  );
}

function ExplainerView({ e, asOf }: { e: NonNullable<Study['explainer']>; asOf: string }) {
  const [ids, setIds] = useState<string[] | null>(null);
  return (
    <section className="panel ex" id="ex">
      <p className="eyebrow">지금 판단하기 · 자료 기준일 {asOf} (역사 연도 선택과 무관)</p>
      <h2 className="ex-q">{e.question}</h2>
      <p className="ex-short">{e.short} <button className="link small" onClick={() => setIds(ids ? null : e.shortIds)}>{ids ? '접기' : '근거 보기'}</button></p>
      {ids && <Claims ids={ids} all />}

      <figure className="ex-fig" aria-label={e.figure.title}>
        <figcaption><b>{e.figure.title}</b></figcaption>
        <ol className="ex-path">
          {e.figure.nodes.map((n, i) => (
            <li key={i} className={n.block ? 'block' : ''}><b>{n.t}</b><span>{n.s}</span></li>
          ))}
        </ol>
        <p className="ex-read">{e.figure.read}</p>
      </figure>

      {e.story.map((sec, i) => (
        <div key={i} className="ex-sec">
          <h3>{sec.h}</h3>
          {sec.intro && <p className="small muted">{sec.intro}</p>}
          {sec.lines.map((x, j) => <SLineView key={j} x={x} />)}
        </div>
      ))}

      <div className="ex-sec">
        <h3>숫자로 확인하기 — 무엇과 비교한 값인가</h3>
        <p className="small">{e.numbersRead}</p>
        <div className="tablewrap"><table className="tz-table ex-num">
          <thead><tr><th>무엇</th><th>값</th><th>비교 기준</th><th>다른 기준으로 보면</th><th>뜻</th></tr></thead>
          <tbody>{e.numbers.map((r) => <tr key={r.what}><th>{r.what}</th><td className="v">{r.value}</td><td>{r.base}</td><td>{r.alt}</td><td>{r.means}</td></tr>)}</tbody>
        </table></div>
      </div>

      <div className="ex-sec">
        <h3>판단이 달라질 조건과 다음에 볼 것</h3>
        {e.changes.map((x, j) => <SLineView key={j} x={x} />)}
        <h3>아직 확실하지 않은 것</h3>
        {e.unsure.map((x, j) => <SLineView key={j} x={x} />)}
      </div>

      <details className="ex-terms">
        <summary>용어 풀이 — 실질·전기 대비·민간소비·이전소득·평균소비성향·DSR</summary>
        <dl>{e.terms.map((t) => <div key={t.t}><dt>{t.t}</dt><dd>{t.d}</dd></div>)}</dl>
      </details>
    </section>
  );
}
