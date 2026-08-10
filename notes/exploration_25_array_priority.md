# 탐구 25 — `__array_priority__`의 정체: 책의 매직 넘버 `200`은 왜 불필요해졌나

> **시점**: step21 진행 중 (2026-08-10)
> **상태**: 📚 학습용 심화 노트 (브로 "찜찜하다" 감각에서 파생)
> **트리거**: 브로 반응 2종 —
>   1. "200이란 매직스러운 숫자값의 의미도 잘 모르겠고, 어떻게 저렇게 돼는 것인지 설명이 전혀없으니"
>   2. ★ "200을 사용하는 부분이 뭔가 굉장히 부자연스럽게 느껴지기도"
> **관련**: step21 (연산자 오버로드 2 — ndarray/scalar 혼합 연산)

## 📌 왜 이 탐구를 했나 — "찜찜함"의 정체

책 step21이 `__array_priority__ = 200`이라는 매직 넘버를 슥 보여주고 넘어감. "이렇게 하면 됩니다" 식.
브로 직감: **"왜 200이지? 어디서 온 숫자야? 이거 없으면 안 돼?"** — 아무 설명 없는 매직 넘버는 학습을 방해함.

이 노트의 결론부터 말하면: **현대 NumPy 환경에선 `__array_priority__ = 200`은 불필요**. `__rmul__`/`__radd__`만으로 충분.
rezero는 `200`을 **버리고**, 왜 버렸는지를 기록으로 남긴다. ★ 이 과정 자체가 "책 코드도 검증하라"는 교훈.

---

## 🎯 핵심 결론 (3줄 요약)

1. `__array_priority__`는 **과거 NumPy**(다른 타입을 만나도 `NotImplemented`를 안 반환하던 시절)를 위한 핵(hack).
2. **현대 NumPy**(Python 3.12 + 최신 NumPy)는 파이썬 표준 디스패치를 잘 존중 → `__rmul__`만 있으면 충분.
3. 따라서 rezero는 `200` 버림. "왜 버렸는지"를 이 문서에 영구 보존.

---

## 1. ufunc란? (가벼운 정리 — 본 주제 벗어나니 깊이 안 파)

**universal function**의 약자. "원소별(element-by-element)로 동작하는 함수".

```python
# 일반 파이썬 리스트
[1,2,3] + [10,20,30]  # → [1,2,3,10,20,30] (이어붙기)

# NumPy ndarray + ndarray
np.array([1,2,3]) + np.array([10,20,30])  # → [11, 22, 33] ★ 원소별 덧셈

# 실제로 + 연산은 np.add라는 ufunc가 처리
np.add(np.array([1,2,3]), np.array([10,20,30]))  # 동일 결과
```

**핵심**: NumPy의 거의 모든 연산(`+`, `*`, `/`, `np.sin`, `np.sqrt`...)은 사실 ufunc.
연산자(`+`)는 ufunc(`np.add`)의 신택스 슈가.

> ufunc를 더 깊이 파면 `np.frompyfunc`(직접 ufunc 만들기), 브로드캐스팅 규칙, 형 캐스팅 등이 나오지만,
> **이 노트의 본 주제("200 불필요")를 벗어나므로 여기서 정리**. ufunc 자체가 궁금하면 NumPy 공식 문서 참조.

