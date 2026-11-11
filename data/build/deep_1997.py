"""2.0 두 번째 심층 사례 — 1997년 외환위기 (원인 → 전개 → 대응 → 장기 결과).

원칙은 deep_1973과 같다.
- 문장은 모두 출처와 연결, 독립 출처 2개 이상일 때만 verified.
- 위기의 '원인'을 하나로 단정하지 않는다: 유동성 위기 해석과 구조적 취약성 해석을 각각 노드로 둔다.
- 앞뒤 순서만 있는 연결은 sequence, 정량 근거가 없는 연결은 hypothesis로 둔다.
"""
from era_1960s import C
from era_1980s import S

SOURCES = [
    S("kr-bizhk-hanbo", "한보그룹, 무리한 대출과 1997년 1월 부도", "비즈한국", "https://bizhankook.com/articles/20442.html", "news"),
    S("kr-insight-1997firms", "IMF 당시 무너진 한국 기업 6곳 (한보·기아·해태 등)", "인사이트", "https://www.insight.co.kr/news/197667", "news"),
    S("kr-econ-kia", "외환위기 다시 보기 — 기아 사태 100일 (2017)", "이코노미스트", "https://economist.co.kr/article/view/ecn201702050005", "news"),
    S("kdev-crisis", "Korea's Financial Crises and Economic Restructuring", "K-Developedia (KDI 국제정책대학원)",
      "https://kdevelopedia.org/k-db-originals/koreas-financial-crises-and-economic-restructuring", "institution"),
    S("core-kr-crisis", "Korea's External Debts, Usable Gross Reserves, and Debt-Equity Ratios (표 1, 한국은행 자료 인용 논문)", "CORE 공개 논문 저장소",
      "https://core.ac.uk/download/51178948.pdf", "academic", "표 1 원자료: 한국은행(1998, 2003), Chopra et al.(2001), 재정경제부"),
    S("scribd-kr-crisis", "Korea's 1997 Financial Crisis (학술지 논문 사본, 353쪽)", "Scribd 게시 학술 논문",
      "https://www.scribd.com/document/515445472/Article-05", "academic", "학술지 원문의 사본. 경상수지 적자 비율을 4.7%로 적어 K-Developedia(4.0%)와 다름"),
    S("nd-kellogg-kr", "The 1997 Financial Crisis and Governance: The Case of South Korea (Kwan S. Kim, WP #272, 2000)", "University of Notre Dame Kellogg Institute",
      "https://kellogg.nd.edu/publications/workingpapers/WPS/272.pdf", "academic"),
    S("dallasfed-2001", "Economic and Financial Review 2001 Q4 — Korea's crisis and recovery", "Federal Reserve Bank of Dallas",
      "https://www.dallasfed.org/~/media/documents/research/efr/2001/efr0104c.pdf", "institution"),
    S("nber-korea", "The Korean Currency Crisis (NBER 회의 보고)", "National Bureau of Economic Research",
      "https://www.nber.org/crisis/korea_report.html", "academic"),
    S("kr-seoul-2001-sympo", "IMF 졸업 심포지엄: '외환보유고 고갈이 아니라 구조적 모순' (2001.8.24)", "서울신문",
      "https://www.seoul.co.kr/news/2001/08/24/20010824009001", "news"),
    S("kr-block-mou", "실록 한국경제 — 1997년 12월 3일 IMF 정책이행각서 서명", "블록미디어", "https://www.blockmedia.co.kr/archives/194644", "news"),
    S("kr-seoul-2001-4y", "IMF 4년 현주소 (2001.12.3)", "서울신문", "https://m.seoul.co.kr/news/2001/12/03/20011203006002", "news"),
    S("kr-newsis-2022-imf", "외환위기 25년 — 외환보유액·환율 (2022.12.29)", "뉴시스", "https://www.newsis.com/view/NISX20221229_0002141045", "news"),
    S("kr-arch-tripartite", "노사정위원회 출범 — 정책 해설", "국가기록원", "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=220", "government"),
    S("kr-khan-2016-tripartite", "사회적 대타협의 역사 (2016.5.28)", "경향신문", "https://www.khan.co.kr/article/201605281845021/amp", "news"),
    S("kr-seoul-2017-pact", "'사회적 대화' 돌파구 없나 — 1998년 사회협약 (2017.10.24)", "서울신문", "https://m.seoul.co.kr/news/2017/10/24/20171024009001", "news"),
    S("kr-seoul-1998-dispatch", "파견업 7월 시행… 기업 정규직 줄여 인건비 절감 (1998.2.12)", "서울신문", "https://www.seoul.co.kr/news/1998/02/12/19980212006002", "news"),
    S("kli-brief-101", "고용·노동브리프 제101호 — 1998년·2009년 경제위기와 고용", "한국노동연구원",
      "https://repository.kli.re.kr/bitstream/2021.oak/7122/2/KLI%20%ea%b3%a0%ec%9a%a9%eb%85%b8%eb%8f%99%eb%b8%8c%eb%a6%ac%ed%94%84%20%ec%a0%9c101%ed%98%b8%282020-08%29.pdf", "institution"),
    S("kr-arch-imf-theme", "기록으로 보는 대한민국: IMF 외환위기", "국가기록원", "https://theme.archives.go.kr/next/koreaOfRecord/imf.do", "government"),
    S("kr-aks-imf", "IMF 관리체제", "한국학중앙연구원 디지털인문학 위키", "https://dh.aks.ac.kr/Edu/wiki/index.php/IMF_관리체제", "reference"),
    S("imf-nb-0182", "IMF Managing Director Congratulates Korea on Early Repayment of 1997 Stand-By Credit (2001.8.22)", "IMF",
      "https://www.imf.org/external/np/sec/nb/2001/nb0182.htm", "institution"),
]

