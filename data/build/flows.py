"""변화 흐름(flows) — 사용자의 질문 하나를 중심으로 여러 사건·통계·주장을 잇는 단위.

원칙
- 단계 제목은 무엇을 다루는지만 적는다. 사실 문장은 모두 주장(claim)으로 두고 출처를 단다.
- 단계 사이 연결은 성격을 따로 적는다:
    causal(자료가 뒷받침하는 인과) / condition(배경·조건) / correlation(상관·통계적 연관)
    sequence(시간적 선후일 뿐) / interpretation(해석) / hypothesis(검증되지 않은 가설)
- 모든 흐름에 같은 단계를 강요하지 않는다. 확인하지 못한 부분(gaps)과 다른 설명(alternatives)을 함께 둔다.
- 사이트가 지표에서 직접 계산한 문장은 claimType='statistical', 출처는 지표 원자료로 둔다.
"""

A = "2026-11-11"


def S(id, title, pub, url, stype, published=None, note=None, origin=None):
    d = {"id": id, "title": title, "publisher": pub, "url": url, "sourceType": stype, "accessedDate": A}
    if published:
        d["publishedDate"] = published
    if note:
        d["note"] = note
    if origin:
        d["origin"] = origin  # 같은 원자료(발표·조사)를 옮긴 출처끼리는 하나로 센다
    return d


def C(id, text, ctype, status, sources, domains, period=None, scope=None, support=None):
    d = {"id": id, "text": text, "claimType": ctype, "status": status, "sourceIds": sources,
         "domains": domains, "countries": ["KR"], "aiSynthesized": False}
    if period:
        d["period"] = period      # 이 문장이 다루는 시기
    if scope:
        d["scope"] = scope        # 적용 범위와 한계
    if support:
        d["support"] = support    # 출처의 어느 부분이 이 문장을 뒷받침하는가
    return d


