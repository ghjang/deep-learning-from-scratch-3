# 📐 코딩 스타일 노트 — rezero 코드 스타일 가이드

> `rezero/` 구현을 진행하며 다루는 **코드 스타일 / 가독성** 주제를 정리하는 누적형 레퍼런스.
> `design_patterns.md`, `debugging.md`와 같은 구조 — 여러 step에 걸쳐 재등장하는 횡단 관심사라 단일 파일에 누적 관리.
>
> 다루는 범위:
> - PEP 8 기반 스타일 (빈 줄, 들여쓰기, 공백)
> - 주석 밀도 / 종류 (docstring vs 인라인 vs 블록)
> - 네이밍 (함수, 변수, 매개변수)
> - 함수 길이 / 분해 (리팩토링 신호)
> - 타입 힌트 정책
>
> 원칙: **PEP 8이 기본 (의무 규칙 준수), 그 위에 브로 취향(가독성)을 일관되게 적용**.

---

## 📋 인덱스

| # | 주제 | 최초 등장 | 분류 |
|---|---|---|---|
| 1 | 빈 줄 (blank line) — 논리 블록 사이 시각적 분리 | step08 | 레이아웃 (PEP 8) |
| 2 | 삼항 연산자 — 단순 2-way 분기 압축 | step09 | 제어 흐름 (Pythonic) |
| 3 | `and` 결합 + 단축 평가 — 중첩 if 평평하게 | step09 | 제어 흐름 (Pythonic) |
| 4 | ★ Pythonic ≠ 짧게 — "의도 투명성"이 진짜 기준 | step09 | 철학 (메타 원칙) |
| 5 | 튜플 언패킹 — 짝인 값 한 줄로 회수 | step09 | 제어 흐름 (Pythonic, 항목 4 양면) |
| 6 | import 위치 (모듈 최상단 vs 함수 지역) + 순환 참조 | step09 | 모듈 시스템 (Pythonic) |
| 7 | 매직메서드는 클래스 안에 정의 — "클래스 밖 대입 비권장" | step20 | 클래스 설계 (정적 분석) |

---

## 1. 빈 줄 (blank line) — "논리 블록 사이 시각적 분리"

### 📖 일반 규칙 (PEP 8 기준)

PEP 8의 빈 줄 규칙 (강제력 순):

| 위치 | 규칙 | 강제력 |
|---|---|---|
| **최상위 함수/클래스 정의 사이** | **2줄** 빈 줄 | ★ 의무 |
| **메서드 정의 사이** (클래스 내) | **1줄** 빈 줄 | ★ 의무 |
| **함수/메서드 본문 내 논리 블록 사이** | 가끔 1줄 (선택적) | 관행 (권장) |
| **관련된 한 줄짜리 묶음** (예: import 여러 줄) | 빈 줄 없이 | 관행 |

### 🎯 핵심 — "의무 규칙" vs "관행"

PEP 8이 **금지**하는 건 아님. 오히려:
- 최상위/메서드 사이는 **의무** (2줄/1줄)
- 함수 내부 논리 블록 사이는 **"가끔 1줄"** 이라는 **암묪적 권장**

→ "논리 블록 사이 빈 줄을 넣지 말라"는 코딩 컨벤션은 **존재하지 않는다**.
오히려 가독성을 위해 넣는 게 널리 합의된 관행.

### 🎯 왜 논리 블록 사이 빈 줄이 좋은가 (4가지 이유)

1. **"단락 나누기"** — 글쓰기와 같은 원리. 빈 줄 없는 긴 함수는 "코드 벽(code wall)"처럼 느껴짐.
   빈 줄은 "여기서 단락이 바뀐다"는 시각적 신호.
2. **PEP 8 암묪적 권장** — "가끔 1줄"이라는 표현 자체가 "논리 구분 필요하면 넣어라"는 뉘앙스.
3. **리팩토링 신호** — 빈 줄로 잘 나뉜 섹션은 "이 섹션을 별도 함수로 빼면?" 힌트.
4. **diff/git 가독성** — 변경 사항이 어느 논리 섹션인지 파악 쉬움.

### 🎯 DeZero/rezero 등장 지점

#### step08 — `fill_grad()` 본문 섹션 분리 (★ 이 노트의 직접 계기)

