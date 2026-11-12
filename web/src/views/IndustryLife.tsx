import { useState } from 'react';
import { D } from '../lib/data';
import type { Route } from '../lib/route';
import { GoChip, SLineView } from '../ui/Story';
import type { SLine, TFuture, TLine, TWorld } from '../lib/data';
import { ConclusionView, FuturesView, WorldBox } from './TopicView';

/** 산업 일대기 — 한 산업을 고르면 그 산업만 시작부터 지금까지 이어진다. 다른 산업과의 관계는 따로 표시. */
interface Stage { period: string; kind: string; what: string; why: SLine[]; from: SLine }
interface Ind { id: string; group: string; label: string; tracks: string; question: string; span: [number, number]; stages: Stage[]; profile: Record<string, SLine[]>; worlds: { at: string; box: TWorld }[]; outward: TLine[]; futures: { split: TLine; items: TFuture[] }; conclusion: { key: TLine; favored: TLine; undecided: TLine; next: TLine; change: TLine }; links: { year: string; to: string | null; rel: string; text: string; line: SLine; goFlow?: [string, string] }[] }
interface SelRow { label: string; status: '선정' | '후속' | '제외'; industry?: string; cells: Record<string, SLine>; note?: string }
interface Inds { selection: { criteria: { key: string; label: string }[]; rows: SelRow[] }; groups: { id: string; label: string; desc: string }[]; industries: Ind[]; pending: { group: string; label: string; note: string }[]; profile: { key: string; label: string }[] }

const X = (D as unknown as { industries: Inds }).industries;
const KIND_CLASS: Record<string, string> = { '이전 상태': 'k0', '시작': 'k1', '성장': 'k2', '확산': 'k2', '전환점': 'k3', '기술 변화': 'k3', '위기': 'k4', '재편': 'k5', '현재': 'k6' };
const startYear = (p: string) => Number((p.match(/\d{4}/) ?? ['0'])[0]);

export function IndustryLife({ nav, init }: { nav: (p: Partial<Route>) => void; init?: string }) {
  const [sel, setSel] = useState(init && X.industries.some((i) => i.id === init) ? init : X.industries[0].id);
  const [compare, setCompare] = useState(false);
  const ind = X.industries.find((i) => i.id === sel)!;
  return (
    <section className="panel indlife" id="indlife">
      <h2>산업 일대기 <span className="sub">산업 하나를 골라 시작부터 지금까지 — 다른 산업은 '만나는 지점'에서만 연결</span></h2>
      <Selection />
      <div className="il-pick">
        {X.groups.map((g) => {
          const items = X.industries.filter((i) => i.group === g.id);
          if (!items.length) return null;
          return (
            <div key={g.id} className="il-group">
              <span className="il-gl">{g.label}</span>
              {items.map((i) => <button key={i.id} className={`chip${sel === i.id && !compare ? ' on' : ''}`} aria-pressed={sel === i.id && !compare} onClick={() => { setSel(i.id); setCompare(false); }}>{i.label}</button>)}
            </div>
          );
        })}
        <button className={`chip${compare ? ' on' : ''}`} aria-pressed={compare} onClick={() => setCompare(!compare)}>여러 산업 같은 시간축으로 비교</button>
      </div>

      {compare ? <Compare onPick={(id) => { setSel(id); setCompare(false); }} /> : (
        <div className="il-one">
          <h3 className="il-q">{ind.question}</h3>
          <p className="small muted">추적 대상: {ind.tracks}</p>
          <ol className="il-stages">
            {ind.stages.map((s, i) => (
              <li key={i} className={`il-st ${KIND_CLASS[s.kind] ?? ''}`}>
                <p className="il-h"><span className="il-kind">{s.kind}</span> <span className="il-per">{s.period}</span></p>
                <p className="il-what"><b>무엇이 달라졌나</b> {s.what}</p>
                <div className="il-why"><b className="small">왜</b>{s.why.map((x, j) => <SLineView key={j} x={x} />)}</div>
                <div className="il-from"><b className="small">앞 단계와의 연결</b><SLineView x={s.from} /></div>
              </li>
            ))}
          </ol>

          <h3>세계시장과 한국 — 세계에서 무엇이 들어왔나</h3>
          <p className="small muted">무엇을 보나: 세계의 변화가 어떤 경로로 들어왔고, 한국 기업이 어떻게 대응해 어떤 결과가 났는지. 함께 움직였다는 것만으로 영향이라고 쓰지 않았습니다.</p>
          {ind.worlds.map((w) => <WorldBox key={w.at} w={w.box} at={w.at} />)}
          <h3>한국 산업이 밖으로 준 영향</h3>
          <div className="il-out">{ind.outward.map((x, j) => <SLineView key={j} x={x} />)}</div>

          <details className="il-profd"><summary>이 산업을 아홉 가지 항목으로 정리한 표</summary>
          <h3 className="sr-only">이 산업을 아홉 가지 항목으로</h3>
          <div className="tablewrap"><table className="tz-table il-prof">
            <tbody>{X.profile.map((p) => (
              <tr key={p.key}><th>{p.label}</th><td>{(ind.profile[p.key] ?? []).map((x, j) => <SLineView key={j} x={x} />)}</td></tr>
            ))}</tbody>
          </table></div>
          </details>

          <h3>다른 산업·생활과 만나는 지점 <span className="sub">이 산업의 단계를 대신하지 않습니다</span></h3>
          <ul className="il-links">
            {ind.links.map((l, i) => (
              <li key={i}>
                <span className="il-per">{l.year}</span> <span className="il-rel">{l.rel}</span> {l.text}
                <SLineView x={l.line} />
                {l.to && <button className="chip go" onClick={() => { setSel(l.to!); window.scrollTo({ top: (document.getElementById('indlife')?.offsetTop ?? 0) - 10, behavior: 'smooth' }); }}>{X.industries.find((x) => x.id === l.to)?.label} 일대기로 →</button>}
                {l.goFlow && <GoChip nav={nav} flow={l.goFlow[0]} step={l.goFlow[1]} />}
              </li>
            ))}
          </ul>
          <FuturesView id="il-future" f={ind.futures} title={`${ind.label} — 앞으로 가능한 방향`} />
          <ConclusionView id="il-end" c={ind.conclusion} />
        </div>
      )}

      {X.pending.length > 0 && (
        <details className="il-pending">
          <summary>작업 현황 — 아직 일대기를 쓰지 않은 산업 {X.pending.length}개</summary>
          <ul>{X.pending.map((p) => <li key={p.label}><b>{p.label}</b> — {p.note}</li>)}</ul>
        </details>
      )}
    </section>
  );
}

