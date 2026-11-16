# HISTORY TO FUTURE 2.0 — 새 대화 인수인계서

> **새 대화의 Claude에게**: 이 파일 하나로 개발을 이어 갈 수 있게 정리했다. 순서대로 읽고 '0. 시작할 때 할 일'부터 실행하라.
> 코드는 전부 GitHub 저장소에 있다. 이 파일은 저장소 루트의 `HANDOFF.md`와 같다(2026-11-16 기준, 커밋 `26fd1c8` 이후).

---

## 0. 시작할 때 할 일(순서대로)

1. **저장소 가져오기**: `joan0611/history-to-future2`를 세션에 추가(add_repo, 푸시 권한)한 뒤 clone한다. 작업 폴더 예: `/home/claude/htf2`.
2. **문서 읽기**(저장소 안):
   - `docs/SPEC_2.0.md` — 사용자의 **2.0 통합 지시서 원문**. 개발 기준의 최상위 문서. 필요한 장만 찾아 읽는다.
   - `TASK_QUEUE.md` — 남은 일과 완료 기록
   - `PROJECT_STATE.md` — 차수별 작업 기록(1~21차)
   - `DIAGNOSIS.md` — 지시서 대비 진단표(5절 '지시서 재점검')
   - `DECISIONS.md`, `PROJECT_BRIEF.md`, `REQUIREMENTS.md` — 결정·목적·요구사항
3. **환경 준비**:
   ```bash
   pip install numpy pytest playwright --break-system-packages
   python3 -m playwright install chromium   # e2e는 CHROME_PATH(기본 /usr/bin/google-chrome) 사용, 없으면 playwright 크로미움 경로로 지정
   cd web && npm ci
   ```
4. **현재 상태가 깨끗한지 확인**: 아래 '3. 빌드·검증' 전체를 한 번 돌려 통과하는지 본다(마지막 확인 때 e2e 259/259, pytest 15, 반복 문장 0).

---

## 1. 반드시 지킬 규칙(사용자 지시)

- **응답은 한국어로만.** 영어 문장이 섞이면 사용자가 "한글말로해"라고 지적한다.
- **기존 사이트 `joan0611/history-to-future`(1.0)는 절대 수정하지 않는다.** 작업 대상은 `history-to-future2`만.
- **확인·구현하지 않은 것을 했다고 말하지 않는다.** 자료·출처·수치·인용을 만들어 내지 않는다.
- **유료 서비스는 하지 않는다**(사용자 결정 2026-11-14). 언어모델 API 연동(T7-5)은 진행하지 않는다. 외부 공개 배포 방식 변경·중요 권한은 승인 후에.
- API 키·사용자 이메일을 코드·주소·커밋에 넣지 않는다. 키 파일 `~/.htf2_keys`는 이전 작업 환경에만 있었다. 빌드에는 필요 없다(지표 값은 빌드 모듈 안에 들어 있음).
- 예약 작업(scheduled task) 만들기는 사용자가 거절했다 — 다시 제안하지 않는다.
- 사용자가 "계속해/채워"라고 하면 묻지 말고 TASK_QUEUE의 다음 일을 진행한다.
- 커밋 메시지 끝 서명:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
  (새 대화에서 시스템이 주는 서명 문구가 있으면 그것을 따른다.)
- **보고 형식**(지시서 20장, 작업 한 차례가 끝날 때 10항목): ①무엇을 했나 ②고친 파일 ③쓴 자료·출처 ④적용한 분야 ⑤새로 할 수 있게 된 것 ⑥실행한 테스트 ⑦결과 ⑧아직 안 된 것 ⑨사실/추론 구분 ⑩커밋·배포. 쉬운 말로 짧게.

---

## 2. 프로젝트 한눈에