`fill_grad`는 논리적으로 3개 섹션:
1. **검증 (A)** — 도입부 guard clause
2. **upstream 설정** — 3단계 우선순위
3. **메인 루프** — 스택 기반 역방향 순회

```python
def fill_grad(start_var, upstream_grad=None):
    # [검증 (A)]
    if start_var.creator is None:
        raise RuntimeError(...)
                                          # ← 빈 줄 + 섹션 헤더 주석
    # [upstream 설정]
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        start_var.grad = np.ones_like(start_var.data)
                                          # ← 빈 줄 + 섹션 헤더 주석
    # --- 메인 루프 ---
    funcs = [start_var.creator]
    while funcs:
        f = funcs.pop()
        ...
```

★ 브로 지적:
> "의미구분을 위해서 빈공백을 좀 넣고 하는 것 자체를 하지 말라는 건 아니지 않냐?"

→ 정확함. 이전(빈 줄 없음)은 PEP 8 관행을 과소평가한 것. 빈 줄 추가로 가독성 향상.

#### 보너스 — 루프 내부 미니 블록도 분리

```python
while funcs:
    f = funcs.pop()
    x = f.input
    y = f.output
                        # ← 빈 줄 (입력 회수 / 검증 / 처리 구분)
    assert x is not None and y is not None
    assert y.grad is not None
                        # ← 빈 줄
    x.grad = f.backward(y.grad)

    if x.creator is not None:
        funcs.append(x.creator)
```

루프 한 바퀴 안에서도 "회수 → 검증 → 처리 → 다음 push" 4단계가 있으면, 빈 줄로 미니 블록 분리.
다만 **너무 잘게 쪼개면 산만** — "논리적 한 단위" 기준. (이건 감, 연습으로 다듬음.)

### 🎯 빈 줄 + 섹션 헤더 주석의 시너지

빈 줄만 있으면 "어디서 어디까지가 한 섹션인지" 애매할 수 있음. **빈 줄 + 섹션 헤더 주석** 결합이 강력:

```python
# --- 메인 루프: 계산 그래프 역방향 순회 (명시적 스택) -----------------
funcs = [start_var.creator]
while funcs:
    ...
```

- 빈 줄: 시각적 단절
- 헤더 주석: 이 섹션이 **무엇**인지 한 줄 요약
- 둘이 합쳐 "섹션 경계 + 의미" 동시 전달

→ 관행 패턴: **논리 섹션이 5줄 이상이고 이름 붙일 수 있으면, 빈 줄 + 헤더 주석**.

### 🎯 언제 빈 줄을 넣고 말지 — 휴리스틱

| 상황 | 빈 줄? |
|---|---|
| 함수가 짧고 한 가지 일만 (3~5줄) | ❌ 필요 없음 |
| 함수에 논리적 단계 2개 이상 | ✅ 단계 사이에 |
| 관련된 한 줄짜리 묶음 (import, 변수 선언 여러 줄) | ❌ 붙여 씀 |
| 제어문(if/for/while) 블록이 3줄 이상 | ✅ 앞뒤로 고려 |
| 한 루프 안에 여러 단계 (회수/검증/처리) | ✅ 단계마다 |

→ 핵심: **"논리적 한 단위"가 어디서 끝나는지** 빈 줄로 신호. 다만 취향 영역이 크니 **일관성**이 최우선.

### ⚠️ 주의 — 과잉 분리 경계

빈 줄을 너무 많이 넣으면 오히려 **파편화** (한 화면에 들어갈 코드가 두 화면이 됨).
- 모든 문장 사이 빈 줄 → ❌ (산만)
- 5줄짜리 함수에 빈 줄 3개 → ❌ (과잉)
- 기준: **"빈 줄이 의미 있는 단락 구분인가?"** 자문. 아니면 빼라.

### 🔑 핵심 키워드

`#빈줄` `#blank-line` `#PEP8` `#논리블록` `#시각적분리` `#단락나누기` `#코드벽` `#섹션헤더주석` `#리팩토링신호` `#가독성` `#의무규칙vs관행` `#일관성`

### 🔗 관련

