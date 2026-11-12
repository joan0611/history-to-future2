"""모든 흐름(질문)이 1960년대~2020년대 일곱 시대를 빠짐없이 지나가도록 하는 모듈.

- 단계(step)마다 시대(era)를 정한다.
- 시대마다 그 질문의 '그 무렵 모습'을 한 줄로 적는다(eraStates). 근거는 그 시대 단계의 주장들.
- 시대와 다음 시대 사이를 잇는 다리(bridges)에 연결 성격과 근거를 단다. 근거를 찾지 못하면 sequence로 두고 그렇게 적는다.
- 질문이 없던 분야(정치·경제·기기·여가)는 새 흐름으로 더한다.
"""

A = "2026-11-12"
ERAS = ["1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]


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
    # 음악
    S("er-seoul-151117", "음악의 타임슬립 효과 '응팔'이 소환한 1980년대 BGM", "서울신문",
      "https://m.seoul.co.kr/news/life/2015/11/17/20151117800024", "news", published="2015-11-17"),
    S("er-koreatimes-090630", "Evolution of Local Music Programs", "The Korea Times",
      "https://www.koreatimes.co.kr/entertainment/shows-dramas/20090630/evolution-of-local-music-programs", "news", published="2009-06-30"),
    # 쇼핑
    S("er-archives-chron-1968", "기록으로 보는 연표 — 1968년 6월 2일 뉴서울 슈퍼마켓 개점", "국가기록원",
      "https://theme.archives.go.kr/next/chronology/searchArchive.do?page=298", "government"),
    S("er-seoul-010509", "[대한포럼] 신용카드 질서 바로잡기", "서울신문",
      "https://m.seoul.co.kr/news/2001/05/09/20010509006003", "news", published="2001-05-09"),
    S("er-kbr-card", "한국 신용카드의 역사", "Korea Business Review",
      "https://www.koreabizreview.com/articles/kbr-legacy-6112", "news"),
    S("er-greened-card", "디자인으로 살펴보는 신용카드 역사", "그린포스트코리아",
      "https://www.greened.kr/news/articleViewAmp.html?idxno=249749", "news"),
    S("er-etoday-bc", "[컴패니줌업] 비씨카드 — 창립 25년", "이투데이",
      "https://www.etoday.co.kr/news/view/124629", "news", published="2007-04-22"),
    S("er-mediahub-myeongdong", "쇼핑의 메카 '명동', 문인과 예술인들의 아지트였다?", "서울시 미디어허브",
      "https://mediahub.seoul.go.kr/archives/2013942", "government"),
    S("er-newsis-180502", "[편의점 30살] 1989년 5월6일 첫 개점…24시간 영업하는 슈퍼마켓", "뉴시스",
      "https://www.newsis.com/view/NISX20180502_0000297836", "news", published="2018-05-03"),
    S("er-newstomato-160921", "국내 편의점 1호점 여전히 건재", "뉴스토마토",
      "https://newstomato.com/ReadNews.aspx?no=690833", "news", published="2016-09-21"),
    S("er-sgsg-160520", "개인신용 등급별 카드이용 한도를 확인해야", "한국경제 생글생글",
      "https://sgsg.hankyung.com/article/2016052072781", "news", published="2016-05-20"),
    # 만남·관계
    S("er-encykorea-dabang", "다방", "한국민족문화대백과사전",
      "https://encykorea.aks.ac.kr/Article/E0013452", "reference"),
    S("er-kyeonggi-170914", "학림다방에서 음악다방까지 — 다방 문화의 변천", "경기일보",
      "https://www.kyeonggi.com/article/201709140944269", "news", published="2017-09-14"),
    S("er-ppss-place", "시간의 흐름 속, 약속장소", "ㅍㅍㅅㅅ",
      "https://ppss.kr/archives/126201", "news"),
    S("er-archives-phone", "사진으로 보는 전화 — 전국 전화자동화와 1,000만 회선", "국가기록원",
      "https://theme.archives.go.kr/next/photo/phoneList.do?subNo=02", "government"),
    S("er-etnews-120911", "[100대 사건_012] 국산 전전자교환기(TDX-1) 상용서비스", "전자신문",
      "https://www.etnews.com/201209110602", "news", published="2012-09-11"),
    # 옷·자기표현
    S("er-encykorea-mini", "미니스커트", "한국민족문화대백과사전",
      "https://encykorea.aks.ac.kr/Article/E0079871", "reference"),
    S("er-weekly-mini", "올여름 초미니여성 거리 누빈다", "주간경향",
      "https://weekly.khan.co.kr/article/14693", "news", origin="khan-group"),
    S("er-archives-fashionshow", "기록으로 만나는 대한민국 — 패션쇼", "국가기록원",
      "https://theme.archives.go.kr/next/koreaOfRecord/fashionShow.do", "government"),
    S("er-ks-menswear", "한국 현대 남성복식 광고의 변화와 특성(1960~1990년대)", "한국복식학회 등(KoreaScience)",
      "https://koreascience.kr/article/JAKO200633063796234.pdf", "academic"),
    S("er-weekly-201023", "\"X세대 등장으로 권위가 무너지기 시작\"", "주간경향",
      "https://weekly.khan.co.kr/article/202010231502261", "news", published="2020-10-23", origin="khan-group"),
    S("er-khan-051005", "X세대를 대표한 인물들", "경향신문",
      "https://www.khan.co.kr/article/200510051546411", "news", published="2005-10-05", origin="khan-group"),
    S("er-seoul-021031", "W세대/ 디카族 \"아무때나 찍는다\"", "서울신문",
      "https://m.seoul.co.kr/news/2002/10/31/20021031019001", "news", published="2002-10-31"),
    S("er-sgsg-070503", "디카와 미니홈피가 바꾼 사진 문화", "한국경제 생글생글",
      "https://sgsg.hankyung.com/article/2007050309031", "news", published="2007-05-03"),
    S("er-kscap-insta", "인스타그램 해시태그 이용동기와 이용행동 연구", "한국심리학회지: 소비자·광고 20(4)",
      "https://accesson.kr/kscap/assets/pdf/15482/journal-20-4-445.pdf", "academic"),
    S("er-journalist-insta", "네이버도 제친 인스타, '국민 SNS' 등극하나", "한국기자협회 기자협회보",
      "https://www.journalist.or.kr/m/m_article.html?no=55913", "news", note="정보통신정책연구원 '세대별 SNS 이용 현황'(2023 한국미디어패널조사) 보도"),
    # 정치
    S("er-imaeil-260818", "5·18 민주화운동 — 10·26 이후 신군부의 비상계엄 전국 확대", "매일신문",
      "https://www.imaeil.com/page/view/2026081810414011204", "news", published="2026-08-18"),
    S("er-seoul-960827", "「12·12」「5·18」 선고/사건의 실체와 의미", "서울신문",
      "https://m.seoul.co.kr/news/1996/08/27/19960827003001", "news", published="1996-08-27"),
    S("er-nocut-518", "5·18 진상규명의 길 — 87년 6월 항쟁과 88년 청문회", "노컷뉴스",
      "https://nocutnews.co.kr/news/6544613", "news"),
    S("er-khan-150711", "5·18 광주민주화운동과 진상규명", "경향신문",
      "https://www.khan.co.kr/article/201507111446581", "news", published="2015-07-11", origin="khan-group"),
    S("er-archives-518law", "정책 기록 — 5·18 특별법과 역사바로세우기", "국가기록원",
      "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=218", "government"),
    S("er-seoul-951229", "김 대통령 95년 \"역사정립 개혁\"", "서울신문",
      "https://m.seoul.co.kr/news/1995/12/29/19951229002005", "news", published="1995-12-29"),
    S("er-khan-100513", "[어제의 오늘] 2004년 노무현 대통령 탄핵 기각", "경향신문",
      "https://www.khan.co.kr/article/201005131754565", "news", published="2010-05-13", origin="khan-group"),
    S("er-newspim-161209", "박근혜 대통령 탄핵 표결 — 헌정 사상 두 번째", "뉴스핌",
      "https://newspim.com/news/view/20161209000029", "news", published="2016-12-09"),
    S("er-weekly-candle1y", "촛불 1년, 우리에게 무엇을 남겼나", "주간경향",
      "https://weekly.khan.co.kr/article/19840", "news", origin="khan-group"),
    S("er-seoul-161108", "미선·효순이 지핀 작은 불꽃… 14년 뒤 세상 바꾸는 함성으로", "서울신문",
      "https://www.seoul.co.kr/news/society/2016/11/08/20161108010024", "news", published="2016-11-08"),
    # 여가
    S("er-cine21-33688", "한국영화 마케팅 30년사 [1] — 1970년대", "씨네21",
      "https://cine21.com/news/view/?mag_id=33688", "news"),
    S("er-inha-theater", "영화 홍보 장소로서의 극장", "인하대 한국학연구소 『한국학연구』 72",
      "https://korea.inha.ac.kr/sites/inhakorea/upfiles/tb_kor_study/72/4.pdf", "academic"),
    S("er-daejung-3s", "1980년대 스포츠 만화·영화와 대중문화(대중서사연구 25-1)", "대중서사학회",
      "https://accesson.kr/daejung/assets/pdf/4935/journal-25-1-315.pdf", "academic"),
    S("er-kyeonggi-250317", "프로야구의 출범과 여가 선용", "경기일보",
      "https://www.kyeonggi.com/article/20250317580437", "news", published="2025-03-17"),
    S("er-khan-030821", "주5일 근무제 국회 환노위 통과", "경향신문",
      "https://www.khan.co.kr/article/200308211830401", "news", published="2003-08-21", origin="khan-group"),
    S("er-archives-5day", "정책 기록 — 주5일근무제 시행", "국가기록원",
      "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=224", "government"),
    # 생활시간
    S("er-kli-hours", "근로시간 국제비교(월간 노동리뷰 2012년 3월호 통계프리즘)", "한국노동연구원",
      "https://repository.kli.re.kr/bitstream/2021.oak/5830/2/%eb%85%b8%eb%8f%99%eb%a6%ac%eb%b7%b0_no.84_2012.3_9.pdf", "institution", published="2012-03"),
    S("er-aju-140825", "한국인 근로시간, 2000년 이후 감소하다 다시 증가..11년 2090시간→13년 2163시간", "아주경제",
      "https://www.ajunews.com/view/20140825173410752", "news", published="2014-08-25", origin="oecd-hours"),
    S("er-jjan-151102", "韓 근로시간 OECD 2위…독일보다 연간 4개월 더 일한다", "전북일보(연합뉴스)",
      "https://www.jjan.kr/articleAmp/20151102564107", "news", published="2015-11-02", origin="oecd-hours"),
    # 스포츠
    S("er-archives-wrestling", "기록으로 만나는 대한민국 — 프로레슬링", "국가기록원",
      "https://theme.archives.go.kr/next/koreaOfRecord/wrestling.do", "government"),
    S("er-bravo-4413", "1960년대 한국 스포츠 — 국제대회와 첫 세계선수권 우승", "브라보마이라이프(이투데이)",
      "https://bravo.etoday.co.kr/view/atc_view/4413", "news"),
    S("er-mediahub-baseball", "MBC청룡, 삼미슈퍼스타즈…응답하라! 프로야구 추억의 구단들", "서울시 미디어허브",
      "https://mediahub.seoul.go.kr/archives/2014610", "government"),
    S("er-journalist-hsbb", "고교야구 인기 하락에 신문사 고민", "한국기자협회 기자협회보",
      "https://www.journalist.or.kr/m/m_article.html?no=35105", "news", published="2014-12-03"),
    S("er-ksq-baseball70", "한국야구의 발전과정에 관한 사회학적 연구 — 1970년대 야구 대중화의 배경을 중심으로", "한국학(한국학중앙연구원) 44(2)",
      "https://www.accesson.kr/ksq/v.44/2/349/41184", "academic"),
    S("er-weekly-baseball", "야구의 '긍정적 외부효과'", "주간경향",
      "https://weekly.khan.co.kr/article/201104131830361", "news", published="2011-04-13", origin="khan-group"),
    S("er-hkmag-220413", "적자 면하기 바쁜 야구단, 선수단 운영에도 등골 휘어", "한경비즈니스",
      "https://magazine.hankyung.com/business/article/202204133226b", "news", published="2022-04-13"),
    # 기기
    S("er-news1-ai", "국민 44.5% 생성형 AI 경험…국민 3명 중 2명 '긍정적 영향' 평가", "뉴스1",
      "https://www.news1.kr/amp/it-science/general-science/6119785", "news", published="2026-03-31", origin="msit-internet-2025"),
    S("er-mt-ai", "국민 10명 중 4.4명 \"생성형 AI, 나도 써봤다\"", "머니투데이",
      "https://www.mt.co.kr/tech/2026/03/31/2026033111234563860", "news", published="2026-03-31", origin="msit-internet-2025"),
    S("er-fn-ai-panel", "2025년 지능정보사회 이용자 패널조사 — 생성형 AI 이용 38.9%", "파이낸셜뉴스",
      "https://www.fnnews.com/news/202605281415233244", "news", published="2026-05-28"),
]