- **목적**: 1960~현재 한국(과 세계)의 변화를 사건·지표·인과로 연결해 '왜 바뀌었나'를 설명하고, 조건별 미래 가능성을 추론하는 분석 웹앱. 일반인이 읽을 수 있는 쉬운 말.
- **사이트**: https://joan0611.github.io/history-to-future2/ (GitHub Pages, push하면 CI가 검증 후 자동 배포)
- **기술**: 데이터 = Python 빌드 스크립트 → `data/seed.json`(약 3.6MB) / 화면 = React 18 + TypeScript + Vite(`web/`) / 테스트 = pytest + Playwright e2e
- **규모(21차 기준)**: 근거 문장 966 · 출처 1,223 · 지표 51 · 원인 지도 사건 255·연결 231 · 주제 이야기 40 · 산업 일대기 13 · 시대 흐름 14 · 취향 흐름 5 · 미래 가능성 159 · 반복 사례 40
- **정보의 7층**(화면 표시 규칙): 사실 / 출처 해석 / 관찰(계산) / AI 추론 / 가설 / 시나리오 / 모름. 사실과 추론을 섞지 않는다.

### 화면(주소는 해시 라우팅 `#/...`, 상태는 전부 주소에)
| 주소 | 화면 | 파일 |
|---|---|---|
| `#/now` | 첫 화면: 입구 4개, 10개 분야 링 카드, 대표 분석, 판단 질문 4개 | `views/NowView.tsx`, `views/QuickStudy.tsx`, `views/StudyView.tsx` |
| `#/now/q-jobs` 등 | 판단 질문(6단계: 질문→과거 흐름→근거→현재·과거 수치 비교→시나리오→관찰 지표) | `views/QuickStudy.tsx` |
| `#/topic`, `#/topic/<id>` | 주제 지도(분야별 묶음, 9단계 상태표) / 주제 이야기 | `views/TopicView.tsx`, `ui/SpecStatus.tsx` |
| `#/flow/<id>`, `#/taste/<id>` | 시대 흐름 / 취향 흐름 | `views/FlowView.tsx`, `views/TasteView.tsx` |
| `#/field/<cat>?ind=<지표id>` | 분야별 지표 그래프. `#/field/industry?ind=<산업id>`는 산업 일대기 | `views/FieldView.tsx`, `views/IndustryLife.tsx` |
| `#/history?y=&why=&path=` | 시대별 사건 + 원인 패널(WHY, 8단계) | `views/HistoryView.tsx`, `ui/WhyPanel.tsx`, `ui/Why8.tsx` |
| `#/cycle` | 반복과 비교: 사이클 엔진, 반복 사례, 공통 원인, 지표 쌍 자동 탐색 | `views/CycleView.tsx` |
| `#/ask?q=` / `#/ask?ta=&tb=&tc=a,b&tf=&tt=` | 질문 분석(규칙 기반, 추론 유형 표시) / 두 지표 검정 | `views/AskView.tsx`, `lib/ask.ts`, `lib/pairtest.ts` |

공통: `lib/data.ts`(seed 타입과 접근자 `D`, `topicById`, `flowById`, `MAX_Y`=올해 자동), `lib/route.ts`(주소 ↔ 상태, `openWhy`), `ui/Story.tsx`(7층 배지 `SBadge`, `SLineView`, `LayerLegend`), `ui/Crumbs.tsx`(지금 위치), `styles.css`.
분야 CATS(고정, 그래프 차선과 연결): politics, economy, industry, society, culture, flow.

