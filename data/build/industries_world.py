"""18차: 산업 선정 기준(R-IN1), 세계시장 속 역할과 세계 → 한국 경로(R-IN2·R-W), 한국 산업이 밖으로 준 영향(R-IN3),
여러 갈래의 미래 가능성(R-FU1·R-Q12)과 이야기형 결론(R-Q14).

- 사실(fact)·출처 해석(source)은 이미 검증된 근거 문장(ix-*, fl-*, c*)이나 이 파일의 새 근거 문장에만 기댄다.
- 추론(inference)·가설(hypothesis)은 이 사이트가 이어 붙인 설명이다. 확률·시점 단정은 쓰지 않는다.
"""
from topic_helpers import C, F, FUT, HYP, INF, S, SRC, WORLD, CONCLUDE

SOURCES = [
    S("iw-kidd-textile", "한국 섬유 및 가발산업과 우리 수출(한국무역협회 국제무역연구원 보고서 보도)", "산업일보(kidd.co.kr)",
      "https://kidd.co.kr/news/178527", "news"),
    S("iw-ppss-chip", "반도체 수출의 위상 변화(수출 1위 품목 변천)", "ppss.kr", "https://ppss.kr/archives/134172", "news"),
    S("iw-nd-display", "디스플레이 산업: 2004년 이후 17년 세계 1위, 2021년 중국에 2위로", "뉴데일리 경제",
      "https://biz.newdaily.co.kr/site/data/html/2023/05/08/2023050800004.amp.html", "news", "2023-05-08"),
    S("iw-etnews-display", "韓디스플레이, 세계 1위 中에 내줬다", "전자신문", "https://www.etnews.com/20220413000245", "news", "2022-04-13"),
    S("iw-inews-display", "디스플레이 산업 주요 통계(한국디스플레이산업협회 발표 보도)", "아이뉴스24", "https://www.inews24.com/view/1589717", "news", "2023-04-27"),
]

CLAIMS = [
    C("iw-textile", "한국무역협회 국제무역연구원 보고서 보도에 따르면 섬유는 1970년 한국의 수출 1위 품목이었고, 1980년대 후반 이후 중화학공업 육성·인건비 상승·후발 개도국 추격으로 경쟁력이 약해졌다. 섬유 수출은 2000년 187억 달러로 최고치를 기록한 뒤 주춤했고, 노동집약적 봉제는 중국·베트남으로 생산기지가 옮겨 갔다.",
      "fact", ["iw-kidd-textile"], period="1970~2014", domains=("industry",)),
    C("iw-top1", "1977~2017년 수출 1위 품목을 차지한 횟수는 반도체 21회, 의류 12회, 선박 5회, 자동차·석유제품 각 1회였고, 1980년대 초반 수출 1위 품목은 의류(전체 수출의 11.7%)였다는 정리가 있다.",
      "statistical", ["iw-ppss-chip"], period="1977~2017", domains=("industry",)),
    C("iw-display", "한국 디스플레이 산업은 2004년부터 17년간 매출 기준 세계 1위였지만, 정부 지원 속에 대형 LCD 설비를 늘린 중국에 밀려 2021년 2위가 됐다(2021년 중국 41.5%, 한국 33.2%). 한국 기업은 국내 LCD TV 패널 생산 중단을 결정하고 OLED로 사업을 옮겼다.",
      "fact", ["iw-nd-display", "iw-etnews-display"], period="2004~2022", domains=("industry",)),
    C("iw-oled", "한국디스플레이산업협회는 2022년 세계 디스플레이 시장 점유율을 중국 42.5%, 한국 36.9%로 발표했고, 전체 시장에서 OLED 비중은 2021년 27.3%에서 2022년 34.3%로 커졌다며 한국이 OLED 확대를 주도했다고 밝혔다.",
      "fact", ["iw-inews-display"], period="2021~2022", domains=("industry",)),
]

CRITERIA = [
    {"key": "export", "label": "수출·부가가치"},
    {"key": "jobs", "label": "고용·지역"},
    {"key": "tech", "label": "기술·생산성"},
    {"key": "spill", "label": "다른 산업으로 번진 영향"},
    {"key": "history", "label": "역사적 중요성"},
]

