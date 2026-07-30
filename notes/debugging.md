# 🐛 디버깅 노트 — 파이썬 런타임 검증/디버깅 메커니즘

> DeZero(및 `rezero`) 구현을 진행하며 마주친 **파이썬의 런타임 검증·디버깅 메커니즘**을 정리하는 누적형 레퍼런스.
> `design_patterns.md`와 같은 구조 — 여러 step에 걸쳐 재등장하는 횡단 관심사라 단일 파일에 누적 관리.
>
> 다루는 범위:
> - 언어 차원의 검증 도구 (`assert`, `__debug__`, `-O` 최적화)
> - 예외/에러 메커니즘 (RecursionError, RuntimeError 등)
> - 향후: logging, traceback, pdb, weakref 기반 메모리 디버깅(step17+), etc.
>
> - 일반적인 메커니즘 설명 (CPython 작동 원리 등)
> - DeZero/rezero의 **어느 부분**에 등장하는지 (step별 위치)
> - 코드 스니펫은 최소, 핵심 구조만

---

## 📋 인덱스

| # | 주제 | 최초 등장 | 분류 |
|---|---|---|---|
| 1 | `assert` + `-O` 모드 + `__debug__` (릴리스 빌드에선 증발) | step08 | 검증 (검증문) |
| 2 | `RecursionError` + `sys.getrecursionlimit()` (재귀 깊이 한계) | step08 | 예외 (런타임 제약) |
| 3 | fail-fast + 부작용 회피 (검증 위치 원칙, guard clause) | step08 | 검증 (위치/순서) |

---

## 1. `assert` + `-O` 모드 + `__debug__` — "릴리스 빌드에선 증발하는 검증문"

### 📖 일반 설명

파이썬의 `assert`는 **"이 조건이 위반되면 내 코드에 버그가 있다"** (프로그래머의 실수 전용)를 표현하는 구문.
사용자 입력이나 런타임 데이터 검증이 아닌, **개발/디버깅 중 불변조건(invariant) 점검** 용도.

**핵심 ★ — 파이썬에도 "디버그/릴리스 구분"이 있다** (C/C++/Java처럼):
단지 그 스위치가 좀 숨어 있어서 모르기 쉽다. 스위치는 `-O` (optimize) 커맨드라인 플래그.

```bash
python script.py       # 일반 모드 — assert 작동 (__debug__ = True)
python -O script.py    # 최적화 모드 — assert가 "코드에서 증발" (__debug__ = False) ★
python -OO script.py   # 최적화 + docstring도 제거
```

**작동 원리**:
- `-O` 플래그 → CPython이 컴파일 시 `__debug__` 내장 상수를 `False`로 설정
- 동시에 **`assert` 문을 소스 레벨에서 아예 제외** (실행이 아니라 컴파일에서 사라짐)
- → assert는 "개발 중엔 검사하지만, 프로덕션 빌드에선 제로 비용"이라는 C/C++의 `assert`/`NDEBUG`와 같은 철학

### 🎯 핵심 교훈 2가지

#### 교훈 1: `assert`엔 **순수 조건만** — 부작용(side effect) 넣으면 재앙

`-O` 모드에서 assert 전체가 사라지므로, **assert 안의 표현식 자체가 평가되지 않음**.
부작용 있는 코드를 넣으면 릴리스 빌드에서 동작이 완전히 달라짐:

```python
funcs = [1, 2, 3]
assert funcs.pop() == 3   # ❌ -O 모드에서 pop 자체가 안 일어남!
```

**실증 (2026-07-29, step08 학습 중)**:
```
--- 일반 모드 ---
assert 이후 funcs = [1, 2]          # pop 실행됨 (assert 조건 평가)

--- -O 모드 (assert 제거) ---
assert 이후 funcs = [1, 2, 3]        # ★ pop 자체가 안 일어남 — 리스트 그대로!
```

→ "assert엔 순수 조건만"은 미적 추천이 아니라 **릴리스 빌드 정합성** 문제.

#### 교훈 2: 런타임 데이터 검증엔 `assert` 쓰면 안 됨