### 데이터 파이프라인(`data/build/`)
- 진입점 `build_seed.py` → `data/seed.json`. **CI는 seed.json이 빌드 결과와 똑같은지 검사**하므로 데이터를 고치면 반드시 다시 빌드해 함께 커밋.
- 주요 모듈:
  - 시대 사건·근거: `era_1960s.py`~`era_2020s.py`, `era_others.py`, 심층 사례 `deep_1973/1997/2008/2020.py`
  - 지표: `indicators*.py`(세계은행·ECOS·KOSIS·FRED 값 내장, 에너지 `indicators_energy.py`)
  - 주제 이야기: `topics.py`(목록·FIELD_MAP·DOMAINS 합치기) + `topics_*.py`, 헬퍼 `topic_helpers.py`
  - 산업: `industries*.py` / 흐름: `flows*.py` / 취향: `tastes*.py`
  - 원인 지도: `graph.py`, `links_extra.py`, 사건 공유 `events_shared.py`
  - 검증: `corroborate.py`(출처 독립성 — 같은 원자료·발행처는 한 곳으로 셈, 'verified'는 두 독립 출처일 때만), `verify_numbers.py`
  - 엔진: `cycles.py`(사이클), `pair_scan.py`(지표 쌍 708개 전수: 변화·추세 제거, 시차 ±3, 3년 묶음 순열 400회, BH q<0.10, 충격 해 제외 견고성)
  - 21차 추가: `future_risks.py`(미래 159개 위험), `future_terms.py`(장기 구조/단기 현상), `repeat_likeness.py`(반복 40개: 원리도 닮음/겉모습만 닮음/반복 아님), `why8.py`(8단계+주체 모델 3사례: 1973 중화학·1987 민주화·2009 스마트폰), `claims_verified2.py`(원문 대조로 두 곳 확인된 문장)
  - 상태표: `spec_fields.py`(지시서 A~J 10개 분야 × 9단계 판정. **tests/e2e.py를 읽어 '화면 시험' 단계를 판정하므로 e2e를 고치면 seed를 다시 빌드**)
- **주제 헬퍼 문법**(topic_helpers.py):
  - 출처 `S(id, 제목, 발행처, url, 종류, 날짜)` / 근거 문장 `C(id, 문장, 'fact'|'statistical'|'source', [출처id], period=, domains=)`; 두 독립 출처를 원문 대조했으면 `dict(C(...), status="verified")`
  - 줄: `F`(사실)·`SRC`(출처 해석)·`INF`(AI 추론)·`HYP`(가설)(문장, *근거id)
  - `TURN`, `LANE`, `REASON`, `REPEAT(..., alternatives=[], counter=[], at=(t,t))`, `FUT(kind,name, change=,basis=,logic=,conditions=,demand=,watch=,against=, risk=)`, `CONCLUDE`, `LINK(target, at, why)`
  - **F/SRC 줄의 숫자는 인용한 근거 문장 안에 그대로 있어야 한다**(빌드가 검사).
  - 새 주제 추가 시: 모듈 작성 → `topics.py`의 import와 TOPICS/SOURCES/CLAIMS/DOMAINS 합치기, FIELD_MAP에 넣기 → 상태표 대상이면 `spec_fields.py` FIELDS의 topics 목록에도 → 미래가 있으면 `future_risks.py`·`future_terms.py`에 키 추가(빌드가 빠진 것을 `seed.futureRisk.missing`에 기록) → e2e에 화면 시험 추가.
- 빠른 점검: `python3 data/build/patch_topics.py`(주제만)

---

## 3. 빌드·검증(작업 끝마다 전부)

```bash
cd /home/claude/htf2
timeout 590 python3 data/build/build_seed.py > /tmp/seed.log 2>&1; echo rc=$?     # 약 2~4분
cd web && npm run build && cd ..
rm -rf /tmp/site/history-to-future2 && mkdir -p /tmp/site && cp -r web/dist /tmp/site/history-to-future2
(cd /tmp/site && nohup python3 -m http.server 8766 >/dev/null 2>&1 &)
python3 -m pytest -q                       # 15건
python3 tests/repeat_check.py              # 반복 문장 0이어야 함
timeout 590 python3 tests/e2e.py http://localhost:8766/history-to-future2/ > /tmp/e2e.log 2>&1; grep FAIL /tmp/e2e.log; tail -1 /tmp/e2e.log
git add -A && git commit -m "..." && git push
gh run list -R joan0611/history-to-future2 -L 1      # CI 약 10~12분, 성공하면 자동 배포
```
- 실사이트 확인: 브라우저로 `https://joan0611.github.io/history-to-future2/?v=<커밋>#/...` (캐시 때문에 `?v=` 붙이기).
- 셸에서 외부 사이트 접근은 막혀 있다. 세계은행 같은 자료는 브라우저로 `https://api.worldbank.org/v2/country/KR/indicator/<코드>?format=json&per_page=100`을 열고 페이지 본문을 JSON으로 읽어 값을 확인했다. 기사 확인은 웹 검색·웹 가져오기 도구로.
- 스크린샷 점검: Playwright로 페이지를 찍어 Read로 본다(이전엔 `/tmp/shot.py <url> <png> [선택자]` 스크립트를 썼다 — 새 환경엔 없으니 필요하면 다시 만든다).

