import seedJson from '../../../data/seed.json';

/** 데이터 계약 — data/build 파이프라인이 만든 seed.json(출처·검증 상태 포함)을 그대로 읽는다. */
export type Cat = 'politics' | 'economy' | 'society' | 'industry' | 'culture' | 'flow';
export const CATS: Cat[] = ['politics', 'economy', 'industry', 'society', 'culture', 'flow'];
export const CAT_KO: Record<Cat, string> = {
  politics: '정치·외교', economy: '경제·에너지', industry: '산업·기술·직업', society: '사회·생활·소비', culture: '문화·음악', flow: '유행·트렌드',
};
export const CAT_SHORT: Record<Cat, string> = { politics: '정치', economy: '경제', industry: '산업', society: '생활', culture: '문화', flow: '트렌드' };

export interface Claim {
  id: string; text: string; claimType: 'fact' | 'statistical' | 'interpretation' | 'hypothesis'; status: 'verified' | 'sourced' | 'needs_source'; sourceIds: string[]; countries: string[];
  period?: string; scope?: string; support?: string; statusNote?: string; independentSources?: number;
}
export interface Source { id: string; title: string; publisher: string; url: string; sourceType: string; publishedDate?: string; accessedDate: string; note?: string; origin?: string }
export interface Era { id: string; label: string; startYear: number; endYear: number | null; title: string; glance: { keyCause?: string; legacy?: string; summaryClaimIds?: string[] } }
export interface Node {
  id: string; kind: string; nodeType: string; label: string; year: number; yearPrecision: 'year' | 'era'; eraId: string; lane: Cat;
  countries: string[]; importance: 1 | 2 | 3; degree: number; claimIds: string[]; eventIds: string[]; docIds?: string[]; flowIds?: string[];
}
export interface Edge { id: string; from: string; to: string; rel: Rel; verification: Verif; chainId: string; note: string; claimIds: string[] }
export type Rel = 'cause' | 'background' | 'trigger' | 'influence' | 'sequence' | 'similar';
export type Verif = 'evidenced' | 'interpretation' | 'statistical' | 'hypothesis';
export interface Chain { id: string; kind: string; title: string; steps: { nodeId: string; stage: string; stageLabel: string }[]; countryResponses?: { country: string; situation: string }[] }
export interface Indicator {
  id: string; title: string; unit: string; frequency: 'annual' | 'monthly'; description: string; note?: string; category?: Cat; log?: boolean; multi?: boolean;
  series: { country: string; label: string; sourceIds: string[]; points: [string, number][] }[]; zeroLine?: boolean; refLine?: { value: number; label: string };
}
export interface Doc { id: string; publication: string; title: string; publishedDate: string; url: string; verification: { accessLevel: string; whatWasViewed?: string } }
export interface Transition { fromEra: string; toEra: string; summary: string }
export interface Analysis {
  key: string; indicator: string; country: string; title: string; unit: string; verdict: 'A' | 'E' | 'none' | 'weak' | 'insufficient'; why: string; n: number; from: number; to: number;
  points?: [number, number][]; residual?: [number, number][]; trend?: [number, number][]; turningPoints?: { year: number; kind: 'peak' | 'trough'; value: number }[];
  highEpisodes?: [number, number][]; lowEpisodes?: [number, number][]; episodeBasis?: string; trendR2?: number; changePoint?: { year: number; before: number; after: number; explained: number } | null;
  periodicity?: { acf: number[]; band: number; bestLag: number; maxAbsAcf: number; pAcf: number; spectralPeriod: number; pSpectral: number };
  sensitivity?: { range: [number, number]; n: number; verdict: string; method?: string; pAcf?: number; pSpectral?: number; period?: number; trendR2?: number }[];
}
export interface Finding {
  id: string; type: 'A' | 'B' | 'C' | 'D' | 'E' | 'N' | 'R' | 'W'; series: string[]; category: Cat; title: string; summary: string;
  periods: [number, number][]; intervals?: number[]; evidence: Record<string, unknown>; confidence: { level: '높음' | '보통' | '낮음'; why: string };
  interest: number; current?: boolean; signal?: string;
}
export interface Parallel { id: string; title: string; a: { eraId: string; label: string; years: string }; b: { eraId: string; label: string; years: string }; rows: { aspect: string; a: { text: string; claimIds: string[] }; b: { text: string; claimIds: string[] }; verdict: string; note: string }[];
  more?: { label: string; years: string; cells: Record<string, [string, string[]]> }[] }