`assert`는 "프로그래머의 논리적 가정" 검증용. **사용자 입력, 파일 내용, 네트워크 데이터** 등
"-O 모드에서 사라지면 치명적인" 검증엔 `if ...: raise`를 써야 함.

```python
# ❌ assert — -O 모드에서 검증 자체가 사라짐 (보안/정합성 구멍)
def divide(a, b):
    assert b != 0
    return a / b

# ✅ 명시적 raise — 최적화 모드와 무관하게 항상 검증
def divide(a, b):
    if b == 0:
        raise ValueError("b must not be zero")
    return a / b
```

**구분 기준**:
| 용도 | 도구 | 예 |
|---|---|---|
| 프로그래먘 논리 가정 (불변조건) | `assert` | `assert self.input is not None` (잘못되면 내 코드 버그) |
| 런타임 데이터/사용자 입력 | `if: raise` | `if b == 0: raise ValueError(...)` (잘못되면 호출자 책임) |

### 🎯 DeZero/rezero 등장 지점

#### step08 — `fill_grad()` 내 검증 (3종, 용도별 분리)

```python
# step08 fill_grad — 도입부 맨 앞 (검증 A: 사용자 오용)
if start_var.creator is None:
    raise RuntimeError("역전파할 계산 그래프가 없습니다...")

# ... upstream 설정 후 루프 내부 (검증 B/C: 불변조건)
assert x is not None and y is not None, "f.input/f.output must be set (__call__ should have run)"
assert y.grad is not None, "y.grad must be filled (start or previous iteration sets it)"
```

★ step08의 핵심 결정 — 검증 3종을 **용도별로 분리**:
- **(A)** start_var.creator None → `if/raise RuntimeError` (사용자 오용, `-O`에서도 살아남아야)
- **(B)(C)** f.input/output/y.grad None → `assert` (프로그래먘 논리 버그, `-O`에서 사라져도 안전)
- ★ (A)는 **도입부 맨 앞**에 둠 (fail-fast / 부작용 회피 — 항목 3 참고)
상세: REZERO_CHANGES.md 항목 16번

#### REZERO_CHANGES 항목 1번 — assert 가드의 런타임 역할
step07 타입 힌트 세트 도입 중 `Variable.backward()`에서 `f.backward(self.grad)` 호출 시
`self.grad: Optional` → None 가능한데 `Function.backward(upstream: np.ndarray)`는 None 안 받음.
→ `assert` 가드로 방어. 단, 이것도 `-O`에선 사라지므로 "프로덕션 보장용"은 아니고 "개발 중 조기 발견용".

### 🎯 ★ assert의 3번째 용도 — 정적 분석과 "협력" (타입 좁히기)

브로 통찰 (step10): *"정적분석 피해가다니... 세맨틱까지 분석해서 빨간줄?"*
→ ★ 정확히 봄. assert는 단순 "런타임 검증"을 넘어 **정적 분석기(Pylance/pyright)와 협력하는 도구**.

#### 정적 분석의 한계 — 런타임 부작용 추적 불가

```python
self.grad: Optional[np.ndarray] = None   # 타입은 Optional

fill_grad(y)                              # ★ 런타임 부작용: x.grad 채움 (정적 분석은 모름!)
np.allclose(x.grad, num_grad)             # ← 정적 분석: "Optional이니 None 가능" 경고
```

정적 분석이 **못 하는 것**:
- 런타임 부작용 추적 (`fill_grad`가 x.grad 채운다는 것)
- 논리적 추론 ("테스트에선 None일 수 없다")
- 이건 **정지 문제(Halting Problem)** 급이라 근본적으로 불가능

→ 그래서 정적 분석은 **보수적** — 모르면 일단 경고. 안전 측 선택.

#### assert로 정적 분석에게 "알려주기" — 타입 좁히기

```python
fill_grad(y)
assert x.grad is not None                 # ★ "이 시점에선 None 아니다" — 정적 분석에게 알림
np.allclose(x.grad, num_grad)             # 이제 정적 분석도 OK (Optional → np.ndarray로 좁혀짐)
```

