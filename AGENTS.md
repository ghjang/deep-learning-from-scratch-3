# AGENTS.md

이 파일은 AI 에이전트(ZCode, Claude Code, GitHub Copilot 등)가 이 저장소에서 작업할 때
참고해야 할 컨텍스트와 규칙을 담습니다. 인간 기여자에게도 유용한 참고 자료입니다.

---

## 📖 프로젝트 개요

**『밑바닥부터 시작하는 딥러닝 ❸』** 학습용 포크 레포지토리.

- 원본: https://github.com/oreilly-japan/deep-learning-from-scratch-3 (일본어 원서, Koki Saitoh 저)
- 한국어 번역본: https://github.com/WegraLee/deep-learning-from-scratch-3
- 이 레포: `ghjang/deep-learning-from-scratch-3` (개인 학습용 포크)

이 저장소의 **목적은 학습**입니다. 책을 따라가며 DeZero라는 딥러닝 프레임워크를
단계적으로 직접 구축해보는 과정을 담습니다. 원본 코드의 무결성을 보존하는 것이
학습 목적 달성의 핵심입니다.

> **DeZero**: PyTorch 스타일의 Define-by-Run(동적 계산 그래프) 딥러닝 프레임워크.
> 책의 5개 고지, 60단계(step01.py ~ step60.py) + 부록 A/B/C에 걸쳐 점진적으로 완성됨.

**고지(Stage) 구성**:

| 고지 | step 범위 | 주제 |
|---|---|---|
| 제 1 고지 | step01 ~ 10 | 미분 자동 계산 |
| 제 2 고지 | step11 ~ 24 | 자연스러운 코드로 |
| 제 3 고지 | step25 ~ 36 | 고차 미분 계산 |
| 제 4 고지 | step37 ~ 51 | 신경망 만들기 |
| 제 5 고지 | step52 ~ 60 | DeZero의 도전 |
| 부록 | A / B / C | (본문 외 보충) |

---

## 🧬 두 개의 프레임워크: `dezero` vs `rezero`

이 레포에는 **같은 목적을 가진 두 개의 프레임워크**가 공존합니다.
이 구분을 이해하는 것이 가장 중요합니다.

| | `dezero/` | `rezero/` |
|---|---|---|
| **역할** | 📖 **정답지** (책 저자의 원본 구현) | ✍️ **학습 노트** (브로가 직접 짜는 변종) |
| **수정** | ❌ 불가 (원본 무결성 보존) | ✅ 자유 (직접 구현/실험/변종 환영) |
| **참고 방향** | `rezero` 작성 중 막힐 때 참조 | `dezero`를 보고 이해한 뒤 내 손으로 재구현 |
| **이름 유래** | Deep + Zero | Re:Zero (다시 시작하는 zero) 오마주 + "다시"의 의미 |

### `rezero/` 디렉터리 구조 (dezero 미러 + steps)

```
rezero/
├── __init__.py
├── core.py         # Variable, Function, Config 등 핵심 (대응: dezero/core.py)
├── core_simple.py  # step23~32 학습용 단순 코어
├── functions.py    # sin, add, matmul 등 연산 함수
├── functions_conv.py  # Conv2d, Pooling, im2col
├── layers.py       # Layer, Linear
├── models.py       # Model, MLP, VGG16, ResNet
├── optimizers.py   # SGD, Momentum, Adam
├── datasets.py     # Dataset, Spiral, MNIST
├── dataloaders.py  # DataLoader
├── cuda.py         # GPU 백엔드 추상화 (현재 NumPy fallback, 향후 MLX 후보)
├── transforms.py   # 데이터 변환 파이프라인
├── utils.py        # 그래프 시각화, gradient_check 등
└── steps/
    ├── step01.py ~ step60.py   # 책 각 단계를 직접 재구현하는 자리
```

→ 모든 파일은 현재 **빈 껍데기**(상단에 "무엇을 구현할 자리인지" 주석만 있음).
→ 브로가 책을 읽으며 직접 채워나가는 구조.
→ 실행 예: `uv run python rezero/steps/step01.py`

### `rezero` 학습 원칙

1. **dezero 복붙 금지** — 막힐 때만 펴서 보고, 다시 내 손으로 짠다.
2. **이해 우선** — 모르는 Python 이디엄/수학은 그때그때 학습.
3. **변종 실험 환영** — 더 나은 이름/구조를 상상하고 시도해본다.
4. **진행 상황 기록** — `rezero/__init__.py`의 `__version__`을 step 진도에 맞춰 올린다.

