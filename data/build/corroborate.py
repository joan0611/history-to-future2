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
