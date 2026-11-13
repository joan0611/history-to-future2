"""분야 A~J 상태 판정·공통 사건 연결이 자료에 따라 실제로 달라지는지(하드코딩이 아닌지) 확인."""
import copy, json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "data", "build"))
import spec_fields as sf  # noqa: E402
import events_shared as es  # noqa: E402

SEED = json.load(open(os.path.join(ROOT, "data", "seed.json"), encoding="utf-8"))


def field(r, fid):
    return next(f for f in r["fields"] if f["id"] == fid)


def test_status_depends_on_data():
    base = field(sf.build(copy.deepcopy(SEED)), "A")
    assert base["stages"][6]["ok"]  # 경제: 검정 가능한 연도 지표 2개 이상
    s = copy.deepcopy(SEED)
    s["indicators"] = [i for i in s["indicators"] if i["id"] not in sf.FIELDS[0]["indicators"]]
    after = field(sf.build(s), "A")
    assert not after["stages"][6]["ok"] and after["passed"] < base["passed"]


def test_every_field_has_nine_stages_and_basis():
    r = sf.build(copy.deepcopy(SEED))
    assert [f["id"] for f in r["fields"]] == list("ABCDEFGHIJ")
    for f in r["fields"]:
        assert len(f["stages"]) == 9 and all(st["basis"] for st in f["stages"])
        assert len(f["gaps"]) == 9 - f["passed"]


def test_shared_events_follow_claims():
    s = copy.deepcopy(SEED)
    es.build(s)
    linked = sum(1 for t in s["topics"]["topics"] for u in t["turns"] if u["events"])
    for n in s["graph"]["nodes"]:
        n["claimIds"] = []
    es.build(s)
    assert linked > 0 and sum(1 for t in s["topics"]["topics"] for u in t["turns"] if u["events"]) == 0


def test_edge_kinds_and_lag():
    s = copy.deepcopy(SEED)
    es.build(s)
    for e in s["graph"]["edges"]:
        assert e["kind7"]
        if e["verification"] == "statistical":
            assert "인과 미입증" in e["kind7"]
