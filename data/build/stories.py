"""흐름 이야기 — 모든 흐름을 같은 11개 질문으로 읽는다.

연표(무슨 일이 언제)가 아니라 '선택 기준이 어떻게 바뀌었나'를 쓴다.
문장마다 층위를 붙인다.
    fact       확인된 사실(근거 문장 필수)
    source     출처의 해석(기자·연구자·업계의 설명, 근거 문장 필수)
    inference  AI 종합 추론(이 사이트의 설명 — 출처의 주장이 아님). 바탕이 된 근거 문장이 있으면 붙인다.
    hypothesis 탐색·전망 가설(확인이 필요)
근거를 찾지 못한 연결은 비워 두지 않고 AI 추론으로 채우되, 그렇다고 표시한다. 수치·날짜·인용은 근거 문장에 있는 것만 쓴다.

STEP_NOTES는 단계 하나를 '그때 분위기 → 이어진 변화(사회·산업·소비·문화)'로 풀고, 다른 흐름의 단계로 바로 넘어가는 연결을 단다.
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


def C(id, text, ctype, sources, domains, period=None, scope=None):
    d = {"id": id, "text": text, "claimType": ctype, "status": "sourced", "sourceIds": sources,
         "domains": domains, "countries": ["KR"], "aiSynthesized": False}
    if period:
        d["period"] = period
    if scope:
        d["scope"] = scope
    return d


def L(layer, text, ids=()):
    assert layer in ("fact", "source", "inference", "hypothesis"), layer
    return {"layer": layer, "text": text, "ids": list(ids)}


SOURCES = [
    # 1987년 이후
    S("sx-tf-labor", "Labor movements in South Korea after 1987 (book chapter abstract)", "Routledge(Taylor & Francis)",
      "https://www.taylorfrancis.com/books/9780203883921/chapters/10.4324/9780203883921-9", "academic"),
    S("sx-loc-korea", "South Korea: A Country Study — Labor", "미국 의회도서관 Country Studies(재게시)",
      "https://countrystudies.us/south-korea/55.htm", "government", published="1990"),
    S("sx-saesayon", "90년대 한국경제는 어떻게 불평등을 줄였을까", "새로운사회를여는연구원",
      "https://saesayon.org/AttachFiles/1332817159594_1.pdf", "report", published="2012-03-27"),
    S("sx-jak-press", "1987년 찾아온 언론자유 시대… 무한경쟁 속 '기업으로서의 생존경쟁'", "기자협회보",
      "https://www.journalist.or.kr/m/m_article.html?no=48025", "news", published="2020-07-29", note="1990년 7월 6일자 기자협회보 기사 재조명"),
    S("sx-jak-hani", "한겨레 창간 20돌…참언론 실천 '한길'", "기자협회보",
      "https://www.journalist.or.kr/m/m_article.html?no=17500", "news", published="2008-05"),
    S("sx-kdi-cars", "자동차 500만대 돌파계기 자동차증가 및 이용률 감소대책", "KDI 경제정보센터(정부 자료)",
      "https://eiec.kdi.re.kr/epic_txt/1992/R9210086.HWP", "government", published="1992"),
    S("sx-seoul-rentcar", "렌터카 작년 매출액 36% 늘어(운수업 통계)", "서울신문",
      "https://www.seoul.co.kr/news/1990/09/11/19900911006005", "news", published="1990-09-11"),
    S("sx-seoul-901209", "고용감소·투자위축 등 부작용 불러/기획원 경제백서", "서울신문",
      "https://www.seoul.co.kr/news/1990/12/09/19901209006001", "news", published="1990-12-09"),
    # 이미지 SNS
    S("sx-asiae-191224", "'인스타에 올려야지' SNS에 갇힌 청춘들", "아시아경제",
      "https://view.asiae.co.kr/article/2019122413533152144", "news", published="2019-12-24"),
    S("sx-aju-190815", "'인스타그래머블'한 장소를 찾는 사람들", "아주경제",
      "https://www.ajunews.com/view/20190815121706002", "news", published="2019-08-15"),
    S("sx-tf-insta", "요식업계 '인스타그래머블' 열풍", "더팩트",
      "https://news.tf.co.kr/read/ogmeta/1740935.htm", "news"),
    S("sx-inews-yellow", "[르포] '#바나나맛우유' 인스타 성지된 옐로우카페 가보니", "아이뉴스24",
      "https://www.inews24.com/view/1182252", "news"),
    S("sx-sidae-220920", "MZ세대가 감성카페에 가는 이유", "머니S(시대 재게시)",
      "https://www.sidae.com/article/2022092023550453184", "news", published="2022-09-20"),
    S("sx-sidae-240424", "스몰 럭셔리 열풍(연구위원 분석)", "머니S(시대 재게시)",
      "https://www.sidae.com/article/2024042416112122937", "news", published="2024-04-24"),
    S("sx-dailian-191201", "국내 명품시장 2년 새 3.5배↑…20대 명품 구매 7.5배(롯데멤버스 트렌드Y)", "데일리안",
      "https://www.dailian.co.kr/news/view/847968/", "news", published="2019-12-01"),
    S("sx-ks-fatigue", "SNS 피로감 유발요인과 지속·중단 의향(학술 논문)", "한국콘텐츠학회 등(KoreaScience)",
      "https://koreascience.kr/article/JAKO201819352299454.pdf", "academic", published="2018"),
    S("sx-qletter-locket", "Z세대가 열광하는 폐쇄형 SNS(로켓 위젯)", "큐레터(아이보스)",
      "https://www.i-boss.co.kr/ab-qletter-761884", "news"),
    S("sx-zdnet-cy", "싸이월드 10년(서비스 히스토리)", "지디넷코리아",
      "https://zdnet.co.kr/view/?no=20100401025113", "news", published="2010-04-01"),
    S("sx-segye-cybgm", "봉인 해제되는 그때 그 시절…'추억송'(싸이월드 BGM)", "세계일보",
      "https://www.segye.com/newsView/20210305512389", "news", published="2021-03-05"),
    S("sx-etnews-cy", "싸이월드는 '자기'에 초점을 맞춘 서비스였다", "전자신문",
      "https://www.etnews.com/201303120160", "news", published="2013-03-12"),
    # 문신
    S("sx-fn-221017", "대중화된 타투…'혐오감 든다' vs '표현의 자유'", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202210171615259109", "news", published="2022-10-17"),
    S("sx-fn-221018", "타투 인식 관련 조사(엠브레인 2018) 인용 보도", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202210181816574349", "news", published="2022-10-18"),
    S("sx-sgsg-211112", "[생글기자] 타투 합법화(한국갤럽 2021 조사 인용)", "한국경제 생글생글",
      "https://sgsg.hankyung.com/article/2021111243931", "news", published="2021-11-12", origin="한국갤럽"),
    S("sx-tenasia-220515", "타투의 부정적 이미지, 퇴폐미로 변화", "텐아시아",
      "https://www.tenasia.co.kr/article/2022051570904", "news", published="2022-05-15"),
    S("sx-sgsg-220929", "'한국 타투이스트 실력, 세계적으로 인정받고 있죠'", "한국경제 생글생글",
      "https://sgsg.hankyung.com/article/202209294206m", "news", published="2022-09-29"),
    S("sx-kt-250927", "Banned at home, Korean tattoo artists thrive abroad", "The Korea Times",
      "https://www.koreatimes.co.kr/amp/southkorea/society/20250927/banned-at-home-korean-tattoo-artists-thrive-abroad", "news", published="2025-09-27"),
    S("sx-vogue-taeyeon", "태연이 새긴 타투의 의미는?", "보그 코리아",
      "https://www.vogue.co.kr/?p=296581", "news"),
    S("sx-mc-remove", "타투 제거 콘텐츠가 늘어나는 이유", "마리끌레르 코리아",
      "https://www.marieclairekorea.com/?p=562240", "news"),
    # 음악
    S("sx-nocut-lp", "[파고들기] '뉴트로' 열풍에 LP 판매량 급상승…韓 MZ '우리는 소장한다'", "노컷뉴스",
      "https://nocutnews.co.kr/news/5908075", "news", published="2023"),
    S("sx-dailian-201218", "[초점] 스트리밍 시대의 'LP 시장 성장'이 의미하는 것", "데일리안",
      "https://m.dailian.co.kr/news/view/947616", "news", published="2020-12-18"),
    S("sx-newsis-251023", "韓 바이닐 시장의 현재와 미래…'제14회 서울 레코드 페어'", "뉴시스",
      "https://www.newsis.com/view/NISX20251023_0003373419", "news", published="2025-10-23"),
    S("sx-kyeongin-lp", "롱 플레이의 귀환(IFPI 2023 음악 리포트 인용)", "경인일보",
      "https://www.kyeongin.com/article/1712854", "news", published="2024", origin="IFPI"),
    S("sx-tf-album", "[앨범의 가치①] 듣지도 않는데…1억 장 팔리는 CD의 역설(한터차트 인용)", "더팩트",
      "https://news.tf.co.kr/read/ogmeta/2377607.htm", "news"),
    S("sx-dailian-album26", "K팝 앨범 시장 반등과 달라진 포맷(써클차트 인용)", "데일리안",
      "https://m.dailian.co.kr/news/view/1707458/", "news", published="2026", origin="써클차트"),
    S("sx-toss-fandustry", "CD를 듣지 않는 시대에 여전히 음반이 중요한 이유", "토스피드",
      "https://toss.im/tossfeed/article/fandustry-02", "news", published="2024"),
    S("sx-daum-240509", "유튜브 뮤직, 2023년 12월 멜론 잡고 1위", "세계일보(다음 재게시)",
      "https://v.daum.net/v/20240509202048747", "news", published="2024-05-09", origin="모바일인덱스"),
    S("sx-newsis-240115", "멜론 MAU 769만→624만, 유튜브뮤직 첫 1위(모바일인덱스)", "뉴시스",
      "https://www.newsis.com/view/NISX20240115_0002592733", "news", published="2024-01-15", origin="모바일인덱스"),
    S("sx-hk-260728", "음원 스트리밍 앱 이용자(와이즈앱·리테일)", "한국경제",
      "https://www.hankyung.com/article/2026072812091", "news", published="2026-07-28", origin="와이즈앱·리테일"),
    S("sx-etoday-kocca", "결국 해 넘긴 유튜브뮤직 제재…몸살 깊어가는 토종 음원앱(콘진원 2024 음악 이용자 조사)", "이투데이",
      "https://www.etoday.co.kr/news/view/2434338", "news", origin="한국콘텐츠진흥원"),
]

P = ["society", "economy"]
X = ["culture", "consumption"]
CLAIMS = [
    # ── 1987년 이후의 파급
    C("sx-wage8889", "한 연구서는 권위주의 정권이 무너진 1987년 이후 노조 조직률·노조 수·조합원 수가 1988~89년 폭발적으로 늘었고(1989년 조직률 18.6%), 명목임금 인상률이 1988년 15.5%, 1989년 21.1%였다고 정리한다.",
      "fact", ["sx-tf-labor"], P, period="1987~1989"),
    C("sx-wage-loc", "미국 의회도서관 국가 연구는 1988년 제조업 임금이 20%, 1989년 25% 올랐고 1989년 전체 경제의 임금이 18.7% 올랐다고 적었다. 1985~88년 가구 평균소득은 연평균 14.8% 늘었다.",
      "fact", ["sx-loc-korea"], P, period="1985~1989"),
    C("sx-golden", "한 연구원 보고서는 1987년 3저 호황과 6월 항쟁·노동자 대투쟁이 겹치며 이후 10년 동안 '노조 활성화 → 취업자 증가 → 임금 상승'의 선순환이 이어졌고, 소비와 투자가 활기를 띠며 불평등이 줄었다고 해석한다.",
      "interpretation", ["sx-saesayon"], P, period="1987~1996"),
    C("sx-press", "1987년 언론기본법 폐지 뒤 서울에서 발행되는 종합일간지는 1987년 6개에서 1989년 10개로, 지역지는 10개에서 30개로 늘었다(기자협회보 1990년 분석).",
      "fact", ["sx-jak-press"], ["society", "culture"], period="1987~1989"),
    C("sx-hani", "6월 항쟁 뒤 해직 기자들이 국민 모금으로 창간 자본금 50억 원을 100여 일 만에 모아 1988년 5월 15일 한겨레신문을 창간했다.",
      "fact", ["sx-jak-hani"], ["society", "culture"], period="1987~1988"),
    C("sx-cars", "전국 자동차 등록 대수는 1985년 5월 100만 대, 1988년 12월 200만 대, 1990년 6월 300만 대, 1992년 10월 500만 대를 넘었다. 정부 자료는 증가 원인으로 국민소득 수준의 향상을 먼저 들었다.",
      "fact", ["sx-kdi-cars"], ["consumption", "society"], period="1985~1992"),
    C("sx-rentcar", "1989년 차량임대업(렌터카) 매출은 36.8% 늘어 운수업 전체(10%)를 크게 앞질렀고, 신문은 이를 '마이카시대'의 호황 업종으로 소개했다.",
      "fact", ["sx-seoul-rentcar"], ["consumption"], period="1989"),
    C("sx-whitepaper90", "1990년 경제기획원 경제백서는 생산성을 웃도는 높은 임금 인상이 고용 감소와 물가 상승 같은 부정적 효과를 내기 시작했다고 분석했다(실업자 2만여 명 증가).",
      "interpretation", ["sx-seoul-901209"], P, period="1990"),
    # ── 이미지 SNS
    C("sx-sns-2016", "대학내일 20대연구소의 2016년 조사(20대 410명)에서 25.6%가 SNS로 관심받는 것을 즐긴다고 답했고, 하루 평균 1.46회 '인증'을 했다. 한 대학생은 음식 맛보다 식당·카페 분위기와 디저트 모양을 더 따진다고 말했다.",
      "fact", ["sx-asiae-191224"], X, period="2016~2019"),
    C("sx-sns-why", "2019년 보도는 SNS에서 남보다 주목받으려면 시선을 끄는 사진이 필요해, 사람들이 플레이팅이 예쁜 식당과 감성 인테리어 카페 같은 '인스타그래머블'한 장소를 찾아 나선다고 설명했다.",
      "interpretation", ["sx-aju-190815"], X, period="2019"),
    C("sx-photozone", "한 주점은 개점 2주 만에 해시태그 게시물 200여 개가 올라왔고, 업계는 포토존과 메뉴가 SNS로 알려지며 홍보 없이도 손님이 늘었다고 말했다. 빙그레는 2016년 3월 '바나나맛우유' 콘셉트의 옐로우카페를 열었고, 여러 식음료 회사가 SNS 인증 시설을 갖춘 브랜드 카페를 냈다.",
      "fact", ["sx-tf-insta", "sx-inews-yellow"], X, period="2016~2019"),
    C("sx-gamsung", "2022년 기사에서 20대는 서비스가 미흡해도 SNS에 올릴 사진을 찍으려고 감성카페에 간다고 말했다('훌륭한 서비스를 원하면 프랜차이즈에 갔을 것').",
      "fact", ["sx-sidae-220920"], X, period="2022"),
    C("sx-smallux", "한 연구위원은 MZ세대가 불황과 고물가의 우울함을 작은 사치로 풀고, 그 소비를 SNS에 인증·기록하며 기분을 바꾸고 남에게 과시하려 한다고 분석했다.",
      "interpretation", ["sx-sidae-240424"], X, period="2024"),
    C("sx-flex", "롯데멤버스 분석에서 20대의 명품 구매 건수는 2017년 3분기 대비 2019년 3분기 약 7.5배였고, 20대는 유튜브·인스타그램 인플루언서로 명품 정보를 얻는다는 응답이 26.7%였다. 보고서는 신상품을 빨리 사고 인증 사진을 남기려는 '플렉스' 문화를 배경으로 들었다.",
      "fact", ["sx-dailian-191201"], X, period="2017~2019"),
    C("sx-fatigue", "한 학술 논문은 SNS 사용자 10명 중 8~9명이 피로·불편을 느낀다는 조사를 인용하고, 남의 행복해 보이는 삶을 보며 박탈감을 느끼는 '카페인 우울증'(카카오스토리·페이스북·인스타그램)이라는 말이 생겼다고 정리했다.",
      "interpretation", ["sx-ks-fatigue"], X, period="2018"),
    C("sx-locket", "친구를 최대 20명까지만 등록하고 휴대폰 바탕화면 위젯으로 사진을 주고받는 폐쇄형 SNS '로켓'이 1020세대에서 인기를 끌었다.",
      "fact", ["sx-qletter-locket"], X, period="2020년대"),
    C("sx-cy", "1999년 문을 연 싸이월드는 2000년대 초 디지털카메라 열풍과 맞물려 10~20대를 끌어들였고, 전문가들은 사진을 주요 수단으로 내세운 점과 무제한 용량을 성공 요인으로 꼽았다(주간 사진 게시물 3천만 건).",
      "fact", ["sx-zdnet-cy"], X, period="1999~2010"),
    C("sx-cy-real", "싸이월드 미니홈피는 아바타 같은 익명 캐릭터가 아니라 실제 자기 정체성으로 지인과 연결되는 첫 서비스였고, 미니홈피는 2003년 400만 개에서 2005년 1,500만 개, 2007년 2,000만 개로 늘었다.",
      "fact", ["sx-etnews-cy"], X, period="2003~2007"),
    C("sx-cy-bgm", "미니홈피 배경음악(BGM)은 '자신을 표현하는 한 수단'으로 쓰였고, 싸이월드는 '도토리'라는 사이버 머니 붐을 일으켰다.",
      "interpretation", ["sx-segye-cybgm"], X, period="2000년대"),
    # ── 음악
    C("sx-lp-yes24", "예스24에서 LP 판매 증가율은 2020년 116.7%, 2021년 47.3%, 2022년 13.8%로 3년 연속 늘었다. 2022년 구매자는 40대 35%, 50대 21.2%, 30대 19.8%, 20대 16.5% 순이었다. 기사는 LP가 MZ세대에게 한정판 굿즈이자 자신을 꾸미는 소장품이라고 해석했다.",
      "fact", ["sx-nocut-lp"], X, period="2020~2022", scope="한 온라인 서점의 판매 자료. 2020년 증가율은 다른 보도(1월~12월 2일 집계 73.1%)와 다르다."),
    C("sx-lp-why", "2020년 보도는 LP 플레이어가 감성을 자극하는 인테리어 소품으로 쓰이고, 직접 산 LP 사진이나 복고풍 공간에서 찍은 사진을 SNS에 올리는 것이 유행이 됐다고 설명했다(예스24 집계 LP 판매 +73.1%, 1월 1일~12월 2일).",
      "interpretation", ["sx-dailian-201218"], X, period="2020"),
    C("sx-lp-ifpi", "IFPI '2023 음악 리포트'에서 소비자들은 LP를 사는 이유로 '음악을 물리적인 형태로 소유할 수 있어서'(22%), '레코드를 재생하는 경험이 좋아서'(19%)를 꼽았다.",
      "fact", ["sx-kyeongin-lp"], X, period="2023", scope="국제 조사이며 한국만의 수치가 아니다."),
    C("sx-lp-fair", "팬데믹이 끝난 뒤 2023~2024년 서울레코드페어 관객은 회당 평균 약 1만 3천 명으로 팬데믹 이전(2018~2019년)보다 20% 이상 줄었고, 국내 제작·유통사는 LP 제작에 여전히 소극적이라는 평가가 나왔다.",
      "fact", ["sx-newsis-251023"], X, period="2018~2025"),
    C("sx-album-hanteo", "한터차트 기준 연간 실물 앨범 판매량은 2017년 1,379만 장에서 2019년 1,857만 장으로 늘었고, 코로나19로 공연이 멈추며 팬들의 소비가 앨범으로 몰려 2023년 1억 장을 넘었다.",
      "fact", ["sx-tf-album"], X, period="2017~2023"),
    C("sx-album-26", "써클차트 기준 앨범 판매량은 2023년 약 1억 2천만 장에서 2024년 약 9,890만 장, 2025년 약 9,350만 장으로 줄었다가 2026년 반등했다. 평균 출고가는 2023년 1만 1,315원에서 2026년 1~9월 1만 3,285원으로 올랐고, QR·NFC로 듣는 플랫폼 앨범 비중은 11.3%에서 17.8%로, 평균 출고가 3만 5천 원 안팎의 LP는 9월까지 92만 장이 팔렸다. 같은 시기 디지털 차트 1위는 2024년 발매 뒤 유튜브로 재조명된 곡이었다.",
      "fact", ["sx-dailian-album26"], X, period="2023~2026"),
    C("sx-goldman", "2024년 4월 골드만삭스는 '케이팝의 음반 판매량은 오염되었다'는 보고서에서 앨범보다 콘서트 관객이 성장을 재기에 더 좋은 지표라고 썼고, 팬데믹 동안 오프라인 활동이 없어 앨범 판매가 급증하며 지표가 왜곡됐다고 지적했다.",
      "interpretation", ["sx-toss-fandustry"], X, period="2024"),
    C("sx-ytm", "모바일인덱스 기준 유튜브 뮤직은 2023년 12월 월간 이용자 649만 6천 명으로 멜론(623만 8천 명)을 처음 앞섰다. 멜론은 2022년 1월 769만 명에서 100만 명 넘게 줄었다. 유튜브는 월 1만 4,900원 프리미엄 가입자에게 유튜브 뮤직을 함께 제공해 '끼워팔기' 논란과 공정위 조사를 받았다.",
      "fact", ["sx-daum-240509", "sx-newsis-240115"], X, period="2022~2023"),
    C("sx-spotify", "와이즈앱·리테일 조사에서 2026년 국내 음원 앱 이용자는 유튜브뮤직 949만 명, 스포티파이 622만 명이었다. 스포티파이는 2024년 같은 달 161만 명에서 약 4배가 됐고, 분석은 광고를 보면 무료로 듣는 '스포티파이 프리'(2024년 10월)와 네이버플러스 멤버십 제휴를 이유로 들었다.",
      "fact", ["sx-hk-260728"], X, period="2024~2026"),
    C("sx-kocca-age", "한국콘텐츠진흥원 '2024 음악 이용자 조사'(10~69세 3,500명)에서 해외 스트리밍 서비스를 이용한다는 비율은 10대 56.3%, 20대 55.1%, 50대 51.3%, 60대 54.7%였고, 국내 서비스를 더 많이 쓰는 세대는 30대·40대뿐이었다.",
      "fact", ["sx-etoday-kocca"], X, period="2024"),
    # ── 문신
    C("sx-tattoo-gallup", "한국갤럽 2021년 조사(성인 1,002명)에서 5%가 타투를, 28%가 반영구 화장 문신을 해 봤다고 답했다. 타투 합법화 찬성은 51%로, 18~29세 81%, 30대 64%, 40대 60%였고 60대 이상만 반대(59%)가 많았다. 반영구 화장 경험은 여성 45%, 남성 10%였다.",
      "fact", ["sx-sgsg-211112", "sx-fn-221017"], X, period="2021"),
    C("sx-tattoo-meaning", "2022년 기사 속 30대는 주변에 세례명이나 연인의 이름을 새긴 친구가 많다며 '소중한 것을 잊지 말자는 의미'라고 말했다. 같은 기사는 기성세대 일부가 혐오감을 이유로 직장 내 불이익을 주는 사례도 전했다.",
      "fact", ["sx-fn-221017"], X, period="2022"),
    C("sx-tattoo-2018", "엠브레인 2018년 조사(1,000명)에서 70.9%가 '타투에 대한 인식이 과거보다 많이 관대해졌다'고 답했다.",
      "fact", ["sx-fn-221018"], X, period="2018"),
    C("sx-tattoo-celeb", "2022년 기사는 영향력 있는 스타들이 타투를 드러내며 타투와 타투 스티커가 새 뷰티 문화가 됐고, MZ세대에게 타투가 '새로운 액세서리'이자 개성을 드러내는 패션이 됐다고 해석했다.",
      "interpretation", ["sx-tenasia-220515"], X, period="2022"),
    C("sx-tattoo-dm", "한 타투이스트는 고객들이 인스타그램 등에 올린 타투이스트의 포트폴리오를 보고 DM으로 부위·그림·가격·날짜를 정해 예약한다고 말했다.",
      "fact", ["sx-sgsg-220929"], X, period="2022"),
    C("sx-ktattoo", "한국 타투이스트들은 섬세한 파인라인 작업으로 뉴욕·LA에서 이름을 알렸고, 한국의 작은·중간 크기 타투 가격은 보통 100~300달러다. 2027년 시행될 합법화로 'K-타투' 관광이 생길 수 있다는 전망이 나왔다.",
      "fact", ["sx-kt-250927"], X, period="2022~2025"),
    C("sx-tattoo-memorial", "가수 태연은 돌아가신 아버지를 기리려 생전 필체로 '1961'을 팔꿈치에 새겼고, 앨범을 낼 때마다 손가락에 타이틀곡을 상징하는 글자를 새긴 것으로 알려졌다. 보그는 타투가 '네일 아트나 향수처럼 일상적인 뷰티 요소'가 됐다고 썼다.",
      "fact", ["sx-vogue-taeyeon"], X),
    C("sx-tattoo-remove", "최근 SNS 숏폼에서 타투를 지우는 과정과 전후 모습을 담은 콘텐츠가 늘었고, 패션지는 과도한 장식을 덜어내는 뷰티 흐름('덜어냄의 미학')이 이를 뒷받침한다고 해석했다.",
      "interpretation", ["sx-mc-remove"], X, period="2025~2026"),
]

QS = [
    ("before", "이전에는 무엇을 골랐고, 왜 매력적이었나"),
    ("popular", "실제로 무엇이 인기를 얻었나 — 상품·스타일·공간·활동"),
    ("spread", "누구에게, 언제, 어떤 계기로 퍼졌나"),
    ("satisfy", "사람들은 어떤 만족을 얻었나"),
    ("friction", "무엇이 흔해지고·비싸지고·불편해졌나"),
    ("newchoice", "새 선택지는 무엇이 달랐나"),
    ("conditions", "가격·소득·주거·기술·인구·제도·미디어는 어떻게 작용했나"),
    ("suppliers", "브랜드·사업자는 새 선택을 어떻게 만들고 퍼뜨렸나"),
    ("relation", "옛 선택과 새 선택의 관계 — 교체·공존·혼합·분화·재등장"),
    ("unmet", "지금 남은 불편과 채워지지 않은 욕구"),
    ("next", "다음 수요 — 조건별 가능성"),
]

# ════════════════════════════════════════════════════════════════════════════
# 흐름 이야기(11개 질문)
# ════════════════════════════════════════════════════════════════════════════
STORIES = {}

STORIES["taste-pants"] = {
    "lead": "통바지 → 스키니 → 와이드로 '바뀌었다'가 아니라, 무엇이 불편해져서 무엇을 찾았고 그 사이에 누가 무엇을 퍼뜨렸는지.",
    "qs": {
        "before": [
            L("fact", "1990년대에는 힙합 음악과 함께 흘러내릴 듯 헐렁한 바지와 큰 신발이 퍼졌고, 후반에는 헐렁한 하의에 몸에 붙는 작은 상의를 맞춰 입었다. 1세대 아이돌도 큰 재킷과 통 큰 바지를 입었다.", ["ts-f-hiphop", "ts-f-1stgen"]),
            L("inference", "매력은 몸을 드러내지 않는 자유로움, 그리고 힙합을 좋아하는 무리에 속한다는 표시였다고 본다.", ["ts-f-hiphop"]),
        ],
        "popular": [
            L("fact", "2006년 '스키니 진'이라는 이름의 상품이 나와 젊은 층에서 퍼졌다. 진 시장은 2000년 수천억 원대에서 2006년 1조 8천억 원대로 커졌다. 한 SPA 브랜드의 데님 판매 1위는 2010~2017년 슬림, 2018년부터 테이퍼드·와이드였고 2024년에는 판매의 절반 이상이 와이드였다.", ["ts-f-skinny-start", "ts-f-jeans-mkt", "ts-f-spao"]),
        ],
        "spread": [
            L("fact", "2006년 말 꽃미남 스타의 영향 속에 젊은 남성들 사이에서 '폭발적 인기'라는 보도가 나왔고, 2009년 소녀시대 'Gee'로 인기가 커졌으며, 2010년 이후 여성의 필수 아이템이 됐다.", ["ts-f-skinny-men", "ts-f-skinny-start"]),
            L("fact", "와이드는 2016년 복고 방송('응답하라'·'토토가')과 놈코어를 배경으로 늘기 시작했고, 2022~23년 Y2K 유행에서는 뉴진스·NCT가 이끈 그룹으로 꼽혔다.", ["ts-f-2016", "ts-f-y2k-idol"]),
            L("inference", "'가는 다리 = 세련·젊음'이라는 이미지가 아이돌 무대와 뮤직비디오로 반복 노출되며 남녀 모두에게 퍼졌다고 본다.", ["ts-f-skinny-men", "ts-f-skinny-start"]),
        ],
        "satisfy": [
            L("source", "연구자들은 하반신 선을 드러내 날씬하고 관능적으로 보이려는 욕구를 스키니의 이유로 들었다. 업계는 와이드의 강점으로 편안한 착용감과 체형 보완을 들었다.", ["ts-f-skinny-why", "ts-f-spao-why"]),
            L("inference", "스키니는 '통바지 10년 뒤의 새로움'과 위에 큰 상의·긴 부츠를 더해 비율을 조절하기 쉬운 점이, 와이드는 '가리면서도 허리선을 올리면 다리가 길어 보이는' 점이 만족을 줬다고 본다.", ["ts-f-skinny-start", "ts-f-spao-why"]),
        ],
        "friction": [
            L("source", "2022년 보도는 스키니가 다리 선에 자신 없는 사람들에게 부담이었고 건강에 해롭다는 주장이 있었으며, '보디 포지티브'가 늦게 스며들었다고 정리했다.", ["ts-f-wide-why"]),
            L("inference", "앉을 때의 조임, 체형이 그대로 드러나는 압박, 10년 가까이 모두 같은 실루엣이라 새로움이 사라진 것이 피로로 쌓였다고 본다.", ["ts-f-spao", "ts-f-wide-why"]),
        ],
        "newchoice": [
            L("fact", "한 매장에서 여성 10~50대 전 연령의 1위가 와이드였고, 에이블리 데님 상위 50개 중 87%가 와이드였다.", ["ts-f-spao"]),
            L("inference", "와이드가 해결한 것은 '조임'과 '체형 노출 부담'이고, 새 매력은 나이·체형에 상관없이 같이 입을 수 있는 '기본'이 됐다는 점이다.", ["ts-f-spao", "ts-f-spao-why"]),
        ],
        "conditions": [
            L("source", "요가·필라테스, 코로나19 이후 홈트레이닝과 '원 마일 웨어'가 레깅스를 키웠고, 2026년 하렘팬츠는 운동과 일상의 경계 없이 입는 '웰니스 웨어' 수요로 설명됐다.", ["ts-f-leggings-why", "ts-f-harem"]),
            L("source", "1990~2000년대 레트로에 대한 향수가 와이드의 배경으로 꼽혔다.", ["ts-f-wide-why"]),
            L("inference", "SPA의 낮은 가격이 실루엣을 바꾸는 부담을 줄였다. 바지 한 벌이 싸면 유행이 바뀔 때 옷장 전체를 바꾸기 쉽다.", ["ts-f-spao", "fl-fash-spa"]),
        ],
        "suppliers": [
            L("source", "스파오는 이틀 만에 기획해 200장 안팎을 소량 생산하고 주말 반응을 본 뒤 생산량을 정하는 방식으로 카고진·카펜터진 같은 변형을 빠르게 냈다.", ["ts-f-spao-why"]),
            L("fact", "패션 플랫폼 지그재그에서 2022년 초 'Y2K' 검색은 61배, 로우라이즈 거래액은 10배 이상 늘었다.", ["ts-f-y2k"]),
            L("inference", "플랫폼은 검색·거래 순위로 '지금 뜨는 모양'을 바로 보여 줘, 작은 변형이 전국 유행이 되는 속도를 높였다.", ["ts-f-y2k", "ts-f-harem"]),
        ],
        "relation": [
            L("fact", "부츠컷(2016), 레깅스(2016~2020), 로우라이즈·카고(2022), 벌룬·하렘(2026)이 차례로 늘었고, 같은 매장에서 남성 50대의 1위는 와이드가 아닌 테이퍼드였다.", ["ts-f-2016", "ts-f-leggings", "ts-f-y2k", "ts-f-harem", "ts-f-spao"]),
            L("inference", "교체가 아니라 '기본(와이드) + 변주(카고·벌룬)'의 분화다. 같은 사람도 출근엔 와이드, 운동엔 레깅스, 놀 때는 카고처럼 상황에 따라 고른다.", ["ts-f-spao", "ts-f-y2k-idol"]),
        ],
        "unmet": [
            L("fact", "2025년 패션지들은 스키니가 돌아올 조짐이라고 보도했지만, 2010년대처럼 발목까지 조이지 않는 형태로 소개했다.", ["ts-f-slim-back"]),
            L("inference", "와이드 8년째라 새로움이 줄었고, 넓은 밑단의 길이 수선과 신발 조합 같은 번거로움이 쌓였을 수 있다. '편하면서 다리가 길어 보이는' 바지는 아직 정답이 없다.", ["ts-f-spao", "ts-f-slim-back"]),
        ],
        "next": [
            L("hypothesis", "조이지 않는 슬림·세미 부츠컷 — 플랫폼 데님 상위권에서 슬림 비중이 오르면 강해지고, 상위권이 계속 와이드면 약해진다.", ["ts-f-slim-back", "ts-f-spao"]),
            L("hypothesis", "볼륨 모양의 변형(벌룬·배럴) — 여름 뒤에도 거래가 이어지면 강해진다.", ["ts-f-harem"]),
            L("hypothesis", "출근도 되는 기능성 바지 — 애슬레저 브랜드의 일상복 매출 비중이 커지면 강해진다.", ["ts-f-leggings", "ts-f-harem"]),
        ],
    },
    "links": [
        {"flow": "flow-fashion", "step": "f5", "why": "SPA가 들어오며 실루엣을 싸게 바꿀 수 있게 됐다"},
        {"flow": "flow-music", "step": "m8", "why": "아이돌 영상이 스타일을 퍼뜨리는 통로"},
        {"flow": "taste-home", "why": "같은 시기 집에서도 '편안함'이 기준이 됐다"},
    ],
}

STORIES["flow-expression"] = {
    "lead": "옷 → 사진 → 몸. 나를 드러내는 수단이 바뀔 때마다 '누가 막았고, 무엇이 가능해졌고, 무엇을 보여 주고 싶었는지'.",
    "qs": {
        "before": [
            L("fact", "1967년 가수 윤복희가 미니스커트를 입고 귀국한 뒤 유행해 1968년 절정에 이르렀고, 1973년 경범죄처벌법 개정으로 장발·미니스커트가 단속 대상이 됐다(1973년에만 장발 단속 1만 2천여 건).", ["er-expr-mini", "c70-taboo", "c70-longhair"]),
            L("inference", "1970년대의 꾸미기는 '국가가 정한 단정함'에 맞서는 일이었다. 짧은 치마·긴 머리·청바지는 옷이 아니라 세대와 태도의 표시였다.", ["c70-youth", "c70-taboo"]),
        ],
        "popular": [
            L("fact", "1990년대 X세대는 '입고 싶은 대로 입는' 세대로 불렸고, 2000년대에는 디지털카메라와 싸이월드 미니홈피(2007년 2,000만 개), 2010년대에는 인스타그램 인증샷, 2020년대에는 작은 타투가 퍼졌다.", ["er-expr-x", "sx-cy-real", "sx-sns-2016", "sx-tattoo-gallup"]),
        ],
        "spread": [
            L("fact", "미니홈피는 디카 열풍과 맞물려 10~20대에게 퍼졌다. 인스타그램은 2023년 조사에서 X세대(만 39~54세)에서도 1순위 SNS였다.", ["sx-cy", "er-expr-insta"]),
            L("source", "타투는 영향력 있는 스타들이 드러내면서 '새로운 액세서리'가 됐다는 해석이 있다. 합법화 찬성은 18~29세 81%로 젊을수록 높았다.", ["sx-tattoo-celeb", "sx-tattoo-gallup"]),
        ],
        "satisfy": [
            L("fact", "2016년 20대의 25.6%는 SNS로 관심받는 것을 즐긴다고 답했고, 하루 평균 1.46회 '인증'을 했다. 밀레니얼은 SNS 목적으로 '일상 기록·공유'를 많이 꼽았다.", ["sx-sns-2016", "er-expr-insta"]),
            L("source", "미니홈피 배경음악은 '자신을 표현하는 수단'이었고, 작은 사치를 SNS에 인증하는 것은 기분 전환과 과시를 함께 준다는 분석이 있다.", ["sx-cy-bgm", "sx-smallux"]),
            L("fact", "타투는 세례명·연인 이름·돌아가신 아버지의 필체처럼 '잊지 않으려는 것'을 새기는 경우가 많았다.", ["sx-tattoo-meaning", "sx-tattoo-memorial"]),
        ],
        "friction": [
            L("source", "SNS 사용자 다수가 피로를 느꼈고, 남의 행복한 삶과 비교하며 박탈감을 느끼는 '카페인 우울증'이라는 말이 생겼다.", ["sx-fatigue"]),
            L("fact", "한 대학생은 SNS를 쓰면 자신이 초라해 보이고 '잘 보이기 위해 꾸며내는' 느낌이 들어 사용을 자제했다고 말했다.", ["sx-sns-2016"]),
            L("inference", "사진은 매일 새로 올려야 하고 남과 비교되지만, 타투는 한 번 새기면 매일 몸에 지니는 '변하지 않는 나'다. 비교와 휘발에 지친 표현 욕구가 더 오래 가는 수단을 찾은 것으로 본다.", ["sx-fatigue", "sx-tattoo-meaning"]),
        ],
        "newchoice": [
            L("fact", "타투이스트의 인스타그램 포트폴리오를 보고 DM으로 부위·그림·가격·날짜를 정해 예약하는 방식이 자리 잡았다. 한국 타투이스트들은 섬세한 파인라인으로 해외에서 이름을 알렸다.", ["sx-tattoo-dm", "sx-ktattoo"]),
            L("inference", "예전 문신(크고 진한 그림)과 달리 파인라인·미니 타투는 작고 옷으로 가릴 수 있어, 직장과 가족의 시선을 피하면서도 '나만 아는 의미'를 지닐 수 있었다. 이 점이 처음 하는 사람의 문턱을 낮췄다고 본다.", ["sx-ktattoo", "sx-tattoo-meaning"]),
        ],
        "conditions": [
            L("fact", "1982년 정부는 두발·교복 자율화를 발표했다. 1980년 신군부의 유화책 가운데 하나로 보는 설명이 있다.", ["fl-expr-uniform"]),
            L("fact", "싸이월드의 성공 요인으로 사진 중심과 무제한 용량, 2000년대 초 디카 열풍이 꼽힌다. 스마트폰은 2010년 한 해에 약 80만에서 722만 가입자로 늘었다.", ["sx-cy", "c00-kr-iphone"]),
            L("fact", "1992년 대법원이 문신을 의료행위로 본 뒤 비의료인 시술은 불법이었지만, 이용자의 81%가 문신 전문숍에서 시술받았다. 국회는 2025년 문신사법을 통과시켰다.", ["fl-expr-tattoo-law", "fl-expr-tattoo-survey"]),
            L("inference", "법은 가장 늦게 움직였다. 기술(카메라·스마트폰)과 미디어(스타·SNS)가 먼저 행동을 바꾸고, 제도는 수십 년 뒤 현실을 따라왔다.", ["fl-expr-tattoo-law", "c00-kr-iphone"]),
        ],
        "suppliers": [
            L("fact", "싸이월드는 도토리로 스킨·배경음악을 팔았다. 식음료 회사들은 SNS 인증용 브랜드 카페를 열었고(빙그레 2016), 한 주점은 포토존으로 개점 2주 만에 게시물 200여 개를 얻었다.", ["sx-cy-bgm", "sx-photozone"]),
            L("fact", "20대는 명품 정보를 인플루언서에게서 얻었고(26.7%), 신상품을 빨리 사서 인증하는 '플렉스' 문화가 보고됐다.", ["sx-flex"]),
            L("source", "사진이 잘 나오는 '인스타그래머블'한 장소가 손님을 모으자, 가게들이 인테리어를 사진 기준으로 바꿨다.", ["sx-sns-why", "sx-gamsung"]),
        ],
        "relation": [
            L("inference", "교체보다 누적이다. 옷으로 하던 표현에 사진이 더해졌고, 사진 위에 몸(타투)이 더해졌다. 같은 사람이 옷은 무난하게, SNS는 비공개로, 몸에는 작은 의미를 새기는 식으로 표현의 강도를 나눠 쓴다.", ["er-expr-x", "sx-locket", "sx-tattoo-meaning"]),
            L("fact", "모두에게 공개하던 SNS 옆에 친구 20명만 보는 폐쇄형 SNS가 1020세대에서 인기를 끌었다.", ["sx-locket"]),
        ],
        "unmet": [
            L("fact", "직장 내 불이익과 세대 간 시선 차이가 남아 있다(60대 이상은 합법화 반대가 많음).", ["sx-tattoo-meaning", "sx-tattoo-gallup"]),
            L("source", "타투 제거 과정을 담은 숏폼이 늘고, 장식을 덜어내는 뷰티 흐름이 이를 뒷받침한다는 해석이 나왔다.", ["sx-tattoo-remove"]),
            L("inference", "'보여 주고 싶은 나'와 '남의 시선에서 자유롭고 싶은 나' 사이의 균형을 맞춰 줄 수단이 아직 부족하다.", ["sx-fatigue", "sx-tattoo-remove"]),
        ],
        "next": [
            L("hypothesis", "되돌릴 수 있는 표현 — 타투 스티커·반영구, 제거 시술. 제거 시술 검색·매출이 늘면 강해진다.", ["sx-tattoo-celeb", "sx-tattoo-remove"]),
            L("hypothesis", "작은 무리 안의 표현 — 폐쇄형·소수 친구 SNS. 공개 SNS 게시 빈도가 줄면 강해진다.", ["sx-locket"]),
            L("hypothesis", "합법화 뒤 'K-타투' 관광과 위생·자격을 내세운 숍. 2027년 시행 이후 등록 숍 수와 외국인 예약이 지표다.", ["sx-ktattoo", "fl-expr-tattoo-law"]),
        ],
    },
    "links": [
        {"flow": "flow-tech", "step": "t5", "why": "스마트폰 — 카메라를 늘 들고 다니게 됐다"},
        {"flow": "flow-fashion", "step": "f2", "why": "청바지·장발 — 옷이 세대를 드러내던 시절"},
        {"flow": "flow-politics", "step": "p4", "why": "1987년 이후 '권위가 무너진' 분위기가 X세대의 배경"},
        {"flow": "taste-goods", "why": "같은 시기 가방·소지품 꾸미기"},
    ],
}

STORIES["flow-shop"] = {
    "lead": "시장 → 편의점·대형마트 → 홈쇼핑 → 모바일·배달. 장소가 바뀐 이유는 '시간·거리·결제'의 불편이 어떻게 풀렸는지에 있다.",
    "qs": {
        "before": [
            L("source", "1970~80년대에는 동네 슈퍼마켓과 재래시장이 유통의 대부분을 맡았고, 큰 가게도 100~200평 규모였다는 설명이 있다.", ["fl-shop-before"]),
            L("inference", "걸어서 가는 단골 가게라 외상·흥정·덤 같은 관계가 매력이었다. 대신 문 닫는 시간이 정해져 있고, 한 번에 살 수 있는 양과 종류가 적었다.", ["fl-shop-before", "c80-curfew"]),
        ],
        "popular": [
            L("fact", "1989년 첫 편의점(세븐일레븐)은 '24시간 여는 슈퍼마켓'으로 받아들여졌다. 1993년 첫 할인점 이마트 뒤 1996년까지 대형 할인점이 30여 곳으로 늘었다. 홈쇼핑 취급고는 1995년 34억 원에서 2014년 14조 원을 넘었다.", ["er-shop-cvs", "fl-shop-emart", "fl-shop-homeshop"]),
            L("fact", "모바일쇼핑은 2015년 11월 온라인쇼핑의 절반에 이르렀고, 배달앱 이용자는 2013년 87만 명에서 2019년 2,500만 명이 됐다.", ["fl-shop-mobile", "c10-delivery"]),
        ],
        "spread": [
            L("fact", "업계는 첫 편의점의 배경으로 올림픽 이후의 국제화 열풍과 높아진 소득을 꼽는다. 1982년 야간통행금지 해제 당일 신문은 '24시간을 생활한다'고 썼다.", ["er-shop-cvs", "c80-ch-24h"]),
            L("fact", "자동차는 1985년 100만 대에서 1988년 200만 대, 1992년 500만 대가 됐다.", ["sx-cars"]),
            L("inference", "밤에도 다닐 수 있게 되고(통금 해제), 차가 생기고(마이카), 소득이 늘자 '밤에 조금씩 사는 곳'(편의점)과 '주말에 차로 많이 사는 곳'(할인점)이 동시에 필요해졌다.", ["c80-curfew", "sx-cars", "sx-wage-loc"]),
        ],
        "satisfy": [
            L("inference", "편의점은 시간의 자유, 할인점은 한 번에 싸게 많이 사는 만족, 홈쇼핑은 집에서 설명을 들으며 사는 편안함, 모바일·배달은 '어디서든 몇 번 누르면 끝'이라는 편리함을 줬다.", ["er-shop-cvs", "fl-shop-emart", "fl-shop-homeshop", "fl-shop-mobile-why"]),
        ],
        "friction": [
            L("fact", "카드 사용을 부추긴 뒤 현금서비스·카드론이 1998년 약 10조 원에서 2002년 하반기 약 60조 원으로 불어났고, 2003년 말 금융채무 불이행자는 372만 명이 됐다.", ["c00-card", "c00-card-why"]),
            L("inference", "할인점은 차를 타고 가서 줄 서고 많이 사야 하는 수고, 홈쇼핑은 방송 시간에 맞춰야 하는 제약이 있었다. 1인 가구가 늘자 '많이 사서 싸게'가 오히려 짐이 됐다고 본다.", ["c10-1person", "fl-shop-emart"]),
        ],
        "newchoice": [
            L("source", "모바일쇼핑이 커진 이유로 모든 연령의 스마트폰 보편화, 화면 대형화, 2015년 간편결제의 경쟁적 도입이 꼽혔다. 배달앱은 1인 가구·맞벌이와 스마트폰 결제가 키웠다는 분석이 있다.", ["fl-shop-mobile-why", "c10-syn-delivery"]),
        ],
        "conditions": [
            L("fact", "1인 가구는 2015년 가장 흔한 가구가 됐다. 2020년 코로나19 속 온라인쇼핑 비중은 소매판매의 27.2%가 됐다.", ["c10-1person", "c20-online"]),
            L("inference", "결제 수단의 변화(백화점 카드 → 은행 카드 → 간편결제)가 매번 '어디서 살 수 있나'를 넓혔다. 결제가 쉬워질수록 장소의 제약이 줄었다.", ["er-shop-card69", "er-shop-card78", "fl-shop-mobile-why"]),
        ],
        "suppliers": [
            L("fact", "신세계는 1993년 창고형 할인점을 열었고, 1996년 유통시장 개방 뒤 외국계와 경쟁하며 점포를 크게 늘렸다. 2015년부터 앱카드·네이버페이·페이코·SSG페이가 경쟁적으로 도입됐다.", ["fl-shop-emart", "fl-shop-discount-stage", "fl-shop-mobile-why"]),
        ],
        "relation": [
            L("inference", "교체가 아니라 역할 분담이다. 편의점은 가까운 곳 소량, 할인점은 주말 대량, 온라인은 반복 구매, 배달은 바로 먹을 것. 같은 사람이 상황에 따라 네 가지를 모두 쓴다.", ["er-shop-cvs", "fl-shop-emart", "fl-shop-mobile", "c10-delivery"]),
        ],
        "unmet": [
            L("inference", "빠른 배송과 배달에 익숙해진 만큼 포장 쓰레기, 배달비, 라이더 안전 같은 비용이 눈에 띄게 됐다. 직접 보고 고르는 재미는 온라인이 채우지 못한다.", ["c10-rider-risk", "c10-delivery"]),
        ],
        "next": [
            L("hypothesis", "직접 보고 경험하는 매장(체험·팝업)과 빠른 배송의 조합 — 오프라인 체험형 매장 수와 매출이 지표다.", ["c20-online"]),
            L("hypothesis", "1인 가구에 맞춘 소량·근거리 — 편의점·퀵커머스 매출이 지표다.", ["c10-1person"]),
        ],
    },
    "links": [
        {"flow": "flow-time", "step": "h3", "why": "통금 해제 — 밤에도 장을 볼 수 있게 됐다"},
        {"flow": "flow-city", "step": "c5", "why": "자동차 — 주말에 차로 대량 구매"},
        {"flow": "flow-family", "step": "f4", "why": "1인 가구 — 소량·배달 수요"},
        {"flow": "flow-tech", "step": "t5", "why": "스마트폰 — 손안의 매장"},
    ],
}

STORIES["flow-music"] = {
    "lead": "음악을 '어디서 누구와 어떻게' 들었나 — 남이 골라 주던 음악에서, 직접 부르고, 무한히 고르고, 다시 손에 쥐는 쪽으로.",
    "qs": {
        "before": [
            L("fact", "1960년대에는 라디오와 도심 음악감상실(세시봉 등)에서, 1970년대에는 음악다방 DJ가 틀어 주는 음악을 들었다. 매니저들은 새 앨범이 나오면 전국 음악다방 DJ를 찾아다녔다.", ["c60-sesibong", "fl-mus-musicroom", "fl-mus-dabang"]),
            L("inference", "매력은 '신곡을 처음 듣는 장소'와 '같은 음악을 함께 듣는 사람들'이었다. 음반과 전축이 비쌌던 시절, 음악은 공간에서 나눠 듣는 것이었다.", ["fl-mus-dabang", "c70-culture-why"]),
        ],
        "popular": [
            L("fact", "1980년대 TV 순위 프로그램('가요톱10')이 가장 영향력이 컸고, 1995년 김건모 3집은 두 달 만에 230만 장이 팔렸다. 노래방은 1992년 1만 곳, 1996년 3만 5천 곳을 넘었다.", ["er-mus-top10", "fl-mus-1995", "fl-mus-noraebang"]),
            L("fact", "2004년 정액제 스트리밍(멜론), 2021년 음악 동영상 사이트 이용 81%, 2023년 실물 앨범 1억 장, 2020년대 LP의 재유행이 이어졌다.", ["fl-mus-melon", "fl-mus-video", "sx-album-hanteo", "sx-lp-yes24"]),
        ],
        "spread": [
            L("fact", "TV 가구 보급률은 1970년 6.3%에서 1979년 79%가 됐고, 1981년 컬러 방송으로 TV 스타가 두드러졌다.", ["c70-culture-why", "er-mus-80s"]),
            L("fact", "1995년 '잘못된 만남'은 레코드 가게와 테이프 리어카에서 종일 흘러나왔다. 2000년 소리바다가 파일 공유를 열었고, 2009년 멜론이 스마트폰 스트리밍을 시작했다.", ["fl-mus-street", "fl-mus-soribada", "fl-mus-melon"]),
            L("fact", "해외 스트리밍 이용은 10·20대(55% 이상)와 50·60대가 높고 30·40대는 국내 서비스를 더 쓴다.", ["sx-kocca-age"]),
        ],
        "satisfy": [
            L("inference", "노래방은 '듣는 사람'을 '부르는 사람'으로 바꿨다. 정액 스트리밍은 곡마다 돈을 내지 않고 무한히 고르는 자유를, 유튜브는 영상과 함께 우연히 발견하는 재미를 줬다.", ["fl-mus-noraebang", "fl-mus-melon", "fl-mus-video"]),
            L("fact", "LP를 사는 이유로는 '물리적으로 소유할 수 있어서'(22%)와 '재생하는 경험'(19%)이 꼽혔다.", ["sx-lp-ifpi"]),
            L("source", "LP 플레이어는 인테리어 소품이 되고, 산 LP를 SNS에 올리는 것이 유행이 됐다는 설명이 있다. LP는 MZ에게 한정판 굿즈이자 소장품이라는 해석도 있다.", ["sx-lp-why", "sx-lp-yes24"]),
        ],
        "friction": [
            L("fact", "음반 시장은 2000년 약 4,100억 원에서 2003년 1,833억 원으로 줄었다. 업계는 무료 파일 공유를 탓했지만, 같은 시기 온라인 매출 대부분은 벨소리였다.", ["fl-mus-cd-crash", "fl-mus-soribada-cause"]),
            L("source", "노래방은 2000년대 중후반을 정점으로 줄었고, 연구소는 회식 문화 변화와 대체 시설을 이유로 들었다.", ["fl-mus-noraebang-peak"]),
            L("source", "K팝 앨범은 팬들의 반복 구매로 부풀어 '오염된 지표'라는 비판을 받았다.", ["sx-goldman"]),
            L("inference", "스트리밍은 곡이 너무 많아 고르기가 피곤하고, 아무리 들어도 '내 것'이 남지 않는다. 이 빈자리가 소유·의식(LP)과 알고리즘 추천(유튜브)으로 각각 채워졌다고 본다.", ["sx-lp-ifpi", "fl-mus-video"]),
        ],
        "newchoice": [
            L("fact", "유튜브 뮤직은 2023년 12월 멜론을 처음 앞섰고, 스포티파이는 광고를 보면 무료로 듣는 요금제(2024년 10월) 뒤 2년 만에 이용자가 약 4배가 됐다.", ["sx-ytm", "sx-spotify"]),
            L("fact", "실물 CD 대신 QR·NFC로 듣는 '플랫폼 앨범'의 비중이 2023년 11.3%에서 2026년 17.8%로 늘었다.", ["sx-album-26"]),
        ],
        "conditions": [
            L("fact", "기기 변화가 매번 통로를 바꿨다 — 라디오 보내기 운동(1960년대), TV 보급(1970년대), 컬러TV(1981), 휴대전화 벨소리(2003), 스마트폰 스트리밍(2009).", ["c60-kr-radio-3", "c70-culture-why", "er-mus-80s", "fl-mus-cd-crash", "fl-mus-melon"]),
            L("fact", "요금 묶음이 승패를 갈랐다 — 통신사 멜론, 유튜브 프리미엄에 묶인 유튜브 뮤직, 네이버플러스와 제휴한 스포티파이.", ["fl-mus-melon", "sx-ytm", "sx-spotify"]),
            L("fact", "코로나19로 공연이 멈추자 팬들의 소비가 앨범으로 몰렸다.", ["sx-album-hanteo"]),
        ],
        "suppliers": [
            L("fact", "SK텔레콤은 2004년 유·무선 연동 정액제 멜론을 냈다. 기획사들은 앨범 평균 출고가를 2023년 1만 1,315원에서 2026년 1만 3,285원으로 올리고, 출고가 3만 5천 원 안팎의 LP를 냈다.", ["fl-mus-melon", "sx-album-26"]),
            L("inference", "기획사는 앨범을 '듣는 매체'에서 '모으고 후원하는 굿즈'로 바꿔 팔았다. 플랫폼은 음악을 다른 구독(영상·쇼핑 멤버십)에 끼워 넣어 '따로 돈 내는 음악'의 문턱을 없앴다.", ["sx-album-hanteo", "sx-ytm", "sx-spotify"]),
        ],
        "relation": [
            L("fact", "2011년에는 스마트폰이 많이 팔리는 동시에 통기타·LP·음악카페 같은 아날로그 복고가 함께 유행했다.", ["c10-analog", "c10-sesibong"]),
            L("inference", "교체가 아니라 역할 분담이다. 평소 듣기는 스트리밍, 발견은 유튜브, 소장과 의식은 LP, 응원은 앨범. 편리한 디지털을 쓰면서 특정 순간에만 아날로그를 찾는다.", ["c10-analog", "sx-lp-ifpi", "fl-mus-video"]),
            L("fact", "LP 구매자는 40·50대가 절반을 넘었고(2022), 해외 스트리밍은 10·20대와 50·60대가 더 많이 쓴다 — 같은 시기 세대마다 다른 조합이다.", ["sx-lp-yes24", "sx-kocca-age"]),
        ],
        "unmet": [
            L("fact", "서울레코드페어 관객은 팬데믹 이전보다 20% 넘게 줄었고, 국내 LP 제작은 아직 소극적이다. 같은 시기 디지털 1위는 유튜브로 재조명된 2년 전 곡이었다.", ["sx-lp-fair", "sx-album-26"]),
            L("inference", "알고리즘이 고른 음악에 익숙해질수록 '내가 찾았다'는 감각과 함께 듣는 경험이 줄었다. 공연·청음 공간 같은 '함께 듣는 자리'가 비어 있다.", ["sx-goldman", "sx-lp-fair"]),
        ],
        "next": [
            L("hypothesis", "함께 듣는 공간(청음 바·LP 카페·소규모 공연) — 공연 관객 수와 청음 공간 창업이 지표다.", ["sx-goldman", "sx-lp-why"]),
            L("hypothesis", "다른 구독에 묶인 음악 — 멤버십 묶음 상품이 늘면 음악 단독 요금은 더 약해진다.", ["sx-ytm", "sx-spotify"]),
            L("hypothesis", "듣는 기능 없는 '소장용' 실물(플랫폼 앨범·한정 LP) — 플랫폼 앨범 비중이 계속 늘면 강해진다.", ["sx-album-26"]),
        ],
    },
    "links": [
        {"flow": "flow-leisure", "step": "l5", "why": "노래방과 PC방 — 집 밖의 여가"},
        {"flow": "flow-tech", "step": "t5", "why": "스마트폰 — 스트리밍의 통로"},
        {"flow": "flow-relations", "step": "r4", "why": "팬카페 — 응원하는 공동체"},
        {"flow": "taste-goods", "why": "굿즈·한정판 — 앨범이 굿즈가 된 흐름과 같은 구조"},
    ],
}

# ════════════════════════════════════════════════════════════════════════════
# 단계 풀이 — 그때 분위기와 이어진 변화(다른 흐름으로 바로 이동)
# ════════════════════════════════════════════════════════════════════════════
STEP_NOTES = {
    ("flow-politics", "p4"): {
        "mood": [
            L("inference", "1987년 여름은 '말해도 된다'는 해방감의 시기였다. 직선제 약속(6·29) 뒤 공장·언론·대학에서 미뤄 두었던 요구가 한꺼번에 나왔다.", ["c80-629", "c80-labor"]),
            L("fact", "6·29선언 뒤 7월 5일 울산 현대엔진 노조 결성을 시작으로 노동자 대투쟁이 전국 공단으로 번졌고, 4개월 동안 400여 개의 민주노조가 생겼다.", ["c80-labor", "c80-labor-unions"]),
        ],
        "ripple": [
            {"area": "일과 소득", "line": L("fact", "명목임금 인상률은 1988년 15.5%, 1989년 21.1%였고, 1989년 노조 조직률은 18.6%로 역대 최고였다. 제조업 임금은 1988년 20%, 1989년 25% 올랐다.", ["sx-wage8889", "sx-wage-loc"]),
             "go": ["flow-jobs", "j6"]},
            {"area": "경제 분위기", "line": L("source", "3저 호황과 겹친 1987년 이후 10년을 '노조 활성화 → 취업 증가 → 임금 상승'의 선순환으로, 소비와 투자가 활기를 띤 시기로 보는 해석이 있다.", ["sx-golden", "c80-3low"]),
             "go": ["flow-economy", "ec3"]},
            {"area": "언론·말의 산업", "line": L("fact", "언론기본법 폐지 뒤 서울 종합일간지는 6개(1987)에서 10개(1989)로, 지역지는 10개에서 30개로 늘었다. 해직 기자들은 국민 모금 50억 원으로 1988년 한겨레를 창간했다.", ["sx-press", "sx-hani"])},
            {"area": "소비 — 마이카", "line": L("fact", "자동차는 1985년 100만 대에서 1988년 200만 대, 1990년 300만 대가 됐고, 1989년 렌터카 매출은 36.8% 늘어 '마이카시대'의 호황 업종이 됐다.", ["sx-cars", "sx-rentcar"]),
             "go": ["flow-city", "c5"]},
            {"area": "소비 — 여행·여가", "line": L("fact", "1989년 1월 해외여행이 전면 자유화됐다. 1991년 노래방이 생겨 이듬해 1만 곳을 넘었다.", ["c80-travel", "fl-mus-noraebang"]),
             "go": ["flow-leisure", "l4"]},
            {"area": "유통", "line": L("fact", "1989년 첫 편의점이 올림픽선수촌 아파트 상가에 문을 열었다. 업계는 국제화 열풍과 높아진 소득을 배경으로 들었다.", ["er-shop-cvs"]),
             "go": ["flow-shop", "s1c"]},
            {"area": "주거", "line": L("fact", "3저 호황·올림픽 특수와 베이비부머의 결혼이 겹쳐 1988년 서울 집값이 24% 올랐고, 정부는 주택 200만 호 건설 계획을 내놨다.", ["fl-city-newtown-why"]),
             "go": ["flow-city", "c7"]},
            {"area": "문화·자기표현", "line": L("inference", "임금이 오르고 말이 자유로워진 뒤 자란 세대가 1990년대 '권위가 무너진' X세대로 불렸다. 부모 세대보다 쓸 돈과 고를 자유가 많았던 것이 '입고 싶은 대로'의 바탕이라고 본다.", ["er-expr-x", "sx-wage8889"]),
             "go": ["flow-expression", "x5"]},
        ],
        "after": L("source", "반대편도 있었다. 1990년 정부 경제백서는 생산성을 웃도는 임금 인상이 고용 감소와 물가 상승을 낳기 시작했다고 분석했다.", ["sx-whitepaper90"]),
    },
}

LEVEL_OK = ("fact", "source", "inference", "hypothesis")


def validate(claims_all, flows, taste_ids):
    cids = {c["id"]: c for c in claims_all}
    fsteps = {f["id"]: {s["id"] for s in f["steps"]} for f in flows}

    def chk_line(x, where):
        if x["layer"] in ("fact", "source") and not x["ids"]:
            raise SystemExit(f"{where}: 사실·출처 해석에는 근거가 필요하다 — {x['text'][:30]}")
        for i in x["ids"]:
            if i not in cids:
                raise SystemExit(f"{where}: 없는 근거 {i}")

    def chk_go(flow, step, where):
        if flow in fsteps:
            if step and step not in fsteps[flow]:
                raise SystemExit(f"{where}: 없는 단계 {flow}/{step}")
        elif flow not in taste_ids:
            raise SystemExit(f"{where}: 없는 흐름 {flow}")

    for fid, st in STORIES.items():
        if fid not in fsteps and fid not in taste_ids:
            raise SystemExit(f"이야기: 없는 흐름 {fid}")
        for k, _ in QS:
            if not st["qs"].get(k):
                raise SystemExit(f"{fid}: 질문 '{k}'에 답이 없다")
            for x in st["qs"][k]:
                chk_line(x, f"{fid}/{k}")
        for ln in st.get("links", []):
            chk_go(ln["flow"], ln.get("step"), f"{fid} 연결")
    for (fid, sid), n in STEP_NOTES.items():
        if sid not in fsteps.get(fid, set()):
            raise SystemExit(f"단계 풀이: 없는 단계 {fid}/{sid}")
        for x in n["mood"]:
            chk_line(x, f"{fid}/{sid} 분위기")
        for r in n["ripple"]:
            chk_line(r["line"], f"{fid}/{sid} 파급")
            if r.get("go"):
                chk_go(r["go"][0], r["go"][1], f"{fid}/{sid} 파급")
        if n.get("after"):
            chk_line(n["after"], f"{fid}/{sid}")
    return {
        "qs": [{"key": k, "label": t} for k, t in QS],
        "stories": STORIES,
        "stepNotes": {f"{f}/{s}": n for (f, s), n in STEP_NOTES.items()},
        "layers": {"fact": "사실", "source": "출처 해석", "inference": "AI 추론", "hypothesis": "가설"},
    }