#### `rezero/__init__.py` 버전 정책

> 학습 진척도를 버전 번호로 인코딩하는 규칙. 모든 세션이 이 규칙을 따를 것.

**형식**: `MAJOR.MINOR.PATCH` (SemVer 스타일이지만 의미는 다름)

| 자리 | 의미 | 올리는 시점 | 예시 |
|---|---|---|---|
| `PATCH` | step 단위 진행 | 해당 step **완료 시** (✅ 전환 시) | `0.0.1` = step01 완료 |
| `MINOR` | 고지(stage) 완료 | 해당 고지 마지막 step 완료 시 | `0.1.0` = 1고지(step10) 완료 |
| `MAJOR` | 책 전체 완료 | step60 + 부록까지 전부 완료 시 | `1.0.0` = 책 완독 |

**예시 진행**:
```
0.0.0   → 시작 전
0.0.1   → step01 완료
0.0.2   → step02 완료
...
0.0.10  → step10 완료 (= 1고지 끝)
0.1.0   → 1고지 마무리(별도 bump, 또는 0.0.10 유지해도 OK — 브로 선택)
0.1.11  → step11 완료 (2고지 진행 중)
...
0.5.60  → step60 완료
1.0.0   → 부록까지 전부 완료 → 책 완독 🎉
```

**동시 업데이트**: 버전 올릴 때 `__init__.py` 상단의 "진행 상황" 주석도 함께 갱신:
```python
진행 상황:
  - 현재 단계: stepNN (주제)
  - 완료한 step: step01 ~ step(N-1)
```

---

## ⚠️ 최우선 규칙 (변경 금지)

1. **`dezero/` 원본 학습 코드 보존**
   - `dezero/`, `steps/`(원본), `examples/` 디렉터리 아래의 코드는 **책 본문 그대로**입니다.
   - 임의로 "개선"하거나 리팩토링하지 마세요. `rezero/`가 변형 실험의 자리입니다.
   - `dezero/` 코드를 수정해야 한다면 반드시 먼저 사용자에게 이유를 설명하고 동의를 구하세요.

2. **`rezero/`는 자유롭게 수정 가능**
   - 브로가 직접 짜는 학습 노트이므로, 브로가 요청하면 얼마든지 수정/실험 가능.
   - 단, "이미 채운 코드를 지우고 싶지 않다" 등 브로 선호가 있으면 존중할 것.

3. **`is_simple_core` 플래그 건드리지 않기**
   - `dezero/__init__.py`의 `is_simple_core`는 책 step23~32 학습 시점용 스위치입니다.
   - 기본값(`False`)을 유지하세요. 책 진도에 따라 사용자가 직접 바꾸는 용도입니다.

4. **커밋은 사용자 명시적 승인 후에만**
   - 브로(owner)가 "커밋해줘", "푸시해줘"라고 명시하지 않으면 커밋/푸시하지 마세요.

---

## 📊 학습 관리 워크플로

> **새 AI 세션에서 가장 먼저 읽을 것**: `LEARNING_PROGRESS.md`
> 그 파일에 현재 학습 진척도(어디까지 했는지)가 step별로 정리되어 있습니다.

### 핵심 문서 (4종)

| 파일 | 역할 |
|---|---|
| `LEARNING_PROGRESS.md` | 📊 **목차/상태 추적**. step01~60 체크리스트 + 이슈 링크 + 상태 이모지 |
| `LEARNING_NOTES.md` | 📝 **step 요약 노트**. step별 핵심 통찰/코드 메모 (가벼움) |
| `notes/` | 🧪 **탐구 노트 디렉터리**. 주제별 개별 파일 (Python/NumPy/수학 등 깊이 파는 주제) |
| GitHub Issues | 📌 **세부 토론**. 각 step 진행 추적 + 막힌 질문 영구 기록 |

이 구조는 **"목차 = LEARNING_PROGRESS.md, step 요약 = LEARNING_NOTES.md, 탐구 = notes/, 본문 = Issues"** 인 하이브리드.
- 어디까지 했는지는 progress에서
- step 핵심은 LEARNING_NOTES.md에서
- 깊이 탐구는 notes/에서 (개별 파일, LEARNING_NOTES.md에서 링크)
- 세부 맥락은 Issues에서

### 🎨 학습 스타일 (브로의 선호, 반드시 존중)

