/**
 * 질문 분석 엔진(추론 1단계) — 언어모델 없이 앱 안의 실제 데이터로 질문에 답한다.
 *
 * 하는 일(지시서 9-1·9-4): 질문 해석 → 근거 검색(문장·사건·주제·산업·지표) → 실제 계산(지표 요약, 두 지표의
 * 상관·차분 상관·시차·앞뒤 절반 안정성) → 근거·반대 증거·한계·미검증 가설·추가 자료·다음 질문을 층위별로 조립.
 * 하지 않는 일: 새 사실을 만들지 않는다. 문장은 모두 seed의 근거 문장·계산 결과·규칙 기반 조립 문장 중 하나이며
 * 어느 것인지 layer로 표시한다. 근거가 모자라면 답 대신 '부족'과 필요한 자료를 돌려준다.
 */
import { D, byId, inc, out, topicById, type Claim, type Indicator, type Node, type Topic, type TLine } from './data';

export type ALayer = 'fact' | 'observed' | 'interpretation' | 'inference' | 'hypothesis' | 'scenario' | 'unknown';
export const ALAYER_KO: Record<ALayer, string> = {
  fact: '사실', observed: '관찰된 관계(계산)', interpretation: '학술·출처 해석', inference: 'AI 추론(규칙 조립)',
  hypothesis: '미검증 가설', scenario: '조건부 시나리오', unknown: '확인 안 됨',
};
export interface ALine { layer: ALayer; text: string; ids: string[]; go?: string }
export interface AHit { kind: 'claim' | 'topic' | 'industry' | 'event' | 'indicator'; id: string; label: string; score: number; go?: string }
export interface Calc { title: string; method: string; rows: [string, string][]; n: number }
export interface Answer {
  q: string; tokens: string[]; missing: string[]; intents: string[]; years: [number, number] | null;
  enough: boolean; trace: string[]; hits: AHit[]; calcs: Calc[];
  sections: { key: string; title: string; lines: ALine[] }[];
}

const INTENT_WORDS = ['공통점', '차이', '차이점', '비교', '원인', '이유', '배경', '상관', '상관관계', '인과', '인과관계', '관계', '연관', '영향', '반복', '되풀이', '주기', '사이클', '재유행', '재등장', '앞으로', '미래', '전망', '가능', '시나리오', '예상', '함께', '움직', '움직였', '성장', '과정', '만약', '달랐다면', '발전', '등장', '시작', '이후', '지금', '현재', '시대', '어땠', '바뀌', '바뀌었', '달라졌', '달라지'];
const GENERIC = new Set(['산업', '경제', '시장', '소비', '구조', '가격', '수출', '생활', '사회', '문화']);
const STOP = new Set([...INTENT_WORDS, '그리고', '그런데', '어떤', '어떻게', '무엇', '무슨', '있을까', '있는지', '있었을까', '했을까', '일까', '할까', '될까', '되었을까', '나타났을까', '정말', '혹시', '대해', '대한', '관련', '때문', '다른', '같은', '사이', '경우', '과정', '정도', '가능성', '확인', '설명', '현상', '변화', '한국', '우리', '나는', '내가', '이런', '그런', '것은', '것이', '수', '더', '중', '및']);
const SUFFIX = ['으로부터', '에서는', '에서도', '으로는', '이라는', '이었을까', '였을까', '했을까', '할까요', '일까요', '까지', '부터', '에서', '에게', '으로', '하고', '이랑', '과의', '와의', '처럼', '보다', '마다', '라는', '이라', '했던', '하는', '하면', '했다', '된다', '되는', '되면', '에는', '에도', '은', '는', '이', '가', '을', '를', '의', '에', '과', '와', '로', '도', '만', '들', '적'];

