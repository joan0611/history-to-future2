import { useEffect, useRef, useState } from 'react';
import { CAT_KO, CLAIM_KO, COUNTRY_KO, D, STATUS_KO, VERIF_KO, byId, inc, lead, out, reliability, type Edge, type Node, type Rel } from '../lib/data';
import type { Route } from '../lib/route';

/**
 * WHY — 어느 화면에서든 항목을 누르면 열리는 공통 원인·결과 탐색.
 * 순서: 핵심 요약 → 원인·결과 연결(누르면 한 단계 더) → 선택한 연결의 설명 → 근거(출처 원문 링크)
 * 원인으로 확인된 관계 / 해석 / 시간적 선후를 항상 구분해 표시한다.
 */
const REL_ORDER: Rel[] = ['background', 'trigger', 'cause', 'influence', 'similar', 'sequence'];

export function WhyPanel({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void }) {
  const n = r.why ? byId[r.why] : undefined;
  const panel = useRef<HTMLElement>(null);
  useEffect(() => { panel.current?.scrollTo({ top: 0 }); panel.current?.focus(); }, [r.why]);
  useEffect(() => {
    const k = (e: KeyboardEvent) => { if (e.key === 'Escape') nav({ why: undefined, path: [], rel: undefined }); };
    window.addEventListener('keydown', k);
    return () => window.removeEventListener('keydown', k);
  });
  if (!n) return null;
  const go = (id: string) => nav({ why: id, path: [...r.path, id].slice(-12), rel: undefined });
  const causes = group(inc[n.id], 'from');
  const results = group(out[n.id], 'to');
  const sel = r.rel ? D.edges.find((e) => e.id === r.rel) : undefined;
  const related = D.findings.filter((f) => f.periods.some(([a, b]) => n.year >= a - 1 && n.year <= b + 1) && f.type !== 'N' && f.type !== 'E').slice(0, 4);
  const pars = D.parallels.filter((p) => p.rows.some((x) => [...x.a.claimIds, ...x.b.claimIds].some((c) => n.claimIds.includes(c))));
  const life = D.chains.filter((c) => c.kind === 'signal' && c.steps.some((s) => s.nodeId === n.id));
  const resp = D.chains.filter((c) => c.steps.some((s) => s.nodeId === n.id)).flatMap((c) => c.countryResponses ?? []);
  const docs = (n.docIds ?? []).map((id) => D.docs[id]).filter(Boolean);

  return (
    <div className="why-wrap" onClick={() => nav({ why: undefined, path: [], rel: undefined })}>
      <aside className="why" ref={panel} tabIndex={-1} onClick={(e) => e.stopPropagation()} role="dialog" aria-label={`${n.label} — 원인과 결과`}>
        <header className="why-top">
          <div className="why-nav">
            {r.path.length > 1 && <button className="btn sm ghost" onClick={() => { const p = r.path.slice(0, -1); nav({ why: p[p.length - 1], path: p, rel: undefined }); }}>← 이전 단계</button>}
            <button className="btn sm ghost close" onClick={() => nav({ why: undefined, path: [], rel: undefined })} aria-label="닫기">닫기 ✕</button>
          </div>
          {r.path.length > 1 && (
            <ol className="crumbs" aria-label="탐색 경로">
              {r.path.map((id, i) => byId[id] && (
                <li key={id + i}>{i === r.path.length - 1 ? <b>{byId[id].label}</b> : <button className="link" onClick={() => nav({ why: id, path: r.path.slice(0, i + 1), rel: undefined })}>{byId[id].label}</button>}</li>
              ))}
            </ol>
          )}
        </header>

        <section className="why-sum">
          <div className="eyebrow"><span className={`cdot c-${n.lane}`} />{CAT_KO[n.lane]} · {D.typeKo[n.nodeType] ?? '현상'} · {n.yearPrecision === 'era' ? `${n.eraId.replace('s', '년대')}(연도 불명확)` : n.year < 1960 ? `${n.year} — 1960년 이전 배경` : `${n.year}년`}</div>
          <h2>{n.label}</h2>
          <p className="why-lead">{lead(n, 220)}</p>
          <p className="meta">{n.countries.map((c) => COUNTRY_KO[c] ?? c).join(' · ') || '국가 정보 없음'} · 근거 {n.claimIds.length}개 · 교차검증 {Math.round(reliability(n) * 100)}%</p>
        </section>

        <section className="why-map" aria-label="원인과 결과">
          <Column title="무엇이 이것을 낳았나" empty="연결된 원인 근거가 아직 없습니다. 근거 없이 선을 긋지 않습니다." groups={causes} side="from" onGo={go} onRel={(id) => nav({ rel: r.rel === id ? undefined : id })} relSel={r.rel} />
          <div className="why-center" aria-hidden><span>↓</span><b>{n.label}</b><span>↓</span></div>
          <Column title="이것이 무엇을 바꾸었나" empty="연결된 결과 근거가 아직 없습니다." groups={results} side="to" onGo={go} onRel={(id) => nav({ rel: r.rel === id ? undefined : id })} relSel={r.rel} />
        </section>

        {sel && (
          <section className="why-rel" aria-live="polite">
            <h3>{byId[sel.from]?.label} → {byId[sel.to]?.label}</h3>
            <p><RelTag e={sel} />{sel.rel === 'sequence' && <span className="muted"> 앞뒤 순서만 정리한 것으로 인과를 주장하지 않습니다.</span>}{sel.verification === 'hypothesis' && <span className="muted"> 검증되지 않은 연결입니다.</span>}</p>
            {sel.note && <p><b>작동 원리</b> {sel.note}</p>}
            <Claims ids={sel.claimIds} />
          </section>
        )}

        {(life.length > 0 || resp.length > 0 || related.length > 0 || pars.length > 0) && (
          <section className="why-more">
            {life.map((c) => (
              <div key={c.id}><h3>흐름의 생애 — {c.title}</h3>
                <ol className="life">{c.steps.map((s) => <li key={s.nodeId} className={s.nodeId === n.id ? 'on' : ''}><button className="link" onClick={() => s.nodeId !== n.id && go(s.nodeId)}><b>{s.stageLabel}</b> {byId[s.nodeId]?.label}</button></li>)}</ol>
              </div>
            ))}
            {resp.length > 0 && <><h3>나라마다 어떻게 대응했나</h3><ul className="plain">{resp.map((x, i) => <li key={i}><b>{COUNTRY_KO[x.country] ?? x.country}</b> {x.situation}</li>)}</ul></>}
            {(related.length > 0 || pars.length > 0) && <h3>다른 시대에도 비슷한 일이 있었나</h3>}
            <ul className="plain">
              {related.map((f) => <li key={f.id}><a href={`#/cycle?f=${f.id}&y=${n.year}`}>자동 발견: {f.title}</a> <span className="muted">· 신뢰도 {f.confidence.level}</span></li>)}
              {pars.map((p) => <li key={p.id}>비교 사례: {p.title} — {p.a.label} ↔ {p.b.label}</li>)}
            </ul>
          </section>
        )}

        <section className="why-ev">
          <h3>근거</h3>
          <Claims ids={n.claimIds} />
          {docs.length > 0 && <><h4>당시 1차 사료</h4><ul className="plain">{docs.map((d) => <li key={d.id}><a href={d.url} target="_blank" rel="noreferrer">{d.publication} {d.publishedDate} — {d.title}</a> <span className="muted">· {ACCESS[d.verification.accessLevel] ?? d.verification.accessLevel}</span></li>)}</ul></>}
        </section>
      </aside>
    </div>
  );
}