> 이 섹션은 브로가 어떻게 학습하기를 원하는지 명문화한 것.
> 새 AI 세션은 이 스타일을 **반드시** 따를 것.

#### 핵심 철학: **쌩짜 재현 ❌, 이해 + 부분 복붙 + 변형/개선 ✅**

책을 보지 않고 완전히 쌩짜로 재현하는 게 목표가 **아님**. 60개 step을 다 그렇게 하면 시간이 너무 오래 걸리고 학습 동력이 떨어짐.

대신 **3단계 사이클**:
```
1. 읽기   : 책 + 정답지(dezero)로 개념 이해
2. 옮기기 : 이해한 걸 rezero로 옮김 (복붙 OK, 단 무지성 복붙은 금지)
3. 변형   : "이 부분은 이렇게 바꾸면 더 낫겠다" 실험 (선택이지만 권장)
```

#### 노트 작성 (`LEARNING_NOTES.md`) — **브로가 직접 타이핑하지 않음**

- 브로가 노트를 직접 치는 건 너무 느리고 학습 흐름을 끊음
- 대신 **AI와 브로가 대화하며 도출한 통찰을 AI가 정리**해서 기록
- 작성 원칙:
  - **핵심 요약 위주** (길게 쓰지 말 것, 노트가 질어지면 곤란)
  - **키워드/태그** 적극 활용 (나중에 검색/재방문 쉽게)
  - 코드 스니펫은 필요한 최소만
  - 출처 링크(관련 이슈, 정답지 위치 등) 남기기

#### 코드 작성 — **협업 정리 방식**

- 브로가 초안을 짬 (엉터리여도 OK, 학습이니까)
- AI가 깔끔하게 정리 (Pythonic 패턴, 중복 제거, 가독성)
- 이 과정에서 브로는 "왜 이렇게 정리했는지"를 보며 학습
- 단, **무지성 복붙은 금지** — 이해 없이 옮기는 건 학습이 아님

#### step 완료 기준 — **유연하게**

- 모든 step을 100% 완벽히 이해해야 다음으로 넘어갈 필요는 없음
- "대략 이해했고 동작 확인함"이면 다음 step으로 넘어가도 됨
- 나중에 다시 돌아와서 깊이 파고드는 것도 OK
- 막히면 그 step을 ⚠️로 표시하고 일단 넘어가도 됨

### step 학습 사이클 (권장 워크플로)

```
1. 새 step 시작
   ├─ .github 의 📌 Step 진행 추적 템플릿으로 이슈 생성 (라벨: step, learning)
   ├─ LEARNING_PROGRESS.md 해당 행: 상태 ⏳→🔄, Issue 컬럼에 링크 등록
   └─ LEARNING_NOTES.md 해당 step 헤딩 아래 학습 시작 메모

2. step 진행 중
   ├─ 책 읽고 rezero/steps/stepNN.py 직접 구현
   ├─ 막히면: 💬 학습 질문 템플릿으로 별도 이슈 OR step 이슈에 코멘트
   └─ LEARNING_NOTES.md에 질문/통찰/코드 메모 자유롭게 누적

3. step 완료
   ├─ step 이슈 close
   ├─ LEARNING_PROGRESS.md: 상태 🔄→✅, 완료일, 메모(한 줄 요약) 입력
   └─ rezero/__init__.py의 __version__ 올려도 좋음 (예: 0.0.1)

4. 🧪 보충 탐구 모드 (step 사이사이, 브로 선택)
   ├─ "잡생각/궁금증"을 자유롭게 파고 싶을 때 발동
   ├─ 주로 Python 기본기, NumPy 깊이, 프레임워크 디자인 등
   ├─ AI와 대화로 탐구 → 핵심만 LEARNING_NOTES.md에 요약
   └─ 반드시 다음 step으로 넘어가야 하는 건 아님. 깊이 파는 게 목표.
```

### 🧪 보충 탐구 모드 (브로의 학습 특성)

> 브로는 프로그래밍/파이썬 기본기 탐구를 좋아함. step 진도만큼 중요하게 다룰 것.

- step 완료 후 다음 step으로 바로 넘어가지 않고, **잡생각/궁금증**을 자유롭게 파도록 장려
- 주제: Python 기본 문법/이디엄, NumPy 깊이, 프로그래밍 패러다임, 프레임워크 디자인 등
- 방식: 브로가 질문 던지면 AI가 깊이 있게 설명 → 핵심을 `notes/`에 요약
- 탐구 노트는 `notes/exploration_NN_*.md` 주제별 파일로 정리

