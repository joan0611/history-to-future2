"""통합 지시서(2026-11-13) 3장 분야 A~J와 15장 9단계 상태를 seed에서 자동으로 계산한다.

- 분야 배정은 아래 규칙(지표 분류·사건 갈래·핵심어·명시 목록)으로만 한다. 사람이 '완료'를 적지 않는다.
- 상태 9단계는 각 분야에 실제로 들어 있는 근거·지표·주제·산업·연결·미래·테스트를 세어 판정한다.
  기준을 넘지 못하면 그 단계는 '아직'으로, 부족한 점은 문장으로 남긴다(지시서 15: 빈 설명으로 완료 처리 금지).
- 화면 테스트 여부는 tests/e2e.py에 그 분야 구성원 id가 실제로 나오는지로 본다.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
E2E = os.path.join(HERE, "..", "..", "tests", "e2e.py")

FIELDS = [
    {"id": "A", "key": "economy", "label": "경제", "subs": ["성장·경기", "물가·금리·통화", "환율·국제수지", "자산·부채", "소득·소비"],
     "indicators": ["gdp-growth", "gdppc-kr", "cpi-kr", "cpi-kr-2022", "call-kr", "disc-kr", "baserate-kr", "fx-kr"],
     "lanes": ["economy"], "flows": ["flow-economy"], "topics": ["money-invest", "money-save", "money-home", "money-insure"], "industries": [],
     "kw": r"외환위기|금융위기|금리|물가|인플레|환율|IMF|성장률|경기|부채|대출|주가|부동산"},
    {"id": "B", "key": "industry", "label": "산업", "subs": ["중화학공업", "전자·정보통신", "경공업", "건설", "유통·서비스"],
     "indicators": ["va-mfg-kr", "va-srv-kr", "va-agr-kr", "exports-kr", "emp-mfg-kr", "pcbang-kr"],
     "lanes": ["industry"], "flows": [], "topics": ["shop-channel"], "industries": "*",
     "kw": r"산업|공장|제철|조선|자동차|반도체|석유화학|건설|섬유|기업"},
    {"id": "C", "key": "energy", "label": "에너지·환경", "subs": ["석유·가스", "전력·원자력", "재생에너지", "환경 규제·기후"],
     "indicators": ["oil-dep-kr"], "lanes": [], "flows": [], "topics": ["space-tableware"], "industries": ["petrochem", "battery"],
     "kw": r"석유|원유|유가|에너지|전력|원자력|원전|석탄|가스|LNG|탄소|기후|환경|재생|태양광|형광등|오일"},
    {"id": "D", "key": "tech", "label": "기술", "subs": ["반도체·디스플레이", "통신·인터넷", "모바일·플랫폼", "AI·자동화"],
     "indicators": ["internet-kr", "mobile-kr", "tel-kr"], "lanes": [], "flows": [], "topics": ["life-record", "media-screen", "tech-home"],
     "industries": ["semiconductor", "display", "tv", "phone", "internet", "battery"],
     "kw": r"인터넷|반도체|스마트폰|휴대전화|컴퓨터|PC|인공지능|AI|로봇|자동화|디지털|플랫폼|통신|TV|텔레비전"},
    {"id": "E", "key": "labor", "label": "노동·고용", "subs": ["직업 구조", "임금·노동시간", "고용 형태", "실업·훈련"],
     "indicators": ["unemp-kr", "emprate-kr", "wage-kr", "realwage-kr", "emp-ag-kr", "emp-mfg-kr", "emp-svc-kr", "wage-share-kr", "unpaid-fam-kr"],
     "lanes": [], "flows": ["flow-jobs"], "topics": ["work-style", "work-learn", "work-cert"], "industries": [],
     "kw": r"노동|고용|실업|임금|파업|일자리|비정규|취업|근로|직업|노조"},
    {"id": "F", "key": "politics", "label": "정치·정책", "subs": ["정치체제·민주화", "경제·산업정책", "복지·교육정책", "규제·조세"],
     "indicators": [], "lanes": ["politics"], "flows": ["flow-politics"], "topics": [], "industries": [],
     "kw": r"정부|정책|법|제도|민주화|선거|정권|헌법|규제|세금|조세|복지"},
    {"id": "G", "key": "world", "label": "외교·국제관계", "subs": ["미국·일본·중국", "무역질서", "냉전·안보", "공급망"],
     "indicators": ["exports-kr", "exp-gdp-kr", "fx-kr"], "lanes": [], "flows": [], "topics": ["travel-abroad"], "industries": [],
     "kw": r"미국|중국|일본|WTO|GATT|FTA|냉전|수교|협정|무역|IMF|세계화|공급망|수출규제|베트남|중동|소련"},
    {"id": "H", "key": "society", "label": "사회·인구·주거", "subs": ["출산·고령화", "가족 구조", "도시화·지역", "주택·주거", "교육"],
     "indicators": ["tfr-kr", "one-person-kr", "aged-kr", "life-kr", "urban-kr", "house-kr", "hsupply-kr"],
     "lanes": ["society"], "flows": ["flow-family"], "topics": ["city-home", "city-move", "family-care", "life-alone", "money-home"], "industries": ["construction"],
     "kw": r"출산|고령|인구|가구|가족|도시|주택|아파트|교육|입시|지역|이주"},
    {"id": "I", "key": "living", "label": "소비·생활방식", "subs": ["쇼핑·결제", "식생활", "여가·여행", "취향·생활양식"],
     "indicators": ["online-kr", "hhcons-kr", "engel-kr", "cons-house-kr", "cons-culture-kr", "carreg-kr", "pcbang-kr"],
     "lanes": [], "flows": ["flow-time", "flow-relations"],
     "topics": ["shop-channel", "shop-pay", "shop-own", "shop-items", "shop-info", "food-cafe", "food-hmr", "food-dessert", "life-convenience", "life-rest",
                "life-health", "life-stuff", "life-nature", "travel-stay", "goods-collect", "hobby-place", "space-tableware", "tech-home"],
     "industries": [], "tastes": "*",
     "kw": r"소비|쇼핑|구매|외식|여행|여가|취미|생활|편의점|배달|카페"},
    {"id": "J", "key": "culture", "label": "문화·트렌드", "subs": ["음악·공연", "영상·방송·게임", "패션·미용", "세대 문화"],
     "indicators": ["music-exp-kr", "album-kr", "cons-culture-kr"], "lanes": ["culture"], "flows": ["flow-music", "flow-fashion", "flow-expression", "flow-sports"],
     "topics": ["media-screen", "media-game", "media-fandom", "fashion-beauty", "fashion-shoes", "fashion-hair"], "industries": [],
     "kw": r"음악|영화|드라마|방송|가요|아이돌|한류|K-?팝|패션|유행|문화|게임|공연"},
]

STAGES = ["시스템 구현", "데이터 확보", "출처 검증", "기본 분석 완료", "심층 인과 분석 완료", "분야 간 연결 완료", "추론·가설 검토 가능", "미래 시나리오 연결 완료", "실제 화면·기능 테스트 완료"]


def _nfut(x):
    if not x:
        return 0
    if isinstance(x, dict):
        return len(x.get("items") or x.get("paths") or [])
    return len(x)


def build(seed):
    nodes = seed["graph"]["nodes"]
    edges = seed["graph"]["edges"]
    claims = {c["id"]: c for c in seed["claims"]}
    topics = {t["id"]: t for t in seed["topics"]["topics"]}
    inds = {i["id"]: i for i in seed["industries"]["industries"]}
    flows = {f["id"]: f for f in seed["flows"]["flows"]}
    indicators = {i["id"]: i for i in seed["indicators"]}
    tastes = [f["id"] for f in seed["tastes"]["flows"]]
    e2e = open(E2E, encoding="utf-8").read() if os.path.exists(E2E) else ""
    annual_ok = {k for k, i in indicators.items() if i.get("frequency") == "annual" and not i.get("multi")}

    out = []
    member_field = {}
    for F in FIELDS:
        kw = re.compile(F["kw"])
        tids = [t for t in F["topics"] if t in topics]
        iids = list(inds) if F["industries"] == "*" else [i for i in F["industries"] if i in inds]
        fids = [f for f in F["flows"] if f in flows] + (tastes if F.get("tastes") == "*" else [])
        xids = [i for i in F["indicators"] if i in indicators]
        nids = [n["id"] for n in nodes if n["lane"] in F["lanes"] or (F["kw"] and kw.search(n["label"]))]
        for m in tids + iids + fids + xids + nids:
            member_field.setdefault(m, set()).add(F["id"])
        out.append({"F": F, "tids": tids, "iids": iids, "fids": fids, "xids": xids, "nids": nids})

    res = []
    for o in out:
        F, tids, iids, fids, xids, nids = o["F"], o["tids"], o["iids"], o["fids"], o["xids"], o["nids"]
        nset = set(nids)
        cids = set()
        for n in nodes:
            if n["id"] in nset:
                cids.update(n.get("claimIds", []))
        kw = re.compile(F["kw"])
        cids.update(c["id"] for c in seed["claims"] if kw.search(c["text"]))
        verified = sum(1 for c in cids if claims.get(c, {}).get("status") == "verified")
        edges_in = [e for e in edges if e["to"] in nset or e["from"] in nset]
        evid = sum(1 for e in edges_in if e["verification"] == "evidenced")
        reasons = sum(len(topics[t]["reasons"]) for t in tids) + sum(1 for i in iids if inds[i].get("stages"))
        rivals = sum(sum(len(r.get("rivals", [])) for r in topics[t]["reasons"]) for t in tids)
        deep_nodes = sum(1 for n in nodes if n["id"] in nset and n.get("deep"))
        futures = sum(_nfut(topics[t].get("futures")) for t in tids) + sum(_nfut(inds[i].get("futures")) for i in iids) + sum(_nfut(flows[f].get("futures")) for f in fids if f in flows)
        cross = set()
        for t in tids:
            for l in topics[t].get("links", []):
                cross.update(member_field.get(l["target"], set()) - {F["id"]})
        for e in edges_in:
            other = e["from"] if e["to"] in nset else e["to"]
            cross.update(member_field.get(other, set()) - {F["id"]})
        ann = [x for x in xids if x in annual_ok]
        tested = sorted({m for m in tids + iids + xids + fids if re.search(r"['\"/=]" + re.escape(m) + r"['\"&)?]", e2e)})
        content = len(tids) + len(iids) + len([f for f in fids if f in flows])
        checks = [
            (True, "공통 구조(주제·산업·흐름·원인 연결·질문 분석)를 이 분야에도 적용"),
            (len(xids) >= 1 or len(cids) >= 20, f"연도별 지표 {len(xids)}개, 관련 근거 문장 {len(cids)}개"),
            (len(cids) > 0 and verified / max(1, len(cids)) >= 0.15, f"두 곳 이상 확인 {verified}/{len(cids)}문장({round(100 * verified / max(1, len(cids)))}%) — 15% 이상이면 통과"),
            (content >= 2, f"주제 이야기 {len(tids)}·산업 일대기 {len(iids)}·흐름 {len([f for f in fids if f in flows])}"),
            ((reasons >= 2 and rivals >= 2) or deep_nodes >= 5, f"원인 추론 {reasons}건·다른 설명 {rivals}개·8단계 심층 사례 사건 {deep_nodes}개"),
            (len(cross) >= 3, f"다른 분야로 이어진 곳: {', '.join(sorted(cross)) or '없음'}"),
            (len(ann) >= 2, f"직접 검정 가능한 연도 지표 {len(ann)}개(2개 이상 필요), 질문 분석은 모든 분야 공통"),
            (futures >= 2, f"미래 갈래 {futures}개"),
            (len(tested) >= 2, f"자동 화면 테스트가 다루는 구성원 {len(tested)}개"),
        ]
        stages = [{"name": STAGES[k], "ok": bool(ok), "basis": basis} for k, (ok, basis) in enumerate(checks)]
        level = 0
        for s in stages:
            if not s["ok"]:
                break
            level += 1
        gaps = [f"{s['name']}: {s['basis']}" for s in stages if not s["ok"]]
        res.append({
            "id": F["id"], "key": F["key"], "label": F["label"], "subs": F["subs"],
            "members": {"topics": tids, "industries": iids, "flows": [f for f in fids if f in flows], "tastes": [f for f in fids if f not in flows], "indicators": xids, "events": len(nids)},
            "counts": {"claims": len(cids), "verified": verified, "edges": len(edges_in), "evidencedEdges": evid, "indicators": len(xids), "annual": len(ann)},
            "stages": stages, "level": level, "passed": sum(1 for s in stages if s["ok"]), "gaps": gaps,
        })
    return {"stages": STAGES, "fields": res,
            "note": "분야 배정과 단계 판정은 spec_fields.py의 규칙으로 빌드 때 계산한다. 사람이 완료를 적지 않는다. 앞 단계를 통과해야 다음 단계로 센다(level), 통과한 단계 수(passed)는 따로 센다."}
