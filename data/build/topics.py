"""주제 이야기 모음 — 분야(domain) > 주제(topic). 한 주제는 같은 대상을 끝까지 추적한다(R-Q3).

화면 순서(R-FU3): 질문·장면 → 시간축 → 전환점 이야기(세계 연결 포함) → 갈래 → 다른 흐름과 만나는 곳 → 핵심 추론 → 반복 → 미래 → 결론.
11개 질문(R-A3)은 사용자 본문이 아니라 내부 점검표(CHECK)로 쓴다(R-Q6).
"""
import topics_shop as tshop
import topics_needs as tneeds
import topics_record as trec
import topics_life as tlife
import topics_life2 as tlife2
import topics_more as tmore
import topics_city as tcity
from topic_helpers import LAYERS, MODES, FUTURE_KINDS

DOMAINS = [
    {"id": "shop", "label": "소비·쇼핑", "desc": "어디서, 무엇으로, 어떻게 갖고, 무엇에 먼저 쓰고, 무엇을 보고 고르나 — 다섯 가지를 따로 추적합니다."},
    {"id": "city", "label": "도시와 주거", "desc": "어디에 사나와 어떻게 오가나를 따로 추적합니다."},
    {"id": "lifestyle", "label": "라이프스타일", "desc": "시간·공간·관계·몸·주의력을 어떻게 쓰고 관리하는지, 무엇을 좋은 삶으로 여기는지."},
] + tmore.DOMAINS

TOPICS = tshop.TOPICS + trec.TOPICS + tlife.TOPICS + tlife2.TOPICS + tcity.TOPICS + tmore.TOPICS
SOURCES = tshop.SOURCES + trec.SOURCES + tlife.SOURCES + tlife2.SOURCES + tcity.SOURCES + tmore.SOURCES
CLAIMS = tshop.CLAIMS + trec.CLAIMS + tlife.CLAIMS + tlife2.CLAIMS + tcity.CLAIMS + tmore.CLAIMS

# 아직 쓰지 않은 주제(탐색 화면에서 활성 콘텐츠와 다른 모양으로 표시, R-Q16)
PLANNED = [
    {"domain": "shop", "id": "shop-pay", "label": "무엇으로 값을 치르나 — 결제·신용·구매 자금"},
    {"domain": "shop", "id": "shop-own", "label": "어떻게 갖나 — 새것·중고·대여·구독"},
    {"domain": "shop", "id": "shop-items", "label": "무엇에 먼저 쓰나 — 구매 품목과 지출 우선순위"},
    {"domain": "shop", "id": "shop-info", "label": "무엇을 보고 고르나 — 구매 결정 정보와 영향력"},
]


