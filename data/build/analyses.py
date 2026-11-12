"""대표 경제 분석 — 과거 흐름 → 연결 근거 → 현재 비교 → 조건별 시나리오 → 관찰 지표.

원칙
- 추적하는 변수를 먼저 정한다(여기서는 '가계의 실질 소비'와 그것을 받치는 조건). 정책·사건은 그 변수의 변화를 설명하는 위치에만 둔다.
- 모든 사실 문장은 주장(claim)으로 두고 출처를 단다. 같은 공식 발표를 옮긴 기사들은 origin으로 묶어 한 곳으로 센다.
- 사이트가 자료를 묶어 쓴 문장은 kind='synthesis'로 표시하고, 근거 주장 id를 함께 단다.
- 시나리오는 '조건 → 작동 과정'만 쓴다. 확률·전망 수치·임의의 기준값은 만들지 않는다.
- 현재 상태는 자료마다 기준일을 붙인다(자료 끝 시점 ≠ 오늘).
"""

A = "2026-11-12"


def S(id, title, pub, url, stype, published=None, note=None, origin=None):
    d = {"id": id, "title": title, "publisher": pub, "url": url, "sourceType": stype, "accessedDate": A}
    if published:
        d["publishedDate"] = published
    if note:
        d["note"] = note
    if origin:
        d["origin"] = origin
    return d


def C(id, text, ctype, status, sources, domains, period=None, scope=None, support=None):
    d = {"id": id, "text": text, "claimType": ctype, "status": status, "sourceIds": sources,
         "domains": domains, "countries": ["KR"], "aiSynthesized": False}
    if period:
        d["period"] = period
    if scope:
        d["scope"] = scope
    if support:
        d["support"] = support
    return d


