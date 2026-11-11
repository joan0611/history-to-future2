"""CYCLE DISCOVERY ENGINE — 실제 시계열에서 반복 후보를 '자동으로' 찾고 유형을 판정한다.

입력: indicators.py의 연간 시계열 전부(사람이 비교 대상을 지정하지 않음) + 신호 추적(문화 재등장).
출력 유형
  A 통계적 주기   — 여러 시차를 동시에 본 순열 검정과 주기도 검정을 모두 통과하고, 관측 기간 안에 3회 이상 반복될 때만
  B 불규칙한 반복 — 같은 종류의 '급변 구간'이 3번 이상 나타났지만 간격이 일정하지 않을 때(변동계수로 판단)
  C 구조적 유사성 — 두 지표를 함께 본 5년 구간끼리의 거리(정규화)로 가장 닮은 시기 쌍을 찾고, 무작위 구간 쌍 대비 순위를 함께 표시
  D 문화적 재유행 — 등장·확산·쇠퇴·재등장 단계가 근거로 확인된 흐름(수치 부족 → 정성적 유사성으로만)
  E 장기 구조 변화 — 직선 추세가 변동의 상당 부분을 설명하거나 평균이 한 번 크게 바뀐 경우(주기로 분류하지 않음)
원칙
- 장기 추세를 먼저 분리한 뒤 주기를 본다(추세가 가짜 주기를 만들지 않게).
- 여러 지표·여러 시차를 한꺼번에 보므로 '가장 큰 값'에 대한 순열 검정을 쓴다. 난수 시드 고정.
- 표본이 작으면(사건 3회 미만, 30년 미만) 주기를 판정하지 않는다.
- 분석 구간을 바꾼 결과(민감도)를 함께 저장한다.
- 양성·음성 대조군(인공 사인파·흰잡음·직선 추세)으로 엔진 자체를 검사한다(test_cycles.py).
"""
import numpy as np

SEED = 20261111
N_PERM = 2000


# ---------- 기본 계산 ----------
def detrend(t, y):
    b = np.polyfit(t, y, 1)
    fit = np.polyval(b, t)
    return y - fit, fit, b


def r2_trend(t, y):
    r, fit, _ = detrend(t, y)
    sst = ((y - y.mean()) ** 2).sum()
    return 0.0 if sst == 0 else float(1 - (r ** 2).sum() / sst)


def acf(r, k):
    return float(np.corrcoef(r[:-k], r[k:])[0, 1])