CLAIMS = [
    # ── 구조적 배경 ──
    C("c97-ca", "1996년 한국의 경상수지 적자는 약 230억 달러로 1995년(85억 달러)의 세 배 가까이로 커졌다. GDP 대비 비율은 자료에 따라 4.0~4.7%로 적혀 있다.",
      "statistical", "verified", ["kdev-crisis", "scribd-kr-crisis"], ["economy"], ["KR"]),
    C("c97-shortdebt", "단기 대외채무는 1996년 말 759억 달러로 가용 외환보유액 294억 달러의 2.5배를 넘었다(K-Developedia는 280%로 정리). 1997년 말에는 단기외채 638억 달러에 가용 보유액이 91억 달러뿐이었다.",
      "statistical", "verified", ["core-kr-crisis", "kdev-crisis"], ["economy"], ["KR"]),
    C("c97-leverage", "제조업 평균 부채비율은 1996년 317%, 1997년 396%였고, 30대 재벌의 평균 부채비율은 1996년 말 400~500%로 국제 기준(약 200%)의 두 배를 넘었다.",
      "statistical", "verified", ["core-kr-crisis", "nd-kellogg-kr", "dallasfed-2001"], ["economy", "industry"], ["KR"]),
    C("c97-mismatch", "1994~96년 종합금융회사가 6곳에서 30곳으로 늘었고, 상당수가 재벌 소유였다. 이들은 값싼 단기 해외자금(주로 일본)을 빌려 장기 투자에 빌려주어, 빌린 돈과 빌려준 돈의 만기가 크게 어긋났다.",
      "interpretation", "verified", ["core-kr-crisis", "dallasfed-2001"], ["economy"], ["KR", "JP"]),
    C("c97-chaebol-root", "재벌의 높은 부채 의존은 1970년대 후반에 이미 흔했다는 분석이 있다. 정책금융으로 중화학공업을 키운 방식이 빚에 기댄 확장 구조를 남겼다는 해석이다.",
      "interpretation", "sourced", ["nd-kellogg-kr"], ["economy", "industry"], ["KR"]),
    # ── 촉발 ──
    C("c97-hanbo", "재계 14위 한보그룹은 당진제철소 건설에 5조 원이 넘는 대출을 끌어 쓰다 1997년 1월 23일 최종 부도 처리되었다. 은행 대출 과정에서 정경유착이 드러났다.",
      "fact", "verified", ["kr-bizhk-hanbo", "kr-insight-1997firms"], ["economy", "politics"], ["KR"]),
    C("c97-kia", "재계 8위 기아그룹은 1997년 7월 15일 부도유예협약 대상이 되었고, 약 100일 뒤인 10월 22일 법정관리로 결론이 났다.",
      "fact", "verified", ["kr-econ-kia", "kr-insight-1997firms"], ["economy"], ["KR"]),
    C("c97-kia-delay", "한보·기아 사태 대응이 늦어 대외 신인도 추락을 재촉했다는 평가가 있다. 대선을 앞두고 정치권이 기아 회생을 약속한 것도 결정을 늦춘 요인으로 거론된다.",
      "interpretation", "sourced", ["kr-econ-kia"], ["economy", "politics"], ["KR"]),
    # ── 전개 ──
    C("c97-rollover", "위기의 핵심은 외국 은행들이 한국 금융기관의 단기외채 만기 연장을 거부한 데 있었다. 외환보유액이 단기외채에 비해 턱없이 적어 갚을 수 없었고, 원화가 급락했다.",
      "interpretation", "verified", ["nber-korea", "dallasfed-2001"], ["economy"], ["KR", "US", "JP"]),
    C("c97-fx", "1997년 7월 336억 달러였던 외환보유액은 12월 말 204억 달러로 줄었고, 11월까지 900원대였던 원·달러 환율은 12월 23일 1,962원까지 치솟았다.",
      "statistical", "sourced", ["kr-newsis-2022-imf"], ["economy"], ["KR"]),
    C("c97-mou", "1997년 12월 3일 정부와 한국은행은 IMF 총재가 지켜보는 가운데 구제금융 정책이행각서에 서명했다. 이날이 'IMF 체제'의 시작으로 기록된다.",
      "fact", "verified", ["kr-block-mou", "kr-seoul-2001-4y"], ["economy", "politics"], ["KR", "WORLD"]),
    # ── 원인에 대한 두 해석 ──
    C("c97-view-liquidity", "NBER 회의에서 여러 경제학자는 한국 위기의 본질을 '유동성 위기'로 보았다. 기업 부채 등 약점이 있었더라도 외환보유액이 단기외채보다 충분했다면 위기가 이 정도로 커졌을지 묻는 문제 제기가 나왔다.",
      "interpretation", "sourced", ["nber-korea"], ["economy"], ["KR"]),
    C("c97-view-structure", "반대로 IMF 졸업 시점의 국내 심포지엄에서는 구제금융을 부른 것이 외환보유고 고갈이 아니라 경제의 구조적 모순(부실 금융·기업 지배구조)이라는 지적이 나왔다. NBER 회의에서도 취약한 금융 부문과 기업 지배구조가 전염에 취약하게 만들었다는 견해가 있었다.",
      "interpretation", "verified", ["kr-seoul-2001-sympo", "nber-korea"], ["economy"], ["KR"]),
    # ── 대응과 사회 변화 ──
    C("c97-tripartite", "1998년 1월 15일 노사정위원회가 출범했고, 2월 '경제위기 극복을 위한 사회협약'에서 노동계는 정리해고제와 근로자파견제를 받아들이는 대신 노조의 정치활동 허용·전교조 합법화 등을 얻었다.",
      "fact", "verified", ["kr-arch-tripartite", "kr-khan-2016-tripartite", "kr-seoul-2017-pact"], ["politics", "society"], ["KR"]),
    C("c97-dispatch", "정리해고제와 파견근로제는 합의 직후 법제화되었고 파견업은 1998년 7월 시행되었다. 당시 한국노동연구원 부원장은 기업들이 정규직 비중을 낮추면서 인력 효율을 높일 수 있게 되었다고 평가했다.",
      "fact", "sourced", ["kr-seoul-1998-dispatch", "kr-seoul-2017-pact"], ["society", "economy"], ["KR"]),
    C("c97-unemp-cause", "한국노동연구원은 1998년 고용위기가 IMF의 고금리 긴축과 강한 구조조정 요구, 부도 기업 속출, 정리해고제 도입에 따른 인원감축 중심 구조조정으로 실업대란이 된 것이라고 정리한다. 실직자는 최대 180만 명이었다.",
      "interpretation", "sourced", ["kli-brief-101"], ["society", "economy"], ["KR"]),
    C("c97-safety", "정부는 1998~2001년 실업대책에 20조 원을 투입하고, 고용보험·산재보험을 1인 이상 사업장으로, 국민연금을 1999년 도시 자영업자까지 넓혔다.",
      "fact", "sourced", ["kr-gold-briefing-proxy"], ["society", "politics"], ["KR"]),
    # ── 장기 결과 ──
    C("c97-repay", "한국은 2001년 8월 23일 IMF 차입금 195억 달러를 예정(2004년 5월)보다 약 3년 앞당겨 모두 갚고 IMF 관리체제를 벗어났다.",
      "fact", "verified", ["kr-arch-imf-theme", "kr-aks-imf", "imf-nb-0182"], ["economy"], ["KR", "WORLD"]),
    C("c97-reserve-build", "외환보유액은 1998년 말 520억 달러, 2001년 말 1,028억 달러, 2005년 2월 2,000억 달러를 넘었다. 위기 뒤 외환보유액을 위기 완충장치로 꾸준히 늘렸다.",
      "statistical", "verified", ["kr-aks-imf", "kr-newsis-2022-imf"], ["economy"], ["KR"]),
]
# korea.kr 정책브리핑(이미 era_1990s의 kr-korea-gold로 등록된 같은 페이지)을 쓴다
for _c in CLAIMS:
    _c["sourceIds"] = ["kr-korea-gold" if s == "kr-gold-briefing-proxy" else s for s in _c["sourceIds"]]

