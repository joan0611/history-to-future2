"""사이클 엔진 대조 검사 — 있는 주기는 찾고, 없는 주기는 만들지 않으며, 추세를 주기로 착각하지 않는지."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "data", "build"))
import cycles as cy  # noqa: E402

T = np.arange(1960, 2026)


def rng():
    return np.random.default_rng(7)


def test_finds_real_cycle():  # 양성 대조: 8년 주기 + 잡음
    y = 3 * np.sin(2 * np.pi * (T - 1960) / 8) + rng().normal(0, 0.8, len(T))
    c = cy.classify_series(T, y, rng())
    assert c["verdict"] == "A", c
    assert 7 <= c["periodicity"]["spectralPeriod"] <= 9


def test_no_cycle_in_noise():  # 음성 대조: 흰잡음 20개 중 거짓 주기 판정은 드물어야
    false = 0
    for s in range(20):
        y = np.random.default_rng(100 + s).normal(0, 1, len(T))
        if cy.classify_series(T, y, np.random.default_rng(s))["verdict"] == "A":
            false += 1
    assert false <= 2, false


def test_trend_is_not_cycle():  # 장기 추세는 E(구조 변화), A(주기)가 아님
    y = 10 - 0.15 * (T - 1960) + rng().normal(0, 1, len(T))
    c = cy.classify_series(T, y, rng())
    assert c["verdict"] == "E", c


def test_short_series_refused():
    c = cy.classify_series(T[:12], np.arange(12.0), rng())
    assert c["verdict"] == "insufficient"


def test_episodes_and_intervals():
    y = np.zeros(len(T)); y[[4, 14, 15, 30]] = 5
    eps = cy.episodes(T, y, 2.5)
    assert eps == [[1964, 1964], [1974, 1975], [1990, 1990]]
    st = cy.interval_stats(eps)
    assert st["gaps"] == [10, 16] and st["regular"] is False


def test_turning_points_found():
    y = np.concatenate([np.linspace(0, 10, 20), np.linspace(10, 0, 20), np.linspace(0, 10, 26)])
    tp = cy.turning_points(T, y)
    kinds = [p["kind"] for p in tp]
    assert "peak" in kinds and "trough" in kinds


def test_sensitivity_reports_windows():
    y = rng().normal(0, 1, len(T))
    sens = cy.sensitivity(T, y, rng(), [(1960, 1992), (1993, 2025), (2015, 2025)])
    assert [s["range"] for s in sens[:3]] == [[1960, 1992], [1993, 2025], [2015, 2025]]
    assert sens[2]["verdict"] == "insufficient" and "1차 차분" in sens[-1]["method"]


def test_real_data_findings_exist_and_are_honest():
    import json
    d = json.load(open(os.path.join(os.path.dirname(__file__), "..", "data", "seed.json")))["cycles"]
    types = {f["type"] for f in d["findings"]}
    assert {"B", "C", "D", "E"} <= types
    # 한국 성장률·물가는 추세가 강하므로 주기(A)로 판정되면 안 된다
    v = {a["key"]: a["verdict"] for a in d["analyses"]}
    assert v["gdp-growth:KR"] != "A" and v["cpi-kr:KR"] != "A"
    # 짧은 시계열은 계산을 거부
    assert v["one-person-kr:KR"] == "insufficient" and v["pcbang-kr:KR"] == "insufficient"
    # 출산율(1960~)은 뚜렷한 장기 하락 → 주기가 아니라 구조 변화(E)
    assert v["tfr-kr:KR"] == "E"
    # 강한 추세 지표의 급변 구간은 '전년 대비 변화' 기준이어야 한다(직선 잔차의 곡선 오차를 반복으로 오인하지 않게)
    basis = {a["key"]: a.get("episodeBasis") for a in d["analyses"]}
    assert basis["fx-kr:KR"] == "전년 대비 변화율" and basis["life-kr:KR"] == "전년 대비 변화"
    for f in d["findings"]:
        assert f["confidence"]["level"] in ("높음", "보통", "낮음") and f["summary"]
