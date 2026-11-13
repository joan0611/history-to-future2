import { D, type TLine } from '../lib/data';
import { SLineView } from './Story';

/** WHY FLOW 8단계 + 주체(동기·제약·대안) — data/build/why8.py. */
interface Actor { who: string; motive: TLine; constraint: TLine; alternative: TLine }
export interface W8Case { id: string; node: string; year: number; title: string; actors: Actor[]; [k: string]: unknown }
const W = (D as unknown as { why8?: { levels: { key: string; label: string }[]; cases: W8Case[] } }).why8;
export const why8ByNode: Record<string, W8Case> = Object.fromEntries((W?.cases ?? []).map((c) => [c.node, c]));
export const why8Cases = W?.cases ?? [];

export function Why8({ c }: { c: W8Case }) {
  if (!W) return null;
  return (
    <div className="why8" id={`w8-${c.id}`}>
      <h3>8단계로 보기 — {c.title}</h3>
      <ol className="w8-steps">
        {W.levels.map((lv, k) => (
          <li key={lv.key} className={`w8-${lv.key}`}>
            <b><span className="w8-n">{k + 1}</span>{lv.label}</b>
            {lv.key === 'actors' ? (
              <div className="tablewrap"><table className="tp-cmp w8-actors">
                <thead><tr><th>주체</th><th>무엇을 원했나(동기)</th><th>무엇에 막혔나(제약)</th><th>다른 선택지(대안)</th></tr></thead>
                <tbody>{c.actors.map((a) => <tr key={a.who}><th>{a.who}</th><td><SLineView x={a.motive} /></td><td><SLineView x={a.constraint} /></td><td><SLineView x={a.alternative} /></td></tr>)}</tbody>
              </table></div>
            ) : (
              <div>{(c[lv.key] as TLine[]).map((x, i) => <SLineView key={i} x={x} />)}</div>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}
