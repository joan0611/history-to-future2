import { useEffect, useMemo, useRef, useState } from 'react';
import { D, MAX_Y, MIN_Y } from '../lib/data';

/**
 * 시계열 차트(직접 작성). 전체 기간을 유지한 채 선택 연도를 세로선으로 강조한다.
 * - 확인한 연도만 점으로 연결, 빠진 구간은 점선(값이 있다고 보이지 않게)
 * - bands: 강조 구간(급변 구간·비교 구간), markers: 전환점, trend: 장기 추세선
 * - 연도를 누르면 onPick(연도)
 */
export interface Series { key: string; label: string; color: string; points: [number, number][] }
export interface Band { from: number; to: number; tone?: 'hi' | 'lo' | 'cmp'; label?: string }
export interface Marker { year: number; kind: 'peak' | 'trough'; label?: string }

export function Chart({ series, unit, year, onPick, bands = [], markers = [], trend, height = 300, zero = true, x0 = MIN_Y, x1 = MAX_Y, eraBands = true, ariaLabel }: {
  series: Series[]; unit: string; year?: number; onPick?: (y: number) => void; bands?: Band[]; markers?: Marker[];
  trend?: [number, number][]; height?: number; zero?: boolean; x0?: number; x1?: number; eraBands?: boolean; ariaLabel: string;
}) {
  const box = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(800);
  const [hover, setHover] = useState<number | null>(null);
  useEffect(() => {
    if (!box.current) return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(280, e.contentRect.width)));
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);
  const narrow = w < 560;
  const all = series.flatMap((s) => s.points.map((p) => p[1]));
  const lo0 = Math.min(...all, zero ? 0 : Infinity), hi0 = Math.max(...all);
  const pad = (hi0 - lo0) * 0.08 || 1;
  const lo = zero && lo0 >= 0 ? 0 : lo0 - pad, hi = hi0 + pad;
  const m = { l: narrow ? 34 : 44, r: narrow ? 10 : 16, t: 16, b: 28 };
  const H = narrow ? Math.round(height * 0.8) : height;
  const X = (y: number) => m.l + ((y - x0) / (x1 - x0)) * (w - m.l - m.r);
  const Y = (v: number) => m.t + (1 - (v - lo) / (hi - lo)) * (H - m.t - m.b);
  const ticks = useMemo(() => {
    const span = hi - lo, step0 = span / 5, mag = 10 ** Math.floor(Math.log10(step0));
    const step = [1, 2, 2.5, 5, 10].map((k) => k * mag).find((s) => span / s <= 6) ?? mag * 10;
    const out = [];
    for (let v = Math.ceil(lo / step) * step; v <= hi; v += step) out.push(Math.round(v * 100) / 100);
    return out;
  }, [lo, hi]);
  const years = [...new Set(series.flatMap((s) => s.points.map((p) => p[0])))].sort((a, b) => a - b);

  const pick = (clientX: number) => {
    const r = box.current!.querySelector('svg')!.getBoundingClientRect();
    const x = ((clientX - r.left) / r.width) * w;
    let best = years[0], bd = Infinity;
    for (const y of years) { const d = Math.abs(X(y) - x); if (d < bd) { bd = d; best = y; } }
    return best;
  };

  const path = (pts: [number, number][]) => {
    let solid = '', gap = '';
    pts.forEach(([x, v], i) => {
      const P = `${X(x).toFixed(1)},${Y(v).toFixed(1)}`;
      if (!i) { solid += `M${P}`; return; }
      const [px, pv] = pts[i - 1];
      if (x - px > 1) { gap += `M${X(px).toFixed(1)},${Y(pv).toFixed(1)}L${P}`; solid += `M${P}`; } else solid += `L${P}`;
    });
    return { solid, gap };
  };
  const [table, setTable] = useState(false);
  const hv = hover !== null ? series.map((s) => ({ s, v: s.points.find((p) => p[0] === hover)?.[1] })) : [];

  return (
    <div className="chart" ref={box}>
      <svg width={w} height={H} role="img" aria-label={ariaLabel}
        onPointerMove={(e) => setHover(pick(e.clientX))} onPointerLeave={() => setHover(null)}
        onClick={(e) => onPick?.(pick(e.clientX))} style={onPick ? { cursor: 'pointer' } : undefined}>
        {eraBands && D.eras.map((e, i) => {
          const a = Math.max(X(e.startYear - 0.5), m.l), b = Math.min(X(Math.min(e.endYear ?? MAX_Y, x1) + 0.5), w - m.r);
          if (b <= a) return null;
          return <g key={e.id}><rect x={a} y={m.t} width={b - a} height={H - m.t - m.b} className={i % 2 ? 'era-b odd' : 'era-b'} />
            <text x={(a + b) / 2} y={H - 8} textAnchor="middle" className="axis-t">{narrow ? `'${String(e.startYear).slice(2)}` : `${e.startYear}s`}</text></g>;
        })}
        {bands.map((b, i) => (
          <g key={i}>
            <rect x={X(b.from - 0.5)} y={m.t} width={X(b.to + 0.5) - X(b.from - 0.5)} height={H - m.t - m.b} className={`band ${b.tone ?? 'cmp'}`} />
            {b.label && !narrow && <text x={X(b.from - 0.5) + 3} y={m.t + 11} className="band-t">{b.label}</text>}
          </g>
        ))}
        {ticks.map((v) => (
          <g key={v}>
            <line x1={m.l} x2={w - m.r} y1={Y(v)} y2={Y(v)} className={v === 0 ? 'zero' : 'grid'} />
            <text x={m.l - 6} y={Y(v) + 4} textAnchor="end" className="axis-t">{v}</text>
          </g>
        ))}
        {trend && <line x1={X(trend[0][0])} y1={Y(trend[0][1])} x2={X(trend[1][0])} y2={Y(trend[1][1])} className="trend" />}
        {year !== undefined && year >= x0 && year <= x1 && <line x1={X(year)} x2={X(year)} y1={m.t - 6} y2={H - m.b} className="sel-year" />}
        {series.map((s) => {
          const { solid, gap } = path(s.points);
          return (
            <g key={s.key}>
              <path d={solid} fill="none" stroke={s.color} strokeWidth={2.2} strokeLinejoin="round" />
              {gap && <path d={gap} fill="none" stroke={s.color} strokeWidth={1.5} strokeDasharray="3 5" opacity={0.7} />}
              {s.points.length < 20 && s.points.map(([x, v]) => <circle key={x} cx={X(x)} cy={Y(v)} r={3.5} fill={s.color} />)}
            </g>
          );
        })}
        {markers.map((mk, i) => {
          const s = series[0]; const v = s.points.find((p) => p[0] === mk.year)?.[1];
          if (v === undefined) return null;
          return (
            <g key={i} className={`mk ${mk.kind}`} onClick={(e) => { e.stopPropagation(); onPick?.(mk.year); }}>
              <circle cx={X(mk.year)} cy={Y(v)} r={9} className="mk-hit" />
              <path d={mk.kind === 'peak' ? `M${X(mk.year) - 5},${Y(v) - 8} L${X(mk.year) + 5},${Y(v) - 8} L${X(mk.year)},${Y(v) - 2} z` : `M${X(mk.year) - 5},${Y(v) + 8} L${X(mk.year) + 5},${Y(v) + 8} L${X(mk.year)},${Y(v) + 2} z`} />
              <title>{`${mk.year} ${mk.kind === 'peak' ? '고점' : '저점'}${mk.label ? ' · ' + mk.label : ''}`}</title>
            </g>
          );
        })}
        {hover !== null && (
          <g pointerEvents="none">
            <line x1={X(hover)} x2={X(hover)} y1={m.t} y2={H - m.b} className="cross" />
            {hv.map(({ s, v }) => v !== undefined && <circle key={s.key} cx={X(hover)} cy={Y(v)} r={4.5} fill={s.color} stroke="var(--bg)" strokeWidth={2} />)}
          </g>
        )}
      </svg>
      {hover !== null && (
        <div className="tip" style={{ left: Math.min(Math.max(X(hover) - 70, 0), w - 150) }}>
          <b>{hover}</b>
          {hv.map(({ s, v }) => <span key={s.key}><i style={{ background: s.color }} />{s.label} {v === undefined ? '자료 없음' : `${v.toLocaleString('ko-KR')}${unit}`}</span>)}
          {onPick && <em>누르면 {hover}년으로</em>}
        </div>
      )}
      <button className="link tiny" onClick={() => setTable(!table)} aria-expanded={table}>{table ? '표 닫기' : '표로 보기'}</button>
      {table && (
        <div className="tbl-wrap"><table className="tbl">
          <thead><tr><th>연도</th>{series.map((s) => <th key={s.key}>{s.label} ({unit})</th>)}</tr></thead>
          <tbody>{years.map((y) => <tr key={y} className={y === year ? 'on' : ''}><td>{y}</td>{series.map((s) => <td key={s.key}>{s.points.find((p) => p[0] === y)?.[1] ?? '—'}</td>)}</tr>)}</tbody>
        </table></div>
      )}
    </div>
  );
}

/** 지표의 출처 줄 */
export function SourceLine({ ids, extra }: { ids: string[]; extra?: string }) {
  const seen = new Set<string>();
  const src = [...new Set(ids)].map((id) => D.sources[id]).filter((x) => x && !seen.has(x.publisher) && seen.add(x.publisher));
  return (
    <p className="src-line">출처: {src.map((s, i) => <span key={s.id}>{i ? ' · ' : ''}<a href={s.url} target="_blank" rel="noreferrer">{s.publisher}</a></span>)}{extra ? ` — ${extra}` : ''}</p>
  );
}
