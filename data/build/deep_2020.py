"""2.0 네 번째 심층 사례 — 코로나19와 한국 (2020~2022): 감염 확산 → 방역·경제 대응 → 생활·소비 변화 → 집값·금리.

원칙은 앞의 심층 사례와 같다. 기존 2020년대 노드(e20-covid, tr-t20-untact, e20-rate, tr-t20-home, e20-kcpi, e20-war)와 잇는다.
"""
from era_1960s import C
from era_1980s import S

SOURCES = [
    S("kr-newsis-covid3y", "[코로나 3년] 확진자 첫 발생부터 실내마스크 완화까지 (2023.1.19)", "뉴시스", "https://www.newsis.com/view/NISX20230119_0002165072", "news"),
    S("kr-korea-covid-2020", "2020년 코로나19 1년 정리 — 31번째 환자 이후 대구·경북 급증", "대한민국 정책브리핑", "https://www.korea.kr/news/policyNewsView.do?newsId=148881350", "government"),
    S("kr-seoul-bigcut", "美 이어 한은도 '빅컷'… 첫 0%대 금리 (2020.3.17)", "서울신문", "https://m.seoul.co.kr/news/2020/03/17/20200317001026", "news"),
    S("kr-newsis-bigcut", "한은, 기준금리 0.75%로 인하…'미지의 길' 간다 (2020.3.16)", "뉴시스", "https://www.newsis.com/view/NISX20200316_0000957725", "news"),
    S("kr-kbmaeil-0528", "한은, 기준금리 0.25%p 인하…0.5%로 역대 최저 (2020.5.28)", "경북매일", "https://kbmaeil.com/article/202005280279610", "news"),
    S("kr-newsis-swap2020", "한·미 600억달러 통화스와프 체결…10년만에 재개 (2020.3.19)", "뉴시스", "https://www.newsis.com/view/NISX20200319_0000962921", "news"),
    S("kr-dailian-swap2020", "한미 통화스왑은 2008년 이후 두 번째 (2020.3.19)", "데일리안", "https://m.dailian.co.kr/news/view/877456", "news"),
    S("kr-kbmaeil-relief", "전국민 긴급재난지원금 5월 13일부터 지급… 총 14조 3천억 원 (2020.4.30)", "경북매일", "https://kbmaeil.com/article/202004300277560", "news"),
    S("kr-seoulmedia-relief", "전 국민 '긴급재난지원금' 이렇게 신청하세요 (2020.5.12)", "서울시 내 손안에 서울", "https://mediahub.seoul.go.kr/archives/1280379", "government"),
    S("kr-bizwatch-hike", "한은 기준금리 0.75%로 인상 — 가계부채·집값 위험 (2021.8.26)", "비즈워치", "https://news.bizwatch.co.kr/article/finance/2021/08/26/0007", "news"),
    S("kr-tomato-hike", "2년 9개월 만에 긴축 선회 — '금융불균형'이 더 심각 판단 (2021.8.26)", "뉴스토마토", "https://newstomato.com/ReadNews.aspx?no=1069502", "news"),
    S("kr-seoulmedia-endsd", "18일부터 사회적 거리두기 전면 해제…마스크 유지 (2022.4.15)", "서울시 내 손안에 서울", "https://mediahub.seoul.go.kr/archives/2004303", "government"),
    S("kr-seoul-endsd", "들뜬 자영업자들 '매출 벌써 올라요' — 757일 만에 해제 (2022.4.18)", "서울신문", "https://m.seoul.co.kr/news/2022/04/18/20220418001012", "news"),
]