### 🚦 step 전환 규칙 (중요)

> **브로가 명시적으로 "다음 step 고고" / "step NN 시작하자" 하기 전에는
> AI가 임의로 다음 step으로 넘어가지 않는다.**

AI는 step 완료 또는 탐구 응답 후, "다음 step으로 넘어갈까?" 같은 유도 질문 대신:

- ✅ **"이번 step/탐구에서 더 살펴볼 주제 없는지"** 브로에게 체크
- ✅ 열린 질문으로 마무리 ("다른 궁금한 점 있어?", "더 파고 싶은 주제?")
- ❌ "다음 step 가볼까요?" 같은 전환 시도 금지
- ❌ 자동으로 다음 step 이슈 생성 / 가이드 시작 금지

step 전환은 **오직 브로의 명시적 선언**으로만 발생.

### 🔄 스텝 랩업 (step 전환 시 의식)

> 브로가 **"다음 step 가자" / "step NN 고고"** 선언했을 때,
> AI는 곧바로 다음 step으로 넘어가지 말고 **먼저 랩업 절차**를 수행.

스텝 랩업은 학습의 한 단위를 마무리하며 문서 품질을 점검하는 의식. 소프트웨어 개발의 "Definition of Done"이나 스프린트 리뷰와 유사.

#### 절차 (6단계)

```
1. [진행 요약] 이번 step/탐구에서 뭘 했는지 한두 문장 요약

2. [문서 점검] 이번 단계에서 만들거나 수정한 문서/코드 목록化
   - 새로 작성한 notes/, LEARNING_*.md, rezero/ 등
   - 산재한 "보충" 라벨, 중복 내용, 번호 불일치 점검
   - 응집도/흐름 자체 평가 (한 섹션이 너무 길진 않은지 등)

   **★ 분리/이관 작업 시 필수 체크리스트** (놓치기 쉬운 함정):
   - [ ] 목차(TOC)에서 이관된 섹션 링크 제거/수정했나?
   - [ ] 본문 헤딩 번호가 목차와 일치하나? (A→B→C 연속성)
   - [ ] **목차 앵커(`#a1-...`)가 본문 헤딩과 일치하나?** (헤딩 바꾸면 앵커도)
   - [ ] **하단 요약(주제 수, 분리 링크 등)이 현재 구조와 일치하나?**
   - [ ] 다른 파일에서 이관된 섹션으로 링크가 깨지지 않았나?
   - [ ] 인덱스(README, LEARNING_NOTES)에 새 파일 추가했나?
   - [ ] 기존 파일의 "관련 링크" 섹션에 새 파일 링크 추가했나?

   > 💡 깨진 링크는 GitHub 사이트에서 직접 클릭해봐야 발견됨.
   > 브로의 GitHub 리뷰가 최종 방어선.

### ⚡ 즉시 수정 원칙 (중요)

> **작업 원칙/체크리스트/절차의 개선이 필요하다고 판단되면, 랩업 등으로 미루지 말고
> 브로에게 제안하고 동의를 받은 후 즉시 반영한다.**

- ✅ "이건 체크리스트에 추가하면 좋겠어요" → **브로에게 제안 → 동의 → 즉시 반영**
- ❌ AI가 독단적으로 규칙 추가/수정 (브로 동의 없이) — 금지
- ❌ "다음 랩업 때 검토" → 까먹을 확률 100%, 지금 제안하자

**핵심**: "미루면 까먹음" + "독단은 위험" = **제안은 즉시, 반영은 동의 후**.

3. [리포팅] 발견된 문제를 브로에게 보고
   - "A.2 섹션이 263라인이라 너무 김 → 재편 권장"
   - "exploration_02와 03에 내용 중복 있음 → 통합 권장"
   - "키워드 태그 누락", "링크 깨짐" 등 사소한 것도 포함

4. [협의] 재편/유지 결정 — 브로가 최종 콜
   - AI가 제안하되, 브로가 우선순위/범위 결정
   - "지금 하자" / "나중에" / "안 해도 됨" 중 선택

5. [실행] 결정된 작업 수행 (재편 등 — 커밋은 아직 안 함)

