"""산업 일대기 — 한 산업을 시작부터 지금까지 같은 대상으로 따라간다(R-M1~M6).

분류: 상위 분야(group) → 개별 산업(industry). 넓은 산업은 세부 흐름(track)으로 나눈다(인터넷: 접속 / 서비스·사업모델).
단계(stage)마다 '무엇이 달라졌나(what)'와 '왜 달라졌나(why)', 그리고 '앞 단계의 무엇이 이것을 가능하게/어렵게 했나(from)'를 쓴다.
다른 산업과 만나는 지점은 단계에 섞지 않고 links로 따로 둔다.
층위: fact / source / inference / hypothesis (stories.py와 같다).
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


def C(id, text, ctype, sources, period=None, scope=None):
    d = {"id": id, "text": text, "claimType": ctype, "status": "sourced", "sourceIds": sources,
         "domains": ["industry", "economy"], "countries": ["KR"], "aiSynthesized": False}
    if period:
        d["period"] = period
    if scope:
        d["scope"] = scope
    return d


def L(layer, text, ids=()):
    assert layer in ("fact", "source", "inference", "hypothesis")
    return {"layer": layer, "text": text, "ids": list(ids)}


SOURCES = [
    # 철강
    S("ix-posco-50", "포항 1기 종합준공 50주년(포스코의 어제와 내일)", "포스코 뉴스룸", "https://newsroom.posco.com/kr/?p=96407", "company", published="2023-07"),
    S("ix-posco-steel1", "50년 동안 포스코 기술력 산실이 된 포항제철소 1제강공장", "포스코 뉴스룸", "https://newsroom.posco.com/kr/?p=97632", "company", published="2023"),
    S("ix-seoul-980901", "적자 모르는 초우량 경영/제철보국 30년", "서울신문", "https://www.seoul.co.kr/news/1998/09/01/19980901008001", "news", published="1998-09-01"),
    S("ix-twig-251209", "철강보국 신화 쓴 포스코… 친환경 미래소재로 재도약", "한국일보(twig24)", "https://twig24.com/news/2025/12/09/20251209020002", "news", published="2025-12-09"),
    S("ix-sidae-260407", "포스코·현대제철 조강생산 3년 연속 동반 하락", "머니투데이(시대 재게시)", "https://www.sidae.com/article/2026040715224021172", "news", published="2026-04-07"),
    S("ix-ibto-250916", "(철강 구조조정)① 침체 악순환…고리 끊을 '구조조정' 절실", "IB토마토", "https://www.ibtomato.com/View.aspx?no=16077&type=1", "news", published="2025-09-16"),
    S("ix-nocut-steel", "'철강 관세 50% 위기'…정부, 구조조정과 수소환원제철 전환", "노컷뉴스", "https://www.nocutnews.co.kr/news/6422853", "news", published="2025"),
    S("ix-khan-260805", "EU 신철강 조치(무관세 쿼터 축소·초과분 50% 관세)", "경향신문", "https://www.khan.co.kr/article/202608052034035", "news", published="2026-08-05"),
    S("ix-weekly-ship", "[특집] 한국 조선 기름때 벗고 세계로(후판 공급)", "주간경향", "https://weekly.khan.co.kr/article/11557", "news"),
    # 조선
    S("ix-aju-200614", "韓조선산업 일으킨 정주영의 '500원권 신화'", "아주경제", "https://www.ajunews.com/view/20200614133259034", "news", published="2020-06-14"),
    S("ix-motir-ship", "한국 조선산업 연표(정부 자료)", "산업통상부", "https://www.motir.go.kr/attach/down/095a2dda9c864e1d90d751f7668a1117/8d1fda7a7fb4d2ef604bb8e788e12671", "government"),
    S("ix-archives-ship", "기록으로 보는 자동차·조선", "국가기록원", "https://theme.archives.go.kr/next/koreaOfRecord/carShipbuld.do", "government"),
    S("ix-ks-ship2006", "창립 10년 만인 1983년, 세계 1위 조선업체로 부상", "KoreaScience(학회지 기사)", "https://koreascience.kr/article/JAKO200656605498801.pdf", "academic", published="2006-02"),
    S("ix-daum-250522", "LNG선 초호황도 끝물 온다…값싼 '중국 상선' 압도하라", "한국일보(다음 재게시)", "https://v.daum.net/v/20250522110003887", "news", published="2025-05-22"),
    S("ix-dealsite-ship", "'골든타임' 남았다 — 조선업 시황 인터뷰(양종서 박사)", "딜사이트", "https://dealsite.co.kr/articles/154040", "news", published="2025"),
    S("ix-daum-250506", "[조선강국의 귀환<중>] 인력난·하청구조…호황의 그늘", "다음(언론 재게시)", "https://v.daum.net/v/20250506000112300", "news", published="2025-05-06"),
    S("ix-dailian-lng", "[韓제조업, 이러다 다 죽어②] 슈퍼 사이클에도 불안한 K조선", "데일리안", "https://www.dailian.co.kr/news/view/1469284", "news"),
    S("ix-tf-masga", "'마스가 프로젝트'…대한민국 산업 살리는 마중물 된 조선", "더팩트", "https://news.tf.co.kr/read/economy/2275592.htm", "news", published="2025-12"),
    S("ix-mtn-mro", "K-조선 새 먹거리 MRO는 노다지?", "머니투데이방송", "https://news.mtn.co.kr/news-detail/2026101407595228974", "news", published="2026-10-14"),
    # 반도체
    S("ix-sec-64k", "1983년 64K D램 개발(삼성 반도체 이야기)", "삼성반도체 뉴스룸", "https://news.samsungsemiconductor.com/kr/?p=12017", "company"),
    S("ix-sec-40y", "삼성 반도체사업 40년 도전과 창조의 역사", "삼성반도체 뉴스룸", "https://news.samsungsemiconductor.com/kr/삼성-반도체사업-40년-도전과-창조의-역사/", "company"),
    S("ix-etnews-160907", "[한국 반도체 50년]<9> 메모리 반도체 세계 평정", "전자신문", "https://m.etnews.com/20160907000235", "news", published="2016-09-07"),
    S("ix-hk-260213", "키몬다의 몰락 — 2008년 D램 치킨게임", "한국경제", "https://www.hankyung.com/article/202602133465i", "news", published="2026-02-13"),
    S("ix-sedaily-241231", "반도체 위기마다 경제 휘청", "서울경제", "https://m.sedaily.com/article/14002127", "news", published="2024-12-31"),
    S("ix-ceoscore-250625", "올해 전 세계 반도체 시장 규모 7009억달러(트렌드포스 HBM 점유율)", "CEO스코어데일리", "https://ceoscoredaily.com/page/view/2025062513472605379", "news", published="2025-06-25", origin="트렌드포스"),
    S("ix-daum-251230", "사상 첫 7000억달러 수출고지…반도체·대만이 견인차", "다음(언론 재게시)", "https://v.daum.net/v/20251230110722827", "news", published="2025-12-30"),
    S("ix-kiwoom-share", "반도체 수출 비중 확대(리포트)", "키움증권", "https://bbn.kiwoom.com/rfSI1262", "report", published="2026-02"),
    S("ix-tomato-gartner", "삼전·하닉 글로벌 매출 2·3위…메모리 의존도 가중(가트너)", "뉴스토마토", "https://newstomato.com/ReadNews.aspx?no=1287805", "news", published="2026", origin="가트너"),
    # 인터넷
    S("ix-imaeil-040619", "'인터넷, 세상을 바꾸었다' — 코넷 10년", "매일신문", "https://www.imaeil.com/page/view/2004061910160092187", "news", published="2004-06-19"),
    S("ix-seoul-021107", "초고속인터넷 1천만시대 — ADSL·PC방이 고속성장 견인", "서울신문", "https://www.seoul.co.kr/news/2002/11/07/20021107010005", "news", published="2002-11-07"),
    S("ix-etri-2002", "초고속 인터넷 서비스 가입자 추정(전자통신동향분석)", "ETRI(KoreaScience)", "https://koreascience.kr/article/JAKO200265349329421.pdf", "academic", published="2002-12"),
    S("ix-archives-net", "초고속인터넷망 보급(정책 기록)", "국가기록원", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=406", "government"),
    S("ix-kyeonggi-991002", "초고속인터넷 가입 급증(모뎀·PC방 요금 비교)", "경기일보", "https://www.kyeonggi.com/article/199910020113645", "news", published="1999-10-02"),
    S("ix-inews-portal", "인터넷 20년 — 포털의 등장(심마니·야후·네이버)", "아이뉴스24", "https://www.inews24.com/view/831508", "news", published="2014"),
    S("ix-seoul-070326", "본격적인 포털 시대(야후 디렉토리 검색)", "서울신문", "https://www.seoul.co.kr/news/2007/03/26/20070326003006", "news", published="2007-03-26"),
    S("ix-aju-220904", "네이버 지식iN 20주년", "아주경제", "https://www.ajunews.com/view/20220904115926862", "news", published="2022-09-04"),
    S("ix-weekly-130225", "[특집|디지털 기억] 온라인 서비스 판도 변화(프리챌 유료화 등)", "주간경향", "https://weekly.khan.co.kr/article/201302251623081", "news", published="2013-02-25"),
]

CLAIMS = [
    # ── 철강
    C("ix-st-73", "포항제철소 1기 설비는 1973년 7월 3일 종합준공해 국내 최초 일관제철소가 됐다(조강 연산 103만 톤). 1958년부터 정부 주도로 다섯 차례 종합제철 건설이 계획됐다가 무산됐고, 대일청구권 자금을 전용해 건설했다. 포스코는 이 설비가 있었기에 같은 해 중화학공업화 선언(철강·석유화학·기계·조선·자동차·전자)을 할 수 있었다고 설명한다.",
      "fact", ["ix-posco-50"], period="1958~1973"),
    C("ix-st-72", "1제강공장 준공 직전인 1972년 한국 전체 조강 생산량은 58만 톤 수준이었는데, 준공으로 단숨에 두 배 규모인 103만 톤 생산능력을 확보했다.",
      "fact", ["ix-posco-steel1"], period="1972~1973"),
    C("ix-st-self", "조강 자급도는 1967년 47%에서 1981년 포항 4기 준공 뒤 89%로 올랐다. 포스코는 외환위기 이후 대기업 가운데 첫 민영화 대상이 됐다.",
      "fact", ["ix-twig-251209"], period="1967~2000"),
    C("ix-st-97", "포항제철의 연간 철강 생산능력은 1997년 2,643만 톤으로 세계 2위 규모였다. 1973년 103만 톤에서 25년 만에 40배 넘게 커졌고, 외환위기 뒤 정부 지분 매각(민영화)이 추진됐다.",
      "fact", ["ix-seoul-980901"], period="1973~1998"),
    C("ix-st-plate", "국내 조선업계는 해마다 500만 톤 이상의 후판(선박용 두꺼운 철판)이 필요하고, 그중 70% 가량을 포스코와 동국제강이 공급한다는 보도가 있다. 전문가들은 원활한 후판 공급을 한국 조선업의 강점으로 꼽았다.",
      "source", ["ix-weekly-ship"], period="2000년대"),
    C("ix-st-25", "포스코와 현대제철의 조강 생산량은 2023~2025년 3년 연속 함께 줄었다(현대제철 2022년 1,958만 톤 → 2025년 1,768만 톤). 한국신용평가는 2025년 국내 철강 수요를 약 4,340만 톤(전년 대비 −9.2%, 2010년 이후 최저)으로 추산했다. 중국은 자국 부동산 침체로 남은 철강을 2024년 1억 1천만 톤 수출했고, 미국은 2025년 6월 철강 관세를 25%에서 50%로 올렸다.",
      "fact", ["ix-sidae-260407"], period="2022~2026"),
    C("ix-st-cut", "포스코는 2024년 11월 1선재 공장을 폐쇄했고 현대제철은 2025년 포항 2공장 가동을 멈췄으며, 철근업계는 가동률을 50~60%대로 낮췄다. 포항시 인구는 2025년 8월 49만 7,943명으로 50만 명 아래로 떨어졌고, 기사는 철강 고용 감소를 원인으로 풀이했다.",
      "fact", ["ix-ibto-250916"], period="2024~2025"),
    C("ix-st-next", "정부는 중국산 과잉 공급과 미국 50% 관세에 대응해 설비 규모 조정 유도와 '산업위기 선제대응지역' 지정, 수소환원제철 전환을 추진했다. 포스코는 2050년 탄소중립을 목표로 석탄 대신 수소로 철을 만드는 수소환원제철 기술을 개발 중이다. EU는 2026년 7월부터 무관세 쿼터를 줄이고 초과분에 50% 관세를 매겨, 한국 쿼터는 258만 톤에서 207만 3천 톤으로 줄었다.",
      "fact", ["ix-nocut-steel", "ix-posco-50", "ix-khan-260805"], period="2025~2026"),
    # ── 조선
    C("ix-sh-72", "현대는 영국 차관을 얻어 1972년 3월 23일 울산 미포만에 조선소를 착공했고, 조선소 건설과 26만 톤급 유조선 2척 건조를 동시에 진행해 1974년 6월 28일 준공식 겸 1·2호선 명명식을 열었다.",
      "fact", ["ix-aju-200614"], period="1972~1974"),
    C("ix-sh-pre", "1972년 현대가 울산에 초대형 조선소를 짓기 전 한국 조선업은 연간 건조량 50만 G/T로 세계 시장점유율 1%에도 못 미쳤고, 선박 건조 경험과 숙련 기술자가 거의 없었다.",
      "fact", ["ix-ks-ship2006"], period="1972 이전"),
    C("ix-sh-timeline", "정부 연표에 따르면 1973년 대한조선공사 옥포조선소(현 한화), 1974년 삼성중공업이 생겼고, 1976년 조선해운 종합육성방안이 나왔다. 현대중공업은 1983년 세계 최대 선박 건조사가 됐고, 1999년 한국 조선소가 세계 1~3위를 처음 차지했으며, 2000년 선박 수주 세계 1위(점유율 35.8%)에 올랐다. 선박은 2009년과 2011년 수출 품목 1위였고, 2015년 대규모 적자와 구조조정을 겪었다.",
      "fact", ["ix-motir-ship"], period="1973~2016"),
    C("ix-sh-cargo", "정부는 1976년 '해운조선종합육성방안'을 발표해 우리 화물은 우리가 건조한 선박으로 실어 나르게 했다.",
      "fact", ["ix-archives-ship"], period="1976"),
    C("ix-sh-crash", "직전 호황(2000년대 중반~2010년대 초)이 끝난 뒤 2014~2016년 해운경기 침체·유가 하락·중국 조선업 부상으로 '수주 절벽'이 왔다. HD현대중공업은 2015~2018년 사내 하청을 포함한 인력의 절반인 약 3만 3천 명을 줄였고, 삼성중공업은 약 5,400명 감축을 실행했으며, 대우조선해양은 정부 지원 속 강도 높은 구조조정을 했다.",
      "fact", ["ix-daum-250522"], period="2014~2018"),
    C("ix-sh-skill", "2016년 채권단 주도 구조조정 때 많은 숙련공이 조선소를 떠났고, 2021년부터 세계 발주가 크게 늘자 인력을 구하지 못해 비숙련 외국인을 데려올 수밖에 없었다는 진단이 있다. 조선업 이주노동자는 2021년 약 4,500명에서 2023년 약 1만 8천 명으로 늘었다.",
      "source", ["ix-dealsite-ship", "ix-daum-250506"], period="2016~2023"),
    C("ix-sh-lng", "2021~2024년 미국·러시아·카타르 등의 LNG 생산 프로젝트로 수백 척 규모의 LNG선 발주가 몰려 조선 3사의 '슈퍼사이클'이 왔다. 2025년 1분기 발주량은 2021~2024년 평균보다 약 60% 적었다는 분석이 나왔다.",
      "fact", ["ix-daum-250522"], period="2021~2025"),
    C("ix-sh-china", "선박 가치 평가 기관 배슬스밸류에 따르면 한국 조선사의 LNG선 수주 점유율은 2021년 87%에서 (기사 기준) 지난해 62%로 떨어졌고, 같은 해 중국의 전체 선박 수주 점유율은 70.6%로 한국(16.7%)을 크게 앞섰다.",
      "fact", ["ix-dailian-lng"], period="2021~2024", scope="기사 발행 시점의 '지난해' 기준"),
    C("ix-sh-masga", "2025년 한·미 조선 협력 '마스가(MASGA)' 프로젝트에 1,500억 달러 규모 투자가 예정됐고, 함정 유지·보수·정비(MRO)가 첫 협력 분야로 떠올랐다. 한편 국내에서 건조한 LNG선 대부분은 중국 조선소에서 정비를 받는다.",
      "fact", ["ix-tf-masga", "ix-mtn-mro"], period="2025~2026"),
    # ── 반도체
    C("ix-cp-83", "삼성은 1983년 12월 1일 64K D램 개발에 성공해 미국·일본과 10년 넘게 벌어져 있던 기술 격차를 4년 정도로 줄였다고 설명한다. 당시 반도체 사업은 인구 1억 명·GNP 1만 달러·국내 소비 50% 이상이 돼야 가능하다는 평가가 있었다.",
      "source", ["ix-sec-64k", "ix-sec-40y"], period="1983"),
    C("ix-cp-92", "가트너(당시 데이터퀘스트) 자료로 1991년 메모리 반도체 1위는 일본 NEC였고 삼성전자는 5위였다. 삼성전자는 1989년 일본과 같은 시기에 16M D램을, 1992년 8월 일본보다 먼저 64M D램을 개발했고, 1992년 D램 시장에서 처음 세계 1위가 됐다.",
      "fact", ["ix-etnews-160907"], period="1989~1992"),
    C("ix-cp-08", "2007년 이후 D램 업계의 대규모 증설 경쟁으로 공급 과잉이 생긴 데다 2008년 금융위기가 겹쳐 D램 가격이 2007년 대비 85% 떨어졌다. 독일 키몬다는 2009년 1월 파산보호를 신청했다. 2008년 3분기 삼성전자 반도체는 2,400억 원 흑자, 하이닉스는 4,600억 원 적자였다.",
      "fact", ["ix-hk-260213"], period="2007~2009"),
    C("ix-cp-hbm", "SK하이닉스는 2013년 세계 최초로 HBM(여러 층으로 쌓아 데이터를 빠르게 주고받는 메모리)을 개발했고, 2024년 하반기 엔비디아 AI 가속기에 HBM3E 납품을 시작했다. 트렌드포스 기준 2024년 HBM 점유율은 SK하이닉스 52.5%, 삼성전자 42.4%였다.",
      "fact", ["ix-sedaily-241231", "ix-ceoscore-250625"], period="2013~2024"),
    C("ix-cp-cycle", "반도체 수출 증가율은 2023년 −23.7%에서 2025년 17.8%로 바뀌었다. 같은 기간 전 세계 서버용 반도체 매출은 780억 달러에서 1,560억 달러로 두 배가 됐고, 스마트폰·PC용은 소폭 늘었다.",
      "fact", ["ix-daum-251230"], period="2023~2025"),
    C("ix-cp-share", "전체 수출에서 반도체 비중은 2024년 20.8%에서 2025년 24.4%, 2026년 1월 31.2%로 커졌다. 리포트는 반도체 경기가 수출·기업 이익·주식시장·거시경제 전반에 주는 영향이 커졌다고 지적했다.",
      "source", ["ix-kiwoom-share"], period="2024~2026"),
    C("ix-cp-rank", "가트너 집계로 2025년 반도체 매출은 엔비디아(1,257억 달러)에 이어 삼성전자(725억 달러) 2위, SK하이닉스(606억 달러) 3위였다.",
      "fact", ["ix-tomato-gartner"], period="2025"),
    # ── 인터넷
    C("ix-nt-94", "1994년 6월 20일 KT는 아시아 최초의 상용 인터넷 서비스 '코넷'을 열었다. 대중화를 이끈 것은 1999년부터 기존 전화선으로 최고 10Mbps가 넘는 속도를 낸 ADSL이었고, 2002년 초고속 인터넷 가입자가 1천만 명을 넘었다. 인터넷 매출은 1999년 364억 원에서 2003년 3조 7천억 원이 됐다.",
      "fact", ["ix-imaeil-040619"], period="1994~2003"),
    C("ix-nt-adsl", "초고속 인터넷은 두루넷이 1998년 케이블 모뎀으로 처음 시작했지만, 이후 ADSL 시장을 놓고 KT와 하나로통신이 벌인 경쟁 속에서 커졌다는 평가가 일반적이다(2002년 보도). 가입자는 1998년 1만 3,800가구, 1999년 말 37만, 2000년 말 400만, 2001년 말 약 800만이었다.",
      "fact", ["ix-seoul-021107", "ix-etri-2002"], period="1998~2001"),
    C("ix-nt-policy", "정부는 1994년 4월 '초고속정보통신기반구축 종합계획'을 세우고 망 구축과 PC 보급을 국가 과제로 삼았으며, 2001년 10월 초고속 인터넷 보급률 세계 1위, 2002년 11월 가입자 1천만 명을 기록했다.",
      "fact", ["ix-archives-net"], period="1994~2002"),
    C("ix-nt-price", "1999년 기사에 따르면 전화선 모뎀은 평균 60시간 쓰는 데 7만 원가량 들었고 PC방은 시간당 1,500~2,000원이었지만, ADSL·케이블 모뎀은 월 3만~4만 원에 전화요금 부담 없이 1~10Mbps로 쓸 수 있어 가정용 가입이 늘었다.",
      "fact", ["ix-kyeonggi-991002"], period="1999"),
    C("ix-nt-portal", "국내 포털의 시초는 1996년 2월 심마니였고, 1997년 들어온 야후코리아가 디렉토리 검색으로 시장을 장악했다. 1999년 시작한 네이버는 2002년 10월 이용자가 묻고 답하는 '지식iN'을 내놓은 뒤 1년 만에 1위 검색 엔진이 됐다고 회사는 밝힌다.",
      "fact", ["ix-inews-portal", "ix-seoul-070326", "ix-aju-220904"], period="1996~2003"),
    C("ix-nt-freechal", "한때 가입자 1천만 명에 이르렀던 프리챌은 2002년 유료화 선언 뒤 이용자가 떠났고, 1999년 만든 아이러브스쿨은 1년 만에 회원 500만 명을 모았다가 쇠락했다.",
      "fact", ["ix-weekly-130225"], period="1999~2002"),
]

GROUPS = [
    {"id": "light", "label": "경공업", "desc": "많은 손으로 실·옷을 만들던 산업"},
    {"id": "heavy", "label": "중공업·소재", "desc": "쇳물·배·화학처럼 큰 설비로 만드는 산업"},
    {"id": "elec", "label": "전자·반도체", "desc": "부품과 기기를 만드는 산업"},
    {"id": "net", "label": "인터넷·플랫폼", "desc": "연결과 그 위의 서비스"},
]

INDUSTRIES = [
    {
        "id": "steel", "group": "heavy", "label": "철강",
        "tracks": "쇳물(조강) 생산 — 고로·제강·압연, 이후 수요처(조선·자동차·건설)와 수출",
        "question": "'산업의 쌀'이던 철강은 왜 지금 공장을 줄이고 있나?",
        "span": [1958, 2026],
        "stages": [
            {"period": "1958~1973", "kind": "시작", "what": "다섯 번 무산된 끝에 첫 일관제철소(포항, 연산 103만 톤)",
             "why": [L("fact", "1958년부터 다섯 차례 계획이 무산됐고, 대일청구권 자금을 돌려 써서야 지을 수 있었다.", ["ix-st-73"]),
                     L("fact", "준공 직전 한국 전체 조강 생산은 58만 톤이었는데, 이 한 설비로 두 배 규모가 됐다.", ["ix-st-72"])],
             "from": L("inference", "공업화 계획(1960년대)이 철을 쓰는 산업을 키우려 했지만 쇠를 수입해야 했다. 쇠를 직접 만들어야 다음 산업이 가능하다는 판단이 시작점이다.", ["cfill-plan2", "ix-st-73"])},
            {"period": "1973~1997", "kind": "성장", "what": "설비 확장 — 생산능력 103만 톤 → 2,643만 톤(세계 2위), 자급도 47% → 89%",
             "why": [L("fact", "포스코는 1기 설비가 있었기에 같은 해 철강·조선·자동차 등을 키우는 중화학공업화 선언이 가능했다고 설명한다.", ["ix-st-73"]),
                     L("fact", "생산능력은 25년 만에 40배 넘게 늘었고, 조강 자급도는 1981년 89%가 됐다.", ["ix-st-97", "ix-st-self"])],
             "from": L("inference", "쇳물이 안정적으로 나오자 조선소·자동차 공장이 철판을 국내에서 싸게 살 수 있게 됐고, 그 수요가 다시 제철소 확장을 정당화했다 — 철강과 수요 산업이 서로를 키운 구조로 본다.", ["ix-st-73", "ix-st-plate"])},
            {"period": "1998~2010년대", "kind": "재편", "what": "외환위기 뒤 민영화, 조선·자동차용 고급 강판",
             "why": [L("fact", "외환위기 뒤 포스코는 대기업 1호 민영화 대상이 됐다.", ["ix-st-self", "ix-st-97"]),
                     L("source", "조선업계가 해마다 쓰는 후판의 70% 가량을 국내 철강사가 공급한다는 보도가 나올 만큼 조선과 묶였다.", ["ix-st-plate"])],
             "from": L("inference", "양을 늘리던 단계가 끝나자 수요 산업(조선·자동차)이 요구하는 '품질'이 경쟁 기준이 됐다.", ["ix-st-plate"])},
            {"period": "2023~2026", "kind": "위기", "what": "3년 연속 생산 감소, 공장 폐쇄·가동 중단, 포항 인구 50만 아래",
             "why": [L("fact", "국내 철강 수요는 2025년 약 4,340만 톤으로 15년 만에 가장 적었고, 중국은 남는 철강을 대량 수출했으며, 미국은 관세를 50%로 올렸다.", ["ix-st-25"]),
                     L("fact", "선재·철근 공장이 멈추거나 문을 닫았고, 포항시 인구가 50만 명 아래로 떨어졌다.", ["ix-st-cut"])],
             "from": L("inference", "성장기에 키운 대형 설비는 수요가 줄면 고정비가 그대로 남는다. 건설 경기 침체(내수)와 무역 장벽(수출)이 동시에 오며 큰 설비가 짐이 됐다.", ["ix-st-25", "ix-st-cut"])},
            {"period": "현재~", "kind": "현재", "what": "설비 조정 + 수소환원제철로의 전환 모색",
             "why": [L("fact", "정부는 설비 조정 유도와 위기지역 지정, 수소환원제철 전환을 추진하고, EU도 쿼터를 줄이고 초과분에 50% 관세를 매기기 시작했다.", ["ix-st-next"])],
             "from": L("inference", "'얼마나 많이'보다 '탄소를 덜 내며 무엇을' 만드느냐가 다음 경쟁 기준이 되고 있다.", ["ix-st-next"])},
        ],
        "profile": {
            "start": [L("fact", "자금·기술이 없어 다섯 차례 무산, 대일청구권 자금과 일본의 기술 지원으로 시작.", ["ix-st-73"])],
            "base": [L("fact", "포항(1973)과 광양 두 일관제철소 중심. 지금은 포스코와 현대제철이 대표.", ["ix-st-73", "ix-st-25"])],
            "product": [L("inference", "쇳물을 대량으로 만드는 단계에서, 선박용 후판·자동차 강판 같은 고급 강재로, 이제는 탄소를 덜 내는 공정(수소환원)으로.", ["ix-st-plate", "ix-st-next"])],
            "customers": [L("source", "조선·자동차·건설·기계. 후판의 큰 몫이 조선으로 간다.", ["ix-st-plate"])],
            "turns": [L("fact", "1973 준공, 1990년대 대형화, 외환위기 뒤 민영화, 2023~ 감산·폐쇄.", ["ix-st-73", "ix-st-97", "ix-st-25"])],
            "trade": [L("fact", "중국산 과잉 공급, 미국 50% 관세, EU 쿼터 축소.", ["ix-st-25", "ix-st-next"])],
            "jobs": [L("fact", "포항은 철강 고용 감소와 함께 인구 50만 명 선이 무너졌다.", ["ix-st-cut"])],
            "now": [L("inference", "강점: 고급 강재와 조선·자동차와의 오랜 공급망. 약점: 줄어든 내수, 무역 장벽, 탄소 배출이 큰 고로 공정.", ["ix-st-25", "ix-st-next"])],
            "watch": [L("hypothesis", "볼 지표: 국내 철강 수요, 중국 감산 실행, 미국·EU 관세, 수소환원제철 투자와 일정. 반대 신호: 건설 경기 반등과 관세 완화가 함께 오면 감산 압력이 줄어든다.", ["ix-st-25", "ix-st-next"])],
        },
        "links": [
            {"year": "1970년대~", "to": "shipbuilding", "rel": "공급", "text": "후판(선박용 철판)을 조선소에 공급 — 조선 성장의 바탕", "line": L("source", "국내 후판의 큰 몫이 조선으로 간다.", ["ix-st-plate"])},
            {"year": "2023~", "to": "shipbuilding", "rel": "엇갈림", "text": "조선은 호황, 철강은 감산 — 같은 공급망 안에서 경기가 갈렸다", "line": L("inference", "조선 호황이 철강 전체를 살리지 못한 것은 철강 수요의 큰 축인 건설이 부진했기 때문으로 본다.", ["ix-st-25", "ix-sh-lng"])},
        ],
    },
    {
        "id": "shipbuilding", "group": "heavy", "label": "조선",
        "tracks": "상선(유조선·컨테이너선·LNG선) 건조와 수주, 이후 해양플랜트·함정·정비(MRO)",
        "question": "배를 만들어 본 적도 없던 나라가 어떻게 1위가 됐고, 왜 호황에도 불안할까?",
        "span": [1972, 2026],
        "stages": [
            {"period": "1972 이전", "kind": "이전 상태", "what": "연 50만 G/T, 세계 점유율 1% 미만",
             "why": [L("fact", "선박 건조 경험과 숙련 기술자가 거의 없었다.", ["ix-sh-pre"])],
             "from": L("inference", "배를 만들 철과 자본, 일감이 모두 부족했다.", ["ix-sh-pre"])},
            {"period": "1972~1976", "kind": "시작", "what": "울산 조선소를 지으면서 동시에 유조선 2척 건조, 옥포·삼성 등 대형 조선소 잇달아",
             "why": [L("fact", "영국 차관으로 착공해 조선소와 배를 동시에 지었고, 1974년 준공·명명식을 열었다.", ["ix-sh-72"]),
                     L("fact", "정부는 1976년 '우리 화물은 우리 배로' 원칙의 해운조선 육성방안을 냈다.", ["ix-sh-cargo", "ix-sh-timeline"])],
             "from": L("inference", "1973년 포항제철 준공으로 국산 철판을 쓸 수 있게 된 시점과 겹친다. 중화학공업화 선언의 6대 산업에 조선이 들어 있었다.", ["ix-st-73"])},
            {"period": "1983~2011", "kind": "성장", "what": "건조량 세계 1위(1983), 수주 세계 1위(2000, 35.8%), 수출 품목 1위(2009·2011)",
             "why": [L("fact", "현대중공업은 1983년 세계 최대 건조사가 됐고, 1999년 한국 조선소가 세계 1~3위를 처음 차지했다.", ["ix-sh-timeline"]),
                     L("source", "국내 철강사가 후판을 원활하게 공급한 것이 강점으로 꼽혔다.", ["ix-st-plate"])],
             "from": L("inference", "대형 도크와 철강 공급망이 먼저 갖춰져 있었기에, 2000년대 세계 해운 호황 때 대량 수주를 소화할 수 있었다.", ["ix-sh-timeline", "ix-st-plate"])},
            {"period": "2014~2018", "kind": "위기", "what": "수주 절벽 — 대규모 적자와 인력 절반 감축",
             "why": [L("fact", "해운 침체·유가 하락·중국 부상으로 수주가 끊겼고, 대형 3사가 수만 명을 줄였다.", ["ix-sh-crash", "ix-sh-timeline"])],
             "from": L("inference", "호황기에 늘린 인력과 설비가 일감이 끊기자 고정비가 됐다 — 조선은 수주와 인도 사이가 2~3년 벌어지는 산업이라 호황과 불황의 진폭이 크다.", ["ix-sh-crash"])},
            {"period": "2021~2025", "kind": "재편", "what": "LNG선 슈퍼사이클, 그러나 숙련공 부족·하청·이주노동자 의존",
             "why": [L("fact", "LNG 프로젝트로 수백 척이 발주됐지만, 구조조정 때 떠난 숙련공 대신 이주노동자가 늘었다.", ["ix-sh-lng", "ix-sh-skill"]),
                     L("fact", "LNG선 점유율은 87%에서 62%로 줄고 중국이 전체 수주의 70%를 가져갔다.", ["ix-sh-china"])],
             "from": L("inference", "앞 단계의 대규모 감원이 이번 호황의 발목을 잡았다. 일감은 돌아왔지만 사람은 바로 돌아오지 않는다.", ["ix-sh-crash", "ix-sh-skill"])},
            {"period": "현재~", "kind": "현재", "what": "미국 협력(MASGA)·정비(MRO)·친환경 선박으로 다음 일감 찾기",
             "why": [L("fact", "1,500억 달러 규모 한·미 협력과 함정 정비가 떠올랐지만, 국내에서 지은 LNG선의 정비는 대부분 중국에서 한다.", ["ix-sh-masga"])],
             "from": L("hypothesis", "건조만으로는 호황·불황을 피하기 어려워, 배를 지은 뒤의 정비·개조처럼 꾸준한 일감으로 넓히려는 움직임으로 본다.", ["ix-sh-masga", "ix-sh-lng"])},
        ],
        "profile": {
            "start": [L("fact", "경험·기술자·자금이 없던 상태에서 차관과 정부 육성책으로 시작.", ["ix-sh-pre", "ix-sh-72", "ix-sh-cargo"])],
            "base": [L("fact", "울산(현대), 거제 옥포(대우→한화), 삼성중공업.", ["ix-sh-timeline"])],
            "product": [L("fact", "유조선 → 컨테이너선 → LNG선·해양플랜트 → 친환경 연료선·함정 정비.", ["ix-sh-72", "ix-sh-lng", "ix-sh-masga"])],
            "customers": [L("inference", "해외 선주와 에너지 기업. 수요는 해운 운임과 에너지 프로젝트에 따라 크게 출렁인다.", ["ix-sh-lng", "ix-sh-crash"])],
            "turns": [L("fact", "1974 첫 인도, 1983 건조 1위, 2000 수주 1위, 2015~18 구조조정, 2021~ 슈퍼사이클.", ["ix-sh-72", "ix-sh-timeline", "ix-sh-crash", "ix-sh-lng"])],
            "trade": [L("fact", "중국의 저가 대량 수주, 미국과의 안보·산업 협력.", ["ix-sh-china", "ix-sh-masga"])],
            "jobs": [L("fact", "구조조정 때 인력 절반 감축, 호황기엔 이주노동자 4배 증가.", ["ix-sh-crash", "ix-sh-skill"])],
            "now": [L("inference", "강점: 고부가 선종 기술과 대형 설비. 약점: 숙련공 부족, 하청 구조, 중국의 점유율.", ["ix-sh-skill", "ix-sh-china"])],
            "watch": [L("hypothesis", "볼 지표: 세계 발주량(1분기 이미 평균보다 60% 적음), 선가, 숙련 인력 확보, 미국 MRO 수주. 반대 신호: 발주 급감과 선가 하락이 함께 오면 다시 하강기.", ["ix-sh-lng", "ix-sh-masga"])],
        },
        "links": [
            {"year": "1973~", "to": "steel", "rel": "수요", "text": "철강의 큰 고객 — 후판 수요", "line": L("source", "후판의 70% 가량을 국내 철강사가 공급.", ["ix-st-plate"])},
        ],
    },
    {
        "id": "semiconductor", "group": "elec", "label": "반도체(메모리)",
        "tracks": "메모리 반도체(D램·낸드, 이후 HBM) — 기술 세대, 가격 사이클, 수요처(PC → 모바일 → AI 서버)",
        "question": "늦게 출발한 한국 메모리는 어떻게 1위가 됐고, 왜 지금 수출이 반도체에 쏠렸나?",
        "span": [1983, 2026],
        "stages": [
            {"period": "1983", "kind": "시작", "what": "64K D램 개발 — 격차를 10년 넘게에서 4년 정도로",
             "why": [L("source", "당시엔 인구 1억·GNP 1만 달러가 돼야 가능한 사업이라는 평가가 있었지만 진입했다.", ["ix-cp-83"]),
                     L("fact", "미국·일본에 이어 세 번째로 64K D램을 개발하고 1984년 기흥 공장을 준공했다.", ["c80-64k"])],
             "from": L("inference", "TV 같은 가전 생산(1960~70년대)으로 전자 부품 수요와 공장 운영 경험이 쌓여 있었다.", ["c60-kr-tv-5"])},
            {"period": "1989~1992", "kind": "성장", "what": "16M(일본과 동시) → 64M(일본보다 먼저) → 1992년 D램 세계 1위",
             "why": [L("fact", "1991년 메모리 1위는 일본 NEC, 삼성은 5위였는데 1992년 D램 1위가 됐다.", ["ix-cp-92"])],
             "from": L("inference", "메모리는 세대마다 먼저 개발해 먼저 대량 생산한 회사가 높은 가격을 받는다. 앞 세대에서 따라잡은 양산 경험이 다음 세대를 먼저 내는 바탕이 됐다.", ["ix-cp-92"])},
            {"period": "2007~2009", "kind": "위기", "what": "D램 치킨게임 — 가격 85% 하락, 키몬다 파산",
             "why": [L("fact", "증설 경쟁에 금융위기가 겹쳐 가격이 폭락했고, 같은 분기 삼성은 흑자·하이닉스는 적자였다.", ["ix-cp-08"])],
             "from": L("inference", "불황기에 버틴 회사가 남은 시장을 가져가는 구조라, 이 위기 뒤 메모리 업체 수가 줄고 한국 업체의 비중이 커졌다고 본다.", ["ix-cp-08"])},
            {"period": "2013~2025", "kind": "기술 변화", "what": "HBM(쌓아 올린 고속 메모리) — AI 서버가 새 수요처",
             "why": [L("fact", "SK하이닉스가 2013년 처음 개발해 2024년 엔비디아에 납품했고, 2024년 HBM 점유율은 두 회사 합쳐 95%였다.", ["ix-cp-hbm"]),
                     L("fact", "서버용 반도체 매출이 2023~2025년 두 배가 되며 반도체 수출 증가율이 −23.7%에서 17.8%로 돌아섰다.", ["ix-cp-cycle"])],
             "from": L("inference", "PC·스마트폰 수요가 정체된 자리에 AI 데이터센터라는 새 수요처가 생겼다. 쌓는 기술을 먼저 준비한 쪽이 앞섰다.", ["ix-cp-hbm", "ix-cp-cycle"])},
            {"period": "현재", "kind": "현재", "what": "수출의 4분의 1~3분의 1이 반도체 — 한국 경제가 메모리 사이클에 묶임",
             "why": [L("fact", "반도체 수출 비중은 2024년 20.8%, 2025년 24.4%, 2026년 1월 31.2%였다. 2025년 삼성전자·SK하이닉스는 세계 반도체 매출 2·3위였다.", ["ix-cp-share", "ix-cp-rank"]),
                     L("fact", "같은 해 15대 수출품 중 9개는 줄어 '반도체 착시'라는 평가가 나왔다.", ["c20-chip-risk"])],
             "from": L("inference", "반도체 호황이 GDP를 끌어올렸지만 가계 소득으로 넓게 퍼지지 않은 것이 지금 경제 분석의 핵심 질문과 이어진다.", ["ix-cp-share", "an-n-kdi"])},
        ],
        "profile": {
            "start": [L("source", "작은 내수·늦은 출발이라는 불리함 속 진입.", ["ix-cp-83"])],
            "base": [L("fact", "기흥(1984) 등 대형 생산 라인. 삼성전자와 SK하이닉스.", ["c80-64k", "ix-cp-rank"])],
            "product": [L("fact", "D램 세대(64K → 64M) → 낸드 → HBM.", ["ix-cp-92", "ix-cp-hbm"])],
            "customers": [L("fact", "PC → 스마트폰 → AI 서버로 이동.", ["ix-cp-cycle"])],
            "turns": [L("fact", "1983 진입, 1992 1위, 2008 치킨게임, 2023 불황, 2024~ AI 호황.", ["ix-cp-92", "ix-cp-08", "ix-cp-cycle"])],
            "trade": [L("fact", "미국 반도체법(2022) 보조금 등 각국의 공장 유치 경쟁.", ["c20-chips"])],
            "jobs": [L("inference", "고용은 설비에 비해 적고 고숙련 중심이라, 수출 호황이 넓은 고용·임금으로 바로 이어지지 않는다.", ["an-n-kdi", "ix-cp-share"])],
            "now": [L("inference", "강점: 메모리·HBM 기술과 양산. 약점: 한 품목·몇몇 고객(AI 투자)에 대한 의존.", ["ix-cp-hbm", "ix-cp-share"])],
            "watch": [L("hypothesis", "볼 지표: 빅테크 AI 투자, HBM 가격·점유율, 반도체 수출 비중. 반대 신호: AI 투자 둔화와 메모리 가격 하락이 함께 오면 2023년 같은 급감 가능.", ["ix-cp-cycle", "c20-chip-risk"])],
        },
        "links": [
            {"year": "1960~70년대", "to": "tv", "rel": "바탕", "text": "가전(TV) 생산 — 전자 부품 수요와 공장 경험", "line": L("fact", "TV 한 대를 만들려면 300여 종의 부품이 들어가, 가전 생산이 전자 부품 수요를 만들었다.", ["c60-kr-tv-5"])},
            {"year": "2009~", "to": "internet", "rel": "수요", "text": "스마트폰·데이터센터 — 인터넷 서비스가 메모리를 쓴다", "line": L("inference", "모바일 인터넷과 AI 서비스가 커질수록 서버·휴대폰용 메모리 수요가 커진다.", ["ix-cp-cycle", "c00-kr-iphone"])},
        ],
    },
    {
        "id": "internet", "group": "net", "label": "인터넷",
        "tracks": "① 접속 인프라(모뎀 → ADSL·케이블 → 무선) ② 서비스·사업모델(PC통신 → 포털·검색 광고 → 모바일 메신저·커머스 → AI)",
        "question": "전화선 모뎀에서 손안의 AI까지 — 사람들은 왜 매번 다른 입구로 옮겨 갔나?",
        "span": [1994, 2026],
        "stages": [
            {"period": "1994~1998", "kind": "시작", "what": "[접속] 코넷 상용 서비스, 전화선 모뎀 / [서비스] PC통신·초기 포털",
             "why": [L("fact", "1994년 6월 KT가 아시아 첫 상용 인터넷 '코넷'을 열었고, 1996년 심마니, 1997년 야후코리아가 포털 시대를 열었다.", ["ix-nt-94", "ix-nt-portal"]),
                     L("fact", "모뎀은 60시간에 7만 원가량 들었다.", ["ix-nt-price"])],
             "from": L("inference", "쓴 만큼 돈을 내는 전화선 접속이라 '오래 머무는' 이용이 어려웠다.", ["ix-nt-price"])},
            {"period": "1998~2002", "kind": "확산", "what": "[접속] 케이블·ADSL 정액제, 가입자 1만 → 1천만 / [이용] PC방",
             "why": [L("fact", "두루넷이 1998년 시작하고 KT·하나로가 ADSL로 경쟁하며 가입자가 1998년 1만 3,800가구에서 2002년 1천만 명이 됐다. 정부는 1994년부터 망 구축을 국가 과제로 삼았다.", ["ix-nt-adsl", "ix-nt-policy"]),
                     L("fact", "ADSL은 월 3만~4만 원 정액에 전화요금 부담이 없었다.", ["ix-nt-price"])],
             "from": L("inference", "정액제가 '켜 두는 인터넷'을 가능하게 해, 게임(PC방)·커뮤니티·검색처럼 오래 머무는 서비스의 바탕이 됐다.", ["ix-nt-price", "c90-pcbang"])},
            {"period": "2002~2009", "kind": "전환점", "what": "[서비스] 검색 포털 경쟁 — 지식iN으로 네이버 1위, 무료 커뮤니티 경쟁",
             "why": [L("fact", "네이버는 2002년 이용자가 묻고 답하는 지식iN 뒤 1년 만에 1위 검색이 됐다고 밝힌다. 같은 해 유료화한 프리챌에서는 이용자가 떠났다.", ["ix-nt-portal", "ix-nt-freechal"]),
                     L("fact", "PC통신은 초고속 인터넷과 포털이 나오며 급격히 위축됐다.", ["fl-rel-pctong-cost"])],
             "from": L("inference", "접속이 정액이 되자 서비스는 '공짜로 사람을 모으고 광고로 버는' 모델로 갔다. 유료화는 이용자를 내쫓았고, 이용자가 직접 만든 글(지식iN)이 검색의 무기가 됐다.", ["ix-nt-portal", "ix-nt-freechal"])},
            {"period": "2009~2019", "kind": "전환점", "what": "[접속] 스마트폰 / [서비스] 메신저(카카오톡)·모바일 쇼핑·배달 앱",
             "why": [L("fact", "스마트폰 가입자는 2009년 말 약 80만에서 2010년 말 약 722만이 됐고, 카카오톡은 2012년 가입자 5천만을 넘었다. 모바일쇼핑은 2015년 온라인쇼핑의 절반에 이르렀다.", ["c00-kr-iphone", "c10-kakao", "fl-shop-mobile"])],
             "from": L("inference", "PC 앞에 앉아야 하던 인터넷이 손에 들어오자, 입구가 '검색창'에서 '메신저·앱'으로 옮겨 갔다. PC 기반 미니홈피의 쇠퇴도 같은 이동이다.", ["c00-cy-decline", "c10-kakao"])},
            {"period": "2022~현재", "kind": "현재", "what": "[서비스] 생성형 AI — 검색·쇼핑의 입구가 다시 바뀌는 중",
             "why": [L("fact", "생성형 AI를 써 봤다는 국민은 2025년 44.5%로 1년 새 11.2%p 늘었다.", ["er-tech-ai"])],
             "from": L("hypothesis", "검색 광고로 벌던 포털이 AI 답변으로 바뀌는 시기다. 입구가 바뀔 때마다 1위가 바뀌었던 역사(야후 → 네이버, 포털 → 메신저)가 반복될지가 관전 지점이다.", ["ix-nt-portal", "er-tech-ai"])},
        ],
        "profile": {
            "start": [L("fact", "1994년 정부 종합계획과 KT 코넷.", ["ix-nt-policy", "ix-nt-94"])],
            "base": [L("fact", "통신사(KT·하나로·두루넷) 경쟁, 공공 망 투자.", ["ix-nt-adsl", "ix-nt-policy"])],
            "product": [L("fact", "모뎀 → ADSL·케이블 → 스마트폰 / PC통신 → 포털 → 메신저·앱 → AI.", ["ix-nt-94", "ix-nt-portal", "c10-kakao", "er-tech-ai"])],
            "customers": [L("inference", "처음엔 학생·직장인 중심의 PC 이용자, 지금은 전 연령의 모바일 이용자. 돈을 내는 쪽은 이용자보다 광고주·판매자가 많다.", ["ix-nt-portal", "fl-shop-mobile"])],
            "turns": [L("fact", "1994 상용화, 2002 1천만, 2002 지식iN, 2009 스마트폰, 2010 카카오톡.", ["ix-nt-94", "ix-nt-portal", "c00-kr-iphone", "c10-kakao"])],
            "trade": [L("inference", "접속은 국내 통신사가, 서비스는 국내 포털과 해외 플랫폼(유튜브 등)이 경쟁한다 — 음악 앱에서 유튜브 뮤직이 1위가 된 것처럼.", ["sx-ytm"])],
            "jobs": [L("fact", "PC방 창업(1998년 100여 곳 → 1999년 1만 5천 곳), 배달 라이더 같은 플랫폼 노동이 생겼다.", ["c90-pcbang", "c10-syn-delivery"])],
            "now": [L("inference", "강점: 빠른 망과 높은 모바일 이용. 약점: 입구(검색·앱)를 해외 플랫폼과 AI에 내줄 위험.", ["sx-ytm", "er-tech-ai"])],
            "watch": [L("hypothesis", "볼 지표: AI 이용률, 포털 검색 점유율, 앱별 이용자 수. 반대 신호: AI 이용이 늘어도 국내 포털 이용이 유지되면 '입구 교체'가 아니라 공존.", ["er-tech-ai", "sx-ytm"])],
        },
        "links": [
            {"year": "1998~", "to": None, "rel": "여가", "text": "PC방과 온라인게임 — 접속 정액제가 만든 여가", "line": L("fact", "PC방은 1998년 초 100여 개에서 1999년 말 1만 5천 개가 됐다.", ["c90-pcbang"]), "goFlow": ["flow-leisure", "l5"]},
            {"year": "2013~", "to": None, "rel": "유통", "text": "모바일 쇼핑·배달 앱 — 쇼핑의 입구가 앱으로", "line": L("fact", "모바일쇼핑은 2015년 온라인쇼핑의 절반이 됐다.", ["fl-shop-mobile"]), "goFlow": ["flow-shop", "s6"]},
            {"year": "2009~", "to": "semiconductor", "rel": "수요", "text": "스마트폰·서버가 메모리를 쓴다", "line": L("inference", "모바일·AI 서비스가 메모리 수요를 키운다.", ["ix-cp-cycle"])},
        ],
    },
]

from industries_more import MORE_SOURCES, MORE_CLAIMS, MORE_INDUSTRIES, MORE_STEEL_LINKS, MORE_SEMI_LINKS  # noqa: E402

SOURCES += MORE_SOURCES
CLAIMS += MORE_CLAIMS
import industries_more2 as _im2  # noqa: E402
SOURCES += _im2.SOURCES
CLAIMS += _im2.CLAIMS
INDUSTRIES += _im2.INDUSTRIES
import industries_world as _iwm  # noqa: E402
SOURCES += _iwm.SOURCES
CLAIMS += _iwm.CLAIMS
INDUSTRIES += MORE_INDUSTRIES
for _ind in INDUSTRIES:
    if _ind["id"] == "steel":
        _ind["links"] += MORE_STEEL_LINKS
    if _ind["id"] == "semiconductor":
        _ind["links"] += MORE_SEMI_LINKS

PENDING = []

KINDS = ["이전 상태", "시작", "성장", "확산", "전환점", "기술 변화", "위기", "재편", "현재"]
PROFILE = [("start", "시작 조건과 수요"), ("base", "생산 기반과 주요 기업"), ("product", "제품과 기술의 변화"), ("customers", "고객과 수요처"),
           ("turns", "성장·위기·재편의 전환점"), ("trade", "경쟁국·무역·정책"), ("jobs", "일자리·지역경제"), ("now", "지금의 강점과 약점"), ("watch", "앞으로 볼 지표와 반대 신호")]


def validate(claims_all, flows):
    cids = {c["id"] for c in claims_all}
    fsteps = {f["id"]: {s["id"] for s in f["steps"]} for f in flows}
    ids = {i["id"] for i in INDUSTRIES}

    def chk(x, w):
        if x["layer"] in ("fact", "source") and not x["ids"]:
            raise SystemExit(f"산업 {w}: 사실에 근거 없음")
        for i in x["ids"]:
            if i not in cids:
                raise SystemExit(f"산업 {w}: 없는 근거 {i}")

    for ind in INDUSTRIES:
        for st in ind["stages"]:
            if st["kind"] not in KINDS:
                raise SystemExit(f"{ind['id']}: 단계 종류 {st['kind']}")
            for x in st["why"]:
                chk(x, ind["id"])
            chk(st["from"], ind["id"])
        for k, _ in PROFILE:
            if not ind["profile"].get(k):
                raise SystemExit(f"{ind['id']}: 항목 '{k}' 비어 있음")
            for x in ind["profile"][k]:
                chk(x, f"{ind['id']}/{k}")
        for ln in ind["links"]:
            chk(ln["line"], f"{ind['id']} 연결")
            if ln["to"] and ln["to"] not in ids:
                raise SystemExit(f"{ind['id']}: 없는 산업 {ln['to']}")
            if ln.get("goFlow") and ln["goFlow"][1] not in fsteps.get(ln["goFlow"][0], set()):
                raise SystemExit(f"{ind['id']}: 없는 흐름 단계 {ln['goFlow']}")
    import industries_world as _iw
    sel = _iw.apply(INDUSTRIES, claims_all)
    return {"groups": GROUPS, "industries": INDUSTRIES, "pending": PENDING, "profile": [{"key": k, "label": t} for k, t in PROFILE], "selection": sel}
