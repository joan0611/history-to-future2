"""출처가 1개뿐이던 사실 주장에 독립 출처를 하나 더 붙여 'verified'로 올린다.

규칙: 두 번째 출처는 첫 출처와 발행처가 달라야 하고, 주장 문장의 핵심(날짜·주체·사건)을
직접 담고 있어야 한다. 문장이 두 번째 출처와 어긋나면 문장을 출처에 맞게 고친다(TEXT_FIX).
"""


def S(id, title, pub, url, stype, note=None):
    d = {"id": id, "title": title, "publisher": pub, "url": url, "sourceType": stype, "accessedDate": "2026-11-11"}
    if note:
        d["note"] = note
    return d


SOURCES = [
    S("kr-etnews-hci-1973", "[과학기술이 미래다] 과학기술처, 5대 전략산업 특정연구기관 지정", "전자신문",
      "https://www.etnews.com/20220713000151", "news", note="1973년 1월 12일 연두 기자회견 서술"),
    S("samsung-semi-40y", "삼성 반도체사업 40년, 도전과 창조의 역사", "삼성전자 반도체 뉴스룸",
      "https://news.samsungsemiconductor.com/kr/삼성-반도체사업-40년-도전과-창조의-역사/", "company",
      note="1983년 12월 1일 국내 최초 64K D램 개발 성공"),
    S("samsung-semi-giheung", "반도체 역사시리즈 6탄: 삼성반도체 45년 사업장의 성장", "삼성전자 반도체 뉴스룸",
      "https://news.samsungsemiconductor.com/kr/%EB%B0%98%EB%8F%84%EC%B2%B4-%EC%97%AD%EC%82%AC%EC%8B%9C%EB%A6%AC%EC%A6%88-6%ED%83%84-%EC%82%BC%EC%84%B1%EB%B0%98%EB%8F%84%EC%B2%B4-45%EB%85%84-%EC%82%AC%EC%97%85%EC%9E%A5%EC%9D%98-%EC%84%B1/",
      "company", note="기흥 라인 1984년 5월 준공, VLSI 양산 시작"),
    S("pressian-1987-labor", "서중석의 현대사 이야기 — 7·8·9월 노동자 대투쟁", "프레시안",
      "https://pressian.com/pages/articles/154486", "news",
      note="1987년 7월 5일 울산 현대엔진 노조 결성이 전국 투쟁을 촉발"),
    S("pressian-2021-labor", "87년 노동자대투쟁 (울산노동역사관 자료)", "프레시안",
      "https://www.pressian.com/pages/articles/2021041119135508343", "news",
      note="1987년 말 노동조합 수가 1년 전보다 50% 증가"),
    S("byline-230113-rate", "한국은행, 기준금리 0.25%p 인상 (2023.1.13)", "바이라인네트워크",
      "https://byline.network/2023/01/13-232/", "news", note="연 3.25% → 3.50%, 2022년 4월 이후 일곱 차례 연속 인상"),
    S("sidae-230411-rate", "한은, 기준금리 2회 연속 3.50% 동결 (2023.4.11)", "머니S",
      "https://www.sidae.com/article/2023041110104448709", "news",
      note="1년 반 동안 10차례 총 3%포인트 인상, 사상 처음 7연속 인상"),
    S("apple-iphone-2007", "Apple Reinvents the Phone with iPhone (2007.1.9)", "Apple Newsroom",
      "https://www.apple.com/newsroom/2007/01/09Apple-Reinvents-the-Phone-with-iPhone/", "company"),
    S("history-chatgpt", "ChatGPT, the generative AI chatbot, is released", "HISTORY (A&E)",
      "https://www.history.com/this-day-in-history/chatgpt-released-openai", "reference"),
    S("chinadaily-3rd-plenum", "Third Plenary Session of 11th Central Committee of CPC held in 1978", "China Daily (People's Daily Online)",
      "https://covid-19.chinadaily.com.cn/bizchina/2008-10/29/content_7169033.htm", "news",
      note="1978년 12월 18~22일 베이징"),
    S("npr-plaza", "Plaza Accord (Planet Money)", "NPR",
      "https://www.npr.org/sections/money/2010/12/17/132142673/plaza-accord", "news"),
    S("cern-www-pd", "CERN puts the World Wide Web in the public domain", "CERN",
      "https://timeline.web.cern.ch/node/794", "institution", note="1993년 4월 30일"),
    S("intel-4004-50", "Intel Marks 50th Anniversary of the 4004", "Intel Newsroom",
      "https://intel.com/content/www/us/en/newsroom/news/intel-marks-50th-anniversary-4004.html", "company"),
    S("guinness-4004", "First microprocessor", "Guinness World Records",
      "https://www.guinnessworldrecords.com/world-records/first-microprocessor", "reference",
      note="1971년 11월 15일 판매 시작"),
    S("frus-iea-1974", "FRUS 1969–76 vol. XXXVII, doc. 20 — Editorial Note", "U.S. Department of State, Office of the Historian",
      "https://history.state.gov/historicaldocuments/frus1969-76v37/d20", "government",
      note="신설 IEA 이사회 첫 회의 1974년 11월 18~19일 파리"),
    S("spectrum-ibmpc", "How the IBM PC Won, Then Lost, the Personal Computer Market", "IEEE Spectrum",
      "https://spectrum.ieee.org/tech-history/silicon-revolution/how-the-ibm-pc-won-then-lost-the-personal-computer-market", "news"),
]