6. [★ step 완료 확정] — 상태 전환 + 커밋/푸시 승인
   - **상태 전환 작업** (한 번에 처리):
     - `LEARNING_PROGRESS.md` 해당 step: 🔄→✅, 완료일, 메모
     - `LEARNING_NOTES.md` 해당 step: 🔄→✅, 완료일
     - `rezero/__init__.py` 버전 bump (예: `0.0.N` → `0.0.N+1`)
     - GitHub Issue close (완료 코멘트와 함께)
     - `LEARNING_PROGRESS.md` 전체 요약 카운트 갱신
   - **브로에게 커밋/푸시 승인 요청** ("이대로 커밋+푸시할까요?")
   - 승인 시 커밋 + push (★최우선 규칙: 브로 명시적 승인 없이 커밋/푸시 금지)

7. [다음 step 시작] — 커밋/푸시 완료 후에만 step 전환
```

#### 핵심 원칙

- **자동 재편 금지**: AI가 독단적으로 "정리해놨어" 하지 말 것. 항상 브로에게 먼저 리포팅.
- **문제 발견은 환영**: 리포팅 자체가 가치. 브로가 "안 고쳐도 돼" 해도 OK.
- **다음 step은 랩업 끝난 후에**: 랩업 미완료 상태로 step 전환 금지.
- **사소한 문제는 스킵 가능**: 사소한 오타/링크 정도는 랩업에서 그냥 고치고 리포팅만.
- **커밋/푸시는 명시적 승인 후에**: 6단계에서 브로가 승인하기 전엔 커밋/푸시하지 않는다 (최우선 규칙 L130 준수). step 전환(7단계)은 커밋/푸시 완료 후에만.

#### 📦 커밋 단위 정책

> 한 step의 변경사항을 어떻게 커밋에 담을지 가이드.

**원칙**: **1 step 완료 = 1 커밋** (국룰)

- 단순 step: 코드 + 노트 + 메타 갱신을 **하나의 커밋**으로.
  - 커밋 메시지 예: `step02 완료 - 변수를 낳는 함수 (Function 도입)`
- 복잡한 step (큰 탐구, 문서 대공사, 다중 주제): **합리적 단위로 분리 커밋 OK**.
  - 예: 코드 커밋 + 탐구 노트 커밋 + 메타 갱신 커밋
  - 단, 분리 시점은 브로가 랩업 6단계에서 결정. AI가 독단 분리 금지.
- **미완성 변경사항은 커밋하지 않는다**: step 진행 중엔 로컬에 쌓아두고, 랩업 6단계 승인 시점에 정리 커밋.
- **커밋 메시지 형식** (Conventional Commits 스타일 권장):
  - `stepNN 완료 - {주제}` 또는
  - `feat(stepNN): {주제}` / `docs(notes): {탐구 주제}`

### AI 에이전트 (다른 세션) 가이드

새 세션에서 브로가 "이어서 작업하자" 하면:
1. `LEARNING_PROGRESS.md`를 읽고 현재 step 파악
2. 해당 step의 Issue를 확인해 진행 맥락 파악
3. `LEARNING_NOTES.md` 해당 step 헤딩 + `notes/` 인덱스 확인해 기존 질문/통찰 파악
4. 그 다음 위 사이클의 적절한 단계부터 이어서 진행

> 브로는 탐구(잡생각)를 좋아하므로, step 진도 외에도 "이것 좀 더 파볼까?" 하는
> 주제가 나오면 `notes/` 에 새 탐구 노트로 정리할 것.

### 상태 이모지 범례

| 이모지 | 의미 |
|---|---|
| ⏳ | 아직 시작 전 |
| 🔄 | 진행 중 |
| ✅ | 완료 |
| ⚠️ | 막힘 (도움 필요) |
| ⏭ | 건너뜀 |

---

## 🛠 개발 환경

### Python / 의존성 (uv 기반)

이 저장소는 **uv**로 Python 환경을 관리합니다.

| 항목 | 값 |
|---|---|
| Python | 3.12 (`pyproject.toml`의 `requires-python = ">=3.12"`) |
| 핵심 의존성 | `numpy`, `matplotlib` |
| 가상환경 | `.venv/` (gitignored) |
| Lock 파일 | `uv.lock` (버전 고정, 커밋 대상) |

> **주의**: 시스템 Python 3.9.6을 쓰지 마세요. 항상 uv 관리 Python 3.12를 사용합니다.

### 자주 쓰는 명령어

```bash
# 의존성 설치/동기화 (clone 후 최초 1회 + 의존성 변경 시)
uv sync

