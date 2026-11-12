"""18차 R-Q12·R-Q14·R-FU1: 시대 흐름 14개와 취향 흐름 5개에 '여러 갈래의 미래(7항목)'와 '5요소 결론'을 붙인다.

- 근거(basis)는 이미 검증된 근거 문장 id에만 기댄다. 확률·시점 단정은 쓰지 않는다.
- 시대 흐름: 갈라지는 이유(split) + 서로 다른 종류의 가능성 2개 이상 + 결론.
- 취향 흐름: 이미 있는 '다음 수요'(조건·상품·신호·반대 신호·근거)에 종류·예상 변화·연결 논리를 더해 7항목으로 맞추고 결론을 붙인다.
"""
from topic_helpers import C, CONCLUDE, F, FUT, HYP, INF, REPEAT, S, SRC, FUTURE_KINDS

SOURCES = [
    S("tf-s-segye26", "[설왕설래] ‘장시간 노동’ 국가 한국", "세계일보", "https://segye.com/newsView/20260706515834", "news", "2026-07-06"),
    S("tf-s-segye23", "한국 주 평균 노동시간 1980년 53.9시간 → 2022년 38.3시간(보고서 보도)", "세계일보", "https://www.segye.com/newsView/20230423508006", "news", "2023-04-23"),
    S("tf-s-kmctu00", "노동시간 국제비교(정책 2000-4)", "전국민주노동조합총연맹", "https://archivecenter.net/kaitArchive/attach/140000/143030/20260104232822384.pdf", "report", "2000-04"),
]
CLAIMS = [
    C("tf-time-law", "1953년 근로기준법은 법정 근로시간을 하루 8시간(주 48시간), 주 6일로 정했고 초과근무를 포함한 1주 최대 근로시간은 72시간이었다. 이후 1989년 주 44시간으로 줄었고, 2004년 주5일제의 단계적 시행을 거쳐 2018년부터 주 40시간제가 본격 도입됐다.", "fact", ["tf-s-segye26"], period="1953~2018", domains=("society",)),
    C("tf-time-1980", "한국의 주 평균 노동시간은 1980년 53.9시간에서 2022년 38.3시간으로 29% 줄었다. 10인 이상 전 산업 노동자의 주당 노동시간은 1989년 49.2시간으로 40시간대에 들어선 뒤 줄어 1998년 45.9시간이 됐다.", "statistical", ["tf-s-segye23", "tf-s-kmctu00"], period="1980~2022", domains=("society",)),
    C("tf-time-oecd25", "2025년 국내 근로자의 연평균 노동시간은 1,833시간으로 OECD 주요 회원국 중 여섯 번째로 길었고 OECD 평균(1,736시간)보다 97시간 많았다. 정부는 2030년까지 OECD 평균 1,700시간대로 낮추는 로드맵(주 4.5일제 도입 포함)을 추진 중이다.", "statistical", ["tf-s-segye26"], period="2025", domains=("society",)),
]


