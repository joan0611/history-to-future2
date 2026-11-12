"""주제 이야기(topic) 공통 도구 — 출처(S)·근거 문장(C)·층위 문장(L)과 전환점·추론·미래·결론 묶음.

한 주제 = 같은 대상을 끝까지 추적하는 이야기(R-Q3).
층위: fact(자료로 확인) / source(출처의 해석) / inference(AI가 여러 근거를 이은 추론) / hypothesis(확인이 필요한 가설).
"""

A = "2026-11-12"
LAYERS = ("fact", "source", "inference", "hypothesis")


def S(id, title, pub, url, stype, published=None, note=None, origin=None):
    d = {"id": id, "title": title, "publisher": pub, "url": url, "sourceType": stype, "accessedDate": A}
    if published:
        d["publishedDate"] = published
    if note:
        d["note"] = note
    if origin:
        d["origin"] = origin
    return d


def C(id, text, ctype, sources, period=None, scope=None, domains=("consumption",)):
    d = {"id": id, "text": text, "claimType": ctype, "status": "sourced", "sourceIds": sources,
         "domains": list(domains), "countries": ["KR"], "aiSynthesized": False}
    if period:
        d["period"] = period
    if scope:
        d["scope"] = scope
    return d


def L(layer, text, ids=()):
    assert layer in LAYERS, layer
    return {"layer": layer, "text": text, "ids": list(ids)}


def F(text, *ids):
    return L("fact", text, ids)


def SRC(text, *ids):
    return L("source", text, ids)


def INF(text, *ids):
    return L("inference", text, ids)


def HYP(text, *ids):
    return L("hypothesis", text, ids)


def TURN(id, years, start, title, why, before, condition, response, change, legacy, world=None, gap=None, end=None):
    """전환점 — 그전 상태 → 새 조건 → 반응 → 구체 변화 → 다음에 남긴 영향(R-Q7).
    why: 왜 이 시점을 전환점으로 잡았나. gap: 이 구간의 자료 공백. world: 세계 → 경로 → 대응 → 결과(R-W2)."""
    d = {"id": id, "years": years, "start": start, "end": end or start, "title": title, "why": why,
         "before": before, "condition": condition, "response": response, "change": change, "legacy": legacy}
    if world:
        d["world"] = world
    if gap:
        d["gap"] = gap
    return d


MODES = {"same": "거의 그대로 들어옴", "late": "늦게 확산", "adapted": "국내 조건에 맞게 변형", "rejected": "들어왔다가 밀려남", "outbound": "한국에서 세계로"}


def WORLD(what, route, response, result, mode):
    assert mode in MODES
    return {"what": what, "route": route, "response": response, "result": result, "mode": mode}


BRANCH_STATES = ("교체", "공존", "혼합", "분화", "축소", "재등장", "확대", "판단 보류")


def LANE(label, start, state, note, end=None):
    assert state in BRANCH_STATES, state
    return {"label": label, "start": start, "end": end, "state": state, "note": note}


def REASON(title, facts, logic, proposal, rivals, scope, check):
    """핵심 추론 6요소(R-Q10): 출발 사실 / 연결 논리 / 제안 설명 / 경쟁 설명 / 적용 시기·집단 / 확인·반박 자료."""
    return {"title": title, "facts": facts, "logic": logic, "proposal": proposal, "rivals": rivals, "scope": scope, "check": check}


FUTURE_KINDS = ("계속", "반작용", "결합", "분화", "경로 변경")


def FUT(kind, name, change, basis, logic, conditions, demand, watch, against, horizon=None):
    """미래 가능성 7항목(R-Q12, R-FU1). horizon은 근거가 있을 때만."""
    assert kind in FUTURE_KINDS
    d = {"kind": kind, "name": name, "change": change, "basis": basis, "logic": logic, "conditions": conditions,
         "demand": demand, "watch": watch, "against": against}
    if horizon:
        d["horizon"] = horizon
    return d


def CONCLUDE(key, favored, undecided, nextwatch, change):
    """결론 5요소(R-Q14)."""
    return {"key": key, "favored": favored, "undecided": undecided, "next": nextwatch, "change": change}


def LINK(target, at, why, kind="topic"):
    """다른 흐름과 만나는 지점(R-Q5) — 다음 단계로 넣지 않고 따로. kind: topic(주제 이야기) / flow(시대별 흐름) / industry."""
    return {"kind": kind, "target": target, "at": at, "why": why}


REPEAT_TYPES = ("재등장", "반작용", "반복되는 긴장", "결합·변형", "경제·산업 순환", "장기 구조 변화")


def REPEAT(type, title, past, now, alike, changed, alternatives, counter, at=(), interval=None):
    """반복·재등장(R-CY2~CY5). past/now: 누가 왜 선택했나. alike: 외형만인지 기능·동기도인지.
    changed: 가격·기술·매체·의미 변화와 과거 불편의 해결 여부. alternatives: '싫증→반대 유행' 외의 설명.
    counter: 반복되지 않은 사례·반대 증거·설명이 안 맞는 조건. at: 이 주제 안의 전환점 id들(과거, 현재)."""
    assert type in REPEAT_TYPES
    d = {"type": type, "title": title, "past": past, "now": now, "alike": alike, "changed": changed,
         "alternatives": alternatives, "counter": counter, "at": list(at)}
    if interval:
        d["interval"] = interval
    return d