/** 일상어 → 앱 자료에 쓰인 말(지시서 9-5: 미리 쓰지 않은 질문도 자료에 닿게). 원래 말이 자료에 없을 때만 바꾼다. */
export const SYN: Record<string, string[]> = {
  집값: ['주택가격'], 아파트값: ['주택가격'], 월급: ['임금'], 연봉: ['임금'], 봉급: ['임금'], 급여: ['임금'],
  저출산: ['출산율'], 출생: ['출산'], 아이: ['출산'], 일자리: ['고용'], 취업: ['고용'], 실직: ['실업'],
  노인: ['65세', '고령'], 고령화: ['65세', '고령'], 휴대폰: ['휴대전화'], 핸드폰: ['휴대전화'], 핸드폰은: ['휴대전화'],
  자동차: ['자동차', '승용차'], 기름값: ['석유'], 유가: ['석유'], 인플레이션: ['물가'], 인플레: ['물가'],
  성장률: ['경제성장률'], 경기: ['경제성장률'], 인터넷쇼핑: ['온라인쇼핑'], 쇼핑몰: ['온라인쇼핑'], 혼자: ['1인'],
  혼밥: ['1인'], 엥겔: ['식료품'], 먹거리: ['식료품'], 공장: ['제조업'], 농사: ['농림어업'], 농업: ['농림어업'],
  한류: ['음악', '수출'], 케이팝: ['음악'], 금리인상: ['금리'], 기준금리: ['기준금리'], 달러: ['환율'],
};
export function tokenize(q: string): string[] {
  const raw = q.replace(/[^\p{L}\p{N}]+/gu, ' ').split(' ').filter(Boolean);
  const outT: string[] = [];
  for (let w of raw) {
    if (/^\d{4}(년대|년)?$/.test(w)) continue;
    for (const s of SUFFIX) if (w.length > s.length + 1 && w.endsWith(s)) { w = w.slice(0, -s.length); break; }
    if (/(까|니|요|다|될|할|질|볼|릴|뀔|을|던|는가|ㄹ까)$/.test(w) && w.length <= 6) continue;
    if (w === '앞으' || w.startsWith('무엇') || w.length < 2 || STOP.has(w)) continue;
    if (!outT.includes(w)) outT.push(w);
  }
  return outT;
}

export function yearsOf(q: string): [number, number] | null {
  const dec = [...q.matchAll(/(19[6-9]0|20[0-2]0)년대/g)].map((m) => Number(m[1]));
  const ys = [...q.replace(/(19[6-9]0|20[0-2]0)년대/g, '').matchAll(/(19[5-9]\d|20[0-3]\d)/g)].map((m) => Number(m[1]));
  const all = [...dec.flatMap((d) => [d, d + 9]), ...ys];
  if (!all.length) return null;
  return [Math.min(...all), Math.max(...all)];
}

const INTENTS: [string, RegExp][] = [
  ['비교', /공통점|차이|비교|닮|다른 점|같은 점|\bvs\b/],
  ['원인', /왜|원인|이유|때문|배경/],
  ['관계', /상관|인과|관계|연관|영향|함께 움직/],
  ['반복', /반복|다시|재유행|되풀이|주기|사이클|재등장/],
  ['미래', /앞으로|미래|전망|가능|될까|시나리오|예상/],
  ['반사실', /만약|않았다면|없었다면|달랐다면/],
];

/* ── 검색 대상(문서) ─────────────────────────────────────────── */
interface Doc { kind: AHit['kind']; id: string; label: string; text: string; years?: [number, number]; go?: string }
const lineTexts = (ls: (TLine | undefined)[]) => ls.filter(Boolean).map((l) => (l as TLine).text).join(' ');
function topicText(t: Topic): string {
  const turns = t.turns.map((u) => [u.title, u.why.text, lineTexts([...u.before, ...u.condition, ...u.response, ...u.change, ...u.legacy])].join(' ')).join(' ');
  return [t.label, t.question, t.tracks, turns].join(' ');
}
let DOCS: Doc[] | null = null;
function docs(): Doc[] {
  if (DOCS) return DOCS;
  const ds: Doc[] = [];
  for (const c of Object.values(D.claims)) {
    const m = (c.period ?? '').match(/(\d{4})(?:\D+(\d{4}))?/);
    ds.push({ kind: 'claim', id: c.id, label: c.text, text: c.text, years: m ? [Number(m[1]), Number(m[2] ?? m[1])] : undefined });
  }
  for (const t of D.topics?.topics ?? []) ds.push({ kind: 'topic', id: t.id, label: t.label, text: topicText(t), years: t.span as [number, number], go: `#/topic/${t.id}` });
  for (const i of (D.industries as unknown as { industries: { id: string; label: string; tracks: string; question: string; span: [number, number]; stages: { what: string; period: string }[] }[] }).industries ?? [])
    ds.push({ kind: 'industry', id: i.id, label: i.label, text: [i.label, i.tracks, i.question, ...i.stages.map((s) => s.what)].join(' '), years: i.span, go: `#/field/industry` });
  for (const n of D.nodes) ds.push({ kind: 'event', id: n.id, label: n.label, text: n.label, years: [n.year, n.year] });
  for (const i of D.indicators) if (!i.multi) ds.push({ kind: 'indicator', id: i.id, label: i.title, text: `${i.title} ${i.description}`, go: `#/field/${i.category ?? 'economy'}?ind=${i.id}` });
  DOCS = ds;
  return ds;
}