★ 핵심: assert는 정적 분석이 **이해할 수 있는 언어**로 상태를 번역해주는 것. Pylance는 assert 이후 코드에서 `x.grad`를 `np.ndarray`로 추론 (타입 좁히기, type narrowing).

#### `assert` vs `# type: ignore` — 협력 vs 억압

| 관점 | `# type: ignore` | `assert x is not None` |
|---|---|---|
| 정적 분석과의 관계 | **억압** — "닥쳐, 내가 안다" | ★ **협력** — "이 시점에선 None 아니야, 이유는 이거" |
| 의미 | 경고 무시 (왜인지 모름) | 불변조건 명시 |
| 런타임 검증 | ❌ 아무것도 안 함 | ★ 진짜 None이면 AssertionError |
| 버그 숨김 위험 | 높음 (다른 에러도 묻힘) | 낮음 (정확히 이 조건만) |
| 코드 블록 전파 | 매 줄마다 써야 | ★ 하나로 아래 전체에 전파 |

→ assert가 **일석삼조**: 정적 분석 만족 + 불변조건 명시 + 런타임 검증.

#### DeZero/rezero 등장 지점 (step09~10)

step10 테스트 4곳 (gradient check 3 + 데모 1)에서 동일 패턴:
```python
fill_grad(y)
assert x.grad is not None            # ★ 방어막 (Pylance 타입 좁히기)
assert np.allclose(x.grad, num_grad)
```

cf. 이건 "방어막 3번(None 가드)"과 짝 — None 가드는 `if ... raise` (사용자 오용),
assert는 프로그래먘 불변조건. 같은 None 처리지만 **용도에 따른 도구 선택** (debugging.md 원칙 일관).

#### ★ 변형 — `assert isinstance(result, T)` 타입 좁히기 (step12 추가)

step10에서 쓴 패턴은 **값 검증** (`assert x.grad is not None` — "None 아니다").
step12에선 **타입 검증** 변형이 등장 (`assert isinstance(result, Variable)` — "이 타입이다").

```python
# step12 wrapper — __call__ 반환은 Variable | list[Variable] (둘 다 가능)
def add(x0: Variable, x1: Variable) -> Variable:
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result    # ★ 이 줄부터 Pylance가 result를 Variable로 추론 (Union → Variable 좁힘)
```

브로 통찰 (step12): *"assert로 Pylance 경고 없애는 거, 이거 이디엄스럽지 않아?"*
→ ★ 맞음. **Type Narrowing은 Python typed 생태계의 정식 이디엄** (mypy/Pylance 매뉴얼에 명시된 패턴).

##### `isinstance` 좁히기 vs `is not None` 좁히기

| | `assert x is not None` (step10) | `assert isinstance(x, T)` (step12) |
|---|---|---|
| 좁히는 것 | `Optional[T]` → `T` | `Union[A, B]` → `A` (또는 B) |
| 상황 | "None일 수 있지만 여기선 아니다" | "여러 타입 가능하지만 여기선 이거다" |
| 런타임 검증 | None이면 AssertionError | 다른 타입이면 AssertionError |
| DeZero 사용처 | grad/creator None 가드 | wrapper 반환값 타입 보장 |

→ 두 변형 모두 같은 이디엄 (Type Narrowing). 상황에 따라 `is not None` / `isinstance` 선택.

##### 3가지 Type Narrowing 도구 비교

| 도구 | 코드 | 적합한 상황 |
|---|---|---|
| **`assert isinstance`** ★ | `assert isinstance(x, T)` | "무조건 T야" — 단일 타입 보장 (step12 wrapper) |
| **`@overload`** | 시그니처 여러 개 선언 | "N개 입력 → M개 출력" 정밀 매핑 (verbose) |
| **`# type: ignore`** ❌ | 경고 무시 | 금지 — 진짜 버그도 숨김 |

→ 브로 감각대로 **assert가 가장 이디엄스럽고 가벼운 선택**. 한 줄에 정적 만족 + 런타임 검증 + 문서화(메시지) 3효과.