CLAIMS = [
    # ── 음악 1980년대 ──
    C("er-mus-top10", "KBS '가요톱10'(1981~1998)은 시청자와 팬의 투표를 반영한 순위 형식의 가요 프로그램으로, 1980년대 가장 영향력 있는 가요 프로그램이었다.",
      "fact", "verified", ["er-seoul-151117", "er-koreatimes-090630"], ["culture"], period="1981~1998"),
    C("er-mus-80s", "1980년대 가요는 발라드·댄스·록·트로트로 장르가 넓어졌고, 1981년 시작된 컬러TV 방송으로 TV 스타가 두드러졌다. 이문세 3·4집은 판매량 100만·200만 장을 넘겼다.",
      "fact", "sourced", ["er-seoul-151117"], ["culture"], period="1980년대",
      scope="컬러 방송 시작은 1980년 12월(국가기록원)이다. 기사는 1981년으로 적었다."),
    C("er-mus-80s-why", "서울신문은 1980년대 가요계가 1970년대 긴급조치 9호에 따른 규제와 억압에 대한 반작용처럼 분출했다고 정리했다.",
      "interpretation", "sourced", ["er-seoul-151117"], ["culture", "politics"], period="1970~1980년대"),
    # ── 쇼핑 ──
    C("er-shop-1968", "1968년 6월 2일 서울에 지하 1층·지상 11층 규모의 뉴서울 슈퍼마켓이 문을 열었다.",
      "fact", "sourced", ["er-archives-chron-1968"], ["consumption"], period="1968"),
    C("er-shop-card69", "국내 신용카드는 1969년 신세계백화점이 발급한 자사 카드에서 시작됐다. 그 백화점에서만 쓰는 회원제 카드였고, 1970년대에는 미도파·롯데 등도 회원제 카드를 냈다.",
      "fact", "verified", ["er-seoul-010509", "er-kbr-card", "er-greened-card"], ["consumption"], period="1969~1970년대"),
    C("er-shop-myeongdong", "1970년대 이후 명동은 신세계·미도파·코스모스백화점(1970~1992)을 중심으로 쇼핑의 중심지가 되었다.",
      "fact", "sourced", ["er-mediahub-myeongdong"], ["consumption"], period="1970~1980년대"),
    C("er-shop-card78", "어디서나 쓰는 범용 신용카드는 1978년 외환은행이 비자(VISA)와 제휴해 발급하면서 시작되었고, 1982년에는 5개 시중은행이 은행신용카드협회(현 BC카드)를 만들었다.",
      "fact", "verified", ["er-greened-card", "er-etoday-bc", "er-kbr-card"], ["consumption", "economy"], period="1978~1982"),
    C("er-shop-cvs", "국내 첫 편의점은 1989년 5월 6일 서울 올림픽선수촌 아파트 상가에 문을 연 세븐일레븐으로, '24시간 여는 슈퍼마켓'으로 받아들여졌다. 업계는 올림픽 이후의 국제화 열풍과 높아진 소득을 배경으로 꼽는다.",
      "fact", "verified", ["er-newsis-180502", "er-newstomato-160921"], ["consumption"], period="1989",
      scope="배경 설명은 업계 관계자의 말을 옮긴 것이다."),
    C("er-shop-cardpolicy", "신용카드 사용을 늘리려는 정책으로 1999년 신용카드 소득공제, 2000년 신용카드 영수증 복권제가 시행되었다.",
      "fact", "sourced", ["er-sgsg-160520"], ["consumption", "economy"], period="1999~2000"),
    # ── 만남·관계 ──
    C("er-rel-dabang", "1960년대 이후 다방은 여주인이 얼굴마담·레지 등을 두고 운영하는 형태로 바뀌며 이전보다 커졌다.",
      "fact", "sourced", ["er-encykorea-dabang"], ["society"], period="1960년대"),
    C("er-rel-dabang70", "1960년대에는 서울 대학로의 학림다방 같은 곳이 다방 문화를 이끌었고, 1970년대에는 DJ가 음악을 틀어 주는 음악다방이 전성기를 맞았다.",
      "fact", "sourced", ["er-kyeonggi-170914"], ["society", "culture"], period="1960~1970년대"),
    C("er-rel-dabang-decline", "1970년대 중반 이후 강남 개발로 대형 상업시설이 생기고, 1970년대 후반부터 커피믹스와 커피자판기가 대중화되면서 다방 문화가 쇠퇴하기 시작했다는 설명이 있다.",
      "interpretation", "sourced", ["er-ppss-place"], ["society"], period="1970년대 후반~"),
    C("er-rel-phone", "1987년 7월 1일 전국 전화 자동화가 완성되었고, 같은 해 9월 전화 시설이 1,000만 회선을 넘어 '1가구 1전화' 시대가 되었다. 한국형 전전자교환기(TDX)의 실용화가 이를 가능하게 했다.",
      "fact", "verified", ["er-archives-phone", "er-etnews-120911"], ["society", "technology"], period="1986~1987"),
    # ── 옷·자기표현 ──
    C("er-expr-mini", "미니스커트는 1967년 가수 윤복희가 입고 귀국하면서 유행하기 시작해 1968년에 절정에 이르렀고, 1971년에는 무릎 위 30cm 이상까지 짧아졌다.",
      "fact", "verified", ["er-encykorea-mini", "er-weekly-mini"], ["society", "culture"], period="1967~1971"),
    C("er-expr-mini-crack", "치마 길이가 계속 짧아지자 1973년 경범죄처벌법에 따른 미니스커트 단속이 벌어졌다. 경찰은 자를 들고 다니며 무릎 위 길이를 쟀다.",
      "fact", "sourced", ["er-weekly-mini"], ["society", "politics"], period="1973",
      scope="단속 기준 길이는 자료마다 '무릎 위 17cm'·'20cm'로 다르다."),
    C("er-fash-ready", "1970년대 기성복이 대량생산되기 전까지 사람들은 집에서 옷을 짓거나 양장점·양복점에서 맞춰 입었다. 1970년대에는 기성복 업체가 주도하는 패션쇼가 열리기 시작했다.",
      "fact", "sourced", ["er-archives-fashionshow"], ["consumption", "culture"], period="1960~1970년대"),
    C("er-fash-men80", "한 복식 연구는 한국 남성복이 1960년대 도입기, 1970년대 발전기(대량생산·대량소비, 기성복 선호)를 거쳐 1980년대에 본격적인 기성복 시대로 들어섰다고 정리한다.",
      "interpretation", "sourced", ["er-ks-menswear"], ["consumption", "culture"], period="1960~1990년대"),
    C("er-expr-x", "1995년 경향신문은 'X세대'의 등장으로 '권위 있는 모든 것이 무너지기 시작했다'고 썼다. 거리 패션은 유행을 단정 지을 수 없을 만큼 '입고 싶은 대로 입는' 모습이었다.",
      "fact", "sourced", ["er-weekly-201023"], ["society", "culture"], period="1990년대 중반"),
    C("er-expr-seotaiji", "'X세대의 심장'으로 불린 서태지와 아이들은 1992년 4월 데뷔해 1996년 1월 은퇴했고, 이들의 은퇴와 함께 X세대 담론도 사실상 막을 내렸다는 평가가 있다.",
      "fact", "sourced", ["er-khan-051005"], ["culture"], period="1992~1996"),
    C("er-expr-dica", "2002년 서울신문은 디지털카메라를 1990년대의 삐삐·휴대폰에 이어 신세대를 대표하는 물건으로 소개했고, 2007년 생글생글은 미니홈피에 올릴 사진을 남보다 '예쁘게, 특이하게' 찍으려는 경쟁이 아마추어 사진가를 늘렸다고 전했다.",
      "fact", "sourced", ["er-seoul-021031", "er-sgsg-070503"], ["society", "technology"], period="2002~2007",
      scope="두 기사가 각각 다른 부분을 말한다."),
    C("er-expr-sns-gen", "한 연구는 SNS가 오프라인 관계 중심의 미니홈피·블로그(1세대)에서 페이스북·트위터 같은 텍스트 기반(2세대), 이미지와 해시태그 중심의 인스타그램(3세대)으로 바뀌었다고 정리한다.",
      "interpretation", "sourced", ["er-kscap-insta"], ["society", "technology"], period="2000~2010년대"),
    C("er-expr-insta", "정보통신정책연구원의 2023년 조사에서 인스타그램은 X세대(만 39~54세)에서도 1순위 SNS(36.5%)였고, 밀레니얼 세대는 SNS 이용 목적으로 '자신의 일상 기록·공유'를 상대적으로 많이 꼽았다.",
      "statistical", "sourced", ["er-journalist-insta"], ["society", "technology"], period="2023"),
    # ── 정치 ──
    C("er-pol-1979", "1979년 10·26으로 박정희 대통령이 숨진 뒤, 12·12 군사반란으로 군의 실권을 잡은 신군부가 비상계엄을 전국으로 확대했고 이에 맞서 광주에서 5·18 민주화운동이 일어났다. 1996년 법원은 12·12를 군사반란, 5·17과 5·18 진압을 내란으로 판결했다.",
      "fact", "verified", ["er-imaeil-260818", "er-seoul-960827"], ["politics"], period="1979~1980"),
    C("er-pol-518truth", "1987년 6월 항쟁 뒤 국회가 여소야대로 바뀌자 1988년 국회에 5·18 진상조사특별위원회가 꾸려지고 청문회가 전국에 생중계되었다.",
      "fact", "verified", ["er-nocut-518", "er-khan-150711"], ["politics"], period="1987~1988"),
    C("er-pol-518law", "1995년 7월 검찰이 '성공한 내란은 처벌할 수 없다'며 공소권 없음 결론을 내리자 항의 집회와 서명운동이 이어졌고, 김영삼 대통령의 지시로 5·18 특별법이 1995년 12월 국회를 통과했다.",
      "fact", "verified", ["er-archives-518law", "er-khan-150711"], ["politics"], period="1995"),
    C("er-pol-local", "1995년 6월 지방선거가 치러지며 본격적인 지방자치 시대가 열렸다.",
      "fact", "sourced", ["er-seoul-951229"], ["politics"], period="1995"),
    C("er-pol-2004", "2004년 3월 국회가 노무현 대통령 탄핵소추안을 가결했고, 헌법재판소는 63일 만인 5월 14일 이를 기각했다.",
      "fact", "verified", ["er-khan-100513", "er-newspim-161209"], ["politics"], period="2004"),
    C("er-pol-candle00", "시민들은 2002년 여중생 사망사건 규탄 집회와 2004년 탄핵 반대 집회에서도 촛불을 들었고, 2008년 미국산 쇠고기 수입 반대 집회를 거치며 '촛불'은 시민 참여를 대표하는 이름이 되었다.",
      "fact", "verified", ["er-weekly-candle1y", "er-seoul-161108"], ["politics", "society"], period="2002~2008"),
    C("er-pol-candle-evo", "서울신문은 2002년 시작된 촛불집회가 2004년·2008년을 거치며 시민의 자발적 참여 방식으로 진화해 2016년 평화적인 대규모 집회로 이어졌다고 정리했다.",
      "interpretation", "sourced", ["er-seoul-161108"], ["politics", "society"], period="2002~2016"),
    C("er-pol-2nd", "2016년 12월 박근혜 대통령 탄핵소추 표결은 헌정 사상 두 번째로, 2004년 이후 12년 만이었다.",
      "fact", "sourced", ["er-newspim-161209"], ["politics"], period="2004~2016"),
    # ── 여가 ──
    C("er-lei-60s", "씨네21은 TV가 1960년대 중반부터 대중화되기 시작해 1970년대는 'TV 시대'라 할 만했고, 관객이 줄자 극장들은 영화 상영 뒤 가수·배우의 쇼를 덧붙이기도 했다고 전한다.",
      "fact", "sourced", ["er-cine21-33688"], ["culture"], period="1960년대 중반~1970년대"),
    C("er-lei-tv-theater", "TV 보급률은 1970년대 후반 크게 높아져 1979년 약 79.2%가 되었고, 1980년 컬러TV 보급이 시작된 뒤 컬러TV 보급률은 1984년 58%, 1980년대 말 80%를 넘었다. 한 연구는 이 무렵 '안방극장'이 커지며 극장의 권위가 흔들렸다고 본다.",
      "statistical", "sourced", ["er-inha-theater"], ["culture", "technology"], period="1970~1980년대"),
    C("er-lei-3s", "신군부가 '자율화'를 내세워 야간통행금지 해제·해외여행 규제 완화 등을 시행했고, 스포츠와 대중문화를 키워 국민의 관심을 정치에서 돌리려 한 '3S 정책'도 그중 하나였다는 해석이 있다. 프로야구(1982)는 '국민의 여가 선용'을 명분으로 출범했다.",
      "interpretation", "verified", ["er-daejung-3s", "er-kyeonggi-250317"], ["culture", "politics"], period="1981~1982",
      scope="정책 의도에 대한 해석이다. 의도를 밝힌 정부 문서는 확인하지 못했다."),
    C("er-lei-5day-why", "주5일 근무제는 1998년 2월 노사정위원회에서 논의가 시작돼 5년 반 만인 2003년 8월 근로기준법 개정으로 입법되었다. 국가기록원은 2000년 5월 노사정위원회에 근로시간단축특별위원회가 생긴 것을 출발점으로 기록한다.",
      "fact", "verified", ["er-khan-030821", "er-archives-5day"], ["society", "labor"], period="1998~2003"),
    # ── 생활시간 ──
    C("er-time-90s", "한국노동연구원은 OECD 자료를 들어 한국의 연간 실근로시간이 1990년대 이후 줄기 시작해 법정 근로시간이 주 40시간으로 단축된 2004년을 기점으로 2,400시간 미만이 되었고, 2010년에도 2,193시간으로 OECD에서 가장 길었다고 정리했다.",
      "statistical", "sourced", ["er-kli-hours"], ["labor", "society"], period="1990~2010",
      scope="전체 취업자 기준. OECD는 이 통계의 국가 간 단순 비교를 권하지 않는다."),
    C("er-time-2000s", "OECD 통계로 한국의 1인당 연간 근로시간은 2000년 2,512시간에서 2011년 2,090시간까지 줄었다가 다시 오르내렸다.",
      "statistical", "sourced", ["er-aju-140825", "er-jjan-151102"], ["labor", "society"], period="2000~2014",
      scope="두 기사 모두 같은 OECD 통계를 옮겼다."),
    # ── 스포츠 ──
    C("er-sp-60s", "1960~70년대 TV가 귀하던 시절 프로레슬링 중계가 있으면 동네 사람들이 만화가게나 TV 있는 집으로 모였고, 김일 선수가 그 중심이었다. 1966년에는 레슬링 장창선이 해방 이후 종목별 세계선수권에서 처음 우승했다.",
      "fact", "sourced", ["er-archives-wrestling", "er-bravo-4413"], ["culture"], period="1960~1970년대",
      scope="두 출처가 각각 다른 부분을 말한다."),
    C("er-sp-hsbb", "1960년대 중반부터 1981년까지는 고교야구의 전성기로, 4대 신문사가 대회를 주관했다. 1982년 프로야구가 지역 연고제로 출발한 데는 고교야구의 인기가 큰 몫을 했다는 설명이 있다.",
      "fact", "verified", ["er-mediahub-baseball", "er-journalist-hsbb"], ["culture"], period="1965~1982"),
    C("er-sp-why70", "한 사회학 연구는 1960년대의 도시화·산업화가 대중 스포츠 성장의 조건을 만들었고, 실업야구팀 증설 같은 야구 진흥 정책과 전국체전 지방 개최로 지어진 야구장이 1970년대 고교야구 성장으로 이어졌다고 분석했다.",
      "interpretation", "sourced", ["er-ksq-baseball70"], ["culture", "society"], period="1960~1970년대"),
    C("er-sp-100m", "1982년 출범한 프로야구의 누적 관중은 2010년 1억 명을 넘었다.",
      "fact", "sourced", ["er-weekly-baseball"], ["culture"], period="1982~2010"),
    C("er-sp-2022", "프로야구는 2022년 3년 만에 관중 입장 제한 없이 시즌을 시작했다. 코로나19 기간 관중이 제한되었다.",
      "fact", "sourced", ["er-hkmag-220413"], ["culture"], period="2020~2022"),
    # ── 기기 ──
    C("er-tech-ai", "과학기술정보통신부 '2025 인터넷이용실태조사'(2026년 3월 발표)에서 생성형 AI를 써 봤다는 국민은 44.5%로 1년 전(33.3%)보다 11.2%p 늘었다.",
      "statistical", "verified", ["er-news1-ai", "er-mt-ai"], ["technology", "society"], period="2024~2025",
      scope="두 기사는 같은 정부 조사를 옮겼다. 다른 조사(지능정보사회 이용자 패널)는 38.9%로 집계해 조사마다 값이 다르다."),
    C("er-tech-tdx-cdma", "TDX 개발에 참여한 연구자는 유선 전화용 TDX를 성공시킨 뒤 1990년대 초 휴대전화용 CDMA 기술 개발에 들어갔고, 일부 무선 기술은 퀄컴에서 들여왔지만 시스템 대부분은 TDX 기술이 바탕이 되었다고 회고한다.",
      "interpretation", "sourced", ["er-etnews-120911"], ["technology", "industry"], period="1980~1990년대",
      scope="개발 당사자의 회고다."),
]