SOURCES += [
    S("ad-lge-hitech", "\"순간의 선택이 10년을 좌우합니다\" — 금성사 광고 카피 이야기", "LG전자 뉴스룸",
      "https://www.lge.co.kr/story/newsroom/172709", "company"),
    S("ad-segye-230502", "2013년 세계 첫 올레드 55형 출시 (금성 하이테크 칼라비전 광고 언급)", "세계일보",
      "https://www.segye.com/newsView/20230502513731", "news", note="제1회 한국방송광고대상 수상 언급"),
    S("ad-samsung-anycall", "애니콜, 새 브랜드 슬로건 'Talk, Play, Love' (역대 슬로건 정리)", "삼성전자 뉴스룸",
      "https://news.samsung.com/kr/%ec%95%a0%eb%8b%88%ec%bd%9c-%ec%83%88-%eb%b8%8c%eb%9e%9c%eb%93%9c-%ec%8a%ac%eb%a1%9c%ea%b1%b4-talk-play-love", "company"),
    S("ad-hk-010625", "[한경 소비자 大賞] 이동전화 — 삼성전자 '애니콜'", "한국경제",
      "https://www.hankyung.com/amp/2001062554441", "news", note="1995년 7월 국내 점유율 1위, 모토로라 추월"),
    S("ad-etnews-080321", "[전자산업 50년] TV국산화와 가전산업의 태동", "전자신문",
      "https://www.etnews.com/200803210022", "news", note="VD-191 출시와 공개 추첨 판매"),
    S("ad-etnews-990603", "가전산업과 TV국산화", "전자신문",
      "https://m.etnews.com/199906030056", "news", note="VD-191 가격 6만 3,510원, 일제·미제와 비교"),
    S("ad-khan-230616-pony", "포니 — 국산화율 90%, 첫해 점유율 43%", "경향신문",
      "https://www.khan.co.kr/article/202306160300045", "news"),
    S("ad-bravo-151209-pony", "40돌 맞은 국내 첫 고유모델 車 '포니'", "브라보마이라이프(이투데이)",
      "https://bravo.etoday.co.kr/view/atc_view/4641", "news"),
    S("hs-economist-211231", "'저금리' vs '공급부족' 집값 폭등 이유 두고 시선 엇갈려", "이코노미스트",
      "https://economist.co.kr/article/view/ecn202112310015", "news", note="국토연구원 기여도 분석·주택산업연구원 분석 소개"),
    S("hs-nocut-210611", "공급 절벽에 매물 잠김까지…뛰고 또 뛰는 집값", "노컷뉴스",
      "https://www.nocutnews.co.kr/news/5568983", "news", note="한국은행 금융안정보고서: 공급 부족·이례적 저금리"),
]

# 가설이던 문장을 확인한 내용으로 바꾼다(확인하지 못한 부분은 문장에 그대로 밝힌다)
REPLACE = {
    "c60-hyp-kr-ad": dict(
        text="금성 VD-191의 광고 원문은 찾지 못했다. 다만 출시 당시 일제(17인치 7만 8천 원)보다 싼 6만 3,510원으로 값을 매겼고, 공급이 모자라 공개 추첨으로 팔았으며, '우리 손으로 TV를 만들었다'는 사실이 큰 자부심을 불러왔다는 기록이 있다.",
        claimType="interpretation", status="sourced", sourceIds=["ad-etnews-080321", "ad-etnews-990603"]),
    "c70-hyp-pony-ad": dict(
        text="포니 광고의 문구는 찾지 못했다. 확인된 것은 국산화율 90%, 1976년 판매 1만 726대·시장 점유율 43%이고, 포니가 '마이카 시대'를 열고 공업화의 상징이 됐다는 평가다.",
        claimType="interpretation", status="verified", sourceIds=["ad-khan-230616-pony", "ad-bravo-151209-pony"]),
    "c80-hyp-ad": dict(
        text="1980년대 초 금성 '하이테크 칼라비전' TV 광고의 카피는 '순간의 선택이 10년을 좌우합니다'였다. 컬러TV를 10년을 쓸 큰 결정으로 내세운 이 카피는 제1회 한국방송광고대상을 받았다.",
        claimType="fact", status="verified", sourceIds=["ad-lge-hitech", "ad-segye-230502"]),
    "c90-hyp-ad": dict(
        text="삼성 애니콜의 첫 브랜드 슬로건은 '한국 지형에 강하다'(1995~98)였다. 외국산 휴대전화보다 한국 산지 지형에서 잘 터진다는 점을 내세웠고, 애니콜은 1995년 7월 모토로라를 제치고 국내 점유율 1위가 되었다. 1990년대 광고가 '세계화된 개인'을 내세웠으리라던 이전 가설과 달리, 확인된 광고는 '국산이 한국에 맞는다'를 강조했다.",
        claimType="fact", status="verified", sourceIds=["ad-samsung-anycall", "ad-hk-010625"]),
    "c10-hyp-asset": dict(
        text="2017~2021년 집값 급등의 원인을 두고 국토연구원은 금리의 기여도가 가장 컸다고 분석했고(2017.5~2021.5, 샤플리 분해), 주택산업연구원은 공급 부족을 가장 큰 요인으로 꼽았다. 한국은행은 공급 부족과 이례적 저금리를 함께 들었다. 어느 한 요인으로 단정하기 어렵다는 평가도 있다.",
        claimType="interpretation", status="sourced", sourceIds=["hs-economist-211231", "hs-nocut-210611"]),
}

