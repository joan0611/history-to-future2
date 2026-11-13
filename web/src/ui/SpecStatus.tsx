import { D, topicById } from '../lib/data';

/** 지시서 3장 분야 A~J × 15장 9단계 상태. 값은 빌드 때 spec_fields.py가 실제 자료를 세어 계산한 것. */
const IND = (D.industries as unknown as { industries: { id: string; label: string }[] }).industries ?? [];
export function SpecStatus() {
  const S = D.spec;
  if (!S) return null;
  return (
    <section className="panel spec" id="spec-status">
      <h2>분야별 진행 상태 <span className="sub">경제·산업·에너지·기술·노동·정치·외교·사회·소비·문화 10개 분야 × 9단계 — 자료를 세어 자동 판정</span></h2>
      <p className="small muted">{S.note} 칸에 마우스를 올리거나 행을 열면 판정 근거가 보입니다.</p>
      <div className="spec-wrap">
        <table className="spec-tab">
          <thead><tr><th>분야</th>{S.stages.map((s, k) => <th key={s} title={s}><span className="spec-n">{k + 1}</span><span className="spec-sn">{s}</span></th>)}<th>통과</th></tr></thead>
          <tbody>{S.fields.map((f) => (
            <tr key={f.id} id={`spec-${f.id}`}>
              <th>{f.id}. {f.label}</th>
              {f.stages.map((s) => <td key={s.name} className={s.ok ? 'spec-ok' : 'spec-no'} title={`${s.name}: ${s.basis}`}>{s.ok ? '●' : '○'}</td>)}
              <td className="spec-pass">{f.passed}/9</td>
            </tr>))}
          </tbody>
        </table>
      </div>
      <div className="spec-detail">{S.fields.map((f) => (
        <details key={f.id} className="spec-f" id={`specd-${f.id}`}>
          <summary><b>{f.id}. {f.label}</b> — 하위: {f.subs.join(' · ')} <span className="muted">(근거 문장 {f.counts.claims} · 사건 {f.members.events} · 지표 {f.counts.indicators})</span></summary>
          {f.members.topics.length > 0 && <p className="small">주제 이야기: {f.members.topics.map((t) => <a key={t} className="chip" href={`#/topic/${t}`}>{topicById[t]?.label.split(' — ')[0] ?? t}</a>)}</p>}
          {f.members.industries.length > 0 && <p className="small">산업 일대기: {f.members.industries.map((i) => <a key={i} className="chip" href={`#/field/industry?ind=${i}`}>{IND.find((x) => x.id === i)?.label ?? i}</a>)}</p>}
          {f.members.flows.length > 0 && <p className="small">변화 흐름: {f.members.flows.map((x) => <a key={x} className="chip" href={`#/flow/${x}`}>{D.flows.find((y) => y.id === x)?.topic ?? x}</a>)}</p>}
          {f.members.indicators.length > 0 && <p className="small">지표: {f.members.indicators.map((x) => { const i = D.indicators.find((y) => y.id === x); return i ? <a key={x} className="chip" href={`#/field/${i.category ?? 'economy'}?ind=${x}`}>{i.title}</a> : null; })}</p>}
          <ul className="small spec-basis">{f.stages.map((s) => <li key={s.name} className={s.ok ? 'spec-ok' : 'spec-no'}>{s.ok ? '통과' : '아직'} — {s.name}: {s.basis}</li>)}</ul>
          {f.gaps.length > 0 && <p className="small spec-gap">부족한 점 {f.gaps.length}개 — 다음 개발 대상</p>}
        </details>))}
      </div>
    </section>
  );
}