export type Phase = 'before' | 'condition' | 'turn' | 'spread' | 'life' | 'cross' | 'now';
export type LinkKind = 'causal' | 'condition' | 'correlation' | 'sequence' | 'interpretation' | 'hypothesis' | 'similar';
export interface FlowStep { id: string; era: string; phase: Phase; period: string; title: string; claimIds: string[]; nodeIds: string[]; empty?: string; measure?: string }
export interface FlowLink { from: string; to: string; kind: LinkKind; note: string; claimIds: string[] }
export interface Bridge { from: string; to: string; kind: LinkKind; note: string; claimIds: string[]; change?: string }
export interface Flow {
  id: string; question: string; cats: Cat[]; span: [number, number]; shape: string; lede: string[]; indicators: string[]; note?: string;
  steps: FlowStep[]; links: FlowLink[]; cross: { flow: string; note: string }[]; gaps: string[]; alternatives: string[];
  eraStates: Record<string, string>; bridges: Bridge[]; domain: string; topic: string;
  econ: { status: 'linked' | 'partial' | 'context'; note: string; analysis?: string };
}
export interface Synth { text: string; claimIds: string[]; kind: 'synthesis' }
export interface Study {
  id: string; question: string; short: string; asOf: string; status: string;
  scope: { target: string; period: string; variable: string; notIncluded: string };
  findings: Synth[]; whyNow: Synth;
  mechanism: { nodes: { id: string; label: string; sub: string }[]; edges: { from: string; to: string; kind: LinkKind; note: string; claimIds: string[] }[] };
  episodes: { id: string; label: string; years: string; current?: boolean }[];
  rows: { item: string; cells: Record<string, [string, string[]]> }[];
  same: Synth[]; different: Synth[];
  scenarios: { id: string; name: string; conditions: string; path: string; affected: string; timing: string; breaks: string; basis: string[] }[];
  watch: { name: string; source: string; supports: string; weakens: string; claimIds: string[] }[];
  revise: string[]; alternatives: string[]; limits: string[]; flows: string[]; indicators: string[]; chartNotes: { year: number; label: string }[];
}

interface Seed {
  eras: Era[]; claims: Claim[]; sources: Source[]; transitions: Transition[]; documents: Doc[]; indicators: Indicator[];
  graph: { nodes: Node[]; edges: Edge[]; chains: Chain[]; relTypes: Record<Rel, string>; nodeTypes: Record<string, string> };
  cycles: { analyses: Analysis[]; findings: Finding[]; params: Record<string, unknown> };
  numberChecks: Record<string, NumberCheck[]>;
  patterns: { parallels: Parallel[] };
  flows: { flows: Flow[]; phaseKo: Record<Phase, string>; linkKo: Record<LinkKind, string>; domains: { id: string; label: string }[] };
  studies: Study[];
}
const seed = seedJson as unknown as Seed;

export interface NumberCheck { indicator: string; title: string; year: number; claimed: number; data: number | null; unit: string; memo: string; ok: boolean | null; verdict: string }

export const D = {
  eras: seed.eras,
  claims: Object.fromEntries(seed.claims.map((c) => [c.id, c])) as Record<string, Claim>,
  checks: (seed.numberChecks ?? {}) as Record<string, NumberCheck[]>,
  sources: Object.fromEntries(seed.sources.map((s) => [s.id, s])) as Record<string, Source>,
  docs: Object.fromEntries(seed.documents.map((d) => [d.id, d])) as Record<string, Doc>,
  transitions: seed.transitions,
  indicators: seed.indicators,
  nodes: seed.graph.nodes,
  edges: seed.graph.edges,
  chains: seed.graph.chains,
  relKo: seed.graph.relTypes,
  typeKo: seed.graph.nodeTypes,
  analyses: seed.cycles.analyses,
  findings: seed.cycles.findings,
  cycleParams: seed.cycles.params,
  parallels: seed.patterns.parallels,
  flows: seed.flows.flows,
  phaseKo: seed.flows.phaseKo,
  linkKo: seed.flows.linkKo,
  domains: seed.flows.domains,
  studies: seed.studies,
};
export const studyById: Record<string, Study> = Object.fromEntries(seed.studies.map((s) => [s.id, s]));
export const ECON_KO = { linked: '경제 판단과 연결 확인', partial: '일부만 연결 확인', context: '문화·역사적 맥락(경제 전망 근거로 쓰지 않음)' } as const;
export const ERA_LABEL: Record<string, string> = { '1960s': '1960년대', '1970s': '1970년대', '1980s': '1980년대', '1990s': '1990년대', '2000s': '2000년대', '2010s': '2010년대', '2020s': '2020년대' };
export const flowById: Record<string, Flow> = Object.fromEntries(seed.flows.flows.map((f) => [f.id, f]));

export const byId: Record<string, Node> = Object.fromEntries(D.nodes.map((n) => [n.id, n]));
export const out: Record<string, Edge[]> = {};
export const inc: Record<string, Edge[]> = {};
for (const n of D.nodes) { out[n.id] = []; inc[n.id] = []; }
for (const e of D.edges) { out[e.from]?.push(e); inc[e.to]?.push(e); }