function score(tokens: string[], yrs: [number, number] | null) {
  const ds = docs();
  const df: Record<string, number> = {};
  for (const t of tokens) df[t] = ds.reduce((a, d) => a + (d.text.includes(t) ? 1 : 0), 0);
  const rarest = [...tokens].filter((t) => df[t]).sort((a, b) => df[a] - df[b])[0];
  const res: { d: Doc; s: number; m: string[] }[] = [];
  for (const d of ds) {
    let s = 0; const m: string[] = [];
    for (const t of tokens) if (df[t] && d.text.includes(t)) { s += Math.log(1 + ds.length / df[t]); m.push(t); }
    if (!s) continue;
    if ((d.kind === 'claim' || d.kind === 'event') && tokens.length >= 2 && m.length < 2 && !(d.kind === 'event' && m.some((t) => d.label.includes(t))) && !(m.length === 1 && m[0] === rarest && df[m[0]] <= ds.length * 0.02)) continue;
    if (m.length > 1) s *= 1 + 0.35 * (m.length - 1);
    if (d.kind === 'indicator' && m.some((t) => d.label.includes(t))) s *= 1.6;
    if (d.kind === 'topic' && m.some((t) => d.label.includes(t))) s *= 1.4;
    if (yrs && d.years) s *= d.years[1] >= yrs[0] && d.years[0] <= yrs[1] ? 1.3 : 0.6;
    res.push({ d, s, m });
  }
  res.sort((a, b) => b.s - a.s);
  return { res, df };
}

const annualOk = (id: string) => { const i = D.indicators.find((x) => x.id === id); return !!i && krSeries(i).length >= 5; };
/* ── 계산 도구 ─────────────────────────────────────────────────── */
type Pt = [number, number];
const krSeries = (i: Indicator): Pt[] => {
  if (i.frequency !== 'annual') return [];
  const s = i.series.find((x) => x.country === 'KR') ?? i.series[0];
  return (s?.points ?? []).map(([y, v]) => [Number(String(y).slice(0, 4)), v] as Pt).filter(([y, v]) => Number.isFinite(y) && Number.isFinite(v));
};
const within = (p: Pt[], yrs: [number, number] | null) => (yrs ? p.filter(([y]) => y >= yrs[0] - 5 && y <= yrs[1] + 5) : p);
export function pearson(a: number[], b: number[]): number | null {
  const n = a.length; if (n < 4) return null;
  const ma = a.reduce((x, y) => x + y, 0) / n, mb = b.reduce((x, y) => x + y, 0) / n;
  let sab = 0, saa = 0, sbb = 0;
  for (let i = 0; i < n; i++) { sab += (a[i] - ma) * (b[i] - mb); saa += (a[i] - ma) ** 2; sbb += (b[i] - mb) ** 2; }
  return saa && sbb ? sab / Math.sqrt(saa * sbb) : null;
}
const diff = (p: Pt[]): Pt[] => p.slice(1).map(([y, v], k) => [y, v - p[k][1]]);
function align(a: Pt[], b: Pt[], lag = 0): [number[], number[], number[]] {
  const mb = new Map(b.map(([y, v]) => [y, v]));
  const xs: number[] = [], ys: number[] = [], yrs: number[] = [];
  for (const [y, v] of a) { const w = mb.get(y + lag); if (w !== undefined) { xs.push(v); ys.push(w); yrs.push(y); } }
  return [xs, ys, yrs];
}
const f2 = (x: number | null) => (x === null ? '계산 불가' : x.toFixed(2));
const fv = (x: number) => (Math.abs(x) >= 100 ? x.toLocaleString('ko-KR', { maximumFractionDigits: 0 }) : x.toFixed(2).replace(/\.?0+$/, ''));

function describe(i: Indicator, yrs: [number, number] | null): Calc | null {
  const p = within(krSeries(i), yrs);
  if (p.length < 3) return null;
  const [y0, v0] = p[0], [y1, v1] = p[p.length - 1];
  const mx = p.reduce((a, b) => (b[1] > a[1] ? b : a)), mn = p.reduce((a, b) => (b[1] < a[1] ? b : a));
  const ch = diff(p).map(([, v]) => v), meanCh = ch.reduce((a, b) => a + b, 0) / ch.length;
  const half = Math.floor(p.length / 2), m1 = p.slice(0, half).reduce((a, b) => a + b[1], 0) / half, m2 = p.slice(half).reduce((a, b) => a + b[1], 0) / (p.length - half);
  return {
    title: `${i.title} (${i.unit})`, method: '한국 계열의 처음·끝·최댓값·최솟값, 해마다 변화의 평균, 앞뒤 절반 평균', n: p.length,
    rows: [['기간', `${y0}~${y1}년 (${p.length}개 해)`], ['처음 → 끝', `${fv(v0)} → ${fv(v1)}`], ['최댓값', `${fv(mx[1])} (${mx[0]}년)`], ['최솟값', `${fv(mn[1])} (${mn[0]}년)`],
      ['해마다 변화 평균', fv(meanCh)], ['앞 절반 평균 → 뒤 절반 평균', `${fv(m1)} → ${fv(m2)}`]],
  };
}

