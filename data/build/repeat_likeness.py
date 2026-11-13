"""반복의 성격 판정(지시서 8: 사이클 — 외형이 닮은 것과 발생 원리가 닮은 것을 구분) — 20차.
겉모습만 닮음: 겉으로 보이는 모양·숫자는 같지만 그것을 낳은 동기·원인이 다르다.
원리도 닮음: 같은 동기·조건이 같은 방향의 결과를 다시 낳았다.
반복 아님: 되풀이처럼 보이지만 한 방향으로 가는 변화다.
판정은 각 반복의 '닮은 점'·'달라진 것' 문장을 읽고 내린 AI 판단이며 화면에도 그렇게 밝힌다."""

LIKE = {
    ('topic', 'shop-channel', '편리함(가까움·빠름)과 싸게 많이 사기 사이의 긴장'): '원리도 닮음',
    ('topic', 'shop-pay', '외상이 돌아왔다 — 가게 장부 → 회원카드 → 신용카드 → 후불결제'): '원리도 닮음',
    ('topic', 'shop-own', '중고 거래 — 1998년 아나바다 장터와 2020년대 동네 앱'): '겉모습만 닮음',
    ('topic', 'shop-own', "렌탈 — 할부가 '관리 서비스'를 입다"): '원리도 닮음',
    ('topic', 'shop-items', '엥겔계수 30% — 1994년과 2025년'): '겉모습만 닮음',
    ('topic', 'shop-items', '물가가 오를 때마다 식비가 앞으로 — 2008~2011, 2020~2025'): '원리도 닮음',
    ('topic', 'shop-info', '믿을 만한 추천과 돈 받은 추천 — 블로그(2011) · 영상(2020) · AI(2026)'): '원리도 닮음',
    ('topic', 'life-record', '종이에 쓰는 붐 — 2015년 다이어리 붐과 2024년 필사 열풍'): '겉모습만 닮음',
    ('topic', 'life-record', '종이책 읽기의 감소 — 되풀이가 아니라 한 방향'): '반복 아님',
    ('topic', 'life-stuff', '쓰기와 아끼기 — 2017년 욜로와 2022년 무지출'): '겉모습만 닮음',
    ('topic', 'life-alone', '혼자 하기의 자유 ↔ 외로움의 공공 문제화'): '원리도 닮음',
    ('topic', 'life-convenience', '빠른 출점 → 과잉 → 정리'): '원리도 닮음',
    ('topic', 'media-screen', '거실의 큰 화면'): '겉모습만 닮음',
    ('topic', 'media-game', "새 게임이 나올 때마다 붙는 '청소년 문제' 시선"): '원리도 닮음',
    ('topic', 'travel-abroad', '충격 때 가장 먼저 줄고 가장 먼저 돌아오는 지출'): '겉모습만 닮음',
    ('topic', 'work-style', '고용 계약이 짧고 느슨해지는 방향'): '원리도 닮음',
    ('topic', 'money-invest', '해외 투자 열풍'): '원리도 닮음',
    ('topic', 'food-cafe', '편리한 싼 커피와 머무는 비싼 커피'): '원리도 닮음',
    ('topic', 'fashion-beauty', '여러 브랜드를 한곳에 — 백화점에서 편집숍으로'): '원리도 닮음',
    ('topic', 'media-fandom', '기념품을 사는 팬'): '원리도 닮음',
    ('topic', 'family-care', '가족에서 제도로 넘어가는 돌봄'): '원리도 닮음',
    ('topic', 'food-hmr', '시간을 아끼기 ↔ 직접 만든 밥'): '원리도 닮음',
    ('topic', 'work-learn', '막으면 숨고, 풀면 퍼진다'): '원리도 닮음',
    ('topic', 'money-save', '위기에 모으고, 지나면 쓴다'): '겉모습만 닮음',
    ('topic', 'money-home', '저금리 → 빚 → 집값 → 규제·금리 인상'): '원리도 닮음',
    ('topic', 'fashion-shoes', '비싼 해외 브랜드와 그 대안'): '겉모습만 닮음',
    ('topic', 'fashion-hair', '풀었다가 다시 묶는 학교 규칙'): '원리도 닮음',
    ('topic', 'food-dessert', '단맛을 원하면서 단맛을 걱정한다'): '원리도 닮음',
    ('topic', 'goods-collect', '포켓몬빵 띠부띠부씰'): '원리도 닮음',
    ('topic', 'travel-stay', '방을 채워 주는 중개자와 그 값'): '원리도 닮음',
    ('topic', 'money-insure', '보장을 줄여 보험료를 낮춘다'): '원리도 닮음',
    ('topic', 'work-cert', '위기가 오면 훈련을 늘린다?'): '겉모습만 닮음',
    ('topic', 'hobby-place', '줄어드는 방은 다른 놀이를 붙인다'): '원리도 닮음',
    ('topic', 'tech-home', '외국 기술과 국산 가전'): '원리도 닮음',
    ('topic', 'space-tableware', '정부가 집 안 물건을 바꾼다'): '원리도 닮음',
    ('topic', 'energy-power', '수입 에너지에 기대면서 자립을 꿈꾼다'): '원리도 닮음',
    ('topic', 'policy-welfare', '넓히기는 쉽고 부담 늘리기는 어렵다'): '원리도 닮음',
    ('topic', 'world-trade', '수출 시장을 얻는 대가로 안방을 연다'): '원리도 닮음',
    ('flow', 'flow-music', '1960년대 세시봉 음악이 2010년 TV로 다시 유행'): '겉모습만 닮음',
    ('flow', 'flow-expression', '교복 자율화 3년 뒤 다시 교복으로 — 자유의 불편이 되돌림을 부르다'): '겉모습만 닮음',
}


def apply(seed):
    groups = [("topic", seed["topics"]["topics"]), ("taste", seed["tastes"]["flows"]), ("flow", seed["flows"]["flows"])]
    n, miss = 0, []
    for kind, objs in groups:
        for o in objs:
            for r in o.get("repeats") or []:
                v = LIKE.get((kind, o["id"], r["title"]))
                if v:
                    r["likeness"] = v
                    n += 1
                else:
                    miss.append(f"{kind}:{o['id']}:{r['title']}")
    seed["repeatLikeness"] = {"filled": n, "missing": miss}
    return seed
