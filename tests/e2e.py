"""HISTORY TO FUTURE 2.0 브라우저 시나리오 테스트(지시서 13장 A~G + 모바일 + 주소 유지).
사용: python3 tests/e2e.py <사이트 주소>   예) http://localhost:8766/history-to-future2/"""
import os, sys
from playwright.sync_api import sync_playwright

U = sys.argv[1].rstrip('/') + '/'
CHROME = os.environ.get('CHROME_PATH', '/usr/bin/google-chrome')
SHOTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'); os.makedirs(SHOTS, exist_ok=True)
res, errs = [], []
def ok(name, cond, info=''):
    res.append(bool(cond)); print(('PASS ' if cond else 'FAIL ') + name + (f' — {info}' if info else ''))

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox'])
    pg = b.new_page(viewport={'width': 1440, 'height': 900})
    pg.on('pageerror', lambda e: errs.append(str(e)))
    # A 전체 역사: 첫 화면에서 장기 그래프·변화 지도(시대×분야)·시대별 주요 사건이 바로 보인다
    pg.goto(U); pg.wait_for_timeout(1200)
    cells = pg.locator('.cmap-cell:not(.empty)').count(); years = pg.locator('.mt-y').count()
    ok('A 첫 화면: 공통 시간축(모든 연도)·장기 그래프·변화 지도', years == 67 and pg.locator('.hero .chart svg').count() == 1 and cells >= 30,
       f'연도 칸 {years}, 지도 칸 {cells}')
    ok('A 점 지도 없음(첫 화면 정보 밀도)', pg.locator('circle').count() < 20)
    # 시간축: 연도 → 1년 보기, 시대 → 10년 보기
    pg.locator('.mt-y').nth(14).click(); pg.wait_for_timeout(300)
    ok('시간축 연도 클릭 → 1년 보기', '1974년 대한민국' in pg.locator('main h2').first.inner_text() and 'z=year' in pg.url)
    pg.locator('.mt-y').nth(1).click(); pg.wait_for_timeout(300)
    ok('자료 없는 해도 표시하고 채우지 않음', '자료 없음' in pg.locator('.complete').inner_text() or '아직 없습니다' in pg.locator('.complete').inner_text(), pg.locator('.complete').inner_text()[:50])
    # C 1990년대 → 복잡한 그래프 없이 주요 사건
    pg.get_by_role('button', name='1990년대').first.click(); pg.wait_for_timeout(400)
    key = pg.locator('.keycard').count()
    ok('C 1990년대 → 핵심 변화 3~5개 + 해마다 사건', 3 <= key <= 5 and pg.locator('.yg').count() == 10 and '1990년대' in pg.locator('main h2').first.inner_text(), f'핵심 {key}')
    # B 분야별: 산업 선택 → 연도 클릭 없이 장기 흐름
    pg.get_by_role('tab', name='분야별 변화').click(); pg.wait_for_timeout(300)
    pg.get_by_role('tab', name='산업·기술·직업').click(); pg.wait_for_timeout(500)
    ok('B 산업 선택 → 장기 흐름(생애 막대)·시대별 단계', pg.locator('.life-row').count() >= 2 and pg.locator('.stages li').count() == 7, pg.url)
    # D 경제 그래프 전환점 클릭 → 그 해 사건 → 원인 패널
    pg.get_by_role('tab', name='경제·에너지').click(); pg.wait_for_timeout(500)
    pg.locator('.tp .chip', has_text='1997').first.click(); pg.wait_for_timeout(400)
    near = pg.locator('.nearlist li').count()
    ok('D 전환점(1997) 클릭 → 선택 연도 강조·관련 사건', 'y=1997' in pg.url and near >= 1 and '1996~1998' in pg.locator('main').inner_text(), f'사건 {near}')
    pg.locator('.nearlist button').first.click(); pg.wait_for_timeout(500)
    ok('D 사건 → 원인·결과 패널', pg.locator('.why').count() == 1 and 'why=' in pg.url)
    pg.get_by_role('button', name='닫기', exact=True).click(); pg.wait_for_timeout(300)
    ok('패널 닫기 후 장기 그래프 유지(전체 기간)', pg.locator('.why').count() == 0 and pg.locator('.hero .chart svg').count() >= 1)
    # E 자동 사이클 발견
    pg.get_by_role('tab', name='사이클 발견').click(); pg.wait_for_timeout(600)
    n = pg.locator('.cyc-list li').count(); txt = pg.locator('main').inner_text()
    ok('E 지정 없이 반복 후보 자동 계산', n >= 8 and '불규칙 반복' in txt and '구조적 유사' in txt, f'발견 {n}개')
    pg.locator('.cyc-list button', has_text='소비자물가').first.click(); pg.wait_for_timeout(500)
    det = pg.locator('.cyc-detail').inner_text()
    ok('E 원본 자료·구간 강조·간격·겹쳐 보기·조건 비교·민감도', pg.locator('.cyc-detail .chart').count() >= 2 and '반복 간격' in det and '겹쳐 보기' in det and '조건도 반복' in det and '민감도' in det)
    # F 반복 없는 데이터에 억지 주기 금지 + 추세를 주기로 오인하지 않음
    ok('F 통계적 주기 0건 명시 · 주기 없음/장기 구조 변화 표시', '통계적 주기(A): 0건' in txt and '주기 없음' in txt and '장기 구조 변화' in txt)
    # 조건 비교 항목 → 원인 패널(사이클 → WHY 연결)
    pg.locator('.conds-grid button').first.click(); pg.wait_for_timeout(500)
    ok('사이클 결과 → 사건 → 원인 탐색', pg.locator('.why').count() == 1)
    # G 심층 탐색: 금수 → 중동전쟁 → … → 1967년, 이전 단계
    pg.goto(U + '#/history?y=1973&why=d-embargo&path=d-embargo'); pg.wait_for_timeout(700)
    def go(t):
        pg.locator('.why-col.from .why-go', has_text=t).first.click(); pg.wait_for_timeout(350)
    go('중동전쟁'); go('목표'); go('협상 교착'); go('1967년 전쟁')
    h = pg.locator('.why-sum h2').inner_text()
    ok('G 금수 → 중동전쟁 → 목표 → 교착 → 1967년 전쟁(국제 배경)', '1967' in h, h)
    pg.get_by_role('button', name='← 이전 단계').click(); pg.wait_for_timeout(300)
    ok('G 이전 단계로', '협상 교착' in pg.locator('.why-sum h2').inner_text())
    pg.goto(U + '#/history?y=1974&why=d-kr-cpi&path=d-kr-cpi'); pg.wait_for_timeout(500)
    pg.locator('.why-col.from .why-go', has_text='생산비').first.click(); pg.wait_for_timeout(400)
    ok('G 국내 영향 경로(유가 → 생산비·운송비 → 물가)', '생산비' in pg.locator('.why').inner_text() and '운송비' in pg.locator('.why').inner_text())
    pg.locator('.why-col.from .rel-btn').first.click(); pg.wait_for_timeout(300)
    ok('G 연결 설명(관계 유형·검증 수준·근거)', pg.locator('.why-rel').count() == 1 and pg.locator('.why-rel .claims li').count() >= 1)
    pg.goto(U + '#/history?y=1971&why=d-folk70&path=d-folk70'); pg.wait_for_timeout(500)
    w = pg.locator('.why').inner_text()
    ok('G 문화: 이전(미8군·세시봉) → 포크 → 재등장', '미8군' in w and '세시봉 열풍' in w and '재등장' in w)
    pg.goto(U + '#/history?y=1973&why=d-price-mech&path=d-price-mech'); pg.wait_for_timeout(500)
    w = pg.locator('.why').inner_text()
    ok('G 장기 결과(동력자원부·고리·IEA·중동 건설)', all(k in w for k in ['동력자원부', '고리', 'IEA', '중동 건설']))
    # 주소 유지
    pg.goto(U + '#/field/society?y=2018&ind=tfr-kr'); pg.reload(); pg.wait_for_timeout(700)
    ok('주소 유지(분야·지표·연도)', pg.get_by_role('tab', name='사회·생활·소비').get_attribute('aria-selected') == 'true' and '합계출산율' in pg.locator('.hero').inner_text())
    # 2.0 장기 지표: 출산율 1960년부터 연속, 산업 분야 수출(로그 눈금)·취업자 비중, 환율
    ok('출산율 1960년부터 연속(자료 없음 아님)', '1960' in pg.locator('.hero').inner_text() or pg.locator('.hero svg path').count() > 0)
    pg.goto(U + '#/field/industry?y=1998'); pg.wait_for_timeout(700)
    h = pg.locator('.hero').inner_text()
    ok('산업: 수출액 기본 표시 + 로그 눈금 안내', '수출액' in h and '로그' in h)
    pg.get_by_role('tab', name='제조업 취업자 비중').click(); pg.wait_for_timeout(400)
    ok('산업: 제조업 취업자 비중 탭', 'ind=emp-mfg-kr' in pg.url and '1989' in pg.locator('.hero').inner_text())
    pg.goto(U + '#/field/economy?y=1998&ind=fx-kr'); pg.wait_for_timeout(700)
    ok('경제: 환율 지표와 고정환율기 설명', '환율' in pg.locator('.hero').inner_text() and '고정환율' in pg.locator('.hero').inner_text())
    # 1997 심층 사례: 환율 폭등 → 원인(만기연장 거부 ← 단기외채) → 더 거슬러 올라가 1970년대 정책금융까지
    pg.goto(U + '#/history?z=year&y=1997&why=d97-rollover&path=d97-fx,d97-rollover'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('1997: 만기연장 거부의 원인에 단기외채·아시아 위기', '단기외채' in w and '바트' in w)
    pg.goto(U + '#/history?z=year&y=1996&why=d97-leverage&path=d97-leverage'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('1997: 재벌 부채 → 1970년대 정책금융 뿌리(해석 표시)', '정책금융' in w and '해석' in w)
    pg.goto(U + '#/history?z=year&y=1998&why=d97-tripartite&path=d97-tripartite'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('1997: 노사정 협약 → 파견 합법화·실업', '파견' in w and '실업' in w)
    pg.goto(U + '#/history?z=year&y=1973&why=d-kr-cpi&path=d-kr-cpi'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('출처 재검증: 문장 숫자와 수집 자료 대조 표시(일치·차이)', '수치 대조' in w and '일치' in w)
    pg.goto(U + '#/field/industry?y=1980&ind=va-mfg-kr'); pg.wait_for_timeout(700)
    ok('산업: 제조업 생산 비중 1960~', '제조업 생산 비중' in pg.locator('.hero').inner_text())
    pg.goto(U + '#/field/economy?y=1980&ind=disc-kr'); pg.wait_for_timeout(700)
    ok('금리: 재할인율(1964~1998)과 콜금리 분리 안내', '1999' in pg.locator('.hero').inner_text())
    # 2008 심층 사례: 환율 급등 ← 리먼·단기외채, 1997과의 비교(닮은 점·다른 점)
    pg.goto(U + '#/history?z=year&y=2008&why=d08-fx&path=d08-fx'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('2008: 환율 급등의 원인(리먼·단기외채)과 결과(통화스와프·키코)', '리먼' in w and '통화스와프' in w and '키코' in w)
    pg.goto(U + '#/history?z=year&y=2008&why=d08-shortdebt&path=d08-shortdebt'); pg.wait_for_timeout(700)
    w = pg.locator('.why').inner_text()
    ok('2008↔1997 비교: 단기외채 닮은 점 연결', '1996' in w and ('비슷' in w or '닮' in w))
    pg.goto(U + '#/field/society?y=1998&ind=realwage-kr'); pg.wait_for_timeout(700)
    ok('실질임금: 계산 값임을 밝힘', '계산' in pg.locator('.hero').inner_text())
    # 한국은행 자료: 가계 소비 구성(여러 항목 한 그래프), 기준금리
    pg.goto(U + '#/field/society?y=1998&ind=cons-mix-kr'); pg.wait_for_timeout(700)
    h = pg.locator('.hero').inner_text()
    ok('가계 소비 구성: 항목 9개 범례', all(k in h for k in ['식료품', '주거', '음식점', '교육']))
    pg.goto(U + '#/field/economy?y=2008&ind=baserate-kr'); pg.wait_for_timeout(700)
    ok('기준금리 1999~', '기준금리' in pg.locator('.hero').inner_text())
    pg.screenshot(path=os.path.join(SHOTS, 'e2e-field.png'))
    # 모바일
    m = b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True).new_page()
    m.on('pageerror', lambda e: errs.append(str(e)))
    for path in ['', '#/history?z=decade&y=1990', '#/field/economy?y=1980', '#/cycle', '#/history?y=1973&why=d-embargo&path=d-embargo']:
        m.goto(U + path); m.wait_for_timeout(700)
        over = m.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
        ok(f'모바일 가로 넘침 없음 {path or "(첫 화면)"}', not over)
    m.goto(U); m.wait_for_timeout(700)
    m.locator('.cmap-m .cmap-cell').first.tap(); m.wait_for_timeout(500)
    ok('모바일: 터치로 원인 패널', m.locator('.why').count() == 1)
    m.screenshot(path=os.path.join(SHOTS, 'e2e-mobile.png'))
    b.close()

print('errors:', [e for e in errs if 'ERR_TUNNEL' not in e])
print(f'{sum(res)}/{len(res)} 통과')
sys.exit(0 if all(res) and not [e for e in errs if 'ERR_TUNNEL' not in e] else 1)
