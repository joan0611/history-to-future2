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
export interface Edge { id: string; from: string; to: string; rel: Rel; verification: Verif; chainId: string; note: string; claimIds: string[]; kind7?: string; lag?: number | null }
export interface EvRef { id: string; label: string; year: number; shared: number }
export interface EvUse { kind: 'topic' | 'industry'; id: string; label: string; at: string; turn: string; shared: number }
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
export interface FlowStep { id: string; era: string; phase: Phase; period: string; title: string; claimIds: string[]; nodeIds: string[]; empty?: string; measure?: string; side?: { why: string; go: [string, string][] } }
export interface FlowLink { from: string; to: string; kind: LinkKind; note: string; claimIds: string[]; infer?: string; inferAlt?: string }
export interface Bridge { from: string; to: string; kind: LinkKind; note: string; claimIds: string[]; change?: string; infer?: string; inferAlt?: string }
export interface Flow {
  tracks?: string;
  turns?: TTurn[]; futures?: { split: TLine; items: TFuture[] }; conclusion?: { key: TLine; favored: TLine; undecided: TLine; next: TLine; change: TLine };
  id: string; question: string; cats: Cat[]; span: [number, number]; shape: string; lede: string[]; indicators: string[]; note?: string;
  steps: FlowStep[]; links: FlowLink[]; cross: { flow: string; note: string }[]; gaps: string[]; alternatives: string[];
  eraStates: Record<string, string>; bridges: Bridge[]; domain: string; topic: string;
  econ: { status: 'linked' | 'partial' | 'context'; note: string; analysis?: string };
}
export interface Synth { text: string; claimIds: string[]; kind: 'synthesis' }
export type MechKind = 'effect' | 'channel' | 'condition' | 'correlation' | 'sequence' | 'interpretation' | 'hypothesis';
export interface WatchItem { id: string; name: string; def: string; latest: string; unit: string; source: string; threshold?: string; supports: [string, string][]; weakens: [string, string][]; caution: string; claimIds: string[] }
export interface ExLine { layer: 'fact' | 'source' | 'inference' | 'hypothesis'; text: string; ids: string[] }
export interface Explainer {
  question: string; short: string; shortIds: string[];
  story: { h: string; intro?: string; lines: ExLine[] }[];
  figure: { title: string; nodes: { t: string; s: string; block?: boolean }[]; read: string; ids: string[] };
  numbers: { what: string; value: string; base: string; alt: string; means: string; ids: string[] }[]; numbersRead: string;
  terms: { t: string; d: string }[]; changes: ExLine[]; unsure: ExLine[];
  compare: { intro: string; cols: string[]; rows: { q: string; common: string; cells: string[]; means: string; ids: string[] }[]; read: string; readIds: string[] };
}
export interface WatchRead { verdict: TLine; rows: { group: string; watch: string[]; dir: string; read: TLine }[]; decide: TLine }
export interface Study {
  watchRead?: WatchRead;
  explainer?: Explainer;
  id: string; title: string; subtitle: string; question: string; short: string; asOf: string;
  status: { content: string; evidence: string; data: string; backtest: string; reviewed: string };
  statusRules: { axis: string; levels: string; rule: string }[];
  timeframe: { asOf: string; observed: string; past: string; history: string };
  scope: { target: string; period: string; variable: string; notIncluded: string };
  summary: { state: Synth; basis: Synth[]; uncertain: Synth[]; watchFirst: string[] };
  findings: Synth[]; whyNow: Synth;
  consSeries: { total: [number, number][]; perCapita: [number, number][]; sourceIds: string[]; periods: [number, number, number][] };
  explain: string[];
  periodTest: { rows: { period: string; reported: number; geo: number; arith: number; exCrisis: number; perCapita: number; gdp: number | null }[]; fixed: { period: string; arith: number; gdp: number | null }[] };
  periodTestNote: string[];
  mechanism: { kinds: Record<MechKind, string>; nodes: { id: string; col: number; label: string; sub: string; bg?: boolean }[]; edges: { from: string; to: string; kind: MechKind; eps: string[]; note: string; claimIds: string[] }[] };
  episodes: { id: string; label: string; years: string; current?: boolean }[];
  rows: { item: string; basis: string; gap?: string; cells: Record<string, [string, string[]]> }[];
  same: Synth[]; different: Synth[];
  scenarios: { id: string; name: string; conditions: string; path: string; affected: string; timing: string; breaks: string; basis: string[] }[];
  watch: WatchItem[];
  revise: string[]; alternatives: string[]; limits: string[]; flows: string[]; chartNotes: { year: number; label: string }[];
  audit: { claim: string; check: string; result: string; change: string }[];
}

