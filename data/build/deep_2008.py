"""2.0 세 번째 심층 사례 — 2008년 글로벌 금융위기와 한국.

1997년과 '닮은 점'(단기외채·환율 급등)과 '다른 점'(외환보유액·통화스와프·재정 대응)을 비교할 수 있게 짠다.
원칙은 deep_1973·deep_1997과 같다(독립 출처 2개 이상일 때만 verified, 근거 없는 연결은 hypothesis).
"""
from era_1960s import C
from era_1980s import S

SOURCES = [
    S("kr-mt-shortdebt-0805", "'단기외채 대책' 발언에 금융시장 요동 (2008.5.21)", "머니투데이", "https://www.mt.co.kr/stock/2008/05/21/2008052119150460656", "news"),
    S("hri-2008-debt", "외채 동향과 시사점 (2008)", "현대경제연구원", "https://test.hri.co.kr/upload/board/20088483610%5b1%5d.pdf", "institution"),
    S("kr-mt-crisis-0811", "한국 위기='금융과 환율 분리'의 비극 (2008.11.4)", "머니투데이", "https://www.mt.co.kr/article/2008110413313571024", "news"),
    S("kmi-2008-crisis", "해운이슈: 글로벌 금융위기와 한국경제 (2008.10)", "한국해양수산개발원 (KoreaScience)", "https://koreascience.kr/article/JAKO200866759248814.pdf", "institution"),
    S("kr-korea-swap-0810", "한·미 300억 달러 통화스와프 체결 (2008.10)", "대한민국 정책브리핑", "https://www.korea.kr/briefing/policyBriefingView.do?newsId=148658723", "government"),
    S("kr-mt-swap-0810", "한은, 미 연준과 300억 달러 통화스와프 (2008.10.30)", "머니투데이", "https://www.mt.co.kr/stock/2008/10/30/2008103009242405699", "news"),
    S("kr-dailian-swap", "한미 통화스와프는 2008년 이후 두 번째 (2020)", "데일리안", "https://m.dailian.co.kr/news/view/877456", "news"),
    S("kr-korea-2009-numbers", "숫자로 본 2009년 (기준금리·환율·슈퍼 추경)", "대한민국 정책브리핑", "https://www.korea.kr/news/policyNewsView.do?newsId=148685908", "government"),
    S("kr-tomato-supplement", "사상 최대 28.9조 슈퍼 추경 편성 (2009.3.24)", "뉴스토마토", "https://newstomato.com/ReadNews.aspx?no=48711", "news"),
    S("kr-mt-supplement", "28.9조 '슈퍼 추경'…경기 '반전포인트' 될까 (2009.3.23)", "머니투데이", "https://www.mt.co.kr/article/2009032315052313611", "news"),
    S("kr-khan-kiko", "환율 급등에 키코 가입 수출 중소기업 손실 (2008.8.26)", "경향신문", "https://www.khan.co.kr/article/200808261805145/amp", "news"),
    S("kr-lawtimes-kiko", "대법원 '키코 계약 유효, 일부 설명의무 위반' (2013)", "법률신문", "https://www.lawtimes.co.kr/news/78717", "news"),
    S("kr-etoday-kiko235", "키코 피해기업 235개 도산 (2017)", "이투데이", "https://www.etoday.co.kr/news/view/1544420", "news"),
    S("kiep-2020-mpm", "대외부문 거시건전성 정책 10년의 성과와 개선방안 (2020)", "대외경제정책연구원 (RePEc)", "https://ideas.repec.org/p/ris/kieppa/2020_018.html", "institution"),
    S("kr-fn-levy-1012", "외환건전성부담금으로 자본유출입 3대 규제 완성 (2010.12.19)", "파이낸셜뉴스", "https://www.fnnews.com/news/201012191908512306", "news"),
]

