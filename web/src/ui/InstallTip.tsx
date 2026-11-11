import { useEffect, useState } from 'react';

// 홈 화면에 앱처럼 추가하기 안내. 이미 앱으로 열었거나 닫기를 누르면 보이지 않는다.
type BIP = Event & { prompt: () => Promise<void>; userChoice: Promise<{ outcome: string }> };

const standalone = () =>
  window.matchMedia?.('(display-mode: standalone)').matches || (navigator as unknown as { standalone?: boolean }).standalone === true;

export function InstallTip() {
  const [evt, setEvt] = useState<BIP | null>(null);
  const [hidden, setHidden] = useState(() => {
    try { return standalone() || localStorage.getItem('htf2-install-dismissed') === '1'; } catch { return standalone(); }
  });
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const on = (e: Event) => { e.preventDefault(); setEvt(e as BIP); };
    window.addEventListener('beforeinstallprompt', on);
    return () => window.removeEventListener('beforeinstallprompt', on);
  }, []);
  if (hidden) return null;
  const ios = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const close = () => { setHidden(true); try { localStorage.setItem('htf2-install-dismissed', '1'); } catch { /* 저장 안 돼도 이번에는 숨김 */ } };
  return (
    <div className="install" role="note">
      <span className="install-ic" aria-hidden>＋</span>
      <span><b>앱처럼 쓰기</b> — 휴대폰 홈 화면에 추가하면 아이콘으로 바로 열리고, 한 번 본 화면은 인터넷이 약해도 열립니다.</span>
      {evt
        ? <button className="install-btn" onClick={async () => { await evt.prompt(); const c = await evt.userChoice; if (c.outcome === 'accepted') close(); }}>홈 화면에 추가</button>
        : <button className="install-btn" onClick={() => setOpen((v) => !v)} aria-expanded={open}>추가하는 법</button>}
      <button className="install-x" aria-label="안내 닫기" onClick={close}>✕</button>
      {open && !evt && (
        <ol className="install-how">
          {ios
            ? <><li>사파리 아래쪽 <b>공유</b> 버튼(네모에 위쪽 화살표)을 누릅니다.</li><li><b>홈 화면에 추가</b>를 누르고 오른쪽 위 <b>추가</b>를 누릅니다.</li></>
            : <><li>크롬·삼성 인터넷의 <b>메뉴(⋮ 또는 ≡)</b>를 엽니다.</li><li><b>홈 화면에 추가</b> 또는 <b>앱 설치</b>를 누릅니다.</li></>}
        </ol>
      )}
    </div>
  );
}