# ── 새 흐름 4개: 정치·경제·기기·여가 ──
NEW_FLOWS = [
    {
        "id": "flow-politics",
        "question": "권력은 어떻게 바뀌었고, 시민은 어떻게 목소리를 냈나?",
        "cats": ["politics"],
        "span": [1960, 2025],
        "shape": "되풀이와 축적 — 권력 연장과 계엄이 반복될 때마다 시민의 저항이 있었고, 1987년 이후에는 그 저항이 선거·헌법재판·평화 집회라는 제도 안의 방식으로 쌓였다.",
        "lede": ["cfill-3term-yushin", "er-pol-candle-evo"],
        "indicators": [],
        "steps": [
            {"id": "p1", "era": "1960s", "phase": "before", "period": "1969", "title": "3선 개헌", "claimIds": ["cfill-3term"], "nodeIds": ["e60-3term"]},
            {"id": "p2", "era": "1970s", "phase": "turn", "period": "1972", "title": "10월 유신 — 연임 제한이 없는 체제", "claimIds": ["c70-yushin"], "nodeIds": ["d-yushin"]},
            {"id": "p3", "era": "1980s", "phase": "turn", "period": "1979~1980", "title": "10·26, 12·12, 그리고 5·18", "claimIds": ["er-pol-1979", "c80-518"], "nodeIds": ["e80-518"]},
            {"id": "p4", "era": "1980s", "phase": "spread", "period": "1987", "title": "6월 항쟁과 직선제", "claimIds": ["c80-629"], "nodeIds": ["e80-629"]},
            {"id": "p5", "era": "1990s", "phase": "life", "period": "1988~1995", "title": "5·18 진상규명과 특별법, 지방자치", "claimIds": ["er-pol-518truth", "er-pol-518law", "er-pol-local"], "nodeIds": []},
            {"id": "p6", "era": "2000s", "phase": "spread", "period": "2002~2008", "title": "촛불 — 광장에 나오는 새 방식", "claimIds": ["er-pol-candle00", "er-pol-2004"], "nodeIds": []},
            {"id": "p7", "era": "2010s", "phase": "turn", "period": "2016~2017", "title": "촛불집회와 첫 대통령 파면", "claimIds": ["c10-candle", "er-pol-2nd"], "nodeIds": ["e10-candle"]},
            {"id": "p8", "era": "2020s", "phase": "now", "period": "2024~2025", "title": "비상계엄과 두 번째 파면", "claimIds": ["c20-martial"], "nodeIds": ["e20-martial"]},
        ],
        "links": [],
        "cross": [
            {"flow": "flow-leisure", "note": "1980년대 통금 해제·프로야구는 정권의 '자율화' 정책과 함께 봐야 한다(해석)."},
            {"flow": "flow-expression", "note": "장발·미니스커트 단속도 유신 체제의 통제와 같은 시기다."},
        ],
        "gaps": [
            "1960~70년대 시민 저항(한일협정 반대, 유신 반대 운동)의 규모를 보여주는 자료는 아직 연결하지 않았다.",
            "1990년대 이후 투표율의 장기 추이.",
            "촛불집회 참여 인원은 주최 측 집계라 독립 검증이 어렵다.",
        ],
        "alternatives": [
            "1987년 민주화를 시민 항쟁의 성과로 보는 설명과, 올림픽을 앞둔 정권의 부담·미국의 압력 같은 조건을 함께 중시하는 설명이 있다.",
        ],
    },
    {
        "id": "flow-economy",
        "question": "경제는 어떤 위기를 겪었고, 위기에서 무엇을 바꿨나?",
        "cats": ["economy"],
        "span": [1960, 2025],
        "shape": "위기와 학습 — 시대마다 바깥에서 충격이 왔고, 앞선 위기의 약점(석유 의존·단기외채·가계부채)을 고치는 방향으로 대응이 쌓였다.",
        "lede": ["c70-kr-structure", "c08-diff97"],
        "indicators": ["gdp-growth", "cpi-kr"],
        "steps": [
            {"id": "ec1", "era": "1960s", "phase": "before", "period": "1962~1964", "title": "경제개발 계획과 수출 1억 달러", "claimIds": ["c60-kr-plan-1", "c60-kr-export-1"], "nodeIds": ["e60-plan", "e60-export"]},
            {"id": "ec2", "era": "1970s", "phase": "turn", "period": "1973~1975", "title": "1차 석유파동 — 물가 24%", "claimIds": ["c70-kr-cpi", "c70-syn-chain"], "nodeIds": ["e70-kr-order", "d-kr-cpi"]},
            {"id": "ec3", "era": "1980s", "phase": "turn", "period": "1980~1988", "title": "2차 석유파동의 역성장, 이어진 3저 호황", "claimIds": ["c70-kr-2nd", "c80-3low"], "nodeIds": ["d-kr-2nd"]},
            {"id": "ec4", "era": "1990s", "phase": "turn", "period": "1996~1998", "title": "외환위기", "claimIds": ["c90-why-open", "c97-fx", "c90-kr-imf"], "nodeIds": ["e90-imf"]},
            {"id": "ec5", "era": "2000s", "phase": "life", "period": "2001~2008", "title": "외환보유액 쌓기, 카드대란, 금융위기", "claimIds": ["c97-reserve-build", "c00-card", "c08-diff97"], "nodeIds": ["d08-diff", "e00-card"]},
            {"id": "ec6", "era": "2010s", "phase": "spread", "period": "2016", "title": "사상 최저 금리와 늘어난 가계부채", "claimIds": ["c10-rate", "c10-debt"], "nodeIds": ["e10-rate"]},
            {"id": "ec7", "era": "2020s", "phase": "now", "period": "2020~2023", "title": "코로나 빅컷 뒤 물가·금리 급등", "claimIds": ["c2020-hike", "c20-kr-cpi"], "nodeIds": ["d20-hike", "e20-kcpi"]},
        ],
        "links": [],
        "cross": [
            {"flow": "flow-jobs", "note": "외환위기 구조조정은 비정규직 확대로 이어졌다."},
            {"flow": "flow-shop", "note": "카드대란은 소비 방식(신용카드 확산)의 이면이다."},
        ],
        "gaps": [
            "1960년대 외채·원조 의존도의 연도별 자료는 아직 연결하지 않았다.",
            "가계부채와 소비 위축의 인과 크기는 이 사이트에서 계산하지 않았다.",
        ],
        "alternatives": [
            "외환위기를 단기 유동성 부족으로 보는 설명과, 재벌·금융의 구조 문제로 보는 설명이 함께 있다(사건 상세 '1997년' 참고).",
        ],
    },
    {
        "id": "flow-tech",
        "question": "집 안의 화면과 손안의 기기는 어떻게 바뀌었나?",
        "cats": ["industry", "society"],
        "span": [1960, 2025],
        "shape": "누적과 이동 — 라디오에서 TV, 전화, 휴대전화, 스마트폰으로 기기가 바뀌었고, 앞 단계의 통신·전자 기술이 다음 기기를 만드는 바탕이 되었다.",
        "lede": ["c70-culture-why", "c00-kr-iphone"],
        "indicators": ["mobile-kr", "internet-kr"],
        "note": "기기를 만드는 산업(반도체 등)은 '산업과 일자리' 흐름에서 다룬다. 이 줄은 가정과 개인이 쓰는 기기만 따라간다.",
        "steps": [
            {"id": "t1", "era": "1960s", "phase": "before", "period": "1963~1966", "title": "라디오 보급과 첫 국산 흑백TV", "claimIds": ["c60-kr-radio-3", "c60-kr-tv-1", "c60-kr-tv-3"], "nodeIds": ["e60-tv"]},
            {"id": "t2", "era": "1970s", "phase": "spread", "period": "1970~1979", "title": "TV가 집집마다 — 보급률 6%에서 79%로", "claimIds": ["c70-culture-why"], "nodeIds": []},
            {"id": "t3", "era": "1980s", "phase": "turn", "period": "1980~1987", "title": "컬러TV와 1가구 1전화", "claimIds": ["c80-colortv", "er-rel-phone"], "nodeIds": ["e80-colortv"]},
            {"id": "t4", "era": "1990s", "phase": "turn", "period": "1996~2000", "title": "CDMA 휴대전화와 초고속 인터넷", "claimIds": ["c90-cdma", "c90-pcbang"], "nodeIds": ["e90-cdma"]},
            {"id": "t5", "era": "2000s", "phase": "turn", "period": "2009", "title": "아이폰과 스마트폰", "claimIds": ["c00-kr-iphone"], "nodeIds": ["e00-kr-iphone"]},
            {"id": "t6", "era": "2010s", "phase": "life", "period": "2010~", "title": "카카오톡 — 손안의 생활", "claimIds": ["c10-kakao"], "nodeIds": ["e10-kakao"]},
            {"id": "t7", "era": "2020s", "phase": "now", "period": "2024~2025", "title": "생성형 AI 이용", "claimIds": ["er-tech-ai"], "nodeIds": []},
        ],
        "links": [],
        "cross": [
            {"flow": "flow-relations", "note": "전화·PC통신·메신저는 사람을 만나는 방식을 바꿨다."},
            {"flow": "flow-music", "note": "카세트·MP3·스트리밍은 기기 변화와 함께 왔다."},
        ],
        "gaps": [
            "1980년대 카세트 플레이어·VTR 보급률(후보 자료만 찾음).",
            "생성형 AI의 한국 내 이용률 공식 통계.",
        ],
        "alternatives": [
            "기기 보급을 정부의 산업 육성 정책으로 설명하는 시각과, 소득 증가와 소비 수요로 설명하는 시각이 있다.",
        ],
    },
    {
        "id": "flow-leisure",
        "question": "사람들은 언제, 어디서, 무엇을 하며 쉬고 놀았나?",
        "cats": ["culture", "society"],
        "span": [1960, 2025],
        "shape": "넓어지는 시간 — 극장과 TV에서, 밤 시간이 풀리고(1982) 주말이 생기며(2004) 놀 수 있는 시간과 장소가 늘었다. 그러다 2020년 집 안으로 잠시 접혔다.",
        "lede": ["c80-curfew", "c00-5day-leisure"],
        "indicators": ["cons-culture-kr"],
        "steps": [
            {"id": "l1", "era": "1960s", "phase": "before", "period": "1960년대", "title": "극장 영화와 라디오", "claimIds": ["er-lei-60s", "c60-kr-radio-3"], "nodeIds": []},
            {"id": "l2", "era": "1970s", "phase": "condition", "period": "1970년대", "title": "TV 시대와 청년문화", "claimIds": ["er-lei-tv-theater", "c70-youth"], "nodeIds": ["tr-t70-youth"]},
            {"id": "l3", "era": "1980s", "phase": "turn", "period": "1982", "title": "통금 해제와 프로야구 — 밤과 주말의 여가", "claimIds": ["c80-curfew", "c80-ch-24h", "c80-baseball", "er-lei-3s"], "nodeIds": ["e80-curfew", "e80-baseball"]},
            {"id": "l4", "era": "1980s", "phase": "spread", "period": "1983~1989", "title": "해외여행 자유화", "claimIds": ["c80-travel"], "nodeIds": ["e80-travel"]},
            {"id": "l5", "era": "1990s", "phase": "spread", "period": "1991~1999", "title": "노래방과 PC방", "claimIds": ["fl-mus-noraebang", "c90-pcbang", "c90-syn-chain"], "nodeIds": ["tr-t90-pcbang"]},
            {"id": "l6", "era": "2000s", "phase": "turn", "period": "2002~2004", "title": "광장 응원과 주5일 근무", "claimIds": ["c00-worldcup", "c00-5day", "c00-5day-leisure"], "nodeIds": ["e00-worldcup", "e00-5day"]},
            {"id": "l7", "era": "2010s", "phase": "life", "period": "2013~2018", "title": "배달앱·혼밥, 주52시간", "claimIds": ["c10-delivery", "c10-52h"], "nodeIds": ["tr-t10-delivery"]},
            {"id": "l8", "era": "2020s", "phase": "now", "period": "2020~2022", "title": "코로나19 — 집 안으로 접힌 여가", "claimIds": ["c2020-spend", "c2020-endsd"], "nodeIds": ["tr-t20-untact"]},
        ],
        "links": [],
        "cross": [
            {"flow": "flow-politics", "note": "통금 해제와 프로야구는 1980년대 정치 상황과 떼어 보기 어렵다(해석)."},
            {"flow": "flow-music", "note": "노래방은 음악을 '부르는' 여가로 바꿨다."},
        ],
        "gaps": [
            "연도별 여가 시간(생활시간조사)은 아직 지표로 연결하지 않았다.",
            "1960년대 영화 관객 수의 연도별 공식 통계.",
        ],
        "alternatives": [
            "1980년대 여가 확대를 정권의 탈정치화 정책으로 보는 해석과, 소득 증가와 도시화가 만든 자연스러운 변화로 보는 해석이 함께 있다.",
        ],
    },
]


