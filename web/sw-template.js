/* HISTORY TO FUTURE 2.0 서비스 워커 — 한 번 연 화면은 인터넷이 약해도 열리게 한다. */
const CACHE = 'htf2-__ID__';
const PRECACHE = __ASSETS__;
self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k.startsWith('htf2-') && k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // 화면(HTML)은 네트워크 우선: 새 버전이 있으면 바로 받고, 끊겼을 때만 저장본
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then((r) => { const c = r.clone(); caches.open(CACHE).then((ca) => ca.put('./', c)); return r; }).catch(() => caches.match('./')));
    return;
  }
  // 같은 사이트의 파일과 글꼴(CDN)은 저장본 우선
  if (url.origin === location.origin || url.hostname === 'cdn.jsdelivr.net') {
    e.respondWith(caches.match(req).then((hit) => hit || fetch(req).then((r) => {
      if (r.ok || r.type === 'opaque') { const c = r.clone(); caches.open(CACHE).then((ca) => ca.put(req, c)); }
      return r;
    })));
  }
});
