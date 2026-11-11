import { D, YEARS, eraEnd, eraOf, yearCount } from '../lib/data';
import type { Route } from '../lib/route';

/**
 * MASTER TIMELINE — 모든 화면의 공통 시간축. 1960년부터 현재까지 모든 연도를 빠짐없이 한 줄에.
 * 칸 높이 = 그 해에 정리된 자료 수(0이면 빈 칸으로 드러냄). 시대 이름을 누르면 10년 보기, 연도를 누르면 1년 보기.
 */
export function MasterTimeline({ r, nav }: { r: Route; nav: (p: Partial<Route>) => void }) {
  const max = Math.max(...Object.values(yearCount));
  const cur = eraOf(r.y);
  const pickYear = (y: number) => nav(r.tab === 'history' ? { y, z: r.z === 'all' ? 'year' : r.z } : { y });
  return (
    <div className="mt" aria-label="1960년부터 현재까지 공통 시간축">
      <div className="mt-eras">
        {D.eras.map((e) => (
          <button key={e.id} className={`mt-era${e.id === cur.id ? ' on' : ''}`} style={{ flexGrow: eraEnd(e) - e.startYear + 1 }}
            onClick={() => nav(r.tab === 'history' ? { y: e.id === '1970s' ? 1973 : e.startYear, z: 'decade' } : { y: e.startYear })}>
            {e.label.replace('~현재', '')}
          </button>
        ))}
      </div>
      <div className="mt-years" role="group" aria-label="연도 선택">
        {YEARS.map((y) => {
          const c = yearCount[y] ?? 0;
          return (
            <button key={y} className={`mt-y${y === r.y ? ' on' : ''}${c ? '' : ' empty'}${y % 10 === 0 ? ' dec' : ''}`} onClick={() => pickYear(y)}
              aria-label={`${y}년 ${c ? `자료 ${c}개` : '자료 없음'}`} aria-pressed={y === r.y} title={`${y} · ${c ? `자료 ${c}개` : '자료 없음'}`}>
              <i style={{ height: c ? 4 + (c / max) * 18 : 2 }} />
            </button>
          );
        })}
      </div>
      <div className="mt-labels" aria-hidden>
        {YEARS.filter((y) => y % 10 === 0).map((y) => <span key={y} style={{ left: `${((y - 1960) / YEARS.length) * 100}%` }}>{y}</span>)}
        <span className="sel" style={{ left: `${((r.y - 1960 + 0.5) / YEARS.length) * 100}%` }}>{r.y}</span>
      </div>
    </div>
  );
}