# ── 기존 흐름: 단계의 시대 지정, 빈 시대 채우기, 시대별 모습, 시대 사이 다리 ──
STEP_ERA = {
    "flow-jobs": {"j1": "1960s", "j2": "1960s", "j3": "1970s", "j4": "1970s", "j5": "1980s", "j6": "1980s", "j7": "1990s",
                  "j8": "1990s", "j11": "2000s", "j9": "2010s", "j10": "2020s"},
    "flow-music": {"m1": "1960s", "m2": "1970s", "m3": "1990s", "m4": "1990s", "m5": "2000s", "m6": "2000s", "m7": "2010s",
                   "m9": "2010s", "m8": "2020s"},
    "flow-shop": {"s1": "1970s", "s2": "1990s", "s3": "1990s", "s4": "2000s", "s5": "2000s", "s6": "2010s", "s7": "2010s", "s8": "2020s"},
    "flow-relations": {"r2": "1990s", "r3": "2000s", "r5": "2010s", "r4": "2010s", "r6": "2020s", "r7": "2020s"},
    "flow-fashion": {"f1": "1960s", "f2": "1970s", "f3": "1980s", "f4": "1990s", "f5": "2000s", "f6": "2020s"},
    "flow-expression": {"x1": "1970s", "x2": "1980s", "x3": "1980s", "x4": "2020s"},
    "flow-family": {"f1": "1960s", "f2": "1970s", "f3": "1980s", "f6": "1990s", "f5": "1990s", "f7": "2000s", "f4": "2010s", "f8": "2010s"},
    "flow-city": {"c1": "1960s", "c2": "1960s", "c3": "1970s", "c4": "1970s", "c5": "1970s", "c6": "1980s", "c7": "1990s",
                  "c8": "2000s", "c9": "2010s", "c10": "2020s"},
}

# (흐름, 새 단계, 이 단계 바로 앞에 끼울 단계 id 또는 None=끝에)
ADD_STEPS = [
    ("flow-music", {"id": "m10", "era": "1980s", "phase": "spread", "period": "1981~1989", "title": "TV 가요 순위와 장르의 확장",
                    "claimIds": ["er-mus-top10", "er-mus-80s"], "nodeIds": ["e80-colortv"]}, "m3"),
    ("flow-shop", {"id": "s0", "era": "1960s", "phase": "before", "period": "1968~1969", "title": "첫 슈퍼마켓과 백화점 카드",
                   "claimIds": ["er-shop-1968", "er-shop-card69"], "nodeIds": []}, "s1"),
    ("flow-shop", {"id": "s1b", "era": "1970s", "phase": "condition", "period": "1970년대", "title": "명동 백화점과 동네 시장",
                   "claimIds": ["er-shop-myeongdong"], "nodeIds": []}, "s2"),
    ("flow-shop", {"id": "s1c", "era": "1980s", "phase": "turn", "period": "1978~1989", "title": "은행 신용카드와 첫 편의점",
                   "claimIds": ["er-shop-card78", "er-shop-cvs"], "nodeIds": []}, "s2"),
    ("flow-relations", {"id": "r0", "era": "1960s", "phase": "before", "period": "1960년대", "title": "다방 — 만남의 장소",
                        "claimIds": ["er-rel-dabang", "er-rel-dabang70"], "nodeIds": []}, "r1"),
    ("flow-relations", {"id": "r0b", "era": "1970s", "phase": "condition", "period": "1970년대", "title": "음악다방의 전성기와 쇠퇴의 시작",
                        "claimIds": ["fl-mus-dabang", "er-rel-dabang-decline"], "nodeIds": []}, "r1"),
    ("flow-relations", {"id": "r1b", "era": "1980s", "phase": "turn", "period": "1987", "title": "1가구 1전화 — 집에서 연락하기",
                        "claimIds": ["er-rel-phone"], "nodeIds": []}, "r2"),
    ("flow-fashion", {"id": "f0", "era": "1960s", "phase": "before", "period": "1960년대", "title": "맞춰 입던 옷과 미니스커트",
                      "claimIds": ["er-fash-ready", "er-expr-mini"], "nodeIds": []}, "f1"),
    ("flow-fashion", {"id": "f3b", "era": "1980s", "phase": "spread", "period": "1980년대", "title": "기성복 시대",
                      "claimIds": ["er-fash-men80"], "nodeIds": []}, "f4"),
    ("flow-fashion", {"id": "f5b", "era": "2010s", "phase": "spread", "period": "2008~2015", "title": "SPA 브랜드 매출 1조 원",
                      "claimIds": ["fl-fash-spa"], "nodeIds": []}, "f6"),
    ("flow-expression", {"id": "x0", "era": "1960s", "phase": "before", "period": "1967~1971", "title": "미니스커트의 등장",
                         "claimIds": ["er-expr-mini"], "nodeIds": []}, "x1"),
    ("flow-expression", {"id": "x5", "era": "1990s", "phase": "spread", "period": "1992~1996", "title": "X세대 — '입고 싶은 대로'",
                         "claimIds": ["er-expr-x", "er-expr-seotaiji"], "nodeIds": []}, "x4"),
    ("flow-expression", {"id": "x6", "era": "2000s", "phase": "life", "period": "2002~2007", "title": "디카와 미니홈피 — 나를 찍어 올리기",
                         "claimIds": ["er-expr-dica", "c00-cyworld"], "nodeIds": ["tr-t00-minihompy"]}, "x4"),
    ("flow-expression", {"id": "x7", "era": "2010s", "phase": "life", "period": "2010~2023", "title": "이미지 SNS — 일상을 기록·공유",
                         "claimIds": ["er-expr-sns-gen", "er-expr-insta"], "nodeIds": []}, "x4"),
    ("flow-family", {"id": "f5b", "era": "2000s", "phase": "turn", "period": "2005~2008", "title": "호주제 폐지",
                     "claimIds": ["cfill-hoju"], "nodeIds": ["e00-hoju"]}, "f6"),
    ("flow-family", {"id": "f9", "era": "2020s", "phase": "now", "period": "2020~2025", "title": "인구 자연감소",
                     "claimIds": ["c20-pop"], "nodeIds": []}, None),
    ("flow-city", {"id": "c6b", "era": "1980s", "phase": "spread", "period": "1988", "title": "서울 인구 1천만 명",
                   "claimIds": ["fl-city-seoulpop"], "nodeIds": []}, "c7"),
]

# 단계 내용 조정(시대에 맞게 나누기)
PATCH_STEPS = {
    ("flow-family", "f5"): {"title": "동성동본 금혼 헌법불합치", "period": "1997", "claimIds": ["fl-fam-ssdb"], "nodeIds": []},
    ("flow-family", "f8"): {"title": "출산율 1명 아래로", "period": "2018~2019", "claimIds": ["c10-tfr"], "phase": "spread"},
    ("flow-family", "f4"): {"title": "1인 가구가 가장 흔한 가구로", "period": "2015~2025"},
    ("flow-relations", "r1"): None,  # '1980년대까지(근거 없음)' 단계는 새로 채운 단계로 대체
    ("flow-music", "m9"): {"title": "노래방의 감소", "period": "2011~2018"},
    ("flow-city", "c7"): {"title": "1기 신도시 입주와 서울 집값 하락", "period": "1989~1996"},
}