# 12개 분야 지도(R-Q16) — 사용자가 실제로 읽을 수 있는 주제만 활성으로, 준비 중은 따로.
#   kind: topic(주제 이야기) / taste(취향 흐름) / flow(같은 대상을 따라가는 시대 흐름) / industry(산업 일대기)
#   대상이 섞여 있어 나누는 중인 흐름(산업·고용, 기술 보급, 여가 공간, 교통·도시·주거, 유통·결제)은 활성 목록에 넣지 않는다(R-Q3).
FIELD_MAP = [
    {"id": "buying", "label": "구매·소유·처분", "items": [("topic", "shop-channel"), ("topic", "shop-pay"), ("topic", "shop-own"), ("topic", "shop-items"), ("topic", "shop-info")], "planned": []},
    {"id": "space", "label": "공간·인테리어·생활용품", "items": [("topic", "city-home"), ("taste", "taste-home"), ("topic", "life-stuff")], "planned": ["식기·조명 단독 흐름"]},
    {"id": "fashion", "label": "패션·미용·자기표현", "items": [("taste", "taste-pants"), ("flow", "flow-expression"), ("flow", "flow-fashion")], "planned": ["신발", "헤어·화장"]},
    {"id": "food", "label": "음식·음료·외식", "items": [("taste", "taste-dining"), ("topic", "life-convenience")], "planned": ["카페·디저트", "간편식(가정간편식·밀키트)"]},
    {"id": "goods", "label": "상품·굿즈·수집", "items": [("taste", "taste-goods")], "planned": ["피규어·캐릭터 카드"]},
    {"id": "media", "label": "음악·영상·게임·팬덤", "items": [("flow", "flow-music"), ("topic", "media-screen"), ("topic", "media-game")], "planned": ["팬덤 지출"]},
    {"id": "relation", "label": "관계·모임·공동체", "items": [("taste", "taste-gather"), ("flow", "flow-relations")], "planned": []},
    {"id": "hobby", "label": "취미·운동·여가", "items": [("flow", "flow-sports"), ("flow", "flow-time"), ("topic", "life-health"), ("topic", "life-nature"), ("topic", "life-rest"), ("topic", "media-game")], "planned": ["여가를 보내는 장소(현재 흐름은 여행·노래방·배달이 섞여 있어 나누는 중)"]},
    {"id": "travel", "label": "여행·숙박·이동", "items": [("topic", "city-move"), ("topic", "travel-abroad")], "planned": ["숙소 고르기"]},
    {"id": "tech", "label": "기술·기기·디지털 생활", "items": [("industry", "tv"), ("industry", "phone"), ("industry", "internet"), ("topic", "life-record"), ("topic", "media-screen")], "planned": ["집 안 기기 보급(현재 흐름은 TV·휴대폰·메신저·AI가 섞여 있어 나누는 중)"]},
    {"id": "family", "label": "가족·주거·돌봄", "items": [("flow", "flow-family"), ("topic", "city-home"), ("topic", "life-alone")], "planned": ["돌봄"]},
    {"id": "work", "label": "일·학습·자기계발", "items": [("topic", "work-style"), ("flow", "flow-jobs")], "planned": ["자격·학습 서비스"]},
    {"id": "industry", "label": "산업(한국 경제를 키운 개별 산업)", "items": [("industry", x) for x in ["steel", "shipbuilding", "automobile", "petrochem", "construction", "semiconductor", "textile", "display", "battery"]], "planned": ["기계·전자부품(후속)"]},
    {"id": "money", "label": "돈·투자·금융 생활", "items": [("topic", "money-invest"), ("topic", "shop-pay")], "planned": ["저축·보험·연금", "대출과 집 마련 자금"]},
    {"id": "society", "label": "경제 위기·정치", "items": [("flow", "flow-economy"), ("flow", "flow-politics")], "planned": []},
    {"id": "lifestyle", "label": "라이프스타일 — 시간·공간·관계·몸·주의력을 쓰는 방식", "items": [("topic", "life-rest"), ("topic", "life-health"), ("topic", "life-stuff"), ("topic", "life-nature"), ("topic", "life-record"), ("topic", "life-alone"), ("topic", "life-convenience")], "planned": []},
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
        if t.get("compare"):
            cp = t["compare"]
            for row in cp["rows"]:
                if len(row["cells"]) != len(cp["cols"]):
                    errs.append(f"{w}: 비교표 칸 수 {row['label']}")
            for i in cp.get("ids", []):
                if i not in cids:
                    errs.append(f"{w}: 비교표 근거 {i}")
        for rp in t.get("repeats", []):
            tids = {tu["id"] for tu in t["turns"]}
            if not isinstance(rp["counter"], list) or not isinstance(rp["alternatives"], list):
                errs.append(f"{w}: 반복 counter/alternatives는 목록이어야 함")
            for a in rp["at"]:
                if a not in tids:
                    errs.append(f"{w}: 반복 링크 {a} 없음")
    if errs:
        raise SystemExit("주제 이야기 검증 실패:\n" + "\n".join(errs))
    have = {t["id"] for t in TOPICS}
    for nd in tneeds.NEEDS:
        for ln in _lines(nd):
            for i in ln["ids"]:
                if i not in cids:
                    errs.append(f"욕구 {nd['id']}: 없는 근거 {i}")
        for c in nd["cases"]:
            if c["kind"] == "topic" and c["id"] not in topic_ids:
                errs.append(f"욕구 {nd['id']}: 없는 주제 {c['id']}")
    if errs:
        raise SystemExit("욕구 검증 실패:\n" + "\n".join(errs))
    return {"needs": tneeds.NEEDS, "relKo": tneeds.REL_KO, "fieldMap": [dict(f, items=[{"kind": k, "id": i} for k, i in f["items"]]) for f in FIELD_MAP], "domains": DOMAINS, "topics": TOPICS, "planned": [p for p in PLANNED if p["id"] not in have],
            "check": [{"key": k, "label": l, "where": wh} for k, l, wh in CHECK]}
