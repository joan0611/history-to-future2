import { D, topicById } from '../lib/data';

/** 지시서 3장 분야 A~J × 15장 9단계 상태. 값은 빌드 때 spec_fields.py가 실제 자료를 세어 계산한 것. */
const IND = (D.industries as unknown as { industries: { id: string; label: string }[] }).industries ?? [];
const HUE = ['#e5532d', '#2f8f6b', '#d39a1d', '#3b74d6', '#9a5bd6', '#c2414b', '#1f9bb3', '#6c8a2b', '#d0632d', '#c4479a'];
/** 분야 카드: 링은 9단계 중 통과한 비율, 아래 점 9개는 단계 순서. 누르면 아래 상세가 열린다. */
export function SpecCards({ compact = false }: { compact?: boolean }) {
  const S = D.spec;
  if (!S) return null;
  const open = (id: string) => {
    const el = document.getElementById(`specd-${id}`) as HTMLDetailsElement | null;
    if (el) { el.open = true; el.scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
    location.hash = '#/topic';
    window.setTimeout(() => { const d = document.getElementById(`specd-${id}`) as HTMLDetailsElement | null; if (d) { d.open = true; d.scrollIntoView({ block: 'center' }); } }, 300);
  };
  return (
    <div className={`spec-cards${compact ? ' compact' : ''}`} id={compact ? 'spec-cards-home' : 'spec-cards'}>
      {S.fields.map((f, k) => (
        <button key={f.id} type="button" className={`spec-card${f.passed === 9 ? ' full' : ''}`} style={{ ['--h' as string]: HUE[k % HUE.length], ['--p' as string]: `${(f.passed / 9) * 360}deg` }} onClick={() => open(f.id)} aria-label={`${f.id} ${f.label}: 9단계 중 ${f.passed}단계 통과`}>
          <span className="spec-ring"><b>{f.id}</b></span>
          <span className="spec-cl"><b>{f.label}</b><small>{f.passed === 9 ? '9단계 모두 통과' : `${f.passed}/9 · 남은 것: ${f.stages.filter((x) => !x.ok).map((x) => x.name).join(', ')}`}</small></span>
          {!compact && <span className="spec-dots" aria-hidden>{f.stages.map((x) => <i key={x.name} className={x.ok ? 'on' : ''} title={x.name} />)}</span>}
        </button>
      ))}
    </div>
  );
}

export function SpecStatus() {
  const S = D.spec;
  if (!S) return null;
  return (
    <section className="panel spec" id="spec-status">
      <h2>분야별 진행 상태 <span className="sub">경제·산업·에너지·기술·노동·정치·외교·사회·소비·문화 10개 분야 × 9단계 — 자료를 세어 자동 판정</span></h2>
      <p className="small muted">{S.note} 카드를 누르면 그 분야의 판정 근거와 읽을거리가 열립니다.</p>
      <SpecCards />
      <details className="spec-tabbox"><summary>9단계 표로 보기</summary>
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
      </details>
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
