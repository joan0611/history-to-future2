"""연결이 하나도 없던 사건을 근거 문장이 뒷받침하는 범위에서만 잇는다.

- 사건과 그 사건이 만든 생활 변화(같은 근거 문장을 쓰는 '트렌드' 항목)는 근거 문장이 직접 말하는 경우만 cause/evidenced.
- 같은 시기에 함께 보도됐을 뿐이면 statistical(함께 움직임), 순서만 맞으면 sequence, 비교일 뿐이면 similar.
- 근거로 이을 수 없는 사건은 억지로 잇지 않고 그대로 둔다(화면에 '연결 근거 없음'으로 보인다).
"""


def E(a, b, rel, ver, cids, note):
    return {"from": a, "to": b, "rel": rel, "verification": ver, "claimIds": cids, "note": note}


CHAIN = {"id": "links-extra", "title": "근거로 확인한 사건—생활 변화 연결", "eraId": "1980s"}
NODES = []

EDGES = [
    # 1960년대
    E("e60-export", "e70-hci", "background", "interpretation", ["c60-kr-export-1", "c70-hci-why"],
      "경공업 중심 수출 구조의 무역적자가 중화학공업화의 배경으로 꼽힌다(국가기록원)."),
    E("e60-refinery", "n-1960s-자동차-석유화학-정유-확대-1960s", "influence", "evidenced", ["c60-kr-refinery-1", "c60-syn-oil"],
      "정유공장 건설은 1960년대 석유 수요 확대의 한 축이었다."),
    E("tr-t60-car", "tr-t70-mycar", "similar", "interpretation", ["c60-us-car-1", "c70-pony-1"],
      "미국의 1960년대 자동차 중심 생활과 한국의 1970년대 후반 '마이카' 시작 — 시기와 규모가 다른 비교."),
    E("tr-t60-appliance", "e60-tv", "sequence", "evidenced", ["c60-kr-firsts", "c60-kr-tv-1"],
      "선풍기·전화기·냉장고에 이어 첫 국산 흑백TV가 나왔다 — 순서일 뿐 인과는 아니다."),
    E("e60-tv", "tr-t60-tv", "cause", "evidenced", ["c60-kr-tv-1", "c60-hyp-kr-ad"], "국산 흑백TV 출시 — 공개 추첨 판매와 국산품 자부심."),
    E("e60-tv", "e80-colortv", "background", "evidenced", ["c80-colortv"],
      "1979년 흑백TV 보급률이 이미 90%였던 것이 컬러 전환의 바탕이었다."),
    # 1970년대
    E("e70-saemaul", "tr-t70-village", "cause", "evidenced", ["c70-saemaul"], "새마을운동 제창과 마을 시멘트 지원."),
    E("d-embargo", "tr-t70-saving", "cause", "evidenced", ["c70-ch-order"], "석유 공급 감축에 따른 정부의 유류절감 명령."),
    E("d-embargo", "n-1970s-값싼-석유를-전제로-짜인-1960년대-성장-모델이-1973년에-깨지자", "cause", "interpretation", ["c70-syn-chain"],
      "석유 충격 이후 각국의 대응(절약·비축·대체 에너지)을 묶은 해석."),
    E("e70-pony", "tr-t70-mycar", "cause", "evidenced", ["c70-pony-1", "c70-pony-2", "c70-hyp-pony-ad"], "첫 고유모델 승용차 판매."),
    # 1980년대
    E("e80-518", "e80-629", "background", "interpretation", ["c80-518-legacy"],
      "5·18 진상 규명 요구가 1980년대 민주화운동과 이어졌다."),
    E("e80-colortv", "tr-t80-color", "cause", "evidenced", ["c80-colortv", "c80-vtr", "c80-hyp-ad"], "컬러 방송 시작과 컬러TV 광고."),
    E("n-1980s-반도체-엔지니어-연구원-수요", "e80-64k", "background", "interpretation", ["c80-rnd"],
      "기업 연구소와 민간 R&D가 늘어난 것이 반도체 개발 인력의 바탕이었다는 해석."),
    E("e80-curfew", "tr-t80-night", "cause", "evidenced", ["c80-curfew", "c80-ch-24h"], "통금 해제로 '24시간 생활'."),
    E("e80-baseball", "tr-t80-night", "influence", "evidenced", ["c80-baseball"], "프로야구 개막."),
    E("tr-t80-travel", "e80-travel", "sequence", "evidenced", ["c80-travel"], "1983년 50세 이상 제한 허용 → 1989년 전면 자유화."),
    E("n-1980s-일본-제품-가격-상승-한국-수출-호황-3저", "tr-t80-stock", "influence", "statistical", ["c80-ch-boom"],
      "수출 흑자와 주가 폭등이 같은 시기 지면에 함께 실렸다 — 함께 움직였을 뿐 인과는 확인하지 않았다."),
    # 1990년대
    E("e90-seongsu", "tr-t90-safety", "cause", "evidenced", ["c90-seongsu"], "15년간 정밀 안전검사가 없었다는 보도."),
    E("e90-seongsu", "e90-sampoong", "similar", "interpretation", ["c90-seongsu", "c90-sampoong"],
      "8개월 사이 이어진 대형 붕괴 — 둘 다 전조가 있었는데도 안전 조치가 없었다는 공통점(비교이며 같은 원인이라는 뜻은 아니다)."),
    E("e90-cdma", "tr-t90-mobile", "cause", "evidenced", ["c90-cdma", "c90-hyp-ad"], "CDMA 상용화 첫해 단말기 약 100만 대, '한국 지형에 강하다' 광고."),
    E("e90-imf", "tr-t90-gold", "trigger", "evidenced", ["c90-gold"], "외환위기 속 금 모으기 운동."),
    E("e90-imf", "n-1990s-노사정위원회-파견근로-허용-실업률-6-8", "cause", "evidenced", ["c90-ch-1998"],
      "구제금융 이후 노사정위원회 발족·파견근로 허용."),
    # 2000년대
    E("e00-worldcup", "tr-t00-street", "cause", "evidenced", ["c00-worldcup"], "길거리 응원 인파 52만 → 700만 명."),
    E("tr-t00-hallyu", "tr-t10-kpop", "sequence", "interpretation", ["c00-hallyu", "c10-psy"],
      "드라마 중심 한류 다음에 유튜브로 퍼진 K팝 — 순서이며 직접 인과는 확인하지 않았다."),
    E("e00-5day", "tr-t00-weekend", "cause", "evidenced", ["c00-5day-leisure"], "주5일제를 여가·가족생활의 전환점으로 본 국가기록원 평가."),
    E("e00-5day", "e10-minwage", "sequence", "evidenced", ["c00-5day", "c10-52h"], "근로시간 단축의 다음 단계(주 52시간)."),
    E("tr-t00-minihompy", "tr-t10-messenger", "influence", "interpretation", ["c00-cy-decline"],
      "스마트폰으로 무게중심이 옮겨 가며 PC 기반 미니홈피의 전성기가 끝났다는 해석."),
    E("e90-un", "e90-china", "sequence", "evidenced", ["cfill-un", "cfill-china"],
      "1991년 유엔 동시 가입 다음 해 한중 수교 — 순서이며 인과는 확인하지 않았다."),
    E("e00-kosdaq", "claim:c20-kr-chip", "similar", "interpretation", ["c00-kosdaq", "c00-sd-venture", "c20-kr-chip"],
      "새 기술 확산기의 투자 열기라는 비교(‘반복·비교’의 인터넷 벤처 붐 ↔ AI 투자) — 같은 결말을 뜻하지 않는다."),
    # 2010년대 이후
    E("e10-kakao", "tr-t10-messenger", "cause", "evidenced", ["c10-kakao"], "카카오톡 출시와 가입자 급증."),
    E("n-2010s-배달앱-이용자-87만-2-500만", "tr-t10-delivery", "cause", "evidenced", ["c10-delivery"], "배달앱 이용자 87만 → 2,500만 명."),
    E("tr-t20-home", "n-2020s-아파트값-2021년-18-2022년-7", "sequence", "evidenced", ["c20-house"],
      "집에 머무는 생활이 늘던 시기 아파트값 급등 뒤 하락 — 순서이며 인과는 근거로 확인하지 않았다."),
    E("tr-t10-candle", "e10-candle", "sequence", "evidenced", ["c10-candle"], "134일 촛불집회 → 헌법재판소 파면 결정."),
    E("tr-t90-safety", "e10-sewol", "similar", "interpretation", ["c90-sampoong", "c10-sewol"],
      "대형 참사가 안전 관리 문제를 다시 드러냈다는 비교 — 원인이 같다는 뜻은 아니다."),
    E("e80-518", "e20-martial", "similar", "interpretation", ["c80-518", "c20-martial"],
      "비상계엄 선포라는 공통점이 있지만 경과는 다르다 — 1980년은 무력 진압, 2024년은 국회 해제 의결과 헌법재판소 파면."),
]