### 🔑 핵심 키워드

`#assert` `#-O` `#-OO` `#__debug__` `#NDEBUG` `#최적화모드` `#릴리스빌드` `#불변조건` `#invariant` `#부작용금지` `#검증문` `#C/C++비교` `#타입좁히기` `#type-narrowing` `#정적분석협력` `#vs-type-ignore` `#런타임부작용추적불가` `#정지문제` `#isinstance좁히기` `#assert-isinstance` `#Union좁히기` `#wrapper반환타입` `#step12추가` `#이디엄` `#브로통찰`

### 🔗 관련

- C/C++의 `assert()` 매크로 + `NDEBUG` 매크로 (같은 철학 — 디버그 빌드에선 작동, 릴리스에선 제거)
- Java의 `assert` (JVM `-ea`/`-da` 스위치로 on/off — 파이썬의 `-O`와 유사)
- PEP 시 참고: 파이썬 공식 문서 [assert statements](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)
- step10 `rezero/steps/step10.py` — pytest 테스트에서 assert로 타입 좁히기 적용 (4곳)
- step12 `rezero/steps/step12.py` — wrapper(add/square)에서 `assert isinstance(result, Variable)` 타입 좁히기 적용

---

## 2. `RecursionError` + `sys.getrecursionlimit()` — "재귀 깊이 한계"

### 📖 일반 설명

파이썬(CPython)은 **재귀 호출 깊이에 기본 한계 1000**을 둔다. 이를 넘으면 `RecursionError` 예외 발생.

```python
def f():
    f()
f()
# RecursionError: maximum recursion depth exceeded
```

**왜 한계를 두나?**:
- CPython은 함수 호출마다 **C 스택(C call stack)** 도 소모함
- 한계 없이 두면 C 스택 오버플로 → **세그폴트(크래시)** 로 직결
- 파이썬이 `RecursionError` 예외로 미리 안전장치를 걸어, 크래시 전에 잡을 수 있게 함

**한계 확인/변경**:
```python
import sys
sys.getrecursionlimit()   # 1000 (기본)
sys.setrecursionlimit(5000)   # 한계 올리기 가능
```

**★ 한계를 올린다고 안전한 건 아님**:
- 파이썬의 카운터는 올렸지만, **C 스택은 운영체제/스레드에 따라 별도 한계**가 있음
- 너무 크게 올리면 `RecursionError`를 안 내고 **진짜 세그폴트** 발생 가능
- 특히 스레드마다 C 스택 크기가 다름 (메인 스레드가 보통 더 큼)
- → 깊은 재귀가 진짜 필요하면 **반복문 + 명시적 스택**이 정답

### 🎯 DeZero/rezero 등장 지점

#### step07 → step08 — 역전파 자동화의 재귀 → 반복문 전환 (★ 이 노트의 직접 계기)

**step07** (재귀적 `backward`):
```python
def backward(start_var):
    f = start_var.creator
    if f is not None:
        x = f.input
        x.grad = f.backward(start_var.grad)
        backward(x)   # ★ 재귀 — 그래프 깊이 = 재귀 깊이
```

**step08** (반복문 `backward`):
```python
def backward(start_var):
    funcs = [start_var.creator]   # 명시적 스택 (리스트 = 힙에 저장)
    while funcs:
        f = funcs.pop()
        x, y = f.input, f.output
        x.grad = f.backward(y.grad)
        if x.creator is not None:
            funcs.append(x.creator)   # 루프로 처리, 재귀 아님
```

**왜 전환했나?**:
- DeZero의 계산 그래프는 "합성 함수 연쇄" → **깊이가 선형으로 늘어날 수 있음**
- 예: 긴 RNN 시퀀스, 깊은 ResNet(100층+) → 재귀 깊이 수천
- step07 재귀 버전은 그래프 깊이 1000 넘으면 `RecursionError`
- step08 반복문 버전은 리스트(힙)에 스택 → 깊이 제한에서 자유로움