interface Rel { a: Indicator; b: Indicator; n: number; rLevel: number | null; rDiff: number | null; bestLag: number; rLag: number | null; rFirst: number | null; rSecond: number | null; years: [number, number] }
function relate(a: Indicator, b: Indicator, yrs: [number, number] | null): Rel | null {
  const pa = within(krSeries(a), yrs), pb = within(krSeries(b), yrs);
  const [x, y, ys] = align(pa, pb);
  if (x.length < 8) return null;
  const da = diff(pa), db = diff(pb);
  const [dx, dy, dys] = align(da, db);
  let bestLag = 0, rLag: number | null = pearson(dx, dy);
  for (let L = -3; L <= 3; L++) { if (!L) continue; const [u, v] = align(da, db, L); const r = u.length >= 8 ? pearson(u, v) : null; if (r !== null && (rLag === null || Math.abs(r) > Math.abs(rLag) + 0.05)) { rLag = r; bestLag = L; } }
  const h = Math.floor(dx.length / 2);
  return { a, b, n: x.length, rLevel: pearson(x, y), rDiff: pearson(dx, dy), bestLag, rLag, rFirst: h >= 4 ? pearson(dx.slice(0, h), dy.slice(0, h)) : null, rSecond: dx.length - h >= 4 ? pearson(dx.slice(h), dy.slice(h)) : null, years: [ys[0], ys[ys.length - 1]] };
  void dys;
}

/* ── 조립 ─────────────────────────────────────────────────────── */
const claimLayer = (c: Claim): ALayer => (c.claimType === 'interpretation' ? 'interpretation' : c.claimType === 'hypothesis' ? 'hypothesis' : 'fact');
const tl = (l: TLine, go?: string): ALine => ({ layer: l.layer === 'fact' ? 'fact' : l.layer === 'source' ? 'interpretation' : l.layer === 'hypothesis' ? 'hypothesis' : 'inference', text: l.text, ids: l.ids, go });