export type Layer = 'claim' | 'fact' | 'source' | 'inference' | 'hypothesis';
/** 취향 흐름의 한 문장 — claim(근거 문장의 종류로 사실/출처 해석 결정) 또는 AI 추론·가설(연결 논리·다른 설명·범위·신호 포함) */
export interface TR { layer: Layer; text: string; basis: string[]; logic?: string; alt?: string; scope?: string; test?: string }
export type Seg = [number, number, string, string];
export interface TasteFlow { turns?: TTurn[];
  futures?: { split: TLine; items: TFuture[] }; conclusion?: { key: TLine; favored: TLine; undecided: TLine; next: TLine; change: TLine };
  id: string; field: string; title: string; subtitle: string; question: string; span: [number, number]; status: string; scene?: TR;
  lanes: { id: string; label: string; desc: string; segs: Seg[]; claims: string[] }[];
  stages: { lane: string; period: string; title: string; items: string[]; appeal: TR; who: string; where: string; signals: [string, string, string[]][] }[];
  moves: { from: string; to: string; year: number; rel: string; why: string; reason: TR }[];
  chains: { title: string; steps: [string, string, Layer, string[]][] }[];
  segments: { group: string; choice: string; layer: Layer; claims: string[] }[];
  coexist: { q: string; a: TR }[];
  contrast?: { title: string; a: string; b: string; rows: { dim: string; a: string; b: string; layer: Layer; basis: string[]; aiCells?: string[]; aiWhy?: string }[]; note: string };
  outfits?: { period: string; pants: string; top: string; shoes: string; layer: Layer; basis: string[]; aiCells?: string[]; aiWhy?: string }[];
  future: { satisfied: TR[]; discomforts: TR[]; unmet: TR[]; directions: { name: string; layer: Layer; condition: string; products: string; signals: string; counter: string; basis: string[] }[] };
  research: { searched: string; missing: string; check: string };
}
export interface TasteField { id: string; label: string; topics: string[]; state: 'deep' | 'scoped' | 'eras' | 'candidate'; flows: string[]; note: string; eraFlows?: string[] }
export interface Tastes {
  flows: TasteFlow[]; fields: TasteField[];
  needs: { id: string; label: string; cases: { flow: string; how: string; claims: string[] }[]; compare: TR }[];
  layers: Record<Layer, string>; signals: Record<string, string>; phases: Record<string, string>; rels: Record<string, string>;
}

export type SLayer = 'fact' | 'source' | 'inference' | 'hypothesis';
export interface SLine { layer: SLayer; text: string; ids: string[] }
export interface Story { lead: string; qs: Record<string, SLine[]>; links: { flow: string; step?: string; why: string }[] }
export interface StepNote { mood: SLine[]; ripple: { area: string; line: SLine; go?: [string, string] }[]; after?: SLine }
export interface Stories { qs: { key: string; label: string }[]; stories: Record<string, Story>; stepNotes: Record<string, StepNote>; layers: Record<SLayer, string> }

