"""변화 흐름 추가분 — '가족과 제도', '도시와 교통'.

flows.py와 같은 원칙을 따른다. 사실 문장은 모두 주장(claim)으로 두고 출처를 단다.
사이트가 지표에서 직접 계산한 문장은 claimType='statistical'.
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
    # ── 가족 ──
    S("fam-archives-family", "기록으로 만나는 대한민국 — 가족계획", "국가기록원",
      "https://theme.archives.go.kr/next/koreaOfRecord/family.do", "government"),
    S("fam-index-hhsize", "가구원수 (e-나라지표)", "통계청·국가데이터처 e-나라지표",
      "https://www.index.go.kr/unify/idx-info.do?idxCd=4229", "government"),
    S("fam-khan-250903", "결혼은 30대부터···초혼 연령, 여자도 남자도 30년새 5~6년 미뤄졌다", "경향신문",
      "https://www.khan.co.kr/article/202509031540001", "news", published="2025-09-03"),
    S("fam-weekly-180917", "[특집] 사회 변화 속도는 '급행' 법률 개정 속도는 '완행'", "주간경향",
      "https://weekly.khan.co.kr/article/201809171425001", "news", published="2018-09-17"),
    # ── 도시·교통 ──
    S("city-archives-gyeongbu", "정책 기록 — 경부고속도로 건설", "국가기록원",
      "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=306", "government"),
    S("city-korea-gyeongbu", "경부고속도로 개통 — 서울~부산 1일 생활권", "대한민국 정책브리핑",
      "https://www.korea.kr/briefing/policyBriefingView.do?newsId=148696466", "government"),
    S("city-newsis-200701", "[경부고속도로 개통 50주년①] 아우토반의 충격, 한강의 기적을 만들다", "뉴시스",
      "https://www.newsis.com/view/NISX20200701_0001080005", "news", published="2020-07-01"),
    S("city-seoulco-160601", "'미친 전세'에 30∼40대 탈(脫)서울 가속화…고령화 최대 과제", "서울신문",
      "https://m.seoul.co.kr/news/2016/06/01/20160601800049", "news", published="2016-06-01",
      origin="kr-resident-registration"),
    S("city-newspim-160426", "서울 인구 1988년 처음 1000만 돌파, 1992년 정점", "뉴스핌",
      "https://newspim.com/news/view/20160426000488", "news", published="2016-04-26",
      origin="kr-resident-registration"),
    S("city-seoul-stat-110829", "'서울 50년 변화상' 통계연보", "서울신문(서울Pn)",
      "https://m.go.seoul.co.kr/news/2011/08/29/20110829014010", "news", published="2011-08-29",
      note="서울시 「2011 서울통계연보」 발표를 옮긴 기사"),
    S("city-seoul-urban", "서울 도시계획 — 교통", "서울특별시 도시계획포털",
      "https://urban.seoul.go.kr/view/html/PMNU1030000001", "government"),
    S("city-archives-subway", "기록으로 만나는 대한민국 — 지하철", "국가기록원",
      "https://theme.archives.go.kr/next/koreaOfRecord/subway.do", "government"),
    S("city-mediahub-line1", "추억 소환! 46돌 맞은 '지하철 1호선'의 모든 것", "서울시 미디어허브",
      "https://mediahub.seoul.go.kr/archives/1292714", "government", published="2020-08-14"),
    S("city-archives-newtown", "정책 기록 — 신도시 조성 및 주택 공급", "국가기록원",
      "https://theme.archives.go.kr/next/govpo/detail.do?policySeq=317", "government"),
    S("city-sgsg-181005", "Cover Story — 신도시 개발 빛과 그늘", "한국경제 생글생글",
      "https://sgsg.hankyung.com/article/2018100546681", "news", published="2018-10-05"),
    S("city-newsis-190829", "한국 가구 절반은 아파트에 산다…거주 비중 50% 첫 돌파", "뉴시스",
      "https://www.newsis.com/view/NISX20190829_0000754688", "news", published="2019-08-29"),
    S("city-newdaily-210303", "'1000만 서울' 32년 만에 1000만 명 아래로", "뉴데일리",
      "https://www.newdaily.co.kr/site/data/html/2021/03/03/2021030300067.amp.html", "news", published="2021-03-03"),
    S("city-korea-capital", "2021년 인구주택총조사 결과 브리핑", "대한민국 정책브리핑",
      "https://www.korea.kr/briefing/policyBriefingView.do?newsId=156518704", "government"),
    S("city-mediahub-ktx", "서울역의 어제와 오늘, 그리고 유라시아 횡단의 꿈", "서울시 미디어허브",
      "https://mediahub.seoul.go.kr/archives/1502210", "government"),
]


CLAIMS = [
    # ── 가족과 제도 ──
    C("fl-fam-tfr",
      "합계출산율은 1960년 6.0명에서 1983년 2.06명으로 떨어져 인구 대체 수준(약 2.1명) 아래로 내려갔고, 2018년 0.98명으로 1명 아래가 되었다.",
      "statistical", "sourced", ["fred-kr-tfr"], ["society"], period="1960~2018",
      scope="2.1명은 흔히 쓰는 대체 출산율 기준값이다.", support="세계은행 WDI(FRED SPDYNTFRTINKOR) 연간 값"),
    C("fl-fam-60s",
      "1960년대 가족계획 구호는 '덮어놓고 낳다보면 거지꼴을 못 면한다'였고, 인구증가율은 1960년대 초 3.3%였다.",
      "fact", "sourced", ["fam-archives-family"], ["society", "politics"], period="1960년대"),
    C("fl-fam-70s",
      "1970년대에는 '세 살 터울로 세 자녀만 35세 이전에 낳자'에서 '아들·딸 구별 말고 둘만 낳아 잘 기르자'로 구호가 바뀌었다. 출생아는 1971년 102만 5천 명으로 가장 많았고, 인구증가율은 1970년대 초 2.0%로 낮아졌다.",
      "fact", "sourced", ["fam-archives-family"], ["society", "politics"], period="1970년대"),
    C("fl-fam-80s",
      "1980년대 구호는 '하나씩만 낳아도 삼천리는 초만원!', '잘 키운 딸 하나 열 아들 안 부럽다'였고, 인구증가율은 1.57%였다.",
      "fact", "sourced", ["fam-archives-family"], ["society", "politics"], period="1980년대"),
    C("fl-fam-pronatal",
      "2000년대 들어 구호는 출산 장려로 돌아섰다('아빠! 하나는 싫어요. 엄마! 저도 동생을 갖고 싶어요'). 2010년대에는 '허전한 한 자녀 흐뭇한 두 자녀 든든한 세 자녀'가 쓰였다.",
      "fact", "sourced", ["fam-archives-family"], ["society", "politics"], period="2000~2010년대"),
    C("fl-fam-hh",
      "평균 가구원수는 2000년 3.1명, 2010년 2.7명, 2020년 2.3명, 2025년 2.2명이다. 가장 많은 가구 유형은 1985~2005년 4인 가구, 2010년 2인 가구, 2015년 이후 1인 가구였다.",
      "statistical", "sourced", ["fam-index-hhsize"], ["society"], period="1985~2025",
      scope="일반가구 기준. 2000년 이전 평균 가구원수는 이 지표 화면에서 확인하지 않았다."),
    C("fl-fam-marriage",
      "혼인 건수는 1996년 43만 5천 건으로 가장 많았고, 2022년 19만 2천 건으로 가장 적었다. 2024년은 22만 2,400건으로 두 해 연속 늘었지만 1996년보다 44.2% 적다. 초혼 연령은 30년 사이 남녀 모두 5~6년 늦어졌다.",
      "statistical", "sourced", ["fam-khan-250903"], ["society"], period="1996~2024",
      support="통계청 혼인 통계를 옮긴 기사"),
    C("fl-fam-ssdb",
      "헌법재판소는 1997년 7월 16일 동성동본 금혼 조항에 헌법불합치 결정을 내렸고(위헌 5·헌법불합치 2·합헌 2), 이로써 약 6만 쌍의 동성동본 부부가 혼인신고를 할 길이 열렸다. 민법에서 이 조항이 빠진 것은 그로부터 8년 뒤다.",
      "fact", "sourced", ["fam-weekly-180917"], ["society", "politics"], period="1997~2005",
      scope="지금은 8촌 이내 혈족이 아니면 혼인신고가 가능하다."),
    C("fl-fam-law-lag",
      "주간경향은 동성동본 금혼·호주제 등의 사례를 들어 가족에 관한 사회 변화는 빠른데 법률 개정은 늦게 따라온다고 지적했다.",
      "interpretation", "sourced", ["fam-weekly-180917"], ["society", "politics"], period="1997~2018",
      scope="한 매체의 해석이다."),

    # ── 도시와 교통 ──
    C("fl-city-urban",
      "도시에 사는 인구 비율은 1960년 27.7%에서 1990년 74.0%로 늘었고, 2000년대 이후 81% 안팎에서 멈췄다.",
      "statistical", "sourced", ["wb-kr-urban"], ["society"], period="1960~2025",
      scope="UN 세계도시화전망 기반 추정치로, 한국 정부의 '도시 지역' 정의와 다를 수 있다.",
      support="WDI SP.URB.TOTL.IN.ZS"),
    C("fl-city-seoulpop",
      "서울 인구는 1960년 245만 명, 1970년 543만 명, 1980년 836만 명으로 늘었고, 1988년 처음 1천만 명을 넘어 1992년 약 1,093만 명으로 정점을 찍었다.",
      "statistical", "sourced", ["city-seoulco-160601", "city-newspim-160426"], ["society"],
      period="1960~1992", scope="주민등록인구 기준. 두 기사는 같은 행정 통계를 옮긴 것이다."),
    C("fl-city-cars",
      "서울의 자동차는 1960년 1만 1,411대였고, 2011년 처음 300만 대를 넘었다. 도로 길이는 같은 기간 1,337km에서 8,142km로 6.1배가 되었다.",
      "statistical", "sourced", ["city-seoul-stat-110829"], ["society", "technology"], period="1960~2011",
      support="서울시 「2011 서울통계연보」"),
    C("fl-city-tram",
      "서울시는 1960년대 말 인구와 자동차가 늘자 전차를 철거하고 도로교통법을 만들어 교통체계를 마련했으며, 이후 한강 다리들과 지하철 1호선을 개통했다고 설명한다.",
      "fact", "sourced", ["city-seoul-urban"], ["society", "technology"], period="1960년대 말~1970년대"),
    C("fl-city-gyeongbu",
      "경부고속도로(서울~부산 428km)는 1968년 2월 1일 착공해 2년 5개월 만인 1970년 7월 7일 완전 개통되었다. 정부가 내건 목적은 '국토 대동맥'을 통한 산업화와 경제 성장 촉진이었다.",
      "fact", "verified", ["city-archives-gyeongbu", "city-korea-gyeongbu"], ["economy", "technology"], period="1968~1970"),
    C("fl-city-gyeongbu-life",
      "개통으로 16시간 걸리던 서울~부산이 5시간 35분으로 줄었고, 경부축이 1일 생활권으로 연결됐다. 총공사비 429억 원은 1967년 국가 예산의 24%에 해당했다.",
      "fact", "verified", ["city-korea-gyeongbu", "city-newsis-200701"], ["economy", "technology"], period="1970",
      scope="소요 시간은 출처마다 4시간~5시간 35분으로 다르게 적혀 있다."),
    C("fl-city-line1",
      "1971년 4월 12일 기공한 서울 지하철 1호선은 1974년 8월 15일 서울역~청량리 9개 역, 7.8km 구간으로 개통했다. 한국 최초의 지하철이다.",
      "fact", "verified", ["city-archives-subway", "city-mediahub-line1"], ["society", "technology"], period="1971~1974"),
    C("fl-city-newtown-why",
      "1980년대 후반 서울에 더 개발할 땅이 부족한 가운데 3저 호황·올림픽 특수와 베이비부머의 결혼이 겹쳐 1988년 한 해 서울 집값이 24% 올랐고, 정부는 1988년 '주택 200만 호 건설 계획'을 발표했다.",
      "interpretation", "sourced", ["city-sgsg-181005"], ["economy", "society"], period="1987~1988",
      scope="원인 설명은 기사의 정리다. 국가기록원은 계획의 시작을 1987년으로 적는다."),
    C("fl-city-newtown",
      "분당·일산·평촌·산본·중동 5개 1기 신도시는 1989~1996년 50.1㎢에 주택 29만 2천 호(인구 약 117만 명)를 공급했다. 서울 집값은 신도시 입주가 시작된 1991년 하락세로 돌아섰다.",
      "fact", "verified", ["city-archives-newtown", "city-sgsg-181005"], ["economy", "society"], period="1989~1996",
      scope="주택 수는 국가기록원 값. 한국경제는 계획 목표를 28만 2천 가구로 적어 차이가 있다. 집값 하락 시점은 한국경제 기사의 설명이다."),
    C("fl-city-apt",
      "2018년 아파트에 사는 가구가 처음으로 전체의 절반을 넘었다. 통계청이 아파트를 따로 집계하기 시작한 1975년 이래 처음이다.",
      "statistical", "sourced", ["city-newsis-190829"], ["society", "consumption"], period="1975~2018",
      support="통계청 인구주택총조사 주택 부문"),
    C("fl-city-2004",
      "2004년 4월 KTX가 처음 개통했고, 같은 해 서울시는 대중교통 체계를 개편했다.",
      "fact", "verified", ["city-mediahub-ktx", "city-seoul-urban"], ["society", "technology"], period="2004"),
    C("fl-city-seoul-decline",
      "서울 총인구(내국인+외국인)는 1992년 정점 뒤 줄어 2016년 1천만 명 아래(993만 명)가 되었다. 뉴데일리는 이를 경기도 신도시 개발과 출산율 감소의 영향으로 설명했다.",
      "interpretation", "sourced", ["city-newdaily-210303"], ["society"], period="1992~2020"),
    C("fl-city-capital",
      "수도권에 사는 인구 비율은 2019년 처음 50%를 넘었고, 2021년 50.4%였다.",
      "statistical", "sourced", ["city-korea-capital"], ["society"], period="2019~2021",
      support="통계청 인구주택총조사 브리핑"),
]


FLOWS = [
    {
        "id": "flow-family",
        "question": "가족의 크기와 가족을 정하는 제도는 어떻게 달라졌나?",
        "cats": ["society", "politics"],
        "span": [1960, 2025],
        "shape": "반전 — 출산을 줄이자던 정부가 40년 뒤 출산을 장려하게 됐다. 제도는 가족의 실제 변화보다 늦게 따라왔다.",
        "lede": ["fl-fam-tfr", "fl-fam-hh"],
        "indicators": ["tfr-kr", "one-person-kr"],
        "steps": [
            {"id": "f1", "phase": "before", "period": "1960년대", "title": "아이가 많던 시대와 가족계획의 시작",
             "claimIds": ["fl-fam-60s", "fl-fam-tfr"], "nodeIds": []},
            {"id": "f2", "phase": "condition", "period": "1970년대", "title": "'둘만 낳자' — 출생아 정점",
             "claimIds": ["fl-fam-70s"], "nodeIds": []},
            {"id": "f3", "phase": "turn", "period": "1980년대", "title": "'하나씩만' — 대체 수준 아래로",
             "claimIds": ["fl-fam-80s"], "nodeIds": []},
            {"id": "f4", "phase": "life", "period": "1985~2025", "title": "작아진 가구 — 4인에서 1인으로",
             "claimIds": ["fl-fam-hh", "c10-1person"], "nodeIds": []},
            {"id": "f5", "phase": "turn", "period": "1997~2008", "title": "동성동본 금혼과 호주제 — 제도가 바뀌다",
             "claimIds": ["fl-fam-ssdb", "cfill-hoju"], "nodeIds": ["e00-hoju"]},
            {"id": "f6", "phase": "spread", "period": "1996~2024", "title": "결혼이 줄고 늦어지다",
             "claimIds": ["fl-fam-marriage"], "nodeIds": []},
            {"id": "f7", "phase": "turn", "period": "2000년대~", "title": "출산 억제에서 출산 장려로",
             "claimIds": ["fl-fam-pronatal"], "nodeIds": []},
            {"id": "f8", "phase": "now", "period": "2018~2025", "title": "출산율 0명대와 인구 감소",
             "claimIds": ["c10-tfr", "c20-pop"], "nodeIds": ["e10-tfr"]},
        ],
        "links": [
            {"from": "f1", "to": "f2", "kind": "sequence", "note": "구호가 '셋'에서 '둘'로 바뀌는 동안 인구증가율이 3.3%에서 2.0%로 낮아졌다. 가족계획 사업이 이 하락에 얼마나 기여했는지 나눈 자료는 여기 없다.", "claimIds": ["fl-fam-60s", "fl-fam-70s"]},
            {"from": "f2", "to": "f3", "kind": "correlation", "note": "캠페인 강화와 출산율 하락이 함께 진행됐다. 같은 시기 도시화·교육 확대도 있었기 때문에 캠페인만의 효과로 볼 수는 없다.", "claimIds": ["fl-fam-tfr"]},
            {"from": "f3", "to": "f7", "kind": "sequence", "note": "출산율이 대체 수준 아래로 내려간 지 약 20년 뒤에야 구호가 출산 장려로 바뀌었다.", "claimIds": ["fl-fam-pronatal"]},
            {"from": "f4", "to": "f5", "kind": "interpretation", "note": "가족에 관한 사회 변화는 빠른데 법 개정은 늦게 따라온다는 지적이 있다. 동성동본 금혼은 헌법불합치 결정 8년 뒤에야 민법에서 빠졌다.", "claimIds": ["fl-fam-law-lag"]},
            {"from": "f6", "to": "f8", "kind": "correlation", "note": "혼인 감소와 출생아 감소가 함께 나타났다. 한국은 혼외 출산이 적어 둘이 함께 움직인다는 설명이 흔하지만, 그 비중 자료는 이 흐름에 연결하지 않았다.", "claimIds": ["fl-fam-marriage", "c10-tfr"]},
        ],
        "cross": [
            {"flow": "flow-city", "note": "서울로 사람이 몰리고 아파트가 주된 집이 된 과정은 가족이 작아진 과정과 같은 시기에 진행됐다."},
            {"flow": "flow-jobs", "note": "무급가족종사자가 줄고 임금근로자가 늘면서 가족이 함께 일하는 단위에서 따로 버는 단위로 바뀌었다(연결은 해석)."},
        ],
        "gaps": [
            "피임 실천율의 연도별 자료 — 1960년대 초 한 자릿수에서 1980년대 후반 70%대로 올랐다는 연구를 찾았지만 원문을 열어 확인하지 못해 넣지 않았다.",
            "출생 성비(남아선호)의 장기 추이.",
            "이혼 건수의 장기 추이.",
            "2000년 이전 평균 가구원수의 연도별 값.",
        ],
        "alternatives": [
            "출산율 하락을 정부 가족계획 사업의 성과로 보는 설명과, 도시화·교육 확대·여성 경제활동 같은 사회경제 변화를 더 중시하는 설명이 함께 있다.",
            "최근의 저출산을 주거비·고용 불안에서 찾는 설명과, 결혼·자녀에 대한 가치관 변화에서 찾는 설명이 함께 있다.",
        ],
    },
    {
        "id": "flow-city",
        "question": "사람들은 어디에 모여 살고 어떻게 이동하게 됐나?",
        "cats": ["society", "economy"],
        "span": [1960, 2025],
        "shape": "집중과 확산 — 서울로 몰렸다가, 서울을 넘어 수도권 신도시로 퍼졌다. 이동 수단은 길(고속도로)·땅 밑(지하철)·고속철로 겹겹이 늘었다.",
        "lede": ["fl-city-urban", "fl-city-seoulpop"],
        "indicators": ["urban-kr", "carreg-kr"],
        "steps": [
            {"id": "c1", "phase": "before", "period": "1960", "title": "도시에 사는 사람이 넷 중 하나",
             "claimIds": ["fl-city-urban"], "nodeIds": []},
            {"id": "c2", "phase": "condition", "period": "1960~1992", "title": "서울로 몰린 인구",
             "claimIds": ["fl-city-seoulpop"], "nodeIds": []},
            {"id": "c3", "phase": "turn", "period": "1968~1970", "title": "경부고속도로 — 1일 생활권",
             "claimIds": ["fl-city-gyeongbu", "fl-city-gyeongbu-life"], "nodeIds": []},
            {"id": "c4", "phase": "turn", "period": "1968~1974", "title": "전차 철거와 지하철 1호선",
             "claimIds": ["fl-city-tram", "fl-city-line1"], "nodeIds": []},
            {"id": "c5", "phase": "life", "period": "1976~2011", "title": "자동차가 생활 속으로",
             "claimIds": ["c70-pony-1", "fl-city-cars"], "nodeIds": ["tr-t70-mycar"]},
            {"id": "c6", "phase": "spread", "period": "1984", "title": "2호선 순환선과 강남",
             "claimIds": ["cfill-line2"], "nodeIds": ["e80-line2"]},
            {"id": "c7", "phase": "turn", "period": "1988~1996", "title": "주택 200만 호와 1기 신도시",
             "claimIds": ["fl-city-newtown-why", "fl-city-newtown"], "nodeIds": []},
            {"id": "c8", "phase": "turn", "period": "2004", "title": "KTX와 대중교통 개편",
             "claimIds": ["fl-city-2004"], "nodeIds": []},
            {"id": "c9", "phase": "life", "period": "2018", "title": "아파트에 사는 가구가 절반을 넘다",
             "claimIds": ["fl-city-apt"], "nodeIds": []},
            {"id": "c10", "phase": "now", "period": "1992~2021", "title": "줄어든 서울, 커진 수도권",
             "claimIds": ["fl-city-seoul-decline", "fl-city-capital"], "nodeIds": []},
        ],
        "links": [
            {"from": "c1", "to": "c2", "kind": "sequence", "note": "전국 도시화와 서울 집중이 같은 시기에 진행됐다.", "claimIds": ["fl-city-urban", "fl-city-seoulpop"]},
            {"from": "c2", "to": "c4", "kind": "condition", "note": "서울시는 인구와 자동차 증가를 전차 철거·교통체계 정비·지하철 건설의 배경으로 설명한다.", "claimIds": ["fl-city-tram"]},
            {"from": "c4", "to": "c6", "kind": "sequence", "note": "1호선 뒤 10년 만에 순환선이 생겼다. 2호선은 도심 기능을 강남으로 옮기는 과정에서 구체화됐다.", "claimIds": ["cfill-line2"]},
            {"from": "c2", "to": "c7", "kind": "condition", "note": "서울에 더 개발할 땅이 없는데 집값이 급등한 것이 신도시 건설의 배경으로 꼽힌다(기사 정리).", "claimIds": ["fl-city-newtown-why"]},
            {"from": "c7", "to": "c10", "kind": "interpretation", "note": "서울 인구가 1천만 아래로 내려간 이유로 경기도 신도시 개발과 출산율 감소가 함께 꼽힌다(언론 설명).", "claimIds": ["fl-city-seoul-decline"]},
            {"from": "c7", "to": "c9", "kind": "sequence", "note": "대규모 아파트 단지 공급이 이어진 끝에 아파트가 가장 흔한 집이 되었다. 연도별 비중 추이는 여기 연결하지 않았다.", "claimIds": []},
            {"from": "c3", "to": "c8", "kind": "sequence", "note": "도로로 시작된 국토 축이 34년 뒤 고속철도로 다시 이어졌다.", "claimIds": []},
        ],
        "cross": [
            {"flow": "flow-family", "note": "가구가 작아지고 1인 가구가 늘어난 것은 주거 형태(아파트·원룸)의 변화와 함께 봐야 한다."},
            {"flow": "flow-jobs", "note": "공업화로 일자리가 도시에 모인 것이 이주의 배경으로 꼽힌다(연결은 해석)."},
            {"flow": "flow-shop", "note": "신도시·아파트 단지와 대형마트의 확산은 같은 시기에 진행됐다."},
        ],
        "gaps": [
            "1960~70년대 서울 이주민의 주거(판자촌·철거 이주) 규모를 보여주는 통계.",
            "통근 시간의 장기 추이.",
            "전국 자동차 등록 대수의 1960년대부터의 연속 통계 — 이 사이트의 지표는 1993년부터의 신규 승용차 등록뿐이다.",
            "아파트 거주 비중의 연도별 추이(1975~2018).",
            "지방 도시의 인구 감소는 아직 다루지 않았다.",
        ],
        "alternatives": [
            "고속도로·신도시를 성장과 주거 안정의 기반으로 보는 설명과, 수도권 집중과 지역 격차를 키웠다고 보는 설명이 함께 있다.",
        ],
    },
]