---

## 4. 지금까지 한 일(요약, 1~21차)

- 1~14차: 새 저장소 구축, 원인 지도·사이클 엔진·지표·흐름·취향·산업 일대기·주제 이야기 40개, 7층 표시, 출처 독립성 검사, 질문 분석(규칙 기반)·두 지표 검정(순열·블록 순열·유효 표본·편상관·다중 통제·월별→연 평균).
- 15~17차: 지시서 A~J × 9단계 상태표(`spec_fields.py`, 화면 `#spec-status`), 사건 공유(eventUses·공통 원인 11·되먹임 2), 7층 범례.
- 18차: 에너지·정책·외교 빈 분야 → 세계은행 지표 5개 + 주제 3개(`energy-power`, `policy-welfare`, `world-trade`), 미래 조건 비교(지시서 12-G), '지금 위치' 표시, 첫 화면 입구 카드·분야 링 카드, 추론 유형 표시, 연도 자동 갱신.
- 19차: 소비·생활방식 출처 원문 대조 → **10개 분야 모두 9단계 통과**. 라이브커머스 추정 출처 바로잡음(3조 원은 이베스트투자증권).
- 20차: 미래 159개 전부 '위험' + '장기 구조/단기 현상'.
- 21차: 첫 화면 '미완성' 질문 4개 → 6단계 판단 질문(`q-jobs`, `q-shop`, `q-family`, `q-time`), 모든 미래에 '현재 신호·과거 유사 국면·판단 수정 조건' 3칸, 반복 성격 판정, 지표 쌍 자동 탐색(27쌍 발견, 24쌍 충격 해 제외해도 유지), WHY 8단계+주체 모델 3사례, 범례 통일, 모바일(390px) 넘침 검사 확대. e2e 255/255.

---

## 5. 남은 일(다음 대화에서 할 것)

`TASK_QUEUE.md`가 원본. 핵심만:
1. **T2-1 사건 연결 약 150개**: 주제 전환점·산업 단계 중 원인 지도 사건과 아직 연결되지 않은 것. 이름이 비슷하다고 잇지 말고 원문으로 같은 사건인지 확인한 뒤 연결(근거 문장 공유 방식, `events_shared.py`).
2. **T10-3 출처 재확인**: 약 1,223개 중 원문 대조한 것은 약 40개. 분야별로 조금씩 대조하고, 두 독립 출처가 확인되면 `status="verified"`(통계 수치는 같은 발표를 옮긴 기사 둘이면 한 곳으로 셈).
3. **WHY 8단계 사례 확대**: 22차에 7개(1973 중화학·1973 석유파동·1987·1997·2008·2009·2020). 다음 후보: 1960년대 수출 드라이브, 1979 2차 석유파동 등.
4. **판단 질문 확대**: `QuickStudy.tsx`의 `QSTUDIES`에 질문 추가(지시서 1장의 14개 질문 중 아직 없는 것).
5. **T9-2 자료 공백**: 공식 통계가 없는 항목은 '자료 없음' 유지, 새 공식 자료가 나오면 연결.
6. 하지 않음: T7-5 언어모델 연동(유료 — 사용자 거절).

---

## 6. 사용자에 대해 알아 둘 것
- 이름 조안. 비개발자 관점에서 결과를 본다 — 보고는 쉬운 말로, 링크와 무엇이 바뀌었는지 위주로.
- "계속해", "다 채워", "홈페이지줘" 같은 짧은 지시를 자주 한다. 홈페이지 요청엔 사이트 주소를 준다.
- 디자인은 "재밌게, 알아보기 쉽게"를 원한다(색 있는 카드, 링, 칩, 단계 번호 등 시각 요소 선호).