def periodicity(r, rng, max_lag=None, n_perm=N_PERM):
    """여러 시차·주파수를 한꺼번에 본 순열 검정. 반환: 가장 강한 시차/주기와 p값."""
    n = len(r)
    L = max_lag or max(2, min(20, n // 2 - 1))
    ac = [acf(r, k) for k in range(1, L + 1)]
    obs = max(abs(a) for a in ac)
    best_lag = int(np.argmax([abs(a) for a in ac]) + 1)
    null = np.array([max(abs(acf(p, k)) for k in range(1, L + 1)) for p in (rng.permutation(r) for _ in range(n_perm))])
    p_acf = float((null >= obs).mean())

    def share(x):
        P = np.abs(np.fft.rfft(x - x.mean())) ** 2
        P = P[1:]
        return P, P.max() / P.sum()
    P, sh = share(r)
    f = np.fft.rfftfreq(n)[1:]
    period = float(1 / f[int(P.argmax())])
    null_s = np.array([share(rng.permutation(r))[1] for _ in range(n_perm)])
    p_spec = float((null_s >= sh).mean())
    return {"acf": [round(a, 3) for a in ac], "bestLag": best_lag, "maxAbsAcf": round(obs, 3), "pAcf": round(p_acf, 3),
            "band": round(1.96 / np.sqrt(n), 3), "spectralPeriod": round(period, 1), "spectralShare": round(float(sh), 3), "pSpectral": round(p_spec, 3)}


def change_point(t, y):
    n = len(y)
    if n < 12:
        return None
    best = None
    for s in range(5, n - 5):
        sse = ((y[:s] - y[:s].mean()) ** 2).sum() + ((y[s:] - y[s:].mean()) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, s)
    sse0 = ((y - y.mean()) ** 2).sum()
    s = best[1]
    return {"year": int(t[s]), "before": round(float(y[:s].mean()), 2), "after": round(float(y[s:].mean()), 2),
            "explained": round(float(1 - best[0] / sse0), 3) if sse0 else 0.0}


def turning_points(t, y, k=1.0):
    """지그재그 방식: 3년 이동평균에서, 직전 극점 대비 표준편차의 k배 이상 되돌아섰을 때만 전환점으로 인정(작은 흔들림 제외)."""
    if len(y) < 7:
        return []
    sm = np.convolve(y, np.ones(3) / 3, mode="same")
    sm[0], sm[-1] = (y[0] + y[1]) / 2, (y[-1] + y[-2]) / 2
    thr = k * float(np.std(y))
    out, d = [], None
    hi = lo = ext = 0
    for i in range(1, len(sm)):
        if d is None:
            if sm[i] > sm[hi]:
                hi = i
            if sm[i] < sm[lo]:
                lo = i
            if sm[i] - sm[lo] >= thr:
                if lo > 0:
                    out.append(("trough", lo))
                d, ext = "up", i
            elif sm[hi] - sm[i] >= thr:
                if hi > 0:
                    out.append(("peak", hi))
                d, ext = "down", i
        elif d == "up":
            if sm[i] >= sm[ext]:
                ext = i
            elif sm[ext] - sm[i] >= thr:
                out.append(("peak", ext)); d, ext = "down", i
        else:
            if sm[i] <= sm[ext]:
                ext = i
            elif sm[i] - sm[ext] >= thr:
                out.append(("trough", ext)); d, ext = "up", i
    return [{"year": int(t[i]), "kind": k_, "value": round(float(y[i]), 2)} for k_, i in out]


def episodes(t, y, thr, above=True, min_gap=2):
    """임계값을 넘는 연속 구간(급변 구간). 간격 min_gap년 미만이면 하나로 묶는다."""
    hits = [int(a) for a, v in zip(t, y) if (v >= thr if above else v <= thr)]
    eps = []
    for yr in hits:
        if eps and yr - eps[-1][1] <= min_gap:
            eps[-1][1] = yr
        else:
            eps.append([yr, yr])
    return eps


def interval_stats(eps):
    starts = [e[0] for e in eps]
    gaps = np.diff(starts).tolist()
    if len(gaps) < 2:
        return {"starts": starts, "gaps": gaps, "cv": None, "regular": None}
    cv = float(np.std(gaps) / np.mean(gaps))
    return {"starts": starts, "gaps": gaps, "cv": round(cv, 2), "regular": cv < 0.2}


# ---------- 판정 ----------
def classify_series(t, y, rng):
    """한 시계열의 성격: E(장기 구조) / A(주기) / 없음. 근거 숫자를 함께 돌려준다."""
    n = len(y)
    res = {"n": n}
    if n < 20:
        res["verdict"] = "insufficient"
        res["why"] = f"관측치 {n}개 — 주기를 판정하기에 너무 짧음"
        return res
    r2 = r2_trend(t, y)
    cp = change_point(t, y)
    r, fit, b = detrend(t, y)
    per = periodicity(r, rng)
    res.update({"trendR2": round(r2, 3), "slopePerDecade": round(float(b[0]) * 10, 2), "changePoint": cp, "periodicity": per})
    cycles_seen = n / per["spectralPeriod"] if per["spectralPeriod"] else 0
    if per["pAcf"] < 0.05 and per["pSpectral"] < 0.05 and cycles_seen >= 3:
        res["verdict"] = "A"
        res["why"] = f"추세 제거 후 약 {per['spectralPeriod']}년 주기, 두 검정 모두 p<0.05, 관측 기간 안 {cycles_seen:.1f}회"
    elif r2 >= 0.3 or (cp and cp["explained"] >= 0.3):
        res["verdict"] = "E"
        res["why"] = (f"직선 추세가 변동의 {round(r2 * 100)}% 설명" if r2 >= 0.3 else f"{cp['year']}년 전후 평균이 {cp['before']}→{cp['after']}로 바뀜(변동의 {round(cp['explained'] * 100)}%)")
    else:
        res["verdict"] = "none"
        res["why"] = f"주기 검정 p={per['pAcf']}(시차)·{per['pSpectral']}(주기도) — 우연 범위, 뚜렷한 장기 추세도 없음"
    return res


def window_analogs(t, ys, w=5, top=3, rng=None):
    """여러 지표(정규화)로 w년 구간끼리 거리를 재서 가장 닮은 '서로 겹치지 않는' 구간 쌍을 찾는다.
    무작위 구간 쌍의 거리 분포에서 몇 % 위치인지(백분위)를 함께 준다 — 낮을수록 드물게 닮음."""
    Z = np.column_stack([(y - y.mean()) / y.std() for y in ys])
    n = len(t)
    wins = [(i, Z[i:i + w].ravel()) for i in range(0, n - w + 1)]
    pairs = []
    for a in range(len(wins)):
        for b in range(a + w, len(wins)):  # 겹치지 않게
            d = float(np.sqrt(((wins[a][1] - wins[b][1]) ** 2).mean()))
            pairs.append((d, wins[a][0], wins[b][0]))
    all_d = np.array([p[0] for p in pairs])
    pairs.sort()
    out, used = [], []
    for d, i, j in pairs:
        if any(abs(i - u) < w and abs(j - v) < w for u, v in used):
            continue
        used.append((i, j))
        out.append({"a": [int(t[i]), int(t[i + w - 1])], "b": [int(t[j]), int(t[j + w - 1])], "distance": round(d, 3),
                    "percentile": round(float((all_d <= d).mean()) * 100, 1)})
        if len(out) >= top:
            break
    return out, len(pairs)


def recent_analog(t, ys, w=5):
    """가장 최근 w년과 가장 닮은 과거 구간(겹치지 않게)."""
    Z = np.column_stack([(y - y.mean()) / y.std() for y in ys])
    n = len(t)
    last = Z[n - w:].ravel()
    cands = []
    for i in range(0, n - 2 * w + 1):
        d = float(np.sqrt(((Z[i:i + w].ravel() - last) ** 2).mean()))
        cands.append((d, i))
    all_d = np.array([c[0] for c in cands])
    cands.sort()
    return [{"past": [int(t[i]), int(t[i + w - 1])], "recent": [int(t[n - w]), int(t[-1])], "distance": round(d, 3),
             "percentile": round(float((all_d <= d).mean()) * 100, 1)} for d, i in cands[:3]]


def lag_corr(t1, y1, t2, y2, rng, lags=range(-3, 4)):
    lo, hi = max(t1[0], t2[0]), min(t1[-1], t2[-1])
    a = detrend(t1[(t1 >= lo) & (t1 <= hi)], y1[(t1 >= lo) & (t1 <= hi)])[0]
    b = detrend(t2[(t2 >= lo) & (t2 <= hi)], y2[(t2 >= lo) & (t2 <= hi)])[0]

    def cc(x, z, L):
        if L > 0:
            return float(np.corrcoef(x[:-L], z[L:])[0, 1])
        if L < 0:
            return float(np.corrcoef(x[-L:], z[:len(z) + L])[0, 1])
        return float(np.corrcoef(x, z)[0, 1])
    vals = [{"lag": L, "r": round(cc(a, b, L), 3)} for L in lags]
    obs = max(abs(v["r"]) for v in vals)
    null = np.array([max(abs(cc(a, rng.permutation(b), L)) for L in lags) for _ in range(N_PERM)])
    return {"from": int(lo), "to": int(hi), "values": vals, "maxAbs": round(obs, 3), "p": round(float((null >= obs).mean()), 3)}


def sensitivity(t, y, rng, windows):
    out = []
    for lo, hi in windows:
        m = (t >= lo) & (t <= hi)
        if m.sum() < 20:
            out.append({"range": [lo, hi], "n": int(m.sum()), "verdict": "insufficient"})
            continue
        c = classify_series(t[m], y[m], rng)
        out.append({"range": [lo, hi], "n": int(m.sum()), "verdict": c["verdict"], "trendR2": c.get("trendR2"),
                    "pAcf": c["periodicity"]["pAcf"], "pSpectral": c["periodicity"]["pSpectral"],
                    "period": c["periodicity"]["spectralPeriod"]})
    # 추세 제거 방식을 바꾸면? (직선 대신 1차 차분)
    d = np.diff(y)
    per = periodicity(d - d.mean(), rng)
    out.append({"range": [int(t[1]), int(t[-1])], "n": len(d), "method": "1차 차분(전년 대비 변화)", "verdict": "A" if per["pAcf"] < 0.05 and per["pSpectral"] < 0.05 else "none",
                "pAcf": per["pAcf"], "pSpectral": per["pSpectral"], "period": per["spectralPeriod"]})
    return out


# ---------- 엔진 ----------
def run(indicators, signals, graph_nodes):
    rng = np.random.default_rng(SEED)
    series = {}
    for ind in indicators:
        if ind["frequency"] != "annual":
            continue
        for s in ind["series"]:
            t = np.array([int(x) for x, _ in s["points"]])
            y = np.array([float(v) for _, v in s["points"]])
            series[f"{ind['id']}:{s['country']}"] = {"ind": ind, "s": s, "t": t, "y": y}

    analyses, findings = [], []
    for key, S in series.items():
        t, y, ind = S["t"], S["y"], S["ind"]
        contiguous = len(t) >= 2 and bool(np.all(np.diff(t) == 1))
        if len(t) < 20 or not contiguous:
            analyses.append({"key": key, "indicator": ind["id"], "country": S["s"]["country"], "title": ind["title"], "unit": ind["unit"],
                             "verdict": "insufficient", "why": f"관측 {len(t)}개{'' if contiguous else '·중간 연도 빠짐'} — 반복을 계산할 수 없음",
                             "n": len(t), "from": int(t[0]), "to": int(t[-1])})
            continue
        c = classify_series(t, y, rng)
        r, fit, _ = detrend(t, y)
        # 장기 추세가 강하면(E) 원값이 아니라 '추세 대비' 이탈로 급변 구간을 찾는다 — 추세를 반복으로 오인하지 않게
        base = r if c.get("trendR2", 0) >= 0.3 else y - y.mean()
        sd = float(np.std(base))
        rel = c.get("trendR2", 0) >= 0.3
        ep_hi = episodes(t, base, sd, True)
        ep_lo = episodes(t, base, -sd, False)
        hi_thr = round(float((y.mean() if not rel else 0) + sd), 2)
        lo_thr = round(float((y.mean() if not rel else 0) - sd), 2)
        sens = sensitivity(t, y, rng, [(1960, 1992), (1993, 2025), (1980, 2025)])
        a = {"key": key, "indicator": ind["id"], "country": S["s"]["country"], "title": ind["title"], "unit": ind["unit"],
             "from": int(t[0]), "to": int(t[-1]), "points": [[int(a_), round(float(b_), 2)] for a_, b_ in zip(t, y)],
             "trend": [[int(t[0]), round(float(fit[0]), 2)], [int(t[-1]), round(float(fit[-1]), 2)]],
             "turningPoints": turning_points(t, y), "highThreshold": hi_thr, "lowThreshold": lo_thr, "episodeBasis": "추세 대비" if rel else "평균 대비",
             "residual": [[int(a_), round(float(b_), 2)] for a_, b_ in zip(t, r)],
             "highEpisodes": ep_hi, "lowEpisodes": ep_lo, "highIntervals": interval_stats(ep_hi), "lowIntervals": interval_stats(ep_lo),
             "sensitivity": sens, **c}
        analyses.append(a)

    A = {x["key"]: x for x in analyses}

    def add(f):
        findings.append(f)

    # 1) 지표별 성격(E 또는 '주기 없음' 또는 A)
    for x in analyses:
        if x["verdict"] in ("E", "A"):
            add({"id": f"f-{x['key']}-shape", "type": x["verdict"], "series": [x["key"]], "category": x_cat(x),
                 "title": (f"{x['title']}({country_ko(x['country'])}): " + ("장기 구조 변화 — 주기가 아님" if x["verdict"] == "E" else "통계적 주기")),
                 "summary": x["why"], "periods": [[x["changePoint"]["year"], x["to"]]] if x["verdict"] == "E" and x["changePoint"] else [],
                 "evidence": {"trendR2": x["trendR2"], "changePoint": x["changePoint"], "pAcf": x["periodicity"]["pAcf"], "pSpectral": x["periodicity"]["pSpectral"]}})
        elif x["verdict"] == "none" and x["n"] >= 30:
            add({"id": f"f-{x['key']}-nocycle", "type": "N", "series": [x["key"]], "category": x_cat(x),
                 "title": f"{x['title']}({country_ko(x['country'])}): 일정한 주기 없음", "summary": x["why"], "periods": [],
                 "evidence": {"pAcf": x["periodicity"]["pAcf"], "pSpectral": x["periodicity"]["pSpectral"], "bestLag": x["periodicity"]["bestLag"]}})

    # 2) 급변 구간의 반복(B): 높은 쪽·낮은 쪽 각각
    for x in analyses:
        if x["verdict"] == "insufficient":
            continue
        for side, eps, st, thr in (("high", x["highEpisodes"], x["highIntervals"], x["highThreshold"]),
                                   ("low", x["lowEpisodes"], x["lowIntervals"], x["lowThreshold"])):
            if len(eps) < 3:
                continue
            reg = st["regular"]
            add({"id": f"f-{x['key']}-{side}", "type": "A" if reg and x["verdict"] == "A" else "B", "series": [x["key"]], "category": x_cat(x),
                 "title": f"{x['title']}({country_ko(x['country'])}) {'급등' if side == 'high' else '급락'} 구간 {len(eps)}회",
                 "summary": (f"추세선보다 1표준편차({thr}%p) 이상 {'높았던' if side == 'high' else '낮았던'} 구간: " if x["episodeBasis"] == "추세 대비" else f"평균±1표준편차({thr}{x['unit']}) 밖으로 나간 구간: ") + ", ".join(f"{a}" if a == b else f"{a}~{b}" for a, b in eps)
                 + f". 간격 {', '.join(map(str, st['gaps']))}년 — 변동계수 {st['cv']}"
                 + (" (간격이 비교적 일정하지만 횟수가 적어 주기로 확정하지 않음)" if reg else " → 간격이 일정하지 않은 불규칙한 반복"),
                 "periods": eps, "intervals": st["gaps"], "evidence": {"threshold": thr, "basis": x["episodeBasis"], "cv": st["cv"], "count": len(eps)}})

    # 3) 구조적 유사성(C): 한국 성장률·물가를 함께 본 5년 구간
    if "gdp-growth:KR" in A and "cpi-kr:KR" in A:
        g, p = series["gdp-growth:KR"], series["cpi-kr:KR"]
        lo, hi = max(g["t"][0], p["t"][0]), min(g["t"][-1], p["t"][-1])
        mg, mp = (g["t"] >= lo) & (g["t"] <= hi), (p["t"] >= lo) & (p["t"] <= hi)
        t = g["t"][mg]
        an, npairs = window_analogs(t, [g["y"][mg], p["y"][mp]], w=5, top=4, rng=rng)
        rec = recent_analog(t, [g["y"][mg], p["y"][mp]], w=5)
        rec_pair = (tuple(rec[0]["past"]), tuple(rec[0]["recent"]))
        for i, x in enumerate([x for x in an if (tuple(x["a"]), tuple(x["b"])) != rec_pair]):
            add({"id": f"f-analog-{i}", "type": "C", "series": ["gdp-growth:KR", "cpi-kr:KR"], "category": "economy",
                 "title": f"닮은 5년: {x['a'][0]}~{x['a'][1]} ↔ {x['b'][0]}~{x['b'][1]} (성장률+물가)",
                 "summary": f"두 지표를 각각 표준화한 5년 궤적의 거리 {x['distance']}. 겹치지 않는 구간 쌍 {npairs}개 중 하위 {x['percentile']}% — 숫자 모양이 닮았다는 뜻이지 원인이 같다는 뜻은 아님",
                 "periods": [x["a"], x["b"]], "evidence": x})
        add({"id": "f-recent-analog", "type": "C", "series": ["gdp-growth:KR", "cpi-kr:KR"], "category": "economy",
             "title": f"최근 5년({rec[0]['recent'][0]}~{rec[0]['recent'][1]})과 가장 닮은 과거: {rec[0]['past'][0]}~{rec[0]['past'][1]}",
             "summary": f"거리 {rec[0]['distance']} (과거 구간 중 하위 {rec[0]['percentile']}%). 2·3위: " + ", ".join(f"{r['past'][0]}~{r['past'][1]}" for r in rec[1:]),
             "periods": [rec[0]["past"], rec[0]["recent"]], "evidence": {"candidates": rec}, "current": True})
        lc = lag_corr(g["t"], g["y"], p["t"], p["y"], rng)
        best = max(lc["values"], key=lambda v: abs(v["r"]))
        add({"id": "f-lag-gdp-cpi", "type": "R", "series": ["gdp-growth:KR", "cpi-kr:KR"], "category": "economy",
             "title": "성장률과 물가: 시차 관계" + (" — 우연 범위" if lc["p"] >= 0.05 else ""),
             "summary": f"추세를 뺀 두 지표의 상관이 가장 큰 시차는 {best['lag']}년(r={best['r']}). 시차 7개를 함께 본 순열 검정 p={lc['p']}. 상관이 있어도 인과를 뜻하지 않음",
             "periods": [], "evidence": lc})

    # 4) 문화적 재유행(D): 근거로 확인된 단계 흐름에서 '재등장'이 있는 것
    for s in signals:
        stages = [st.get("stage", "") for st in s["steps"]]
        if any("재등장" in x for x in stages):
            years = []
            for st in s["steps"]:
                n = graph_nodes.get(st.get("nodeId", ""))
                years.append(n["year"] if n else None)
            first, back = years[0], years[stages.index(next(x for x in stages if "재등장" in x))]
            n0 = graph_nodes.get(s["steps"][0].get("nodeId", ""))
            first_txt = f"{first // 10 * 10}년대" if n0 and n0.get("yearPrecision") == "era" else f"{first}년"
            add({"id": f"f-{s['id']}", "type": "D", "series": [], "category": "culture", "title": f"{s['title']}",
                 "summary": f"등장({first_txt}) → 대중화 → 쇠퇴 → 재등장({back}). 재등장 사례가 1개라 간격({back - first}년 안팎)을 주기로 볼 수 없음 — 정성적 유사성",
                 "periods": [[first, first + 9], [back, back + 1]], "intervals": [back - first], "signal": s["id"], "evidence": {"stages": stages}})

    # 점수: 흥미(새로움·연결) 와 신뢰도(통계 근거)를 따로
    for f in findings:
        f["confidence"] = confidence(f, A)
        f["interest"] = interest(f)
    findings.sort(key=lambda f: (-f["interest"], CONF_RANK[f["confidence"]["level"]]))
    return {"analyses": analyses, "findings": findings, "params": {"permutations": N_PERM, "seed": SEED, "episodeRule": "평균±1표준편차, 2년 이내 이웃은 한 구간",
            "windowYears": 5}}


CONF_RANK = {"높음": 0, "보통": 1, "낮음": 2}


def confidence(f, A):
    t = f["type"]
    if t == "A":
        return {"level": "보통", "why": "검정은 통과했지만 60여 년 자료로는 반복 횟수가 적음"}
    if t == "E":
        e = f["evidence"]
        return {"level": "높음" if (e.get("trendR2") or 0) >= 0.4 or (e.get("changePoint") or {}).get("explained", 0) >= 0.4 else "보통",
                "why": "추세·변화점의 설명력 기준"}
    if t == "N":
        return {"level": "높음", "why": "주기가 '없다'는 판단은 순열 검정 결과가 직접 뒷받침"}
    if t == "B":
        c = (f["evidence"] or {}).get("count", 0)
        return {"level": "보통" if c >= 4 else "낮음", "why": f"급변 구간 {c}회 — 횟수가 적을수록 간격 판단이 불안정"}
    if t == "C":
        pc = (f["evidence"] or {}).get("percentile", (f["evidence"].get("candidates") or [{}])[0].get("percentile", 50) if f["evidence"] else 50)
        return {"level": "보통" if pc <= 1 else "낮음", "why": f"닮은 정도가 무작위 구간 쌍의 하위 {pc}% — 지표 2개·5년 구간만 사용"}
    if t == "R":
        p = f["evidence"]["p"]
        return {"level": "보통" if p < 0.01 else "낮음", "why": f"시차 7개를 함께 본 순열 검정 p={p}. 상관일 뿐 인과가 아님"}
    return {"level": "낮음", "why": "수치가 아닌 기록(단계)만 있어 정성적 유사성"}


def interest(f):
    base = {"C": 3, "B": 3, "D": 2.5, "E": 2, "A": 4, "N": 1, "R": 1.5}[f["type"]]
    if f.get("current"):
        base += 1.5
    if "급등" in f["title"] and "물가" in f["title"]:
        base += 1
    return round(base + 0.1 * len(f.get("periods", [])), 2)


def country_ko(c):
    return {"KR": "한국", "US": "미국", "JP": "일본"}.get(c, c)


def x_cat(x):
    return {"gdp-growth": "economy", "cpi-kr": "economy", "tfr-kr": "society", "one-person-kr": "society", "online-kr": "society",
            "pcbang-kr": "industry", "oil-dep-kr": "economy"}.get(x["indicator"], "economy")