CLAIMS = [
    C("c08-shortdebt", "한국의 단기외채는 1997년 말 638억 달러에서 2001년 403억 달러로 줄었다가 2006년 1,000억 달러를 넘었고 2007년 말 1,587억 달러가 되었다(한국은행 집계 보도).",
      "statistical", "sourced", ["kr-mt-shortdebt-0805"], ["economy"], ["KR"]),
    C("c08-shortdebt-why", "단기외채가 늘어난 주된 이유로 조선업체 등 수출기업의 선물환 매도(환위험 회피)가 꼽힌다. 은행이 이를 받아주며 해외 단기차입을 늘렸고, 외국계 은행 지점의 재정거래와 해외 인수합병 차입도 더해졌다.",
      "interpretation", "verified", ["kr-mt-shortdebt-0805", "hri-2008-debt"], ["economy", "industry"], ["KR"]),
    C("c08-diff97", "당시 한국은행·금융감독원은 1997년과 달리 경상수지 적자로 단기차입이 급증한 것이 아니고, 외환보유액(2008년 6월 말 2,581억 달러)도 훨씬 많다며 위기 재발 가능성을 낮게 봤다.",
      "interpretation", "verified", ["kr-mt-shortdebt-0805", "hri-2008-debt"], ["economy"], ["KR"]),
    C("c08-outflow", "외국인은 2006~2008년 11월 초까지 한국 주식을 약 77조 원(약 750억 달러) 순매도했고, 경상수지 흑자는 2004년 281억 달러에서 2006~07년 50억 달러대로 줄었다. 2008년 1~8월에는 원자재값 급등으로 경상수지가 125.8억 달러 적자였다.",
      "statistical", "verified", ["kr-mt-crisis-0811", "kmi-2008-crisis"], ["economy"], ["KR", "WORLD"]),
    C("c08-swap", "2008년 10월 30일 한국은행은 미 연준과 300억 달러 통화스와프를 맺었다. 발표 당일 원·달러 환율은 177원 내린 1,250원으로 마감했고 코스피는 115포인트 올랐다. 계약은 두 차례 연장돼 2010년 2월까지 유지되었다.",
      "fact", "verified", ["kr-korea-swap-0810", "kr-mt-swap-0810", "kr-dailian-swap"], ["economy", "politics"], ["KR", "US"]),
    C("c08-rate", "한국은행 기준금리는 리먼 사태 뒤 2008년 10월부터 2009년 2월까지 6차례 인하돼 5.25%에서 2.00%가 되었다. 원·달러 환율은 2009년 2월 말 1,534원까지 올랐다가 미국·일본·중국과의 통화스와프 뒤 안정되었다.",
      "fact", "sourced", ["kr-korea-2009-numbers"], ["economy"], ["KR", "US", "JP", "CN"]),
    C("c08-supplement", "정부는 2009년 3월 사상 최대인 28조 9천억 원 규모의 '슈퍼 추경'을 편성했다(국회 확정 28조 4천억 원). 외환위기 때인 1998년 추경(13조 9천억 원)의 두 배가 넘었고, 일자리 유지·저소득층 생활안정·중소기업 지원에 집중했다.",
      "fact", "verified", ["kr-tomato-supplement", "kr-mt-supplement", "kr-korea-2009-numbers"], ["economy", "politics"], ["KR"]),
    C("c08-kiko", "환율이 계속 내릴 것에 대비해 환헤지 통화옵션 상품 '키코(KIKO)'에 가입한 수출 중소기업들은 2008년 환율이 900원대 후반에서 1,400원대로 치솟자 큰 손실을 입었다. 이후 피해 기업 가운데 235곳이 법정관리에 가거나 폐업한 것으로 집계되었다.",
      "fact", "verified", ["kr-khan-kiko", "kr-lawtimes-kiko", "kr-etoday-kiko235"], ["economy", "industry"], ["KR"]),
    C("c08-jobs-share", "한국노동연구원은 2009년 고용충격이 1998년보다 훨씬 작았던 이유로 위기 강도 차이와 함께 임금조정·일자리 나누기형 구조조정, 기업의 상시적 고용조정 체제, 정부의 고용유지 지원을 든다(실직자 최대: 1998년 180만 명, 2009년 98만 명).",
      "interpretation", "sourced", ["kli-brief-101"], ["society", "economy"], ["KR"]),
    C("c08-mpm", "위기 뒤 한국은 2010년부터 '거시건전성 3종 세트'(은행 선물환포지션 한도, 외국인 채권투자 과세 환원, 2011년 외환건전성부담금)를 도입해 단기외채와 급격한 자본 유출입을 억제했다. 대외경제정책연구원은 이 정책이 외화부채 만기구조를 개선했다고 평가한다.",
      "fact", "verified", ["kiep-2020-mpm", "kr-fn-levy-1012"], ["economy", "politics"], ["KR"]),
]

CHAIN = {"id": "deep-2008", "title": "2008년 글로벌 금융위기와 한국 (선물환·단기외채 → 리먼 → 환율 급등 → 통화스와프·금리·추경 → 거시건전성 규제)", "eraId": "2000s"}


def N(id, label, year, lane, ntype, countries, imp, claims, prec="year"):
    return {"id": id, "label": label, "year": year, "yearPrecision": prec, "lane": lane, "nodeType": ntype,
            "countries": countries, "importance": imp, "claimIds": claims}