export const MIN_Y = 1960, MAX_Y = 2026;
export const YEARS = Array.from({ length: MAX_Y - MIN_Y + 1 }, (_, i) => MIN_Y + i);
export const eraOf = (y: number) => D.eras.find((e) => y >= e.startYear && y <= (e.endYear ?? MAX_Y)) ?? D.eras[0];
export const eraEnd = (e: Era) => Math.min(e.endYear ?? MAX_Y, MAX_Y);
/** 한국 사건인가 — 국가 표시가 없더라도 이름에 '(미국)' 등 해외 표시가 있으면 해외 사례로 본다 */
export const isKR = (n: Node) => n.countries.includes('KR') || (n.countries.length === 0 && !/\((미국|일본|중국|영국|세계|유럽)\)/.test(n.label));
export const COUNTRY_KO: Record<string, string> = { KR: '한국', US: '미국', JP: '일본', CN: '중국', MIDEAST: '중동', WORLD: '세계', GB: '영국', DE: '독일', FR: '프랑스' };
export const VERIF_KO: Record<Verif, string> = { evidenced: '근거 있는 인과', interpretation: '해석', statistical: '통계적 연관', hypothesis: '가설' };
export const CLAIM_KO = { fact: '사실', statistical: '통계', interpretation: '해석', hypothesis: '가설' } as const;
/** 문장(사실) 하나의 확인 수준 — 인과 연결의 확실성과는 따로 표시한다 */
export const STATUS_KO = { verified: '서로 다른 두 곳 이상에서 확인', sourced: '한 곳에서 확인', needs_source: '출처 미확보 — 사실 여부 미확인' } as const;
export const STATUS_SHORT = { verified: '두 곳 이상 확인', sourced: '한 곳 확인', needs_source: '출처 미확보' } as const;

/** 원인·결과 연결의 성격(관계망 연결을 변화 흐름과 같은 6가지 말로) */
export function linkKindOf(e: Edge): LinkKind {
  if (e.rel === 'sequence') return 'sequence';
  if (e.verification === 'hypothesis') return 'hypothesis';
  if (e.verification === 'statistical') return 'correlation';
  if (e.verification === 'interpretation') return 'interpretation';
  return e.rel === 'background' ? 'condition' : 'causal';
}

/** 한 항목의 근거 문장들이 어느 수준까지 확인됐는지 — 숫자 하나로 합치지 않고 그대로 센다 */
export function evidenceCount(ids: string[]) {
  const cs = ids.map((id) => D.claims[id]).filter(Boolean);
  return { total: cs.length, verified: cs.filter((c) => c.status === 'verified').length, sourced: cs.filter((c) => c.status === 'sourced').length, missing: cs.filter((c) => c.status === 'needs_source').length };
}

/** 근거 신뢰도: 독립 출처 2개 이상인 문장의 비율 */
export function reliability(n: Node) {
  const cs = n.claimIds.map((id) => D.claims[id]).filter(Boolean);
  return cs.length ? cs.reduce((a, c) => a + (c.status === 'verified' ? 1 : c.status === 'sourced' ? 0.6 : 0), 0) / cs.length : 0;
}

/** 근거 문장의 첫 문장(짧은 설명) */
export function lead(n: Node, max = 110) {
  const c = n.claimIds.map((id) => D.claims[id]).find(Boolean);
  if (!c) return '';
  const first = c.text.split(/(?<=다\.)\s/)[0];
  return first.length > max ? first.slice(0, max - 1) + '…' : first;
}

/** 핵심 변화 고르기 — 점수(중요도·연결·신뢰도) 순, 단 분야가 한쪽으로 몰리지 않게 분야별 1개씩 먼저 */
export function pickKey(nodes: Node[], k: number) {
  const cand = nodes.filter((n) => n.yearPrecision === 'year' && isKR(n) && n.claimIds.length);
  const score = (n: Node) => n.importance * 10 - Math.min(n.degree, 6) - reliability(n) * 2;
  const sorted = [...cand].sort((a, b) => score(a) - score(b));
  const pick: Node[] = [];
  const seen = new Set<string>();
  for (const n of sorted) { if (pick.length >= k) break; if (!seen.has(n.lane) && n.importance <= 2) { pick.push(n); seen.add(n.lane); } }
  for (const n of sorted) { if (pick.length >= k) break; if (!pick.includes(n)) pick.push(n); }
  return pick.sort((a, b) => a.year - b.year || score(a) - score(b));
}

export const nodesIn = (y0: number, y1: number, f?: (n: Node) => boolean) =>
  D.nodes.filter((n) => n.yearPrecision === 'year' && n.year >= y0 && n.year <= y1 && (!f || f(n)));

export const yearCount = (() => {
  const m: Record<number, number> = {};
  for (const n of D.nodes) if (n.yearPrecision === 'year' && isKR(n)) m[n.year] = (m[n.year] ?? 0) + 1;
  return m;
})();