export function ask(q: string): Answer {
  const yrs = yearsOf(q);
  const tokens: string[] = [];
  for (const t of tokenize(q)) {
    if (t.length >= 4 && !docs().some((d) => d.text.includes(t))) {
      let split: string[] | null = null;
      for (let k = 2; k <= t.length - 2 && !split; k++) { const a = t.slice(0, k), b = t.slice(k); if (docs().some((d) => d.text.includes(a)) && docs().some((d) => d.text.includes(b))) split = [a, b]; }
      if (split) { tokens.push(...split.filter((x) => !tokens.includes(x) && !STOP.has(x))); continue; }
    }
    if (!tokens.includes(t)) tokens.push(t);
  }
  const intents = INTENTS.filter(([, re]) => re.test(q)).map(([k]) => k);
  const trace: string[] = [];
  const swapped: string[] = [];
  for (const t of [...tokens]) {
    const rep = SYN[t]; if (!rep) continue;
    const inDocs = docs().some((d) => d.text.includes(t));
    for (const x of rep) if (!tokens.includes(x)) tokens.push(x);
    if (!inDocs) tokens.splice(tokens.indexOf(t), 1);
    swapped.push(`${t}→${rep.join('·')}`);
  }
  if (swapped.length) trace.push(`말 바꾸기: ${swapped.join(', ')} (앱 자료에 쓰인 말로)`);
  trace.push(`질문 해석: 핵심어 ${tokens.length}개(${tokens.join(', ') || '없음'}), 기간 ${yrs ? `${yrs[0]}~${yrs[1]}년` : '지정 없음'}, 질문 유형 ${intents.join('·') || '설명'}`);
  const { res, df } = score(tokens, yrs);
  const missing = tokens.filter((t) => !df[t]);
  trace.push(`근거 검색: 문서 ${docs().length}개(근거 문장·주제·산업·사건·지표) 중 ${res.length}개가 핵심어와 겹침${missing.length ? ` · 앱 안에 없는 말: ${missing.join(', ')}` : ''}`);
  const top = (k: Doc['kind'], n: number, min = 0) => res.filter((r) => r.d.kind === k && r.s >= min).slice(0, n);
  const best = res[0]?.s ?? 0;
  // 지표·산업·주제는 이름에 핵심어가 들어간 것을 핵심어마다 하나씩 먼저 고른다(여러 대상을 묻는 질문을 위해).
  const byLabel = (k: Doc['kind'], n: number) => {
    const picked: typeof res = [];
    const rare = [...tokens].filter((t) => df[t] && df[t] <= docs().length * 0.08 && !(k === 'indicator' && GENERIC.has(t))).sort((a, b) => df[a] - df[b]);
    for (const t of rare) { const r = res.find((x) => x.d.kind === k && x.d.label.includes(t) && !picked.includes(x) && (k !== 'indicator' || annualOk(x.d.id))); if (r) picked.push(r); }
    return picked.slice(0, n);
  };
  const inds = byLabel('indicator', 3);
  const industries = byLabel('industry', 3);
  const topics = [...byLabel('topic', 2), ...top('topic', 3, best * 0.5)].filter((x, k, a) => a.indexOf(x) === k).slice(0, 3);
  const claims = top('claim', 12, best * 0.25), events = top('event', 4, best * 0.3);
  const hits: AHit[] = [...topics, ...industries, ...inds, ...events, ...claims.slice(0, 6)].map((r) => ({ kind: r.d.kind, id: r.d.id, label: r.d.label, score: Math.round(r.s * 10) / 10, go: r.d.go }));
  const covered = tokens.length ? tokens.filter((t) => !missing.includes(t)).length / tokens.length : 0;
  const enough = tokens.length > 0 && claims.length + topics.length + inds.length >= 2 && (missing.length === 0 || covered >= 0.75);

  const calcs: Calc[] = [];
  const facts: ALine[] = [], data: ALine[] = [], expl: ALine[] = [], support: ALine[] = [], against: ALine[] = [], limits: ALine[] = [], concl: ALine[] = [], need: ALine[] = [], next: ALine[] = [];

  for (const r of claims) { const c = D.claims[r.d.id]; if (c) (c.claimType === 'interpretation' ? expl : facts).push({ layer: claimLayer(c), text: c.text, ids: [c.id] }); }
  // 지표 계산
  const indObjs = inds.map((r) => D.indicators.find((i) => i.id === r.d.id)!).filter(Boolean);
  for (const i of indObjs) {
    const c = describe(i, yrs);
    if (c) { calcs.push(c); data.push({ layer: 'observed', text: `${i.title}: ${c.rows[1][1]} (${c.rows[0][1]}), 최댓값 ${c.rows[2][1]}, 최솟값 ${c.rows[3][1]}.`, ids: i.series.flatMap((s) => s.sourceIds), go: `#/field/${i.category ?? 'economy'}?ind=${i.id}` }); }
  }
  if (calcs.length) trace.push(`계산: 지표 ${calcs.length}개 요약(실제 시계열)`);
  // 두 지표 관계
  const rels: Rel[] = [];
  for (let a = 0; a < indObjs.length; a++) for (let b = a + 1; b < indObjs.length; b++) { const r = relate(indObjs[a], indObjs[b], yrs); if (r) rels.push(r); }
  for (const r of rels) {
    calcs.push({ title: `${r.a.title} ↔ ${r.b.title}`, method: '같은 해끼리 짝지은 피어슨 상관(수준), 전년 대비 변화끼리의 상관(추세 제거), 변화의 시차 −3~+3년 중 가장 강한 것, 앞·뒤 절반 기간 재계산', n: r.n,
      rows: [['겹치는 해', `${r.years[0]}~${r.years[1]}년 (${r.n}개)`], ['수준 상관', f2(r.rLevel)], ['변화끼리 상관', f2(r.rDiff)], ['가장 강한 시차', r.bestLag ? `${r.b.title}이(가) ${Math.abs(r.bestLag)}년 ${r.bestLag > 0 ? '뒤' : '앞'} (상관 ${f2(r.rLag)})` : `같은 해 (상관 ${f2(r.rLag)})`], ['앞 절반 / 뒤 절반 변화 상관', `${f2(r.rFirst)} / ${f2(r.rSecond)}`]] });
    data.push({ layer: 'observed', text: `${r.a.title}와 ${r.b.title}: 수준 상관 ${f2(r.rLevel)}, 해마다 변화끼리 상관 ${f2(r.rDiff)} (${r.n}개 해).`, ids: [] });
    const trendOnly = r.rLevel !== null && r.rDiff !== null && Math.abs(r.rLevel) >= 0.6 && Math.abs(r.rDiff) < 0.3;
    if (trendOnly) against.push({ layer: 'observed', text: `수준은 함께 움직이지만(${f2(r.rLevel)}) 해마다 변화는 거의 따로 움직인다(${f2(r.rDiff)}). 두 지표가 모두 긴 추세를 가졌기 때문에 생긴 겉보기 상관일 가능성이 크다.`, ids: [] });
    const strong = r.rLag !== null && Math.abs(r.rLag) >= 0.4 && r.n >= 15;
    const unstable = r.rFirst !== null && r.rSecond !== null && (Math.sign(r.rFirst) !== Math.sign(r.rSecond) || Math.abs(r.rFirst - r.rSecond) > 0.5);
    if (strong) {
      const dir = r.rLag! > 0 ? '같은 방향' : '반대 방향';
      expl.push({ layer: 'hypothesis', text: `미검증 가설: ${r.a.title}의 변화와 ${r.b.title}의 변화는 ${dir}으로 움직이며${r.bestLag ? ` ${r.b.title} 쪽이 ${Math.abs(r.bestLag)}년 ${r.bestLag > 0 ? '늦게' : '먼저'} 반응한다` : ''}. 공통 원인(경기·정책)이 둘을 함께 움직였을 수도 있어 인과로 단정하지 않는다.`, ids: [] });
      support.push({ layer: 'observed', text: `변화끼리 상관 ${f2(r.rLag)} (${r.n}개 해) — 우연으로 보기 어려운 크기지만 표본이 작다.`, ids: [] });
      need.push({ layer: 'unknown', text: `반증 조건: 다른 나라 같은 지표나 월·분기 자료에서 시차·방향이 재현되지 않으면 가설은 약해진다. 공통 원인(성장률·금리)을 통제한 회귀가 필요하다.`, ids: [] });
    } else if (!trendOnly) {
      against.push({ layer: 'observed', text: `해마다 변화끼리의 관계가 약하다(가장 강한 값 ${f2(r.rLag)}). 이 두 지표만으로는 함께 움직인다고 말하기 어렵다.`, ids: [] });
    }
    if (unstable) against.push({ layer: 'observed', text: `앞 절반(${f2(r.rFirst)})과 뒤 절반(${f2(r.rSecond)})에서 관계가 크게 달라 시대에 따라 관계가 바뀌었을 수 있다.`, ids: [] });
  }
  if (rels.length) trace.push(`계산: 지표 쌍 ${rels.length}개의 상관·시차·안정성 검사`);
  if (intents.includes('관계') && indObjs.length < 2) limits.push({ layer: 'unknown', text: '관계를 계산하려면 두 현상 모두 연도별 지표가 앱에 있어야 하는데, 이 질문에서는 그런 지표를 둘 이상 찾지 못했다.', ids: [] });

  // 주제·산업에서 원인·반대 설명·미래·반복
  for (const r of topics) {
    const t = topicById[r.d.id]; if (!t) continue;
    const go = `#/topic/${t.id}`;
    if (intents.includes('원인') || intents.includes('관계') || !intents.length || intents.includes('비교')) for (const rs of t.reasons.slice(0, 1)) {
      expl.push({ ...tl(rs.proposal, go), text: `[${t.label.split(' — ')[0]}] ${rs.proposal.text}` });
      support.push(...rs.facts.slice(0, 2).map((l) => tl(l, go)));
      against.push(...rs.rivals.map((l) => ({ ...tl(l, go), text: `다른 설명 — ${l.text}` })));
      need.push(...rs.check.map((l) => ({ ...tl(l, go), layer: 'unknown' as ALayer })));
    }
    if (intents.includes('반복')) for (const rp of t.repeats ?? []) { support.push(tl(rp.alike, go)); against.push(...rp.counter.map((l) => tl(l, go))); }
    if (intents.includes('미래') || intents.includes('반사실')) {
      expl.push({ ...tl(t.futures.split, go), layer: 'scenario' });
      for (const f of t.futures.items) expl.push({ layer: 'scenario', text: `${f.kind} — ${f.name}: ${f.change.text} 볼 지표: ${f.watch.join(', ')}. 약해지는 조건: ${f.against.join(', ')}.${f.risk ? ` 위험: ${f.risk.text}` : ''}`, ids: f.change.ids, go });
    }
    if (t.conclusion.undecided) limits.push({ ...tl(t.conclusion.undecided, go), layer: 'unknown' });
    for (const l of (t.links ?? []).slice(0, 2)) next.push({ layer: 'inference', text: `${l.why}`, ids: [], go: l.kind === 'topic' ? `#/topic/${l.target}` : undefined });
  }
  // 사건 그래프 — 들어오는 연결(원인 후보)
  for (const r of events) {
    const n: Node | undefined = byId[r.d.id]; if (!n) continue;
    for (const e of (inc[n.id] ?? []).slice(0, 3)) { const f = byId[e.from]; if (f) support.push({ layer: e.verification === 'evidenced' ? 'fact' : e.verification === 'hypothesis' ? 'hypothesis' : 'interpretation', text: `원인 후보: ${f.label} (${f.year}) → ${n.label} (${n.year}) — 연결 성격: ${D.relKo[e.rel] ?? e.rel}`, ids: e.claimIds.slice(0, 3) }); }
    for (const e of (out[n.id] ?? []).slice(0, 2)) { const t2 = byId[e.to]; if (t2) next.push({ layer: 'inference', text: `${n.label}에서 이어진 것: ${t2.label} (${t2.year})`, ids: [] }); }
  }
  if (events.length) trace.push(`연결 탐색: 관련 사건 ${events.length}개의 원인·결과 연결 확인`);

  // 비교 질문: 상위 두 대상을 나란히
  if (intents.includes('비교')) {
    const ents = [...industries.map((r) => r.d), ...topics.map((r) => r.d)].filter((d, k, a) => a.findIndex((x) => x.label === d.label) === k).slice(0, 2);
    if (ents.length === 2) {
      const [A, B] = ents;
      expl.push({ layer: 'inference', text: `비교 대상: ${A.label}(${A.years?.join('~') ?? '기간 미상'}) / ${B.label}(${B.years?.join('~') ?? '기간 미상'}). 시작 시점 차이 ${A.years && B.years ? Math.abs(A.years[0] - B.years[0]) + '년' : '확인 불가'}.`, ids: [] });
      const wa = new Set(tokenize(A.text)), wb = new Set(tokenize(B.text));
      const common = [...wa].filter((w) => wb.has(w) && w.length >= 2 && !tokens.includes(w)).slice(0, 12);
      if (common.length) expl.push({ layer: 'observed', text: `두 대상의 설명에 함께 나오는 말(공통 조건 후보): ${common.join(', ')}. 말이 겹친다고 구조가 같다는 뜻은 아니다.`, ids: [] });
      trace.push('비교: 두 대상의 기간과 설명에 함께 나오는 말을 계산');
      const IND = (D.industries as unknown as { industries: { id: string; label: string; stages: { period: string; kind: string; what: string; why: { layer: string; text: string; ids: string[] }[] }[]; worlds?: { at: string; box: { mode: string } }[] }[] }).industries ?? [];
      const ia = IND.find((x) => x.label === A.label), ib = IND.find((x) => x.label === B.label);
      if (ia && ib) {
        const seq = (x: typeof ia) => x.stages.map((st) => `${st.kind}(${st.period})`).join(' → ');
        calcs.push({ title: `${ia.label} ↔ ${ib.label} 단계 구조`, method: '두 산업 일대기의 단계 종류·시기를 나란히 놓고 같은 종류 단계의 시작 연도 차이를 계산', n: ia.stages.length + ib.stages.length,
          rows: [[ia.label, seq(ia)], [ib.label, seq(ib)], ...ia.stages.filter((st) => ib.stages.some((u) => u.kind === st.kind && parseInt(u.period) > 0) && parseInt(st.period) > 0).map((st) => { const u = ib.stages.find((v) => v.kind === st.kind && parseInt(v.period) > 0)!; return [`'${st.kind}' 단계 시작 차이`, `${parseInt(st.period)} vs ${parseInt(u.period)} (${Math.abs(parseInt(st.period) - parseInt(u.period))}년)`] as [string, string]; }),
            ['세계에서 들어온 방식', `${(ia.worlds ?? []).map((w) => `${w.at}: ${w.box.mode}`).join(', ') || '없음'} / ${(ib.worlds ?? []).map((w) => `${w.at}: ${w.box.mode}`).join(', ') || '없음'}`]] });
        const onlyA = ia.stages.filter((st) => !ib.stages.some((u) => u.kind === st.kind)).map((st) => st.kind), onlyB = ib.stages.filter((st) => !ia.stages.some((u) => u.kind === st.kind)).map((st) => st.kind);
        if (onlyA.length || onlyB.length) against.push({ layer: 'observed', text: `단계 구성이 다르다 — ${ia.label}에만 있는 단계: ${onlyA.join(', ') || '없음'} / ${ib.label}에만 있는 단계: ${onlyB.join(', ') || '없음'}. 같은 경로를 밟았다고 볼 수 없다.`, ids: [] });
        for (const [x, st] of [[ia, ia.stages[1] ?? ia.stages[0]], [ib, ib.stages[1] ?? ib.stages[0]]] as const) for (const w of st.why.slice(0, 1)) facts.push({ layer: w.layer === 'fact' ? 'fact' : 'interpretation', text: `[${x.label} · ${st.kind}] ${w.text}`, ids: w.ids, go: '#/field/industry' });
      }
    } else limits.push({ layer: 'unknown', text: '비교할 두 대상을 앱 안의 주제·산업에서 모두 찾지 못했다.', ids: [] });
  }
  if (intents.includes('반사실')) limits.push({ layer: 'unknown', text: '실제로 일어나지 않은 전개는 사실로 확인할 수 없다. 위 내용은 조건이 달랐다면 볼 지표와 갈림길을 보여 줄 뿐이다.', ids: [] });

  // 한계 — 규칙
  limits.push({ layer: 'inference', text: '이 답은 앱에 들어 있는 근거 문장과 지표에서만 만든다. 언어모델은 연결돼 있지 않고, 새로운 사실을 만들지 않는다.', ids: [] });
  if (rels.length) limits.push({ layer: 'inference', text: '상관은 인과가 아니다. 연도별 자료는 표본이 수십 개뿐이고, 같은 경기 흐름이 두 지표를 함께 움직일 수 있다.', ids: [] });
  if (!indObjs.length) need.push({ layer: 'unknown', text: `이 질문을 수치로 확인할 연도별 지표가 앱에 없다${tokens.length ? ` (${tokens.slice(0, 3).join('·')} 관련 통계 필요)` : ''}.`, ids: [] });
  if (missing.length) need.push({ layer: 'unknown', text: `앱 안에서 찾지 못한 말: ${missing.join(', ')} — 이 부분은 자료를 더 모아야 답할 수 있다.`, ids: [] });

  // 잠정 결론 — 근거의 양과 종류만 말한다
  const nf = facts.length, nh = expl.filter((l) => l.layer === 'hypothesis').length, na = against.length;
  if (!enough) concl.push({ layer: 'unknown', text: `근거 부족 — 핵심어 ${tokens.length}개 중 ${tokens.length - missing.length}개만 앱 자료에서 찾았다. 결론을 내지 않는다.`, ids: [] });
  else concl.push({ layer: 'inference', text: `확인된 사실 ${nf}개, 계산 ${calcs.length}건, 미검증 가설 ${nh}개, 반대 증거·다른 설명 ${na}개를 찾았다. ${na ? '반대 설명이 있어 한쪽으로 단정할 수 없다.' : '반대 증거를 찾지 못했지만, 찾지 못한 것이 없다는 뜻은 아니다.'}${topics[0] ? ` 가장 가까운 주제는 '${topicById[topics[0].d.id]?.label.split(' — ')[0]}'이며 그 결론: ${topicById[topics[0].d.id]?.conclusion.key.text}` : ''}`, ids: topics[0] ? topicById[topics[0].d.id]?.conclusion.key.ids ?? [] : [] });
  if (!next.length) next.push({ layer: 'inference', text: '기간을 정해(예: 1990년대) 다시 물으면 그 시기 자료만 계산한다.', ids: [] });

  trace.push(enough ? '조립: 사실·계산·해석·가설·반대 증거를 층위별로 나눔' : '조립 중단: 근거가 모자라 답 대신 필요한 자료를 정리');
  const dedup = (ls: ALine[]) => ls.filter((l, k) => ls.findIndex((m) => m.text === l.text) === k);
  return {
    q, tokens, missing, intents, years: yrs, enough, trace, hits, calcs,
    sections: [
      { key: 'target', title: '1. 질문과 분석 대상', lines: [{ layer: 'inference', text: `분석 대상: ${hits.slice(0, 5).map((h) => h.label.slice(0, 30)).join(' / ') || '찾지 못함'}`, ids: [] }] },
      { key: 'facts', title: '2. 확인된 사실', lines: dedup(facts).slice(0, 8) },
      { key: 'data', title: '3. 사용한 데이터와 계산', lines: dedup(data) },
      { key: 'expl', title: '4. 가능한 설명·가설·시나리오', lines: enough ? dedup(expl).slice(0, 10) : [] },
      { key: 'support', title: '5. 뒷받침하는 근거', lines: enough ? dedup(support).slice(0, 8) : [] },
      { key: 'against', title: '6. 반대 증거와 다른 설명', lines: enough ? dedup(against).slice(0, 8) : [] },
      { key: 'limits', title: '7. 인과 판단의 한계', lines: dedup(limits) },
      { key: 'concl', title: '8. 잠정 결론', lines: concl },
      { key: 'need', title: '9. 추가 검증에 필요한 자료와 방법', lines: dedup(need).slice(0, 6) },
      { key: 'next', title: '10. 다음에 물어볼 만한 것', lines: dedup(next).slice(0, 5) },
    ],
  };
}

