"""2.0 빈 해 채우기 (2026-11-11): 한국 사건이 하나도 없던 해(1967·1969·1981·1984·1991·1992·2005·2006)에 출처 2개 이상인 사건을 넣는다.
관계는 deep 모듈 형식(CHAIN/NODES/EDGES)으로 기존 노드와 잇는다. 새 노드는 만들지 않고 사건 노드만 쓴다.
"""
from era_1960s import C
from era_1980s import S

SOURCES = [
    S("arch-plan2", "제2차 경제개발 5개년 계획(1967~1971)", "국가기록원 '기록으로 보는 경제개발 5개년 계획'", "https://theme.archives.go.kr/next/economicDevelopment/secondary.do", "government"),
    S("kdev-plan2", "The Second Five-Year Economic Development Plan (1967-1971)", "K-Developedia (KDI 국제정책대학원)", "https://www.kdevelopedia.org/Resources/view/04201403110130852.do", "institution"),
    S("arch-const6", "헌법개정사 — 제6차 개정(1969년 10월 21일)", "국가기록원 '헌법이야기'", "https://theme.archives.go.kr/next/rule/sub2_07.do", "government"),
    S("arch-chron-1969", "연표: 1969년 9월 14일 개헌안 국회 통과, 10월 17일 국민투표(투표율 77.1%)", "국가기록원 '연표와 기록'", "https://theme.archives.go.kr/next/chronology/searchArchive.do?page=331", "government"),
    S("pressian-3term", "서중석의 현대사 이야기 — 3선 개헌 반대 운동", "프레시안", "https://pressian.com/pages/articles/132058", "news"),
    S("arch-olympic", "88서울올림픽 개최 — 1981년 9월 30일 개최지 선정", "국가기록원 '대통령기록·정책'", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=402", "government"),
    S("khan-badenbaden", "1981년 9월 30일 바덴바덴 — '서울 52, 나고야 27' (2011.9.29)", "경향신문", "https://www.khan.co.kr/article/201109292200245", "news"),
    S("arch-line2", "1984년 5월 22일 서울지하철 2호선 전 구간 개통", "국가기록원 '오늘의 기록'", "https://theme.archives.go.kr/next/daily/viewMain.do?selectDay=19840522", "government"),
    S("arch-subway", "기록으로 보는 대한민국: 지하철", "국가기록원", "https://theme.archives.go.kr/next/koreaOfRecord/subway.do", "government"),
    S("seoul-subway50", "서울 지하철 50년사 — 2호선 1984년 순환선 완전 개통", "서울시 내 손안에 서울", "https://mediahub.seoul.go.kr/archives/2012200", "government"),
    S("arch-un", "남북 유엔 동시가입 (1991.9.17)", "국가기록원 '대통령기록·정책'", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=602", "government"),
    S("seoul-1991-un", "만장일치 가입… 태극기 오르던 날 (1991.9.18)", "서울신문", "https://www.seoul.co.kr/news/1991/09/18/19910918003001", "news"),
    S("arch-china", "한중수교 (1992.8.24)", "국가기록원 '대통령기록·정책'", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=508", "government"),
    S("seoul-1992-china", "한중 수교 공동성명 — 대사급 외교관계 수립 (1992.8.25)", "서울신문", "https://www.seoul.co.kr/news/1992/08/25/19920825003001", "news"),
    S("arch-hoju", "호주제 폐지", "국가기록원 '대통령기록·정책'", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=225", "government"),
    S("pressian-hoju", "2008년부터 호적 대신 가족관계등록부", "프레시안", "https://pressian.com/pages/articles/88102", "news"),
    S("seoul-2005-hoju", "개정 민법 국회 통과 — 자녀의 성·본 (2005.3.16)", "서울신문", "https://m.seoul.co.kr/news/2005/03/16/20050316029004", "news"),
    S("arch-korusfta", "한미FTA 협상 타결", "국가기록원 '대통령기록·정책'", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=324", "government"),
    S("cine21-bc-ad", "'부자되세요' 유행시킨 BC카드 광고 — 애교있는 직설화법 (2002)", "씨네21", "https://cine21.com/news/view/?mag_id=7559", "news"),
    S("kr-seoul-2002-star", "'2002년은 우리 해' — CF '부자 되세요'로 인기 모은 김정은 (2002.12.25)", "서울신문", "https://m.seoul.co.kr/news/2002/12/25/20021225015001", "news"),
    S("kr-seoul-2002-cardcrime", "'빚으로 사세요' 돈놀이 혈안 — 카드 광고 패러디 (2002.5.10)", "서울신문", "https://www.seoul.co.kr/news/2002/05/10/20020510010001", "news"),
    S("book-trend2018", "트렌드 코리아 2018 (서울대 소비트렌드분석센터, 미래의창) — 책 소개", "왓챠피디아 도서 정보", "https://pedia.watcha.com/en/contents/bovqkeb/book_description", "reference"),
    S("kr-jjan-2019-trend", "신문으로 되짚은 2018년 — '소확행'·'워라밸'이 한 해 내내 (2019.1.3)", "전북일보", "https://jjan.kr/article/20190103659767", "news"),
    S("nielsen-sohwak", "한국인의 소소한 행복 — 닐슨코리아 '소확행' 버즈 분석", "아이보스(닐슨코리아 발표 인용)", "https://www.i-boss.co.kr/ab-2877-2632", "news"),
    S("etoday-fta-log", "한미FTA 주요 일지 (2012.2.21)", "이투데이", "https://www.etoday.co.kr/news/view/548002", "news"),
]

CLAIMS = [
    C("cfill-plan2", "1967년 시작된 제2차 경제개발 5개년 계획(1967~1971)은 산업구조 근대화와 자립경제 확립을 목표로 하고, 경공업에서 화학·철강·기계 같은 중화학공업으로 옮겨 가는 방향을 내세웠다. 계획안은 1966년 중반에 확정되었다.",
      "fact", "verified", ["arch-plan2", "kdev-plan2"], ["economy", "industry"], ["KR"]),
    C("cfill-3term", "대통령의 3선 연임을 허용하는 개헌안은 1969년 9월 14일 새벽 여당 의원만 모인 국회 제3별관에서 처리되었고, 10월 17일 국민투표(투표율 77.1%)로 확정되었다. 야당과 대학가의 반대 시위가 이어졌다.",
      "fact", "verified", ["arch-const6", "arch-chron-1969", "pressian-3term"], ["politics"], ["KR"]),
    C("cfill-3term-yushin", "3선 개헌으로 1971년 세 번째 대통령 선거에 나설 수 있게 된 박정희 대통령은 이듬해 1972년 10월 유신으로 연임 제한이 없는 체제를 만들었다. 3선 개헌이 유신 체제로 가는 길을 열었다는 평가가 일반적이다.",
      "interpretation", "sourced", ["pressian-3term"], ["politics"], ["KR"]),
    C("cfill-bid", "1981년 9월 30일 서독 바덴바덴 국제올림픽위원회 총회에서 서울이 일본 나고야를 52대 27로 누르고 1988년 하계올림픽 개최지로 뽑혔다. 열세라는 예상을 뒤집은 결과였다.",
      "fact", "verified", ["arch-olympic", "khan-badenbaden"], ["politics", "culture"], ["KR", "JP"]),
    C("cfill-line2", "서울지하철 2호선은 1984년 5월 22일 전 구간이 개통되어 강남과 강북을 한 바퀴 도는 순환선이 되었다. 처음 계획에는 없던 노선으로, 서울의 도심 기능을 강남으로 옮기는 과정에서 구체화되었다.",
      "fact", "verified", ["arch-line2", "arch-subway", "seoul-subway50"], ["society"], ["KR"]),
    C("cfill-un", "1991년 9월 17일 제46차 유엔총회는 남북한 유엔 가입안을 표결 없이 통과시켰다. 북한이 160번째, 한국이 161번째 회원국이 되었다.",
      "fact", "verified", ["arch-un", "seoul-1991-un"], ["politics"], ["KR", "WORLD"]),
    C("cfill-china", "한국과 중국은 1992년 8월 24일 베이징에서 수교 공동성명에 서명해 대사급 외교관계를 맺었고, 같은 날 한국은 대만과 단교했다. 이후 중국은 한국의 최대 교역국이 되었다.",
      "fact", "verified", ["arch-china", "seoul-1992-china"], ["politics", "economy"], ["KR", "CN"]),
    C("cfill-hoju", "헌법재판소의 헌법불합치 결정(2005년 2월 3일)에 이어 국회는 2005년 3월 2일 호주제를 없애는 민법 개정안을 통과시켰다. 2008년 1월 1일부터 호적 대신 개인별 가족관계등록부를 쓰고, 부부가 합의하면 자녀가 어머니의 성을 따를 수도 있게 되었다.",
      "fact", "verified", ["arch-hoju", "pressian-hoju", "seoul-2005-hoju"], ["society", "politics"], ["KR"]),
    C("cfill-fta", "한국과 미국은 2006년 2월 3일 자유무역협정(FTA) 협상 개시를 선언했고, 2007년 4월 2일 타결, 추가 협상을 거쳐 2012년 3월 15일 발효되었다. 협상 기간 내내 격렬한 반대 시위가 이어졌다.",
      "fact", "verified", ["arch-korusfta", "etoday-fta-log"], ["economy", "politics"], ["KR", "US"]),
]

EVENTS = [
    {"id": "e60-plan2", "eraId": "1960s", "date": "1967", "title": "제2차 경제개발 5개년 계획 시작 (1967~1971)", "countries": ["KR"], "domains": ["economy", "industry"], "claimIds": ["cfill-plan2"], "priority": 2},
    {"id": "e60-3term", "eraId": "1960s", "date": "1969-10-17", "title": "3선 개헌 국민투표 확정", "countries": ["KR"], "domains": ["politics"], "claimIds": ["cfill-3term", "cfill-3term-yushin"], "priority": 2},
    {"id": "e80-bid", "eraId": "1980s", "date": "1981-09-30", "title": "바덴바덴: 1988 서울올림픽 유치 결정", "countries": ["KR"], "domains": ["politics", "culture"], "claimIds": ["cfill-bid"], "priority": 2},
    {"id": "e80-line2", "eraId": "1980s", "date": "1984-05-22", "title": "서울지하철 2호선 순환선 완전 개통", "countries": ["KR"], "domains": ["society"], "claimIds": ["cfill-line2"], "priority": 3},
    {"id": "e90-un", "eraId": "1990s", "date": "1991-09-17", "title": "남북한 유엔 동시 가입", "countries": ["KR"], "domains": ["politics"], "claimIds": ["cfill-un"], "priority": 2},
    {"id": "e90-china", "eraId": "1990s", "date": "1992-08-24", "title": "한중 수교 (대만과 단교)", "countries": ["KR", "CN"], "domains": ["politics", "economy"], "claimIds": ["cfill-china"], "priority": 1},
    {"id": "e00-hoju", "eraId": "2000s", "date": "2005-03-02", "title": "호주제 폐지 민법 개정 (2008년 시행)", "countries": ["KR"], "domains": ["society"], "claimIds": ["cfill-hoju"], "priority": 2},
    {"id": "e00-korusfta", "eraId": "2000s", "date": "2006-02-03", "title": "한미 FTA 협상 개시 (2007 타결·2012 발효)", "countries": ["KR", "US"], "domains": ["economy", "politics"], "claimIds": ["cfill-fta"], "priority": 2},
]

CHAIN = {"id": "fill-years", "title": "빈 해 채우기로 더한 사건들의 연결", "eraId": "1990s"}
NODES = []


def E(a, b, rel, ver, claims, note=""):
    return {"from": a, "to": b, "rel": rel, "verification": ver, "claimIds": claims, "note": note}


EDGES = [
    E("e60-plan", "e60-plan2", "sequence", "evidenced", ["cfill-plan2"], "제1차 계획(1962~66)에 이은 제2차 계획"),
    E("e60-3term", "d-yushin", "background", "interpretation", ["cfill-3term-yushin"], "3선 개헌이 유신 체제로 가는 길을 열었다는 평가"),
    E("e80-bid", "e80-olympic", "sequence", "evidenced", ["cfill-bid"], "유치 결정 7년 뒤 개최"),
    E("e90-china", "claim:c00-cn-trade", "influence", "interpretation", ["cfill-china", "c00-cn-trade"], "수교 이후 대중 교역이 급증하는 출발점"),
]
