import { InstallTip } from './ui/InstallTip';
import { useEffect } from 'react';
import { useRoute, type Tab } from './lib/route';
import { MasterTimeline } from './views/MasterTimeline';
import { HistoryView } from './views/HistoryView';
import { FieldView } from './views/FieldView';
import { CycleView } from './views/CycleView';
import { FlowView } from './views/FlowView';
import { NowView } from './views/NowView';
import { WhyPanel } from './ui/WhyPanel';
import { byId, eraOf } from './lib/data';

/**
 * HISTORY TO FUTURE 2.0 — 목적: 과거 변화의 조건과 전달 과정을 근거로 확인하고, 현재와 비교해 앞으로 볼 지표를 찾는다.
 *   지금 판단하기: 판단 질문 → 과거 흐름 → 연결 근거 → 현재 비교 → 조건별 시나리오 → 관찰 지표(첫 화면)
 *   전체 역사: 시대 전체의 의미(이전 → 달라진 것 → 다음으로) / 변화 흐름: 질문 하나를 근거와 함께 깊게
 *   분야별 변화: 한 분야의 장기 흐름과 그 안에서의 역할 / 반복·비교: 닮은 점·다른 점·한계
 *   사건 상세(원인·결과 패널): 구체적인 내용과 근거 — 어디서든 열리고, 들어온 흐름으로 돌아갈 수 있다.
 */
const TABS: { id: Tab; t: string; d: string }[] = [
  { id: 'now', t: '지금 판단하기', d: '과거로 현재를 읽고 볼 지표 찾기' },
  { id: 'flow', t: '변화 흐름', d: '한 주제를 시대별로 끝까지' },
  { id: 'history', t: '전체 역사', d: '시대별 사건 둘러보기' },
  { id: 'field', t: '분야별 변화', d: '한 분야의 지표와 사건' },
  { id: 'cycle', t: '반복·비교', d: '닮은 점·다른 점 검증' },
];

export function App() {
  const [r, nav] = useRoute();
  const why = (id: string, from?: string) => nav({ why: id, path: [id], rel: undefined, from: from ?? (r.tab === 'flow' ? r.flow : undefined) });
  useEffect(() => { document.body.classList.toggle('lock', !!r.why); }, [r.why]);
  const sel = r.why ? byId[r.why] : undefined;
  return (
    <div className="app">
      <header className="top">
        <a className="brand" href="#/now" aria-label="HISTORY TO FUTURE 2.0 처음으로">
          <span className="logo" aria-hidden /> HISTORY <em>TO</em> FUTURE <sup>2.0</sup>
        </a>
        <nav className="tabs" role="tablist" aria-label="탐색">
          {TABS.map((t) => (
            <button key={t.id} role="tab" aria-selected={r.tab === t.id} className={r.tab === t.id ? 'on' : ''} onClick={() => nav({ tab: t.id, flow: undefined, study: undefined, why: undefined, path: [], from: undefined })}>
              <b>{t.t}</b><span>{t.d}</span>
            </button>
          ))}
        </nav>
      </header>
      <div className="sticky">
        <MasterTimeline r={r} nav={nav} />
        <p className="ctx">지금 보는 시점 <b>{eraOf(r.y).label} · {r.y}년</b>{sel && <> · 원인 탐색: <b>{sel.label}</b></>}</p>
      </div>
      <main>
        {r.tab === 'now' && <NowView r={r} nav={nav} why={why} />}
        {r.tab === 'history' && <HistoryView r={r} nav={nav} why={why} />}
        {r.tab === 'flow' && <FlowView r={r} nav={nav} why={why} />}
        {r.tab === 'field' && <FieldView r={r} nav={nav} why={why} />}
        {r.tab === 'cycle' && <CycleView r={r} nav={nav} why={why} />}
      </main>
      <InstallTip />
      <footer className="foot">
        <p>모든 문장은 출처와 확인 수준(두 곳 이상 확인 / 한 곳 확인 / 출처 미확보)을 가집니다. 같은 발표를 옮긴 기사들은 한 곳으로 셉니다. 원인·결과 연결은 인과·조건·상관·시간 순서·해석·가설로 따로 표시합니다. 자료가 없는 부분은 채우지 않고 '자료 없음'으로 둡니다 — 자료가 없다는 것과 그런 일이 없었다는 것은 다릅니다.</p>
        <p className="muted">빌드 {__BUILD_ID__} · 경제 지표: FRED(원자료 OECD·세계은행) — This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.</p>
      </footer>
      <WhyPanel r={r} nav={nav} />
    </div>
  );
}