SOURCES = [
    # ── 음악 ──
    S("mus-seoul-mediahub", "낭만 가득한 7080 서울 여행, '여기는 대한민국 1970KHz'", "서울시 미디어허브",
      "https://mediahub.seoul.go.kr/archives/193794", "government", note="서울역사박물관 전시 소개"),
    S("mus-skhan-2012-dj", "오늘은 왠지~ 그 DJ 오빠 보고 싶어라", "스포츠경향",
      "https://sports.khan.co.kr/article/201204231948023", "news", published="2012-04-23"),
    S("mus-themusical-sesibong", "쎄시봉 — 음악 감상실의 시대", "더뮤지컬",
      "https://www.themusical.co.kr/Magazine/Detail?num=2420", "news"),
    S("mus-seoul-950327", "김건모 3집 앨범 「잘못된 만남」 두 달 만에 230만 장 팔려", "서울신문",
      "https://www.seoul.co.kr/news/1995/03/27/19950327013001", "news", published="1995-03-27"),
    S("mus-seoul-950508", "김건모·룰라 앨범 1백만 장 이상 팔려", "서울신문",
      "https://www.seoul.co.kr/news/1995/05/08/19950508011001", "news", published="1995-05-08"),
    S("mus-wk-10man", "'10만 장 시대'로 추락한 우리 가요계", "주간경향",
      "https://weekly.khan.co.kr/article/18283", "news", note="2000년대 후반 기사(한국음악산업협회 판매 통계 인용)"),
    S("mus-dc-2004", "디지털콘텐츠의 저작권 문제 ②", "디지털콘텐츠(월간, KoreaScience 수록)",
      "https://koreascience.or.kr/article/JAKO200463369807055.pdf", "academic", published="2004",
      note="음반·온라인 음악 시장 규모 수치"),
    S("mus-wk-soribada", "[특집] 소리바다는 독인가, 약인가", "주간경향",
      "https://weekly.khan.co.kr/article/10360", "news"),
    S("mus-seoul-020713", "소리바다 판결 의미·파장", "서울신문",
      "https://m.seoul.co.kr/news/2002/07/13/20020713022004", "news", published="2002-07-13"),
    S("mus-amj-melon", "MelOn 사례 연구", "Asia Marketing Journal(한국마케팅학회)",
      "https://amj.kma.re.kr/journal/vol8/iss3/7", "academic", published="2006"),
    S("mus-tenasia-melon", "멜론 10주년 — 10년간 이용 현황", "텐아시아",
      "https://www.tenasia.co.kr/article/2014112825024", "news", published="2014-11-28"),
    S("mus-segye-melon", "멜론 20년 — 음악을 듣고, 보는 플랫폼", "세계일보",
      "https://www.segye.com/newsView/20231010518342", "news", published="2023-10-10"),
    S("mus-tomato-230130", "유튜브와 격차 더 벌어진 멜론 (2022 음악 이용자 실태조사)", "뉴스토마토",
      "https://www.newstomato.com/ReadNews.aspx?no=1174352", "news", published="2023-01-30",
      origin="한국콘텐츠진흥원 음악 이용자 실태조사"),
    S("mus-pressian-211228", "콘진원 만화웹툰·애니·캐릭터·음악 이용자 실태조사(2021)", "프레시안",
      "https://pressian.com/pages/articles/2021122812061890109", "news", published="2021-12-28",
      origin="한국콘텐츠진흥원 음악 이용자 실태조사"),
    S("mus-ladykhan-251224", "콘진원 설문, 국내 이용률 1위 음원 플랫폼은 (2025 음악산업백서)", "레이디경향",
      "https://lady.khan.co.kr/culture/article/202512240950001", "news", published="2025-12-24",
      origin="한국콘텐츠진흥원 음악산업백서"),
    S("mus-busan-noraebang", "[노래방 변천사] 전 국민 '나가수' 만들어 준 '한 평 반 무대'", "부산일보",
      "https://www.busan.com/view/busan/view.php?code=20190528000121", "news", published="2019-05-28"),
    S("mus-hk-noraebang", "국내 노래방의 역사는 부산의 한 오락실에서 시작됐다", "한국경제",
      "https://www.hankyung.com/amp/2019032724921", "news", published="2019-03-27"),
    S("mus-ytn-noraebang", "노래방 2011년 정점 뒤 감소 (KB금융지주 경영연구소 분석)", "YTN",
      "https://www.ytn.co.kr/_ln/0103_201907282200278282", "news", published="2019-07-28"),

    # ── 쇼핑·결제 ──
    S("shop-hk-emart", "이마트 1호점 창동점 1993년 11월 12일 개점", "한국경제",
      "https://www.hankyung.com/amp/201911030638g", "news", published="2019-11-03"),
    S("shop-seoul-961009", "킴스클럽·뉴마트·E마트·프라이스클럽 — 창고형 할인점 급속 확산", "서울신문",
      "https://m.seoul.co.kr/news/1996/10/09/19961009031001", "news", published="1996-10-09"),
    S("shop-ks-discount", "국내 할인점 발전 단계(도입기 1993~96, 성장기 1997~99)", "KoreaScience 수록 논문",
      "https://koreascience.kr/article/JAKO200420152774368.pdf", "academic", published="2004"),
    S("shop-etnews-050729", "TV홈쇼핑 10년", "전자신문",
      "https://m.etnews.com/200507290054", "news", published="2005-07-29"),
    S("shop-etnews-150811", "홈쇼핑 20년 — 1995년 첫 방송, 14조 원 규모로", "전자신문",
      "https://m.etnews.com/20150811000194", "news", published="2015-08-11"),
    S("shop-seoulgov-160405", "온라인 쇼핑 시 PC보다 모바일 선호 (서울시 모바일 쇼핑 이용실태 조사)", "서울특별시",
      "https://news.seoul.go.kr/economy/?p=63737", "government", published="2016-04-05"),
    S("shop-etnews-160202", "작년 소매판매·온라인쇼핑·모바일쇼핑 사상 최대치", "전자신문",
      "https://m.etnews.com/20160202000244", "news", published="2016-02-02", origin="통계청 온라인쇼핑 동향"),
    S("shop-kbm-170307", "모바일쇼핑 비중 역대 최고", "경북매일",
      "https://kbmaeil.com/article/201703070186371", "news", published="2017-03-07", origin="통계청 온라인쇼핑 동향"),

    # ── 관계·모임 ──
    S("rel-wk-130225", "[특집 | 디지털 기억] 온라인 서비스 판도 변화, 빨라도 너~무 빨라", "주간경향",
      "https://weekly.khan.co.kr/article/201302251623081", "news", published="2013-02-25"),
    S("rel-seoul-950420", "컴퓨터통신망 동호회가 멀티미디어시대를 앞당긴다", "서울신문",
      "https://www.seoul.co.kr/news/1995/04/20/19950420012002", "news", published="1995-04-20"),
    S("rel-segye-220306", "PC통신 시절의 기억 — 유니텔 서비스 종료", "세계일보",
      "https://www.segye.com/newsView/20220306509477", "news", published="2022-03-06"),
    S("rel-kakao-cafe-2009", "다음 카페, 오픈 10주년 맞아 '카페 더넥스트'로 전면 개편", "다음커뮤니케이션(카카오)",
      "https://www.kakaocorp.com/page/detail/6292", "company", published="2009-06-04"),
    S("rel-kakao-cafe-2019", "스무살 된 다음카페", "카카오",
      "https://www.kakaocorp.com/page/detail/8695", "company", published="2019-05-30"),
    S("rel-etnews-130313", "카페와 블로그 — 1999년은 인터넷 커뮤니티 원년", "전자신문",
      "https://m.etnews.com/201303130176", "news", published="2013-03-13"),
    S("rel-kakao-openchat", "카카오톡 오픈채팅 (2015년 8월 출시, 2023년 5월 3탭 개편)", "카카오",
      "https://www.kakaocorp.com/page/detail/10811", "company", published="2024-01-09"),
    S("rel-kakao-voiceroom", "카카오톡 오픈채팅에 음성 대화 기능 '보이스룸'", "카카오",
      "https://www.kakaocorp.com/page/detail/9696", "company", published="2022-04-05"),
    S("rel-byline-250318", "어느덧 15살…카카오톡", "바이라인네트워크",
      "https://byline.network/2025/03/18-413/", "news", published="2025-03-18"),
    S("rel-asiae-221104", "사는 동네 기반, 데이트보다 취미 공유 플랫폼이 인기 (NHN데이터 앱 트렌드)", "아시아경제",
      "https://view.asiae.co.kr/article/2022110409162146453", "news", published="2022-11-04",
      origin="NHN데이터 2022 하반기 앱 트렌드 리포트"),
    S("rel-hk-220919", "MZ저격 커뮤니티 '문토' 이미리 대표", "한국경제",
      "https://www.hankyung.com/amp/202209190713i", "news", published="2022-09-19"),
    S("rel-fn-250224", "국민 삶의 질 2024 — 사회단체 참여율", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202502241823220512", "news", published="2025-02-24", origin="통계청 국민 삶의 질 보고서"),
    S("rel-newsis-250224", "코로나19 극복 아직… [삶의 질 2024]", "뉴시스",
      "https://mobile.newsis.com/view/NISX20250224_0003075845", "news", published="2025-02-24", origin="통계청 국민 삶의 질 보고서"),
    S("rel-fn-260305", "국민 삶의 질 2025 — 사회단체 참여율 52.3%", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202603051815055950", "news", published="2026-03-05", origin="통계청 국민 삶의 질 보고서"),

    # ── 자기표현 ──
    S("expr-arch-uniform", "교복 이야기 — 교복 자율화와 다시 교복으로", "국가기록원",
      "https://theme.archives.go.kr/next/koreaOfRecord/schoolUniform.do", "government"),
    S("expr-aks-uniform", "교복·두발 자율화 조치", "한국민족문화대백과사전(한국학중앙연구원)",
      "https://encykorea.aks.ac.kr/Article/E0076165", "reference"),
    S("expr-herald-250925", "문신사법, 국회 본회의 통과…비의료인 문신 시술 합법화", "헤럴드경제",
      "https://www.heraldk.com/article/2025092501185919992", "news", published="2025-09-25"),
    S("expr-medigate-250925", "'문신사법' 국회 본회의 통과…비의료인 문신 시술 가능해져", "메디게이트뉴스",
      "https://medigatenews.com/news/2465570495", "news", published="2025-09-25"),
    S("expr-tf-250828", "의사 아니어도 문신 시술 합법화 눈앞 (복지부 문신 시술 이용자 현황 조사 인용)", "더팩트",
      "https://news.tf.co.kr/read/life/2238310.htm", "news", published="2025-08-28"),
]


CLAIMS = [
    # ── 산업·일자리 (지표에서 계산) ──
    C("fl-jobs-status",
      "통계청 종사상 지위별 취업자로 계산하면 임금근로자 비중은 1963년 31.5%에서 1990년 60.6%, 2025년 77.6%가 되었고, 무급가족종사자는 같은 기간 31.2%에서 2.9%로 줄었다.",
      "statistical", "sourced", ["kosis-status"], ["labor", "economy"], period="1963~2025",
      scope="취업자 전체 중 비중. 정규·비정규 구분은 이 통계로 알 수 없다(상용근로자 구분은 1989년부터).",
      support="KOSIS DT_1DA7010S 연간 값을 사이트가 비중으로 계산"),
    C("fl-jobs-va",
      "세계은행 자료로 보면 농림어업이 GDP에서 차지하는 비중은 1963년 42.9%에서 1990년 7.4%, 2024년 1.5%로 줄었고, 제조업 비중은 같은 기간 12.8%에서 25.2%, 26.6%로 커졌다.",
      "statistical", "sourced", ["wb-kr-va-agr", "wb-kr-va-mfg"], ["economy", "industry"], period="1963~2024",
      scope="생산(부가가치) 비중이며 일자리 비중과 다르다.", support="WDI NV.AGR.TOTL.ZS, NV.IND.MANF.ZS"),
    C("fl-jobs-emp",
      "취업자 중 농림어업 비중은 1983년 29.8%에서 2024년 5.2%로, 제조업 비중은 1990년 27.2%에서 2024년 15.6%로 줄었고, 서비스업 비중은 1983년 41.1%에서 2024년 71.1%로 늘었다.",
      "statistical", "sourced", ["fred-kr-emp-ag", "fred-kr-emp-mfg", "fred-kr-emp-svc", "fred-kr-emp-all"], ["labor"],
      period="1983~2024", scope="1983년 이전 산업별 취업자 연속 자료는 확보하지 못했다. 제조업은 1990년부터.",
      support="OECD(FRED) 산업별 취업자 ÷ 전체 취업자"),
    C("fl-jobs-exports",
      "상품 수출액은 1963년 약 0.9억 달러, 1970년 8.3억 달러, 1980년 174.8억 달러, 2025년 7,111억 달러였다.",
      "statistical", "sourced", ["fred-kr-exports"], ["economy", "industry"], period="1963~2025",
      scope="명목 달러 금액이라 물가·환율 변화가 섞여 있다.", support="OECD(FRED) XTEXVA01KRA667S"),

    C("fl-jobs-1987-irregular",
      "경상대 김공회 교수는 1987년 7~9월 투쟁으로 노조가 생기고 임금이 크게 오르자 노동자 한 명을 뽑는 비용이 커져 기업이 비정규직 채용을 선호하게 됐다고 보며, 비정규직의 본격 확산은 1997년 외환위기 이후라고 지적했다.",
      "interpretation", "sourced", ["kr-khan-1987labor"], ["labor"], period="1987~1997",
      scope="연구자 한 명의 해석을 기사가 옮긴 것이다."),

    # ── 음악 ──
    C("fl-mus-musicroom",
      "1960년대 서울에는 쎄시봉 외에도 뉴월드·아카데미·카네기·르네상스 같은 음악 감상실이 여럿 문을 열었고, 인기 DJ와 신곡 확보가 경쟁 요소였다.",
      "fact", "sourced", ["mus-themusical-sesibong"], ["culture"], period="1960년대",
      scope="서울 도심의 사례. 지방·농촌의 음악 이용은 이 자료로 알 수 없다."),
    C("fl-mus-dabang",
      "서울시는 음악다방을 1970년대 문화를 대표하는 상징의 하나로 소개한다. 당시 매니저들은 새 앨범이 나오면 전국 음악다방 DJ를 찾아다니며 홍보를 부탁했고, 1980년대~1990년대 초에는 DJ 연합회 차트가 가요계에 영향력을 가졌다는 회고가 있다.",
      "fact", "verified", ["mus-seoul-mediahub", "mus-skhan-2012-dj"], ["culture"], period="1970년대~1990년대 초",
      scope="'홍보 창구' 역할은 당사자 회고(스포츠경향)에 근거한다. 이용자 수 통계는 없다.",
      support="서울시: '1970년대 문화를 대표하는 상징 중 하나인 음악다방' / 스포츠경향: 김정호 매니저 회고"),
    C("fl-mus-1995",
      "1995년 김건모 3집은 발매 두 달 만에 230만 장이 팔렸고 5월에는 250만 장을 향했다. 같은 시기 신문은 댄스 음반만 100만 장을 넘기고 발라드·록 음반은 20만 장도 넘기기 어렵다고 썼다.",
      "statistical", "verified", ["mus-seoul-950327", "mus-seoul-950508"], ["culture"], period="1995",
      scope="당시 기사에 실린 판매 추정치이며 공식 집계가 아니다. 최종 판매량은 자료마다 280만~330만 장으로 다르다.",
      support="서울신문 1995.3.27 제목·본문, 1995.5.8 본문"),
    C("fl-mus-street",
      "1995년 기사는 '잘못된 만남'이 레코드 가게와 테이프를 파는 리어카에서 종일 흘러나왔다고 전한다 — 음반 매장과 길거리 테이프 판매가 음악이 퍼지는 통로였다.",
      "fact", "sourced", ["mus-seoul-950327"], ["culture", "consumption"], period="1995",
      scope="한 기사의 묘사다. 길거리 복제 테이프 판매 규모 통계는 확보하지 못했다."),
    C("fl-mus-noraebang",
      "번호를 누르면 반주가 나오는 한국식 노래방은 1991년 4월 부산 동아대 앞 오락실에서 시작됐다고 업계는 본다. 이듬해 등록 업소가 1만 곳을 넘었고 1996년에는 3만 5천 곳을 넘었다.",
      "fact", "verified", ["mus-hk-noraebang", "mus-busan-noraebang"], ["culture"], period="1991~1996",
      scope="'최초'는 업계 통설이며 공식 기록은 없다. 업소 수는 부산일보 기사 수치."),
    C("fl-mus-noraebang-peak",
      "노래방 수의 정점은 자료에 따라 다르다. 부산일보는 2005년 3만 7,568곳을, KB금융지주 경영연구소(YTN 보도)는 2011년 약 3만 5천 곳을 정점으로 본다. 연구소는 이후 감소의 이유로 회식 문화 변화와 대체 시설 증가를 꼽았다.",
      "statistical", "verified", ["mus-busan-noraebang", "mus-ytn-noraebang"], ["culture", "consumption"], period="2005~2018",
      scope="두 출처의 정점 연도가 서로 다르다. 감소 이유는 분석(해석)이다."),
    C("fl-mus-cd-crash",
      "국내 음반 시장은 2000년 약 4,100억 원에서 2002년 2,861억 원, 2003년 1,833억 원으로 줄었고, 유·무선 온라인 음악 시장은 2003년 1,850억 원으로 음반 시장을 앞질렀다. 이 중 벨소리·통화연결음이 1,767억 원이었다.",
      "statistical", "sourced", ["mus-dc-2004"], ["culture", "industry"], period="2000~2003",
      scope="벨소리·통화연결음이 온라인 음악의 대부분이라, '음악을 듣는 방식'이 바로 온라인으로 옮겨 갔다고 보기는 어렵다.",
      support="본문 첫 단락의 시장 규모 수치"),
    C("fl-mus-soribada",
      "P2P 음악 파일 공유 서비스 소리바다는 2000년 5월 시작했고, 2002년 7월 법원의 서비스 중지 가처분 결정으로 서비스를 멈췄다가 방식을 바꿔 재개했다.",
      "fact", "verified", ["mus-wk-soribada", "mus-seoul-020713"], ["culture", "technology"], period="2000~2002"),
    C("fl-mus-soribada-cause",
      "음반업계는 소리바다 같은 무료 파일 공유가 음반 매출 급감의 원인이라고 주장했다. 다만 같은 시기 온라인 음악 매출의 대부분이 벨소리였고, 음반 감소의 원인별 크기를 나눈 자료는 확보하지 못했다.",
      "interpretation", "sourced", ["mus-wk-soribada", "mus-dc-2004"], ["culture"], period="2000~2004",
      scope="원인에 대한 이해당사자 주장과 사이트의 판단을 구분해 적었다."),
    C("fl-mus-melon",
      "SK텔레콤은 2004년 11월 16일 유·무선 연동 정액제 음악 서비스 멜론을 내놓았다. 멜론은 2009년 국내 처음으로 스마트폰 스트리밍을 시작했고, 2014년 회원 2,500만 명을 밝혔다.",
      "fact", "verified", ["mus-amj-melon", "mus-tenasia-melon", "mus-segye-melon"], ["culture", "technology"], period="2004~2014",
      scope="회원 수는 회사 발표. 유료 이용자 수와 다르다."),
    C("fl-mus-video",
      "한국콘텐츠진흥원 조사(전국 10~69세 3,200명, 온라인)에서 음악을 들을 때 '음악 동영상 사이트'를 쓴다는 응답은 2021년 81%로 2019년보다 34.2%p 늘었다. 10대(88.5%)와 20대(86.6%)가 높았지만 모든 연령대가 75%를 넘었다.",
      "statistical", "sourced", ["mus-pressian-211228"], ["culture"], period="2019~2021",
      scope="온라인 조사라 인터넷 이용자 위주다. 2020~2021년 코로나19 시기가 겹친다."),
    C("fl-mus-platform",
      "콘진원 조사에서 주로 쓰는 음악 서비스는 2022년 멜론 32.8%, 유튜브 28.7%, 유튜브 뮤직 9.8%였다. 2025 음악산업백서에서는 유튜브 뮤직 37.6%, 멜론 31.7%였는데, 이 해부터 유튜브와 유튜브 뮤직을 한 항목으로 묶어 조사해 앞 해와 그대로 비교하기 어렵다.",
      "statistical", "sourced", ["mus-tomato-230130", "mus-ladykhan-251224"], ["culture"], period="2022~2025",
      scope="두 기사 모두 같은 기관(콘진원)의 조사를 옮긴 것이라 독립 출처 2곳으로 세지 않는다. 조사 항목이 바뀌었다."),

    # ── 쇼핑·결제 ──
    C("fl-shop-emart",
      "신세계는 1993년 11월 12일 서울 창동에 국내 첫 창고형 할인점 이마트를 열었다. 1996년 10월 기사는 그 뒤 대형 할인점이 30여 곳으로 늘었다고 전한다.",
      "fact", "verified", ["shop-hk-emart", "shop-seoul-961009"], ["consumption", "industry"], period="1993~1996"),
    C("fl-shop-discount-stage",
      "한 연구는 할인점 도입기를 1993~1996년으로 나누고, 1994년 창고형 회원제 매장의 개장과 1996년 유통시장 개방을 정착의 계기로 본다. 1997~1999년은 업체마다 점포를 크게 늘리고 외국계와 경쟁한 성장기다.",
      "interpretation", "sourced", ["shop-ks-discount"], ["consumption"], period="1993~1999"),
    C("fl-shop-homeshop",
      "케이블TV 홈쇼핑은 1995년 8월 1일 39쇼핑의 4시간 시험 판매방송으로 시작했다. 두 회사를 합친 취급고는 1995년 34억 원, 1996년 335억 원이었고 2011년 10조 원, 2014년 14조 원을 넘었다.",
      "statistical", "verified", ["shop-etnews-050729", "shop-etnews-150811"], ["consumption", "industry"], period="1995~2014",
      scope="두 출처 모두 전자신문 기사라 발행처는 같지만, 다른 해(2005·2015)에 다른 취재로 쓴 기사다."),
    C("fl-shop-mobile",
      "통계청 집계로 모바일쇼핑 거래액은 2013년 6조 5,600억 원에서 2015년 24조 4,270억 원으로 늘어 온라인쇼핑의 45.3%가 되었다. 월별 비중은 2015년 11월 처음 50%에 이르렀다.",
      "statistical", "sourced", ["shop-seoulgov-160405", "shop-etnews-160202", "shop-kbm-170307"], ["consumption", "technology"],
      period="2013~2015", scope="세 출처 모두 통계청 같은 원자료를 옮긴 것이다."),
    C("fl-shop-mobile-why",
      "서울시 전자상거래센터는 모바일쇼핑이 커진 이유로 모든 연령층의 스마트폰 이용 보편화와 화면 대형화, 2015년부터 앱카드·네이버페이·페이코·SSG페이 등 간편결제의 경쟁적 도입을 들었다.",
      "interpretation", "sourced", ["shop-seoulgov-160405"], ["consumption", "technology"], period="2015",
      scope="기관 관계자의 설명이며 요인별 효과 크기는 측정되지 않았다."),
    C("fl-shop-survey-2015",
      "서울시 조사(4,000명)에서 인터넷 쇼핑 때 모바일 기기를 쓰는 비중은 2014년 42.3%에서 2015년 50.3%로 PC(49.7%)를 넘었다.",
      "statistical", "sourced", ["shop-seoulgov-160405"], ["consumption"], period="2014~2015",
      scope="서울 거주자 대상 조사다."),

    # ── 관계·모임 ──
    C("fl-rel-pctong",
      "PC통신은 1986년 천리안이 등장해 1988년 유료 가입자를 받으며 게시판·채팅·자료실을 시작했고, 하이텔(1992)·나우누리(1994)·유니텔(1996)이 뒤따르며 1990년대에 전성기를 누렸다.",
      "fact", "verified", ["rel-wk-130225", "rel-segye-220306"], ["technology", "society"], period="1986~1990년대"),
    C("fl-rel-club-1995",
      "1995년 기사는 하이텔·천리안·나우누리 등에서 수천 개의 동호회가 활동하고, 연령에 제한 없이 활동할 수 있는 동호회가 프로그래머 같은 전문가를 배출한다고 전했다.",
      "fact", "sourced", ["rel-seoul-950420"], ["society", "technology"], period="1995",
      scope="동호회 수는 기사 표현('수천 개')이며 정확한 집계가 아니다."),
    C("fl-rel-pctong-cost",
      "당시 PC통신은 모뎀 이용료를 합쳐 월 5만~6만 원이 들었다는 회고가 있고, 1990년대 후반 초고속 인터넷과 포털이 등장하면서 급격히 위축되었다.",
      "fact", "verified", ["rel-segye-220306", "rel-wk-130225"], ["technology"], period="1990년대",
      scope="비용은 회고 기사 수치. 이용자의 연령·소득 분포 자료는 확보하지 못했다."),
    C("fl-rel-cafe",
      "다음 카페는 1999년 5월 문을 열어 10년 동안 770만 개의 카페가 만들어지고 3,800만 회원이 가입했다고 회사가 밝혔다. 1999년에는 세이클럽·디시인사이드도 등장했다.",
      "fact", "verified", ["rel-kakao-cafe-2009", "rel-etnews-130313"], ["society", "technology"], period="1999~2009",
      scope="카페·회원 수는 회사 발표이며 중복 가입·휴면 회원이 포함된다."),
    C("fl-rel-cafe-fandom",
      "카카오는 2019년 다음 카페 월간 이용자가 2,500만 명이고, 한류 스타의 공식 팬카페 491개가 모여 있다고 밝혔다.",
      "statistical", "sourced", ["rel-kakao-cafe-2019"], ["society", "culture"], period="2019",
      scope="회사 발표 수치."),
    C("fl-rel-openchat",
      "카카오톡은 2015년 8월 '오픈채팅'을 내놓았다. 전화번호를 몰라도 링크나 검색으로 들어가 채팅방마다 다른 프로필로 대화할 수 있는, 관심사 중심의 비지인 대화 기능이다. 2023년 5월에는 별도 탭으로 승격되었다.",
      "fact", "verified", ["rel-kakao-openchat", "rel-kakao-voiceroom"], ["society", "technology"], period="2015~2023",
      scope="두 출처 모두 카카오 자료다(회사 설명). 오픈채팅 이용자 수는 공개 자료를 찾지 못했다."),
    C("fl-rel-kakao-mau",
      "카카오톡의 국내 월간 이용자는 2024년 12월 약 4,900만 명으로 인구의 94% 수준이다.",
      "statistical", "sourced", ["rel-byline-250318"], ["technology"], period="2024"),
    C("fl-rel-apps",
      "NHN데이터가 안드로이드 이용자 약 2,800만 명의 앱 설치 자료를 분석한 결과, 2022년 하반기 관심사 기반 모임 앱 '문토'의 설치 수가 5월 대비 102.2% 늘었고 모임 앱 설치자의 77%가 20~30대였다.",
      "statistical", "sourced", ["rel-asiae-221104"], ["society", "technology"], period="2022",
      scope="'설치' 자료라 실제 모임 참여나 이용 빈도를 뜻하지 않는다. 아이폰 이용자는 빠져 있다."),
    C("fl-rel-orgrate",
      "통계청 '국민 삶의 질' 보고서의 사회단체 참여율(동호회·동창회·시민단체·지역모임 등 포함)은 2019년 51.8%에서 코로나19 첫해인 2020년 46.4%로 떨어졌다가 2023년 58.2%로 높아졌고, 2024년에는 52.3%로 다시 낮아졌다. 통계청은 2023년 증가에 동창회·동호회 모임이 많이 늘어난 영향이 컸다고 설명했다.",
      "statistical", "sourced", ["rel-fn-250224", "rel-newsis-250224", "rel-fn-260305"], ["society"], period="2019~2024",
      scope="세 기사 모두 통계청 같은 보고서를 옮긴 것이다. 모임의 규모(대규모·소규모)는 이 지표로 구분되지 않는다."),

    # ── 자기표현 ──
    C("fl-expr-uniform",
      "정부는 1982년 1월 중·고등학생 머리 모양과 교복 자율화를 발표했다. 두발은 1982년부터, 교복은 1983년 신입생부터 자유복이 허용되어 1898년 이후 85년 만에 교복 의무가 풀렸다.",
      "fact", "verified", ["expr-arch-uniform", "expr-aks-uniform"], ["society", "politics"], period="1982~1983",
      scope="발표일은 출처에 따라 1월 2일(국가기록원)과 1월 4일(한국민족문화대백과)로 다르다."),
    C("fl-expr-uniform-back",
      "자유복의 가계 부담, 빈부 격차로 인한 위화감, 교외 생활지도의 어려움이 제기되면서 1986년 2학기부터 교복 착용 여부가 학교장 판단에 맡겨졌고, 이후 교복으로 돌아가는 학교가 늘었다.",
      "fact", "verified", ["expr-arch-uniform", "expr-aks-uniform"], ["society"], period="1986~"),
    C("fl-expr-tattoo-law",
      "국회는 2025년 9월 25일 문신사법을 통과시켰다(재석 202명 중 찬성 195명). 1992년 대법원이 문신을 의료행위로 본 뒤 비의료인의 문신 시술은 처벌 대상이었는데, 국가시험에 합격한 문신사의 시술을 허용했다. 시행은 공포 2년 뒤다.",
      "fact", "verified", ["expr-herald-250925", "expr-medigate-250925"], ["society", "politics"], period="1992~2025"),
    C("fl-expr-tattoo-survey",
      "보건복지부의 2024년 문신 시술 이용자 조사(1,685명)에서 시술 장소는 문신 전문숍이 81.0%, 병·의원이 1.4%였고, 54.2%가 비의료인 시술 허용에 찬성했다. 찬성 이유로는 '대부분 비의료인이 시술하고 있어 제도화로 관리해야 한다'(52.4%)가 가장 많았다.",
      "statistical", "sourced", ["expr-tf-250828"], ["society"], period="2024",
      scope="문신·반영구화장 이용자만 대상으로 한 조사라 국민 전체의 인식을 대표하지 않는다."),
]


# ─────────────────────────────────────────────────────────────
# 변화 흐름
#   phase: before 변화 이전 / condition 조건과 배경 / turn 전환점 / spread 확산과 참여 집단
#          life 행동·생활의 변화 / cross 다른 분야로 / now 지금 이어지는 것·달라진 것
#   nodeIds: 지도(그래프)의 사건 노드 — 사건 상세로 이어진다
# ─────────────────────────────────────────────────────────────
FLOWS = [
    {
        "id": "flow-jobs",
        "question": "한국의 산업과 일자리는 어떻게 바뀌었나?",
        "cats": ["industry", "economy"],
        "span": [1962, 2025],
        "shape": "교체 — 농업 중심에서 제조업, 다시 서비스업 중심으로. 다만 일하는 방식(임금근로·비정규·플랫폼)은 단계마다 갈라졌다.",
        "lede": ["fl-jobs-va", "fl-jobs-status"],
        "indicators": ["empstatus-mix-kr", "va-mfg-kr"],
        "steps": [
            {"id": "j1", "phase": "before", "period": "1960년대 초", "title": "농업과 가족 노동이 일의 중심",
             "claimIds": ["fl-jobs-va", "fl-jobs-status"], "nodeIds": []},
            {"id": "j2", "phase": "condition", "period": "1962~1971", "title": "계획에 따른 공업화와 저임금 노동",
             "claimIds": ["c60-kr-ulsan-1", "cfill-plan2", "c60-kr-labor-1"], "nodeIds": ["e60-plan", "e60-plan2"]},
            {"id": "j3", "phase": "turn", "period": "1973", "title": "중화학공업화 선언",
             "claimIds": ["c70-kr-hci", "c70-hci-why"], "nodeIds": ["e70-hci", "d-hci-why"]},
            {"id": "j4", "phase": "spread", "period": "1970년대 후반", "title": "중동 건설 — 일자리가 국경을 넘다",
             "claimIds": ["c70-kr-mideast"], "nodeIds": []},
            {"id": "j5", "phase": "turn", "period": "1983", "title": "반도체 — 다음 주력 산업의 진입",
             "claimIds": ["c80-64k"], "nodeIds": ["e80-64k"]},
            {"id": "j6", "phase": "life", "period": "1987", "title": "노동자 대투쟁과 노조 결성",
             "claimIds": ["c80-labor", "c80-labor-unions", "c80-labor-num"], "nodeIds": ["e80-629"]},
            {"id": "j7", "phase": "spread", "period": "1983~2024", "title": "서비스업으로 옮겨 간 일자리",
             "claimIds": ["fl-jobs-emp"], "nodeIds": []},
            {"id": "j8", "phase": "turn", "period": "1997~2004", "title": "외환위기 구조조정과 비정규직 확대",
             "claimIds": ["c90-ch-1998", "c00-irregular"], "nodeIds": ["e90-imf"]},
            {"id": "j9", "phase": "life", "period": "2013~", "title": "앱으로 연결되는 일 — 배달 라이더",
             "claimIds": ["c10-delivery", "c10-rider-risk"], "nodeIds": []},
            {"id": "j10", "phase": "now", "period": "2013~2025", "title": "전문직 비중의 증가와 AI",
             "claimIds": ["c20-hyp-ai-jobs", "fl-jobs-exports"], "nodeIds": []},
        ],
        "links": [
            {"from": "j1", "to": "j2", "kind": "sequence", "note": "농업 비중이 줄어든 것과 공업화 계획은 같은 시기에 진행됐다. 두 흐름의 인과 크기를 나눈 자료는 여기 없다.", "claimIds": []},
            {"from": "j2", "to": "j3", "kind": "condition", "note": "제2차 계획이 이미 중화학공업으로 옮겨 가는 방향을 내세웠고, 선언의 배경으로 무역적자·부품 수입 의존·안보 위기가 꼽힌다.", "claimIds": ["cfill-plan2", "c70-hci-why"]},
            {"from": "j3", "to": "j5", "kind": "interpretation", "note": "중화학·전자 산업 기반이 반도체 진입의 바탕이 됐다는 해석이 있지만, 64K D램 개발과의 직접 연결을 보여주는 자료는 여기 없다.", "claimIds": []},
            {"from": "j3", "to": "j6", "kind": "condition", "note": "대규모 공장 노동자가 늘어난 것이 1987년 대기업 노조 결성의 조건이었다. 직접 계기는 6·29선언 이후의 통제 이완이다.", "claimIds": ["c80-labor"]},
            {"from": "j6", "to": "j8", "kind": "interpretation", "note": "1987년 이후 정규직 채용 비용이 커지자 기업이 비정규직을 선호했다는 연구자 해석이 있다. 본격 확산은 외환위기 이후다.", "claimIds": ["fl-jobs-1987-irregular"]},
            {"from": "j8", "to": "j9", "kind": "sequence", "note": "비정규·특수고용 형태가 늘어난 뒤 플랫폼 노동이 등장했다. 두 현상을 잇는 인과 자료는 확보하지 못했다.", "claimIds": []},
            {"from": "j7", "to": "j10", "kind": "correlation", "note": "서비스업 비중과 전문직 비중이 함께 늘었다. 같은 원인(산업 구조 변화)의 결과일 수 있다.", "claimIds": ["fl-jobs-emp", "c20-hyp-ai-jobs"]},
        ],
        "cross": [
            {"flow": "flow-shop", "note": "임금근로자가 늘고 가계 소득이 화폐 소득이 되면서 소비 방식도 달라졌다(연결은 해석)."},
            {"flow": "flow-relations", "note": "직장이 관계의 중심이던 시기와, 관심사 중심 모임이 늘어난 시기를 비교해 볼 수 있다."},
        ],
        "gaps": [
            "1983년 이전 산업별 취업자 연속 통계(통계청 KOSIS도 1983년부터).",
            "1960~70년대 여성 공장 노동(섬유·가발·전자 조립)의 규모를 보여주는 통계.",
            "자영업자 감소가 어떤 업종에서 일어났는지 — 업종별 자영업 통계는 아직 연결하지 않았다.",
            "생성형 AI가 직업 구성에 미친 영향은 아직 통계로 구분할 수 없다.",
        ],
        "alternatives": [
            "고도성장을 정부 계획의 성과로 보는 설명과, 냉전·베트남전 특수·저임금 노동 같은 외부·구조 조건을 더 중시하는 설명이 있다.",
        ],
    },
    {
        "id": "flow-music",
        "question": "음악을 듣고 발견하는 방식은 어떻게 달라졌나?",
        "cats": ["culture", "industry"],
        "span": [1960, 2025],
        "shape": "교체와 공존 — 새 매체가 오면 옛 매체가 줄었지만, 노래방·통기타·LP처럼 형태를 바꿔 다시 나타난 것도 있다.",
        "lede": ["fl-mus-dabang", "fl-mus-video"],
        "indicators": ["album-kr"],
        "steps": [
            {"id": "m1", "phase": "before", "period": "1960년대", "title": "라디오와 도심 음악 감상실",
             "claimIds": ["c60-kr-radio-3", "fl-mus-musicroom", "c60-sesibong"], "nodeIds": ["d-sesibong"]},
            {"id": "m2", "phase": "condition", "period": "1970년대", "title": "음악다방 DJ와 라디오·TV 보급",
             "claimIds": ["fl-mus-dabang", "c70-culture-why"], "nodeIds": ["d-culture-cond"]},
            {"id": "m3", "phase": "turn", "period": "1991~1996", "title": "노래방 — 듣는 음악에서 부르는 음악으로",
             "claimIds": ["fl-mus-noraebang"], "nodeIds": []},
            {"id": "m4", "phase": "spread", "period": "1995", "title": "음반 판매의 정점과 쏠림",
             "claimIds": ["fl-mus-1995", "fl-mus-street"], "nodeIds": []},
            {"id": "m5", "phase": "turn", "period": "2000~2003", "title": "MP3·파일 공유와 음반 시장의 축소",
             "claimIds": ["fl-mus-soribada", "fl-mus-cd-crash", "fl-mus-soribada-cause"], "nodeIds": []},
            {"id": "m6", "phase": "turn", "period": "2004~2009", "title": "정액제 스트리밍과 휴대전화",
             "claimIds": ["fl-mus-melon"], "nodeIds": []},
            {"id": "m7", "phase": "life", "period": "2010~2011", "title": "옛 음악의 재등장",
             "claimIds": ["c10-sesibong", "c10-analog"], "nodeIds": ["d-sesibong-revival"]},
            {"id": "m8", "phase": "now", "period": "2019~2025", "title": "동영상 플랫폼에서 듣고 발견하기",
             "claimIds": ["fl-mus-video", "fl-mus-platform"], "nodeIds": []},
            {"id": "m9", "phase": "cross", "period": "2005~2018", "title": "노래방의 정점과 감소",
             "claimIds": ["fl-mus-noraebang-peak"], "nodeIds": []},
        ],
        "links": [
            {"from": "m1", "to": "m2", "kind": "condition", "note": "라디오·TV 보급과 도시로 모인 청년층이 음악다방 문화가 커진 조건으로 꼽힌다.", "claimIds": ["c70-culture-why"]},
            {"from": "m2", "to": "m4", "kind": "sequence", "note": "음악다방 DJ 차트의 영향력이 줄어든 시기와 TV 가요 순위·음반 판매가 커진 시기가 겹친다. 둘 사이의 인과 자료는 없다.", "claimIds": []},
            {"from": "m4", "to": "m5", "kind": "sequence", "note": "1995년 정점 이후 2000년대 초에 음반 시장이 급감했다.", "claimIds": ["fl-mus-cd-crash"]},
            {"from": "m5", "to": "m6", "kind": "causal", "note": "소송과 저작권 분쟁 끝에 무료 공유 서비스가 유료화되고, 통신사가 정액제 서비스를 내놓았다(소리바다·벅스 유료화, 멜론 출시).", "claimIds": ["fl-mus-soribada", "fl-mus-melon"]},
            {"from": "m6", "to": "m8", "kind": "sequence", "note": "스트리밍 정액제가 자리 잡은 뒤, 무료 동영상 플랫폼이 주된 듣기 경로로 떠올랐다.", "claimIds": ["fl-mus-platform"]},
            {"from": "m3", "to": "m9", "kind": "interpretation", "note": "노래방 감소의 이유로 회식 문화 변화와 대체 시설 증가가 제시됐다(연구소 분석).", "claimIds": ["fl-mus-noraebang-peak"]},
        ],
        "cross": [
            {"flow": "flow-relations", "note": "다음 카페의 팬카페(491개)처럼, 음악을 좋아하는 일은 팬 커뮤니티라는 관계 형성으로 이어졌다."},
            {"flow": "flow-shop", "note": "음악 구매도 레코드 가게·길거리 테이프에서 디지털 정액제로 옮겨 갔다."},
        ],
        "gaps": [
            "1980년대 휴대용 카세트 플레이어 보급률 — 신뢰할 수 있는 통계를 찾지 못했다.",
            "길거리 복제 테이프('길보드') 판매 규모.",
            "공연 관람률과 팬덤 소비(굿즈·앨범 다량 구매)의 장기 통계 — 실물 앨범 판매량은 2019년부터만 연결했다.",
            "지방·농촌, 고령층의 음악 이용 방식 변화.",
        ],
        "alternatives": [
            "음반 시장 축소의 원인으로 무료 파일 공유를 드는 설명(음반업계)과, 벨소리 등 모바일 부가서비스로 소비가 옮겨 간 영향을 함께 봐야 한다는 설명이 있다.",
        ],
    },
    {
        "id": "flow-shop",
        "question": "쇼핑 장소와 결제 방식은 어떻게 달라졌나?",
        "cats": ["society", "economy"],
        "span": [1993, 2020],
        "shape": "추가와 이동 — 대형마트·홈쇼핑·온라인이 차례로 더해졌고, 온라인 안에서도 PC에서 모바일로 옮겨 갔다.",
        "lede": ["fl-shop-emart", "c20-online"],
        "indicators": ["online-kr"],
        "steps": [
            {"id": "s1", "phase": "before", "period": "1993년 이전", "title": "시장·백화점·동네 가게",
             "claimIds": [], "nodeIds": [], "empty": "1993년 이전 소매 업태별 매출 비중 자료를 아직 확보하지 못했다."},
            {"id": "s2", "phase": "turn", "period": "1993~1999", "title": "대형 할인점의 등장",
             "claimIds": ["fl-shop-emart", "fl-shop-discount-stage"], "nodeIds": []},
            {"id": "s3", "phase": "turn", "period": "1995~2014", "title": "TV 홈쇼핑 — 집에서 전화로 주문",
             "claimIds": ["fl-shop-homeshop"], "nodeIds": []},
            {"id": "s4", "phase": "spread", "period": "1998~2003", "title": "신용카드 확산과 카드대란",
             "claimIds": ["c00-card", "c00-card-why"], "nodeIds": ["e00-card"]},
            {"id": "s5", "phase": "condition", "period": "2009~2010", "title": "스마트폰 보급",
             "claimIds": ["c00-kr-iphone"], "nodeIds": ["e00-kr-iphone"]},
            {"id": "s6", "phase": "turn", "period": "2013~2015", "title": "모바일쇼핑과 간편결제",
             "claimIds": ["fl-shop-mobile", "fl-shop-survey-2015", "fl-shop-mobile-why"], "nodeIds": []},
            {"id": "s7", "phase": "life", "period": "2013~2019", "title": "배달앱 — 음식도 앱으로",
             "claimIds": ["c10-delivery", "c10-syn-delivery"], "nodeIds": []},
            {"id": "s8", "phase": "now", "period": "2020", "title": "코로나19와 온라인 비중 27%",
             "claimIds": ["c20-online"], "nodeIds": []},
        ],
        "links": [
            {"from": "s2", "to": "s3", "kind": "sequence", "note": "대형마트와 홈쇼핑은 2년 차이로 등장한 별개의 새 판매 경로다.", "claimIds": []},
            {"from": "s4", "to": "s6", "kind": "condition", "note": "카드 결제가 이미 보편화된 상태가 앱카드·간편결제의 바탕이 됐다는 연결은 해석이다.", "claimIds": []},
            {"from": "s5", "to": "s6", "kind": "condition", "note": "서울시 전자상거래센터는 스마트폰 보편화와 간편결제 도입을 모바일쇼핑 증가 이유로 들었다.", "claimIds": ["fl-shop-mobile-why"]},
            {"from": "s5", "to": "s7", "kind": "condition", "note": "스마트폰 결제와 1인 가구·맞벌이 증가가 배달앱 수요를 키웠다는 분석이 있다.", "claimIds": ["c10-syn-delivery"]},
            {"from": "s6", "to": "s8", "kind": "correlation", "note": "온라인 비중은 2015년 이후 계속 커졌고 2020년 감염병 상황에서 크게 뛰었다.", "claimIds": ["c20-online"]},
        ],
        "cross": [
            {"flow": "flow-jobs", "note": "배달앱은 라이더라는 새 일자리를 만들었다."},
            {"flow": "flow-music", "note": "음악 구매도 실물에서 정액제로 같은 방향으로 움직였다."},
        ],
        "gaps": [
            "전통시장·동네 슈퍼의 매출 변화 장기 통계 — '대형마트가 전통시장을 줄였다'는 설명은 아직 근거를 연결하지 않았다.",
            "대형마트 매출과 온라인 매출이 역전된 시점(공식 통계로 확인 필요).",
            "편의점 확산(1989년 이후)과 1인 가구의 관계.",
            "연령대별 온라인 쇼핑 이용 차이.",
        ],
        "alternatives": [
            "모바일쇼핑 증가를 기술(스마트폰) 중심으로 보는 설명과, 택배망·간편결제·플랫폼 할인 경쟁 같은 공급 측 요인을 더 중시하는 설명이 있다.",
        ],
    },
    {
        "id": "flow-relations",
        "question": "사람들은 어떻게 만나고 모임을 만들게 됐나?",
        "cats": ["society", "flow"],
        "span": [1986, 2024],
        "shape": "추가와 공존 — 온라인 관심사 모임이 늘었지만, 동창회·동호회 같은 기존 모임이 사라졌다는 근거는 없다.",
        "lede": ["fl-rel-pctong", "fl-rel-orgrate"],
        "indicators": [],
        "steps": [
            {"id": "r1", "phase": "before", "period": "1980년대까지", "title": "학교·직장·지역 중심의 관계",
             "claimIds": [], "nodeIds": [], "empty": "1980년대 이전 모임 참여(계·동창회·향우회 등) 통계를 아직 확보하지 못했다. 자료가 없다는 뜻이지 그런 모임이 없었다는 뜻이 아니다."},
            {"id": "r2", "phase": "turn", "period": "1986~1990년대", "title": "PC통신 동호회 — 모르는 사람과 관심사로 모이기",
             "claimIds": ["fl-rel-pctong", "fl-rel-club-1995", "fl-rel-pctong-cost"], "nodeIds": []},
            {"id": "r3", "phase": "spread", "period": "1999~2009", "title": "인터넷 카페와 미니홈피",
             "claimIds": ["fl-rel-cafe", "c00-cyworld"], "nodeIds": ["tr-t00-minihompy"]},
            {"id": "r4", "phase": "life", "period": "2019", "title": "팬카페 — 좋아하는 것을 중심으로 한 공동체",
             "claimIds": ["fl-rel-cafe-fandom"], "nodeIds": []},
            {"id": "r5", "phase": "turn", "period": "2010~2015", "title": "메신저와 오픈채팅",
             "claimIds": ["c10-kakao", "fl-rel-openchat", "fl-rel-kakao-mau"], "nodeIds": ["e10-kakao"]},
            {"id": "r6", "phase": "spread", "period": "2022", "title": "모임 앱 — 20~30대의 관심사 모임",
             "claimIds": ["fl-rel-apps"], "nodeIds": []},
            {"id": "r7", "phase": "now", "period": "2019~2024", "title": "모임 참여율 — 코로나19 전후",
             "claimIds": ["fl-rel-orgrate", "c2020-endsd"], "nodeIds": []},
        ],
        "links": [
            {"from": "r2", "to": "r3", "kind": "sequence", "note": "PC통신 동호회 활동이 인터넷 카페로 흡수됐다는 설명(전자신문)이 있지만, 회원 이동을 보여주는 자료는 없다.", "claimIds": ["fl-rel-cafe"]},
            {"from": "r3", "to": "r5", "kind": "condition", "note": "스마트폰 보급이 PC 기반 미니홈피의 쇠퇴와 모바일 메신저 확산의 조건이었다는 해석이 있다.", "claimIds": ["c00-cy-decline", "c00-kr-iphone"]},
            {"from": "r5", "to": "r6", "kind": "sequence", "note": "오픈채팅(2015)과 모임 앱의 성장(2020년대)은 시간 순서다. 이용자가 겹치는지는 확인하지 못했다.", "claimIds": []},
            {"from": "r6", "to": "r7", "kind": "hypothesis", "note": "'큰 모임에서 작은 관심사 모임으로 옮겨 갔다'는 설명은 아직 검증되지 않았다. 통계청 참여율은 2023년 동창회·동호회 증가를 보여주며, 모임 규모는 구분하지 않는다.", "claimIds": ["fl-rel-orgrate"]},
        ],
        "cross": [
            {"flow": "flow-music", "note": "팬카페·팬덤은 음악 소비와 관계 형성이 겹치는 곳이다."},
            {"flow": "flow-expression", "note": "채팅방마다 다른 프로필(오픈채팅)은 자신을 드러내는 방식의 변화와도 이어진다."},
        ],
        "gaps": [
            "대규모 모임과 소규모 모임의 비중 변화 — 통계청 참여율은 모임 규모를 구분하지 않는다.",
            "오픈채팅·모임 앱의 실제 이용자 수와 이용 빈도(설치 수만 있음).",
            "연령·지역·성별로 관계 형성 방식이 어떻게 다른지에 대한 장기 자료.",
            "1인 가구 증가와 모임 참여의 관계 — 2010년 인구총조사 연구가 있으나 아직 연결하지 않았다.",
        ],
        "alternatives": [
            "관심사 모임의 증가를 '관계 피로'나 '외로움' 같은 하나의 동기로 설명하는 글이 많지만, 이 사이트는 근거가 확인된 요인(기술·서비스 공급·감염병 이후 회복)만 연결했다.",
        ],
    },
    {
        "id": "flow-expression",
        "question": "자기표현의 방식과 이를 받아들이는 제도는 어떻게 달라졌나?",
        "cats": ["society", "politics"],
        "span": [1973, 2025],
        "shape": "규제와 완화, 되돌림 — 단속에서 자율화로 갔다가 일부는 다시 규칙으로 돌아왔고, 현실이 먼저 바뀐 뒤 법이 따라온 경우도 있다.",
        "lede": ["c70-taboo", "fl-expr-tattoo-law"],
        "indicators": [],
        "steps": [
            {"id": "x1", "phase": "before", "period": "1973~1974", "title": "장발·미니스커트 단속",
             "claimIds": ["c70-taboo", "c70-longhair"], "nodeIds": ["e70-taboo"]},
            {"id": "x2", "phase": "turn", "period": "1982~1983", "title": "교복·두발 자율화",
             "claimIds": ["fl-expr-uniform"], "nodeIds": []},
            {"id": "x3", "phase": "life", "period": "1986~", "title": "다시 교복으로 — 학교장 재량",
             "claimIds": ["fl-expr-uniform-back"], "nodeIds": []},
            {"id": "x4", "phase": "turn", "period": "1992~2025", "title": "문신 — 불법이던 시술이 제도 안으로",
             "claimIds": ["fl-expr-tattoo-law", "fl-expr-tattoo-survey"], "nodeIds": []},
        ],
        "links": [
            {"from": "x1", "to": "x2", "kind": "interpretation", "note": "한국민족문화대백과는 자율화를 신군부의 사회 유화정책의 하나로 설명한다. 단속 완화가 청년층 요구의 결과였는지는 이 자료로 알 수 없다.", "claimIds": ["fl-expr-uniform"]},
            {"from": "x2", "to": "x3", "kind": "causal", "note": "가계 부담·위화감·생활지도 문제가 제기된 것이 1986년 학교장 재량 전환의 이유로 기록돼 있다.", "claimIds": ["fl-expr-uniform-back"]},
        ],
        "cross": [
            {"flow": "flow-relations", "note": "온라인에서 채팅방마다 다른 프로필을 쓰는 것도 자신을 드러내는 방식의 변화다."},
            {"flow": "flow-shop", "note": "패션 소비 장소의 변화는 쇼핑 흐름에서 이어 볼 수 있다(자료 보강 필요)."},
        ],
        "gaps": [
            "패션 유행을 누가 만들고 어떻게 퍼뜨렸는지(잡지·방송·연예인·온라인 쇼핑몰) — 신뢰할 수 있는 장기 자료를 아직 확보하지 못해 이 흐름에서 패션은 다루지 않았다.",
            "장발 단속이 언제 어떻게 끝났는지.",
            "문신에 대한 사회 전체의 인식 변화(국민 대상 조사) — 이용자 조사만 확보했다.",
            "키링·굿즈 같은 '꾸미기' 소비의 규모.",
        ],
        "alternatives": [
            "교복 자율화의 의도를 학생 개성 존중으로 보는 설명(당시 문교부 발표)과 정권의 이미지 쇄신으로 보는 설명이 함께 있다.",
        ],
    },
]

PHASE_KO = {"before": "변화 이전", "condition": "조건과 배경", "turn": "전환점", "spread": "확산과 참여 집단",
            "life": "행동·생활의 변화", "cross": "다른 분야로", "now": "지금 이어지는 것 · 달라진 것"}
LINK_KO = {"causal": "자료가 뒷받침하는 인과", "condition": "배경·조건", "correlation": "함께 움직임(상관)",
           "sequence": "시간 순서일 뿐", "interpretation": "해석", "hypothesis": "검증되지 않은 가설"}


def validate(claims, nodes, indicators):
    """흐름이 가리키는 주장·사건·지표가 실제로 있는지, 단계 연결이 올바른지 확인한다."""
    cids = {c["id"] for c in claims}
    nids = {n["id"] for n in nodes}
    iids = {i["id"] for i in indicators}
    fids = {f["id"] for f in FLOWS}
    for f in FLOWS:
        sids = {s["id"] for s in f["steps"]}
        for s in f["steps"]:
            for c in s["claimIds"]:
                if c not in cids:
                    raise SystemExit(f"{f['id']}/{s['id']}: 없는 주장 {c}")
            for n in s["nodeIds"]:
                if n not in nids:
                    raise SystemExit(f"{f['id']}/{s['id']}: 없는 사건 노드 {n}")
            if s["phase"] not in PHASE_KO:
                raise SystemExit(f"{f['id']}/{s['id']}: 알 수 없는 단계 {s['phase']}")
            if not s["claimIds"] and not s.get("empty"):
                raise SystemExit(f"{f['id']}/{s['id']}: 근거가 없으면 'empty'로 이유를 적어야 한다")
        for l in f["links"]:
            if l["from"] not in sids or l["to"] not in sids or l["kind"] not in LINK_KO:
                raise SystemExit(f"{f['id']}: 잘못된 연결 {l}")
            for c in l["claimIds"]:
                if c not in cids:
                    raise SystemExit(f"{f['id']}: 연결 근거 없음 {c}")
        for i in f["indicators"]:
            if i not in iids:
                raise SystemExit(f"{f['id']}: 없는 지표 {i}")
        for x in f["cross"]:
            if x["flow"] not in fids:
                raise SystemExit(f"{f['id']}: 없는 흐름 {x['flow']}")
        for c in f["lede"]:
            if c not in cids:
                raise SystemExit(f"{f['id']}: 요약 근거 없음 {c}")
    return {"flows": FLOWS, "phaseKo": PHASE_KO, "linkKo": LINK_KO}