# 파이썬 스크립트 실행 (venv 자동 활성화)
uv run python steps/step01.py
uv run python your_script.py

# 단위 테스트 실행
uv run python -m unittest discover tests            # 원본 dezero 테스트
uv run python -m unittest discover rezero/tests     # rezero 학습 테스트

# 새 의존성 추가 (pyproject.toml + uv.lock 자동 갱신)
uv add scipy pillow opencv-python   # examples 일부에 필요할 때
```

### 의존성 정책

- **핵심**: `numpy`, `matplotlib`만 `pyproject.toml`에 명시되어 있습니다.
  - 책 본문(`steps/`)과 프레임워크(`dezero/`) 실행에는 이것만 있으면 충분합니다.
- **선택적** (`examples/` 일부에 필요): `scipy`, `pillow`, `opencv-python`
  - 필요한 예제를 실행할 때 그때 `uv add`로 추가하세요.
- **GPU 백엔드**: CuPy는 macOS 미지원으로 설치하지 않습니다. → 아래 "Known Gotchas" 참조.

---

## 📁 디렉터리 구조

```
dezero/        DeZero 프레임워크 소스 (책이 완성해가는 결과물)
├── core.py         Variable, Function 등 핵심 클래스 (step33 이후)
├── core_simple.py  단순화된 코어 (step23~32용)
├── functions.py    함수 구현 (sin, add, matmul 등)
├── functions_conv.py  합성곱 관련 함수
├── layers.py       Layer 클래스
├── models.py       Model, VGG16, SimpleConvNet 등
├── optimizers.py   SGD, Momentum, Adam
├── datasets.py     Dataset 클래스
├── dataloaders.py  DataLoader
├── cuda.py         GPU(CuPy) 백엔드 (macOS에선 fallback)
├── transforms.py   데이터 변환
└── utils.py        유틸리티

steps/         step01.py ~ step60.py (책 각 단계별 코드) — 원본, 수정 금지
examples/      DeZero 응용 예제 (VGG, GAN, VAE, style transfer 등) — 원본, 수정 금지
tests/         단위 테스트 — 원본

rezero/        ✍️ 학습 노트 — dezero/를 정답지로 삼아 직접 재구현 (자유 수정 가능)
├── steps/     step01.py ~ step60.py (빈 템플릿, 브로가 채워나감)
└── tests/     test_*.py (원본 tests/와 1:1 대응, 현재 전부 @skip)