**실증 (2026-07-29, step08 학습 중)**:
```
sys.getrecursionlimit() = 1000
RecursionError 잡음: maximum recursion depth exceeded
```

### 🎯 핵심 교훈

**"깊이가 입력 크기에 비례하는 재귀는 위험하다"**:
- 재귀가 자연스러운 알고리즘(트리 순회 등)이라도, 깊이가 무한히 커질 수 있으면 반복문 고려
- 특히 프레임워크/라이브러리 코드는 사용자가 얼마나 깊은 구조를 만들지 예측 불가
- DeZero가 step07(재귀) 직후 바로 step08(반복문)로 넘어가는 이유 — 일반적 프레임워크 설계 원칙

**참고 — 다른 언어의 재귀 한계**:
| 언어 | 재귀 한계 | 특징 |
|---|---|---|
| Python (CPython) | ~1000 (기본, 조정 가능) | C 스택 연동, 꼬리재귀 최적화 없음 |
| JavaScript (V8 등) | ~10000~16000 (엔진별 상이) | 꼬리재귀 최적화 스펙 있으나 미구현 많음 |
| Java | JVM 스택에 의존 (~n천~수만) | `-Xss` 플래그로 조절 |
| C/C++ | OS/스레드 스택에 의존 | 스택 오버플로 = 세그폴트 (예외 안 잡힘) |
| Scheme/Lisp | 사실상 무한 (꼬리재귀 최적화 의무) | 반복문을 재귀로 표현하는 패러다임 |

→ Python은 "재귀는 가급적 얕게, 깊어지면 반복문"이 합의된 관용구.

### 🔑 핵심 키워드

`#RecursionError` `#sys.getrecursionlimit` `#sys.setrecursionlimit` `#재귀한계` `#스택오버플로` `#세그폴트` `#C스택` `#반복문전환` `#명시적스택` `#꼬리재귀` `#tail-call` `#언어비교`

### 🔗 관련

