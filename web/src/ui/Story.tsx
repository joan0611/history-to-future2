import { useState } from 'react';
import { D, flowById, type SLine, type StepNote } from '../lib/data';
import type { Route } from '../lib/route';
import { Claims } from './WhyPanel';

/** 흐름 이야기(11개 질문)와 단계 풀이(그때 분위기 → 이어진 변화) — 시대별 흐름과 취향 흐름이 같이 쓴다. */
const X = D.stories;
const HELP: Record<string, string> = {
  fact: '자료에서 직접 확인한 사실', source: '기자·연구자·업계가 한 해석(출처의 말)',
  inference: 'AI 종합 추론 — 이 사이트가 사실을 이어 붙인 설명(출처의 주장이 아님)', hypothesis: '탐색·전망 가설 — 확인이 필요',
};

export function SBadge({ l }: { l: SLine['layer'] }) {
  return <span className={`lyr l-${l}`} title={HELP[l]}>{X.layers[l]}</span>;
}

export function SLineView({ x }: { x: SLine }) {
  const [open, setOpen] = useState(false);
  return (
    <div className={`tl l-${x.layer}`}>
      <span className="tl-t"><SBadge l={x.layer} /> {x.text} {x.ids.length > 0 && <button className="link small" onClick={() => setOpen(!open)}>{open ? '접기' : x.layer === 'inference' || x.layer === 'hypothesis' ? `바탕이 된 사실 ${x.ids.length}` : `근거 ${x.ids.length}`}</button>}</span>
      {open && <Claims ids={x.ids} all />}
    </div>
  );
}

type Nav = (p: Partial<Route>) => void;
const tasteIds = new Set(D.tastes.flows.map((f) => f.id));
const flowName = (id: string) => (tasteIds.has(id) ? D.tastes.flows.find((f) => f.id === id)?.title : flowById[id]?.topic) ?? id;
const stepName = (flow: string, step?: string) => (step ? flowById[flow]?.steps.find((s) => s.id === step)?.title : undefined);

/** 다른 흐름(의 특정 단계)으로 바로 이동 */
export function goTo(nav: Nav, flow: string, step?: string) {
  if (tasteIds.has(flow)) nav({ tab: 'taste', taste: flow, flow: undefined, study: undefined });
  else nav({ tab: 'flow', flow, taste: undefined, study: undefined });
  if (step) window.setTimeout(() => document.getElementById(`step-${step}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' }), 450);
  else window.setTimeout(() => window.scrollTo({ top: 0 }), 50);
}

export function GoChip({ nav, flow, step, label }: { nav: Nav; flow: string; step?: string; label?: string }) {
  const st = stepName(flow, step);
  return <button className="chip go" onClick={() => goTo(nav, flow, step)}>{label ?? `${flowName(flow)}${st ? ` · ${st}` : ''}`} →</button>;
}

/** 흐름 이야기 — 11개 질문은 내부 점검 기준으로만 쓰고, 화면에는 시간 순서로 이어지는 세 대목의 이야기로 보여 준다(R-Q6). */
const ACTS: { id: string; title: string; keys: string[] }[] = [
  { id: 'a1', title: '처음에는 — 무엇을 골랐고 어떻게 퍼졌나', keys: ['before', 'popular', 'spread', 'satisfy'] },
  { id: 'a2', title: '그다음 — 무엇이 불편해졌고, 어떤 조건에서 새 선택이 자랐나', keys: ['friction', 'newchoice', 'conditions', 'suppliers', 'relation'] },
  { id: 'a3', title: '지금과 앞으로 — 남은 불편, 그리고 갈 수 있는 방향', keys: ['unmet', 'next'] },
];
export function StoryQA({ id, nav }: { id: string; nav: Nav }) {
  const st = X.stories[id];
  if (!st) return null;
  return (
    <section className="panel story" id="story">
      <h2>이 흐름의 이야기 <span className="sub">연표가 아니라 선택 기준이 어떻게 바뀌었나</span></h2>
      <p className="lead">{st.lead}</p>
      <p className="muted small">표시: <SBadge l="fact" /> <SBadge l="source" /> <SBadge l="inference" /> <SBadge l="hypothesis" /> — 'AI 추론'과 '가설'은 출처의 주장이 아닙니다.</p>
      <div className="story-acts">
        {ACTS.map((a) => {
          const lines = a.keys.flatMap((k) => st.qs[k] ?? []);
          if (!lines.length) return null;
          return (
            <div key={a.id} className="story-act">
              <h3>{a.title}</h3>
              {lines.map((x, i) => <SLineView key={i} x={x} />)}
            </div>
          );
        })}
      </div>
      {st.links.length > 0 && (
        <div className="story-links">
          <h3>이어서 보기 — 연결된 흐름</h3>
          <ul>{st.links.map((l, i) => <li key={i}><GoChip nav={nav} flow={l.flow} step={l.step} /> <span className="muted small">{l.why}</span></li>)}</ul>
        </div>
      )}
    </section>
  );
}

/** 단계 하나의 풀이 — 그때 분위기, 이어진 변화(분야별), 다른 흐름으로 바로 가기 */
export function StepNoteView({ flow, step, nav }: { flow: string; step: string; nav: Nav }) {
  const n: StepNote | undefined = X.stepNotes[`${flow}/${step}`];
  if (!n) return null;
  return (
    <div className="stepnote">
      <p className="sn-h">그때 분위기</p>
      {n.mood.map((x, i) => <SLineView key={i} x={x} />)}
      <p className="sn-h">이어진 변화 — 사회·산업·소비·문화</p>
      <ul className="sn-ripple">
        {n.ripple.map((r, i) => (
          <li key={i}><span className="sn-area">{r.area}</span><SLineView x={r.line} />{r.go && <GoChip nav={nav} flow={r.go[0]} step={r.go[1]} />}</li>
        ))}
      </ul>
      {n.after && <><p className="sn-h">반대편</p><SLineView x={n.after} /></>}
    </div>
  );
}