.github/       이슈/PR 템플릿 (Issue Forms + PR 템플릿)
pyproject.toml uv 프로젝트 명세
uv.lock        의존성 버전 고정
.python-version  (gitignored) Python 3.13 고정
LEARNING_PROGRESS.md  📊 학습 진척도 추적 (목차)
LEARNING_NOTES.md     📝 학습 step 요약 노트 (가벼움)
notes/                🧪 보충 탐구 노트 (주제별 개별 파일, 깊이 파는 주제)
```

---

## 🧪 Known Gotchas (이미 알려진 함정들)

### 1. chainer 의존 테스트 11개 (현재 환경에서 실패)

`uv run python -m unittest discover tests`를 돌리면 **11개 테스트가 ERROR**로 실패합니다.
원인은 `chainer` 패키지 미설치. Chainer는 DeZero의 레퍼런스 비교 구현으로 쓰이며
2024년 프로젝트 종료 + Python 3.12 미지원이라 설치하지 않습니다.

영향 받는 테스트: `test_batchnorm`, `test_conv2d`, `test_deconv2d`, `test_linear`,
`test_pooling`, `test_relu`, `test_resnet`, `test_sigmoid`, `test_softmax`,
`test_softmax_cross_entropy`, `test_vgg16`

→ **이 11개 실패는 정상입니다.** DeZero 자체 기능 이상이 아님. 나머지 66개는 통과합니다.

> 참고: `rezero/tests/`는 현재 전부 `@unittest.skip("rezero 구현 대기 중")` 상태입니다.
> `uv run python -m unittest discover rezero/tests`를 돌리면 `OK (skipped=21)`로 떠야 정상.
> 브로가 rezero 모듈을 구현하면서 skip을 풀고 테스트를 채워나갑니다.

### 2. CuPy / GPU 백엔드 (macOS 미지원)

`dezero/cuda.py`는 `try: import cupy except ImportError`로 보호되어 있습니다.
CuPy가 없으면 `gpu_enable = False`로 빠져 자동으로 NumPy로 fallback됩니다.

→ 책 읽고 DeZero를 **CPU(NumPy)로 돌리는 데에는 아무런 지장이 없습니다.**

향후 방향(아이디어 단계): M시리즈 칩에서 **MLX 백엔드** 포팅을 검토 중.
`dezero/cuda.py`와 유사한 `dezero/mlx.py`를 두는 구조가 될 수 있음.

### 3. SyntaxWarning: "is" with 'str' literal

`dezero/datasets.py:234`에서 `label_type is 'fine'` 코드가 Python 3.12에서
SyntaxWarning을 냅니다 (원본 코드 자체 버그). 동작에는 영향 없음.
원본 코드 보존 원칙에 따라 일단러두되, 별도 이슈로 추적 중인 상태.

### 4. NumPy 2.x 마이그레이션

최근 커밋들(`np.int → int`)이 NumPy 1.24+ 호환 작업입니다.
현재 `uv.lock`은 NumPy 2.5.1로 고정되어 있으며, DeZero는 정상 동작합니다.

### 5. CI / `.travis.yml` 제거 (이 레포 기준)

원본 상위 레포에는 `.travis.yml`(Python 3.6 + chainer 기반 unittest)이 있었으나,
**이 포크에서는 제거**했습니다. 이유:

- Travis CI는 명시적 연동(활성화 승인)이 있어야 도는데, 이 레포는 연동한 적 없음 →
  어차피 서버에서 돌지 않는 죽은 페이퍼였음.
- 저 내용대로라도 `python: 3.6` / `pip install chainer`가 현재 환경에서 설치 실패.
- 이 레포의 정식 환경은 `uv` 기반 Python 3.12이므로 `.travis.yml`과 충돌/혼란 유발.

→ 로컬 테스트는 `uv run python -m unittest discover tests`로 직접 돌립니다.
   (GitHub Actions 워크플로도 현재는 없음. 필요하면 `.github/workflows/`에 추가.)

### 6. `setup.py` 제거 (uv 마이그레이션)

원본 상위 레포에는 `setup.py`(setuptools 기반 패키지 정의)가 있었으나,
**이 포크에서는 제거**했습니다. 이유:

- 이 레포의 정식 패키지 명세는 이제 `pyproject.toml` (uv 관리) 한 곳으로 통일.
- 기존 `setup.py`가 담던 정보(`name`, `version`, `install_requires`, `packages` 등)는
  전부 `pyproject.toml`로 옮겨졌습니다.
- 이중 관리(두 파일에 같은 정보)를 피해 혼동을 방지.
- 단, `version = "0.0.13"`은 원본 `dezero/__init__.py`의 `__version__`과 일치하도록 보존.

→ 이 레포는 학습 목적이라 PyPI 등록하지 않으며, `[tool.uv] package = false`로
   설정되어 있어 빌드/배포 용도가 아닙니다. `uv sync`로 의존성만 관리합니다.

### 7. VSCode Markdown Preview, 외부 파일 변경 즉시 반영 안 됨

VSCode의 Markdown Preview 창이 **외부 도구(ZCode/CLI/다른 에디터)에서 수정한
`.md` 파일을 자동으로 새로고침하지 않는** 버그. 파일에 직접 한 글자라도
타이핑해야 그제야 렌더링이 갱신됨.

**원인**: VSCode의 파일 시스템 감시(file watcher)가 같은 프로세스 내 변경사항만
잘 잡고, 외부 프로세스의 디스크 변경을 놓치는 경우가 있음. (유닉스 권한/inotify 한계)

**워크로라운드** (가벼운 것부터):
1. **명령 팔레트** (`Cmd+Shift+P`) → `Markdown: Open Preview to the Side` 다시 실행
2. **파일에 한 글자 타이핑 후 삭제** → VSCode가 강제로 리프레시
3. **`Cmd+Shift+P` → `Developer: Reload Window`** (가장 확실하지만 무거움)
4. **설정 변경** (`.vscode/settings.json`에 추가, 근본 해결 시도):
   ```json
   "files.useExperimentalFileWatcher": true,
   "markdown.preview.refreshOnSave": true
   ```
5. **포커스 전환**: 다른 앱으로 갔다가 VSCode로 돌아오면 대부분 갱신됨

> 브로 패턴: AI가 문서 수정하면 → VSCode Preview가 안 갱신 → 타이핑 한 글자로 갱신.
> 이 이슈는 VSCode/OS 레벨이라 레포에서 해결 불가. 워크로라운드로 대응.

### 8. GitHub Issues 목록에 새 이슈가 바로 안 보임 (UI 지연/캐싱)

`gh issue create`로 이슈를 생성하면 API 레벨에선 **즉시 정상 반영**되지만,
GitHub 웹 UI(특히 Safari)의 이슈 목록엔 **바로 나타나지 않는** 경우가 있음.

**증상** (브로 경험: step02~04 진행 중 발생):
- `gh issue list`로 확인하면 OPEN 상태로 정상 존재
- 직접 이슈 URL(`issues/5`)로 가면 정상 보임
- **탭 카운트(Issues 옆 숫자)는 정상 업데이트**되나, 실제 목록에 새 이슈가 안 보임
- **"Issues" 탭을 클릭해서 들어가도 여전히 안 보임** (브로가 밥 먹기 전에 확인)
- 강력 새로고침(`Cmd+Option+R`), 캐시 비우기(`Cmd+Option+E`)도 효과 없음
- **시간이 지나(약 30분~1시간 후) 그제서야 목록에 나타남** (브로가 밥 먹고 온 후 확인)

**원인 추정**:
- GitHub 검색/인덱싱 지연 — 새 이슈가 목록 뷰에 반영되는 데 시간이 걸림
  (탭 카운트는 빠르게 업데이트되지만, 목록 렌더링은 별도 인덱스 사용 추정)
- Safari의 JS 캐시가 GitHub SPA 코드와 충돌하는 경우 (Chrome에선 덜 발생)
- 캐시 비우기로도 안 풀리는 걸 보면, **브라우저 캐시 문제가 아니라 GitHub 서버쪽 인덱싱 지연**일 가능성이 높음

**워크로라운드** (가벼운 것부터):
1. **직접 이슈 URL로 접근** — `https://github.com/.../issues/N`. 항상 정상 보임
2. **터미널에서 확인** — `gh issue list` / `gh issue view N` (API 레벨은 항상 정확)
3. **기다리기** — 보통 30분~1시간 내 자연 해결. 다음 작업 진행하면 됨
4. **Chrome/Firefox 사용** — Safari보다 GitHub 렌더링이 안정적. 재발이 잦으면 브라우저 교체 권장

