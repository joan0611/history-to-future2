import { InstallTip } from './ui/InstallTip';
import { useEffect } from 'react';
import { useRoute, type Tab } from './lib/route';
import { MasterTimeline } from './views/MasterTimeline';
import { HistoryView } from './views/HistoryView';
import { FieldView } from './views/FieldView';
import { CycleView } from './views/CycleView';
import { WhyPanel } from './ui/WhyPanel';
import { byId, eraOf } from './lib/data';

/**
 * HISTORY TO FUTURE 2.0 — 최상위 진입점 세 개(전체 역사 · 분야별 변화 · 사이클 발견)와
 * 어디서든 열리는 원인·결과 패널. 모든 화면이 같은 시간축(MASTER TIMELINE)과 같은 주소 상태를 공유한다.
 */
const TABS: { id: Tab; t: string; d: string }[] = [
  { id: 'history', t: '전체 역사', d: '1960→현재 흐름과 주요 사건' },
  { id: 'field', t: '분야별 변화', d: '분야마다 수십 년의 동향' },
  { id: 'cycle', t: '사이클 발견', d: '데이터가 찾은 반복과 유사성' },
];

export function App() {
  const [r, nav] = useRoute();
  const why = (id: string) => nav({ why: id, path: [id], rel: undefined });
  useEffect(() => { document.body.classList.toggle('lock', !!r.why); }, [r.why]);
  const sel = r.why ? byId[r.why] : undefined;
  return (
    <div className="app">
      <header className="top">
        <a className="brand" href="#/history" aria-label="HISTORY TO FUTURE 2.0 처음으로">
          <span className="logo" aria-hidden /> HISTORY <em>TO</em> FUTURE <sup>2.0</sup>
        </a>
        <nav className="tabs" role="tablist" aria-label="탐색">
          {TABS.map((t) => (
            <button key={t.id} role="tab" aria-selected={r.tab === t.id} className={r.tab === t.id ? 'on' : ''} onClick={() => nav({ tab: t.id })}>
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
        {r.tab === 'history' && <HistoryView r={r} nav={nav} why={why} />}
        {r.tab === 'field' && <FieldView r={r} nav={nav} why={why} />}
        {r.tab === 'cycle' && <CycleView r={r} nav={nav} why={why} />}
      </main>
      <InstallTip />
      <footer className="foot">
        <p>모든 문장은 출처와 검증 상태를 가집니다(독립 출처 2개 이상 / 1개 / 출처 필요). 인과·해석·시간적 선후를 구분해 표시합니다. 자료가 없는 기간은 채우지 않고 '자료 없음'으로 둡니다.</p>
        <p className="muted">빌드 {__BUILD_ID__} · 경제 지표: FRED(원자료 OECD·세계은행) — This product uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis.</p>
      </footer>
      <WhyPanel r={r} nav={nav} />
    </div>
  );
}