ERA_STATES = {
    "flow-jobs": {
        "1960s": "농업과 가족 노동이 중심, 계획에 따른 공업화가 시작",
        "1970s": "중화학공업으로 전환, 중동 건설로 일자리가 국경을 넘음",
        "1980s": "반도체 진입, 1987년 노동자 대투쟁과 노조 결성",
        "1990s": "서비스업으로 일자리 이동, 외환위기 구조조정",
        "2000s": "비정규직 비중 정점(2004), FTA로 수출 시장 확대",
        "2010s": "앱으로 연결되는 플랫폼 노동",
        "2020s": "서비스업 70%대, 전문직 증가와 AI",
    },
    "flow-music": {
        "1960s": "라디오와 도심 음악감상실(세시봉)",
        "1970s": "음악다방 DJ, 통기타 포크, 라디오·TV 보급",
        "1980s": "TV 가요 순위와 장르의 다양화",
        "1990s": "노래방과 음반 판매의 정점",
        "2000s": "MP3·파일 공유 뒤 정액제 스트리밍",
        "2010s": "유튜브로 퍼진 K팝, 옛 음악의 재등장",
        "2020s": "동영상 플랫폼에서 듣고 발견하기",
    },
    "flow-shop": {
        "1960s": "시장 중심, 첫 슈퍼마켓과 백화점 카드",
        "1970s": "명동 백화점과 동네 시장·슈퍼",
        "1980s": "은행 신용카드와 첫 편의점(1989)",
        "1990s": "대형마트·TV홈쇼핑의 등장",
        "2000s": "신용카드 확산과 카드대란, 스마트폰 도입",
        "2010s": "모바일쇼핑·간편결제·배달앱",
        "2020s": "코로나19와 온라인 비중 27%",
    },
    "flow-relations": {
        "1960s": "다방이 만남의 장소",
        "1970s": "음악다방의 전성기, 후반부터 쇠퇴",
        "1980s": "1가구 1전화 — 집에서 연락",
        "1990s": "PC통신 동호회 — 관심사로 모르는 사람과",
        "2000s": "인터넷 카페와 미니홈피",
        "2010s": "메신저·오픈채팅·팬카페",
        "2020s": "모임 앱과 줄었다 늘어난 모임 참여",
    },
    "flow-fashion": {
        "1960s": "맞춰 입던 옷, 미니스커트, 동대문 평화시장",
        "1970s": "기성복 대량생산, 청바지와 장발",
        "1980s": "교복 자율화와 기성복 시대",
        "1990s": "동대문 패션몰 — 10~20대의 유행 상권",
        "2000s": "인터넷 쇼핑몰과 SPA 진출, 동대문 주춤",
        "2010s": "SPA 브랜드 매출 1조 원",
        "2020s": "패션 플랫폼 중심의 소비",
    },
    "flow-expression": {
        "1960s": "미니스커트의 등장",
        "1970s": "장발·미니스커트 단속",
        "1980s": "교복·두발 자율화, 3년 뒤 학교장 재량",
        "1990s": "X세대 — '입고 싶은 대로'",
        "2000s": "디카와 미니홈피로 나를 드러내기",
        "2010s": "이미지 SNS에 일상 기록·공유",
        "2020s": "불법이던 문신 시술의 제도화",
    },
    "flow-family": {
        "1960s": "아이가 많던 시대, 가족계획 시작",
        "1970s": "'둘만 낳자', 출생아 정점(1971)",
        "1980s": "'하나씩만', 출산율 대체 수준 아래로",
        "1990s": "혼인 정점(1996)과 동성동본 금혼 헌법불합치",
        "2000s": "출산 장려로 반전, 호주제 폐지",
        "2010s": "1인 가구가 가장 흔한 가구, 출산율 1명 아래",
        "2020s": "인구 자연감소, 출산율 0명대",
    },
    "flow-city": {
        "1960s": "도시 인구 28%, 서울로 몰리는 사람들",
        "1970s": "경부고속도로·지하철 1호선·마이카",
        "1980s": "2호선 순환선, 서울 인구 1천만",
        "1990s": "1기 신도시 입주, 서울 인구 정점",
        "2000s": "KTX와 대중교통 개편",
        "2010s": "아파트에 사는 가구가 절반을 넘음",
        "2020s": "줄어든 서울, 수도권 인구 50% 넘음",
    },
    "flow-politics": {
        "1960s": "3선 개헌으로 장기 집권의 길",
        "1970s": "유신 체제와 긴급조치",
        "1980s": "5·18의 진압, 1987년 6월 항쟁과 직선제",
        "1990s": "5·18 특별법과 지방자치",
        "2000s": "탄핵 기각과 촛불 집회의 등장",
        "2010s": "촛불집회와 첫 대통령 파면",
        "2020s": "비상계엄과 두 번째 파면",
    },
    "flow-economy": {
        "1960s": "개발 계획과 수출 주도 성장의 시작",
        "1970s": "1차 석유파동, 물가 24%",
        "1980s": "2차 석유파동 역성장, 3저 호황",
        "1990s": "개방 속 단기외채, 외환위기",
        "2000s": "외환보유액 확충, 카드대란, 금융위기",
        "2010s": "사상 최저 금리, 가계부채 증가",
        "2020s": "코로나 빅컷 뒤 물가·금리 급등",
    },
    "flow-tech": {
        "1960s": "라디오 보급, 첫 국산 흑백TV",
        "1970s": "TV 보급률 6% → 79%",
        "1980s": "컬러TV·반도체·1가구 1전화",
        "1990s": "CDMA 휴대전화와 초고속 인터넷",
        "2000s": "아이폰 도입과 스마트폰",
        "2010s": "카카오톡 — 손안의 생활",
        "2020s": "생성형 AI를 써 본 국민 44.5%",
    },
    "flow-leisure": {
        "1960s": "극장 영화와 라디오",
        "1970s": "TV 시대와 통기타 청년문화",
        "1980s": "통금 해제·프로야구·해외여행 자유화",
        "1990s": "노래방과 PC방",
        "2000s": "광장 응원과 주5일 근무",
        "2010s": "배달앱·혼밥, 주52시간",
        "2020s": "코로나19로 집 안에 접힌 여가",
    },
}


def B(fr, to, kind, note, claims=()):
    return {"from": fr, "to": to, "kind": kind, "note": note, "claimIds": list(claims)}