interface Seed {
  eras: Era[]; claims: Claim[]; sources: Source[]; transitions: Transition[]; documents: Doc[]; indicators: Indicator[];
  graph: { nodes: Node[]; edges: Edge[]; chains: Chain[]; relTypes: Record<Rel, string>; nodeTypes: Record<string, string> };
  cycles: { analyses: Analysis[]; findings: Finding[]; params: Record<string, unknown> };
  specFields?: SpecFields;
  eventUses?: Record<string, EvUse[]>;
  numberChecks: Record<string, NumberCheck[]>;
  patterns: { parallels: Parallel[] };
  flows: { flows: Flow[]; phaseKo: Record<Phase, string>; linkKo: Record<LinkKind, string>; domains: { id: string; label: string }[] };
  studies: Study[];
  tastes: Tastes;
  stories: Stories;
  industries: unknown;
  topics: Topics;
}
const seed = seedJson as unknown as Seed;

export interface NumberCheck { indicator: string; title: string; year: number; claimed: number; data: number | null; unit: string; memo: string; ok: boolean | null; verdict: string }

export interface SpecStage { name: string; ok: boolean; basis: string }
export interface SpecField { id: string; key: string; label: string; subs: string[]; members: { topics: string[]; industries: string[]; flows: string[]; tastes: string[]; indicators: string[]; events: number }; counts: Record<string, number>; stages: SpecStage[]; level: number; passed: number; gaps: string[] }
export interface SpecFields { stages: string[]; fields: SpecField[]; note: string }
export const D = {
  tastes: seed.tastes,
  stories: seed.stories,
  industries: seed.industries,
  topics: seed.topics,
  eras: seed.eras,
  claims: Object.fromEntries(seed.claims.map((c) => [c.id, c])) as Record<string, Claim>,
  checks: (seed.numberChecks ?? {}) as Record<string, NumberCheck[]>,
  sources: Object.fromEntries(seed.sources.map((s) => [s.id, s])) as Record<string, Source>,
  docs: Object.fromEntries(seed.documents.map((d) => [d.id, d])) as Record<string, Doc>,
  transitions: seed.transitions,
  indicators: seed.indicators,
  nodes: seed.graph.nodes,
  edges: seed.graph.edges,
  graphX: seed.graph as unknown as Record<string, unknown>,
  chains: seed.graph.chains,
  relKo: seed.graph.relTypes,
  typeKo: seed.graph.nodeTypes,
  analyses: seed.cycles.analyses,
  findings: seed.cycles.findings,
  cycleParams: seed.cycles.params,
  spec: seed.specFields,
  eventUses: seed.eventUses ?? {},
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

// 해가 바뀌면 시간축 끝도 함께 늘어난다(지시서 4: 연도 자동 갱신). 자료가 없는 해는 '자료 없음'으로 둔다.
export const MIN_Y = 1960, MAX_Y = Math.max(2026, new Date().getFullYear());
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

/* ── 주제 이야기(R-Q) ───────────────────────────────── */
export interface TLine { layer: 'fact' | 'source' | 'inference' | 'hypothesis'; text: string; ids: string[] }
export interface TWorld { what: TLine; route: TLine; response: TLine; result: TLine; mode: string }
export interface TTurn { id: string; years: string; start: number; end: number; title: string; why: TLine; before: TLine[]; condition: TLine[]; response: TLine[]; change: TLine[]; legacy: TLine[]; world?: TWorld; gap?: string; events?: EvRef[] }
export interface TLane { label: string; start: number; end: number | null; state: string; note: TLine }
export interface TReason { title: string; facts: TLine[]; logic: TLine; proposal: TLine; rivals: TLine[]; scope: TLine; check: TLine[] }
export interface TFuture { kind: string; name: string; change: TLine; basis: TLine[]; logic: TLine; conditions: TLine; demand: TLine; watch: string[]; against: string[]; horizon?: string }
export interface TRepeat { type: string; title: string; past: TLine; now: TLine; alike: TLine; changed: TLine; alternatives: TLine[]; counter: TLine[]; at: string[]; interval?: string }
export interface TLink { kind: 'topic' | 'flow' | 'industry'; target: string; at: string; why: string }
export interface Topic {
  id: string; domain: string; label: string; tracks: string; question: string; scene: TLine; span: [number, number]; scope?: TLine[];
  turns: TTurn[]; branches: { intro: string; lanes: TLane[]; read: TLine }; reasons: TReason[]; repeats?: TRepeat[]; links?: TLink[];
  futures: { split: TLine; items: TFuture[] }; conclusion: { key: TLine; favored: TLine; undecided: TLine; next: TLine; change: TLine };
  compare?: { intro: string; cols: string[]; rows: { label: string; cells: string[] }[]; ids: string[]; read: TLine };
  probes?: { q: string; a: TLine[] }[];
}
export interface TNeed { id: string; label: string; rel: string; intro: string; cases: { kind: string; id: string; label: string; when: string; who: string; before: TLine; trigger: TLine; after: TLine; motive: TLine }[]; whyNow: TLine; common: TLine; differ: TLine; counter: TLine }
export interface Topics { needs: TNeed[]; relKo: Record<string, string>; fieldMap: { id: string; label: string; items: { kind: string; id: string }[]; planned: string[] }[]; domains: { id: string; label: string; desc: string }[]; topics: Topic[]; planned: { domain: string; id: string; label: string }[]; check: { key: string; label: string; where: string[] }[] }
export const topicById: Record<string, Topic> = Object.fromEntries((seed.topics?.topics ?? []).map((t) => [t.id, t]));
export const MODE_KO: Record<string, string> = { same: '거의 그대로 들어옴', late: '늦게 확산', adapted: '국내 조건에 맞게 변형', rejected: '들어왔다가 밀려남', outbound: '한국에서 세계로' };

/* 사건(근거 문장) → 그 사건이 들어 있는 이야기(R-Q19). 이야기 안에서 쓴 근거 문장 id로 잇는다(추측 없음). */
function collectIds(x: unknown, out: Set<string>) {
  if (Array.isArray(x)) { for (const v of x) { if (typeof v === 'string') out.add(v); else collectIds(v, out); } return; }
  if (x && typeof x === 'object') for (const v of Object.values(x as Record<string, unknown>)) collectIds(v, out);
}
export interface StoryRef { kind: 'topic' | 'taste' | 'industry'; id: string; title: string; at?: string }
const STORY_INDEX: { ref: StoryRef; ids: Set<string>; turns?: { id: string; years: string; ids: Set<string> }[] }[] = [
  ...(seed.topics?.topics ?? []).map((t) => { const ids = new Set<string>(); collectIds(t, ids); return { ref: { kind: 'topic' as const, id: t.id, title: t.label }, ids, turns: t.turns.map((tu) => { const s2 = new Set<string>(); collectIds(tu, s2); return { id: tu.id, years: tu.years, ids: s2 }; }) }; }),
  ...seed.tastes.flows.map((f) => { const ids = new Set<string>(); collectIds(f, ids); return { ref: { kind: 'taste' as const, id: f.id, title: f.title }, ids }; }),
  ...((seed.industries as { industries: { id: string; label: string }[] })?.industries ?? []).map((i) => { const ids = new Set<string>(); collectIds(i, ids); return { ref: { kind: 'industry' as const, id: i.id, title: i.label }, ids }; }),
];
export function storiesFor(claimIds: string[]): StoryRef[] {
  const out: StoryRef[] = [];
  for (const s of STORY_INDEX) {
    if (!claimIds.some((c) => s.ids.has(c))) continue;
    const tu = s.turns?.find((t) => claimIds.some((c) => t.ids.has(c)));
    out.push({ ...s.ref, at: tu ? `${tu.years} 전환점` : undefined });
  }
  return out;
}
