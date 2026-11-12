"""빠른 반복용: 기존 seed.json에 주제 이야기만 다시 넣는다(전체 빌드는 build_seed.py)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import importlib, topics_shop, topics
importlib.reload(topics_shop); importlib.reload(topics)
p = os.path.join(os.path.dirname(__file__), "..", "seed.json")
seed = json.load(open(p, encoding="utf-8"))
new_c = {c["id"] for c in topics.CLAIMS}
new_s = {s["id"] for s in topics.SOURCES}
seed["claims"] = [c for c in seed["claims"] if c["id"] not in new_c] + topics.CLAIMS
seed["sources"] = [s for s in seed["sources"] if s["id"] not in new_s] + topics.SOURCES
srcs = {s["id"]: s for s in seed["sources"]}
for c in topics.CLAIMS:
    org = {srcs[s].get("origin") or srcs[s]["publisher"] for s in c["sourceIds"] if s in srcs}
    c["independentSources"] = len(org)
    missing = [s for s in c["sourceIds"] if s not in srcs]
    if missing:
        raise SystemExit(f"{c['id']}: 없는 출처 {missing}")
seed["topics"] = topics.validate(seed["claims"], seed["flows"]["flows"], [f["id"] for f in seed["tastes"]["flows"]])
json.dump(seed, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("topics", len(seed["topics"]["topics"]))