- step08 `rezero/steps/step08.py` — 반복문 전환의 실제 코드
- CPython 소스: `ceval.c`의 `Py_CheckRecursionLimit` (한계 카운팅 로직)
- PEP 시 참고: [bpo-31461](https://bugs.python.org/issue31461) — `RecursionError` 관련 개선 이력

---

## 3. fail-fast + 부작용 회피 — "검증 위치 원칙" (guard clause)

### 📖 일반 설명

**Fail-fast (빠른 실패)**: 잘못된 입력/상태를 감지하면 **가능한 한 빨리** 실패시키는 설계 원칙.
검증을 미루지 않고 함수 **도입부**에서 바로 거부 → 후속 작업(wasted work)도 부작용도 없음.

**부작용(side effect) 회피와의 결합**: 검증이 부작용 있는 코드 **뒤에** 오면, 실패하더라도
이미 외부 상태를 변경한 뒤라 "실패한 연산이 흔적을 남김". 도입부에서 검사하면
**실패한 연산은 부작용을 일으키지 않음**(transactional semantics)까지 보장.

```python
# ❌ 나쁜 예 — 검증이 부작용 뒤에: 실패해도 start_var.grad를 변경해버림
def fill_grad(start_var):
    start_var.grad = np.ones_like(start_var.data)   # 부작용 (먼저 실행됨)
    if start_var.creator is None:                    # 검증 (나중)
        raise RuntimeError(...)
    ...

# ✅ 좋은 예 — guard clause (도입부에서 검사): 부작용 없이 즉시 실패
def fill_grad(start_var):
    if start_var.creator is None:                    # ★ 도입부에서 검증
        raise RuntimeError(...)
    start_var.grad = np.ones_like(start_var.data)    # 부작용은 검증 통과 후에만
    ...
```

### 🎯 핵심 원칙 2가지

1. **Fail-fast**: 잘못된 입력이면 가장 빨리 실패. 검증을 함수 도입부(guard clause)에 배치.
2. **Transactionality**: 실패한 연산은 외부 상태를 변경하지 않음. 부작용 있는 코드는 **검증 통과 후**에 실행.

→ 둘은 같은 말의 양면: **"검증을 앞당기면 부작용 회피까지 자동으로 따라온다."**

### 🎯 DeZero/rezero 등장 지점

#### step08 — `fill_grad()` 도입부 검증 (★ 이 노트의 직접 계기)

```python
def fill_grad(start_var, upstream_grad=None):
    # ★ 검증 (A) — 함수 도입부 맨 앞 (guard clause / fail-fast)
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )
    # upstream 설정 (부작용)은 검증 통과 후에
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    ...
```

★ 브로 지적 (2차) — 처음엔 upstream 설정 **뒤에** 검사를 뒀으나:
> "오류 체크는 메서드 도입부 초반에 바로 해주는 게 나은 것 아니냐?"

→ 맞음. 도입부로 옮기니 두 가지가 한 번에 해결:
1. **Fail-fast**: 잘못된 입력이 wasted work 없이 즉시 실패
2. **부작용 회피**: 실패한 호출이 `start_var.grad`를 건드리지 않음 (transactional)

**실증 (step08 검증)**:
```
호출 전 x.grad = None
fill_grad(x) → RuntimeError (fail-fast, 도입부에서 즉시)
호출 후 x.grad = None  ← ★ 부작용 없음 (이전 위치였으면 ones_like로 채워졌을 것)
```

### 🎯 guard clause (보호 구문) — 이 패턴의 이름

"함수 도입부에 `if ...: raise/return` 형태로 조기 거부/반환을 두는 구조"를
**guard clause** (보호 구문)라 부름. 핵심 효과:
- **중첩 감소**: `if valid: ...` 깊은 들여쓰기 대신, "아니면 빠져나감"으로 평평한 구조
- **의도 명확**: "이 조건이 아니면 여기서 끝"이 코드 구조로 드러남
- **fail-fast 자동**: 검증이 항상 도입부에 오는 구조적 강제

```python
# guard clause 패턴 (flat)
def f(x):
    if x is None: raise ValueError(...)    # guard
    if x < 0: raise ValueError(...)        # guard
    # 본문 (평평)
    return x * 2

# vs 중첩 if (deep) — 회피
def f(x):
    if x is not None:
        if x >= 0:
            return x * 2
    raise ValueError(...)
```

### 🔑 핵심 키워드

`#fail-fast` `#빠른실패` `#guard-clause` `#보호구문` `#부작용회피` `#transactional` `#검증위치` `#도입부검증` `#wasted-work` `#early-return` `#조기반환` `#부작용` `#side-effect`

### 🔗 관련

- [exploration_16_side_effect.md](./exploration_16_side_effect.md) — 부작용(side effect) 개념 자체
- REZERO_CHANGES.md 항목 16번 — step08 fill_grad 검증 위치 개선
- Refactoring (Martin Fowler) — "Replace Nested Conditional with Guard Clauses" 기법

---

## 📖 용어집 (필요 시 확장)

| 용어 | 의미 |
|---|---|
| 불변조건 (invariant) | 코드의 특정 지점에서 항상 참이어야 하는 조건. assert로 검증하는 전형적 대상. |
| 부작용 (side effect) | 표현식 평가가 값을 반환하는 것 외에 상태를 바꾸는 것 (예: `list.pop()`, `print()`). assert 조건에 넣으면 `-O` 모드에서 사라짐. |
| `-O` 모드 | CPython의 최적화 모드. `__debug__ = False` + assert 제거. `-OO`는 추가로 docstring 제거. |

---

## 🔗 연결 고리

- `LEARNING_NOTES.md` 각 step 섹션에서 relevant 디버깅 주제로 링크
- `design_patterns.md` — 같은 "누적형 횡단 관심사" 구조 (디자인 패턴은 이쪽)
- `AGENTS.md` "학습 관리 워크플로" — notes/ 디렉터리 역할
- [exploration_16_side_effect.md](./exploration_16_side_effect.md) — "부작용" 번역 비판.
  항목 1(assert + 외부 효과 충돌)에서 파생. assert에 side effect를 넣으면 안 되는 "진짜 이유"를 번역어 관점에서 재조명.