BRIDGES = {
    "flow-jobs": [
        B("1960s", "1970s", "condition", "제2차 경제개발 계획이 이미 중화학공업으로 옮겨 가는 방향을 내세웠고, 무역적자·부품 수입 의존·안보 위기가 선언의 배경으로 꼽힌다.", ["cfill-plan2", "c70-hci-why"]),
        B("1970s", "1980s", "condition", "공장에 모인 대규모 노동자가 1987년 대기업 노조 결성의 조건이었다. 직접 계기는 6·29선언 뒤의 통제 이완이다. 중화학·전자 기반이 반도체 진입의 바탕이 됐다는 해석도 있지만 직접 연결 자료는 없다.", ["c80-labor"]),
        B("1980s", "1990s", "interpretation", "1987년 이후 정규직 채용 비용이 커지자 기업이 비정규직을 선호하게 됐다는 연구자 해석이 있다. 본격 확산은 외환위기 이후다.", ["fl-jobs-1987-irregular"]),
        B("1990s", "2000s", "causal", "외환위기 구조조정과 1998년 파견근로 허용 뒤 비정규직이 빠르게 늘어 2004년 정점에 이르렀다.", ["c90-ch-1998", "c00-irregular"]),
        B("2000s", "2010s", "sequence", "비정규·특수고용이 늘어난 뒤 앱으로 연결되는 플랫폼 노동이 등장했다. 두 현상을 잇는 인과 자료는 확보하지 못했다."),
        B("2010s", "2020s", "correlation", "서비스업 비중과 전문직 비중이 함께 늘었다. 같은 원인(산업 구조 변화)의 결과일 수 있다.", ["fl-jobs-emp", "c20-hyp-ai-jobs"]),
    ],
    "flow-music": [
        B("1960s", "1970s", "condition", "라디오·TV 보급과 도시로 모인 청년층이 음악다방·포크 붐이 커진 조건으로 꼽힌다.", ["c70-culture-why"]),
        B("1970s", "1980s", "interpretation", "1975년 금지곡 사태 같은 규제에 대한 반작용처럼 1980년대 가요가 분출했다는 정리가 있고, 컬러TV 방송(1980)이 TV 스타와 순위 프로그램을 키웠다.", ["c70-ban", "er-mus-80s-why", "c80-colortv"]),
        B("1980s", "1990s", "sequence", "TV 순위 프로그램의 시대 뒤에 노래방(1991)과 음반 판매 정점(1995)이 왔다. 둘을 잇는 인과 자료는 없다."),
        B("1990s", "2000s", "sequence", "1995년 정점 이후 2000년대 초 MP3·파일 공유와 함께 음반 시장이 급감했다.", ["fl-mus-cd-crash"]),
        B("2000s", "2010s", "sequence", "정액제 스트리밍이 자리 잡은 뒤 유튜브가 노래를 세계로 퍼뜨리는 통로가 되었다(강남스타일 10억 뷰, 2012).", ["c10-psy"]),
        B("2010s", "2020s", "correlation", "음악을 동영상 사이트에서 듣는다는 응답이 2019~2021년 크게 늘었다. 코로나19 시기와 겹쳐 원인을 가르기 어렵다.", ["fl-mus-video"]),
    ],
    "flow-shop": [
        B("1960s", "1970s", "sequence", "1969년 신세계에 이어 1970년대 미도파·롯데 등 다른 백화점도 회원제 카드를 냈고, 명동 백화점이 쇼핑의 중심이 되었다.", ["er-shop-card69", "er-shop-myeongdong"]),
        B("1970s", "1980s", "sequence", "백화점 안에서만 쓰던 카드가 1978년 비자 제휴와 1982년 BC카드로 어디서나 쓰는 카드가 되었다.", ["er-shop-card78"]),
        B("1980s", "1990s", "condition", "한 연구는 '정적인 구조'이던 소매업이 1980년대 말부터 새 업태가 들어오며 급변했다고 본다. 편의점(1989)과 할인점(1993), 유통시장 개방(1996)이 차례로 이어졌다.", ["fl-shop-before", "fl-shop-discount-stage"]),
        B("1990s", "2000s", "causal", "외환위기 뒤 정부가 신용카드 사용을 장려(소득공제·영수증 복권)했고, 무분별한 발급과 현금서비스 한도 폐지가 겹쳐 2003년 카드대란이 일어났다.", ["er-shop-cardpolicy", "c00-card-why"]),
        B("2000s", "2010s", "causal", "서울시 전자상거래센터는 모바일쇼핑이 커진 이유로 스마트폰 보편화와 간편결제 도입을 든다.", ["fl-shop-mobile-why"]),
        B("2010s", "2020s", "correlation", "모바일·배달로 이미 옮겨 가던 소비가 코로나19 첫해 온라인 비중 27%로 뛰었다. 코로나 효과와 원래 추세를 나눈 자료는 여기 없다.", ["c20-online"]),
    ],
    "flow-relations": [
        B("1960s", "1970s", "sequence", "1960년대 학림다방 같은 다방에 이어 1970년대에는 DJ가 있는 음악다방이 전성기를 맞았다.", ["er-rel-dabang70"]),
        B("1970s", "1980s", "interpretation", "1970년대 후반부터 커피믹스·자판기로 다방이 쇠퇴하기 시작했고, 1987년 1가구 1전화로 집에서 바로 연락할 수 있게 되었다. 두 변화를 직접 잇는 자료는 없다(작성자 정리).", ["er-rel-dabang-decline", "er-rel-phone"]),
        B("1980s", "1990s", "interpretation", "PC통신은 전화선에 모뎀을 연결해 접속했으므로, 전화 회선의 보급이 PC통신 이용의 바탕이었다고 볼 수 있다(작성자 해석). 비싼 접속료가 걸림돌이었다는 기록도 있다.", ["er-rel-phone", "fl-rel-pctong-cost"]),
        B("1990s", "2000s", "sequence", "PC통신 동호회가 하던 관심사 모임이 인터넷 카페로 옮겨 갔다(다음 카페 1999).", ["fl-rel-cafe"]),
        B("2000s", "2010s", "causal", "트위터·페이스북이 들어오고 스마트폰으로 무게중심이 옮겨 가면서 PC 기반 미니홈피의 전성기가 끝났다.", ["c00-cy-decline"]),
        B("2010s", "2020s", "correlation", "모임 참여율은 코로나19 첫해 떨어졌다가 2023년 다시 높아졌다. 같은 시기 관심사 모임 앱 설치가 늘었다.", ["fl-rel-orgrate", "fl-rel-apps"]),
    ],
    "flow-fashion": [
        B("1960s", "1970s", "sequence", "맞춤옷의 시대 뒤 1970년대 기성복 대량생산이 시작되었다. 같은 시기 동대문은 내수 의류의 대부분을 만들었다.", ["er-fash-ready", "fl-fash-dongdaemun"]),
        B("1970s", "1980s", "interpretation", "한 연구는 남성복이 1970년대 발전기를 거쳐 1980년대 본격적인 기성복 시대에 들어섰다고 본다. 1983년 교복 자율화로 학생도 옷을 고르게 되었다.", ["er-fash-men80", "fl-expr-uniform"]),
        B("1980s", "1990s", "sequence", "기성복과 자율화 다음, 1990년대에는 동대문 패션몰이 10~20대의 유행 상권이 되었다.", ["fl-fash-mall"]),
        B("1990s", "2000s", "interpretation", "2000년대 중반 인터넷 쇼핑몰과 SPA 브랜드로 10~20대 고객이 옮겨 가면서 동대문이 주춤했다는 분석이 있다.", ["fl-fash-decline"]),
        B("2000s", "2010s", "sequence", "2005년 유니클로, 2008년 자라 진출 뒤 SPA가 커져 2015년 유니클로 국내 매출이 1조 원을 넘었다.", ["fl-fash-spa"]),
        B("2010s", "2020s", "interpretation", "가격 비교·리뷰·빠른 배송을 앞세운 패션 플랫폼이 퍼지며 매장 중심 SPA가 상대적으로 고전한다는 분석이 있다.", ["fl-fash-platform"]),
    ],
    "flow-expression": [
        B("1960s", "1970s", "causal", "치마가 계속 짧아지자 1973년 경범죄처벌법 개정으로 장발·미니스커트 단속에 법적 근거가 생겼다.", ["er-expr-mini-crack", "c70-taboo"]),
        B("1970s", "1980s", "interpretation", "1982~83년 교복·두발 자율화를 신군부의 유화정책의 하나로 보는 설명이 있다.", ["fl-expr-uniform"]),
        B("1980s", "1990s", "sequence", "자율화 뒤 1990년대 X세대가 '입고 싶은 대로 입는' 세대로 불렸다. 두 변화를 잇는 인과 자료는 없다."),
        B("1990s", "2000s", "sequence", "삐삐·휴대폰에 이어 디지털카메라가 신세대의 물건이 되었고, 미니홈피가 사진으로 나를 드러내는 장소가 되었다.", ["er-expr-dica"]),
        B("2000s", "2010s", "interpretation", "SNS가 미니홈피(1세대)에서 텍스트 SNS(2세대), 이미지·해시태그 중심의 인스타그램(3세대)으로 바뀌었다는 정리가 있다.", ["er-expr-sns-gen"]),
        B("2010s", "2020s", "sequence", "옷과 사진 다음으로 몸 자체를 꾸미는 문신이 늘었고, 법이 2025년에야 그 현실을 따라왔다.", ["fl-expr-tattoo-survey", "fl-expr-tattoo-law"]),
    ],
    "flow-family": [
        B("1960s", "1970s", "sequence", "구호가 '셋'에서 '둘'로 바뀌는 동안 인구증가율이 3.3%에서 2.0%로 낮아졌다. 가족계획 사업의 기여 크기를 나눈 자료는 없다.", ["fl-fam-60s", "fl-fam-70s"]),
        B("1970s", "1980s", "correlation", "캠페인 강화와 출산율 하락이 함께 진행됐다. 같은 시기 도시화·교육 확대도 있었다.", ["fl-fam-tfr"]),
        B("1980s", "1990s", "sequence", "출산율이 낮아진 뒤에도 혼인 건수는 1996년까지 늘었다(베이비붐 세대의 혼인 연령 도달과 겹친다는 설명은 확인하지 못했다).", ["fl-fam-marriage"]),
        B("1990s", "2000s", "interpretation", "가족에 관한 사회 변화는 빠른데 법은 늦게 따라온다는 지적이 있다. 동성동본 금혼은 8년, 호주제는 그 뒤에 바뀌었다.", ["fl-fam-law-lag"]),
        B("2000s", "2010s", "sequence", "출산 장려로 구호가 바뀌었지만 출산율은 2018년 1명 아래로 떨어졌다.", ["fl-fam-pronatal", "c10-tfr"]),
        B("2010s", "2020s", "correlation", "혼인 감소와 출생아 감소가 함께 나타나 2020년 인구가 자연감소로 돌아섰다.", ["fl-fam-marriage", "c20-pop"]),
    ],
    "flow-city": [
        B("1960s", "1970s", "condition", "서울시는 인구와 자동차가 늘자 전차를 철거하고 교통체계를 정비하며 지하철을 만들었다고 설명한다.", ["fl-city-tram"]),
        B("1970s", "1980s", "sequence", "1호선 뒤 10년 만에 순환선(2호선)이 생겼다. 2호선은 도심 기능을 강남으로 옮기는 과정에서 구체화됐다.", ["cfill-line2"]),
        B("1980s", "1990s", "condition", "서울에 더 개발할 땅이 없는데 1988년 집값이 24% 오른 것이 신도시 건설의 배경으로 꼽힌다(기사 정리).", ["fl-city-newtown-why"]),
        B("1990s", "2000s", "sequence", "수도권이 넓어진 뒤 서울 대중교통 개편과 KTX가 같은 해(2004) 시작됐다. 둘을 잇는 인과 자료는 없다.", ["fl-city-2004"]),
        B("2000s", "2010s", "sequence", "대규모 아파트 공급이 이어진 끝에 2018년 아파트 거주 가구가 절반을 넘었다. 연도별 비중 추이는 연결하지 않았다.", ["fl-city-apt"]),
        B("2010s", "2020s", "interpretation", "서울 인구가 1천만 아래로 내려간 이유로 경기도 신도시 개발과 출산율 감소가 함께 꼽힌다(언론 설명).", ["fl-city-seoul-decline"]),
    ],
    "flow-politics": [
        B("1960s", "1970s", "interpretation", "3선 개헌으로 세 번째 출마가 가능해진 박정희 대통령은 1972년 유신으로 연임 제한 없는 체제를 만들었다. 3선 개헌이 유신으로 가는 길을 열었다는 평가가 일반적이다.", ["cfill-3term-yushin"]),
        B("1970s", "1980s", "causal", "유신 체제는 1979년 10·26으로 끝났지만, 그 공백에서 12·12로 군을 장악한 신군부가 계엄을 전국으로 확대했고 이것이 5·18의 직접 계기가 되었다.", ["er-pol-1979"]),
        B("1980s", "1990s", "causal", "6월 항쟁 뒤 여소야대 국회가 5·18 청문회를 열었고, 1995년 '처벌할 수 없다'는 검찰 결정에 대한 항의 끝에 특별법이 만들어졌다.", ["er-pol-518truth", "er-pol-518law"]),
        B("1990s", "2000s", "sequence", "1987년 헌법 아래에서 처음으로 대통령 탄핵 심판이 열렸고(2004), 시민들은 촛불을 들고 광장에 나왔다.", ["er-pol-2004", "er-pol-candle00"]),
        B("2000s", "2010s", "interpretation", "2002년 시작된 촛불집회가 2004·2008년을 거치며 진화해 2016년 평화적 대규모 집회로 이어졌다는 정리가 있다. 2016년 탄핵 표결은 2004년 이후 두 번째였다.", ["er-pol-candle-evo", "er-pol-2nd"]),
        B("2010s", "2020s", "similar", "2017년에 이어 2025년에도 헌법재판소가 대통령을 파면했다. 2024년 계엄은 1980년 계엄 확대와 비교되지만 국회가 몇 시간 만에 해제를 요구했다는 점이 다르다.", ["c10-candle", "c20-martial"]),
    ],
    "flow-economy": [
        B("1960s", "1970s", "causal", "값싼 석유를 전제로 짜인 1960년대 성장 모델이 1973년 석유파동으로 깨졌다. 한국은 절약과 함께 중동 건설로 오일머니를 벌려 했다.", ["c70-syn-chain"]),
        B("1970s", "1980s", "causal", "석유 의존도가 높은 중화학공업 중심으로 바뀐 뒤 맞은 2차 석유파동은 1차 때보다 충격이 커서 1980년 성장률이 -5.2%가 되었다.", ["c70-kr-structure", "c70-kr-2nd"]),
        B("1980s", "1990s", "condition", "3저 호황의 흑자 뒤 1990년대 금융 자유화·OECD 가입을 위한 개방 속에서 단기 외화차입이 늘었고, 외환보유액 부족이 위기의 직접 원인이었다는 해석이 있다.", ["c80-3low", "c90-why-open"]),
        B("1990s", "2000s", "causal", "외환위기 뒤 외환보유액을 위기 완충장치로 쌓았고, 2008년 당국은 '1997년과 다르다'며 그 차이를 들었다.", ["c97-reserve-build", "c08-diff97"]),
        B("2000s", "2010s", "condition", "2008년 위기 뒤 미국의 양적완화와 세계적 저금리 속에 한국도 2016년 사상 최저 금리(1.25%)까지 내렸다.", ["c10-fed-qe", "c10-rate"]),
        B("2010s", "2020s", "causal", "한국은행은 2021년 코로나보다 가계부채 급증과 집값 상승을 더 큰 위험으로 보고 금리를 올리기 시작했다.", ["c10-debt", "c2020-hike"]),
    ],
    "flow-tech": [
        B("1960s", "1970s", "sequence", "비싼 가격에도 추첨으로 팔리던 TV가 1970년대에 빠르게 퍼졌다(가구 보급률 1970년 6.3% → 1979년 79%).", ["c60-kr-tv-3", "c70-culture-why"]),
        B("1970s", "1980s", "condition", "1979년 흑백TV 보급률이 이미 90%였고, 정부는 불황 타개와 가전산업 육성을 목적으로 1980년 컬러TV를 허용했다.", ["c80-colortv"]),
        B("1980s", "1990s", "interpretation", "TDX로 1가구 1전화를 이룬 연구진이 1990년대 초 CDMA 개발에 들어갔고, 시스템 대부분이 TDX 기술을 바탕으로 했다는 개발자 회고가 있다.", ["er-tech-tdx-cdma"]),
        B("1990s", "2000s", "sequence", "CDMA 휴대전화와 초고속 인터넷이 퍼진 뒤 2009년 아이폰으로 스마트폰 시대가 열렸다.", ["c00-kr-iphone"]),
        B("2000s", "2010s", "causal", "카카오톡은 아이폰용 앱으로 출시되었고, 스마트폰 가입자가 2009년 80만 명에서 2010년 722만 명으로 늘던 때였다.", ["c10-kakao", "c00-kr-iphone"]),
        B("2010s", "2020s", "sequence", "스마트폰·앱 생활 위에서 생성형 AI 이용이 1년 새 33.3%에서 44.5%로 늘었다. 스마트폰 보급이 AI 이용을 낳았다는 인과 자료는 없다.", ["er-tech-ai"]),
    ],
    "flow-leisure": [
        B("1960s", "1970s", "correlation", "TV가 1960년대 중반부터 대중화되며 극장 관객의 발길이 뜸해졌다. 씨네21은 TV만이 원인은 아니었다고 덧붙인다.", ["er-lei-60s", "er-lei-tv-theater"]),
        B("1970s", "1980s", "condition", "정부는 통금 해제의 배경으로 개방사회와 올림픽을 앞둔 국가 이미지 개선을 들었다. 같은 시기 '3S 정책'으로 여가를 키워 정치적 관심을 돌리려 했다는 해석도 있다.", ["c80-curfew", "er-lei-3s"]),
        B("1980s", "1990s", "interpretation", "외환위기 실직자·명예퇴직자와 초고속망 구축이 맞물려 PC방 창업이 늘었다는 설명이 있다. 창업자 중 실직자 비율은 확인하지 못했다.", ["c90-syn-chain"]),
        B("1990s", "2000s", "causal", "1998년 노사정위원회에서 시작된 근로시간 단축 논의가 2003년 법 개정으로 이어져 2004년 주5일 근무가 시작되었다.", ["er-lei-5day-why"]),
        B("2000s", "2010s", "condition", "1인 가구·맞벌이 증가와 스마트폰 결제가 배달앱 수요를 키웠다는 분석이 있다.", ["c10-syn-delivery"]),
        B("2010s", "2020s", "correlation", "배달과 비대면 여가가 이미 늘던 중에 코로나19가 겹쳐 문화·오락 지출 비중이 줄고 배달 시장은 2.6배가 되었다.", ["c2020-spend", "c20-delivery"]),
    ],
}