- [PEP 8 — Blank Lines](https://peps.python.org/pep-0008/#blank-lines) — 공식 규칙 (최상위 2줄, 메서드 1줄)
- step08 `rezero/steps/step08.py` — `fill_grad` 섹션 분리 적용
- Refactoring (Fowler) — "Extract Function" (빈 줄로 나뉜 섹션 → 함수 추출 후보)

---

## 2. 삼항 연산자 — "단순 2-way 분기 압축"

### 📖 일반 규칙

**단순 2-way 분기 + 각 갈래가 한 표현식** → `if/return` 2번 대신 **삼항 연산자** (`A if cond else B`) 사용.
Python 커뮤니티 합의: 이런 케이스엔 삼항이 더 Pythonic.

```python
# ❌ 보일러플레이트 (if/return 2번 반복)
if np.isscalar(x):
    return np.array(x)
return x

# ✅ 삼항 — 한 줄로 의미 응축
return np.array(x) if np.isscalar(x) else x
```

### 🎯 언제 삼항을 쓰나 — 가이드라인

| 상황 | 삼항? |
|---|---|
| 2-way 분기 + 각 갈래가 한 표현식 | ✅ |
| 분기마다 여러 문장 (블록) | ❌ (if/else) |
| 조건이 복잡 (and/or 조합) | ⚠️ 가독성 떨어지면 if/else |
| "기본값 + 예외" 패턴 | ✅ (`default if not cond else special`) |

→ 핵심: **"한 줄에 A if cond else B 가 읽히는가?"** 안 읽히면 if/else로.

### 🎯 DeZero/rezero 등장 지점

#### step09 — `as_array()` 스칼라 변환 (★ 이 항목의 계기)

브로 제안: *"as_array의 3줄, 1줄로 줄이는 게 더 읽기 쉽지 않나?"*
→ 맞음. 단순 "스칼라면 np.array(x), 아니면 x" 분기라 삼항이 Pythonic.

```python
# step09 as_array — 삼항 1줄
def as_array(x: object) -> np.ndarray:
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]
```

★ 디테일 — `# type: ignore`는 유지:
- pyright가 "스칼라 갈래(np.array→ndarray) / ndarray 갈래(x 그대로)" 두 리턴 타입을
  단일 타입으로 못 좁혀서 경고. type: ignore로 의도 표시.
- 상세 설명은 docstring으로 이동 (1줄화하면서 주석 정보 손실 방지).

### 🔑 핵심 키워드

`#삼항연산자` `#ternary` `#Pythonic` `#2-way분기` `#보일러플레이트제거` `#조건표현식` `#A-if-cond-else-B` `#PEP8`

### 🔗 관련

- [PEP 308 — Conditional Expressions](https://peps.python.org/pep-0308/) — 삼항 연산자 도입 PEP
- step09 `rezero/steps/step09.py` `as_array()` — 적용 사례

---

## 3. `and` 결합 + 단축 평가 — "중첩 if 평평하게"

### 📖 일반 규칙

**중첩 if가 "조건 A and 조건 B" 형태** → 중첩 대신 `and`로 한 줄 결합. 들여쓰기 감소 + Pythonic.

```python
# ❌ 중첩 if (들여쓰기 2단계)
if data is not None:
    if not isinstance(data, np.ndarray):
        raise TypeError(...)

# ✅ and 결합 (평평, 1단계)
if data is not None and not isinstance(data, np.ndarray):
    raise TypeError(...)
```

### 🎯 핵심 메커니즘 — 단축 평가 (short-circuit)

`and`의 왼쪽이 False면 **오른쪽 평가 안 함**. 그래서 중첩 if와 동일한 안전성:

```python
# data가 None이면 "data is not None"이 False → isinstance(None, ...) 호출 안 됨 ★
if data is not None and not isinstance(data, np.ndarray):
    #                                ↑ data가 None면 여기 도달 안 함 (안전)
    raise TypeError(...)
```

- 중첩 if의 "바깥 if가 False면 안쪽 if 안 실행"과 **논리적으로 동일**
- 단, 평평한 1단계 구조라 가독성 향상 (guard clause와 같은 철학)

### 🎯 왜 and가 더 나은가 (3가지 이유)

1. **단축 평가** — 왼쪽 False면 오른쪽 미평가. 중첩과 동일 안전성 (위 예시)
2. **들여쓰기 감소** — 2단계 → 1단계. 평평한 구조 = 읽기 쉬움
3. **논리적 조건 자연스러움** — "data가 None이 아니고 AND ndarray가 아니면"은 하나의 조건이라 `and`가 자연스러움

### 🎯 언제 and 결합을 쓰나 — 가이드라인

| 상황 | and 결합? |
|---|---|
| 두 조건이 하나의 논리적 조건을 이룸 | ✅ |
| 두 조건이 서로 다른 관심사 (순차적 단계) | ❌ (중첩 또는 순차 if) |
| 바깥 조건이 안쪽의 **전제 조건** (가드) | ⚠️ 케이스 바이 케이스 |
| 조건이 3개 이상 (and/and/and) | ⚠️ 가독성 떨어지면 분리 |

→ 핵심: **"두 조건이 하나의 의미를 이루는가?"** 그러면 `and`, 아니면 분리.

### 🎯 DeZero/rezero 등장 지점

#### step09 — `Variable.__init__` 타입 체크 (★ 이 항목의 계기)

브로 제안: *"중첩 if 말고 `and` 쓰면 안 돼? 파이썬에 and 같은 거 없어?"*
→ 맞음. "data가 None이 아니고 AND ndarray가 아니면"은 하나의 조건이라 and 결합이 Pythonic.

```python
# step09 Variable.__init__
def __init__(self, data: Optional[np.ndarray]):
    if data is not None and not isinstance(data, np.ndarray):
        raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")
    self.data = data
    ...
```

★ 실증 (단축 평가 정상 작동):
```
Variable(None)   → OK (data is None → isinstance 호출 안 됨, TypeError 안 남)
Variable(ndarray) → OK
Variable(1.0)    → TypeError 정상 (방어막 2번 작동)
```

### ⚠️ 주의 — 중첩이 나은 경우도 있음

**안쪽 if가 바깥 if에 의존하는 복잡한 로직**이면 중첩이 더 명확할 수 있음:
```python
# 이런 건 and 결합이 오히려 산만
if data is not None:
    if not isinstance(data, np.ndarray):
        raise TypeError(...)
    # ★ 여기서 data.ndim 체크 등 추가 로직 — and로는 표현 안 됨
    if data.ndim != 0:
        ...
```
→ 이런 케이스는 중첩 유지. 핵심은 **"두 조건이 하나의 의미인가"** 로 판단.

### 🔑 핵심 키워드

`#and결합` `#단축평가` `#short-circuit` `#중첩if회피` `#평평한구조` `#Pythonic` `#guard-clause철학` `#들여쓰기감소`

### 🔗 관련

- 항목 2 (삼항 연산자) — 같은 "제어 흐름 압축" 시리즈
- step09 `rezero/steps/step09.py` `Variable.__init__` — 적용 사례
- debugging.md 항목 3 (guard clause) — "평평한 구조" 철학의 원류

---

## 4. ★ Pythonic ≠ 짧게 — "의도 투명성"이 진짜 기준

### 📖 메타 원칙 — 항목 2-3의 안티테제스

항목 2(삼항), 항목 3(and)에서 "평평하게/짧게"가 Pythonic 가치를 보여줬다면,
이 항목은 **역설**을 짚는다: **짧다고 무조건 Pythonic이 아니다.**

### 🎯 핵심 — "Pythonic"의 진짜 의미

Pythonic은 **"코드 길이"가 아니라 "의도 투명성(intention transparency)"** 이 기준.

> 코드를 읽는 사람이 **"이 코드가 무엇을 하려는지"** 한눈에 파악할 수 있는가?

- 삼항/and: 의도를 더 명확히 해서 Pythonic ✅
- 의미 담긴 변수명/반복: 의도를 더 명확히 해서 이미 Pythonic ✅
- 무리한 1줄 압축: 의도를 가려서 **안티 Pythonic** ❌

### 🎯 "짧게 하면 안 좋은" 케이스들

#### 케이스 1: 의미 담긴 변수명을 희생하며 압축

```python
# ❌ 1줄 압축 (의도 가려짐)
return self.derivative()(self.input.data) * upstream_grad

# ✅ 3줄 (변수명이 의도 전달 — 더 Pythonic)
x = self.input.data           # "입력 데이터"
df = self.derivative()        # "도함수 객체"
local_deriv = df(x)           # "국소적 미분값"
return local_deriv * upstream_grad
```

- 중간 변수 `x`, `df`, `local_deriv`는 **의도를 담은 이름** — 디버깅/가독성에 유용
- 1줄 압축하면 이 의미가 사라짐 → "짧게 = 안 좋음"

#### 케이스 2: 반복을 무리게 루프로 묶기

```python
# ❌ 루프로 묶기 (오히려 안 읽힘)
cases = [(np.array(1.0), "ndarray"), (None, "None 허용")]
for val, desc in cases:
    v = Variable(val)
    print(f"Variable({val}): OK ({desc}) → data={v.data}")

# ✅ 반복 print (데모의 본질 — 각 케이스 명시)
x_ok = Variable(np.array(1.0))
print(f"Variable(np.array(1.0)): OK (ndarray) → x_ok.data = {x_ok.data}")
x_none = Variable(None)
print(f"Variable(None): OK (None 허용) → x_none.data = {x_none.data}")
```

- 데모는 **각 케이스가 무엇을 실증하는지** 명시가 핵심 → 반복이 의도 전달
- 루프로 묶으면 "각 케이스의 의미"가 묻힘 → "짧게 = 안 좋음"

### 🎯 판단 휴리스틱 — "짧게" vs "그대로"

질문: **"더 짧게 만들면 의도가 더 잘 드러나는가, 가려지는가?"**

| 답 | 행동 |
|---|---|
| 더 잘 드러남 | ✅ 짧게 (삼항, and 등) |
| 가려짐 | ❌ 그대로 (의미 변수, 반복) |
| 모호함 | ⚠️ 취향 영역 — 팀 합의 or 주석으로 보강 |

### 🎯 핵심 키워드

`#Pythonic` `#파이써닉` `#의도투명성` `#intention-transparency` `#짧게≠좋음` `#가독성` `#메타원칙` `#항목2-3안티테제스` `#변수명의미` `#PEP20`

### 🔗 관련

- 항목 2 (삼항), 항목 3 (and) — "짧게가 좋은" 케이스 (이 항목의 대척점)
- [PEP 20 — The Zen of Python](https://peps.python.org/pep-0020/) — "Readability counts"
- step09 `rezero/steps/step09.py` — 스캔 결과 "이미 Pythonic" 4곳 발견의 계기

---

## 5. 튜플 언패킹 — "짝인 값 한 줄로 회수"

### 📖 일반 규칙

**같은 맥락의 짝인 값들을 동시에 회수** → 튜플 언패킹(`a, b = x, y`)으로 한 줄 표현.
두 값이 "짝"이라는 구조가 코드에 드러남.

```python
# ❌ 2줄 — 같은 맥락인데 분리된 것처럼 보임
x = f.input
y = f.output

# ✅ 튜플 언패킹 — "input/output을 한 쌍으로 회수" 의도가 구조로 드러남
x, y = f.input, f.output
```

### 🎯 왜 Pythonic한가 — 항목 4 (Pythonic ≠ 짧게)의 양면 예시

항목 4에서 "짧게 ≠ 좋음"이라 했지만, **이 케이스는 "짧게 = 의도 더 명확"** 인 예시:
- 2줄: "input 할당, output 할당" — 별개 연산처럼 보임
- 1줄: **"input/output을 짝으로 회수"** — 같은 맥락(현재 Function의 입출력)이라는 구조 전달

→ 항목 4의 휴리스틱("짧게 하면 의도가 더 잘 드러나는가?")에 정확히 부합하는 "짧게 = 좋음" 사례.
**양면성**: Pythonic은 줄 수가 아니라 "의도 투명성"이 기준이라는 걸 더 명확히 함.

### 🎯 언제 튜플 언패킹을 쓰나

| 상황 | 언패킹? |
|---|---|
| 같은 맥락의 짝 (input/output, key/value) | ✅ |
| 여러 값 동시 회수 (`a, b, c = func()`) | ✅ |
| 서로 다른 관심사의 값 | ❌ (분리) |
| 짝이지만 각각 후속 처리가 길면 | ⚠️ 케이스 바이 케이스 |

### 🎯 DeZero/rezero 등장 지점

#### step09 — `fill_grad` 루프 내 input/output 회수 (★ 이 항목의 계기)

브로 제안: *"책에서 스트럭처드 바인딩 스럽게 한 줄로 표기했던 것 같은데?"*
→ 정확함. 튜플 언패킹 (구조화 바인딩). 책 원본 step08/step09 모두 `x, y = f.input, f.output` 한 줄.

```python
# step09 fill_grad 루프
while worklist:
    f = worklist.pop()
    x, y = f.input, f.output          # ★ 튜플 언패킹 — 짝 회수
    ...
```

cf. JavaScript의 구조 분해 할당(`const {a, b} = obj`)과 같은 철학 — "여러 값을 구조적으로 바인딩".

### 🔑 핵심 키워드

`#튜플언패킹` `#tuple-unpacking` `#구조화바인딩` `#structured-binding` `#짝회수` `#한줄표현` `#Pythonic` `#항목4양면`

### 🔗 관련

- 항목 4 (Pythonic ≠ 짧게) — "짧게 = 좋음" 양면 예시
- JavaScript 구조 분해 할당 (destructuring assignment) — 같은 철학
- step09 `rezero/steps/step09.py` `fill_grad` — 적용 사례

---

## 6. import 위치 (모듈 최상단 vs 함수 지역) + 순환 참조

### 📖 기본 규칙 — 모듈 최상단이 기본 (PEP 8)

PEP 8: **모든 import는 파일 최상단에** (모듈 docstring 직후, 다른 코드 이전).

```python
"""모듈 docstring"""

from abc import ABC              # ★ 최상단 — 표준 라이브러리
from functools import reduce
import numpy as np               # 서드파티

# 그 다음에 코드
```

### 🎯 예외 — 함수 지역 import (local import)

특정 상황에선 **함수 내부**에서 import. 언제?

#### 1. ★ 순환 참조 (circular import) 회피 — 가장 흔한 이유

A와 B가 서로 import할 때, 모듈 최상단에 두면 **부분 초기화 에러** 발생:

```python
# a.py
from b import b_func      # ← a 로드 중 b 로드 → b 로드 중 a 로드 시도
                          #   근데 a는 아직 다 안 끝남 → b_func 정의 안 됨 → ImportError

def a_func():
    from b import b_func  # ★ 지역 import — 함수 호출 시점엔 a/b 다 로드됨. 안전.
    b_func()
```

**★ 순환 참조는 "무한 루프"가 아니다**:
- 파이썬은 모듈 import 시작 즉시 `sys.modules`에 (빈) 모듈 객체 등록
- b에서 `from a import` 시도 → `sys.modules['a']` 존재 → **재귀 안 하고 캐시 객체 사용**
- 근데 그 객체엔 아직 `a_func`이 없음 → `ImportError: cannot import name 'a_func'`
- 즉 **sys.modules 캐시가 무한 루프를 막지만, "부분 초기화로 인한 미묘한 ImportError"** 발생

#### 2. 무거운 모듈 선택적 로딩

```python
def export_pdf(data):
    import matplotlib         # ← PDF 내보낼 때만 로딩 (다른 기능엔 불필요)
    ...
```

#### 3. 이름 충돌 회피 / 스코프 제한

모듈 네임스페이스에 노출시키지 않고 함수 내에서만 이름 사용.
(브로 짐작 "모듈 범위 아닌 함수 지역 범위에서 이름 룩업 유지" — 이 케이스)

### 🎯 정적 언어 vs 동적 언어 (Python) — 결정적 차이

브로 통찰: *"정적 로딩이면 컴파일러/링커가 순환 끊어주지 않나?"* → ★ 맞음.

| 언어 | 순환 참조 처리 |
|---|---|
| **C/C++ (정적)** | 컴파일러/링커가 **빌드 시점** 감지 → 에러 또는 자동 해결 (전방 선언 등) |
| **Java** | 컴파일러가 클래스 의존성 그래프 분석. 순환 허용하지만 JVM 로딩 순서로 해결 |
| **Python (동적)** | **런타임에만 import 실행** → 순환 발생 시 부분 초기화 모듈 사용 → 미묘한 `ImportError` |

→ 정적 언어는 빌드 타임에 순환 처리, Python은 런타임이라 **미리 알기 어렵고 발생하면 미묘한 에러**.
그래서 Python 개발자가 **지역 import로 수동 대처**해야 하는 경우가 생김.

### 🎯 DeZero/rezero 등장 지점

#### step09 — `pipe()` 헬퍼의 functools import (★ 이 항목의 계기)

브로 질문: *"함수 안에서 import 하는 이유? 모듈 범위 아닌 함수 지역 범위에서 이름 룩업 유지?"*
→ 답: 위 예외 상황 1~3이 주 이유. 근데 ★ **step09 pipe엔 이유 중 어느 것도 해당 안 함**:
- 순환 참조 없음 (functools는 표준 라이브러리)
- 무거운 모듈 아님
- 이름 충돌 위험 없음

→ 결론: **모듈 최상단으로 이동** (PEP 8 기본 + 일반적 관례).
원래 코드는 "관례적으로" 지역 import 썼으나, 이유 없는 관례는 항목 4("Pythonic ≠ 짧게")와 같은 결로 제거.

```python
# step09 — 최상단으로 이동
from functools import reduce    # ← 모듈 최상단 (PEP 8)

def pipe(value, *funcs):
    return reduce(lambda val, f: f(val), funcs, value)   # 본문은 순수 알고리즘만
```

### 🎯 판단 가이드라인 — 지역 import를 쓸까?

| 상황 | 지역 import? |
|---|---|
| 순환 참조 발생/우려 | ✅ (주된 해결책) |
| 무거운 모듈, 조건부 사용 | ✅ |
| 이름 충돌 위험 | ✅ |
| 일반적인 경우 (위 해당 없음) | ❌ 모듈 최상단 (PEP 8) |

→ 핵심: **"왜 지역 import하는가?" 이유가 명확하지 않으면 모듈 최상단이 기본**.

### 🔑 핵심 키워드

`#import위치` `#지역import` `#local-import` `#순환참조` `#circular-import` `#부분초기화` `#sys.modules` `#무한루프아님` `#정적vs동적` `#PEP8` `#선택적로딩` `#이름충돌`

### 🔗 관련

- [PEP 8 — Imports](https://peps.python.org/pep-0008/#imports) — "Imports are always put at the top of the file"
- [Python docs — The import system](https://docs.python.org/3/reference/import.html) — sys.modules 캐싱 메커니즘
- step09 `rezero/steps/step09.py` `pipe()` — 지역→최상단 이동 사례

---

## 7. 매직메서드는 클래스 안에 정의 — "클래스 밖 대입 비권장"

### 📖 일반 규칙

파이썬의 매직메서드(`__add__`, `__mul__`, `__repr__` 등)는 **클래스 정의 안에** 넣는 게 원칙.
클래스 밖에서 `ClassName.__method__ = func` 식으로 대입할 수는 있지만 **비권장**.

```python
# ✅ 클래스 안 정의 (원칙)
class Variable:
    def __add__(self, other):
        return add(self, other)


# ⚠️ 클래스 밖 대입 (가능은 하나 비권장)
class Variable: ...
def add(x0, x1): ...
Variable.__add__ = add      # ← 정의 밖에서 속성 대입
```

### 🎯 왜 클래스 안이 원칙인가 (4가지 이유)

| 이유 | 설명 |
|---|---|
| **1. 정적 분석 호환성** ★ | pyright/Pylance/mypy는 클래스 정의를 정적으로 분석. 클래스 밖 대입은 인식 못 함 → "지원하지 않는 연산자" 에러 + `type: ignore` 남발 |
| **2. 가독성** | "이 클래스가 지원하는 연산자"를 클래스 정의만 보고 즉시 파악 가능. 밖에 흩어져 있으면 찾아야 함 |
| **3. 서브클래싱** | 자식이 `super().__add__()` 호출할 때, 부모 정의가 클래스 안에 있어야 자연스러움 |
| **4. 관행** | 파이썬 생태계 전반 (NumPy, PyTorch, pandas 등) 이 클래스 안 정의가 표준 |

### 🎯 step20 실증 — pyright 11 에러 (클래스 밖 대입의 치명적 단점)

step20 1차 코드에서 책 원본 방식(`Variable.__add__ = add`)을 그대로 따랐더니 **pyright 11 에러** 발생:
```
Attribute "__add__" is unknown (reportAttributeAccessIssue)
Operator "*" not supported for types "Variable" and "Variable" (reportOperatorIssue)
```
→ 클래스 밖 대입은 pyright가 "Variable에 `__add__` 없다"고 판단. `a * b` 연산을 에러로 봄.
→ 11곳에 `# type: ignore` 달아야 하는데, 이건 rezero 원칙("정적 분석과 협력", `debugging.md`)에 정면 위반.

**해결**: 클래스 안에 정의하니 pyright **0 errors**. 깔끔.

### 🎯 왜 책 원본은 클래스 밖 대입을 택했나 (가설)

| 가설 | 설명 |
|---|---|
| **wrapper 함수 먼저 정의** | `__add__`가 `add` wrapper를 호출하니, `add`가 먼저 정의되어야 함. 근데 이건 실행 시점엔 문제 없음 (메서드는 호출 시 평가) |
| **설명 목적 분리** | "함수 wrapper → 연산자 연결" 두 단계를 분리해 보여주려는 의도 |
| **저자 코딩 스타일** | 일본어 원서의 다른 부분도 비슷한 경향 |

즉 책만의 특수한 선택이지, 일반적인 파이썬 관행이 아님.

### 🎯 언제 클래스 밖 대입이 (이론상) 의미 있나

사실 "반드시"는 없음. 하지만 드문 정당화 가능성:

- **런타임에 조건부로 매직메서드 추가** (예: 플러그인 시스템, 특정 조건에서만 `__add__` 지원)
- **서드파티 클래스 확장** (본인이 수정 못 하는 클래스에 매직메서드 추가 — 근데 몽키 패치라 위험)
- ★ DeZero/rezero에선 이런 케이스 없음 → 항상 클래스 안 정의.

### 🎯 DeZero/rezero 등장 지점

#### step20 — `Variable.__add__` / `Variable.__mul__` (★ 이 항목의 계기)

책 원본 방식 (비권장):
```python
class Variable: ...
def add(x0, x1): ...
Variable.__add__ = add      # 클래스 밖 대입 → pyright 11 에러
```

rezero 방식 (권장):
```python
class Variable:
    def __add__(self, other: "Variable") -> "Variable":
        return add(self, other)    # 클래스 안 정의 → pyright 0 에러
```

### 🔑 핵심 키워드

`#매직메서드` `#클래스안정의` `#클래스밖대입비권장` `#pyright정적분석` `#typeIgnore남발방지` `#operatorOverloading` `#식택스슈가` `#step20`

### 🔗 관련

- step20 `rezero/steps/step20.py` — `__add__`/`__mul__` 클래스 안 정의 (이 항목의 계기)
- `debugging.md` — "정적 분석과 협력하는 assert" (같은 결 — 정적 분석 도구와 잘 협력)
- `design_patterns.md` — "오버로딩" 용어 (매직메서드 = 연산자 오버로딩의 도구)

---

## 📖 용어집 (필요 시 확장)

| 용어 | 의미 |
|---|---|
| **빈 줄 (blank line)** | 엔터만 친 줄 (아무 내용 없음). PEP 8의 "Blank Lines" 규칙 대상. |
| **공백 문자 (space)** | 스페이스바 한 칸. 인라인 규칙(연산자 주변 등)은 별도. 빈 줄과 다름. ★ 브로가 "공백"이라 부른 건 빈 줄. |
| **논리 블록 (logical block)** | 함수 내에서 하나의 논리적 단위를 이루는 코드 묶음. 빈 줄로 시각적으로 분리. |
| **섹션 헤더 주석** | `# --- 섹션명 ---` 형태. 빈 줄과 결합해 섹션 경계 + 의미 동시 전달. |
| **코드 벽 (code wall)** | 빈 줄 없이 쭉 이어진 긴 코드. 가독성 떨어뜨리는 안티패턴. |
| **매직메서드 (dunder method)** | `__add__`, `__repr__` 등 밑줄 두 개(`__`)로 둘러싸인 특수 메서드. 파이썬 프로토콜(연산자 오버로딩 등)을 구현하는 도구. |
| **클래스 밖 대입** | `ClassName.__method__ = func` 식으로 클래스 정의 밖에서 속성을 대입하는 패턴. 가능하나 정적 분석기가 인식 못 해 비권장 (항목 7). |

---

## 🔗 연결 고리

- `LEARNING_NOTES.md` 각 step 섹션에서 relevant 스타일 주제로 링크
- `design_patterns.md` — 같은 "누적형 횡단 관심사" 구조 (디자인 패턴은 이쪽)
- `debugging.md` — 같은 구조 (검증/예외 메커니즘은 이쪽)
- `AGENTS.md` "학습 관리 워크플로" — notes/ 디렉터리 역할