function Compare({ onPick }: { onPick: (id: string) => void }) {
  const a = Math.min(...X.industries.map((i) => i.span[0])), b = 2026;
  const W = 900, L = 120, top = 24, rowH = 40;
  const x = (y: number) => L + ((y - a) / (b - a)) * (W - L - 10);
  const ticks = [1960, 1970, 1980, 1990, 2000, 2010, 2020].filter((t) => t >= a);
  return (
    <>
      <p className="small">산업마다 한 줄입니다. 칸은 그 산업의 단계 시작 시점이고, 색은 단계 종류입니다. 이름을 누르면 그 산업의 일대기로 갑니다.</p>
      <div className="tz-tlwrap"><svg className="tz-tl il-cmp" viewBox={`0 0 ${W} ${top + X.industries.length * rowH + 10}`} role="img" aria-label="산업별 단계 비교">
        {ticks.map((t) => <g key={t}><line x1={x(t)} x2={x(t)} y1={top - 6} y2={top + X.industries.length * rowH} className="tick" /><text x={x(t)} y={14} className="tickl" textAnchor="middle">{t}</text></g>)}
        {X.industries.map((ind, r) => {
          const y = top + r * rowH + rowH / 2;
          return (
            <g key={ind.id}>
              <text x={L - 8} y={y + 4} textAnchor="end" className="lanel il-name" onClick={() => onPick(ind.id)} style={{ cursor: 'pointer' }}>{ind.label}</text>
              <line x1={L} x2={W - 10} y1={y} y2={y} className="laneline" />
              {ind.stages.map((s, i) => {
                const starts = ind.stages.map((t) => startYear(t.period) || 2025);
                const s0 = Math.max(s.kind === '이전 상태' ? starts[i] - 5 : starts[i], a);
                const s1 = i + 1 < ind.stages.length ? Math.max(starts[i + 1], s0 + 1) : b;
                return <rect key={i} x={x(s0) + 1} y={y - 11} width={Math.max(x(s1) - x(s0) - 2, 4)} height={22} rx={4} className={`ilk ${KIND_CLASS[s.kind] ?? ''}`}><title>{`${ind.label} ${s.period} ${s.kind}: ${s.what}`}</title></rect>;
              })}
            </g>
          );
        })}
      </svg></div>
      <p className="il-legend">{Object.entries({ '이전 상태': 'k0', 시작: 'k1', '성장·확산': 'k2', '전환점·기술 변화': 'k3', 위기: 'k4', 재편: 'k5', 현재: 'k6' }).map(([t, k]) => <span key={t}><i className={`ilk-i ${k}`} /> {t}</span>)}</p>
      <p className="small">같은 시간축에 놓으면 2014~2018년 조선의 위기와 2023~2025년 철강의 위기가 서로 다른 시기에, 반도체의 회복과 철강의 감산이 같은 시기에 일어났다는 것이 보입니다 — 산업마다 경기가 따로 움직입니다.</p>
    </>
  );
}

/** 어떤 산업을 왜 골랐나(R-IN1) — 기준별 근거가 있는 칸만 채우고, 후속·제외 이유를 밝힌다. */
function Selection() {
  const sel = X.selection;
  return (
    <details className="il-sel">
      <summary>어떤 산업을 왜 골랐나 — 선정 기준과 다음에 다룰 산업</summary>
      <p className="small">무엇을 보나: 한국 경제의 성장과 구조 변화에 기여한 정도를 다섯 기준으로 봤습니다. 근거를 찾은 칸만 채웠고, 빈칸은 '확인 전'입니다.</p>
      <div className="tablewrap"><table className="tz-table il-seltab">
        <thead><tr><th>산업</th><th>판정</th>{sel.criteria.map((c) => <th key={c.key}>{c.label}</th>)}</tr></thead>
        <tbody>{sel.rows.map((r) => (
          <tr key={r.label} className={`sel-${r.status}`}>
            <th>{r.label}{r.note && <p className="small muted">{r.note}</p>}</th>
            <td><span className={`il-stat s-${r.status}`}>{r.status}</span></td>
            {sel.criteria.map((c) => <td key={c.key}>{r.cells[c.key] ? <SLineView x={r.cells[c.key]} /> : <span className="muted small">확인 전</span>}</td>)}
          </tr>
        ))}</tbody>
      </table></div>
      <p className="small">읽어낼 것: 선정한 아홉 산업은 수출과 다른 산업으로 번진 영향이 크다는 공통점이 있습니다. 섬유·의류와 디스플레이는 수출 비중이 컸던 시기가 분명해 다음 일대기 후보이고, 경공업 일부는 지금 구조를 설명하는 비중이 작아 제외했습니다.</p>
    </details>
  );
}