# 주장 id → 추가 출처 id
ADD = {
    "c70-kr-hci": ["kr-etnews-hci-1973"],
    "c80-64k": ["samsung-semi-40y", "samsung-semi-giheung"],
    "c80-labor": ["pressian-1987-labor"],
    "c20-kr-rate": ["byline-230113-rate", "sidae-230411-rate"],
    "c00-iphone": ["apple-iphone-2007"],
    "c20-chatgpt": ["history-chatgpt"],
    "c80-cn-reform": ["chinadaily-3rd-plenum"],
    "c80-plaza": ["npr-plaza"],
    "c90-www": ["cern-www-pd"],
    "c70-4004": ["intel-4004-50", "guinness-4004"],
    "c70-iea": ["frus-iea-1974"],
    "c80-ibmpc": ["spectrum-ibmpc"],
}

# 두 번째 출처와 맞춰 고친 문장
TEXT_FIX = {
    # 전자신문 단독 '11월' → 삼성 자료는 12월 1일 개발 성공 발표, 기흥 라인 준공 1984년 5월
    "c80-64k": "삼성반도체통신은 1983년 64K D램 개발에 성공했다(12월 1일 발표). 미국·일본에 이은 세계 세 번째로, 1984년 5월 기흥 공장을 준공해 VLSI 양산을 시작했다.",
    # '400여 개'는 주간경향 단독 수치 → 별도 주장(c80-labor-unions)으로 분리
    "c80-labor": "6·29선언 이후 1987년 7월 5일 울산 현대엔진 노조 결성을 시작으로 노동자 대투쟁이 전국 공단으로 번졌다.",
    "c00-iphone": "애플은 2007년 1월 9일 맥월드에서 아이폰을 발표했다.",
    "c80-cn-reform": "중국은 1978년 12월 18~22일 공산당 11기 3중전회를 계기로 개혁·개방 정책을 시작했다.",
    "c90-www": "CERN은 1993년 4월 30일 월드와이드웹 소프트웨어를 공개 영역(퍼블릭 도메인)으로 풀었다.",
    "c70-4004": "인텔은 1971년 11월 15일 최초의 상용 마이크로프로세서 4004를 발표했다.",
}


def _C(id, text, ctype, status, sources, domains, countries):
    return {"id": id, "text": text, "claimType": ctype, "status": status, "sourceIds": sources,
            "domains": domains, "countries": countries, "aiSynthesized": False}


CLAIMS = [
    _C("c80-labor-unions",
       "대투쟁은 이후 4개월 동안 400여 개의 민주노조를 낳았고(주간경향), 1987년 말 노동조합 수는 1년 전보다 50% 늘었다(프레시안).",
       "statistical", "sourced", ["kr-khan-1987labor", "pressian-2021-labor"], ["labor"], ["KR"]),
]


def apply(claims):
    """claims 목록을 제자리에서 고친다. 바뀐 주장 수를 돌려준다."""
    by = {c["id"]: c for c in claims}
    for cid, r in REPLACE.items():
        if cid not in by:
            raise KeyError(f"corroborate: 없는 주장 {cid}")
        by[cid].update(r)
    n = 0
    for cid, extra in ADD.items():
        c = by.get(cid)
        if c is None:
            raise KeyError(f"corroborate: 없는 주장 {cid}")
        for s in extra:
            if s not in c["sourceIds"]:
                c["sourceIds"].append(s)
        if cid in TEXT_FIX:
            c["text"] = TEXT_FIX[cid]
        if c["status"] == "sourced" and len(c["sourceIds"]) >= 2:
            c["status"] = "verified"
            n += 1
    return n


# 같은 원자료를 옮긴 기존 출처(발행처가 달라도 한 곳으로 센다)
ORIGIN = {
    "jj-230113-rate": "한국은행 금융통화위원회 발표",
    "byline-230113-rate": "한국은행 금융통화위원회 발표",
    "sidae-230411-rate": "한국은행 금융통화위원회 발표",
    "nd-210203-online": "통계청 온라인쇼핑 동향",
    "sg-210405-online": "통계청 온라인쇼핑 동향",
}
