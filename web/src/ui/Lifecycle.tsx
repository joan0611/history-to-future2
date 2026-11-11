import { useEffect, useRef, useState } from 'react';
import { MAX_Y, MIN_Y, byId, type Chain } from '../lib/data';

/** 생애 막대 — 흐름마다 한 줄. 확인된 단계만 점으로 찍고, 단계 이름은 막대 아래 글로(겹침 없음). */
export function Lifecycle({ chains, year, why }: { chains: Chain[]; year: number; why: (id: string) => void }) {
  const box = useRef<HTMLDivElement>(null);
  const [w, setW] = useState(800);
  useEffect(() => {
    if (!box.current) return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(260, e.contentRect.width)));
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);
  const X = (y: number) => 8 + ((Math.max(y, MIN_Y) - MIN_Y) / (MAX_Y - MIN_Y)) * (w - 16);
  return (
    <div className="life-box" ref={box}>
      <svg width={w} height={18} aria-hidden className="life-axis">
        {[1960, 1970, 1980, 1990, 2000, 2010, 2020].map((y) => <text key={y} x={X(y)} y={12} textAnchor={y === 1960 ? 'start' : 'middle'}>{y}</text>)}
      </svg>
      {chains.map((c) => {
        const steps = c.steps.map((s) => ({ s, n: byId[s.nodeId] })).filter((x) => x.n);
        const xs = steps.map((x) => X(x.n.year));
        return (
          <div key={c.id} className="life-row">
            <div className="life-t">{c.title}</div>
            <svg width={w} height={24} role="img" aria-label={`${c.title}: ${steps.map((x) => x.s.stageLabel).join(' → ')}`}>
              <line x1={Math.min(...xs)} x2={Math.max(...xs)} y1={12} y2={12} className="life-line" />
              <line x1={X(year)} x2={X(year)} y1={0} y2={24} className="sel-year" />
              {steps.map(({ s, n }, i) => (
                <g key={i} className="life-dot" onClick={() => why(n.id)} role="button" tabIndex={0} onKeyDown={(e) => e.key === 'Enter' && why(n.id)}>
                  <circle cx={X(n.year)} cy={12} r={11} className="hit" />
                  <circle cx={X(n.year)} cy={12} r={6} className={`d s${Math.min(i, 4)}`} />
                  <title>{`${s.stageLabel} · ${n.yearPrecision === 'era' ? n.eraId : n.year} · ${n.label}`}</title>
                </g>
              ))}
            </svg>
            <ol className="life-steps">
              {steps.map(({ s, n }, i) => (
                <li key={i}><button className="link" onClick={() => why(n.id)}><b>{s.stageLabel}</b> {n.yearPrecision === 'era' ? `${n.year}년대` : n.year} {n.label}</button></li>
              ))}
            </ol>
          </div>
        );
      })}
    </div>
  );
}
