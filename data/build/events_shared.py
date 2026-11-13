"""공통 사건·관계 유형 확장(통합 지시서 7장·14장).

1) 사건 공유: 주제 전환점·산업 단계가 원인 지도의 사건(node)과 **같은 근거 문장**을 쓰면 같은 사건으로 잇는다.
   이름이 비슷하다는 이유로는 잇지 않는다(근거 문장 공유만). 결과: turn["events"], stage["events"], seed["eventUses"].
2) 관계 유형: 기존 관계(rel)·검증 수준(verification)에서 지시서의 유형으로 옮겨 적고, 시차(년)를 붙인다.
   - 직접 원인 / 촉발 / 구조적 배경(간접) / 영향(간접) / 시간 순서(인과 미입증) / 상관(인과 미입증) / 유사 사례 / 미검증 추론
3) 공통 원인: 한 사건에서 서로 다른 분야(lane)의 둘 이상 사건으로 2년 안에 이어진 경우 → '공통 원인에 의한 동시 변화' 후보.
4) 피드백: A→B와 B→A(또는 A→B→C→A)가 모두 있는 경우.
모두 기존 연결에서 계산한 것이며 새 연결을 만들지 않는다.
"""

KIND = {
    ("cause", "evidenced"): "직접 원인", ("cause", "interpretation"): "직접 원인(해석)", ("cause", "hypothesis"): "미검증 추론",
    ("trigger", None): "촉발 요인", ("background", None): "구조적 배경(간접)", ("influence", None): "영향(간접)",
    ("sequence", None): "시간 순서(인과 미입증)", ("similar", None): "유사 사례",
}


def _ids(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "ids" and isinstance(v, list):
                yield from v
            else:
                yield from _ids(v)
    elif isinstance(o, list):
        for v in o:
            yield from _ids(v)


def kind_of(e):
    if e["verification"] == "hypothesis":
        return "미검증 추론"
    if e["verification"] == "statistical":
        return "상관(인과 미입증)"
    return KIND.get((e["rel"], e["verification"])) or KIND.get((e["rel"], None)) or e["rel"]


def build(seed):
    nodes = seed["graph"]["nodes"]
    by = {n["id"]: n for n in nodes}
    byc = {}
    for n in nodes:
        for c in n.get("claimIds", []):
            byc.setdefault(c, []).append(n["id"])
    uses = {}

    def attach(obj, use):
        cnt = {}
        for c in set(_ids(obj)):
            for nid in byc.get(c, []):
                cnt[nid] = cnt.get(nid, 0) + 1
        top = sorted(cnt, key=lambda k: (-cnt[k], by[k]["year"], k))[:3]
        obj["events"] = [{"id": k, "label": by[k]["label"], "year": by[k]["year"], "shared": cnt[k]} for k in top]
        for k in top:
            uses.setdefault(k, []).append({**use, "shared": cnt[k]})

    for t in seed["topics"]["topics"]:
        for u in t["turns"]:
            attach(u, {"kind": "topic", "id": t["id"], "label": t["label"].split(" — ")[0], "at": u["title"], "turn": u["id"]})
    for i in seed["industries"]["industries"]:
        for k, st in enumerate(i["stages"]):
            attach(st, {"kind": "industry", "id": i["id"], "label": i["label"], "at": f"{st['kind']}({st['period']})", "turn": str(k)})
    for k in uses:
        uses[k].sort(key=lambda x: (-x["shared"], x["kind"], x["id"]))

    edges = seed["graph"]["edges"]
    for e in edges:
        a, b = by.get(e["from"]), by.get(e["to"])
        e["kind7"] = kind_of(e)
        e["lag"] = (b["year"] - a["year"]) if a and b else None
    outs = {}
    for e in edges:
        if e["rel"] in ("cause", "trigger", "influence", "background"):
            outs.setdefault(e["from"], []).append(e)
    common = []
    for src, es in sorted(outs.items()):
        tg = [by[e["to"]] for e in es if e["to"] in by and e.get("lag") is not None and 0 <= e["lag"] <= 2]
        lanes = sorted({n["lane"] for n in tg})
        if len(tg) >= 2 and len(lanes) >= 2:
            common.append({"cause": src, "label": by[src]["label"], "year": by[src]["year"], "lanes": lanes,
                           "effects": [{"id": n["id"], "label": n["label"], "year": n["year"], "lane": n["lane"]} for n in sorted(tg, key=lambda n: (n["year"], n["id"]))]})
    pairs = {(e["from"], e["to"]) for e in edges if e["rel"] != "similar"}
    nxt = {}
    for a, b in pairs:
        nxt.setdefault(a, set()).add(b)
    fb = []
    seen = set()
    for a, b in sorted(pairs):
        if (b, a) in pairs and (b, a) not in seen:
            fb.append({"loop": [a, b], "labels": [by[a]["label"], by[b]["label"]]}); seen.add((a, b))
        for c in sorted(nxt.get(b, ())):
            if c != a and a in nxt.get(c, ()) and tuple(sorted((a, b, c))) not in seen:
                fb.append({"loop": [a, b, c], "labels": [by[x]["label"] for x in (a, b, c)]}); seen.add(tuple(sorted((a, b, c))))
    kinds = {}
    for e in edges:
        kinds[e["kind7"]] = kinds.get(e["kind7"], 0) + 1
    seed["graph"]["commonCauses"] = common
    seed["graph"]["feedbacks"] = fb
    seed["graph"]["kind7Counts"] = dict(sorted(kinds.items()))
    seed["eventUses"] = uses
    return {"turnsLinked": sum(1 for t in seed["topics"]["topics"] for u in t["turns"] if u["events"]),
            "stagesLinked": sum(1 for i in seed["industries"]["industries"] for s in i["stages"] if s["events"]),
            "common": len(common), "feedback": len(fb)}
