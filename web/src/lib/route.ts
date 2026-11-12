import { useEffect, useState } from 'react';
import { CATS, MAX_Y, MIN_Y, type Cat } from './data';

/**
 * 모든 탐색 상태는 주소(#/...)에 있다 → 새로고침·공유·뒤로 가기가 그대로 동작.
 *   #/history?z=all|decade|year&y=1973
 *   #/field/economy?y=1973&ind=cpi-kr
 *   #/cycle?f=<발견 id>&y=1973
 *   #/flow/<흐름 id>?y=1995 (흐름 목록은 #/flow)
 *   #/now (첫 화면: 목적과 판단 질문) · #/now/<분석 id>
 *   from=<흐름 id>: 흐름을 읽다가 사건 상세를 열었을 때 돌아갈 곳
 *   공통: why=<노드 id>&path=a,b,c (원인 탐색 패널), rel=<관계 id>
 */
export type Tab = 'now' | 'history' | 'flow' | 'field' | 'cycle';
export type Zoom = 'all' | 'decade' | 'year';
export interface Route { tab: Tab; cat: Cat; z: Zoom; y: number; ind?: string; f?: string; flow?: string; study?: string; from?: string; why?: string; path: string[]; rel?: string }

export function parse(hash: string): Route {
  const [p, q = ''] = hash.replace(/^#\/?/, '').split('?');
  const [tab0, cat0] = p.split('/');
  const s = new URLSearchParams(q);
  const y = Number(s.get('y'));
  const tab: Tab = (['now', 'history', 'flow', 'field', 'cycle'] as Tab[]).includes(tab0 as Tab) ? (tab0 as Tab) : 'now';
  const z = s.get('z') as Zoom;
  return {
    tab,
    cat: CATS.includes(cat0 as Cat) ? (cat0 as Cat) : 'economy',
    z: (['all', 'decade', 'year'] as Zoom[]).includes(z) ? z : 'all',
    y: y >= MIN_Y && y <= MAX_Y ? y : 1973,
    ind: s.get('ind') || undefined,
    f: s.get('f') || undefined,
    flow: tab === 'flow' ? cat0 || undefined : undefined,
    study: tab === 'now' ? cat0 || undefined : undefined,
    from: s.get('from') || undefined,
    why: s.get('why') || undefined,
    path: (s.get('path') ?? '').split(',').filter(Boolean),
    rel: s.get('rel') || undefined,
  };
}

export function hashOf(r: Route): string {
  const s = new URLSearchParams();
  if (r.tab === 'history' && r.z !== 'all') s.set('z', r.z);
  s.set('y', String(r.y));
  if (r.tab === 'field' && r.ind) s.set('ind', r.ind);
  if (r.tab === 'cycle' && r.f) s.set('f', r.f);
  if (r.why) { if (r.from) s.set('from', r.from); s.set('why', r.why); if (r.path.length) s.set('path', r.path.join(',')); if (r.rel) s.set('rel', r.rel); }
  const p = r.tab === 'field' ? `field/${r.cat}` : r.tab === 'flow' && r.flow ? `flow/${r.flow}` : r.tab === 'now' && r.study ? `now/${r.study}` : r.tab;
  return `#/${p}?${s.toString().replace(/%2C/g, ',')}`;
}

export function useRoute(): [Route, (patch: Partial<Route>) => void] {
  const [h, setH] = useState(location.hash);
  useEffect(() => {
    const f = () => setH(location.hash);
    window.addEventListener('hashchange', f);
    return () => window.removeEventListener('hashchange', f);
  }, []);
  const r = parse(h);
  return [r, (patch) => { location.hash = hashOf({ ...r, ...patch }); }];
}
