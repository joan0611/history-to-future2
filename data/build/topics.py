"""주제 이야기 모음 — 분야(domain) > 주제(topic). 한 주제는 같은 대상을 끝까지 추적한다(R-Q3).

화면 순서(R-FU3): 질문·장면 → 시간축 → 전환점 이야기(세계 연결 포함) → 갈래 → 다른 흐름과 만나는 곳 → 핵심 추론 → 반복 → 미래 → 결론.
11개 질문(R-A3)은 사용자 본문이 아니라 내부 점검표(CHECK)로 쓴다(R-Q6).
"""
import topics_shop as tshop
from topic_helpers import LAYERS, MODES, FUTURE_KINDS

DOMAINS = [
    {"id": "shop", "label": "소비·쇼핑", "desc": "어디서, 무엇으로, 어떻게 갖고, 무엇에 먼저 쓰고, 무엇을 보고 고르나 — 다섯 가지를 따로 추적합니다."},
]

TOPICS = tshop.TOPICS
SOURCES = tshop.SOURCES
CLAIMS = tshop.CLAIMS

# 아직 쓰지 않은 주제(탐색 화면에서 활성 콘텐츠와 다른 모양으로 표시, R-Q16)
PLANNED = [
    {"domain": "shop", "id": "shop-pay", "label": "무엇으로 값을 치르나 — 결제·신용·구매 자금"},
    {"domain": "shop", "id": "shop-own", "label": "어떻게 갖나 — 새것·중고·대여·구독"},
    {"domain": "shop", "id": "shop-items", "label": "무엇에 먼저 쓰나 — 구매 품목과 지출 우선순위"},
    {"domain": "shop", "id": "shop-info", "label": "무엇을 보고 고르나 — 구매 결정 정보와 영향력"},
]

# 내부 점검표: 11개 질문 → 주제 안 어느 부분이 답하나(사용자 화면에는 본문으로 내보내지 않음)
CHECK = [
    ("before", "이전 선택과 매력", ["turns.before"]),
    ("popular", "인기 상품·스타일·공간·활동", ["turns.response", "turns.change"]),
    ("who", "누구·언제·계기", ["turns.condition", "turns.why"]),
    ("satisfy", "만족", ["turns.change", "reasons"]),
    ("pain", "흔해짐·비싸짐·불편", ["turns.legacy"]),
    ("diff", "새 선택의 차이", ["turns.change"]),
    ("forces", "가격·소득·주거·기술·인구·제도·미디어", ["turns.condition", "turns.world"]),
    ("brands", "브랜드·사업자", ["turns.response"]),
    ("relation", "교체·공존·혼합·분화·재등장", ["branches"]),
    ("remain", "남은 불편", ["turns.legacy", "conclusion"]),
    ("next", "다음 수요", ["futures"]),
]


def _lines(x):
    """객체 안의 모든 층위 문장을 꺼낸다."""
    if isinstance(x, dict):
        if "layer" in x and "text" in x:
            yield x
        else:
            for v in x.values():
                yield from _lines(v)
    elif isinstance(x, list):
        for v in x:
            yield from _lines(v)


def validate(claims_all, flows, taste_ids=()):
    cids = {c["id"] for c in claims_all}
    topic_ids = {t["id"] for t in TOPICS} | {p["id"] for p in PLANNED}
    flow_ids = {f["id"] for f in flows} | set(taste_ids)
    errs = []
    for t in TOPICS:
        w = t["id"]
        for k in ("id", "domain", "label", "tracks", "question", "scene", "turns", "branches", "reasons", "futures", "conclusion"):
            if not t.get(k):
                errs.append(f"{w}: '{k}' 없음")
        for ln in _lines(t):
            if ln["layer"] not in LAYERS:
                errs.append(f"{w}: 층위 {ln['layer']}")
            if ln["layer"] in ("fact", "source") and not ln["ids"]:
                errs.append(f"{w}: 근거 없는 사실/출처 문장 — {ln['text'][:30]}")
            for i in ln["ids"]:
                if i not in cids:
                    errs.append(f"{w}: 없는 근거 {i}")
        prev = None
        for tu in t["turns"]:
            for k in ("before", "condition", "response", "change", "legacy"):
                if not tu.get(k):
                    errs.append(f"{w}/{tu['id']}: 전환점 요소 '{k}' 비어 있음")
            if prev is not None and tu["start"] < prev - 30:
                errs.append(f"{w}/{tu['id']}: 시작 연도 순서 이상")
            prev = tu["start"]
            if tu.get("world") and tu["world"]["mode"] not in MODES:
                errs.append(f"{w}/{tu['id']}: 세계 유입 방식")
        for r in t["reasons"]:
            for k in ("facts", "logic", "proposal", "rivals", "scope", "check"):
                if not r.get(k):
                    errs.append(f"{w}: 추론 '{r['title'][:10]}' 요소 {k} 없음")
        fu = t["futures"]
        if not fu.get("split") or len(fu["items"]) < 2:
            errs.append(f"{w}: 미래는 갈라지는 이유 + 2개 이상")
        kinds = {x["kind"] for x in fu["items"]}
        if len(kinds) < 2:
            errs.append(f"{w}: 미래 가능성이 한 종류뿐")
        for x in fu["items"]:
            if x["kind"] not in FUTURE_KINDS:
                errs.append(f"{w}: 미래 종류 {x['kind']}")
            for k in ("change", "basis", "logic", "conditions", "demand", "watch", "against"):
                if not x.get(k):
                    errs.append(f"{w}: 미래 '{x['name'][:10]}' 항목 {k} 없음")
            if "%" in x["name"] and "확률" in x["name"]:
                errs.append(f"{w}: 확률 표기 금지")
        for k in ("key", "favored", "undecided", "next", "change"):
            if not t["conclusion"].get(k):
                errs.append(f"{w}: 결론 '{k}' 없음")
        for ln in t.get("links", []):
            if ln["kind"] == "topic" and ln["target"] not in topic_ids:
                errs.append(f"{w}: 없는 주제 {ln['target']}")
            if ln["kind"] == "flow" and ln["target"] not in flow_ids:
                errs.append(f"{w}: 없는 흐름 {ln['target']}")
        for rp in t.get("repeats", []):
            tids = {tu["id"] for tu in t["turns"]}
            for a in rp["at"]:
                if a not in tids:
                    errs.append(f"{w}: 반복 링크 {a} 없음")
    if errs:
        raise SystemExit("주제 이야기 검증 실패:\n" + "\n".join(errs))
    have = {t["id"] for t in TOPICS}
    return {"domains": DOMAINS, "topics": TOPICS, "planned": [p for p in PLANNED if p["id"] not in have],
            "check": [{"key": k, "label": l, "where": wh} for k, l, wh in CHECK]}