**진단 체크리스트** (재발 시):
- [ ] `gh issue list`로 실제 존재 확인 (API = 진실의 원천)
- [ ] 직접 이슈 URL로 접근 → 보이면 100% UI/인덱싱 문제
- [ ] 탭 카운트는 정상인데 목록만 안 보임 → GitHub 인덱싱 지연
- [ ] 기다리거나 다른 작업 진행 — 보통 자연 해결

> 💡 핵심: **API(`gh`)가 진실**. UI가 안 보여도 이슈는 정상 생성되어 있고,
> 작업 흐름(progress/notes 링크 등)엔 영향 없음. 기다리면 해결됨.
> "Issues 탭 클릭하면 보인다"는 **오해** — 클릭이 아니라 **시간**이 해결책.

---

## 🔄 워크플로

### 이슈 관리

GitHub Issue Forms(`.github/ISSUE_TEMPLATE/`)로 3종 이슈를 관리합니다:

| 템플릿 | 라벨 | 용도 |
|---|---|---|
| 🐛 버그 리포트 | `bug` | 실행 중 오동작/에러 |
| ✨ 기능/개선 제안 | `enhancement` | MLX 포팅, 테스트 정리 등 |
| 💬 학습 질문/토론 | `question`, `discussion` | 책 읽다 막힌 점 기록 |

`config.yml`에서 blank issue를 비활성화했으므로, 모든 이슈는 위 템플릿 중
하나를 통해 생성됩니다.

### 변경 전 체크리스트

1. `uv sync`로 환경이 최신인지 확인.
2. 작업 후 `uv run python -m unittest discover tests`로 회귀 확인
   (chainer 관련 11개 실패는 무시).
3. `dezero/`, `steps/`, `examples/` 원본 코드를 건드렸다면 사용자에게 사전 설명 필수.

---

## 🏷 중요 태그

- `baseline-before-uv-setup`: uv 환경 도입 직전의 원본 상태 스냅샷 (커밋 `38374db`).
  언제든 `git reset --hard baseline-before-uv-setup`으로 원복 가능.
