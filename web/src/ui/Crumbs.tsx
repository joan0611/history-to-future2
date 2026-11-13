import { CAT_KO, D, flowById, studyById, topicById } from '../lib/data';
import type { Route } from '../lib/route';

/**
 * 지금 어디에 있나(지시서 13): 처음 → 큰 화면 → 분야 → 지금 보는 것.
 * 각 칸을 누르면 그 단계로 돌아가고, 사건을 읽다 들어왔으면 '읽던 곳으로' 버튼이 생긴다.
 */
type Nav = (p: Partial<Route>) => void;
const TAB_KO: Record<string, string> = { now: '지금 판단하기', topic: '주제 이야기', taste: '주제 이야기', flow: '주제 이야기', history: '시대별 사건 찾기', field: '분야별 지표', cycle: '반복과 비교', ask: '질문 분석' };
const short = (s: string, n = 26) => (s.length > n ? s.slice(0, n - 1) + '…' : s);

export function Crumbs({ r, nav }: { r: Route; nav: Nav }) {
  if (r.tab === 'now' && !r.study) return null;
  const items: { label: string; go?: () => void }[] = [{ label: '처음', go: () => nav({ tab: 'now', study: undefined, topic: undefined, flow: undefined, taste: undefined, why: undefined, path: [], from: undefined }) }];
  const toTab = () => nav({ tab: r.tab === 'taste' || r.tab === 'flow' ? 'topic' : r.tab, topic: undefined, flow: undefined, taste: undefined, study: undefined, ind: undefined, f: undefined, why: undefined, path: [] });
  items.push({ label: TAB_KO[r.tab] ?? r.tab, go: toTab });
  if (r.tab === 'topic' && r.topic) {
    const t = topicById[r.topic];
    const fd = D.topics.fieldMap.find((f) => f.items.some((x) => x.kind === 'topic' && x.id === r.topic));
    if (fd) items.push({ label: short(fd.label.split(' — ')[0], 18), go: () => { nav({ topic: undefined }); window.setTimeout(() => document.getElementById(`fd-${fd.id}`)?.scrollIntoView(), 120); } });
    items.push({ label: short(t?.label.split(' — ')[0] ?? r.topic) });
  }
  if (r.tab === 'flow' && r.flow) items.push({ label: short(flowById[r.flow]?.topic ?? r.flow) });
  if (r.tab === 'taste' && r.taste) items.push({ label: short(D.tastes.flows.find((f) => f.id === r.taste)?.title ?? r.taste) });
  if (r.tab === 'now' && r.study) items.push({ label: short((studyById[r.study] as unknown as { question?: string; title?: string })?.question ?? r.study) });
  if (r.tab === 'field') {
    items.push({ label: CAT_KO[r.cat], go: () => nav({ ind: undefined }) });
    if (r.ind) items.push({ label: short(D.indicators.find((i) => i.id === r.ind)?.title ?? r.ind) });
  }
  if (r.tab === 'cycle' && r.f) items.push({ label: short(D.findings.find((f) => f.id === r.f)?.title ?? r.f) });
  if (r.tab === 'ask') items.push({ label: r.q ? `"${short(r.q, 30)}"` : r.ta ? '두 지표 검정' : '새 질문' });
  return (
    <nav className="where" aria-label="지금 위치">
      <span className="where-k">지금 위치</span>
      <ol>
        {items.map((x, i) => (
          <li key={i} aria-current={i === items.length - 1 ? 'page' : undefined}>
            {x.go && i < items.length - 1 ? <button type="button" className="link" onClick={x.go}>{x.label}</button> : <b>{x.label}</b>}
          </li>
        ))}
      </ol>
      {r.from && flowById[r.from] && <button type="button" className="chip where-back" onClick={() => nav({ tab: 'flow', flow: r.from, from: undefined, why: undefined, path: [] })}>← 읽던 흐름으로: {short(flowById[r.from].topic, 18)}</button>}
    </nav>
  );
}