# 선정표 — 근거가 있는 칸만 채우고, 확인하지 못한 칸은 '확인 전'으로 둔다.
SELECTION = [
    {"label": "철강", "status": "선정", "industry": "steel",
     "cells": {"export": F("1997년 생산능력 세계 2위 규모.", "ix-st-97"), "jobs": F("포항 인구가 철강 고용 감소와 함께 50만 아래로.", "ix-st-cut"),
               "spill": SRC("조선이 쓰는 후판의 약 70%를 국내 철강사가 공급.", "ix-st-plate"), "history": F("중화학공업화 선언의 바탕이 된 첫 일관제철소(1973).", "ix-st-73")}},
    {"label": "조선", "status": "선정", "industry": "shipbuilding",
     "cells": {"export": F("수출 1위 품목을 5번 차지(1977~2017).", "iw-top1"), "jobs": F("구조조정 때 인력 절반 감축, 호황기 이주노동자 4배.", "ix-sh-crash", "ix-sh-skill"),
               "tech": F("유조선 → LNG선·친환경선.", "ix-sh-lng"), "history": F("점유율 1% 미만에서 1983년 건조량 세계 1위.", "ix-sh-pre", "ix-sh-timeline")}},
    {"label": "반도체", "status": "선정", "industry": "semiconductor",
     "cells": {"export": F("수출 1위 21회, 2026년 1월 수출의 31.2%.", "iw-top1", "ix-cp-share"), "tech": F("1992년 D램 1위, HBM 세계 최초 개발.", "ix-cp-92", "ix-cp-hbm"),
               "spill": INF("휴대폰·TV 같은 완제품 산업의 부품 기반.", "ix-ph-fold"), "history": F("1983년 64K D램으로 늦은 진입.", "ix-cp-83")}},
    {"label": "자동차", "status": "선정", "industry": "automobile",
     "cells": {"export": F("2025년 수출 719억 달러로 역대 최대.", "ix-au-tariff"), "jobs": INF("완성차 도시와 부품 협력사가 함께 움직인다.", "c60-kr-ulsan-1"),
               "tech": F("2010년 생산 세계 5위.", "ix-au-rank"), "spill": INF("철강(강판)·마이카 생활과 연결.", "fl-city-cars")}},
    {"label": "석유화학", "status": "선정", "industry": "petrochem",
     "cells": {"export": F("중국이 최대 수출처(2019년 44%).", "ix-pc-cn"), "jobs": F("단지별 감축 협약이 지역경제 영향 최소화를 함께 다룸.", "ix-pc-cut"),
               "spill": INF("플라스틱·섬유 원료를 공급하는 소재 산업.", "ix-pc-72"), "history": F("1972년 첫 NCC — 미국·유럽보다 20~30여 년 늦은 출발.", "ix-pc-72")}},
    {"label": "가전(TV)", "status": "선정", "industry": "tv",
     "cells": {"export": F("2006년부터 매출 기준 세계 1위.", "ix-tv-06", "ix-tv-25"), "tech": F("브라운관 → LCD·LED → 프리미엄.", "ix-tv-06"),
               "history": F("첫 국산 흑백TV(1966), 컬러TV 허용(1980).", "c80-colortv")}},
    {"label": "휴대폰", "status": "선정", "industry": "phone",
     "cells": {"export": F("2011년 세계 스마트폰 1위.", "ix-ph-gs"), "tech": F("1996년 세계 최초 CDMA 상용화.", "c90-cdma"),
               "history": F("LG의 철수(2021)로 국내 제조사 하나만 남음.", "ix-ph-lg")}},
    {"label": "건설", "status": "선정", "industry": "construction",
     "cells": {"export": F("1970~80년대 중동 건설과 2025년 해외 원전 수주.", "c70-kr-mideast", "ix-cn-25"), "jobs": F("2024년 종사자 수 3년 7개월 만에 최소.", "ix-cn-24"),
               "spill": INF("아파트 공급이 주거·소비 방식과 연결.", "fl-city-apt")}},
    {"label": "인터넷·플랫폼", "status": "선정", "industry": "internet",
     "cells": {"tech": F("2001년 초고속 인터넷 보급률 세계 1위.", "ix-nt-policy"), "jobs": F("PC방 창업, 배달 라이더 같은 플랫폼 노동.", "c90-pcbang", "c10-syn-delivery"),
               "spill": INF("쇼핑·음악·만남의 입구가 됐다.", "fl-shop-mobile")}},
    {"label": "섬유·의류", "status": "후속",
     "cells": {"export": F("1970년 수출 1위, 의류는 1977~2017년 수출 1위 12회.", "iw-textile", "iw-top1"),
               "history": F("2000년 수출 최고치 뒤 봉제 생산기지가 해외로.", "iw-textile")},
     "note": "산업화 초기를 이해하는 데 꼭 필요하다. 시작 조건·고용 규모 자료를 모은 뒤 일대기로 만든다. 지금은 옷의 생산·유통 시대 흐름에서 일부를 다룬다."},
    {"label": "디스플레이", "status": "후속",
     "cells": {"export": F("2004~2020년 매출 기준 세계 1위, 2021년 중국에 2위.", "iw-display"), "tech": F("LCD에서 OLED로 — 2022년 OLED 비중 확대를 한국이 주도.", "iw-oled")},
     "note": "TV·휴대폰과 부품으로 이어져 있어 다음 일대기 후보 1순위. 지금은 TV 일대기 안에서만 언급된다."},
    {"label": "전자부품·기계", "status": "후속", "cells": {},
     "note": "수출 비중이 크지만 품목이 넓어 하나의 대상을 정하지 못했다. 품목을 좁힌 뒤(예: 2차전지) 다시 검토한다."},
    {"label": "가발·신발 등 경공업", "status": "제외", "cells": {"history": F("가발 수출은 1990년을 정점으로 하락했다가 2005년 이후 다시 올랐다.", "iw-textile")},
     "note": "1960~70년대에는 중요했지만 지금 한국 경제 구조를 설명하는 비중은 작다고 판단했다. 시대별 사건(1960년대 수출 품목)에서만 다룬다."},
]
STATUS = ("선정", "후속", "제외")