const ACCESS: Record<string, string> = { original: '원문 직접 확인', archive_metadata: '아카이브 제목·메타데이터만 확인', secondary: '2차 자료로 확인', unverified: '미확인' };

function group(es: Edge[], side: 'from' | 'to') {
  const g: Record<string, Edge[]> = {};
  for (const e of es) (g[side === 'from' ? e.from : e.to] ??= []).push(e);
  const rank = (x: Edge[]) => Math.min(...x.map((e) => REL_ORDER.indexOf(e.rel)));
  return Object.entries(g).filter(([id]) => byId[id]).sort((a, b) => rank(a[1]) - rank(b[1])).map(([id, x]) => ({ n: byId[id], es: x }));
}

function Column({ title, empty, groups, side, onGo, onRel, relSel }: {
  title: string; empty: string; groups: { n: Node; es: Edge[] }[]; side: 'from' | 'to'; onGo: (id: string) => void; onRel: (id: string) => void; relSel?: string;
}) {
  const [all, setAll] = useState(false);
  const shown = all ? groups : groups.slice(0, 6);
  return (
    <div className={`why-col ${side}`}>
      <h3>{title} <span className="muted">{groups.length}</span></h3>
      {groups.length === 0 ? <p className="muted empty">{empty}</p> : (
        <ul>
          {shown.map(({ n, es }) => (
            <li key={n.id} className={`why-item c-${n.lane}`}>
              <button className="why-go" onClick={() => onGo(n.id)}>
                <span className="why-y">{n.yearPrecision === 'era' ? n.eraId.replace('s', '년대') : n.year < 1960 ? `${n.year}·이전` : n.year}</span>
                <span className="why-l">{n.label}</span>
                <span className="why-deg">{(inc[n.id].length + out[n.id].length) > 1 ? `더 깊이 ${inc[n.id].length + out[n.id].length - 1} →` : '→'}</span>
              </button>
              <span className="why-tags">{es.map((e) => <button key={e.id} className={`rel-btn${relSel === e.id ? ' on' : ''}`} onClick={() => onRel(e.id)} aria-label="이 연결의 설명 보기"><RelTag e={e} /></button>)}</span>
            </li>
          ))}
        </ul>
      )}
      {groups.length > 6 && <button className="link" onClick={() => setAll(!all)}>{all ? '줄이기' : `${groups.length - 6}개 더`}</button>}
    </div>
  );
}

export function RelTag({ e }: { e: Edge }) {
  return <><span className={`rel r-${e.rel}`}>{D.relKo[e.rel]}</span><span className={`ver v-${e.verification}`}>{VERIF_KO[e.verification]}</span></>;
}

export function Claims({ ids }: { ids: string[] }) {
  const [open, setOpen] = useState(false);
  const cs = ids.map((id) => D.claims[id]).filter(Boolean);
  const shown = open ? cs : cs.slice(0, 3);
  return (
    <ul className="claims">
      {shown.map((c) => (
        <li key={c.id}>
          <p>{c.text}</p>
          <p className="claim-meta"><span className={`ct t-${c.claimType}`}>{CLAIM_KO[c.claimType]}</span> <span className={`st s-${c.status}`}>{STATUS_KO[c.status]}</span>
            {c.sourceIds.map((s) => D.sources[s]).filter(Boolean).map((s) => <a key={s.id} href={s.url} target="_blank" rel="noreferrer" title={s.title}>{s.publisher}</a>)}</p>
        </li>
      ))}
      {cs.length > 3 && <li><button className="link" onClick={() => setOpen(!open)}>{open ? '접기' : `근거 ${cs.length - 3}개 더`}</button></li>}
    </ul>
  );
}