def apply(flows, claims_all):
    """기존 흐름에 시대 정보를 붙이고 새 흐름을 더한다. 검증 실패 시 멈춘다."""
    cids = {c["id"] for c in claims_all}
    by = {f["id"]: f for f in flows}
    for f in NEW_FLOWS:
        if f["id"] in by:
            continue
        flows.append(f)
        by[f["id"]] = f
    # 단계 수정·삭제
    for (fid, sid), patch in PATCH_STEPS.items():
        f = by[fid]
        if patch is None:
            f["steps"] = [s for s in f["steps"] if s["id"] != sid]
            f["links"] = [l for l in f["links"] if l["from"] != sid and l["to"] != sid]
            continue
        for s in f["steps"]:
            if s["id"] == sid:
                s.update(patch)
    # 시대 지정
    for fid, m in STEP_ERA.items():
        for s in by[fid]["steps"]:
            if s["id"] in m:
                s["era"] = m[s["id"]]
    # 단계 추가
    for fid, step, before in ADD_STEPS:
        steps = by[fid]["steps"]
        if any(s["id"] == step["id"] for s in steps):
            continue
        idx = next((i for i, s in enumerate(steps) if s["id"] == before), len(steps)) if before else len(steps)
        steps.insert(idx, dict(step))
    # 시대별 모습·다리
    for f in flows:
        f["span"] = [1960, 2025]
        meta = FLOW_META[f["id"]]
        f["domain"], f["topic"], f["econ"] = meta["domain"], meta["topic"], meta["econ"]
        for s in f["steps"]:
            m = STEP_MEASURE.get((f["id"], s["id"]))
            if m:
                s["measure"] = m
        f["eraStates"] = ERA_STATES[f["id"]]
        f["bridges"] = [dict(b) for b in BRIDGES[f["id"]]]
        for b, ch in zip(f["bridges"], BRIDGE_CHANGE.get(f["id"], [])):
            b["change"] = ch
        # 단계를 시대 순서로 정렬(같은 시대 안에서는 원래 순서 유지)
        order = {e: i for i, e in enumerate(ERAS)}
        import re as _re

        def _y(s):
            m = _re.search(r"(19|20)\d{2}", s["period"])
            return int(m.group()) if m else 0
        f["steps"] = sorted(f["steps"], key=lambda s: (order[s["era"]], _y(s)))
        # 시대 사이 연결(links)은 같은 시대 안의 것만 남긴다 — 시대를 넘는 연결은 bridges가 맡는다
        era_of = {s["id"]: s["era"] for s in f["steps"]}
        f["links"] = [l for l in f["links"] if era_of.get(l["from"]) == era_of.get(l["to"])]
    # 검증
    for f in flows:
        missing = [e for e in ERAS if not any(s.get("era") == e for s in f["steps"])]
        if missing:
            raise SystemExit(f"{f['id']}: 단계가 없는 시대 {missing}")
        if set(f["eraStates"]) != set(ERAS):
            raise SystemExit(f"{f['id']}: 시대별 모습이 빠짐")
        pairs = [(b["from"], b["to"]) for b in f["bridges"]]
        if pairs != list(zip(ERAS, ERAS[1:])):
            raise SystemExit(f"{f['id']}: 시대 사이 다리가 맞지 않음 {pairs}")
        for b in f["bridges"]:
            for c in b["claimIds"]:
                if c not in cids:
                    raise SystemExit(f"{f['id']} {b['from']}→{b['to']}: 없는 주장 {c}")
            if b["kind"] not in ("causal", "condition", "correlation", "sequence", "interpretation", "hypothesis", "similar"):
                raise SystemExit(f"{f['id']}: 알 수 없는 연결 {b['kind']}")
            if b["kind"] != "sequence" and not b["claimIds"]:
                raise SystemExit(f"{f['id']} {b['from']}→{b['to']}: 근거 없는 '{b['kind']}' 연결")
    return {"flows": flows, "domains": DOMAINS}


# ─────────────────────────────────────────────────────────────
# 여가 줄 분리: '24시간 도시'(생활시간)와 '프로스포츠'(스포츠)는 같은 시기에 나타났다는 이유로 묶지 않는다.
#   flow-time   생활시간 — 일하지 않는 시간(밤·주말)이 언제 얼마나 생겼나
#   flow-sports 스포츠 — 보는 스포츠와 하는 스포츠
#   flow-leisure 여가 공간 — 여가를 집 밖/안 어디서 보내나
# ─────────────────────────────────────────────────────────────
_LEISURE = {
    "id": "flow-leisure",
    "question": "여가는 집 밖과 집 안 가운데 어디에서 보내게 됐나?",
    "cats": ["culture", "society"],
    "span": [1960, 2025],
    "shape": "밖과 안의 왕복 — 극장에서 안방 TV로 들어왔다가, 해외여행·노래방·PC방으로 다시 나갔고, 배달과 코로나19로 집 안 비중이 다시 커졌다.",
    "lede": ["er-lei-tv-theater", "c2020-spend"],
    "indicators": ["cons-culture-kr"],
    "steps": [
        {"id": "l1", "era": "1960s", "phase": "before", "period": "1960년대", "title": "극장 영화", "claimIds": ["er-lei-60s"], "nodeIds": []},
        {"id": "l2", "era": "1970s", "phase": "condition", "period": "1970년대", "title": "안방으로 들어온 TV", "claimIds": ["er-lei-tv-theater"], "nodeIds": []},
        {"id": "l4", "era": "1980s", "phase": "spread", "period": "1983~1989", "title": "해외여행 자유화", "claimIds": ["c80-travel"], "nodeIds": ["e80-travel"]},
        {"id": "l5", "era": "1990s", "phase": "spread", "period": "1991~1999", "title": "노래방과 PC방", "claimIds": ["fl-mus-noraebang", "c90-pcbang"], "nodeIds": ["tr-t90-pcbang"]},
        {"id": "l6", "era": "2000s", "phase": "turn", "period": "2004~", "title": "주말 여가의 확산", "claimIds": ["c00-5day-leisure"], "nodeIds": ["tr-t00-weekend"]},
        {"id": "l7", "era": "2010s", "phase": "life", "period": "2013~2019", "title": "배달앱 — 집에서 먹는 여가", "claimIds": ["c10-delivery", "c10-syn-delivery"], "nodeIds": ["tr-t10-delivery"]},
        {"id": "l8", "era": "2020s", "phase": "now", "period": "2020~2022", "title": "코로나19 — 집 안으로 접힌 여가와 다시 나가기", "claimIds": ["c2020-spend", "c2020-endsd"], "nodeIds": ["tr-t20-untact"]},
    ],
    "links": [],
    "cross": [
        {"flow": "flow-time", "note": "여가가 늘어난 시간(밤·주말)은 생활시간 흐름에서 따로 본다."},
        {"flow": "flow-sports", "note": "스포츠 관람·참여는 스포츠 흐름에서 따로 본다."},
    ],
    "gaps": [
        "연도별 여가 시간(생활시간조사)은 아직 지표로 연결하지 않았다.",
        "1960년대 영화 관객 수의 연도별 공식 통계.",
        "노래방·PC방 이용이 극장·TV 이용을 대신했는지(대체인지 공존인지)를 보여주는 자료.",
    ],
    "alternatives": [
        "여가 장소의 변화를 기술(TV·인터넷·앱) 중심으로 설명하는 시각과, 소득·노동시간·정책(통금 해제·주5일) 중심으로 설명하는 시각이 함께 있다.",
    ],
}

_TIME = {
    "id": "flow-time",
    "question": "밤과 주말 — 일하지 않는 시간은 언제, 얼마나 생겼나?",
    "cats": ["society"],
    "span": [1960, 2025],
    "shape": "제도로 열린 시간 — 야간통행금지 해제(1982), 법정 근로시간 단축(2004)과 주52시간(2018)처럼 시간의 경계가 대부분 법과 제도로 바뀌었다.",
    "lede": ["c80-curfew", "er-time-2000s"],
    "indicators": [],
    "steps": [
        {"id": "h1", "era": "1960s", "phase": "before", "period": "1945~", "title": "밤에는 다닐 수 없던 시대(야간통행금지)", "claimIds": ["c80-curfew"], "nodeIds": []},
        {"id": "h2", "era": "1970s", "phase": "condition", "period": "1970년대", "title": "장시간 노동 — 근로시간 통계 미확보", "claimIds": [], "nodeIds": [],
         "empty": "1970년대 연간 근로시간을 같은 기준으로 보여주는 자료를 확보하지 못했다. 1970년 전태일의 근로기준법 준수 요구는 '산업과 일자리' 흐름에서 다룬다."},
        {"id": "h3", "era": "1980s", "phase": "turn", "period": "1982~1989", "title": "통금 해제와 24시간 영업의 시작", "claimIds": ["c80-curfew", "c80-ch-24h", "er-shop-cvs"], "nodeIds": ["e80-curfew"]},
        {"id": "h4", "era": "1990s", "phase": "condition", "period": "1990~1998", "title": "줄기 시작한 근로시간과 단축 논의", "claimIds": ["er-time-90s", "er-lei-5day-why"], "nodeIds": []},
        {"id": "h5", "era": "2000s", "phase": "turn", "period": "2004~2011", "title": "주5일 근무 — 주말이 생기다", "claimIds": ["c00-5day", "er-time-2000s"], "nodeIds": ["e00-5day"]},
        {"id": "h6", "era": "2010s", "phase": "spread", "period": "2018", "title": "주52시간 상한", "claimIds": ["c10-52h"], "nodeIds": ["e10-minwage"]},
        {"id": "h7", "era": "2020s", "phase": "now", "period": "2020~2022", "title": "코로나19 영업시간 제한과 해제", "claimIds": ["c2020-endsd"], "nodeIds": ["d20-endsd"]},
    ],
    "links": [],
    "cross": [
        {"flow": "flow-leisure", "note": "늘어난 시간이 어디에서 쓰였는지는 여가 공간 흐름에서 본다."},
        {"flow": "flow-shop", "note": "24시간 편의점은 유통의 변화이기도 하다."},
    ],
    "gaps": [
        "1960~80년대 연간 근로시간의 같은 기준 통계.",
        "야간 활동(심야 영업·야간 근무) 규모의 연속 통계.",
        "근로시간 단축이 여가 지출을 얼마나 늘렸는지 나눈 자료.",
    ],
    "alternatives": [
        "근로시간 감소를 법 개정의 결과로 보는 설명과, 서비스업 확대·시간제 일자리 증가 같은 구성 변화의 결과로 보는 설명이 함께 있다(OECD 통계는 시간제 근로자를 포함한다).",
    ],
}

_SPORTS = {
    "id": "flow-sports",
    "question": "스포츠는 '보는 것'과 '하는 것'으로 어떻게 바뀌었나?",
    "cats": ["culture"],
    "span": [1960, 2025],
    "shape": "관람의 상업화 — 동네 TV 앞 프로레슬링, 신문사가 주관한 고교야구에서 기업 구단의 프로야구로 옮겨 갔다. '하는 스포츠'(생활체육)의 장기 자료는 부족하다.",
    "lede": ["er-sp-hsbb", "er-lei-3s"],
    "indicators": [],
    "steps": [
        {"id": "sp1", "era": "1960s", "phase": "before", "period": "1960년대", "title": "TV 앞에 모인 프로레슬링과 첫 세계 우승", "claimIds": ["er-sp-60s"], "nodeIds": []},
        {"id": "sp2", "era": "1970s", "phase": "spread", "period": "1965~1981", "title": "고교야구의 전성기", "claimIds": ["er-sp-hsbb", "er-sp-why70"], "nodeIds": []},
        {"id": "sp3", "era": "1980s", "phase": "turn", "period": "1982~1988", "title": "프로야구 출범과 서울올림픽", "claimIds": ["c80-baseball", "er-lei-3s", "c80-olympic"], "nodeIds": ["e80-baseball", "e80-olympic"]},
        {"id": "sp4", "era": "1990s", "phase": "life", "period": "1997~1998", "title": "외환위기와 프로 스포츠팀 해체", "claimIds": ["c90-ch-imfdaily"], "nodeIds": []},
        {"id": "sp5", "era": "2000s", "phase": "spread", "period": "2002", "title": "월드컵 길거리 응원", "claimIds": ["c00-worldcup"], "nodeIds": ["e00-worldcup"]},
        {"id": "sp6", "era": "2010s", "phase": "spread", "period": "2010~", "title": "프로야구 누적 관중 1억 명", "claimIds": ["er-sp-100m"], "nodeIds": []},
        {"id": "sp7", "era": "2020s", "phase": "now", "period": "2020~2022", "title": "무관중 시즌과 관중 복귀", "claimIds": ["er-sp-2022"], "nodeIds": []},
    ],
    "links": [],
    "cross": [
        {"flow": "flow-politics", "note": "프로야구 출범은 1980년대 정권의 정책과 함께 해석된다(해석)."},
        {"flow": "flow-tech", "note": "TV 보급이 스포츠 관람 방식을 바꿨다."},
    ],
    "gaps": [
        "생활체육(직접 하는 스포츠) 참여율의 장기 자료 — 2020년대 동호회 참여 자료만 확보했다.",
        "프로 스포츠 관중 수의 연도별 통계는 아직 지표로 연결하지 않았다.",
        "1990년대 프로 스포츠의 변화(농구·축구 리그 등)는 조사하지 않았다.",
    ],
    "alternatives": [
        "프로야구 출범을 정권의 '3S 정책'으로 보는 해석과, 1970년대 고교야구 인기와 기업의 수요가 쌓인 결과로 보는 해석이 함께 있다.",
    ],
}