NODES = [
    N("d08-subprime", "미국 서브프라임 주택대출 부실 (2007~)", 2007, "economy", "background", ["US"], 2, ["c00-subprime"]),
    N("d08-forward", "조선사 선물환 매도 → 은행 단기 해외차입", 2007, "industry", "mechanism", ["KR"], 2, ["c08-shortdebt-why"]),
    N("d08-shortdebt", "단기외채 다시 급증 (2007년 말 1,587억 달러)", 2007, "economy", "background", ["KR"], 2, ["c08-shortdebt"]),
    N("d08-diff", "1997년과 다른 점: 외환보유액 2,581억 달러", 2008, "economy", "background", ["KR"], 3, ["c08-diff97"]),
    N("d08-outflow", "외국인 주식 매도·경상수지 악화 (2006~08)", 2008, "economy", "background", ["KR", "WORLD"], 2, ["c08-outflow"]),
    N("d08-fx", "환율 1,500원 돌파·코스피 반토막 (2008.11)", 2008, "economy", "outcome", ["KR"], 1, ["c00-kr-2008"]),
    N("d08-kiko", "키코 사태: 수출 중소기업 환손실", 2008, "industry", "outcome", ["KR"], 2, ["c08-kiko"]),
    N("d08-swap", "한·미 300억 달러 통화스와프 (2008.10.30)", 2008, "politics", "event", ["KR", "US"], 1, ["c08-swap"]),
    N("d08-rate", "기준금리 5.25% → 2.00% (2008.10~2009.2)", 2009, "economy", "reaction", ["KR"], 2, ["c08-rate"]),
    N("d08-supplement", "28조 원대 '슈퍼 추경' (2009.3)", 2009, "politics", "reaction", ["KR"], 2, ["c08-supplement"]),
    N("d08-jobs", "일자리 나누기: 1998년보다 작은 고용충격", 2009, "society", "outcome", ["KR"], 2, ["c08-jobs-share"]),
    N("d08-mpm", "거시건전성 3종 세트 (2010~2011)", 2010, "economy", "outcome", ["KR"], 2, ["c08-mpm"]),
]


def E(a, b, rel, ver, claims, note=""):
    return {"from": a, "to": b, "rel": rel, "verification": ver, "claimIds": claims, "note": note}


EDGES = [
    E("d08-subprime", "e00-lehman", "cause", "evidenced", ["c00-subprime", "c00-lehman"], "서브프라임 손실이 대형 투자은행 파산으로 번짐"),
    E("d08-forward", "d08-shortdebt", "cause", "evidenced", ["c08-shortdebt-why", "c08-shortdebt"], "선물환을 받아준 은행의 단기 해외차입이 단기외채를 키움"),
    E("d97-shortdebt", "d08-shortdebt", "similar", "interpretation", ["c97-shortdebt", "c08-shortdebt"], "두 위기 모두 단기외채가 불안의 통로였다는 점에서 닮음"),
    E("d97-reserve", "d08-diff", "influence", "interpretation", ["c97-reserve-build", "c08-diff97"], "1997년 뒤 쌓은 외환보유액이 2008년의 완충장치가 됨"),
    E("e00-lehman", "d08-fx", "trigger", "evidenced", ["c00-lehman", "c00-kr-2008"], "리먼 파산 뒤 세계적 달러 경색 → 원화 급락"),
    E("d08-shortdebt", "d08-fx", "influence", "interpretation", ["c08-shortdebt", "c00-kr-2008"], "단기외채가 많아 달러 유동성 우려가 환율 급등을 키웠다는 해석"),
    E("d08-outflow", "d08-fx", "influence", "evidenced", ["c08-outflow", "c00-kr-2008"], "외국인 자금 이탈과 경상수지 악화로 달러 부족"),
    E("d08-fx", "d08-kiko", "cause", "evidenced", ["c08-kiko"], "환율이 키코 계약 상단을 넘으며 중소기업 손실 확대"),
    E("d08-fx", "d08-swap", "cause", "evidenced", ["c08-swap"], "달러 유동성 위기 우려 속 통화스와프 체결"),
    E("d08-swap", "d08-fx", "influence", "evidenced", ["c08-swap"], "발표 당일 환율 177원 하락(이후 2009년 2월 다시 1,534원까지 오름)"),
    E("e00-lehman", "d08-rate", "cause", "evidenced", ["c08-rate"], "리먼 사태 뒤 6차례 금리 인하"),
    E("d08-rate", "d08-supplement", "sequence", "evidenced", ["c08-rate", "c08-supplement"], "통화 완화에 이어 재정 확대"),
    E("d08-supplement", "d08-jobs", "influence", "interpretation", ["c08-supplement", "c08-jobs-share"], "일자리 유지 예산과 고용유지 지원이 고용충격을 줄인 요인 중 하나(한국노동연구원)"),
    E("d97-unemp", "d08-jobs", "similar", "interpretation", ["c97-unemp-cause", "c08-jobs-share"], "같은 위기라도 1998년은 인원감축, 2009년은 일자리 나누기 중심"),
    E("d08-shortdebt", "d08-mpm", "cause", "evidenced", ["c08-mpm"], "단기외채·자본 유출입 변동성을 억제하려는 규제"),
    E("d08-fx", "d08-mpm", "background", "evidenced", ["c08-mpm"], "통화정책·미시건전성 정책만으로는 대응하기 어렵다는 반성"),
]
