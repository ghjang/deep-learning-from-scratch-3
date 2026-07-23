# 🧪 탐구 노트 #12 — 언어 바인딩과 타이핑: 파이썬 vs C/C++ vs JS

> **시점**: step04 직후 (step04.py의 `f` 변수 재사용에서 출발)
> **동기**: step04.py에서 `f = Square()` 후 `def f(x):`로 같은 이름 재사용 → IDE 빨간줄.
> "왜 빨간줄이지?" → "파이썬은 후방 선언 안 해도 되나?" → "C/C++과 차이?" → "이게 동적 타이핑이랑 관련?"
> 질문이 연쇄적으로 이어져 언어 철학의 핵심인 **바인딩(binding)** 과 **타이핑(typing)** 개념까지 도달.
>
> ⚠️ 이 노트는 **언어 비교에 집중**. JS 호이스팅/var/let 등 디테일은 §7에서 **키워드만** 소개 (심화는 추후).

---

## 📋 목차

1. [TL;DR](#tldr)
2. [출발점: step04.py의 `f` 재사용 — name shadowing](#출발점)
3. [핵심 개념: 바인딩(binding)이란?](#바인딩)
4. [Early vs Late binding — 두 철학](#early-late)
5. [정적 vs 동적 타이핑 — 바인딩과 같은 뿌리](#타이핑)
6. [언어별 비교 — C/C++/Java/Python/JS](#언어비교)
7. [JavaScript — 가벼운 언급 (심화 키워드만)](#js)
8. [★ 왜 Python은 전방 선언이 필요 없나 (step04 사례)](#python-전방)
9. [요약 / 결론](#결론)

---

<a id="tldr"></a>
## 🎯 TL;DR

| 핵심 개념 | 정적(early) | 동적(late) |
|---|---|---|
| **바인딩 시점** | 컴파일 타임 | 런타임 |
| **타이핑 시점** | 컴파일 타임 | 런타임 |
| **대표 언어** | C, C++, Java (타입), Rust | Python, JS, Ruby, Lua |
| **전방 선언** | 필요 | 불필요 |
| **철학** | 성능, 안전 (컴파일러가 버그 잡음) | 유연성, 생산성 (빠른 프로토타이핑) |

**브로 핵심 통찰**: "동적 타이핑 ↔ late binding은 같은 뿌리" — ✅ 정확함. 둘 다 "런타임에 결정한다"는 동적 언어의 본질.

---

<a id="출발점"></a>
## 1. 출발점: step04.py의 `f` 재사용 — name shadowing

step04 원본 코드:

```python
f = Square()                    # f는 Square 인스턴스 (전역)
dy = numerical_diff(f, x)       # 미분에 사용

def f(x):                       # 같은 이름 f를 함수로 재정의!
    A = Square(); B = Exp(); C = Square()
    return C(B(A(x)))

dy = numerical_diff(f, x)       # 이제 f는 함수 (위 객체를 덮어씀)
```

### 왜 IDE가 빨간줄을 긋나?

| IDE 경고 이름 | 의미 |
|---|---|
| **Redefined name** / **Shadows outer name** | 같은 스코프에서 같은 이름 재사용 |
| **Used before def** | 정의 전 사용 (함수 컨텍스트) |

### 왜 이게 위험한가 — "실행 순서 의존적"

Python은 top-to-bottom 실행이라:
1. `f = Square()` → f는 객체
2. `numerical_diff(f, x)` → 객체로 미분 ✅
3. `def f(x):` → f가 **함수로 덮어씌워짐**
4. `numerical_diff(f, x)` → 함수로 미분 ✅

→ 두 번 다 우연히 잘 돌아가지만, **누군가 순서를 바꾸면 깨짐**:

```python
def f(x): ...      # 맨 위로
f = Square()       # f가 Square로 덮어씌워짐
numerical_diff(f, x)  # ← def f 무효화
```

이게 **"name shadowing"** 또는 **"mutable global state"** 악취. PEP 8에서도 같은 이름 재사용 경고.

### 결론 — 버그는 아니지만 나쁜 패턴

- 문법적 버그: ❌ (Python 허용)
- 논리적 버그: ❌ (현재는 정상 동작)
- 좋은 코드: ❌ (IDE 워닝 정당, 순서 바꾸면 깨짐)
- 책에서 이렇게 쓴 이유: 교육적 편의 (한 파일에 단계별 예제 연속 배치)

**우리 `rezero/steps/step04.py` 처리**: `sq` / `composite_f`로 이름 분리하여 악취 제거.

---

<a id="바인딩"></a>
## 2. 핵심 개념: 바인딩(binding)이란?

> **바인딩(binding)**: 이름(식별자)이 **어떤 대상(값, 함수, 객체 등)에 연결되는 것**.

```python
x = 10         # x 라는 이름이 값 10에 바인딩
def f(): ...   # f 라는 이름이 함수 객체에 바인딩
import math    # math 라는 이름이 모듈에 바인딩
```

모든 프로그래밍 언어가 다루는 근본 메커니즘. 핵심 질문은 **"이 바인딩이 언제 일어나는가?"**

---

<a id="early-late"></a>
## 3. Early vs Late binding — 두 철학

### Early binding (정적 바인딩)

- 바인딩이 **컴파일 타임**에 결정됨
- 컴파일러가 이름을 미리 다 찾고 고정
- 장점: 런타임 성능 (룩업 비용 없음), 타입 안전성
- 단점: 유연성 낮음, 전방 선언/헤더 파일 등 번거로움

### Late binding (동적 바인딩)

- 바인딩이 **런타임**에 결정됨
- 코드 실행하면서 이름을 동적으로 찾음
- 장점: 유연성, 빠른 프로토타이핑, 전방 선언 불필요
- 단점: 런타임 룩업 비용, 타입 불안전 (런타임 에러 위험)

### 💡 step04에서 체감한 차이

```python
def numerical_diff(x):
    return composite_f(x - 1) - composite_f(x + 1)
    #          ↑ 이 이름을 "호출 시점"에 찾음 (late binding)

def composite_f(x):
    return x * x
```

- **C/C++**: 이 코드 컴파일 에러. `composite_f`를 먼저 전방 선언해야 함 (early binding)
- **Python**: 정상 작동. `numerical_diff` 호출 시점에 `composite_f` 찾음 (late binding)

---

<a id="타이핑"></a>
## 4. 정적 vs 동적 타이핑 — 바인딩과 같은 뿌리

★ 브로 핵심 통찰: **"동적 타이핑 ↔ late binding은 같은 뿌리"**.

| | 결정 대상 | 시점 |
|---|---|---|
| **동적 타이핑 (dynamic typing)** | 변수의 **타입** | 런타임 |
| **late binding (dynamic binding)** | 이름이 **가리키는 대상** | 런타임 |

→ 둘 다 "런타임에 결정한다"는 **동적 언어(dynamic language)** 의 본질. 같은 철학의 두 측면.

### 코드로 보는 동일성

```python
x = 10          # x 타입이 int로 결정 (런타임)
x = "hello"     # 같은 x가 str로 결정 (런타임) ← 동적 타이핑

def g(): ...    # g가 이 함수로 결정 (런타임)
def g(): ...    # 같은 g가 다른 함수로 결정 (런타임) ← late binding
```

→ **"이름은 그대로인데, 그 이름이 가리키는 게 실행 흐름에 따라 변한다"** — 이게 동적 타이핑이자 late binding. Python, JS, Ruby 등 동적 언어의 공통 특징.

---

<a id="언어비교"></a>
## 5. 언어별 비교 — C/C++/Java/Python/JS

| 언어 | 타이핑 | 바인딩 | 전방 선언 | 비고 |
|---|---|---|---|---|
| **C** | 정적 | early | ✅ 필수 (header) | 둘 다 정적. 최고 성능 |
| **C++** | 정적 | early (`virtual`은 late!) | ✅ 필수 | hybrid — 가상함수가 유일한 late 예외 |
| **Java** | 정적 | early (메서드는 late!) | ❌ (JVM이 클래스 전체 로드) | hybrid — 메서드 디스패치만 late |
| **Python** | **동적** | **late** | ❌ | 둘 다 동적, 전방 선언 불필요 |
| **JavaScript** | **동적** | **late** | ❌ | 둘 다 동적, 호이스팅(hoisting)은 별개 함정 |
| **TypeScript** | 정적(검사) | late(런타임은 JS) | ❌ | "정적 타입 검사 + 동적 실행" 절충 |

### 💡 Hybrid 언어들의 특이점

#### C++의 `virtual` — 정적 언어 안의 late 예외

```cpp
class Base { virtual void foo() { } };     // virtual!
class Derived : public Base { void foo() override { } };

Base* b = new Derived();
b->foo();    // Derived::foo() 호출 ← 런타임에 결정 (late binding)
```

→ C++은 기본 early지만, `virtual` 키워드로 **런타임 다형성(vtable)** 제공. OOP의 핵심.

#### Java의 메서드 디스패치

Java는 타입은 정적이지만, **메서드 호출은 기본 late** (인스턴스의 실제 타입 따라). 그래서 전방 선언 필요 없이 JVM이 클래스 전체 로드 후 실행.

---

<a id="js"></a>
## 6. JavaScript — 가벼운 언급 (심화 키워드만)

> 브로 배경: JS도 종종 쓴다고 함. JS는 late binding이지만 **별도 함정**이 있음.
> 깊이 파면 딥러닝 학습에서 벗어나니, **키워드만 남기고 추후 필요 시 검색**.

### JS도 late binding + 동적 타이핑

```javascript
let x = 10;          // 타입이 number
x = "hello";         // 같은 x가 string (동적 타이핑)
```

→ Python과 동일한 철학. 이름을 런타임에 찾는다.

### JS 특유 함정 — 키워드 정리 (추후 검색용)

| 키워드 | 한 줄 요약 | 심화 검색 키워드 |
|---|---|---|
| **var** | 함수 스코프, 호이스팅 됨 (undefined로 초기화), 전역 var는 window 프로퍼티 | `var vs let vs const` |
| **let / const** | 블록 스코프, 호이스팅은 되지만 TDZ로 접근 에러 | `Temporal Dead Zone`, `TDZ` |
| **암묵적 전역** | `var` 안 쓰고 할당하면 전역 객체에 생성 (strict mode에선 에러) | `implicit global`, `use strict` |
| **호이스팅 (hoisting)** | 선언이 스코프 최상단으로 끌어올려지는 현상 (var, function declaration) | `JS hoisting`, `function declaration vs expression` |
| **function declaration vs expression** | `function foo(){}`는 호이스팅, `var bar = function(){}`는 안 됨 | `JS function hoisting` |

### 💡 모던 JS 권장 (국룰)

- 기본: **`const`**
- 재할당 필요: `let`
- **`var`는 절대 쓰지 마** (ES6+부턴 필요 없음)
- 항상 strict mode (`"use strict"` 또는 ES module)

→ 브로가 "var 안 쓰려고 한다"는 완전 정답.

---

<a id="python-전방"></a>
## 7. ★ 왜 Python은 전방 선언이 필요 없나 (step04 사례)

브로 질문의 핵심을 step04 코드로 검증.

### Python의 late binding 원리

Python은 함수 본문 안의 이름을 **정의할 때가 아니라 호출할 때** 찾는다 (late binding).

```python
# step04 우리 코드에서
def numerical_diff(f, x, eps=1e-4):   # 정의. 본문 실행 아직 안 됨
    ...
    y0 = f(x0)                         # f를 호출 시점에 찾음
    ...

def composite_f(x):                   # 정의. 이제 composite_f 등록
    ...

numerical_diff(composite_f, x)        # 호출. 이때 f 매개변수 = composite_f
                                     # → composite_f를 찾음 → 찾음! ✅
```

### "호출 시점"이 핵심

| 단계 | 발생하는 일 |
|---|---|
| 1. `def numerical_diff(...)` | 함수 객체 생성, 본문은 실행 안 함. `f`가 뭔지 몰라도 OK |
| 2. `def composite_f(...)` | 함수 객체 생성, `composite_f` 이름이 전역에 등록 |
| 3. `numerical_diff(composite_f, x)` | 본문 실행. `f(x0)` 평가 → `f` 찾음 → `composite_f` 찾음 → 정상 |

→ **"호출되는 시점"에 모든 정의가 이미 보이기 때문에** 후방 참조 문제 없음.

### C/C++ 대조

```c
// C라면 컴파일 에러
int numerical_diff(int (*f)(int), int x) {
    return f(x-1) - f(x+1);   // f는 매개변수라 OK, 근데...
}

int composite_f(int x) { ... }  // 이건 OK, 미리 prototype만 있으면
```

→ C는 **함수 포인터 타입**을 컴파일 타임에 알아야. 그래서 헤더 파일에 prototype 쓰는 것.

### 💡 Python late binding의 부작용 — Monkey Patching

런타임에 함수를 교체 가능 (C/C++에선 상상도 못 할 일):

```python
def f():
    return g()           # g는 호출 시점에 찾음

def g():
    return "원래 g"

print(f())               # "원래 g"

def g():                 # g를 런타임에 교체!
    return "새로운 g"

print(f())               # "새로운 g" ← f는 그대로인데 결과 바뀜!
```

→ 이게 **Monkey Patching** (exploration_08 참조). Python의 late binding이 가능케 하는 강력한(그리고 위험한) 기능.

---

<a id="결론"></a>
## 8. 요약 / 결론

### 핵심 한 줄
> **바인딩(이름↔대상 연결)과 타이핑(변수↔타입)은 "언제 결정하느냐"로 정적/동적이 갈린다. Python은 둘 다 동적이라 전방 선언 불필요 + Monkey Patching 가능.**

### 브로 질문 답변 요약

| 질문 | 답 |
|---|---|
| step04 `f` 재사용은 버그인가? | ❌ 버그 아님. 단, name shadowing 악취 (순서 바꾸면 깨짐) |
| 후방 참조된 함수를 전방에서 쓰면 에러? | ❌ Python은 OK (late binding). C/C++은 에러 |
| late binding이 동적 타이핑 특징? | ✅ 정확. 같은 뿌리 (둘 다 런타임 결정) |
| JS도 late binding? | ✅ 맞음. 다만 호이스팅/TDZ 등 별개 함정 존재 |

### 동적 언어의 트레이드오프

| 장점 | 단점 |
|---|---|
| 유연성, 빠른 프로토타이핑 | 런타임 에러 위험 |
| 전방 선언/헤더 불필요 | 타입 안전성 낮음 |
| REPL로 실험 가능 | 성능 약간 손해 (룩업 비용) |
| Monkey Patching 등 메타 프로그래밍 | 코드 이해 어려움 (동적 변형) |

→ 최근 추세: **동적 타이핑 + 정적 분석 도구(mypy/pyright/TypeScript)** 로 절충.
브로가 step03에서 `@override` 도입한 것도 이 맥락!

### 🔗 관련 링크

- step04 노트 (`f` 재사용 문제 → 본 탐구 출발점)
- [exploration_08_monkey_patching.md](./exploration_08_monkey_patching.md) — late binding이 가능케 하는 Python의 런타임 조작
- [exploration_07_syntax_idioms.md](./exploration_07_syntax_idioms.md) C.1.3 — `@override`와 정적 분석 도구
- [exploration_09_abc_abstract.md](./exploration_09_abc_abstract.md) §9 — `@override` (런타임 강제력 ❌) ↔ `@abstractmethod` (런타임 강제력 ✅)

**키워드**: `#바인딩` `#binding` `#early-binding` `#late-binding` `#정적바인딩` `#동적바인딩` `#타이핑` `#정적타이핑` `#동적타이핑` `#전방선언` `#forward-declaration` `#name-shadowing` `#C++` `#Java` `#JavaScript` `#호이스팅` `#TDZ` `#var-let-const` `#virtual` `#vtable` `#Monkey-Patching` `#mypy` `#pyright` `#TypeScript`