CLAIMS = [
    C("c2020-first", "국내 첫 코로나19 확진자는 2020년 1월 20일 인천공항 검역 단계에서 확인되었다(중국 우한에서 입국한 여성). 한 달 동안 30명 안팎이던 확진자는 2월 18일 대구의 31번째 환자 이후 급증해, 한 달 만에 대구·경북 누적 확진자가 약 8,000명이 되었다.",
      "fact", "verified", ["kr-newsis-covid3y", "kr-korea-covid-2020"], ["society", "politics"], ["KR", "CN"]),
    C("c2020-bigcut", "한국은행은 2020년 3월 16일 임시 금융통화위원회를 열어 기준금리를 1.25%에서 0.75%로 0.5%포인트 내렸다(사상 첫 0%대). 전날 미국 연준이 제로금리로 돌아간 직후였고, 5월 28일 다시 0.5%로 내렸다.",
      "fact", "verified", ["kr-seoul-bigcut", "kr-newsis-bigcut", "kr-kbmaeil-0528"], ["economy"], ["KR", "US"]),
    C("c2020-swap", "2020년 3월 19일 한국은행은 미 연준과 600억 달러 통화스와프를 맺었다. 2008년(300억 달러) 이후 두 번째로, 달러 자금시장 경색과 환율 급등(이날 1,285.7원)에 대응한 것이다.",
      "fact", "verified", ["kr-newsis-swap2020", "kr-dailian-swap2020"], ["economy", "politics"], ["KR", "US"]),
    C("c2020-relief", "정부는 2020년 5월 모든 가구에 긴급재난지원금(1인 가구 40만 원~4인 이상 가구 100만 원)을 지급했다. 국비 12조 2천억 원과 지방비 2조 1천억 원을 합쳐 14조 3천억 원 규모였다.",
      "fact", "verified", ["kr-kbmaeil-relief", "kr-seoulmedia-relief"], ["politics", "society"], ["KR"]),
    C("c2020-hike", "한국은행은 2021년 8월 26일 기준금리를 0.5%에서 0.75%로 올려 2년 9개월 만에 긴축으로 돌아섰다. 코로나 확산보다 가계부채 급증과 집값 상승(금융불균형)을 더 큰 위험으로 본 결정으로 해석되었다.",
      "fact", "verified", ["kr-bizwatch-hike", "kr-tomato-hike"], ["economy"], ["KR"]),
    C("c2020-endsd", "사회적 거리두기는 2022년 4월 18일 2년 1개월(757일) 만에 전면 해제되었다. 영업시간·사적모임 인원 제한이 사라졌고, 오미크론 유행이 3월 셋째 주를 정점으로 줄어든 것이 배경이었다.",
      "fact", "verified", ["kr-seoulmedia-endsd", "kr-seoul-endsd"], ["society", "politics"], ["KR"]),
    C("c2020-spend", "한국은행 국민계정으로 계산하면 가계 소비 가운데 오락·스포츠·문화의 몫은 2019년 7.54%에서 2020년 6.16%로, 의류·신발은 6.08%에서 5.15%로 줄었다. 반대로 식료품 몫은 11.53%에서 12.95%로 늘었다.",
      "statistical", "sourced", ["ecos-hhcons"], ["society", "culture"], ["KR"]),
    C("c2020-gdp", "한국은행 실질 GDP로 계산한 2020년 성장률은 -0.7%로, 1998년(-4.9%) 이후 처음 마이너스였다. 2021년에는 4.7%로 반등했다.",
      "statistical", "sourced", ["ecos-rgdp"], ["economy"], ["KR"]),
]

CHAIN = {"id": "deep-2020", "title": "코로나19와 한국 (2020~2022: 감염 확산 → 금리·재정 대응 → 생활·소비 변화 → 집값·금리 인상)", "eraId": "2020s"}


def N(id, label, year, lane, ntype, countries, imp, claims, prec="year"):
    return {"id": id, "label": label, "year": year, "yearPrecision": prec, "lane": lane, "nodeType": ntype,
            "countries": countries, "importance": imp, "claimIds": claims}