SOURCES = [
    # 과거 국면
    S("an-newsis-250423", "외환위기·카드대란·금융위기·코로나 때 '뚝' — 대한상의 내수소비 분석", "뉴시스",
      "https://mobile.newsis.com/view/NISX20250423_0003150282", "news", published="2025-04-23", origin="korcham-2025-consumption"),
    S("an-kyeonggi-210126", "2020년 연간 GDP -1%… 민간소비 1998년 이후 최대 감소", "경기일보",
      "https://www.kyeonggi.com/article/202101261154451", "news", published="2021-01-26", origin="bok-gdp-2020"),
    S("an-kostat-0304", "소비 부진의 원인(1996~2004년 GDP·고용·가계수지 분석)", "통계청",
      "https://lib1.kostat.go.kr/dl_image2/IMG/01/000000000238/SERVICE/000000000238_01.PDF", "government",
      note="당시 국민계정 기준. 이후 기준년 개편으로 값이 달라졌다."),
    S("an-saesayon-card", "2003 신용카드 부실 확산으로 국민경제 흔들", "새로운사회를여는연구원",
      "https://saesayon.org/AttachFiles/1267085553255_1.pdf", "institution"),
    S("an-hri-041013", "경제주평 — 소비 침체의 원인(2004.10.13)", "현대경제연구원",
      "https://test.hri.co.kr/upload/board/BSR20041013_2.pdf", "institution", published="2004-10-13"),
    S("an-aju-100126", "지난해 성장률 0.2%… 외환위기 이후 11년 만에 최저", "아주경제",
      "https://www.ajunews.com/view/20100126000014", "news", published="2010-01-26", origin="bok-gdp-2009"),
    S("an-hri-2014", "민간소비 침체와 일자리 기회 상실(2014)", "현대경제연구원",
      "https://test.hri.co.kr/upload/board/201431081028%5b1%5d.pdf", "institution", published="2014"),
    S("an-seoul-200423", "1분기 성장률 -1.4%, 2008년 이후 최저…민간소비·서비스업 '직격탄'", "서울신문",
      "https://m.seoul.co.kr/news/2020/04/23/20200423500014", "news", published="2020-04-23"),
    S("an-aju-230308", "빚 상환 부담에 집값 하락까지…한은 \"올해 국내 민간소비 상당폭 둔화\"", "아주경제",
      "https://www.ajunews.com/view/20230308100949352", "news", published="2023-03-08", note="한국은행 BOK이슈노트 '국별 비교를 통한 소비흐름 평가 및 향후 점검' 보도"),
    S("an-newsis-230828", "한은 '민간소비 회복 모멘텀에 대한 평가' — 주택대출 동반한 집값 반등이 소비 제약", "뉴시스(블록미디어 전재)",
      "https://www.blockmedia.co.kr/archives/359165", "news", published="2023-08-28"),
    S("an-imaeil-250112", "지갑 닫는 시민들…'소매판매 절벽' 21년 만에 최악", "매일신문",
      "https://www.imaeil.com/page/view/2025011214043063683", "news", published="2025-01-12"),
    S("an-dailian-221207", "한은 \"DSR 1%p 증가 시, 가구 연간 소비 평균 0.37%↓\"", "데일리안",
      "https://www.dailian.co.kr/news/view/1181080/", "news", published="2022-12-07"),
    S("an-fn-251128", "\"쌓이는 가계부채가 소비를 누른다\" 한은의 지적", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202511281540422411", "news", published="2025-11-28"),
    S("an-asiae-260115", "지난해 말 GDP 대비 가계부채 비율 89.0%", "아시아경제",
      "https://view.asiae.co.kr/article/2026011514373334962", "news", published="2026-01-15"),
    # 현재
    S("an-kdi-mpc-1022", "통화정책방향: 기준금리 3.00% 유지(2026.10.22)", "한국은행(KDI 경제교육·정보센터 게시)",
      "https://eiec.kdi.re.kr/policy/materialView.do?num=288401", "government", published="2026-10-22", origin="bok-mpc-2026-10"),
    S("an-kbmaeil-261022", "한은, 기준금리 3.00% 동결…물가·집값에 11월 인상 불씨", "경북매일",
      "https://kbmaeil.com/article/20261022500138", "news", published="2026-10-22", origin="bok-mpc-2026-10"),
    S("an-sidae-260923", "9월 소비자심리지수 106.6 — 8월 기준금리 2.75%→3.00% 인상 뒤 첫 조사", "시대에듀 시사",
      "https://www.sidae.com/article/2026092310184299257", "news", published="2026-09-23"),
    S("an-tomato-261027", "수출·혈세로 버틴 '성장'…반도체 호황 '착시'", "뉴스토마토",
      "https://newstomato.com/ReadNews.aspx?no=1318201", "news", published="2026-10-27", origin="bok-gdp-2026q3"),
    S("an-khan-261027", "3분기 성장률 1.0% — 민간소비는 특이 요인으로 감소", "경향신문",
      "https://khan.co.kr/article/202610271630001", "news", published="2026-10-27", origin="bok-gdp-2026q3"),
    S("an-yna-kdi-11", "KDI 경제동향 — '美 중간선거' 결과에 \"주요국 정책 불확실성 확대\"", "연합뉴스(한민족센터 전재)",
      "https://www.koreancenter.or.kr/news/articleView.html?idxno=1436714", "news", published="2026-11"),
    S("an-korea-cpi-1103", "2026년 10월 소비자물가동향 브리핑", "대한민국 정책브리핑(국가데이터처)",
      "https://www.korea.kr/briefing/policyBriefingView.do?newsId=156787698", "government", published="2026-11-03", origin="kostat-cpi-2026-10"),
    S("an-tomato-cpi-1103", "소비자물가 두 달째 '2%대 ↑'…'석유 최고가격제' 딜레마", "뉴스토마토",
      "https://newstomato.com/ReadNews.aspx?no=1319121", "news", published="2026-11-03", origin="kostat-cpi-2026-10"),
    S("an-inews-0827", "고유가지원금이 가린 소득 감소…2분기 실질 근로소득 사실상 뒷걸음질", "아이뉴스24",
      "https://www.inews24.com/view/1998873", "news", published="2026-08-27", origin="kostat-hh-2026q2"),
    S("an-herald-0826", "4~6월 가구소득 4.5%↑…근로소득은 0.8% '찔끔', 나랏돈이 끌어올렸다", "헤럴드경제",
      "https://www.heraldk.com/article/2026082620003918464", "news", published="2026-08-27", origin="kostat-hh-2026q2"),
    S("an-sbs-0827", "유가지원금 등에 소비 5년반 연속 증가…물가 감안하면 제자리", "SBS Biz",
      "https://biz.sbs.co.kr/amp/article/20000331131", "news", published="2026-08-27", origin="kostat-hh-2026q2"),
    S("an-future-0827", "2분기 가구소득 4.5% 상승…'고유가 지원금'이 끌어올렸다", "더나은미래(조선일보)",
      "https://futurechosun.com/archives/158901", "news", published="2026-08-27", origin="kostat-hh-2026q2"),
    S("an-nocut-0819", "가계빚 2천조원 돌파…'빚투', 5년만에 '영끌' 역전", "노컷뉴스",
      "https://nocutnews.co.kr/news/6564700", "news", published="2026-08-19", origin="bok-credit-2026q2"),
    S("an-dt-0819", "석 달 새 25.9조원 늘어…19분기 만에 최대폭", "디지털타임스",
      "https://www.dt.co.kr/article/12078929", "news", published="2026-08-19", origin="bok-credit-2026q2"),
    S("an-fn-0616", "韓 GDP 대비 가계부채 88.6% '6년래 최저'", "파이낸셜뉴스(연합뉴스)",
      "https://www.fnnews.com/news/202606161140389240", "news", published="2026-06-16", origin="bis-hh-debt"),
    S("an-kdaily-0915", "GDP 대비 가계부채 비율 2분기 81%대 추산", "중앙일보(미주)",
      "https://www.koreadaily.com/article/20260915181155214", "news", published="2026-09-15", origin="bis-hh-debt"),
    S("an-kdi-ccsi-1027", "2026년 10월 소비자동향조사 결과", "한국은행(KDI 경제교육·정보센터 게시)",
      "https://eiec.kdi.re.kr/policy/materialView.do?num=288557", "government", published="2026-10-27", origin="bok-ccsi-2026-10"),
    S("an-kbmaeil-0720", "가계대출 더 깐깐해진다...은행권 \"주담대 줄이고 신용대출 관리\"", "경북매일",
      "https://kbmaeil.com/article/20260720500556", "news", published="2026-07-20"),
]

CLAIMS = [
    # ── 과거에 관찰된 변화 ──
    C("an-c-avg", "대한상공회의소 분석에 따르면 평균 소비 증가율은 1988~1996년 9.1%에서 외환위기 이후(1997~2002) 4.5%, 카드대란 이후(2003~2007) 3.1%, 금융위기 이후(2008~2019) 2.4%, 코로나19 이후 1.2%로 충격을 겪을 때마다 한 단계씩 낮아졌다. 대한상의는 중장기 요인으로 고령화와 고령층의 소비성향 감소를 먼저 꼽았다.",
      "statistical", "sourced", ["an-newsis-250423"], ["economy", "consumption"], period="1988~2024",
      scope="구간 평균이다. 각 충격이 낮춘 크기와 고령화의 몫을 나눈 것이 아니다."),
    C("an-c-1998", "1998년 민간소비는 11.9% 줄었다(2021년 한국은행 발표 계열). 당시 통계청 분석 자료에는 -13.4%로 적혀 있고, 이듬해 1999년에는 11.5% 늘었다. 같은 시기 실업률은 2.6%에서 6.8%로 올랐다.",
      "statistical", "verified", ["an-kyeonggi-210126", "an-kostat-0304"], ["economy", "consumption"], period="1997~1999",
      scope="국민계정 기준년 개편 때마다 값이 달라진다."),
    C("an-c-2003", "카드 빚이 급증한 뒤 2003년 민간소비는 -0.4%(당시 발표)로, 한국은행의 연초 전망(+5.3%)과 크게 어긋났고 2004년에도 0.3%에 그쳤다. 자영업 취업자는 2003년 4월 1년 전보다 33만 4천 명 줄었다.",
      "statistical", "sourced", ["an-saesayon-card"], ["economy", "consumption"], period="2003~2004",
      scope="통계청 당시 분석 자료에는 2003년 -1.2%, 2004년 -0.5%로 적혀 있어 계열마다 다르다."),
    C("an-c-2003-why", "현대경제연구원은 2003년 이후의 소비 침체를 실질소득 감소만으로는 설명할 수 없고, 가계부채 급증과 신용불량자 증가에 따른 유동성 제약과, 미래 불확실성이 키운 예비적 저축으로 설명하는 것이 타당하다고 봤다.",
      "interpretation", "sourced", ["an-hri-041013"], ["economy", "consumption"], period="2003~2004"),
    C("an-c-2009", "2009년 실질 GDP는 0.2% 성장으로 1998년 이후 가장 낮았다. 현대경제연구원은 2003년 카드 사태 때는 소비가 2년 만에 회복했지만, 2009년 금융위기 이후에는 민간소비 증가율이 GDP 증가율을 계속 밑돌았다고 분석했다.",
      "statistical", "verified", ["an-aju-100126", "an-hri-2014"], ["economy", "consumption"], period="2009~2013"),
    C("an-c-2020", "2020년 민간소비는 5.0% 줄어 1998년 이후 가장 크게 감소했다(2021년 1월 속보). 1분기에는 외출 자제로 음식·숙박·오락 같은 서비스와 승용차·의류 같은 재화 소비가 함께 줄어 전기 대비 6.4% 감소했다.",
      "statistical", "verified", ["an-kyeonggi-210126", "an-seoul-200423"], ["economy", "consumption"], period="2020",
      scope="속보·잠정치는 이후 개정될 수 있다."),
    C("an-c-2023", "한국은행은 2023년 3월, 금리 상승에 따른 원리금 상환 부담과 주택가격 하락(역자산효과)으로 민간소비가 상당폭 둔화될 것으로 봤다. 한국은 가계부채가 크고 변동금리 대출 비중이 높아 금리가 오르면 상환 부담이 빠르게 늘고, 팬데믹 동안 쌓인 초과저축이 완충 역할을 할 것이라고 설명했다.",
      "interpretation", "sourced", ["an-aju-230308"], ["economy", "consumption"], period="2022~2023"),
    C("an-c-2023b", "한국은행은 2023년 8월, 집값 반등이 주택대출 증가를 동반하면 원리금 상환 부담이 커져 집값 상승의 소비 증대 효과가 상쇄될 수 있고, 주택 구매 대기자는 자금 마련을 위해 소비를 줄일 수 있다고 분석했다.",
      "interpretation", "sourced", ["an-newsis-230828"], ["economy", "consumption"], period="2023"),
    C("an-c-2024", "2024년 1~11월 소매판매액 지수는 1년 전보다 2.1% 줄어 2003년(-3.1%) 이후 가장 큰 감소였고, 내구재·준내구재·비내구재 소비가 2년 연속 함께 줄었다(1995년 집계 이후 처음).",
      "statistical", "sourced", ["an-imaeil-250112"], ["economy", "consumption"], period="2023~2024",
      scope="소매판매는 상품 판매이며 서비스 소비는 포함하지 않는다."),
    C("an-c-dsr", "한국은행 분석에 따르면 소득 대비 원리금 상환 비율(DSR)이 1%p 오르면 가구의 연간 소비는 평균 0.37% 줄었다.",
      "statistical", "sourced", ["an-dailian-221207"], ["economy", "consumption"], period="2022 분석",
      scope="평균 효과이며 가구 특성에 따라 다르다(보도 제목 기준)."),
    C("an-c-debtdrag", "한국은행은 2025년 11월, 부동산에서 비롯된 가계부채 누증이 지난 10여 년 동안 소비를 연평균 0.44% 둔화시켰다고 분석했다.",
      "statistical", "sourced", ["an-fn-251128"], ["economy", "consumption"], period="2010년대~2025"),
    C("an-c-debtgrowth", "한국은행 연구에 따르면 GDP 대비 가계신용 비율(3년 누적)이 1%p 오르면 4~5년 시차를 두고 GDP 성장률(3년 누적)이 0.25~0.28%p 낮아진다.",
      "statistical", "sourced", ["an-asiae-260115"], ["economy"], period="연구 기간 미상(기사 기준)"),
    # ── 현재(기준일은 문장마다) ──
    C("an-n-rate", "한국은행은 2026년 상반기 기준금리를 2.50%로 유지하다 7월 2.75%, 8월 3.00%로 올렸고, 10월 22일에는 3.00%로 동결했다. 한은은 수출·투자 호조로 성장세가 높고 물가가 3% 내외의 오름세를 이어가는 가운데 중동 사태 등 불확실성이 커져 금리 인상의 파급 영향을 점검할 필요가 있다고 밝혔다.",
      "fact", "sourced", ["an-kdi-mpc-1022", "an-kbmaeil-261022", "an-sidae-260923"], ["economy"], period="2026.1~2026.10",
      support="기준일 2026-10-22(한국은행 통화정책방향)"),
    C("an-n-gdp", "2026년 3분기 실질 GDP는 전기 대비 1.0%(속보, 10월 27일) 늘었지만 민간소비는 0.2% 줄었다. 한국은행은 7월부터의 증시 조정에 따른 금융서비스 감소와 승용차 제조업체 전면 파업을 특이 요인으로 들며, 이를 빼면 민간소비가 0.4% 늘었을 것으로 추정했다.",
      "statistical", "sourced", ["an-tomato-261027", "an-khan-261027"], ["economy", "consumption"], period="2026년 3분기",
      support="기준일 2026-10-27(한국은행 GDP 속보)"),
    C("an-n-kdi", "KDI는 반도체 호황에 따른 소득 증가 효과가 가계 전반으로 확산하는 흐름이 아직 뚜렷하지 않고 고유가에 따른 가계 부담이 이어져 3분기 민간소비 증가율이 상대적으로 낮았다고 분석했다.",
      "interpretation", "sourced", ["an-yna-kdi-11"], ["economy", "consumption"], period="2026년 3분기"),
    C("an-n-cpi", "2026년 10월 소비자물가는 1년 전보다 2.8%, 근원물가(식료품·에너지 제외)도 2.8% 올랐다. 석유류는 14.9% 올랐고, 정부는 석유 최고가격제가 10월 상승률을 약 0.8%p 낮췄다고 추정했다(없었다면 3.6%).",
      "statistical", "sourced", ["an-korea-cpi-1103", "an-tomato-cpi-1103"], ["economy"], period="2026년 10월",
      support="기준일 2026-11-03(국가데이터처 소비자물가동향)",
      scope="최고가격제 효과는 정부 추산이다."),
    C("an-n-income", "2026년 2분기 가구당 월평균 소득은 529만 5천 원으로 4.5%(실질 1.5%) 늘었지만, 근로소득은 0.8% 증가에 그쳤고 고유가 피해지원금 등으로 이전소득이 20.4% 늘었다. 소비지출은 293만 2천 원으로 3.4% 늘었다. 국가데이터처는 2분기 임금근로자 수가 감소로 돌아서고 임금 상승률도 둔화했다고 설명했다.",
      "statistical", "sourced", ["an-inews-0827", "an-herald-0826", "an-sbs-0827", "an-future-0827"], ["economy", "consumption"], period="2026년 2분기",
      support="기준일 2026-08-27(국가데이터처 가계동향조사)",
      scope="근로소득의 실질 증가율은 공식 발표가 없어 언론이 명목 증가율과 물가로 추정한 값만 있다."),
    C("an-n-debt", "2026년 2분기 말 가계신용 잔액은 2,019조 8천억 원으로 통계 공표(2002년) 이후 처음 2천조 원을 넘었다. 한 분기에 25조 9천억 원이 늘어 2021년 3분기 이후 증가 폭이 가장 컸고, 주택담보대출과 함께 주식 투자 수요로 신용대출·증권사 신용공여가 늘었다.",
      "statistical", "sourced", ["an-nocut-0819", "an-dt-0819"], ["economy"], period="2026년 2분기",
      support="기준일 2026-08-19(한국은행 가계신용 잠정)"),
    C("an-n-debtratio", "국제결제은행(BIS) 기준 GDP 대비 가계부채 비율은 2021년 3분기 99.1%로 정점을 찍은 뒤 2025년 말 88.6%, 2026년 1분기 85.1%로 낮아졌다. 부채 잔액이 줄어서가 아니라 명목 GDP가 빠르게 늘었기 때문이다(1분기 명목 GDP 증가율 17.1%).",
      "statistical", "sourced", ["an-fn-0616", "an-kdaily-0915"], ["economy"], period="2021~2026년 1분기",
      support="기준일 2026-09-15(BIS 1분기 통계 보도)",
      scope="2분기 81%대는 언론 추산이며 공식 통계가 아니다."),
    C("an-n-ccsi", "2026년 10월 소비자심리지수는 105.4로 한 달 전보다 1.2p 낮아졌지만 장기평균(100)보다는 높았다. 현재생활형편은 93, 가계수입전망 101, 소비지출전망 109였고, 향후 1년 기대인플레이션은 2.7%였다.",
      "statistical", "sourced", ["an-kdi-ccsi-1027"], ["economy", "consumption"], period="2026년 10월",
      support="기준일 2026-10-27(한국은행 소비자동향조사)"),
    C("an-n-lending", "한국은행 대출행태서베이에서 국내 은행의 2026년 3분기 대출태도 종합지수는 -7로, 1분기(-1)·2분기(-2)보다 대출 기준이 더 강화될 것으로 나타났다.",
      "statistical", "sourced", ["an-kbmaeil-0720"], ["economy"], period="2026년 3분기 전망",
      support="기준일 2026-07-20"),
]


# 사이트 종합(synthesis): 근거 주장 id를 함께 단다. 사실 주장이 아니라 '사이트가 자료를 묶은 해석'으로 표시된다.
def Y(text, ids):
    return {"text": text, "claimIds": list(ids), "kind": "synthesis"}


ANALYSES = [
    {
        "id": "an-consumption",
        "question": "가계의 소비 여력은 어떤 조건에서 줄고 늘었으며, 지금 소비를 판단하려면 무엇을 봐야 하나?",
        "short": "가계 소비 여력",
        "asOf": "2026-11-03",
        "status": "complete",
        "scope": {
            "target": "한국 가계의 실질 소비(국민계정 민간소비, 소매판매, 가계동향조사)",
            "period": "1988년~2026년 3분기. 같은 기준의 소비 통계를 연결한 1988년부터 본다. 1960~80년대 소비 구조는 '소비·쇼핑'과 '가계 소비 비중' 지표에서 따로 본다.",
            "variable": "추적 변수: 실질 소비 증가율. 설명 변수: 실질 소득(고용·임금·물가), 이자 부담(금리×부채), 자산 가격, 심리·불확실성, 정부 이전소득, 인구 구조.",
            "notIncluded": "기업 투자·수출은 소비에 영향을 주는 범위에서만 다룬다. 소득 계층별 차이는 일부만 확인했다.",
        },
        "findings": [
            Y("한국의 가계 소비는 큰 충격을 겪을 때마다 크게 줄었고, 회복 뒤의 평균 증가율은 매번 한 단계 낮아졌다(9.1% → 4.5% → 3.1% → 2.4% → 1.2%).", ["an-c-avg", "an-c-1998", "an-c-2003", "an-c-2020"]),
            Y("충격이 소비로 들어온 길은 매번 달랐다. 1998년은 실업과 소득, 2003년은 카드 빚(유동성 제약)과 불안, 2020년은 이동 제한, 2022~24년은 물가와 이자 부담이었다.", ["an-c-1998", "an-c-2003-why", "an-c-2020", "an-c-2023"]),
            Y("2010년대 이후에는 가계부채가 소비를 오래 누르는 조건이 되었다. 금리가 오르면 상환 부담을 통해 소비가 줄고, 집값이 올라도 대출이 함께 늘면 소비 증대 효과가 상쇄된다는 한국은행 분석이 있다.", ["an-c-dsr", "an-c-debtdrag", "an-c-2023b"]),
        ],
        "whyNow": Y("2026년에는 반도체 수출로 성장률이 높지만(3분기 전기 대비 1.0%) 민간소비는 줄었다. 성장과 가계 소비가 따로 움직이는 지금, 소비를 판단하려면 GDP가 아니라 소득이 가계로 퍼지는지와 이자 부담을 봐야 한다.", ["an-n-gdp", "an-n-kdi", "an-n-rate"]),
        # 전달 과정(관계도): 노드와 연결. 연결마다 성격·근거.
        "mechanism": {
            "nodes": [
                {"id": "shock", "label": "바깥·안의 충격", "sub": "외환·유가·감염병·금리"},
                {"id": "jobs", "label": "고용·임금", "sub": "근로소득"},
                {"id": "prices", "label": "물가", "sub": "실질 구매력"},
                {"id": "transfer", "label": "정부 이전소득", "sub": "지원금·연금"},
                {"id": "debt", "label": "이자·원리금 부담", "sub": "금리 × 부채"},
                {"id": "assets", "label": "자산 가격", "sub": "주식·주택"},
                {"id": "mood", "label": "심리·불확실성", "sub": "예비적 저축"},
                {"id": "aging", "label": "인구 구조", "sub": "고령화·소비성향"},
                {"id": "cons", "label": "가계 소비", "sub": "재화·서비스"},
            ],
            "edges": [
                {"from": "shock", "to": "jobs", "kind": "causal", "note": "1998년 외환위기 때 실업률이 2.6%에서 6.8%로 올랐다.", "claimIds": ["an-c-1998"]},
                {"from": "jobs", "to": "cons", "kind": "causal", "note": "소득이 줄면 소비가 준다. 1998년 소비 -11.9%.", "claimIds": ["an-c-1998"]},
                {"from": "shock", "to": "prices", "kind": "causal", "note": "에너지 가격 급등이 물가로 번진다(2022년 6.3%, 2026년 석유류 14.9%).", "claimIds": ["c20-kr-cpi", "an-n-cpi"]},
                {"from": "prices", "to": "cons", "kind": "condition", "note": "물가가 소득보다 빨리 오르면 실질 구매력이 준다.", "claimIds": ["an-n-income", "an-n-kdi"]},
                {"from": "debt", "to": "cons", "kind": "causal", "note": "DSR 1%p 상승 → 연간 소비 평균 0.37% 감소(한은).", "claimIds": ["an-c-dsr", "an-c-2023"]},
                {"from": "assets", "to": "debt", "kind": "condition", "note": "집값 반등이 대출 증가를 동반하면 상환 부담이 커진다.", "claimIds": ["an-c-2023b"]},
                {"from": "assets", "to": "cons", "kind": "interpretation", "note": "주가 조정이 금융서비스 소비를 줄인 사례(2026년 3분기). 부의 효과의 크기는 확인하지 않았다.", "claimIds": ["an-n-gdp"]},
                {"from": "mood", "to": "cons", "kind": "interpretation", "note": "2003년 소비 침체는 불확실성이 키운 예비적 저축으로 설명된다(연구 해석).", "claimIds": ["an-c-2003-why"]},
                {"from": "transfer", "to": "cons", "kind": "correlation", "note": "2026년 2분기 이전소득 +20.4%와 소비지출 +3.4%가 함께 나타났다. 지원금의 소비 효과 크기는 확인하지 않았다.", "claimIds": ["an-n-income"]},
                {"from": "aging", "to": "cons", "kind": "interpretation", "note": "대한상의는 고령화와 고령층 소비성향 감소를 장기 부진의 첫째 요인으로 꼽는다.", "claimIds": ["an-c-avg"]},
            ],
        },
        # 과거 국면 여러 개를 같은 항목으로 비교
        "episodes": [
            {"id": "e1998", "label": "1998 외환위기", "years": "1997~1999"},
            {"id": "e2003", "label": "2003 카드대란", "years": "2003~2004"},
            {"id": "e2009", "label": "2009 금융위기", "years": "2008~2009"},
            {"id": "e2020", "label": "2020 코로나19", "years": "2020~2021"},
            {"id": "e2023", "label": "2022~24 물가·금리", "years": "2022~2024"},
            {"id": "now", "label": "지금(2026)", "years": "2026년 1~3분기", "current": True},
        ],
        "rows": [
            {"item": "충격의 원인", "cells": {
                "e1998": ["외화 유동성 위기·기업 도산(국내 금융)", ["c90-kr-imf", "c97-fx"]],
                "e2003": ["카드 빚 급증과 부실(국내 가계 신용)", ["c00-card", "c00-card-why"]],
                "e2009": ["미국발 금융위기(바깥)", ["c00-lehman"]],
                "e2020": ["감염병과 이동 제한", ["c2020-first"]],
                "e2023": ["에너지 가격 급등과 금리 인상", ["c20-kr-cpi", "c20-kr-rate"]],
                "now": ["중동 사태 유가 상승, 금리 재인상", ["an-n-cpi", "an-n-rate"]]}},
            {"item": "소비의 변화", "cells": {
                "e1998": ["1998년 -11.9%, 1999년 +11.5% 반등", ["an-c-1998"]],
                "e2003": ["2003년 -0.4%, 2004년 0.3%", ["an-c-2003"]],
                "e2009": ["성장률 0.2%, 이후 소비가 GDP를 밑돎", ["an-c-2009"]],
                "e2020": ["2020년 -5.0%", ["an-c-2020"]],
                "e2023": ["2024년 소매판매 -2.1%(2003년 이후 최대 감소)", ["an-c-2024"]],
                "now": ["3분기 -0.2%(전기 대비, 특이 요인 제외 시 +0.4% 추정)", ["an-n-gdp"]]}},
            {"item": "소득과 고용", "cells": {
                "e1998": ["실업률 2.6% → 6.8%", ["an-c-1998"]],
                "e2003": ["자영업 취업자 급감(4월 -33만 4천 명)", ["an-c-2003"]],
                "e2009": ["고용 충격이 1998년보다 작음(일자리 나누기)", ["c08-jobs-share"]],
                "e2020": ["", []],
                "e2023": ["", []],
                "now": ["근로소득 +0.8%, 이전소득 +20.4%(2분기)", ["an-n-income"]]}},
            {"item": "물가", "cells": {
                "e1998": ["", []],
                "e2003": ["", []],
                "e2009": ["", []],
                "e2020": ["", []],
                "e2023": ["2022년 7월 6.3%(24년 만의 최고)", ["c20-kr-cpi"]],
                "now": ["10월 2.8%, 근원 2.8%(최고가격제로 약 0.8%p 낮춤)", ["an-n-cpi"]]}},
            {"item": "금리·신용 여건", "cells": {
                "e1998": ["", []],
                "e2003": ["카드 발급·현금서비스 한도 폐지 뒤 급격한 축소", ["c00-card-why"]],
                "e2009": ["기준금리 5.25% → 2.00%", ["c08-rate"]],
                "e2020": ["기준금리 0.5%까지 인하(빅컷)", ["c2020-bigcut"]],
                "e2023": ["일곱 차례 인상, 3.50%", ["c20-kr-rate"]],
                "now": ["2.50% → 3.00%(7·8월), 대출 기준 강화", ["an-n-rate", "an-n-lending"]]}},
            {"item": "가계부채", "cells": {
                "e1998": ["", []],
                "e2003": ["현금서비스·카드론 10조 → 60조, 채무불이행자 372만 명", ["c00-card"]],
                "e2009": ["", []],
                "e2020": ["", []],
                "e2023": ["GDP 대비 99.1%(2021년 3분기 정점)", ["an-n-debtratio"]],
                "now": ["2,019조 8천억 원(사상 최대), GDP 대비 85.1%(1분기)", ["an-n-debt", "an-n-debtratio"]]}},
            {"item": "정책 대응", "cells": {
                "e1998": ["IMF 프로그램, 구조조정", ["c90-kr-imf"]],
                "e2003": ["카드 사용 장려(소득공제·복권) 뒤 규제", ["er-shop-cardpolicy", "c00-card-why"]],
                "e2009": ["금리 인하, 28조 원대 슈퍼 추경", ["c08-rate", "c08-supplement"]],
                "e2020": ["빅컷, 전 국민 재난지원금", ["c2020-bigcut", "c2020-relief"]],
                "e2023": ["금리 인상(물가 대응)", ["c20-kr-rate"]],
                "now": ["고유가 피해지원금, 석유 최고가격제, 금리 인상", ["an-n-income", "an-n-cpi", "an-n-rate"]]}},
        ],
        "same": [
            Y("에너지 가격 급등 → 물가 → 실질 구매력 감소라는 경로는 2022~24년과 같다.", ["c20-kr-cpi", "an-n-cpi", "an-n-kdi"]),
            Y("가계부채가 많고 금리가 오를 때 상환 부담이 소비를 누르는 조건은 2022~24년과 같다. 잔액은 오히려 더 많다(2천조 원 돌파).", ["an-c-dsr", "an-c-2023", "an-n-debt", "an-n-rate"]),
            Y("집값 상승이 대출 증가를 동반하는 모습은 2023년 한국은행이 소비 제약 요인으로 짚은 상황과 같다.", ["an-c-2023b", "an-n-debt"]),
        ],
        "different": [
            Y("과거 소비 급감 국면(1998·2003·2020)에는 성장 자체가 꺾였지만, 지금은 반도체 수출로 성장률이 높다. 소비 부진이 '경기 침체'가 아니라 '소득이 가계로 퍼지지 않는 문제'일 수 있다.", ["an-n-gdp", "an-n-kdi"]),
            Y("GDP 대비 가계부채 비율은 낮아지고 있지만, 이는 부채가 줄어서가 아니라 명목 GDP가 급증해서다. 가계가 실제로 느끼는 부담은 소득 대비 원리금으로 봐야 한다.", ["an-n-debtratio", "an-n-income"]),
            Y("이번 소득 증가의 큰 몫이 정부 이전소득(지원금)이다. 지원금은 끝나는 시점이 있어, 근로소득으로 이어지는 2020년 이후 회복과 성격이 다르다.", ["an-n-income"]),
            Y("1998년(실업 급증)과 달리 지금은 고용 충격의 증거를 확보하지 못했다. 다만 2분기 임금근로자 수가 감소로 돌아섰다는 정부 설명이 있다(가계동향 브리핑 보도).", ["an-n-income"]),
            Y("인구 고령화가 진행된 정도는 과거 어느 국면보다 크다. 대한상의는 이를 장기 소비 부진의 첫째 요인으로 꼽는다.", ["an-c-avg", "c20-pop"]),
        ],
        "scenarios": [
            {"id": "s-spread", "name": "소득 확산형",
             "conditions": "반도체·수출 호황이 임금(성과급·임금 인상)과 고용으로 번지고, 물가가 지금보다 낮아지며, 금리 인상이 멈춘다.",
             "path": "근로소득이 물가보다 빨리 늘어남 → 가계수입·소비지출 전망 개선 → 미뤄 둔 내구재·서비스 소비 회복.",
             "affected": "외식·여행·문화 서비스, 승용차·가전 같은 내구재, 대면 서비스 자영업과 그 일자리.",
             "timing": "임금은 연 단위 협상·성과급 지급 주기로 반영돼 시차가 있다. 얼마나 걸릴지는 자료로 확인하지 못했다.",
             "breaks": "근로소득 증가율이 계속 물가를 밑돌거나, 임금근로자 수 감소가 이어지면 이 경로는 성립하지 않는다.",
             "basis": ["an-n-kdi", "an-n-income", "an-n-ccsi"]},
            {"id": "s-debt", "name": "이자 부담 누적형",
             "conditions": "물가·집값 때문에 금리 인상이 이어지고, 변동금리 대출이 많은 상태에서 대출 금리가 오른다.",
             "path": "상환 부담(DSR) 상승 → 대출이 많은 가구의 소비 감소 → 집을 사려는 가구는 저축을 늘림 → 소비 회복이 늦어짐.",
             "affected": "대출 비중이 큰 30~40대와 저소득·자영업 가구, 내구재·준내구재 판매, 소매·음식점.",
             "timing": "변동금리 대출은 금리 변경 주기에 따라 몇 달 안에 반영된다. 소비 둔화가 얼마나 이어질지는 확인하지 못했다.",
             "breaks": "금리 인상이 멈추거나 내리고, 소득 증가가 이자 증가를 앞서면 약해진다.",
             "basis": ["an-c-dsr", "an-c-2023", "an-c-2023b", "an-n-rate", "an-n-debt"]},
            {"id": "s-asset", "name": "자산·지원금 의존형",
             "conditions": "근로소득은 정체한 채 주가·집값 상승과 정부 지원금이 소비를 받친다.",
             "path": "자산 보유 가구와 지원금 수령 가구의 소비는 유지 → 평균 소비는 버티지만 가구 사이 격차가 커짐 → 증시 조정이나 지원금 종료 때 소비가 급히 줄 수 있음(2026년 3분기 금융서비스 감소처럼).",
             "affected": "자산 시장과 연결된 금융서비스, 고가 소비재, 지원금이 쓰이는 생활 소비.",
             "timing": "지원금 종료 시점과 자산 가격 변동에 따라 달라진다.",
             "breaks": "근로소득 증가가 이전소득을 대신하게 되면 이 의존은 줄어든다.",
             "basis": ["an-n-income", "an-n-gdp", "an-n-debt"]},
            {"id": "s-shock", "name": "외부 충격 재발형",
             "conditions": "중동 사태 등으로 유가가 다시 크게 오르고, 가격 통제(최고가격제)를 계속 유지하기 어려워진다.",
             "path": "에너지 가격 → 소비자물가 → 실질 구매력 감소. 1973년·2022년에 같은 경로가 관찰되었다.",
             "affected": "교통·난방 등 에너지 의존 지출이 큰 가구, 운송·음식점 등 원가에 에너지 비중이 큰 업종.",
             "timing": "유가는 몇 달 안에 물가에 반영된다(과거 국면 기준). 정확한 시차는 확인하지 않았다.",
             "breaks": "유가가 안정되거나, 다른 품목 물가가 내려 전체 물가 상승을 상쇄하면 약해진다.",
             "basis": ["an-n-cpi", "c20-kr-cpi", "c70-kr-cpi"]},
        ],
        "watch": [
            {"name": "근로소득·실질소득(가계동향조사)", "source": "국가데이터처, 분기", "supports": "근로소득이 물가보다 빨리 늘면 '소득 확산형'", "weakens": "이전소득을 빼면 소득이 줄면 '자산·지원금 의존형'", "claimIds": ["an-n-income"]},
            {"name": "민간소비(GDP 속보)·소매판매액", "source": "한국은행 분기 / 국가데이터처 산업활동동향 월", "supports": "특이 요인이 사라진 뒤 소비가 늘면 3분기 감소는 일시적", "weakens": "특이 요인 없이도 감소가 이어지면 구조적 부진", "claimIds": ["an-n-gdp", "an-c-2024"]},
            {"name": "소비자물가(근원 포함)", "source": "국가데이터처, 월", "supports": "근원물가가 내려가면 실질 구매력 회복", "weakens": "최고가격제 효과를 빼고도 3%를 넘으면 '외부 충격 재발형'", "claimIds": ["an-n-cpi"]},
            {"name": "기준금리·대출금리·대출태도", "source": "한국은행 금통위(연 8회), 은행연합회 코픽스, 대출행태서베이", "supports": "인상이 이어지면 '이자 부담 누적형'", "weakens": "동결·인하로 바뀌면 그 경로가 약해짐", "claimIds": ["an-n-rate", "an-n-lending"]},
            {"name": "가계신용 증가 폭과 차주별 상환 부담", "source": "한국은행 가계신용(분기), 차주별 가계부채 통계", "supports": "대출이 빠르게 늘면 상환 부담 증가", "weakens": "증가 폭이 줄고 소득이 늘면 부담 완화", "claimIds": ["an-n-debt"]},
            {"name": "소비자심리 세부(가계수입전망·소비지출전망)", "source": "한국은행 소비자동향조사, 월", "supports": "가계수입전망이 오르면 소득 확산 기대", "weakens": "종합지수만 높고 현재생활형편이 낮으면 심리와 실제 형편이 따로 감", "claimIds": ["an-n-ccsi"]},
        ],
        "revise": [
            "근로소득이 물가보다 빨리 늘고 가계수입전망이 오르는데도 민간소비가 계속 줄면, '소득이 열쇠'라는 이 분석의 설명이 약해진다. 고령화·예비적 저축 같은 구조 요인의 몫을 다시 봐야 한다.",
            "금리가 오르는데도 대출이 많은 가구의 소비가 줄지 않으면, 상환 부담 경로(DSR)의 힘이 과거보다 약해진 것이다(고정금리 비중 변화 등 확인 필요).",
            "지원금이 끝난 뒤에도 소비가 유지되면 '자산·지원금 의존형'의 위험은 과장된 것이다.",
        ],
        "alternatives": [
            "소비 부진을 경기 순환(일시적)으로 보는 설명과, 고령화·가계부채 같은 구조 요인으로 보는 설명이 함께 있다.",
            "2003년 소비 침체를 유동성 제약·예비적 저축으로 보는 연구가 있지만, 실질소득 감소의 몫을 더 크게 보는 시각도 있다.",
        ],
        "limits": [
            "민간소비 연간 값은 국민계정 기준년이 바뀔 때마다 달라진다(1998년 -11.9%/-13.4%, 2003년 -0.4%/-1.2%). 이 사이트는 한국은행 원자료 시계열을 직접 내려받지 못해 공표 값을 인용했다.",
            "과거 국면 비교는 결과를 아는 상태에서 정리한 것이다. 당시 이 지표들로 그 결과를 미리 판단할 수 있었는지는 검증하지 않았다(2003년 한은 전망이 크게 빗나간 사례가 있다).",
            "인용한 효과 크기(DSR 1%p → 소비 0.37% 등)는 각 연구의 결과이며, 이 사이트가 다시 계산한 것이 아니다.",
            "소득 계층별·연령별 소비 변화는 일부 보도만 확인했다.",
            "2026년 수치는 속보·잠정치이며 개정될 수 있다.",
        ],
        "flows": ["flow-economy", "flow-shop", "flow-family", "flow-city"],
        "indicators": ["baserate-kr", "cpi-kr", "unemp-kr"],
        "chartNotes": [
            {"year": 1998, "label": "외환위기"},
            {"year": 2003, "label": "카드대란"},
            {"year": 2009, "label": "금융위기"},
            {"year": 2020, "label": "코로나19"},
            {"year": 2023, "label": "고금리"},
        ],
    },
]


def validate(claims):
    cids = {c["id"] for c in claims}
    for a in ANALYSES:
        def chk(ids, where):
            for i in ids:
                if i not in cids:
                    raise SystemExit(f"{a['id']} {where}: 없는 주장 {i}")
        for y in a["findings"] + a["same"] + a["different"] + [a["whyNow"]]:
            chk(y["claimIds"], "종합")
            if not y["claimIds"]:
                raise SystemExit(f"{a['id']}: 근거 없는 종합 문장 {y['text'][:20]}")
        for e in a["mechanism"]["edges"]:
            chk(e["claimIds"], "관계도")
        for r in a["rows"]:
            for k, (txt, ids) in r["cells"].items():
                chk(ids, f"비교표 {r['item']}")
                if txt and not ids:
                    raise SystemExit(f"{a['id']}: 근거 없는 비교 칸 {r['item']}/{k}")
        for s in a["scenarios"]:
            chk(s["basis"], "시나리오")
        for w in a["watch"]:
            chk(w["claimIds"], "지표")
    return ANALYSES
