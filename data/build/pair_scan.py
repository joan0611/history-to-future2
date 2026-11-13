"""지표 쌍 시차 자동 탐색(T6-2, 지시서 8: 사이클·관계를 사람이 고르지 않고 엔진이 찾는다) — 20차.

방법(빌드 때 계산, 결과는 seed["pairScan"]):
  1) 연도 지표(여러 계열을 묶은 지표·월별 지표 제외) 모든 쌍에서, 겹치는 해 20개 이상인 쌍만 본다.
  2) 수준이 아니라 '전년 대비 변화'에서 직선 추세까지 뺀 값끼리 상관을 낸다(긴 추세 때문에 생기는 겉보기 상관을 피함).
  3) 시차 −3~+3년 가운데 |r|이 가장 큰 시차를 고른다.
  4) 같은 방식으로 'b 쪽을 3년 묶음 단위로 섞은' 가짜 자료 400개를 만들어, 가짜에서도 그만큼 큰 |r|이 나오는 비율(p)을 낸다.
     시차를 7개 중에서 고른 것까지 가짜에도 똑같이 적용하므로 '여러 시차를 뒤져서 생긴 우연'이 p에 반영된다.
  5) 쌍이 많아 우연히 걸리는 것을 막으려고 벤자민-호크버그 방식으로 거짓 발견 비율(q)을 낸다. q < 0.10만 '발견'으로 남긴다.
  6) 큰 충격의 해(1980·1998·2009·2020)를 빼고 다시 계산해, 상관이 한 해의 충격에만 기대는지 표시한다.
  7) 같은 표의 비중끼리(합이 100%), 같은 금리 계열처럼 정의상 함께 움직이는 쌍은 처음부터 뺀다.
결과는 '관찰된 관계(계산)'이며 인과가 아니다. 공통 원인(경기·인구)이 둘을 함께 움직였을 수 있다.
"""
import numpy as np

SAME = [
    {"emp-ag-kr", "emp-mfg-kr", "emp-svc-kr"}, {"va-agr-kr", "va-mfg-kr", "va-srv-kr"},
    {"elec-nucl-kr", "elec-coal-kr", "elec-rnew-kr"}, {"call-kr", "disc-kr", "baserate-kr"},
    {"wage-kr", "realwage-kr"}, {"cpi-kr", "cpi-kr-2022"}, {"wage-share-kr", "unpaid-fam-kr"},
    {"gdp-growth", "gdppc-kr"}, {"exports-kr", "exp-gdp-kr"}, {"engel-kr", "cons-house-kr", "cons-culture-kr"},
]
LAGS = range(-3, 4)
N_PERM = 400


def _series(ind):
    ss = [s for s in ind["series"] if s.get("country") == "KR"] or ind["series"]
    out = {}
    for d, v in ss[0]["points"]:
        try:
            out[int(str(d)[:4])] = float(v)
        except (TypeError, ValueError):
            pass
    return out


def _diff(d):
    """전년 대비 변화에서 직선 추세까지 뺀 값. 인구·도시화처럼 매끄러운 계열은 변화 자체에도 추세가 남아 겉보기 상관을 만든다."""
    dd = {y: d[y] - d[y - 1] for y in d if y - 1 in d}
    if len(dd) < 5:
        return dd
    ys = np.array(sorted(dd), dtype=float)
    vs = np.array([dd[int(y)] for y in ys])
    k, c = np.polyfit(ys, vs, 1)
    return {int(y): float(v - (k * y + c)) for y, v in zip(ys, vs)}


def _corr(x, y):
    if len(x) < 8:
        return None
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return None
    return float(((x - x.mean()) * (y - y.mean())).mean() / (sx * sy))


def _best(da, db):
    best = (0, None, 0)
    for lag in LAGS:  # lag > 0: b가 a보다 lag년 늦게 움직임
        ys = [y for y in da if (y + lag) in db]
        if len(ys) < 15:
            continue
        r = _corr(np.array([da[y] for y in ys]), np.array([db[y + lag] for y in ys]))
        if r is not None and (best[1] is None or abs(r) > abs(best[1])):
            best = (lag, r, len(ys))
    return best


def _perm_p(da, db, obs, rng):
    yb = sorted(db)
    vals = np.array([db[y] for y in yb])
    blocks = [vals[i:i + 3] for i in range(0, len(vals), 3)]
    hit = 0
    for _ in range(N_PERM):
        order = rng.permutation(len(blocks))
        sh = np.concatenate([blocks[i] for i in order])[:len(yb)]
        fake = dict(zip(yb, sh))
        _, r, _ = _best(da, fake)
        if r is not None and abs(r) >= abs(obs) - 1e-12:
            hit += 1
    return (hit + 1) / (N_PERM + 1)


def build(seed):
    inds = [i for i in seed["indicators"] if i.get("frequency") == "annual" and not i.get("multi")]
    data = {i["id"]: _diff(_series(i)) for i in inds}
    title = {i["id"]: i["title"] for i in inds}
    rng = np.random.default_rng(20261113)
    rows = []
    ids = sorted(data)
    for k, a in enumerate(ids):
        for b in ids[k + 1:]:
            if any(a in g and b in g for g in SAME):
                continue
            if len(set(data[a]) & set(data[b])) < 20:
                continue
            lag, r, n = _best(data[a], data[b])
            if r is None:
                continue
            rows.append({"a": a, "b": b, "lag": lag, "r": round(r, 3), "n": n})
    # 큰 것부터 순열 검정(작은 상관은 p가 클 것이 분명해 계산을 줄인다: |r| < 0.25는 p=1로 둔다)
    for row in rows:
        row["p"] = round(_perm_p(data[row["a"]], data[row["b"]], row["r"], rng), 4) if abs(row["r"]) >= 0.25 else 1.0
    m = len(rows)
    order = sorted(range(m), key=lambda i: rows[i]["p"])
    q = [1.0] * m
    prev = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        prev = min(prev, rows[i]["p"] * m / rank)
        q[i] = round(prev, 4)
    for i, row in enumerate(rows):
        row["q"] = q[i]
        row["aTitle"], row["bTitle"] = title[row["a"]], title[row["b"]]
    # 견고성: 큰 충격의 해(1980·1998·2009·2020)를 빼고도 같은 시차의 상관이 남는지
    shock = {1980, 1998, 2009, 2020}
    for row in rows:
        if row["q"] >= 0.10:
            continue
        da, db, lag = data[row["a"]], data[row["b"]], row["lag"]
        ys = [y for y in da if (y + lag) in db and y not in shock and (y + lag) not in shock]
        r2 = _corr(np.array([da[y] for y in ys]), np.array([db[y + lag] for y in ys])) if len(ys) >= 8 else None
        row["rNoShock"] = None if r2 is None else round(r2, 3)
        row["robust"] = r2 is not None and abs(r2) >= 0.3 and (r2 > 0) == (row["r"] > 0)
    found = sorted([r for r in rows if r["q"] < 0.10], key=lambda r: (r["q"], -abs(r["r"])))
    near = sorted([r for r in rows if 0.10 <= r["q"] < 0.30], key=lambda r: r["q"])[:8]
    return {"tested": m, "indicators": len(ids), "perm": N_PERM, "found": found, "near": near,
            "method": "전년 대비 변화(직선 추세 제거)끼리 상관, 시차 −3~+3년 중 최대, 3년 묶음 순열 400회(시차 선택 포함), 벤자민-호크버그 q<0.10"}