# 산업별: 세계 → 한국 경로(worlds), 한국이 밖으로 준 영향(outward), 미래(futures), 결론(conclusion)
EXTRA = {
    "steel": {
        "worlds": [
            {"at": "1973", "box": WORLD(F("제철 자금·기술은 국내에 없었다.", "ix-st-73"), F("대일청구권 자금과 일본의 기술 지원.", "ix-st-73"),
                                         F("정부 주도로 포항에 일관제철소를 지었다.", "ix-st-73"), F("한국 조강 생산이 한 설비로 두 배가 됐다.", "ix-st-72"), "adapted")},
            {"at": "2023~", "box": WORLD(F("중국이 부동산 침체로 남은 철강을 수출로 돌렸고, 미국은 50% 관세, EU는 쿼터를 줄였다.", "ix-st-25", "ix-st-next"),
                                          INF("싼 수입재가 국내 시장으로, 관세가 수출 가격으로 들어왔다.", "ix-st-25"),
                                          F("감산·공장 폐쇄, 정부의 설비 조정 유도.", "ix-st-cut", "ix-st-next"), F("포스코·현대제철 3년 연속 생산 감소.", "ix-st-25"), "same")},
        ],
        "outward": [SRC("한국 철강이 국내 조선소에 후판을 안정적으로 공급한 것이 조선업의 강점으로 꼽힌다 — 철강이 다른 산업의 경쟁력이 된 경로.", "ix-st-plate"),
                    INF("1990년대 세계 2위 규모의 생산능력은 한국이 철을 수입하던 나라에서 조선·자동차에 철을 대는 나라로 바뀌었다는 뜻이다.", "ix-st-97", "ix-st-self")],
        "split": INF("국내 수요가 회복할지보다 '어떤 철을 누가 만드느냐'(범용재는 중국, 고급재·저탄소 철은 누구)가 갈림길이다.", "ix-st-25", "ix-st-next"),
        "futures": [
            FUT("계속", "범용재를 줄이고 고급 강재·조선용 후판에 집중",
                change=INF("범용 철근·선재 설비를 줄이고, 조선·자동차용 고급 강재 비중을 높인다.", "ix-st-cut", "ix-st-plate"),
                basis=[F("2024~2025년 선재·철근 공장 폐쇄와 가동률 하향.", "ix-st-cut"), SRC("후판 안정 공급이 조선업 강점.", "ix-st-plate")],
                logic=INF("중국과 값으로 경쟁하는 제품은 줄이고, 국내 수요처가 붙어 있는 제품은 지킨다.", "ix-st-25"),
                conditions=INF("조선 호황이 이어지고, 자동차 강판 수요가 국내·현지 공장에서 유지되어야 한다.", "ix-sh-lng", "ix-au-alabama"),
                demand=INF("고강도 강판·후판, 공급 계약 안정성.", "ix-st-plate"),
                watch=["후판 가격과 조선사 공급 계약", "철근 가동률", "수출 중 고급재 비중"],
                against=["조선 발주가 급감하면 고급재 집중 전략의 수요처도 함께 줄어든다"]),
            FUT("경로 변경", "탄소 배출 규제가 경쟁의 기준을 바꾼다",
                change=HYP("가격보다 '얼마나 탄소를 덜 내고 만들었나'가 수출 조건이 되고, 수소환원제철 투자가 경쟁력을 가른다.", "ix-st-next"),
                basis=[F("포스코는 2050 탄소중립 목표로 수소환원제철을 개발 중.", "ix-st-next"), F("EU가 2026년 7월부터 쿼터 축소·초과분 관세.", "ix-st-next")],
                logic=INF("무역 장벽이 물량뿐 아니라 생산 방식을 기준으로 삼기 시작하면, 고로 중심 설비는 비용이 커진다.", "ix-st-next"),
                conditions=INF("탄소 기준 무역 규제가 실제로 강화되고, 수소 공급 비용이 감당할 수준이 되어야 한다.", "ix-st-next"),
                demand=INF("저탄소 철, 수소 공급망, 전기로 설비.", "ix-st-next"),
                watch=["수소환원제철 실증 설비 일정", "EU 탄소 관련 수입 규제 적용", "전기로 투자 발표"],
                against=["탄소 규제가 유예되거나 완화되면 가격 경쟁이 다시 기준이 된다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("철강은 '다른 산업을 위해 만든 산업'이었고, 그 수요처(건설·조선·자동차)와 무역 질서가 바뀔 때마다 함께 흔들렸다. 지금의 감산은 한국 철강이 약해져서만이 아니라, 국내 수요 감소와 중국 과잉 공급이 동시에 온 결과다.", "ix-st-25", "ix-st-plate"),
            favored=INF("'철강 몰락'보다 '범용재 축소와 수요처 중심 재편' 해석을 지지한다. 근거: 폐쇄는 선재·철근 같은 범용 설비에 몰렸고, 조선용 후판 수요는 남아 있다.", "ix-st-cut", "ix-st-plate"),
            undecided=INF("탄소 규제가 실제 무역 조건이 될지, 수소환원제철이 언제 상업 생산될지는 아직 판단할 수 없다.", "ix-st-next"),
            nextwatch=INF("EU 쿼터·탄소 규제 적용과 미국 관세가 실제 수출 물량을 얼마나 줄이는지.", "ix-st-next"),
            change=INF("건설 경기 반등과 관세 완화가 함께 오면 '구조적 축소' 판단을 '경기적 하강'으로 고친다.", "ix-st-25")),
    },
    "shipbuilding": {
        "worlds": [
            {"at": "1972~1976", "box": WORLD(F("배를 만들 경험·자금이 없었다.", "ix-sh-pre"), F("영국 차관으로 조선소를 지었다.", "ix-sh-72"),
                                               F("조선소 건설과 유조선 건조를 동시에 진행, 정부는 국내 화물 국적선 건조를 정책으로.", "ix-sh-72", "ix-sh-cargo"), F("1974년 첫 인도, 1983년 건조량 세계 1위.", "ix-sh-timeline"), "adapted")},
            {"at": "2021~2024", "box": WORLD(F("미국·러시아·카타르 등 LNG 생산 프로젝트로 LNG선 발주가 몰렸다.", "ix-sh-lng"), INF("해외 선주의 대량 발주로 들어왔다.", "ix-sh-lng"),
                                               F("숙련공이 부족해 이주노동자가 4배로 늘었다.", "ix-sh-skill"), F("슈퍼사이클, 그러나 2025년 1분기 발주는 평균보다 약 60% 적었다.", "ix-sh-lng"), "same")},
        ],
        "outward": [F("1999년 한국 조선소가 세계 1~3위를 처음 차지했고 2000년 수주 점유율 35.8%로 세계 1위 — 세계 선박 공급의 큰 몫을 한국이 맡게 됐다.", "ix-sh-timeline"),
                    F("2025년 한·미 조선 협력(MASGA)은 미국 함정 정비를 한국 조선사가 맡는 방향으로 논의됐다.", "ix-sh-masga")],
        "split": INF("선박 수요는 해운·에너지 사이클에 따라 반드시 출렁인다. 갈림길은 다음 하강기에 한국 조선이 무엇(LNG선·정비·함정)으로 버티느냐다.", "ix-sh-crash", "ix-sh-lng"),
        "futures": [
            FUT("경로 변경", "선박 판매에서 정비·함정으로 일감을 넓힌다",
                change=INF("신조선 수주가 줄어드는 시기를 미국 함정 정비(MRO)와 친환경선 개조로 메운다.", "ix-sh-masga"),
                basis=[F("MASGA에 1,500억 달러 규모 투자 예정, MRO가 첫 협력 분야.", "ix-sh-masga"), F("발주량이 슈퍼사이클 평균보다 크게 줄었다.", "ix-sh-lng")],
                logic=INF("정비는 발주 사이클과 다르게 움직이므로, 하강기의 완충이 될 수 있다.", "ix-sh-crash"),
                conditions=INF("미국과의 협력이 실제 계약으로 이어지고, 안보 관련 규제가 풀려야 한다.", "ix-sh-masga"),
                demand=INF("정비 인력·도크, 방산 협력 체계.", "ix-sh-skill"),
                watch=["미국 함정 MRO 계약 건수", "MASGA 투자 집행"],
                against=["협력이 발표에 그치고 계약이 없으면 하강기 완충 역할은 생기지 않는다"]),
            FUT("반작용", "숙련 인력 부족이 수주를 제한한다",
                change=INF("일감이 있어도 숙련공이 없어 납기와 품질이 흔들리고, 중국과의 격차가 좁아진다.", "ix-sh-skill", "ix-sh-china"),
                basis=[F("2016년 구조조정 때 숙련공이 떠났고 2021년 이후 인력을 구하지 못했다.", "ix-sh-skill"), F("중국 전체 수주 점유율 70.6%.", "ix-sh-china")],
                logic=INF("호황과 불황 사이 인력을 줄였다 늘리는 방식이 반복되면, 다음 호황에서 같은 부족이 다시 생긴다.", "ix-sh-crash", "ix-sh-skill"),
                conditions=INF("발주가 다시 늘 때 숙련 인력 양성이 따라가지 못해야 한다.", "ix-sh-skill"),
                demand=INF("자동화 용접·교육 프로그램, 이주노동자 정착 지원.", "ix-sh-skill"),
                watch=["조선업 종사자 수와 이주노동자 수", "납기 지연 보도", "LNG선 수주 점유율"],
                against=["이주노동자 비중이 늘어도 LNG선 점유율이 회복되면 인력 문제가 수주를 막지 않는다는 뜻"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("한국 조선의 역사는 '호황 → 대규모 설비·인력 → 불황 → 인력 절반 감축 → 다음 호황의 인력 부족'이 되풀이된 이야기다. 1위가 된 이유(대형 설비·고부가 선종)와 매번 흔들리는 이유(사이클·인력)가 같은 곳에 있다.", "ix-sh-crash", "ix-sh-skill"),
            favored=INF("'중국에 밀려 쇠퇴'보다 '고부가 선종에서 버티되 사이클은 피할 수 없다'를 지지한다. 근거: 전체 수주는 중국이 앞서지만 LNG선은 여전히 한국이 다수.", "ix-sh-china"),
            undecided=INF("미국 협력이 실제 일감이 될지, LNG선 수요가 언제 줄어들지는 판단할 수 없다.", "ix-sh-masga", "ix-sh-lng"),
            nextwatch=INF("세계 발주량과 선가가 함께 꺾이는지.", "ix-sh-lng"),
            change=INF("LNG선 점유율이 계속 떨어지면 '고부가에서 버틴다' 판단을 고친다.", "ix-sh-china")),
    },
    "semiconductor": {
        "worlds": [
            {"at": "2007~2009", "box": WORLD(F("D램 업계 증설 경쟁과 2008년 금융위기로 가격이 85% 떨어졌다.", "ix-cp-08"), INF("수출 가격으로 바로 들어왔다.", "ix-cp-08"),
                                               F("버틴 기업과 적자 기업이 갈렸다(삼성 흑자, 하이닉스 적자).", "ix-cp-08"), F("독일 키몬다 파산 — 경쟁자가 줄었다.", "ix-cp-08"), "same")},
            {"at": "2023~2025", "box": WORLD(F("세계 서버용 반도체 매출이 두 배가 됐다(AI 투자).", "ix-cp-cycle"), F("엔비디아 AI 가속기에 HBM 납품.", "ix-cp-hbm"),
                                               F("HBM 생산 확대.", "ix-cp-hbm"), F("반도체 수출 증가율 −23.7% → 17.8%.", "ix-cp-cycle"), "same")},
        ],
        "outward": [F("1992년 D램 세계 1위 이후 한국 기업은 세계 메모리 공급의 중심이 됐고, 2024년 HBM 점유율은 SK하이닉스·삼성전자가 합쳐 9할을 넘었다.", "ix-cp-92", "ix-cp-hbm"),
                    INF("메모리 공급이 한국에 몰려 있어서, 한국 기업의 증설·감산 결정이 세계 메모리 가격에 영향을 준다.", "ix-cp-08", "ix-cp-hbm")],
        "split": INF("갈림길은 AI 투자가 계속되느냐보다, 메모리 수요처가 AI 한 곳에 몰린 상태가 얼마나 오래 가느냐다.", "ix-cp-cycle", "ix-cp-share"),
        "futures": [
            FUT("계속", "AI 수요가 이어지며 수출 쏠림이 깊어진다",
                change=INF("HBM 같은 고부가 메모리 수요가 이어져 반도체가 수출의 3분의 1 안팎을 계속 차지한다.", "ix-cp-share", "ix-cp-hbm"),
                basis=[F("2026년 1월 수출 중 반도체 31.2%.", "ix-cp-share"), F("서버용 반도체 매출 두 배.", "ix-cp-cycle")],
                logic=INF("AI 서버 투자가 이어지는 한 고속 메모리 수요는 PC·폰보다 빨리 는다.", "ix-cp-cycle"),
                conditions=INF("빅테크의 AI 설비 투자가 줄지 않아야 한다.", "ix-cp-cycle"),
                demand=INF("HBM·고용량 메모리, 첨단 패키징.", "ix-cp-hbm"),
                watch=["빅테크 설비투자 발표", "HBM 가격·점유율", "반도체 수출 비중"],
                against=["AI 투자 둔화와 메모리 가격 하락이 함께 오면 2023년 같은 급감"]),
            FUT("반작용", "쏠림이 경기 변동을 키운다",
                change=INF("반도체 경기가 꺾일 때 수출·기업 이익·주가·성장률이 한꺼번에 흔들린다.", "ix-cp-share", "c20-chip-risk"),
                basis=[SRC("반도체 경기가 거시경제 전반에 주는 영향이 커졌다는 리포트.", "ix-cp-share"), F("2023년 수출 증가율 −23.7%.", "ix-cp-cycle")],
                logic=INF("한 품목 비중이 클수록 그 품목의 사이클이 나라 경제의 사이클이 된다.", "ix-cp-share"),
                conditions=INF("메모리 가격이 다시 떨어지는 국면이 와야 드러난다.", "ix-cp-08"),
                demand=INF("수출 품목 다변화 정책, 비메모리·다른 산업 투자.", "ix-cp-share"),
                watch=["반도체 제외 수출 증가율", "메모리 현물가격"],
                against=["반도체를 뺀 수출이 함께 늘면 쏠림 위험은 작아진다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("한국 메모리는 '불리한 조건에서 늦게 시작해, 가격 폭락기를 버티며 경쟁자가 사라지는 동안 1위가 된' 산업이다. 같은 사이클이 지금은 AI라는 한 수요처 위에서 되풀이된다.", "ix-cp-83", "ix-cp-08", "ix-cp-hbm"),
            favored=INF("지금의 호황을 '구조적 성장'으로만 보기보다 '사이클 위의 큰 상승'으로 보는 해석을 더 지지한다. 근거: 2023년 −23.7% 뒤 2025년 +17.8%로 바뀐 폭 자체가 사이클의 모양이다.", "ix-cp-cycle"),
            undecided=INF("AI 투자가 언제 둔화할지는 이 자료로 판단할 수 없다.", "ix-cp-cycle"),
            nextwatch=INF("반도체 수출 비중이 더 오르는지, 반도체를 뺀 수출이 함께 느는지.", "ix-cp-share"),
            change=INF("메모리 가격 하락 없이 AI 수요가 몇 년 더 이어지면 '사이클' 해석을 '수요처 구조 변화'로 고친다.", "ix-cp-cycle")),
    },
    "internet": {
        "worlds": [
            {"at": "1994~2002", "box": WORLD(INF("인터넷이 세계적으로 상용화됐다.", "ix-nt-94"), F("정부 종합계획과 통신사 경쟁(ADSL)으로 들어왔다.", "ix-nt-policy", "ix-nt-adsl"),
                                               F("정액제 초고속 인터넷과 PC방이 퍼졌다.", "ix-nt-price", "c90-pcbang"), F("2001년 보급률 세계 1위.", "ix-nt-policy"), "adapted")},
            {"at": "2009~", "box": WORLD(F("아이폰과 해외 플랫폼(유튜브 등).", "c00-kr-iphone", "sx-ytm"), INF("스마트폰과 앱 장터로 바로 들어왔다.", "c00-kr-iphone"),
                                           F("카카오톡 같은 국내 앱이 생겼다.", "c10-kakao"), SRC("음악 앱에서는 유튜브 뮤직이 1위가 됐다.", "sx-ytm"), "same")},
        ],
        "outward": [F("2001년 10월 초고속 인터넷 보급률 세계 1위 — 망 보급에서 앞선 나라가 됐다.", "ix-nt-policy"), INF("빠른 망 위에서 먼저 자리 잡은 PC방·메신저 같은 이용 방식이 국내 서비스(카카오톡 1억 명 돌파)를 키운 바탕이 됐다고 본다.", "c90-pcbang", "c10-kakao")],
        "split": INF("입구(검색·메신저·AI)가 바뀔 때마다 국내 서비스가 이겼다 졌다 했다. 다음 입구인 AI에서 어느 쪽이 될지가 갈림길이다.", "ix-nt-portal", "er-tech-ai"),
        "futures": [
            FUT("경로 변경", "AI가 검색·쇼핑의 입구를 바꾼다",
                change=HYP("사람들이 검색창 대신 AI에게 묻고, 쇼핑·정보 찾기의 첫 화면이 AI 서비스로 옮겨 간다.", "er-tech-ai"),
                basis=[F("생성형 AI 이용이 1년 새 33.3% → 44.5%.", "er-tech-ai"), F("지식iN처럼 새 방식이 1년 만에 1위를 바꾼 전례.", "ix-nt-portal")],
                logic=INF("입구가 바뀔 때마다 1위가 바뀌었다(야후 → 네이버, PC → 모바일).", "ix-nt-portal"),
                conditions=INF("AI 답변이 검색보다 편하고 믿을 만하다고 여겨져야 한다.", "er-tech-ai"),
                demand=INF("AI 검색·추천, 광고 방식의 변화.", "er-tech-ai"),
                watch=["AI 이용률", "포털 검색 점유율"],
                against=["AI 이용이 늘어도 포털 이용이 유지되면 교체가 아니라 공존"]),
            FUT("결합", "국내 포털이 AI를 붙여 입구를 지킨다",
                change=INF("국내 서비스가 자체 AI를 검색·쇼핑에 붙여 이용자를 유지한다.", "ix-nt-portal"),
                basis=[F("지식iN처럼 이용자 참여 기능을 붙여 1위가 된 전례.", "ix-nt-portal")],
                logic=INF("이용자가 이미 쓰는 서비스에 새 기능이 붙으면 옮겨 갈 이유가 줄어든다.", "ix-nt-portal"),
                conditions=INF("국내 AI 품질이 해외 서비스와 비슷해야 한다.", "er-tech-ai"),
                demand=INF("한국어 특화 AI, 국내 상품·지역 정보와의 결합.", "fl-shop-mobile"),
                watch=["국내 포털의 AI 기능 이용자 수"],
                against=["해외 AI 서비스 이용자가 국내 포털 이용자를 앞지르면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("인터넷 산업의 30년은 '접속(망)은 국내 통신사가 계속 지켰지만, 입구(서비스)는 바뀔 때마다 주인이 바뀐' 역사다.", "ix-nt-adsl", "ix-nt-portal", "sx-ytm"),
            favored=INF("AI도 '입구 교체'가 될 가능성을 열어 두되, 아직은 공존 단계라는 해석이 자료와 맞는다.", "er-tech-ai"),
            undecided=INF("AI 이용이 포털 이용을 줄이는지 직접 보여 주는 자료는 아직 확보하지 못했다.", "er-tech-ai"),
            nextwatch=INF("포털 검색 점유율의 변화.", "ix-nt-portal"),
            change=INF("포털 검색 이용이 눈에 띄게 줄면 '공존' 판단을 '교체'로 고친다.", "er-tech-ai")),
    },
    "automobile": {
        "worlds": [
            {"at": "1986", "box": WORLD(INF("미국 소형차 시장이 열려 있었다.", "ix-au-86"), F("엑셀 미국 수출.", "ix-au-86"),
                                          F("첫해 16만 대, 이듬해 26만 대 판매 뒤 품질 문제로 이미지 실추.", "ix-au-86"), F("2005년 미국 현지 공장으로 방식이 바뀌었다.", "ix-au-alabama"), "outbound")},
            {"at": "2025~2026", "box": WORLD(F("미국이 무관세였던 한국 차에 25% → 15% 관세, 2026년 재인상 위협.", "ix-au-tariff", "ix-au-2026"), INF("수출 가격으로 바로 들어왔다.", "ix-au-tariff"),
                                               F("관세에 따른 이익 감소 4조 1천억 원.", "ix-au-profit"), F("북미 수출 10.8% 감소, 전체 수출은 역대 최대.", "ix-au-tariff"), "same")},
        ],
        "outward": [F("현대·기아 세계 판매가 1998년 12위에서 2010년 4위로 올랐다 — 한국 차가 세계 시장의 주요 공급자가 됐다.", "ix-au-rank"),
                    F("미국 현지 공장(2005~)으로 한국 기업이 미국 안에서 생산·고용하는 쪽으로 바뀌었다.", "ix-au-alabama")],
        "split": INF("관세가 계속 바뀌는 상황에서 '한국에서 만들어 수출'과 '현지에서 만들어 판매' 중 어느 쪽 비중이 커지느냐가 갈림길이다.", "ix-au-tariff", "ix-au-alabama"),
        "futures": [
            FUT("경로 변경", "현지 생산이 늘고 국내 공장 일감이 줄어든다",
                change=INF("관세를 피해 미국 현지 생산 비중을 높이고, 국내 공장은 다른 시장·차종으로 일감을 찾는다.", "ix-au-tariff", "ix-au-alabama"),
                basis=[F("관세 이익 감소 4조 1천억 원.", "ix-au-profit"), F("미국 현지 공장이 이미 있다.", "ix-au-alabama")],
                logic=INF("관세가 불확실할수록 시장 안에서 만드는 쪽이 안전하다.", "ix-au-2026"),
                conditions=INF("관세가 15% 이상으로 오래 유지되어야 한다.", "ix-au-2026"),
                demand=INF("미국 현지 부품 공급망, 국내 공장의 차종 재배치.", "ix-au-alabama"),
                watch=["미국 현지 생산 비중", "국내 생산 대수"],
                against=["관세가 내려가거나 고정되면 국내 생산·수출 구조가 유지된다"]),
            FUT("분화", "시장별로 다른 차를 판다",
                change=HYP("미국은 현지 생산 차, 다른 시장은 국내 생산 차와 전기차로 나뉜다.", "ix-au-tariff", "ix-au-profit"),
                basis=[F("2025년 전체 수출은 최대, 북미는 감소.", "ix-au-tariff")],
                logic=INF("북미가 줄어도 전체가 늘었다면 다른 시장 수출이 늘었다는 뜻이다.", "ix-au-tariff"),
                conditions=INF("유럽·신흥시장 수요가 유지되어야 한다.", "ix-au-tariff"),
                demand=INF("시장별 차종 전략, 전기차 보조금 변화 대응.", "ix-au-profit"),
                watch=["시장별 수출액", "전기차 판매"],
                against=["북미 외 시장 수출도 줄면 분화가 아니라 전반적 하강"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("한국 차는 '싸게 팔다 품질로 실패 → 품질과 현지 생산으로 회복'의 길을 걸었고, 지금은 무역 정책이 다시 생산 위치를 정하는 시기다.", "ix-au-86", "ix-au-alabama", "ix-au-tariff"),
            favored=INF("'위기'보다 '생산 위치 재배치' 해석을 지지한다. 근거: 전체 수출은 최대였고 감소는 북미에 집중됐다.", "ix-au-tariff"),
            undecided=INF("2026년 관세 재인상이 실제로 적용될지는 판단할 수 없다(보도 시점 행정명령 없음).", "ix-au-2026"),
            nextwatch=INF("대미 관세율의 실제 적용과 현지 생산 비중.", "ix-au-2026"),
            change=INF("관세가 15%에 고정되고 북미 수출이 반등하면 '재배치' 판단도 약해진다.", "ix-au-tariff")),
    },
    "petrochem": {
        "worlds": [
            {"at": "1973~1980", "box": WORLD(F("값싼 석유를 전제로 짜인 성장 모델이 1973년 석유파동으로 깨졌다.", "c70-syn-chain"), INF("수입 원료(나프타·원유) 가격으로 들어왔다.", "ix-pc-72"),
                                               INF("단지 가동을 이어 가며 원가 부담을 떠안았다.", "ix-pc-72"), INF("원료를 수입해야 하는 구조의 약점이 드러났다.", "ix-pc-72"), "same")},
            {"at": "2019~2024", "box": WORLD(F("중국 에틸렌 자급률 74% → 98%, 생산능력 약 두 배.", "ix-pc-self", "ix-pc-cn"), INF("최대 수출처 수요 감소로 들어왔다.", "ix-pc-cn"),
                                               F("2025년 설비 18~25% 감축 협약.", "ix-pc-cut"), F("롯데케미칼 3년 연속 적자.", "ix-pc-lotte"), "same")},
        ],
        "outward": [INF("2000~2010년대 한국 석유화학은 중국 공장들의 원료를 대는 역할을 했다 — 중국 제조업 성장의 한 공급자였다.", "ix-pc-cn")],
        "split": INF("범용 제품을 얼마나 줄이고, 줄인 자리를 무엇으로 채우느냐가 지역(울산·여수·대산)마다 다르게 갈린다.", "ix-pc-cut", "ix-pc-2026"),
        "futures": [
            FUT("계속", "감축과 통합이 지역별로 진행된다",
                change=INF("대산·여수처럼 합의가 된 곳부터 설비가 통합·감축되고, 이해관계가 얽힌 곳은 늦어진다.", "ix-pc-2026"),
                basis=[F("2026년 대산·여수 재편안, 울산은 교착 보도.", "ix-pc-2026")],
                logic=INF("감축은 회사 간 합의가 필요해 지역마다 속도가 다르다.", "ix-pc-cut"),
                conditions=INF("정부·공정위 승인과 회사 간 합의가 이어져야 한다.", "ix-pc-2026"),
                demand=INF("고부가 소재, 지역 고용 전환 지원.", "ix-pc-cut"),
                watch=["단지별 감축 실행", "에틸렌 스프레드(톤당 300달러 선)"],
                against=["감축이 계획에 그치면 적자가 계속된다"]),
            FUT("반작용", "중국 노후설비 정리로 업황이 일부 회복",
                change=HYP("중국이 오래된 설비를 정리하면 공급 과잉이 줄어 스프레드가 회복된다.", "ix-pc-cn"),
                basis=[F("손익분기 스프레드 대비 낮은 현재 수준.", "ix-pc-cn")],
                logic=INF("과잉은 한쪽의 증설에서 왔으므로, 그쪽의 정리가 회복의 조건이다.", "ix-pc-self"),
                conditions=INF("중국의 실제 감산이 일어나야 한다.", "ix-pc-cn"),
                demand=INF("범용 제품 가격 회복.", "ix-pc-cn"),
                watch=["중국 신규 증설과 폐쇄 발표", "에틸렌 스프레드"],
                against=["중국이 증설을 계속하면 회복은 일어나지 않는다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("석유화학은 '늦게 시작해 과잉생산을 되풀이한' 산업이고, 최대 고객이던 중국이 스스로 만들게 되자 이번 과잉은 일시적이 아니라 구조적이 됐다.", "ix-pc-72", "ix-pc-91", "ix-pc-self"),
            favored=INF("'경기 하강'보다 '구조적 과잉' 해석을 지지한다. 근거: 중국 자급률 98%는 경기가 아니라 구조의 변화다.", "ix-pc-self"),
            undecided=INF("감축 뒤 고부가 제품이 그 자리를 채울 수 있을지는 판단할 수 없다.", "ix-pc-cut"),
            nextwatch=INF("울산 단지의 재편 합의 여부.", "ix-pc-2026"),
            change=INF("중국 감산으로 스프레드가 손익분기를 넘어 유지되면 '구조적' 판단을 약화한다.", "ix-pc-cn")),
    },
    "tv": {
        "worlds": [
            {"at": "2006", "box": WORLD(INF("세계 TV가 브라운관과 평판(PDP·LCD)으로 나뉘어 경쟁하던 전환기였다.", "ix-tv-06q"), INF("세계 시장의 제품 교체로 열렸다.", "ix-tv-06q"),
                                          F("평판 TV(보르도) 출시.", "ix-tv-06"), F("세계 1위(매출 14.6%).", "ix-tv-06"), "outbound")},
            {"at": "2019~", "box": WORLD(F("TCL·하이센스 점유율 상승.", "ix-tv-25"), INF("중저가 제품 경쟁으로 들어왔다.", "ix-tv-25"),
                                           F("프리미엄으로 이동(2,500달러 이상에서 삼성 53.4%).", "ix-tv-26"), F("출하량 기준 TCL이 한 달 1위.", "ix-tv-25"), "same")},
        ],
        "outward": [F("2008년 세계 LCD TV의 30% 이상이 한국 제품이었다는 추정 — 평판 TV로의 전환을 한국이 주도한 쪽에 있었다.", "ix-tv-lcd")],
        "split": INF("매출 1위(프리미엄)와 출하량 1위(대량)가 갈라졌다. 어느 쪽 기준이 시장을 정하게 되느냐가 갈림길이다.", "ix-tv-25", "ix-tv-26"),
        "futures": [
            FUT("분화", "프리미엄은 한국, 대량은 중국",
                change=INF("매출 기준 1위와 출하량 기준 1위가 다른 상태가 굳어진다.", "ix-tv-25", "ix-tv-26"),
                basis=[F("2026년 1분기 매출 점유율 삼성 31.3%, 프리미엄 53.4%.", "ix-tv-26"), F("출하량 기준 TCL 1위(2025년 12월).", "ix-tv-25")],
                logic=INF("성장이 멈춘 시장에서는 값비싼 제품과 싼 제품이 다른 회사의 몫이 되기 쉽다.", "ix-tv-25"),
                conditions=INF("프리미엄 수요가 유지되어야 한다.", "ix-tv-26"),
                demand=INF("대형·고화질 프리미엄 TV.", "ix-tv-26"),
                watch=["매출과 출하량 점유율의 차이"],
                against=["TCL이 프리미엄 점유율을 늘리면 분화가 아니라 추월"]),
            FUT("반작용", "중국의 프리미엄 진출로 매출 1위도 흔들린다",
                change=HYP("중국 업체가 프리미엄 시장에 들어와 매출 기준 1위도 위협한다.", "ix-tv-25"),
                basis=[SRC("TCL이 소니와 합작을 추진한다는 보도.", "ix-tv-25")],
                logic=INF("한국이 평판 TV 전환기에 일본을 앞섰던 것처럼, 기술 전환기가 순위를 바꾼다.", "ix-tv-06"),
                conditions=INF("중국 업체의 브랜드 신뢰가 프리미엄에서도 쌓여야 한다.", "ix-tv-25"),
                demand=INF("가격 대비 고화질 TV.", "ix-tv-25"),
                watch=["2,500달러 이상 시장 점유율"],
                against=["프리미엄 점유율이 유지되면 위협은 제한적"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("한국 TV는 '브라운관에서 평판으로 바뀌는 순간' 1위가 됐다. 순위를 바꾼 것은 기술 전환이었고, 지금은 전환 없이 가격 경쟁이 이어지는 시기다.", "ix-tv-06", "ix-tv-25"),
            favored=INF("'1위 상실'보다 '기준에 따라 1위가 갈리는 분화' 해석이 자료와 맞는다.", "ix-tv-25", "ix-tv-26"),
            undecided=INF("다음 기술 전환이 무엇이고 언제 올지는 판단할 수 없다.", "ix-tv-25"),
            nextwatch=INF("프리미엄 시장 점유율.", "ix-tv-26"),
            change=INF("프리미엄 점유율이 크게 떨어지면 '분화' 판단을 '추월'로 고친다.", "ix-tv-26")),
    },
    "phone": {
        "worlds": [
            {"at": "1996", "box": WORLD(INF("세계 이동통신은 여러 방식이 경쟁 중이었다.", "c90-cdma"), F("국내가 CDMA를 상용화했다.", "c90-cdma"),
                                          F("국산 폰이 외국산을 밀어냈다.", "c90-hyp-ad"), F("1995년 국내 1위 탈환.", "c90-hyp-ad"), "adapted")},
            {"at": "2009~2011", "box": WORLD(F("아이폰 등장.", "c00-kr-iphone"), F("국내 출시로 들어왔다.", "c00-kr-iphone"),
                                               F("갤럭시S 출시.", "ix-ph-2010", "ix-ph-gs"), F("2011년 세계 스마트폰 1위.", "ix-ph-gs"), "same")},
        ],
        "outward": [F("2011년 세계 스마트폰 1위 — 한국 기업이 세계 스마트폰 공급의 한 축이 됐다.", "ix-ph-gs")],
        "split": INF("국내 제조사가 하나만 남은 상태에서, 국내 점유율이 애플 쪽으로 계속 옮겨 가느냐가 갈림길이다.", "ix-ph-share"),
        "futures": [
            FUT("계속", "폴더블로 차별화를 이어 간다",
                change=INF("폴더블 같은 형태 차별화로 프리미엄에서 애플과 경쟁한다.", "ix-ph-fold"),
                basis=[F("폴더블 출시 뒤 국내 점유율 89%까지.", "ix-ph-share"), SRC("폴더블 '대흥행' 평가.", "ix-ph-fold")],
                logic=INF("같은 모양의 폰으로는 브랜드 경쟁이 되므로, 형태가 차별화 수단이 된다.", "ix-ph-lgpeak"),
                conditions=INF("폴더블 수요가 일부 층을 넘어 넓어져야 한다.", "ix-ph-fold"),
                demand=INF("접는 화면, 관련 부품.", "ix-ph-fold"),
                watch=["폴더블 판매량", "국내 점유율"],
                against=["애플이 폴더블을 내고 점유율을 가져가면"]),
            FUT("반작용", "국내 점유율이 애플로 옮겨 간다",
                change=INF("젊은 층 중심으로 애플 점유율이 계속 늘어 국내 1위가 흔들린다.", "ix-ph-share"),
                basis=[F("애플 국내 점유율 17.3% → 25.9%.", "ix-ph-share")],
                logic=INF("LG 철수로 생긴 수요 일부가 애플로 갔다.", "ix-ph-share"),
                conditions=INF("애플 상승이 이어져야 한다.", "ix-ph-share"),
                demand=INF("젊은 층이 고르는 디자인과 기기 사이 연결(생태계) 경쟁.", "ix-ph-share"),
                watch=["연령별 점유율"],
                against=["점유율이 25% 선에서 멈추면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("한국 폰은 통신 방식(CDMA)과 스마트폰 전환이라는 두 번의 큰 변화에서 빠르게 따라붙어 1위가 됐고, 같은 전환에서 LG는 사라졌다. 전환기를 넘는 속도가 승패를 갈랐다.", "c90-cdma", "ix-ph-gs", "ix-ph-lg"),
            favored=INF("지금은 '국내 양강 구도의 고착' 해석이 자료와 맞는다.", "ix-ph-share"),
            undecided=INF("AI 기능 경쟁이 순위를 바꿀지는 판단할 수 없다.", "ix-ph-share"),
            nextwatch=INF("국내 점유율 추이.", "ix-ph-share"),
            change=INF("애플 국내 점유율이 30%를 넘어 계속 오르면 판단을 고친다.", "ix-ph-share")),
    },
    "construction": {
        "worlds": [
            {"at": "1975~1985", "box": WORLD(F("석유파동 뒤 중동 산유국이 오일머니로 건설을 발주했다.", "c70-kr-mideast", "c70-syn-chain"), F("해외 수주로 들어왔다.", "c70-kr-mideast"),
                                               F("건설사와 노동자가 중동으로 갔다.", "c70-kr-mideast"), F("중동 수주 700억 달러.", "c70-kr-mideast"), "outbound")},
            {"at": "2008", "box": WORLD(F("세계 금융위기.", "ix-cn-0809"), F("금리·집값을 통해 들어왔다.", "ix-cn-0809"),
                                          F("분양 위축, PF 이자 누적.", "ix-cn-0809"), F("건설사 40여 곳 폐업 보도.", "ix-cn-pf"), "same")},
        ],
        "outward": [F("1970~80년대 중동 건설과 2025년 해외 원전 수주 — 한국 건설사가 해외 대형 시공을 맡는 쪽이 됐다.", "c70-kr-mideast", "ix-cn-25")],
        "split": INF("국내 주택(분양·PF)과 해외 플랜트·원전이 다른 방향으로 움직인다. 어느 쪽 비중이 커지느냐가 갈림길이다.", "ix-cn-25", "ix-cn-24"),
        "futures": [
            FUT("분화", "해외 원전·플랜트와 국내 주택이 갈라진다",
                change=INF("대형사는 해외 원전·플랜트로, 지방 중소 건설사는 주택 부진에 남는다.", "ix-cn-25", "ix-cn-24"),
                basis=[F("2025년 국내 유동성 고갈과 해외 원전 성과가 동시에.", "ix-cn-25")],
                logic=INF("국내 주택은 금리·PF에, 해외는 발주국 정책에 달려 서로 다르게 움직인다.", "ix-cn-0809"),
                conditions=INF("해외 원전 계약이 이어져야 한다.", "ix-cn-25"),
                demand=INF("원전 시공 인력, PF 구조조정.", "ix-cn-24"),
                watch=["해외 원전 계약", "지방 미분양"],
                against=["국내 주택이 빠르게 회복하면 분화가 약해진다"]),
            FUT("계속", "몇 년마다 PF 위기가 되풀이된다",
                change=INF("분양에 기대는 사업 구조가 그대로면 금리가 오를 때마다 PF 위기가 다시 온다.", "ix-cn-0809", "ix-cn-24"),
                basis=[F("2008~2011년과 2022~2024년 두 번의 PF 위기.", "ix-cn-pf", "ix-cn-24")],
                logic=INF("같은 구조(선분양·PF)가 같은 충격(금리)에 같은 결과를 낸다.", "ix-cn-0809"),
                conditions=INF("PF 구조가 바뀌지 않아야 한다.", "ix-cn-24"),
                demand=INF("PF 감독·자기자본 비율 강화.", "ix-cn-24"),
                watch=["PF 연체율", "준공 후 미분양"],
                against=["PF 제도가 바뀌면 반복 고리가 끊길 수 있다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("건설은 나라가 고속도로·신도시를 지을 때 커졌고, 그 뒤로는 금리와 분양 경기에 몇 년마다 흔들리는 구조가 되었다.", "fl-city-gyeongbu", "fl-city-newtown", "ix-cn-0809"),
            favored=INF("'건설 위기'를 하나로 보기보다 '국내 주택과 해외 플랜트의 분화'로 보는 해석을 지지한다.", "ix-cn-25"),
            undecided=INF("국내 주택 경기가 언제 바닥을 칠지는 판단할 수 없다.", "ix-cn-24"),
            nextwatch=INF("준공 후 미분양과 PF 연체율.", "ix-cn-24"),
            change=INF("금리 하락과 미분양 감소가 함께 오면 회복 국면으로 판단을 고친다.", "ix-cn-0809")),
    },
}


def apply(industries, claims_all):
    cids = {c["id"] for c in claims_all}
    ids = {i["id"] for i in industries}

    def chk(x, w):
        if x["layer"] in ("fact", "source") and not x["ids"]:
            raise SystemExit(f"산업 {w}: 근거 없는 사실")
        for i in x["ids"]:
            if i not in cids:
                raise SystemExit(f"산업 {w}: 없는 근거 {i}")

    for row in SELECTION:
        assert row["status"] in STATUS
        if row["status"] == "선정" and row.get("industry") not in ids:
            raise SystemExit(f"선정표: 일대기 없는 산업 {row['label']}")
        for x in row["cells"].values():
            chk(x, f"선정표 {row['label']}")
    if {r["industry"] for r in SELECTION if r["status"] == "선정"} != ids:
        raise SystemExit("선정표와 산업 일대기 목록이 다름")
    by = {i["id"]: i for i in industries}
    for k, ex in EXTRA.items():
        ind = by[k]
        if len(ex["futures"]) < 2 or len({f["kind"] for f in ex["futures"]}) < 2:
            raise SystemExit(f"{k}: 미래 가능성은 서로 다른 종류 2개 이상")
        for w in ex["worlds"]:
            for part in ("what", "route", "response", "result"):
                chk(w["box"][part], f"{k} 세계")
        if not ex["outward"]:
            raise SystemExit(f"{k}: 밖으로 준 영향 없음")
        for x in ex["outward"]:
            chk(x, f"{k} 밖으로")
        chk(ex["split"], k)
        for f in ex["futures"]:
            for part in ("change", "logic", "conditions", "demand"):
                chk(f[part], f"{k} 미래")
            for x in f["basis"]:
                chk(x, f"{k} 미래 근거")
        for part in ("key", "favored", "undecided", "next", "change"):
            chk(ex["conclusion"][part], f"{k} 결론")
        ind["worlds"], ind["outward"] = ex["worlds"], ex["outward"]
        ind["futures"] = {"split": ex["split"], "items": ex["futures"]}
        ind["conclusion"] = ex["conclusion"]
    miss = ids - set(EXTRA)
    if miss:
        raise SystemExit(f"세계·미래·결론이 없는 산업 {miss}")
    return {"criteria": CRITERIA, "rows": SELECTION}
