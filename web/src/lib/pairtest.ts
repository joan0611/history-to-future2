/**
 * 두 지표 직접 검정(지시서 12-E·F, 9-4) — 사용자가 고른 두 연도별 지표와 기간으로 실제 계산한다.
 *  - 수준 상관, 전년 대비 변화끼리 상관(추세 제거)
 *  - 변화 상관의 95% 신뢰구간(피셔 z), 순열 검정 p값(같은 시드로 재현 가능)
 *  - 시차 −3~+3년 탐색
 *  - 공통 원인 통제: 세 번째 지표의 변화를 통제한 부분상관
 *  - 앞·뒤 절반 기간 재계산(관계가 시대에 따라 바뀌는지)
 * 결과 문장은 계산 값에서 규칙으로만 만든다. 인과를 판정하지 않는다.
 */
import { D, type Indicator } from './data';

type Pt = [number, number];
export const annualSeries = (i: Indicator): Pt[] => {
  if (i.frequency !== 'annual') return [];
  const s = i.series.find((x) => x.country === 'KR') ?? i.series[0];
  return (s?.points ?? []).map(([y, v]) => [Number(String(y).slice(0, 4)), v] as Pt).filter(([y, v]) => Number.isFinite(y) && Number.isFinite(v));
};
export const testable = (): Indicator[] => D.indicators.filter((i) => !i.multi && annualSeries(i).length >= 10);