CHAIN = {"id": "deep-1997", "title": "1997년 외환위기 심층 사례 (단기외채·재벌 부채 → 만기연장 거부 → IMF → 노동시장·외환보유액)", "eraId": "1990s"}


def N(id, label, year, lane, ntype, countries, imp, claims, prec="year"):
    return {"id": id, "label": label, "year": year, "yearPrecision": prec, "lane": lane, "nodeType": ntype,
            "countries": countries, "importance": imp, "claimIds": claims}


NODES = [
    N("d97-chaebol-root", "정책금융으로 커진 재벌의 빚 의존 구조", 1978, "industry", "background", ["KR"], 3, ["c97-chaebol-root"], prec="era"),
    N("d97-ca", "경상수지 적자 확대 (1996년 약 230억 달러)", 1996, "economy", "background", ["KR"], 2, ["c97-ca"]),
    N("d97-leverage", "재벌·제조업의 높은 부채비율 (400~500%)", 1996, "industry", "background", ["KR"], 2, ["c97-leverage"]),
    N("d97-mismatch", "종금사 급증: 단기로 빌려 장기로 빌려줌", 1996, "economy", "mechanism", ["KR", "JP"], 2, ["c97-mismatch"]),
    N("d97-shortdebt", "단기외채가 외환보유액의 2.5배 이상", 1996, "economy", "background", ["KR"], 1, ["c97-shortdebt"]),
    N("d97-hanbo", "한보 부도 (1997.1.23)", 1997, "economy", "trigger", ["KR"], 2, ["c97-hanbo"]),
    N("d97-kia", "기아 부도유예·법정관리 (1997.7~10)", 1997, "economy", "trigger", ["KR"], 2, ["c97-kia", "c97-kia-delay"]),
    N("d97-rollover", "외국 은행의 만기연장 거부 → 외화 고갈", 1997, "economy", "mechanism", ["KR", "US", "JP"], 1, ["c97-rollover"]),
    N("d97-fx", "환율 1,962원·외환보유액 급감 (1997.12)", 1997, "economy", "outcome", ["KR"], 1, ["c97-fx"]),
    N("d97-mou", "IMF 정책이행각서 서명 (1997.12.3)", 1997, "politics", "event", ["KR", "WORLD"], 1, ["c97-mou"]),
    N("d97-view-liq", "해석 ①: 유동성 위기 — 외화가 모자라 생긴 위기", 1997, "economy", "background", ["KR"], 3, ["c97-view-liquidity"]),
    N("d97-view-str", "해석 ②: 구조적 위기 — 부실 금융·기업 지배구조", 1997, "economy", "background", ["KR"], 3, ["c97-view-structure"]),
    N("d97-unemp", "실업대란 (1998, 실직자 최대 180만)", 1998, "society", "outcome", ["KR"], 1, ["c97-unemp-cause", "c90-unemp"]),
    N("d97-tripartite", "노사정 사회협약: 정리해고·파견 수용 (1998.2)", 1998, "politics", "change", ["KR"], 1, ["c97-tripartite"]),
    N("d97-dispatch", "파견근로 합법화 → 정규직 비중 축소 압력", 1998, "society", "change", ["KR"], 2, ["c97-dispatch"]),
    N("d97-safety", "사회안전망 확대 (고용보험·국민연금)", 1999, "society", "change", ["KR"], 2, ["c97-safety"]),
    N("d97-repay", "IMF 차입금 조기 상환 (2001.8.23)", 2001, "economy", "outcome", ["KR", "WORLD"], 2, ["c97-repay"]),
    N("d97-reserve", "외환보유액 확충 (2001년 1,000억 → 2005년 2,000억 달러)", 2001, "economy", "outcome", ["KR"], 2, ["c97-reserve-build"]),
]