/** 지시서 9-2: 이 답이 어떤 추론 유형으로 만들어졌는지 — 답의 층위와 질문 유형에서 센다(꾸며 넣지 않는다). */
export const REASON_KO: Record<string, string> = {
  인과: '원인→결과 연결을 따라감', 귀납: '여러 해의 수치·사례에서 경향을 셈', 연역: '이미 정리된 규칙(주제의 핵심 추론)을 이 질문에 적용',
  유추: '닮은 두 대상·시기를 나란히 놓음', 가설: '확인되지 않은 설명을 가설로 표시', 반사실: '일어나지 않은 전개를 조건으로만 다룸', 시나리오: '조건별로 갈라지는 가능성',
};
export function reasoningTypes(a: Answer): string[] {
  const ls = a.sections.flatMap((s) => s.lines);
  const has = (l: ALayer) => ls.some((x) => x.layer === l);
  const out: string[] = [];
  if (ls.some((x) => x.text.startsWith('원인 후보'))) out.push('인과');
  if (a.calcs.length || has('observed')) out.push('귀납');
  if (ls.some((x) => /^\[.+\] /.test(x.text) && x.layer !== 'fact')) out.push('연역');
  if (a.intents.includes('비교') || a.intents.includes('반복')) out.push('유추');
  if (has('hypothesis')) out.push('가설');
  if (a.intents.includes('반사실')) out.push('반사실');
  if (has('scenario')) out.push('시나리오');
  return out;
}
