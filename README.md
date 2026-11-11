# HISTORY TO FUTURE 2.0

대한민국 1960년부터 현재까지의 변화를 **넓게(전체 흐름) → 분야별(수십 년 동향) → 깊게(원인과 결과)** 탐색하고, 데이터에서 **반복과 유사성을 자동으로 찾아내는** 웹사이트입니다.

- 웹사이트: https://joan0611.github.io/history-to-future2/
- 이전 사이트(그대로 보존): https://joan0611.github.io/history-to-future/

## 화면
| 진입점 | 내용 |
|---|---|
| 전체 역사 | 공통 시간축(1960~2026 모든 연도) · 전체/10년/1년 보기 · 장기 그래프 · 변화 지도(분야×시대) · 시대별 주요 사건 |
| 분야별 변화 | 분야를 고르면 1960~현재 대표 그래프(또는 생애 막대)부터 · 자동 탐지 전환점 · 시대별 단계 · 선택 시기 사건 · 이 분야의 자동 발견 |
| 사이클 발견 | 엔진이 지정 없이 모든 연간 지표를 분석한 결과 — 유형(통계적 주기·불규칙 반복·구조적 유사·문화 재유행·장기 구조 변화·주기 없음·지표 간 관계)과 신뢰도 분리 표시, 원본·구간·간격·겹쳐 보기·조건 비교·민감도 |
| 원인·결과(공통 패널) | 어디서든 항목을 누르면 열림. 관계 유형(직접 원인·구조적 배경·촉발·영향·시간적 선후·유사)과 검증 수준(근거 있는 인과·해석·가설) 구분, 1960년 이전 배경까지 |

주소에 모든 상태가 들어 있습니다: `#/history?z=decade&y=1990`, `#/field/economy?y=1980&ind=cpi-kr`, `#/cycle?f=…`, `…&why=d-embargo&path=…`

## 구조
- `data/build/` — 출처·문장·사건·관계망·지표를 만드는 파이썬 파이프라인(이전 프로젝트에서 가져와 다시 검증). `python3 data/build/build_seed.py` → `data/seed.json`
- `data/build/cycles.py` — **사이클 발견 엔진**(추세 분리, 지그재그 전환점, 여러 시차를 함께 본 순열 검정, 주기도, 급변 구간과 간격 변동계수, 5년 구간 궤적 비교, 구간·방법 민감도)
- `web/` — Vite + React + TypeScript 사이트(새로 설계)
- `tests/test_cycles.py` — 엔진 대조 검사(진짜 주기는 찾고, 흰잡음에서 만들지 않고, 추세를 주기로 보지 않는지)
- `tests/e2e.py` — 브라우저 시나리오 A~G·모바일

## 실행
```bash
pip install numpy && python3 data/build/build_seed.py   # 데이터·엔진 다시 계산
cd web && npm install && npm run dev                      # http://localhost:5173
python3 -m pytest -q tests/test_cycles.py
```
main에 올리면 GitHub Actions가 위 검사를 모두 통과한 경우에만 사이트를 바꿉니다. 사이트 아래 '빌드 xxxx'와 `cd web && npm run fingerprint` 결과가 같으면 사이트가 지금 코드와 같습니다.