def E(a, b, rel, ver, claims, note=""):
    return {"from": a, "to": b, "rel": rel, "verification": ver, "claimIds": claims, "note": note}


EDGES = [
    # 뿌리: 1970년대 정책금융 → 재벌 부채
    E("d-hci-fund", "d97-chaebol-root", "background", "interpretation", ["c70-hci-fund", "c97-chaebol-root"], "정책금융으로 중화학공업에 빚을 몰아준 방식이 빚에 기댄 확장의 출발점이라는 해석"),
    E("d97-chaebol-root", "d97-leverage", "background", "interpretation", ["c97-chaebol-root", "c97-leverage"], "1970년대 후반부터 이어진 높은 부채 의존"),
    # 개방·자유화 → 단기차입
    E("e90-oecd", "d97-mismatch", "background", "interpretation", ["c90-why-open", "c97-mismatch"], "OECD 가입을 위한 금융 개방 속에서 단기 외화차입이 늘어남"),
    E("d97-ca", "d97-shortdebt", "influence", "evidenced", ["c97-ca", "c97-shortdebt"], "경상수지 적자를 주로 외국 자본 유입으로 메워 외채가 늘어남"),
    E("d97-mismatch", "d97-shortdebt", "cause", "evidenced", ["c97-mismatch", "c97-shortdebt"], "금융기관의 단기 해외차입이 단기외채를 키움"),
    E("d97-leverage", "d97-hanbo", "background", "interpretation", ["c97-leverage", "c97-hanbo"], "빚으로 확장한 대기업이 금리·수익 악화를 견디지 못함"),
    E("d97-leverage", "d97-kia", "background", "interpretation", ["c97-leverage", "c97-kia"]),
    # 촉발과 전개
    E("d97-hanbo", "d97-kia", "sequence", "interpretation", ["c97-hanbo", "c97-kia"], "1997년 대기업 연쇄 부도의 시작과 정점. 한보가 기아 부도를 일으켰다는 근거는 없음"),
    E("d97-kia", "d97-rollover", "influence", "interpretation", ["c97-kia-delay", "c97-rollover"], "처리 지연이 대외 신인도 하락을 재촉했다는 평가(한 출처의 해석)"),
    E("e90-baht", "d97-rollover", "trigger", "interpretation", ["c90-baht", "c97-rollover"], "아시아 위기가 번지며 외국 은행들이 아시아 단기 대출을 회수"),
    E("d97-shortdebt", "d97-rollover", "cause", "evidenced", ["c97-shortdebt", "c97-rollover"], "갚아야 할 단기외채가 보유 외화보다 훨씬 많아 연장 거부가 곧 지급불능 위험이 됨"),
    E("d97-rollover", "d97-fx", "cause", "evidenced", ["c97-rollover", "c97-fx"], "외화 유출 → 보유액 급감 → 환율 폭등"),
    E("d97-fx", "e90-imfreq", "cause", "evidenced", ["c97-fx", "c90-kr-imf"], "외화가 바닥나 IMF에 구제금융 요청"),
    E("e90-imfreq", "d97-mou", "sequence", "evidenced", ["c97-mou", "c90-ch-550"], "요청 12일 뒤 이행각서 서명"),
    # 두 해석 (관계는 '해석'으로만)
    E("d97-shortdebt", "d97-view-liq", "similar", "interpretation", ["c97-view-liquidity"], "단기외채 대비 외화 부족을 핵심으로 보는 견해"),
    E("d97-leverage", "d97-view-str", "similar", "interpretation", ["c97-view-structure"], "부실 금융·기업 지배구조를 핵심으로 보는 견해"),
    # 대응 → 사회 변화
    E("d97-mou", "d97-unemp", "cause", "evidenced", ["c97-unemp-cause"], "고금리 긴축과 구조조정 요구 → 부도 속출 → 실업대란(한국노동연구원)"),
    E("d97-mou", "d97-tripartite", "background", "evidenced", ["c97-tripartite"], "IMF가 요구한 구조조정을 위한 사회적 합의"),
    E("d97-tripartite", "d97-dispatch", "cause", "evidenced", ["c97-tripartite", "c97-dispatch"], "사회협약 직후 정리해고제·파견근로제 법제화"),
    E("d97-tripartite", "d97-unemp", "influence", "evidenced", ["c97-unemp-cause"], "정리해고제 도입으로 인원감축 중심의 구조조정"),
    E("d97-unemp", "d97-safety", "cause", "evidenced", ["c97-safety"], "대량 실업에 대응한 실업대책·사회보험 확대"),
    E("d97-unemp", "tr-t90-pcbang", "influence", "hypothesis", ["c90-unemp", "c90-pcbang"], "실직자의 PC방 창업이 많았다는 이야기가 있으나 정량 근거는 아직 없음(가설)"),
    E("d97-mou", "e90-gold", "sequence", "evidenced", ["c90-gold"], "IMF 체제 직후 금 모으기 운동"),
    # 장기 결과
    E("d97-mou", "d97-repay", "sequence", "evidenced", ["c97-repay"], "3년 8개월 뒤 조기 상환"),
    E("d97-fx", "d97-reserve", "influence", "interpretation", ["c97-reserve-build"], "외화가 바닥났던 경험 뒤 외환보유액을 위기 완충장치로 쌓음"),
]