export function corr(a: number[], b: number[]): number | null {
  const n = a.length; if (n < 4) return null;
  const ma = a.reduce((x, y) => x + y, 0) / n, mb = b.reduce((x, y) => x + y, 0) / n;
  let sab = 0, saa = 0, sbb = 0;
  for (let k = 0; k < n; k++) { sab += (a[k] - ma) * (b[k] - mb); saa += (a[k] - ma) ** 2; sbb += (b[k] - mb) ** 2; }
  return saa && sbb ? sab / Math.sqrt(saa * sbb) : null;
}
const diff = (p: Pt[]): Pt[] => p.slice(1).filter((_, k) => p[k + 1][0] - p[k][0] === 1).map(([y, v]) => { const prev = p.find(([yy]) => yy === y - 1)!; return [y, v - prev[1]] as Pt; });
function join(...ss: Pt[][]): { years: number[]; cols: number[][] } {
  const maps = ss.map((s) => new Map(s));
  const years = ss[0].map(([y]) => y).filter((y) => maps.every((m) => m.has(y)));
  return { years, cols: maps.map((m) => years.map((y) => m.get(y)!)) };
}
export function fisherCI(r: number, n: number): [number, number] | null {
  if (n < 5 || Math.abs(r) >= 1) return null;
  const z = Math.atanh(r), se = 1 / Math.sqrt(n - 3);
  return [Math.tanh(z - 1.96 * se), Math.tanh(z + 1.96 * se)];
}
/** 결정적 의사난수(mulberry32) — 같은 입력이면 같은 p값 */
function rng(seed: number) { return () => { seed |= 0; seed = (seed + 0x6d2b79f5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
export function permP(a: number[], b: number[], iters = 2000): number | null {
  const r0 = corr(a, b); if (r0 === null) return null;
  const R = rng(a.length * 7919 + Math.round(Math.abs(r0) * 1e6));
  const bb = [...b]; let hit = 0;
  for (let k = 0; k < iters; k++) {
    for (let j = bb.length - 1; j > 0; j--) { const m = Math.floor(R() * (j + 1)); [bb[j], bb[m]] = [bb[m], bb[j]]; }
    const r = corr(a, bb); if (r !== null && Math.abs(r) >= Math.abs(r0) - 1e-12) hit++;
  }
  return (hit + 1) / (iters + 1);
}
export function partial(rxy: number, rxz: number, ryz: number): number | null {
  const d = Math.sqrt((1 - rxz ** 2) * (1 - ryz ** 2));
  return d > 1e-9 ? (rxy - rxz * ryz) / d : null;
}

export interface PairResult {
  a: Indicator; b: Indicator; c?: Indicator; years: [number, number]; n: number; nd: number;
  rLevel: number | null; rDiff: number | null; ci: [number, number] | null; p: number | null;
  lags: { lag: number; r: number | null; n: number }[]; best: { lag: number; r: number | null };
  rPartial: number | null; ciPartial: [number, number] | null; rAC: number | null; rBC: number | null;
  first: number | null; second: number | null; split: number | null;
  verdict: { layer: 'observed' | 'unknown'; text: string }[];
}

export function pairTest(aId: string, bId: string, cId?: string, from?: number, to?: number): PairResult | { error: string } {
  const a = D.indicators.find((x) => x.id === aId), b = D.indicators.find((x) => x.id === bId), c = cId ? D.indicators.find((x) => x.id === cId) : undefined;
  if (!a || !b) return { error: '지표를 찾지 못했다.' };
  if (a.id === b.id) return { error: '서로 다른 두 지표를 골라야 한다.' };
  const cut = (p: Pt[]) => p.filter(([y]) => (from === undefined || y >= from) && (to === undefined || y <= to));
  const pa = cut(annualSeries(a)), pb = cut(annualSeries(b)), pc = c ? cut(annualSeries(c)) : [];
  const lv = join(pa, pb);
  if (lv.years.length < 8) return { error: `두 지표가 겹치는 해가 ${lv.years.length}개뿐이라 계산하지 않는다(최소 8개).` };
  const da = diff(pa), db = diff(pb), dc = c ? diff(pc) : [];
  const dv = join(da, db);
  const rLevel = corr(lv.cols[0], lv.cols[1]);
  const rDiff = dv.years.length >= 6 ? corr(dv.cols[0], dv.cols[1]) : null;
  const ci = rDiff !== null ? fisherCI(rDiff, dv.years.length) : null;
  const p = rDiff !== null ? permP(dv.cols[0], dv.cols[1]) : null;
  const lags: PairResult['lags'] = [];
  for (let L = -3; L <= 3; L++) {
    const shifted: Pt[] = db.map(([y, v]) => [y - L, v]);
    const j = join(da, shifted);
    lags.push({ lag: L, r: j.years.length >= 6 ? corr(j.cols[0], j.cols[1]) : null, n: j.years.length });
  }
  const best = lags.reduce((m, x) => (x.r !== null && (m.r === null || Math.abs(x.r) > Math.abs(m.r) + 0.05) ? { lag: x.lag, r: x.r } : m), { lag: 0, r: lags.find((x) => x.lag === 0)?.r ?? null });
  let rPartial: number | null = null, ciPartial: [number, number] | null = null, rAC: number | null = null, rBC: number | null = null;
  if (c && c.id !== a.id && c.id !== b.id) {
    const j3 = join(da, db, dc);
    if (j3.years.length >= 8) {
      const rab = corr(j3.cols[0], j3.cols[1]); rAC = corr(j3.cols[0], j3.cols[2]); rBC = corr(j3.cols[1], j3.cols[2]);
      if (rab !== null && rAC !== null && rBC !== null) { rPartial = partial(rab, rAC, rBC); ciPartial = rPartial !== null && j3.years.length >= 6 ? fisherCI(rPartial, j3.years.length - 1) : null; }
    }
  }
  const h = Math.floor(dv.years.length / 2);
  const first = h >= 5 ? corr(dv.cols[0].slice(0, h), dv.cols[1].slice(0, h)) : null;
  const second = dv.years.length - h >= 5 ? corr(dv.cols[0].slice(h), dv.cols[1].slice(h)) : null;
  const f = (x: number | null) => (x === null ? '계산 불가' : x.toFixed(2));
  const verdict: PairResult['verdict'] = [];
  const nd = dv.years.length;
  if (rLevel !== null && rDiff !== null && Math.abs(rLevel) >= 0.6 && Math.abs(rDiff) < 0.3)
    verdict.push({ layer: 'observed', text: `수준은 함께 움직이지만(${f(rLevel)}) 해마다 변화는 거의 따로 움직인다(${f(rDiff)}). 둘 다 긴 추세가 있어서 생긴 겉보기 상관일 가능성이 크다.` });
  if (p !== null) verdict.push(p < 0.05
    ? { layer: 'observed', text: `해마다 변화끼리 상관 ${f(rDiff)}는 순서를 무작위로 섞은 2,000번 중 ${(p * 100).toFixed(1)}%에서만 그만큼 크게 나왔다(p=${p.toFixed(3)}). 우연만으로 보기는 어렵다.` }
    : { layer: 'observed', text: `해마다 변화끼리 상관 ${f(rDiff)}는 무작위로 섞어도 ${(p * 100).toFixed(1)}%에서 그만큼 나온다(p=${p.toFixed(3)}). 함께 움직인다는 증거로 부족하다.` });
  if (ci && ci[0] < 0 && ci[1] > 0) verdict.push({ layer: 'observed', text: `95% 신뢰구간(${f(ci[0])}~${f(ci[1])})이 0을 포함한다 — 관계의 방향조차 확정할 수 없다.` });
  if (best.lag !== 0 && best.r !== null) verdict.push({ layer: 'observed', text: `${b.title}을(를) ${Math.abs(best.lag)}년 ${best.lag > 0 ? '늦춰' : '앞당겨'} 맞췄을 때 상관이 가장 컸다(${f(best.r)}). 시차는 인과의 방향을 암시할 뿐 증명하지 않는다.` });
  if (c && rPartial !== null && rDiff !== null) verdict.push(Math.abs(rPartial) < Math.abs(rDiff) - 0.15
    ? { layer: 'observed', text: `${c.title}의 변화를 통제하자 관계가 ${f(rDiff)} → ${f(rPartial)}로 약해졌다. 둘을 함께 움직인 공통 원인 후보다.` }
    : { layer: 'observed', text: `${c.title}의 변화를 통제해도 관계가 거의 그대로다(${f(rDiff)} → ${f(rPartial)}). 적어도 이 지표는 공통 원인으로 설명되지 않는다.` });
  if (first !== null && second !== null && (Math.sign(first) !== Math.sign(second) || Math.abs(first - second) > 0.5))
    verdict.push({ layer: 'observed', text: `앞 절반(${dv.years[0]}~${dv.years[h - 1]}년, ${f(first)})과 뒤 절반(${dv.years[h]}~${dv.years[nd - 1]}년, ${f(second)})에서 관계가 크게 다르다. 시대에 따라 관계가 바뀌었을 수 있다.` });
  verdict.push({ layer: 'unknown', text: `한계: 연도 자료 ${nd}개, 해마다 변화가 자기 자신과 이어지는 성질(자기상관)이 있으면 순열 검정의 p값은 실제보다 작게 나올 수 있다. 인과 판단에는 다른 나라·월별 자료로의 재현과 메커니즘 근거가 필요하다.` });
  return { a, b, c, years: [lv.years[0], lv.years[lv.years.length - 1]], n: lv.years.length, nd, rLevel, rDiff, ci, p, lags, best, rPartial, ciPartial, rAC, rBC, first, second, split: h ? dv.years[h] : null, verdict };
}