NEW_FLOWS = [f for f in NEW_FLOWS if f["id"] != "flow-leisure"] + [_LEISURE, _TIME, _SPORTS]

ERA_STATES["flow-leisure"] = {
    "1960s": "극장 영화가 대표 여가",
    "1970s": "TV가 안방으로 — 보급률 79%(1979)",
    "1980s": "해외여행 자유화(1989)",
    "1990s": "노래방과 PC방",
    "2000s": "주5일 근무 뒤 주말 여가 확산",
    "2010s": "배달앱 — 집에서 먹는 여가",
    "2020s": "코로나19로 집 안에, 2022년 다시 밖으로",
}
ERA_STATES["flow-time"] = {
    "1960s": "야간통행금지 — 밤에는 다닐 수 없음",
    "1970s": "통금 지속, 근로시간 통계 미확보",
    "1980s": "통금 해제(1982), 24시간 편의점(1989)",
    "1990s": "근로시간 감소 시작, 단축 논의(1998)",
    "2000s": "주5일 근무(2004~), 연 2,512→2,090시간",
    "2010s": "주52시간 상한(2018)",
    "2020s": "코로나19 영업시간 제한과 해제",
}
ERA_STATES["flow-sports"] = {
    "1960s": "TV 앞 프로레슬링, 첫 세계 우승",
    "1970s": "신문사 주관 고교야구의 전성기",
    "1980s": "프로야구 출범(1982), 서울올림픽",
    "1990s": "외환위기로 프로팀 해체",
    "2000s": "월드컵 길거리 응원(2002)",
    "2010s": "프로야구 누적 관중 1억 명",
    "2020s": "무관중 시즌 뒤 관중 복귀",
}

BRIDGES["flow-leisure"] = [
    B("1960s", "1970s", "correlation", "TV가 1960년대 중반부터 대중화되며 극장 관객의 발길이 뜸해졌다. 씨네21은 TV만이 원인은 아니었다고 덧붙인다.", ["er-lei-60s", "er-lei-tv-theater"]),
    B("1970s", "1980s", "interpretation", "신군부가 '자율화'를 내세워 해외여행 규제를 완화했다는 해석이 있다. 1983년 50세 이상 제한 허용 뒤 1989년 전면 자유화되었다.", ["er-lei-3s", "c80-travel"]),
    B("1980s", "1990s", "interpretation", "외환위기 실직자·명예퇴직자와 초고속망 구축이 맞물려 PC방이 늘었다는 설명이 있다. 노래방은 1991년 부산에서 시작해 이듬해 1만 곳을 넘었다.", ["c90-syn-chain", "fl-mus-noraebang"]),
    B("1990s", "2000s", "condition", "1998년 시작된 근로시간 단축 논의가 2004년 주5일 근무로 이어졌고, 국가기록원은 이를 여가·가족·문화생활 확산의 전환점으로 평가한다.", ["er-lei-5day-why", "c00-5day-leisure"]),
    B("2000s", "2010s", "condition", "1인 가구·맞벌이 증가와 스마트폰 결제가 배달앱 수요를 키웠다는 분석이 있다.", ["c10-syn-delivery"]),
    B("2010s", "2020s", "correlation", "배달이 이미 늘던 중에 코로나19가 겹쳐 문화·오락 지출 비중은 줄고 배달 시장은 2.6배가 되었다. 2022년 거리두기 해제로 다시 밖으로 나갔다.", ["c2020-spend", "c20-delivery", "c2020-endsd"]),
]
BRIDGES["flow-time"] = [
    B("1960s", "1970s", "sequence", "통금은 그대로였다. 1970년대 근로시간 변화를 보여주는 자료는 확보하지 못했다."),
    B("1970s", "1980s", "condition", "정부는 1982년 통금 해제의 배경으로 개방사회 구현과 아시안게임·올림픽을 앞둔 국가 이미지 개선을 들었다. 정치적 관심을 돌리려는 '자율화'의 하나였다는 해석도 있다.", ["c80-curfew", "er-lei-3s"]),
    B("1980s", "1990s", "sequence", "밤 시간이 풀린 뒤에도 일하는 시간 자체는 1990년대에야 줄기 시작했다. 통금 해제와 근로시간 감소를 잇는 자료는 없다.", ["er-time-90s"]),
    B("1990s", "2000s", "causal", "1998년 노사정위원회에서 시작된 근로시간 단축 논의가 2003년 근로기준법 개정으로 입법되어 2004년부터 단계적으로 시행되었다.", ["er-lei-5day-why", "c00-5day"]),
    B("2000s", "2010s", "sequence", "연간 근로시간은 2011년까지 줄었다가 다시 오르내렸고, 2018년 주 최대 근로시간이 68시간에서 52시간으로 줄었다.", ["er-time-2000s", "c10-52h"]),
    B("2010s", "2020s", "sequence", "법이 정한 시간과 별개로, 2020~22년에는 감염병 방역이 영업시간과 모임 시간을 직접 제한했다.", ["c2020-endsd"]),
]
BRIDGES["flow-sports"] = [
    B("1960s", "1970s", "interpretation", "1960년대 도시화·산업화와 실업야구팀 증설, 전국체전 지방 개최로 지어진 야구장이 1970년대 고교야구 성장의 조건이었다는 연구가 있다.", ["er-sp-why70"]),
    B("1970s", "1980s", "interpretation", "고교야구의 지역 대결 인기가 지역 연고제 프로야구의 바탕이 되었다는 설명과, 정권이 정치적 관심을 돌리려 했다는 '3S 정책' 해석이 함께 있다.", ["er-sp-hsbb", "er-lei-3s"]),
    B("1980s", "1990s", "sequence", "기업이 운영하던 프로 팀은 외환위기 때 해체되기도 했다(국가기록원 기록).", ["c90-ch-imfdaily"]),
    B("1990s", "2000s", "sequence", "2002년 월드컵에서 길거리 응원 인파가 52만 명에서 700만 명으로 늘었다. 1990년대 팀 해체와 잇는 자료는 없다.", ["c00-worldcup"]),
    B("2000s", "2010s", "sequence", "프로야구 누적 관중이 2010년 1억 명을 넘었다.", ["er-sp-100m"]),
    B("2010s", "2020s", "sequence", "코로나19로 관중이 제한되었다가 2022년 3년 만에 제한 없는 시즌이 열렸다.", ["er-sp-2022"]),
]

# ─────────────────────────────────────────────────────────────
# 대분류(8)와 경제 판단과의 관계
#   econ.status: linked(경제 판단 경로가 근거로 확인됨) / partial(일부만 확인) / context(문화·역사적 맥락 — 경제 전망 근거로 쓰지 않음)
# ─────────────────────────────────────────────────────────────
DOMAINS = [
    {"id": "politics", "label": "정치·제도"},
    {"id": "economy", "label": "경제·금융"},
    {"id": "industry", "label": "산업·기술·일자리"},
    {"id": "life", "label": "생활·도시·주거"},
    {"id": "culture", "label": "문화·여가"},
    {"id": "style", "label": "패션·미용·자기표현"},
    {"id": "consumption", "label": "소비·쇼핑"},
    {"id": "relations", "label": "관계·모임·공동체"},
]

FLOW_META = {
    "flow-politics": {"domain": "politics", "topic": "정치 참여와 권력", "econ": {"status": "context", "note": "정치 변화가 경제에 미친 경로는 이 흐름에서 검증하지 않았다. 경제 전망의 근거로 쓰지 않는다."}},
    "flow-economy": {"domain": "economy", "topic": "위기와 대응", "econ": {"status": "linked", "note": "외부 충격이 물가·외환·금리를 거쳐 가계와 기업에 전달된 경로를 시대별로 본다. 가계 소비로 이어지는 부분은 대표 분석에서 끝까지 따라간다.", "analysis": "an-consumption"}},
    "flow-jobs": {"domain": "industry", "topic": "산업구조와 고용", "econ": {"status": "partial", "note": "산업 구조와 고용 형태의 변화는 통계로 확인했지만, 이것이 소득·소비로 이어진 크기는 연결하지 않았다."}},
    "flow-tech": {"domain": "industry", "topic": "기술 보급(가정·개인 기기)", "econ": {"status": "partial", "note": "기기 보급이 유통·관계 방식을 바꾼 연결은 다른 흐름에서 일부 확인했다. 소비 지출 규모와의 관계는 연결하지 않았다."}},
    "flow-city": {"domain": "life", "topic": "교통·도시·주거", "econ": {"status": "partial", "note": "신도시·아파트 공급과 집값의 관계는 기사 정리 수준으로만 확인했다. 주거비와 소비 여력의 관계는 대표 분석에서 다룬다.", "analysis": "an-consumption"}},
    "flow-family": {"domain": "life", "topic": "가족·가구", "econ": {"status": "partial", "note": "가구 축소·고령화가 소비 성향을 낮춘다는 분석(대한상의)을 대표 분석에서 다룬다. 이 흐름 자체에서는 인과 크기를 확인하지 않았다.", "analysis": "an-consumption"}},
    "flow-time": {"domain": "life", "topic": "생활시간", "econ": {"status": "partial", "note": "근로시간 단축이 여가 수요를 키웠다는 평가(국가기록원)는 있지만 지출 증가 크기를 나눈 자료는 없다."}},
    "flow-music": {"domain": "culture", "topic": "음악의 유통·청취", "econ": {"status": "partial", "note": "음반 시장 급감과 스트리밍 전환은 매출 자료로 확인했다. 다른 소비로의 파급은 확인하지 않았다."}},
    "flow-sports": {"domain": "culture", "topic": "스포츠 관람·참여", "econ": {"status": "context", "note": "관중·구단 운영의 경제 자료를 연결하지 않았다. 문화적 맥락으로만 쓴다."}},
    "flow-leisure": {"domain": "culture", "topic": "여가 공간", "econ": {"status": "partial", "note": "코로나19 때 문화·오락 지출 비중 변화는 국민계정으로 확인했다. 장기 여가 지출 추이는 지표(오락·문화 지출 비중)로만 본다."}},
    "flow-fashion": {"domain": "style", "topic": "의복의 생산·유통", "econ": {"status": "partial", "note": "유통 채널 변화(패션몰→SPA→플랫폼)는 기사·기업 매출로 확인했다. 시장 규모 연속 통계는 없다."}},
    "flow-expression": {"domain": "style", "topic": "꾸미기와 사회적 인식", "econ": {"status": "context", "note": "자기표현의 변화가 특정 지출을 만들었다는 근거는 확인하지 못했다. 문화적 맥락으로만 쓴다."}},
    "flow-shop": {"domain": "consumption", "topic": "유통 채널과 결제", "econ": {"status": "linked", "note": "결제 수단(신용카드)의 확산이 2003년 소비 급감으로 이어진 경로가 연구로 확인된다. 대표 분석의 비교 국면으로 쓴다.", "analysis": "an-consumption"}},
    "flow-relations": {"domain": "relations", "topic": "만남의 경로와 모임", "econ": {"status": "context", "note": "서비스 가입·설치 자료는 실제 만남·지출과 다르다. 모임 앱 시장 등 경제적 연결은 확인하지 못했다."}},
}

# 관계·모임: 자료가 무엇을 재는지(가입·설치·이용·참여)와 앞뒤 변화의 관계(교체·공존·추가)
STEP_MEASURE = {
    ("flow-relations", "r0"): "제도·운영 방식 설명 — 이용자 수 자료 없음",
    ("flow-relations", "r0b"): "회고와 해석",
    ("flow-relations", "r1b"): "전화 회선 수(인프라) — 통화량이 아님",
    ("flow-relations", "r2"): "서비스 개시·가입(회사 기록)",
    ("flow-relations", "r3"): "개설 카페 수·가입 회원(회사 발표) — 실제 활동이 아님",
    ("flow-relations", "r4"): "개설 카페 수 — 실제 활동이 아님",
    ("flow-relations", "r5"): "가입자·월간 이용자",
    ("flow-relations", "r6"): "앱 설치 수 — 실제 모임 참여가 아님",
    ("flow-relations", "r7"): "참여율(정부 조사)",
}
BRIDGE_CHANGE = {
    "flow-relations": ["공존", "추가", "추가", "일부 이동", "교체(PC→모바일)", "공존"],
    "flow-music": ["추가", "공존", "추가", "교체", "추가", "일부 이동"],
    "flow-shop": ["추가", "추가", "추가", "공존", "추가", "공존"],
    "flow-leisure": ["일부 이동", "추가", "추가", "추가", "추가", "왕복"],
    "flow-fashion": ["추가", "추가", "추가", "일부 이동", "추가", "일부 이동"],
}