참고: [NumPy ufuncs 공식 문서](https://numpy.org/doc/stable/reference/ufuncs.html), [W3Schools ufunc 기초](https://www.w3schools.com/python/numpy/numpy_ufunc.asp)

---

## 2. 세 가지 메커니즘의 역사적 계층

브로가 "찜찜하다"고 한 이유: **세 가지 비슷한 메커니즘이 역사적으로 겹쳐 있어서**. 한눈에 보는 표:

| 세대 | 메커니즘 | 시대 | 철학 |
|---|---|---|---|
| **1세대** | `__rmul__`/`__radd__` (Python 표준) | 파이썬 태초 | 좌변이 `NotImplemented` 반환하면 우변이 역순으로 처리 |
| **2세대** | `__array_priority__` | NumPy 고대 (~2017 이전) | "NumPy가 무식하게 삼키지 않게 협상" — 구식 핵 |
| **3세대** | `__array_ufunc__` (NEP 13, 2017) | 현대 | "ufunc 자체를 통째로 가로채기" — 가장 강력/깔끔 |

**왜 3세대나 필요했나?** — 각각이 이전 세대의 한계를 보완하며 진화:

### 1세대: 파이썬 표준 `__rmul__`

```
a * b → a.__mul__(b) 시도
      → a가 NotImplemented 반환 → b.__rmul__(a) 시도 (역순)
      → 둘 다 못 하면 TypeError
```

이게 파이썬 표준 디스패치 규칙. **이것만 있으면 되는 거 아닌가?** — 아니, 과거엔 안 됐음.

### 2세대: `__array_priority__` — 왜 필요했나

**문제 상황 (과거 NumPy)**:
```
ndarray * Variable
→ ndarray.__mul__(Variable) 시도
→ ★ 과거 NumPy는 "이 타입 모르겠다"고 NotImplemented를 안 반환함.
→ 대신 "적극적으로" Variable을 ndarray로 캐스팅하려 시도.
→ Variable이 data 속성(ndarray)을 가지고 있어서 캐스팅이 "성공해버림"
→ 결과: Variable이 아니라 ndarray가 됨 → 역전파 안 됨 → 잘못된 결과
```

즉 과거 NumPy는 **파이썬 표준 디스패치를 안 따름**. 다른 타입을 무식하게 삼켰음.

**해법**: `__array_priority__` — " NumPy야, 다른 타입 만나면 일단 내비둬. 내가 더 높으니까."라는 **협상 카드**.
- ndarray 기본 우선순위: `0.0`
- 우리가 `200` 설정 → "내가 더 높아!" → NumPy가 양보 → `Variable.__rmul__` 호출 허용

★ 왜 `200`인가? — **아무 의미 없음**. ndarray 기본값(`0.0` 또는 `1.0`)보다 **충분히 크면 됨**. `10`, `1000`, `9999` 전부 동일 동작. 책이 200 쓴 건 "적당히 큰 수" 선택일 뿐. ★ 이게 브로가 "부자연스럽다" 느낀 진짜 이유 — 의미 없는 매직 넘버라서.

참고: [NumPy standard array subclasses 문서](https://numpy.org/doc/stable/reference/arrays.classes.html), [Stack Overflow — __rmul__과 NumPy](https://stackoverflow.com/questions/38229953/array-and-rmul-operator-in-python-numpy)

### 3세대: `__array_ufunc__` (NEP 13, 2017) — 현대의 정석

NEP 13([공식 문서](https://numpy.org/neps/nep-0013-ufunc-overrides.html))이 도입한 **가장 현대적인 메커니즘**.

`__array_ufunc__`를 정의하면, NumPy가 ufunc 연산(`+`, `*`, `np.sin` 등 전부)을 **통째로 우리 클래스에 위임**:
```python
class Variable:
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        # ufunc: np.add, np.multiply 등의 ufunc 객체
        # method: '__call__', 'reduce', 'accumulate' 등
        # inputs: 실제 인자들
        # ★ 여기서 우리가 원하는 대로 처리
        ...
```

PyTorch, JAX, Dask, CuPy 등 현대 프레임워크가 다 이 방식. 가장 강력하지만 **구현이 복잡** (모든 ufunc 케이스 처리).

★ DeZero/rezero는 이걸 안 씀. 이유: Variable은 ufunc 전체 가로챌 필요 없이 `__add__`/`__mul__` 몇 개만 지원하면 됨. `__array_ufunc__`는 over-engineering.

---

## 3. 실험으로 증명 — `200`은 현대에 불필요

### 실험 설계 (3가지 케이스 비교)

```python
class NaiveVar:
    """__rmul__만 있고 __array_priority__ 없음."""
    def __init__(self, data): self.data = data
    def __mul__(self, other): ...
    def __rmul__(self, other): ...

class PriorityOnly:
    """__array_priority__=200만 있고 __rmul__ 없음."""
    __array_priority__ = 200
    def __mul__(self, other): ...
    # __rmul__ 정의 안 함!
```

### 결과

| 케이스 | `ndarray * obj` 결과 | 의미 |
|---|---|---|
| `NaiveVar` (rmul만, priority 없음) | **NaiveVar 유지** ✅ | 현대 NumPy에선 `__rmul__`만으로 충분 |
| `PriorityOnly` (priority만, rmul 없음) | **TypeError** ❌ | priority만 있다고 역순이 안 불림. `__rmul__`이 있어야 |
| `UfuncTest` (`__array_ufunc__` 정의) | ufunc 가로채짐 | 3세대 메커니즘 정상 동작 |

### 핵심 통찰

1. **`__rmul__`만 있으면 현대 NumPy에선 잘 동작** (priority 불필요)
2. **반대로 priority만 있다고 자동으로 역순이 안 불림** — `__rmul__`이 필수
3. 즉 `__array_priority__ = 200`은 **belt and suspenders(혹시 몰라)** 또는 **과거 NumPy 호환용**이지, 현대에필수 아님

참고: [NumPy issue #27348 — 최신 NumPy가 NotImplemented를 잘 반환하게 된 이력](https://github.com/numpy/numpy/issues/27348)

---

## 4. ★★★ 핵심 교훈 — "책 코드도 검증하라"

이 탐구의 진짜 가치는 단순히 `200`이 불필요하다는 사실이 아니라, **"왜 불필요한지"를 이해한 과정**:

### 교훈 1: 매직 넘버를 대충 쓰지 말 것

책이 `200`을 보여주고 넘어갔을 때 "뭐 이유가 있겠지" 하고 넘어갔으면:
- "왜 200이지?" 계속 거슬림
- 다른 프로젝트에서도 "그냥 200 쓰는" 앵무새 전염
- 결국 이해 없이 복붙하는 것 (AGENTS.md "무지성 복붙 금지" 위반)

브로가 "찜찜하다"고 한 직감 → 탐구 → "아, 과거 핵이었구나, 현대엔 불필요" 납득. **이게 학습**.

### 교훈 2: 책/교과서 코드도 시대가 지나면 구식이 됨

`__array_priority__`는 과거 NumPy엔 필수였음. 하지만:
- NEP 13 (2017) 이후 NumPy가 표준 디스패치를 존중하게 됨
- Python 3.12 + 최신 NumPy 환경에선 `__rmul__`만으로 충분

→ 책이 쓰인 시점엔 합리적이었을 수 있으나, **현재 시점엔 불필요**. 책을 맹신하지 말 것.

### 교훈 3: "왜?"라고 묻는 습관이 코드를 투명하게 만듦

브로가 "200이 부자연스럽다"고 한 순간, 우리는:
1. 실험으로 priority가 정말 필요한지 검증
2. 내 가설이 틀렸음을 솔직히 인정 (성실 보고 원칙)
3. NEP 13 공식 문서로 진짜 메커니즘 파악
4. "왜 불필요한지" 영구 기록

이 전체 사이클이 **한 줄의 `__array_priority__ = 200`에서 파생**. "왜?"가 만드는 학습 가치의 증명.

---

## 5. rezero의 결정 — `200` 버림, 이유는 기록

```python
# 책 원본 (step21)
class Variable:
    __array_priority__ = 200    # ← rezero는 이 줄 버림
    def __init__(self, data, name=None): ...

# rezero (step21)
class Variable:
    def __init__(self, data, *, name=None): ...
    # __array_priority__ 없음 — 현대 NumPy에선 __rmul__로 충분 (탐구 25번 참조)
```

**버린 이유 (영구 기록)**:
1. 현대 NumPy (Python 3.12 + 최신 버전)는 표준 디스패치 존중 → `__rmul__` 정상 호출
2. 실험 1(NaiveVar)로 증명 — priority 없이도 `ndarray * Variable`이 Variable 유지
3. `200`이라는 매직 넘버의 의미 불투명 → "왜 200?" 거슬림 → 학습 방해
4. 구버전 NumPy 호환성은 우리 환경(Python 3.12 고정)에서 무관

★ 주의: 만약 구버전 NumPy 환경에서 rezero를 돌린다면 `__array_priority__ = 200`이 다시 필요할 수 있음. 그때는 이 노트를 보고 "아, 그때 버렸었지" 하고 복구하면 됨.

---

## 6. 요약 — "찜찜함"이 해독되기까지

1. 브로 "찜찜" → 왜?
2. 실험 1: priority 없이도 `__rmul__` 동작 → "어라?"
3. 내 가설 틀림 인정 ("NumPy가 무식하게 삼킨다" X)
4. NEP 13 검색 → 과거 NumPy의 `NotImplemented` 미반환 이력 발견
5. 드디어 이해: **`200`은 과거 핵, 현대엔 불필요**
6. 결정: 버리고 이유 기록

브로의 직감 하나가 파낸 것:
- 세대별 메커니즘 역사 정리 (1/2/3세대)
- "책 코드도 검증하라" 교훈 영구화
- rezero 정체성 강화 ("이유 없는 매직 넘버 안 쓴다")

**키워드**: `#step21` `#__array_priority__` `#200매직넘버` `#ufunc` `#__rmul__` `#__radd__` `#__array_ufunc__` `#NEP13` `#NumPy` `#역사적계층` `#과거핵` `#현대불필요` `#책검증` `#매직넘버의의심` `#브로찜찜감각` `#성실보고` `#가설틀림인정`

---

## 🔗 참고 자료

- [NEP 13 — ufunc overriding 공식 문서](https://numpy.org/neps/nep-0013-ufunc-overrides.html) — 3세대 메커니즘 명세
- [NumPy ufuncs 공식 매뉴얼](https://numpy.org/doc/stable/reference/ufuncs.html) — ufunc 기초
- [NumPy basics.ufuncs 튜토리얼](https://numpy.org/doc/stable/user/basics.ufuncs.html) — 입문용
- [NumPy issue #27348](https://github.com/numpy/numpy/issues/27348) — 최신 NumPy가 NotImplemented를 잘 반환하게 된 이력
- [Stack Overflow — __rmul__과 NumPy](https://stackoverflow.com/questions/38229953/array-and-rmul-operator-in-python-numpy) — 과거 동작 설명
- [NumPy standard array subclasses 문서](https://numpy.org/doc/stable/reference/arrays.classes.html) — `__array_priority__` 공식 설명
- [W3Schools ufunc 기초](https://www.w3schools.com/python/numpy/numpy_ufunc.asp) — ufunc 초간단 설명
- step21 이슈: #26