ERA = {
    "flow-jobs": {
        "split": INF("갈림길은 '일자리를 잇는 방식'이다: 회사가 사람을 고용하는 방식이 다시 강해질지, 앱이 일감과 사람을 바로 잇는 방식이 더 넓어질지, 그리고 AI가 전문직 증가 추세를 바꿀지가 아직 정해지지 않았다.", "c10-delivery", "c20-hyp-ai-jobs"),
        "items": [
            FUT("계속", "전문직·서비스 비중이 계속 오른다",
                change=INF("전문가 비중이 2013년 이후처럼 조금씩 오르고 서비스업 중심 구조가 이어진다.", "c20-hyp-ai-jobs", "fl-jobs-emp"),
                basis=[F("전문가 비중 2013년 19.6% → 2025년 23.1%.", "c20-hyp-ai-jobs"), F("서비스업으로의 일자리 이동.", "fl-jobs-emp")],
                logic=INF("AI 이전부터 이어진 추세라, 새 충격이 없다면 같은 방향이 이어질 가능성이 크다.", "c20-hyp-ai-jobs"),
                conditions=INF("AI가 전문직 일을 대체하기보다 보조하는 쪽으로 쓰여야 한다.", "c20-hyp-ai-jobs"),
                demand=INF("전문 교육·재교육, 전문 서비스.", "c20-hyp-ai-jobs"),
                watch=["직업별 취업자 중 전문가 비중", "서비스업 취업자 비중"],
                against=["전문가 비중이 처음으로 꺾이면 AI 대체 쪽으로 판단을 옮긴다"]),
            FUT("분화", "앱으로 이어지는 일과 회사 고용이 갈라진다",
                change=INF("배달처럼 앱이 일감을 나누는 일이 다른 업종으로 넓어지고, 회사 고용과 다른 보호 체계가 따로 만들어진다.", "c10-delivery", "c10-syn-delivery"),
                basis=[F("배달앱 이용자 2013년 87만 → 2019년 2,500만.", "c10-delivery"), F("배달앱이 플랫폼 노동이라는 새 고용 형태를 만들었다는 분석.", "c10-syn-delivery")],
                logic=INF("2000년대 비정규직이 늘어난 뒤 플랫폼 노동이 나왔듯, 회사 밖의 일은 새 기술이 생길 때마다 다른 모양으로 늘었다.", "c00-irregular", "c10-syn-delivery"),
                conditions=INF("일감 중개 앱이 배달 밖(청소·돌봄·전문 용역)으로 퍼져야 한다.", "c10-syn-delivery"),
                demand=INF("플랫폼 노동자 보험·안전 장비, 일감 중개 서비스.", "c10-rider-risk"),
                watch=["플랫폼 종사자 수", "배달 외 업종의 중개 앱 이용"],
                against=["배달 시장이 줄고 다른 업종으로 퍼지지 않으면 분화는 배달에 머문다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("일자리의 역사는 '농업 → 공장 → 서비스'로 옮겨 가면서, 고용 조건이 위기마다 새로 정해진 이야기다. 1987년에는 조직된 정규직이, 외환위기 뒤에는 비정규직이, 스마트폰 뒤에는 앱 노동이 새 조건을 만들었다.", "c80-labor", "c00-irregular", "c10-syn-delivery"),
            favored=INF("'일자리가 줄어든다'보다 '일하는 조건이 갈라진다' 해석을 지지한다. 근거: 전문직 비중은 늘었고, 동시에 회사 밖의 일(비정규직·플랫폼)도 시기마다 새 모양으로 늘었다.", "c20-hyp-ai-jobs", "c00-irregular"),
            undecided=INF("생성형 AI가 이 흐름을 바꾸는지는 통계로 아직 구분할 수 없다.", "c20-hyp-ai-jobs"),
            nextwatch=INF("AI 이용이 빠르게 는 2024~2025년 이후 직업별 취업자 구성.", "c20-hyp-ai-jobs", "er-tech-ai"),
            change=INF("전문가 비중이 줄기 시작하면 '조건의 분화'보다 '일자리 대체'가 더 맞는 설명이 된다.", "c20-hyp-ai-jobs")),
    },
    "flow-music": {
        "split": INF("음악을 '어디서 듣고 무엇에 값을 내나'가 동영상 플랫폼 하나로 모일지, 공연·실물(LP)처럼 몸으로 겪는 소비와 둘로 나뉠지가 갈림길이다.", "fl-mus-video", "c10-analog"),
        "items": [
            FUT("계속", "동영상 플랫폼이 듣기·발견의 중심이 된다",
                change=INF("음악을 동영상 사이트·통합 플랫폼에서 듣고 찾는 비중이 더 커진다.", "fl-mus-video", "fl-mus-platform"),
                basis=[F("음악 동영상 사이트 이용 응답 2021년 81%.", "fl-mus-video"), F("2025년 유튜브(뮤직 포함) 37.6%가 1위.", "fl-mus-platform")],
                logic=INF("음반 → MP3 → 스트리밍처럼, 더 싸고 넓게 닿는 통로가 매번 다음 중심이 되었다.", "fl-mus-cd-crash", "fl-mus-melon"),
                conditions=INF("영상 플랫폼의 묶음 상품(동영상+음악)이 유지되어야 한다.", "fl-mus-platform"),
                demand=INF("영상과 함께 퍼지는 곡, 숏폼용 음악.", "c10-psy"),
                watch=["주로 쓰는 음악 서비스 순위", "국내 음악 앱 이용자 수"],
                against=["국내 음악 앱 이용자가 다시 늘면 한 곳 쏠림이 아니라 공존"]),
            FUT("반작용", "실물·현장 음악이 따로 자란다",
                change=HYP("화면으로 듣는 음악이 흔해질수록 LP·공연·노래방처럼 몸으로 겪는 음악이 따로 수요를 갖는다.", "c10-analog", "c10-sesibong"),
                basis=[SRC("2011년 스마트폰 판매와 함께 통기타·LP·음악카페 복고가 유행했다는 보도.", "c10-analog"), F("세시봉 재등장(2010~2011).", "c10-sesibong")],
                logic=INF("디지털이 기능(듣기)을 가져가면, 실물은 경험·추억이라는 다른 의미로 남는다 — 기록 도구와 같은 모양이다.", "c10-analog"),
                conditions=INF("공연·실물 가격을 감당할 여유가 있어야 한다.", "c10-sesibong"),
                demand=INF("LP·공연·음악 감상 공간.", "c10-analog"),
                watch=["LP 판매", "공연 관객 수"],
                against=["노래방처럼 현장 음악 공간이 계속 줄면 반작용은 일부 층에 그친다"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("음악 듣기는 '공간에서 함께(음악감상실·다방) → 집에서 TV로 → 혼자 기기로 → 화면에서 영상과 함께'로 옮겨 갔다. 통로가 바뀔 때마다 돈을 내는 방식(음반 → 정액제 → 묶음 구독)이 함께 바뀌었다.", "fl-mus-dabang", "fl-mus-cd-crash", "fl-mus-platform"),
            favored=INF("통로 쏠림(동영상)과 실물·현장의 공존이 함께 진행된다는 해석을 지지한다.", "fl-mus-video", "c10-analog"),
            undecided=INF("2025년부터 조사 항목이 바뀌어(유튜브·유튜브 뮤직 합산) 쏠림의 정확한 크기는 이전과 비교할 수 없다.", "fl-mus-platform"),
            nextwatch=INF("국내 음악 앱과 동영상 플랫폼의 이용자 격차.", "fl-mus-platform"),
            change=INF("국내 음악 앱 이용이 다시 늘면 '동영상 쏠림' 판단을 고친다.", "fl-mus-platform")),
    },
    "flow-shop": {
        "split": INF("자세한 갈림길은 소비·쇼핑 5개 주제가 다룬다. 시대 개관에서 보면, 배송이 거의 모든 반복 구매를 가져갈지, 매장이 경험·급한 소량으로 역할을 나눠 남을지가 갈린다.", "c20-online", "fl-shop-mobile"),
        "items": [
            FUT("계속", "모바일·배송 비중이 더 오른다",
                change=INF("온라인·모바일 비중이 계속 오르지만 오름 폭은 줄어든다.", "c20-online", "fl-shop-mobile"),
                basis=[F("2020년 온라인 비중 27.2%.", "c20-online"), F("모바일이 2015년 절반을 넘었다.", "fl-shop-mobile")],
                logic=INF("이동과 운반을 대신하는 배송이 반복 구매에서 가장 큰 이점을 준다.", "fl-shop-mobile-why"),
                conditions=INF("배송 비용을 기업·회원비가 계속 감당해야 한다.", "c20-online"),
                demand=INF("빠른 배송, 멤버십.", "fl-shop-mobile-why"),
                watch=["온라인쇼핑 비중", "모바일 비중"], against=["온라인 증가율이 0에 가까워지면 포화"]),
            FUT("분화", "매장은 경험·급한 소량으로 남는다",
                change=INF("편의점·백화점처럼 배송이 대신하기 어려운 역할의 매장은 남고, 주말 대량 장보기 매장은 줄어든다.", "er-shop-cvs", "fl-shop-emart"),
                basis=[F("편의점(1989)·할인점(1993)이 서로 다른 역할로 시작했다.", "er-shop-cvs", "fl-shop-emart")],
                logic=INF("장소마다 맡은 과업이 달라, 배송은 그중 일부만 대신한다.", "er-shop-cvs"),
                conditions=INF("매장 방문의 이유(즉시·경험)가 유지되어야 한다.", "er-shop-cvs"),
                demand=INF("체험형 매장, 근거리 소형 매장.", "er-shop-cvs"),
                watch=["업태별 매출"], against=["편의점까지 줄면 오프라인 전반 쇠퇴"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("구매 장소와 결제는 '시간과 운반의 제약을 누가 대신 지나'와 '돈을 언제 치르나'가 함께 바뀐 역사다. 자세한 이야기는 다섯 주제로 나눴다.", "fl-shop-before", "c00-card"),
            favored=INF("교체보다 역할 분화 해석을 지지한다(자세한 근거는 '어디서 사나' 주제).", "fl-shop-mobile"),
            undecided=INF("온라인 증가율 둔화가 포화인지 경기 탓인지는 아직 판단할 수 없다.", "c20-online"),
            nextwatch=INF("업태별 매출과 규제 변화.", "c20-online"),
            change=INF("매장 전반이 함께 줄면 '분화'가 아니라 '대체'로 판단을 고친다.", "c20-online")),
    },
    "flow-relations": {
        "split": INF("만남이 '아는 사람 중심'으로 돌아갈지, '관심사로 모르는 사람과' 모이는 방식이 더 넓어질지가 갈림길이다. 모임 참여율이 2023년에 올랐다가 2024년 다시 내려 아직 방향이 정해지지 않았다.", "fl-rel-orgrate", "fl-rel-apps"),
        "items": [
            FUT("계속", "관심사 모임이 더 넓어진다",
                change=INF("PC통신 동호회 → 인터넷 카페 → 오픈채팅·모임 앱처럼, 관심사로 모르는 사람과 모이는 방식이 넓어진다.", "fl-rel-pctong", "fl-rel-openchat", "fl-rel-apps"),
                basis=[F("모임 앱 설치 2022년 하반기 102.2% 증가, 설치자 77%가 20~30대.", "fl-rel-apps"), F("오픈채팅(2015), 2023년 별도 탭 승격.", "fl-rel-openchat")],
                logic=INF("통로가 바뀔 때마다 같은 욕구(관심사로 모이기)가 새 통로로 옮겨 갔다.", "fl-rel-pctong", "fl-rel-cafe"),
                conditions=INF("20~30대의 모임 앱 이용이 이어져야 한다.", "fl-rel-apps"),
                demand=INF("관심사 모임 앱, 모임 장소.", "fl-rel-apps"),
                watch=["모임 앱 이용자", "사회단체 참여율"], against=["참여율이 계속 내려가면 '다르게'가 아니라 '덜' 만나는 쪽"]),
            FUT("반작용", "온라인 모임의 피로로 가까운 정기 모임이 돌아온다",
                change=HYP("일회성 온라인 모임 대신 동네·운동처럼 정기적으로 얼굴 보는 모임이 늘어난다.", "fl-rel-sports", "fl-rel-orgrate"),
                basis=[F("운동하는 사람 중 함께하는 비율 2013년 71.5%.", "fl-rel-sports"), F("참여율 2023년 58.2% → 2024년 52.3%.", "fl-rel-orgrate")],
                logic=INF("만남의 깊이에 대한 불만이 쌓이면 접근성보다 지속성을 고르게 된다.", "fl-rel-orgrate"),
                conditions=INF("일회성 모임에 대한 피로가 실제로 커져야 한다.", "fl-rel-apps"),
                demand=INF("동네 기반 모임, 정기 운동 모임.", "fl-rel-sports"),
                watch=["체육 동호회 가입률", "정기 모임 재참여율"], against=["동호회 가입률이 계속 11% 안팎에 머물면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("만남의 장소는 '공간(다방) → 집 전화 → 화면'으로 옮겨 갔고, 그때마다 '아는 사람'과 '모르는 사람'의 비중이 달라졌다. 화면이 생긴 뒤로 관심사로 모이는 통로가 계속 새로 생겼다.", "er-rel-dabang", "er-rel-phone", "fl-rel-openchat"),
            favored=INF("'덜 만난다'보다 '다르게 만난다' 해석을 지지하지만, 참여율이 오르내려 근거가 약하다.", "fl-rel-orgrate", "fl-rel-apps"),
            undecided=INF("앱 설치·가입 자료는 실제 만남과 다르다 — 실제 만남 빈도는 판단할 수 없다.", "fl-rel-apps"),
            nextwatch=INF("2025년 이후 사회단체 참여율.", "fl-rel-orgrate"),
            change=INF("참여율이 2019년 수준 아래로 계속 내려가면 '덜 만난다' 쪽으로 판단을 고친다.", "fl-rel-orgrate")),
    },
    "flow-fashion": {
        "split": INF("옷을 사는 곳이 플랫폼 한 곳으로 모일지, 플랫폼·매장·중고로 나뉠지가 갈림길이다.", "fl-fash-platform", "fl-fash-spa"),
        "items": [
            FUT("계속", "패션 플랫폼 중심이 굳는다",
                change=INF("가격 비교·리뷰·빠른 배송을 앞세운 플랫폼이 중심이 된다.", "fl-fash-platform"),
                basis=[SRC("2026년 기사: 플랫폼 중심 소비, 매장 중심 해외 SPA 고전.", "fl-fash-platform")],
                logic=INF("동대문 → 인터넷 쇼핑몰 → SPA → 플랫폼처럼, 더 싸고 빠르게 유행을 보여 주는 곳이 매번 10~20대를 데려갔다.", "fl-fash-mall", "fl-fash-decline"),
                conditions=INF("플랫폼이 배송·반품 비용을 계속 감당해야 한다.", "fl-fash-platform"),
                demand=INF("리뷰·사이즈 정보, 빠른 반품.", "fl-fash-platform"),
                watch=["플랫폼 거래액", "SPA 매출"], against=["매장 중심 브랜드 매출이 다시 늘면"]),
            FUT("분화", "매장은 체험, 플랫폼은 구매로 나뉜다",
                change=HYP("매장은 입어 보고 경험하는 곳, 플랫폼은 사는 곳으로 역할이 나뉜다.", "fl-fash-spa", "fl-fash-platform"),
                basis=[F("SPA는 매장 중심으로 1조 원 매출까지 컸다(2015).", "fl-fash-spa")],
                logic=INF("옷은 입어 봐야 하는 상품이라 매장의 기능이 완전히 사라지기 어렵다.", "fl-fash-spa"),
                conditions=INF("매장 방문이 구매로 이어지는 연결(매장 픽업 등)이 생겨야 한다.", "fl-fash-platform"),
                demand=INF("체험 매장, 온·오프라인 연동.", "fl-fash-platform"),
                watch=["플랫폼의 오프라인 매장 출점"], against=["플랫폼이 매장 없이도 반품률을 낮추면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("옷을 사는 곳은 '맞춤 → 기성복 → 동대문 → 인터넷·SPA → 플랫폼'으로, 매번 더 싸고 빠르게 유행을 보여 주는 곳으로 옮겨 갔다.", "er-fash-ready", "fl-fash-mall", "fl-fash-platform"),
            favored=INF("플랫폼 중심 이동을 지지하되, 매장 기능이 사라진다고 보지는 않는다.", "fl-fash-platform"),
            undecided=INF("시장 규모 연속 통계가 없어 채널별 비중 변화를 숫자로 판단할 수 없다.", "fl-fash-platform"),
            nextwatch=INF("플랫폼의 오프라인 확장 여부.", "fl-fash-platform"),
            change=INF("매장 중심 브랜드가 다시 성장하면 판단을 고친다.", "fl-fash-spa")),
    },
    "flow-expression": {
        "split": INF("표현을 허용하는 제도가 계속 넓어질지, 새 표현(문신 등)이 제도 안에서 관리·제한될지가 갈림길이다.", "fl-expr-tattoo-law", "fl-expr-tattoo-opinion"),
        "items": [
            FUT("계속", "제도가 표현의 현실을 뒤따라 넓어진다",
                change=INF("미니스커트 단속 → 자율화 → 문신 합법화처럼, 이미 퍼진 표현을 제도가 뒤늦게 받아들이는 일이 이어진다.", "c70-taboo", "fl-expr-uniform", "fl-expr-tattoo-law"),
                basis=[F("문신사법 통과(2025), 시술 장소 81%가 문신 전문숍.", "fl-expr-tattoo-law", "fl-expr-tattoo-survey")],
                logic=INF("제도는 단속보다 관리가 쉬운 쪽을 고른다 — 이미 대부분이 하는 일은 금지하기 어렵다.", "fl-expr-tattoo-survey"),
                conditions=INF("새 표현이 다수에게 퍼져야 한다.", "fl-expr-tattoo-survey"),
                demand=INF("문신사 자격·위생 관리, 제거 시술.", "fl-expr-tattoo-law"),
                watch=["문신사 국가시험·등록 수"], against=["시행 뒤 규제가 강화되면"]),
            FUT("분화", "법은 허용하지만 인식은 갈린다",
                change=INF("제도는 허용해도 직장·세대에 따라 받아들이는 정도가 계속 갈린다.", "fl-expr-tattoo-opinion"),
                basis=[F("합법화 찬성은 절반 수준, 문신 자체엔 부정적 인식 여전(2021).", "fl-expr-tattoo-opinion")],
                logic=INF("법이 바뀌어도 인식은 세대 교체를 따라 천천히 바뀐다.", "fl-expr-tattoo-opinion"),
                conditions=INF("세대별 인식 차이가 유지되어야 한다.", "fl-expr-tattoo-opinion"),
                demand=INF("가릴 수 있는 작은 문신, 반영구 화장.", "fl-expr-tattoo-survey"),
                watch=["문신 인식 조사의 세대 차이"], against=["찬성이 크게 늘어 다수가 되면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("표현의 역사는 '먼저 퍼지고, 제도가 단속하다가, 뒤늦게 허용하는' 반복이다. 표현 수단은 옷 → 사진 → 몸으로 옮겨 갔다.", "c70-taboo", "er-expr-dica", "fl-expr-tattoo-law"),
            favored=INF("제도가 현실을 뒤따른다는 해석을 지지한다.", "fl-expr-tattoo-survey"),
            undecided=INF("문신사법 시행(공포 2년 뒤) 뒤의 실제 변화는 아직 판단할 수 없다.", "fl-expr-tattoo-law"),
            nextwatch=INF("시행 뒤 등록 문신사 수와 시술 장소 변화.", "fl-expr-tattoo-law"),
            change=INF("시행 뒤에도 불법 시술이 줄지 않으면 '제도화로 관리' 판단을 고친다.", "fl-expr-tattoo-survey")),
    },
    "flow-family": {
        "split": INF("2024~2025년 출산율 반등이 일시적인지(늦춰진 혼인의 회복) 방향 전환인지가 갈림길이다.", "c20-pop"),
        "items": [
            FUT("계속", "작은 가구가 계속 늘어난다",
                change=INF("평균 가구원수가 계속 줄고 1인 가구가 가장 흔한 가구로 남는다.", "fl-fam-hh", "c10-1person"),
                basis=[F("평균 가구원수 2000년 3.1명 → 2025년 2.2명.", "fl-fam-hh"), F("1인 가구 2015년부터 가장 흔한 유형.", "c10-1person")],
                logic=INF("고령 1인 가구와 혼인 감소가 함께 작용해 가구가 작아진다.", "fl-fam-hh"),
                conditions=INF("혼인·출산이 크게 늘지 않아야 한다.", "c20-pop"),
                demand=INF("소형 주택, 1인용 상품·서비스, 돌봄.", "c10-1person"),
                watch=["평균 가구원수", "1인 가구 비중"], against=["혼인 건수가 몇 년 연속 크게 늘면"]),
            FUT("경로 변경", "출산율이 0명대 바닥에서 조금씩 반등한다",
                change=HYP("늦춰졌던 혼인·출산이 이어지며 출산율이 0.8명 안팎에서 조금씩 오른다.", "c20-pop"),
                basis=[F("합계출산율 2023년 0.72 → 2024년 0.75 → 2025년 0.80.", "c20-pop")],
                logic=INF("코로나로 미뤄진 혼인이 회복되며 출산이 뒤따랐다는 설명이 가능하다(추론).", "c20-pop"),
                conditions=INF("혼인 증가가 이어지고 주거·돌봄 부담이 커지지 않아야 한다.", "c20-pop"),
                demand=INF("육아 용품·돌봄 서비스.", "c20-pop"),
                watch=["혼인 건수", "합계출산율"], against=["반등이 1~2년에 그치고 다시 내려가면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("가족의 크기는 정책 구호보다 빠르게 작아졌고, 제도(동성동본·호주제)는 늘 사회 변화보다 늦게 따라왔다.", "fl-fam-pronatal", "fl-fam-law-lag"),
            favored=INF("'작은 가구로의 장기 구조 변화'라는 해석을 지지한다. 출산율 반등은 그 안의 작은 움직임으로 본다.", "fl-fam-hh", "c20-pop"),
            undecided=INF("반등이 이어질지는 2~3년 자료가 더 필요하다.", "c20-pop"),
            nextwatch=INF("2026~2027년 혼인·출산 통계.", "c20-pop"),
            change=INF("출산율이 몇 년 연속 오르면 '반등'을 '경로 변경'으로 고친다.", "c20-pop")),
    },
    "flow-city": {
        "split": INF("수도권 집중이 더 커질지, 서울 인구 감소처럼 수도권 안에서 다시 퍼질지가 갈림길이다.", "fl-city-capital", "fl-city-seoul-decline"),
        "items": [
            FUT("계속", "수도권 집중이 이어진다",
                change=INF("수도권 인구 비중이 50%를 넘은 상태에서 조금씩 더 오른다.", "fl-city-capital"),
                basis=[F("수도권 인구 비율 2019년 처음 50% 넘음.", "fl-city-capital")],
                logic=INF("일자리·학교가 몰린 곳으로 사람이 모이는 흐름은 1960년대부터 이어졌다.", "fl-city-seoulpop"),
                conditions=INF("지방 일자리 정책이 큰 변화를 만들지 못해야 한다.", "fl-city-capital"),
                demand=INF("광역 교통, 수도권 주택.", "fl-city-2004"),
                watch=["수도권 인구 비율"], against=["수도권 비율이 몇 년 연속 줄면"]),
            FUT("분화", "서울은 줄고 경기는 커진다",
                change=INF("서울 인구는 줄고 경기 신도시가 커지며 통근 거리가 늘어난다.", "fl-city-seoul-decline", "fl-city-newtown"),
                basis=[F("서울 인구 1992년 정점, 2016년 1천만 아래.", "fl-city-seoul-decline")],
                logic=INF("서울 집값이 오를수록 신도시로 옮기는 흐름은 1기 신도시 때부터 반복됐다.", "fl-city-newtown-why"),
                conditions=INF("서울 집값이 높게 유지되어야 한다.", "fl-city-newtown-why"),
                demand=INF("광역 급행 교통, 신도시 생활 시설.", "fl-city-2004"),
                watch=["서울 인구", "광역 통근 시간"], against=["서울 인구가 다시 늘면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("도시의 역사는 '서울로 모임 → 서울이 넓어짐 → 서울 밖 수도권으로 넓어짐'이고, 교통이 매번 그 확장을 따라가거나 이끌었다.", "fl-city-seoulpop", "cfill-line2", "fl-city-newtown"),
            favored=INF("'수도권 안의 분산과 수도권 전체의 집중이 함께 진행된다'는 해석을 지지한다.", "fl-city-capital", "fl-city-seoul-decline"),
            undecided=INF("거주와 교통을 따로 추적하지 않아, 교통이 집중을 키웠는지 따라갔는지는 판단하지 않았다.", "fl-city-2004"),
            nextwatch=INF("수도권 비율과 서울 인구의 방향.", "fl-city-capital"),
            change=INF("수도권 비율이 줄기 시작하면 판단을 고친다.", "fl-city-capital")),
    },
    "flow-politics": {
        "split": INF("1987년 헌법의 장치(탄핵·헌법재판소)가 위기 때마다 작동한 흐름이 이어질지, 제도 자체를 바꾸는 개헌으로 갈지가 갈림길이다.", "c10-candle", "c20-martial"),
        "items": [
            FUT("계속", "광장과 헌법 절차가 함께 작동한다",
                change=INF("권력 위기 때 시민 집회와 헌법 절차(탄핵·심판)가 함께 쓰이는 방식이 이어진다.", "c10-candle", "c20-martial"),
                basis=[F("2017년·2025년 두 번의 파면.", "c10-candle", "c20-martial")],
                logic=INF("같은 제도가 두 번 같은 방식으로 작동했다.", "er-pol-2nd"),
                conditions=INF("1987년 헌법 체계가 유지되어야 한다.", "c80-629"),
                demand=INF("정치 정보 플랫폼, 집회 안전 관리.", "c10-candle"),
                watch=["헌법재판 사건 수"], against=["개헌으로 제도가 바뀌면"]),
            FUT("경로 변경", "권력 구조를 바꾸는 개헌",
                change=HYP("반복된 위기를 계기로 대통령 권한·임기를 바꾸는 개헌 논의가 실제 개헌으로 이어진다.", "c20-martial"),
                basis=[F("2024년 비상계엄과 2025년 파면.", "c20-martial")],
                logic=INF("같은 위기가 반복되면 제도 자체를 바꾸자는 요구가 커진다.", "c20-martial"),
                conditions=INF("국회 3분의 2 동의와 국민투표가 필요하다.", "c20-martial"),
                demand=INF("제도 설명·숙의 플랫폼.", "c20-martial"),
                watch=["개헌안 발의"], against=["개헌 논의가 발의 없이 멈추면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("권력 교체 방식은 '개헌·체제 변경(1960~70년대) → 시민 항쟁(1980년대) → 헌법 절차와 광장(2000년대 이후)'으로 바뀌었다.", "cfill-3term-yushin", "c80-629", "c10-candle"),
            favored=INF("1987년 이후 헌법 절차가 위기를 처리하는 통로가 됐다는 해석을 지지한다.", "c10-candle", "c20-martial"),
            undecided=INF("정치 변화가 경제에 미친 경로는 이 흐름에서 검증하지 않았다.", "c20-martial"),
            nextwatch=INF("개헌 논의의 진행.", "c20-martial"),
            change=INF("헌법 절차가 작동하지 않는 위기가 생기면 판단을 고친다.", "c20-martial")),
    },
    "flow-economy": {
        "split": INF("다음 위기가 외부 충격(유가·금리)에서 올지, 안쪽(가계부채·부동산)에서 올지가 갈림길이다.", "c10-debt", "c20-kr-cpi"),
        "items": [
            FUT("계속", "외부 충격이 물가로 들어오는 반복",
                change=INF("에너지·원자재 충격이 물가를 올리고 금리를 움직이는 일이 되풀이된다.", "c70-kr-cpi", "c20-kr-cpi"),
                basis=[F("1973년 물가 24%, 2022년 6.3% — 둘 다 석유가 앞장섰다.", "c70-kr-cpi", "c20-kr-cpi")],
                logic=INF("에너지를 수입하는 구조가 그대로라 같은 경로가 남아 있다.", "c70-syn-chain"),
                conditions=INF("에너지 수입 의존이 유지되어야 한다.", "c70-syn-chain"),
                demand=INF("에너지 절약·대체 에너지, 물가 방어 상품.", "c70-syn-chain"),
                watch=["국제유가", "소비자물가 중 석유류"], against=["에너지 수입 의존이 크게 줄면"]),
            FUT("경로 변경", "가계부채가 다음 위기의 출발점이 된다",
                change=HYP("금리가 오를 때 가계부채 부담이 소비를 누르는 쪽이 외부 충격보다 큰 위험이 된다.", "c10-debt", "c2020-hike"),
                basis=[F("2016년 가계신용 1,257조 원, 1년 새 125조 원 증가.", "c10-debt"), F("2021년 금리 인상은 가계부채·집값을 더 큰 위험으로 본 결정.", "c2020-hike")],
                logic=INF("외환위기 뒤 외환보유액을 쌓아 바깥 충격 완충은 커졌지만, 안쪽의 빚은 커졌다.", "c97-reserve-build", "c10-debt"),
                conditions=INF("금리가 높게 유지되고 집값이 떨어져야 드러난다.", "c2020-hike"),
                demand=INF("부채 조정·상담 서비스.", "c10-debt"),
                watch=["가계부채 비율", "연체율"], against=["가계부채가 줄어들면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("위기마다 한국은 다음 위기를 막을 수단을 하나씩 만들었다(외환보유액, 금리 정책). 그런데 그 수단이 또 다른 약점(저금리 → 가계부채)을 키우기도 했다.", "c97-reserve-build", "c10-rate", "c10-debt"),
            favored=INF("외부 충격의 완충력은 커졌지만 안쪽 부채가 새 약점이라는 해석을 지지한다.", "c08-diff97", "c10-debt"),
            undecided=INF("다음 위기가 언제 어디서 올지는 판단할 수 없다.", "c10-debt"),
            nextwatch=INF("가계부채와 금리의 방향(대표 분석에서 끝까지 따라감).", "c2020-hike"),
            change=INF("가계부채 비율이 크게 줄면 '안쪽 위기' 판단을 고친다.", "c10-debt")),
    },
    "flow-tech": {
        "split": INF("다음 '손안의 기기'가 스마트폰 위의 AI 서비스로 머물지, 새 기기로 옮겨 갈지가 갈림길이다.", "er-tech-ai", "c00-kr-iphone"),
        "items": [
            FUT("결합", "AI가 스마트폰 안으로 들어온다",
                change=INF("새 기기보다 이미 쓰는 스마트폰·앱에 AI가 붙어 쓰임이 넓어진다.", "er-tech-ai", "c10-kakao"),
                basis=[F("생성형 AI 이용 1년 새 33.3% → 44.5%.", "er-tech-ai")],
                logic=INF("카카오톡이 아이폰 위에서 퍼졌듯, 새 서비스는 이미 보급된 기기 위에서 가장 빨리 퍼졌다.", "c10-kakao"),
                conditions=INF("AI 서비스가 기존 앱 안에서 쓸 만해야 한다.", "er-tech-ai"),
                demand=INF("AI 기능 탑재 기기·앱.", "er-tech-ai"),
                watch=["AI 이용률", "AI 탑재 스마트폰 판매"], against=["별도 AI 기기가 빠르게 팔리면"]),
            FUT("경로 변경", "새 기기가 나타난다",
                change=HYP("TV → 휴대폰 → 스마트폰처럼 AI를 중심으로 한 새 기기가 나타난다.", "c60-kr-tv-1", "c00-kr-iphone"),
                basis=[F("스마트폰 가입자 2009년 80만 → 2010년 722만 — 새 기기는 빠르게 퍼졌다.", "c00-kr-iphone")],
                logic=INF("화면과 기기가 바뀔 때마다 '집 안 → 손안'으로 거리가 좁혀졌다.", "c70-culture-why", "c00-kr-iphone"),
                conditions=INF("새 기기가 스마트폰보다 확실히 편해야 한다.", "c00-kr-iphone"),
                demand=INF("착용형 기기, 음성 기반 기기.", "er-tech-ai"),
                watch=["새 기기 판매"], against=["새 기기 판매가 정체되면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("기기는 '집에 하나(라디오·TV) → 가족마다(전화) → 사람마다(휴대폰) → 손안의 생활(스마트폰)'으로, 점점 더 개인에게 가까워졌다.", "c60-kr-radio-3", "er-rel-phone", "c00-kr-iphone"),
            favored=INF("지금은 AI가 새 기기보다 기존 기기 위에서 퍼지는 '결합' 해석을 지지한다.", "er-tech-ai"),
            undecided=INF("AI 이용이 생활을 얼마나 바꾸는지(쓰는 시간·목적)는 판단할 수 없다.", "er-tech-ai"),
            nextwatch=INF("AI 이용률과 이용 목적.", "er-tech-ai"),
            change=INF("별도 AI 기기가 빠르게 보급되면 판단을 고친다.", "er-tech-ai")),
    },
    "flow-leisure": {
        "split": INF("코로나 뒤 다시 밖으로 나간 여가가 계속 밖에 머물지, 배달·화면 중심의 집 안 여가로 돌아갈지가 갈림길이다.", "c2020-endsd", "c10-delivery"),
        "items": [
            FUT("분화", "집 안과 집 밖이 목적별로 나뉜다",
                change=INF("일상의 여가는 집 안(배달·영상), 특별한 여가는 집 밖(여행·공연)으로 나뉜다.", "c10-delivery", "c80-travel"),
                basis=[F("배달앱 이용자 2,500만(2019).", "c10-delivery"), F("2022년 거리두기 해제 뒤 다시 밖으로.", "c2020-endsd")],
                logic=INF("극장 → TV, 노래방 → 배달처럼 집 안 여가가 늘 때도 밖의 여가는 다른 의미로 남았다.", "er-lei-tv-theater", "c10-delivery"),
                conditions=INF("배달·영상 비용이 유지되어야 한다.", "c10-delivery"),
                demand=INF("집 안 오락, 특별한 외출 경험.", "c10-delivery"),
                watch=["오락·문화 지출 비중", "배달 거래액"], against=["오락 지출 비중이 코로나 전보다 크게 높아지면"]),
            FUT("계속", "주말·휴가가 늘어 밖의 여가가 커진다",
                change=HYP("근로시간이 더 줄면 여행·운동 같은 집 밖 여가가 커진다.", "c00-5day-leisure"),
                basis=[F("주5일 근무 뒤 주말 여가가 퍼졌다.", "c00-5day-leisure")],
                logic=INF("일하지 않는 시간이 늘 때 밖의 여가가 함께 늘었다.", "c00-5day-leisure"),
                conditions=INF("근로시간 단축(주 4.5일 논의 등)이 실현되어야 한다.", "c10-52h"),
                demand=INF("국내 여행, 레저 시설.", "c00-5day-leisure"),
                watch=["근로시간", "국내 여행 횟수"], against=["근로시간이 줄지 않으면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("여가는 새 기기가 생길 때마다 집 안으로 들어왔고(TV·배달), 시간이 생길 때마다 밖으로 나갔다(통금 해제·주5일).", "er-lei-tv-theater", "c00-5day-leisure"),
            favored=INF("목적별 분화 해석을 지지한다.", "c2020-spend", "c2020-endsd"),
            undecided=INF("장기 여가 지출 추이는 지표로만 보고 원인을 나누지 않았다.", "c2020-spend"),
            nextwatch=INF("근로시간 단축 논의의 결과.", "c10-52h"),
            change=INF("집 안 여가 지출이 계속 크게 늘면 판단을 고친다.", "c2020-spend")),
    },
    "flow-time": {
        "split": INF("일하는 시간을 법으로 더 줄일지(주 4.5일 논의), 지금 수준에서 유연하게 나눌지가 갈림길이다.", "c10-52h"),
        "items": [
            FUT("계속", "일하는 시간이 더 줄어든다",
                change=INF("법정 근로시간이 1953년 주 48시간 → 1989년 44시간 → 2004년 주5일 → 2018년 52시간 상한으로 줄었듯, 다음 단계 단축이 이어진다.", "tf-time-law", "c10-52h"),
                basis=[F("근로시간 단축의 단계들.", "tf-time-law", "c00-5day"), F("2025년 연평균 1,833시간으로 OECD 평균보다 여전히 길다.", "tf-time-oecd25")],
                logic=INF("OECD 평균과의 차이가 줄지 않아 단축 압력이 남아 있다.", "tf-time-oecd25"),
                conditions=INF("생산성 우려를 넘는 합의가 필요하다.", "tf-time-oecd25"),
                demand=INF("주중 여가·자기계발 서비스.", "c00-5day-leisure"),
                watch=["연간 근로시간", "주 4.5일제 시범 사업"], against=["단축 논의가 생산성 문제로 멈추면"]),
            FUT("분화", "시간을 나누는 방식이 갈라진다",
                change=HYP("총 시간은 비슷해도 재택·유연근무로 '언제 일하나'가 사람마다 달라진다.", "c2020-endsd"),
                basis=[F("감염병 시기에 방역이 영업·모임 시간을 직접 바꿨다.", "c2020-endsd")],
                logic=INF("시간을 정하는 주체가 법·방역·회사로 옮겨 다녔다 — 다음은 개인 단위 조정일 수 있다.", "c2020-endsd", "c10-52h"),
                conditions=INF("유연근무 제도가 넓어져야 한다.", "c10-52h"),
                demand=INF("평일 낮 여가, 유연근무 도구.", "c10-52h"),
                watch=["유연근무 이용률"], against=["출근 중심 근무가 다시 강해지면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("일하지 않는 시간은 '밤(통금 해제, 1982)'이 먼저 열리고 '주말(주5일, 2004)'이 다음에 생겼다. 밤이 풀린 뒤에도 일하는 시간 자체는 1980년 주 53.9시간에서 천천히 줄었다.", "c80-curfew", "c00-5day", "tf-time-1980"),
            favored=INF("시간은 기술이 아니라 제도(통금·노동법·방역)가 정해 왔다는 해석을 지지한다.", "c80-curfew", "c10-52h", "c2020-endsd"),
            undecided=INF("1970년대 연도별 근로시간은 아직 연결하지 못해, 1970년대 안의 변화는 판단하지 않았다.", "tf-time-1980"),
            nextwatch=INF("주 4.5일제 논의와 연간 근로시간.", "tf-time-oecd25"),
            change=INF("근로시간이 다시 늘기 시작하면 판단을 고친다.", "tf-time-oecd25")),
    },
    "flow-sports": {
        "split": INF("스포츠가 '보는 것(관중·중계)' 중심으로 더 커질지, '직접 하는 것(동호회·운동)'이 커질지가 갈림길이다.", "er-sp-2022", "fl-rel-sports"),
        "items": [
            FUT("계속", "경기장 관람이 다시 커진다",
                change=INF("관중 제한이 풀린 뒤 경기장 관람이 이어진다.", "er-sp-2022", "er-sp-100m"),
                basis=[F("2022년 관중 제한 없는 시즌 재개.", "er-sp-2022"), F("누적 관중 1억 명(2010).", "er-sp-100m")],
                logic=INF("함께 응원하는 경험에 대한 수요는 팀 해체·감염병 같은 중단 뒤에도 돌아왔다.", "c00-worldcup", "er-sp-2022"),
                conditions=INF("관람 가격이 감당할 수준이어야 한다.", "er-sp-2022"),
                demand=INF("응원 상품, 경기장 식음료.", "er-sp-2022"),
                watch=["프로야구 관중 수"], against=["관중이 코로나 전보다 계속 적으면"]),
            FUT("분화", "보는 사람과 하는 사람이 나뉜다",
                change=HYP("관람은 중계·경기장으로, 직접 운동은 동호회·러닝처럼 따로 커진다.", "fl-rel-sports"),
                basis=[F("함께 운동하는 비율 71.5%(2013), 동호회 가입 11.3%(2023).", "fl-rel-sports")],
                logic=INF("보는 즐거움과 하는 즐거움은 다른 시간·돈을 쓴다.", "fl-rel-sports"),
                conditions=INF("운동 동호회 가입이 늘어야 한다.", "fl-rel-sports"),
                demand=INF("운동 장비, 동호회 플랫폼.", "fl-rel-sports"),
                watch=["체육 동호회 가입률"], against=["가입률이 정체되면"]),
        ],
        "conclusion": CONCLUDE(
            key=INF("스포츠는 'TV 앞(1960년대) → 신문사·학교(1970년대) → 프로 리그(1982) → 광장 응원(2002) → 경기장 복귀'로, 보는 방식이 크게 바뀌었다.", "er-sp-60s", "c80-baseball", "c00-worldcup"),
            favored=INF("관람 수요는 중단 뒤에도 돌아온다는 해석을 지지한다.", "er-sp-2022"),
            undecided=INF("관중·구단의 경제 자료는 연결하지 않아 산업 규모는 판단하지 않았다.", "er-sp-100m"),
            nextwatch=INF("관중 수와 동호회 참여.", "er-sp-2022"),
            change=INF("관중이 장기적으로 줄면 판단을 고친다.", "er-sp-2022")),
    },
}

# 시대 흐름 안의 반복(R-CY) — at은 그 흐름의 단계 id
ERA_REPEATS = {
    "flow-expression": [REPEAT("반작용", "교복 자율화 3년 뒤 다시 교복으로 — 자유의 불편이 되돌림을 부르다",
        past=F("1982~83년 정부가 두발·교복 자율화를 발표해 85년 만에 교복 의무가 풀렸다.", "fl-expr-uniform"),
        now=F("1986년 2학기부터 자유복의 가계 부담, 빈부 차이에서 오는 위화감, 생활지도의 어려움을 이유로 교복 여부가 학교장 재량이 되었고 교복으로 돌아가는 학교가 늘었다.", "fl-expr-uniform-back"),
        alike=INF("겉모양(교복)은 돌아왔지만 동기는 달랐다 — 처음의 교복은 규율이었고, 돌아온 교복은 비용·위화감을 줄이는 수단으로 설명됐다.", "fl-expr-uniform-back"),
        changed=INF("의무에서 학교 선택으로 바뀌었다. 자율화가 낳은 새 불편(옷값·비교)이 되돌림의 조건이 됐다.", "fl-expr-uniform", "fl-expr-uniform-back"),
        alternatives=[INF("정치 설명 — 자율화 자체가 유화정책의 하나였다는 설명이 있어, 되돌림도 정치 상황의 변화일 수 있다.", "fl-expr-uniform")],
        counter=[F("두발 단속과 장발 단속은 1970년대 방식으로 돌아오지 않았고, 1990년대 X세대는 '입고 싶은 대로' 입었다.", "er-expr-x")],
        at=["x2", "x3"])],
    "flow-music": [REPEAT("재등장", "1960년대 세시봉 음악이 2010년 TV로 다시 유행",
        past=F("1960년대 도심 음악감상실 세시봉에서 통기타 가수들이 활동했다.", "c60-sesibong"),
        now=F("2010~2011년 방송 출연 뒤 통기타 판매·음반 주문이 늘고 '세시봉' 간판의 라이브 클럽이 생겼다.", "c10-sesibong"),
        alike=INF("같은 가수·같은 노래였지만, 듣는 사람은 그때의 청년이 중장년이 되어 추억으로 들었다.", "c10-sesibong"),
        changed=INF("통로가 음악감상실에서 TV 예능으로 바뀌었고, 스마트폰 시대의 아날로그 복고와 겹쳤다.", "c10-analog"),
        alternatives=[INF("공급 설명 — 방송사의 기획이 먼저였고, 수요가 저절로 돌아온 것은 아닐 수 있다.", "c10-sesibong")],
        counter=[F("같은 시기 노래방 수는 줄기 시작했다 — 옛 음악 공간 전부가 돌아온 것은 아니다.", "fl-mus-noraebang-peak")],
        at=["m1", "m7"])],
}

# 취향 흐름: 기존 '다음 수요'에 종류·예상 변화·연결 논리를 더한다(이름 → (종류, 예상 변화, 연결 논리)).
TASTE_ADD = {
    "taste-home": {
        "이사해도 데려가는 모듈·원상복구 생활용품": ("계속", "셋집에서 흔적 없이 꾸미는 상품이 기본이 된다.", "원상복구 기준과 잦은 이사가 지금의 선택을 만들었으므로, 그 조건이 남는 한 같은 방향이 이어진다."),
        "믿고 사는 중고·복원 가구": ("결합", "빈티지 선호와 검수·운반 서비스가 합쳐진다.", "좋은 물건을 오래 쓰고 싶은 욕구와 중고의 불안을 서비스가 메운다."),
        "손이 덜 가는 집(수납·자동화)": ("분화", "꾸미는 집과 관리가 쉬운 집으로 나뉜다.", "시간이 부족한 가구는 연출보다 관리의 수고를 줄이는 쪽을 고른다."),
        "사진용이 아닌 '생활감' 있는 내추럴": ("반작용", "연출된 집에 대한 피로로 생활감 있는 집이 다시 선택된다.", "획일화된 연출에 대한 불편이 반대 방향의 선택을 부른다."),
    },
    "taste-pants": {
        "조이지 않는 슬림·세미 부츠컷": ("반작용", "와이드가 오래 기본이 된 뒤 슬림이 '조이지 않는' 형태로 돌아온다.", "새로움이 줄어든 기본 핏에 대한 반대 방향의 선택이지만, 편안함 기준은 남는다."),
        "볼륨 모양의 변주": ("분화", "와이드 안에서 모양을 바꾼 변형들이 계속 나온다.", "편안함은 공통 기준, 구별은 디테일로 하는 구조가 이어진다."),
        "기능성 소재의 일상복": ("결합", "운동복 소재와 일상복이 합쳐진다.", "운동 인구와 웰니스 관심이 일상복의 기준을 바꾼다."),
    },
    "taste-dining": {
        "중간 가격대 '특별한 날' 경험": ("분화", "특별한 외식이 고가와 중간 가격대로 나뉜다.", "고물가 속에서 '특별함'의 기준 가격이 내려왔다."),
        "셰프 경험을 집으로 — 간편식·협업 상품": ("결합", "식당 경험과 간편식이 합쳐진다.", "매장 예약이 어려울 때 경험의 일부를 상품으로 산다."),
        "술 없이 오래 머무는 모임 공간": ("경로 변경", "음주 중심 모임 장소가 식사 중심으로 바뀐다.", "회식·음주 감소가 모임 장소의 기준을 바꾼다."),
        "혼자 먹는 한 그릇": ("계속", "1인 메뉴가 더 늘어난다.", "1인 가구 증가가 이어지는 한 같은 방향이다."),
    },
    "taste-goods": {
        "하나만 다는 고급 참": ("반작용", "여러 개 다는 연출 대신 하나만 다는 고급 소품.", "식상함에 대한 반대 방향의 선택이 고급화로 나타난다."),
        "꾸미는 대상의 확장": ("계속", "가방 다음으로 텀블러·휴대폰까지 꾸민다.", "꾸미기 행동이 남아 대상만 바뀐다."),
        "다음 캐릭터로의 이동": ("경로 변경", "인기 캐릭터가 바뀌며 수요가 옮겨 간다.", "블라인드·한정 판매 방식은 남고 대상만 교체된다."),
    },
    "taste-gather": {
        "술 없이 오래 머무는 모임 장소": ("경로 변경", "술 중심 모임 장소가 식사·낮 모임으로 바뀐다.", "음주 감소가 모임 장소를 바꾼다."),
        "정기적인 동네·운동 모임": ("반작용", "일회성 앱 모임의 피로로 정기 모임이 늘어난다.", "관계가 깊어지지 않는 불편이 지속성을 고르게 한다."),
        "업무 시간 안의 짧은 팀 모임": ("분화", "저녁 회식이 업무 시간 안 짧은 모임으로 바뀐다.", "회식 거부가 아니라 형식 변경 요구라는 자료와 맞는다."),
    },
}

TASTE_END = {
    "taste-home": CONCLUDE(
        key=INF("집을 채우는 기준이 '세트로 한 번에 장만'에서 '적은 돈으로 바꾸고, 흔적 없이, 남과 다르게'로 옮겨 갔다. 셋집·잦은 이사라는 조건이 선택을 크게 정했다.", "ts-h-mz", "ts-h-2025"),
        favored=INF("유행의 교체보다 조건(주거 형태)이 기준을 정했다는 해석을 지지한다.", "ts-h-2025"),
        undecided=INF("비우는 사람과 모으는 사람이 같은 사람인지는 판단할 수 없다.", "ts-h-minimal"),
        nextwatch=INF("무타공·모듈·중고 가구 거래의 지속 여부.", "ts-h-2025", "ts-h-carrot"),
        change=INF("자가 비중이 늘고 시공 수요가 반등하면 판단을 고친다.", "ts-h-2025")),
    "taste-pants": CONCLUDE(
        key=INF("바지 모양은 '조이는 것 ↔ 넓은 것' 사이를 오갔지만, 와이드 이후에는 편안함이 공통 기준이 되고 구별은 디테일로 하는 구조로 바뀌었다.", "ts-f-spao-why", "ts-f-harem"),
        favored=INF("'반대 유행의 반복'보다 '편안함 기준의 고정 + 변주' 해석을 지지한다.", "ts-f-spao", "ts-f-slim-back"),
        undecided=INF("돌아온 슬림이 얼마나 퍼질지는 판단할 수 없다.", "ts-f-slim-back"),
        nextwatch=INF("데님 판매 순위에서 슬림·부츠컷 비중.", "ts-f-slim-back"),
        change=INF("조이는 스키니가 다시 다수가 되면 판단을 고친다.", "ts-f-slim-back")),
    "taste-dining": CONCLUDE(
        key=INF("외식에서 사는 것은 '음식'보다 '경험'이었고, 고물가 속에서 그 경험의 값이 내려왔다(오마카세 → 애프터눈 티·뷔페).", "ts-d-omakase-fall", "ts-d-tea", "ts-d-family"),
        favored=INF("'특별한 날은 쓴다, 다만 기준 가격이 내려왔다' 해석을 지지한다.", "ts-d-highend-survey", "ts-d-tea"),
        undecided=INF("소득별 외식 자료가 없어 같은 사람이 절약·지출을 함께 하는지는 판단할 수 없다.", "ts-d-highend-survey"),
        nextwatch=INF("중간 가격대 코스와 모임형 식당 예약.", "ts-d-tea", "ts-d-family"),
        change=INF("기념일 외식도 크게 줄면 판단을 고친다.", "ts-d-highend-survey")),
    "taste-goods": CONCLUDE(
        key=INF("작은 인형 하나는 '새 가방 대신'이라는 절약과 '한정판 웃돈'이라는 수집을 동시에 담았다.", "ts-g-bagku-why", "ts-g-labubu"),
        favored=INF("같은 물건에 서로 다른 동기가 겹쳤다는 해석을 지지한다.", "ts-g-bagku-why", "ts-g-soldout"),
        undecided=INF("두 동기가 같은 사람의 것인지는 판단할 수 없다.", "ts-g-labubu"),
        nextwatch=INF("리셀 가격과 만들기·꾸미기 검색.", "ts-g-fall", "ts-g-search"),
        change=INF("리셀 거래가 크게 살아나면 판단을 고친다.", "ts-g-fall")),
    "taste-gather": CONCLUDE(
        key=INF("회식이 줄었다고 덜 만나는 것이 아니라, 강요 없는 짧은 모임과 취향 모임으로 '다르게' 만나는 쪽이 자료와 맞는다.", "ts-r-zgen", "ts-r-munto"),
        favored=INF("'덜'보다 '다르게' 해석을 지지하지만, 플랫폼 수치는 회사 발표가 많다.", "ts-r-munto", "ts-r-somoim"),
        undecided=INF("전체 인구의 만남 빈도 자료가 없어 판단할 수 없다.", "ts-r-zgen"),
        nextwatch=INF("정기 모임 재참여율.", "ts-r-somoim"),
        change=INF("모임 참여 자체가 줄어든다는 조사가 나오면 판단을 고친다.", "ts-r-zgen")),
}


def _short(t, n=110):
    t = t.strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind(". "), cut.rfind("다."))
    return (cut[:k + 2] if k > 40 else cut.rstrip() + "…").strip()


def _chk(x, cids, w):
    if x["layer"] in ("fact", "source") and not x["ids"]:
        raise SystemExit(f"{w}: 근거 없는 사실")
    for i in x["ids"]:
        if i not in cids:
            raise SystemExit(f"{w}: 없는 근거 {i}")


def apply(flows, tastes, claims_all):
    cids = {c["id"] for c in claims_all}
    ctext = {c["id"]: c for c in claims_all}
    by = {f["id"]: f for f in flows}
    miss = set(by) - set(ERA)
    if miss:
        raise SystemExit(f"미래·결론이 없는 시대 흐름 {miss}")
    for fid, ex in ERA.items():
        items = ex["items"]
        if len(items) < 2 or len({x["kind"] for x in items}) < 2:
            raise SystemExit(f"{fid}: 서로 다른 종류의 미래 2개 이상")
        _chk(ex["split"], cids, fid)
        for x in items:
            for k in ("change", "logic", "conditions", "demand"):
                _chk(x[k], cids, f"{fid} 미래")
            for b in x["basis"]:
                _chk(b, cids, f"{fid} 미래 근거")
        for k in ("key", "favored", "undecided", "next", "change"):
            _chk(ex["conclusion"][k], cids, f"{fid} 결론")
        by[fid]["futures"] = {"split": ex["split"], "items": items}
        rps = ERA_REPEATS.get(fid, [])
        sids = {st["id"] for st in by[fid]["steps"]}
        for rp in rps:
            for a in rp["at"]:
                if a not in sids:
                    raise SystemExit(f"{fid}: 반복 링크 단계 {a} 없음")
            for part in ("past", "now", "alike", "changed"):
                _chk(rp[part], cids, f"{fid} 반복")
            for x in rp["alternatives"] + rp["counter"]:
                _chk(x, cids, f"{fid} 반복")
        by[fid]["repeats"] = rps
        by[fid]["conclusion"] = ex["conclusion"]
    for t in tastes:
        add = TASTE_ADD[t["id"]]
        items = []
        for d in t["future"]["directions"]:
            if d["name"] not in add:
                raise SystemExit(f"{t['id']}: 종류가 없는 다음 수요 {d['name']}")
            kind, change, logic = add[d["name"]]
            assert kind in FUTURE_KINDS
            ids = [i for i in d.get("basis", []) if i in cids]
            if not ids:
                raise SystemExit(f"{t['id']} {d['name']}: 근거 없음")
            items.append(FUT(kind, d["name"],
                             change=HYP(change, *ids), basis=[(F if ctext[i]["claimType"] in ("fact", "statistical") else SRC)(_short(ctext[i]["text"]), i) for i in ids],
                             logic=INF(logic, *ids), conditions=HYP(d["condition"], *ids), demand=HYP(d["products"], *ids),
                             watch=[d["signals"]], against=[d["counter"]]))
        if len({x["kind"] for x in items}) < 2:
            raise SystemExit(f"{t['id']}: 미래 종류가 한 가지")
        un = t["future"].get("unmet") or []
        split = INF(un[0]["text"], *[i for i in un[0].get("basis", []) if i in cids]) if un else INF("—")
        t["futures"] = {"split": split, "items": items}
        end = TASTE_END[t["id"]]
        for k in ("key", "favored", "undecided", "next", "change"):
            _chk(end[k], cids, f"{t['id']} 결론")
        t["conclusion"] = end