NODES = [
    N("d20-spread", "대구 집단감염과 1차 대유행 (2020.2~3)", 2020, "society", "trigger", ["KR"], 1, ["c2020-first"]),
    N("d20-bigcut", "기준금리 '빅컷' 1.25% → 0.5% (2020.3~5)", 2020, "economy", "reaction", ["KR", "US"], 1, ["c2020-bigcut"]),
    N("d20-swap", "한·미 600억 달러 통화스와프 (2020.3.19)", 2020, "politics", "event", ["KR", "US"], 2, ["c2020-swap"]),
    N("d20-relief", "전 국민 긴급재난지원금 14조 3천억 원 (2020.5)", 2020, "politics", "reaction", ["KR"], 2, ["c2020-relief"]),
    N("d20-gdp", "1998년 이후 첫 역성장 (2020년 -0.7%)", 2020, "economy", "outcome", ["KR"], 2, ["c2020-gdp"]),
    N("d20-spend", "소비의 이동: 문화·의류 ↓, 식료품 ↑", 2020, "society", "outcome", ["KR"], 2, ["c2020-spend"]),
    N("d20-hike", "금리 인상 전환 (2021.8) — 가계부채·집값", 2021, "economy", "reaction", ["KR"], 2, ["c2020-hike"]),
    N("d20-endsd", "사회적 거리두기 전면 해제 (2022.4.18)", 2022, "society", "event", ["KR"], 2, ["c2020-endsd"]),
]


def E(a, b, rel, ver, claims, note=""):
    return {"from": a, "to": b, "rel": rel, "verification": ver, "claimIds": claims, "note": note}


EDGES = [
    E("e20-covid", "d20-spread", "sequence", "evidenced", ["c2020-first"], "첫 확진 한 달 뒤 대구에서 급증"),
    E("d20-spread", "d20-bigcut", "cause", "evidenced", ["c2020-bigcut"], "감염 확산에 따른 경제 충격에 대응한 임시 금리 인하"),
    E("d20-spread", "d20-swap", "cause", "evidenced", ["c2020-swap"], "세계적 달러 경색과 환율 급등"),
    E("d08-swap", "d20-swap", "similar", "evidenced", ["c08-swap", "c2020-swap"], "2008년 통화스와프의 경험을 같은 방식으로 다시 씀(규모는 두 배)"),
    E("d20-spread", "d20-relief", "cause", "evidenced", ["c2020-relief"], "생계 충격에 대한 재정 대응"),
    E("d20-spread", "d20-gdp", "cause", "interpretation", ["c2020-gdp"], "방역에 따른 활동 위축이 역성장으로 이어졌다는 일반적 해석(성장률 분해는 아직 하지 않음)"),
    E("d20-spread", "d20-spend", "influence", "interpretation", ["c2020-spend"], "모임·공연·외출이 줄며 소비 구성이 바뀜(항목별 비중 변화는 통계, 원인은 해석)"),
    E("d20-spread", "tr-t20-untact", "cause", "evidenced", ["c20-covid-kr", "c20-online"], "온라인 수업·온라인쇼핑 급증"),
    E("d20-bigcut", "tr-t20-home", "influence", "interpretation", ["c2020-bigcut", "c20-house"], "초저금리가 2020~21년 집값 급등을 키웠다는 해석(지역별 대출 자료와의 연결은 아직 없음)"),
    E("tr-t20-home", "d20-hike", "cause", "evidenced", ["c2020-hike"], "가계부채·집값 위험을 이유로 금리 인상 시작"),
    E("d20-hike", "e20-rate", "sequence", "evidenced", ["c2020-hike", "c20-kr-rate"], "2022~23년 연속 인상으로 이어짐(물가 급등도 겹침)"),
    E("e20-kcpi", "e20-rate", "cause", "evidenced", ["c20-kr-cpi", "c20-kr-rate"], "물가 급등이 빠른 금리 인상의 배경"),
    E("d20-spread", "d20-endsd", "sequence", "evidenced", ["c2020-endsd"], "2년 1개월 뒤 거리두기 해제"),
]
