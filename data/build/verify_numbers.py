"""문장 속 숫자를 수집한 장기 지표(FRED·WDI)와 자동 대조한다.

- 대조할 숫자는 사람이 문장에서 골라 아래 표에 적는다(정규식 추출로 엉뚱한 숫자를 비교하지 않게).
- 차이가 허용 범위를 넘으면 '차이'로 표시하고 이유를 적는다. 문장을 몰래 고치지 않는다.
  (예: 성장률은 한국은행 국민계정 기준연도가 여러 번 개편돼 옛 자료의 값과 현재 계열이 다르다)
"""

# (claim, indicator, country, year, 문장 속 값, 허용 오차, 메모)
CHECKS = [
    ("c70-kr-cpi", "cpi-kr", "KR", 1974, 24, 0.6, ""),
    ("c70-kr-cpi", "cpi-kr", "KR", 1975, 25, 0.6, ""),
    ("c70-kr-growth", "gdp-growth", "KR", 1973, 12.3, 0.6, "문장의 값은 옛 국민계정(개편 전) 집계로 보임"),
    ("c70-kr-growth", "gdp-growth", "KR", 1974, 7.4, 0.6, "문장의 값은 옛 국민계정(개편 전) 집계로 보임"),
    ("c70-kr-growth", "gdp-growth", "KR", 1976, 11.2, 0.6, "문장의 값은 옛 국민계정(개편 전) 집계로 보임"),
    ("c70-kr-2nd", "gdp-growth", "KR", 1980, -5.2, 0.6, "문장의 값은 옛 국민계정(개편 전) 집계로 보임"),
    ("c70-kr-2nd", "cpi-kr", "KR", 1980, 30, 1.5, "문장은 '30%에 이르렀다'(어림값)"),
    ("c90-unemp", "unemp-kr", "KR", 1997, 2.6, 0.2, ""),
    ("c90-unemp", "unemp-kr", "KR", 1998, 6.8, 0.2, "통계청 연평균과 OECD 계절조정 연평균의 차이"),
    ("c90-growth98", "gdp-growth", "KR", 1998, -6.9, 0.6, "문장이 이미 '현재 기준치(약 -5%대)와 다르다'고 밝힘"),
    ("c10-tfr", "tfr-kr", "KR", 2018, 0.98, 0.01, ""),
    ("c20-pop", "tfr-kr", "KR", 2023, 0.72, 0.01, ""),
    ("c20-pop", "tfr-kr", "KR", 2024, 0.75, 0.01, ""),
    ("c60-kr-export-1", "exports-kr", "KR", 1964, 1.0, None, "문장: 1964년 수출 1억 달러 돌파 → 연간 값이 1억 달러 이상인지 확인"),
    ("c20-kr-chip", "exports-kr", "KR", 2025, 7097, 0.01, "상대 오차 1% (통관 기준과 OECD 집계 차이)"),
]


def bok_growth(year):
    import indicators_ecos as E
    return E.BOK_GROWTH.get(year)


def run(indicators):
    I = {i["id"]: i for i in indicators}
    out = {}
    for cid, ind, cc, year, claimed, tol, memo in CHECKS:
        s = next(s for s in I[ind]["series"] if s["country"] == cc)
        v = next((p[1] for p in s["points"] if p[0] == str(year)), None)
        if v is None:
            res = {"ok": None, "verdict": "대조 자료 없음"}
        elif tol is None:  # '넘었다' 형식
            res = {"ok": v >= claimed, "verdict": "일치" if v >= claimed else "차이"}
        else:
            lim = tol * abs(claimed) if ind == "exports-kr" and tol < 0.1 else tol
            ok = abs(v - claimed) <= lim
            res = {"ok": ok, "verdict": "일치" if ok else "차이"}
        if ind == "gdp-growth":
            b = bok_growth(year)
            memo = (f"한국은행 현재 국민계정(ECOS 실질 GDP) 기준 {b}%와 비교. " if b is not None else "") + memo
        out.setdefault(cid, []).append({"indicator": ind, "title": I[ind]["title"], "year": year, "claimed": claimed, "data": v,
                                        "unit": I[ind]["unit"], "memo": memo, **res})
    return out
