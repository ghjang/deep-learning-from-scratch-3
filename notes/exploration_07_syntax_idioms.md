# 🧪 보충 탐구 #7 — Python 문법과 이디엄 (데코레이터, f-string, lambda 등)

> **step01 직후 보충 학습 #7** (2026-07-21)
> 원래 탐구 #1의 C 섹션이었으나, 01이 비대해져서 분리.
> 파이썬 문법/이디엄 중 DeZero 학습과 직결되는 것들을 모음.

---

## 목차


- [A.1 데코레이터(`@`)](#a1-데코레이터)
- [A.2 f-string (포맷팅)](#a2-f-string-포맷팅)
- [A.3 `==` vs `is`](#a3--vs-is)
- [A.4 "primitive"와 박싱](#a4-primitive와-박싱--python의-객체-철학)
- [A.5 파이썬은 진짜 편한가?](#a5-파이썬은-진짜-편한가)
- [A.6 lambda 표현식](#a6-lambda-표현식--제한적이지만-특정-용도에선-국룰)
- [A.7 언패킹(unpacking) — 리스트/튜플을 변수로 쪼개기](#a7-언패킹unpacking--리스트튜플을-변수로-쪼개기)
  - [A.7.1 핵심 — "상자를 열어 내용물을 각자에게"](#a71-핵심--상자를-열어-내용물을-각자에게)
  - [A.7.2 변수 개수 불일치 — 엄격한 규칙](#a72-변수-개수-불일치--엄격한-규칙)
  - [A.7.3 `*` 스플래트 — "나머지 전부를 리스트로"](#a73-star-스플래트--나머지-전부를-리스트로)
  - [A.7.4 `*`는 여러 개 불가 — 모호성 때문에 문법 금지](#a74-star는-여러-개-불가--모호성-때문에-문법-금지)
  - [A.7.5 `*`의 이중성 — 함수 정의 vs 호출 (★ step12 핵심)](#a75-star의-이중성--함수-정의-vs-호출-step12-핵심)
  - [A.7.6 for 루프에서 동시 언패킹](#a76-for-루프에서-동시-언패킹--자주-쓰는-이디엄)
  - [A.7.7 head/tail 패턴 — 함수형 프로그래밍 연결](#a77-headtail-패턴--함수형-프로그래밍-연결)
  - [A.7.8 DeZero에서 언패킹이 계속 등장할 곳 (복선)](#a78-dezero에서-언패킹이-계속-등장할-곳-복선)
  - [A.7.9 요약표](#a79-요약표)
- [C.1.4 심화 — 오버라이드 시그니처 자유 (★ step12 문화충격)](#심화--오버라이드는-시그니처가-달라도-된다-문화충격-포인트)

---

## A. Python 문법과 이디엄

### A.1 데코레이터(`@`)

**요약**: `@staticmethod` 같이 `@`로 시작하는 것을 **데코레이터**라 함. "함수를 인자로 받아 새로운 함수를 반환하는 함수"를 간결하게 적용하는 문법. PEP 318 (Python 2.4, 2004년) 도입.

```python
@staticmethod
def forward(x):
    return x ** 2

# 위는 아래의 설탕(syntactic sugar) — 의미 동일
def forward(x):
    return x ** 2
forward = staticmethod(forward)
```

#### C.1.1 DeZero에서 데코레이터 사용 현황 (검증)

| 데코레이터 | 책 본문(steps/) | 완성 프레임워크(dezero/) |
|---|---|---|
| `@staticmethod` | ❌ 안 나옴 | ✅ 5곳 (models.py, datasets.py) |
| `@classmethod` | ❌ 안 나옴 | 일부 |
| `@property` | ✅ step19부터 빈번 | ✅ 많음 |
| `@contextlib.contextmanager` | ✅ step18부터 빈번 | ✅ |

→ 책은 학습 목적상 복잡한 데코레이터(`@staticmethod`/`@classmethod`)는 피하고, 유용한 것(`@property`, `@contextmanager`)은 적극 사용.

#### C.1.2 데코레이터 2개 이상 쌓기 — 가능!

데코레이터는 **여러 개를 쌓을 수 있음**. 가장 아래 데코레이터가 먼저 적용돼.

```python
@decorator_a
@decorator_b
@decorator_c
def foo():
    pass

# 실제로 일어나는 일:
def foo():
    pass
foo = decorator_a(decorator_b(decorator_c(foo)))
# 적용 순서: c → b → a (아래에서 위로!)
```

##### 실전 예시 (웹 프레임워크에서 흔함)

```python
# Flask 웹 라우트 예시
@app.route("/api")        # 라우팅 등록
@require_auth             # 인증 확인
@log_request              # 로깅
def api_handler():
    return {"status": "ok"}

# 적용 순서: log_request → require_auth → route
```

##### 다른 데코레이터와 같이 쓰기

```python
class Variable:
    @property
    def shape(self):
        return self.data.shape

class TensorVariable(Variable):
    @property
    @override                    # ← property랑 같이 쓰기 가능
    def shape(self):
        return super().shape + ("tensor",)
```

#### C.1.3 `@override` — Python 3.12+ (PEP 698)

**요약**: 부모 메서드를 오버라이드한다는 표시. **타입 체커(pyright/mypy)용**이고 런타임엔 효과 없음 (no-op).

```python
from typing import override

class Animal:
    def speak(self) -> str:
        return "..."

class Dog(Animal):
    @override                    # ← "부모 메서드 오버라이드한다" 표시
    def speak(self) -> str:
        return "Woof"
```

##### 진짜 역할 — 오타/실수 잡기

```python
class Animal:
    def bark(self) -> str:       # bark이라고 정의했다 치자
        return "..."

class Dog(Animal):
    @override
    def spak(self) -> str:       # ❌ 오타! spak vs bark
        return "Woof"
# pyright: "spak은 부모에 없는 메서드" 경고!
```

→ 부모에 해당 메서드가 없으면 **pyright가 잡아줌**. 이게 진짜 가치.

##### Java/C#과의 비교

| 언어 | 문법 | 런타임 효과 |
|---|---|---|
| **Java** | `@Override` 어노테이션 | 없음 (컴파일러용) |
| **C#** | `override` 키워드 | 있음 (필수) |
| **Python** | `@override` 데코레이터 (3.12+) | 없음 (타입 체커용) |

→ 파이썬 `@override`는 Java `@Override`와 같은 철학. **컴파일/검증용**이지 런타임용이 아님.

##### 실전 함정과 연결 (exploration_05 A.8.1)

```python
class Variable:
    def __init__(self, data):
        self.data = data

class Parameter(Variable):
    @override
    def __init__(self, data):
        super().__init__(data)
        self.requires_grad = True
# pyright가 부모 시그니처와 비교해서 문제 잡아줌
```

→ A.8.1의 "이름 충돌 덮어쓰기" 함정을 잡는 도구 중 하나. 브로가 Pylance 쓰고 있으니 진짜 유용.

##### 우리 프로젝트에선?

파이썬 3.13이니 `@override` 바로 쓸 수 있음. 다만 DeZero 책에선 안 나옴 (3.12+ 기능이라). 학습 후 실험적으로 도입 가능.

> 🔬 **심화**: step03에서 abc + `@override`를 함께 도입하며 강제력 차이를 실험함. `@override`(정적 분석) vs `@abstractmethod`(런타임) 비교 → [exploration_09 §9](./exploration_09_abc_abstract.md#override)

#### C.1.4 메서드 오버로딩 — 파이썬은 미지원! (`@overload`는 타입 힌트용)

> 브로 질문: "메서드 오버로딩을 파이썬이 지원하나?"

**결론**: **네이티브 메서드 오버로딩 미지원**. C++/Java/C#처럼 "같은 이름, 다른 시그니처" 불가.

##### 직접 확인 — 안 됨

```python
class Foo:
    def bar(self, x: int):
        return x + 1
    
    def bar(self, x: str):       # ❌ 이전 bar를 덮어써버림!
        return x + "!"

f = Foo()
f.bar(1)      # ❌ TypeError — 마지막 bar만 남아서 int 못 받음
```

→ 클래스의 이름 공간이 딕셔너리라 같은 이름은 마지막이 이김.

##### 왜 안 지원할까?

1. **동적 타입** — 컴파일 타임에 시그니처 구분 불가
2. **단순함** — 같은 이름 여러 개면 혼란 (PEP 20: Simple is better than complex)
3. **대안이 충분함** — `*args`, `**kwargs`, 기본값, `singledispatch` 등

##### 우회 방법 4가지

**방법 1: 기본 인자 + 조건문 (가장 흔함)**
```python
class Foo:
    def bar(self, x=None, s=None):
        if x is not None:
            return x + 1           # int 버전
        elif s is not None:
            return s + "!"         # str 버전
```

**방법 2: `*args` + isinstance**
```python
class Foo:
    def bar(self, *args):
        if len(args) == 1 and isinstance(args[0], int):
            return args[0] + 1
        elif len(args) == 1 and isinstance(args[0], str):
            return args[0] + "!"
```

**방법 3: `functools.singledispatch` (가장 정석)**
```python
from functools import singledispatch

@singledispatch
def bar(x):
    raise TypeError(f"지원 안 함: {type(x)}")

@bar.register
def _(x: int):
    return x + 1

@bar.register
def _(x: str):
    return x + "!"
```

**방법 4: `@overload` (typing) — 타입 힌트용, 런타임 효과 없음!**
```python
from typing import overload

class Foo:
    @overload
    def bar(self, x: int) -> int: ...      # 선언만 (구현 없음)
    @overload
    def bar(self, x: str) -> str: ...      # 선언만
    def bar(self, x):                      # 실제 구현은 하나!
        if isinstance(x, int):
            return x + 1
        elif isinstance(x, str):
            return x + "!"
```

→ `@overload`는 pyright/mypy에게 "이런 시그니처로 쓸 수 있다" 알려주는 역할. **런타임엔 아무 효과 없음** (`@override`와 같은 패턴).

##### 아이러니 — 연산자는 오버로딩되는데, 메서드는 안 됨

| 종류 | 파이썬 지원 | 이유 |
|---|---|---|
| **연산자 오버로딩** (`+`, `==`) | ✅ 지원 | 시그니처 고정 (`__add__(self, other)`) |
| **메서드 오버로딩** (`foo(int)`, `foo(str)`) | ❌ 미지원 | 시그니처 자유로워 구분 애매 |

→ 연산자는 시그니처가 고정이라 오버로딩이 단순하지만, 메서드는 임의 시그니처라 복잡해서 포기.

##### DeZero에서의 우회 패턴

```python
class Function:
    def __call__(self, *inputs):           # *inputs로 가변 인자
        if len(inputs) == 1:
            return self.forward_single(inputs[0])
        else:
            return self.forward_multi(*inputs)
```

→ DeZero는 **가변 인자 + 조건문**으로 오버로딩 흉내. step11~13(가변 길이 인수)이 이 패턴 학습.

**키워드**: `#메서드오버로딩` `#미지원` `#@overload` `#typing` `#타입힌트용` `#singledispatch` `#가변인자` `#연산자오버로딩과비교` `#DeZero우회` `#Java오버로딩비교`

##### ★ 심화 — 오버라이드는 시그니처가 달라도 된다 (문화충격 포인트)

> **step12 학습 중 추가** (2026-07-30). 오버로딩(같은 이름 다른 시그니처)은 미지원인데,
> 오버라이드(자식이 부모 메서드 재정의)는 **시그니처가 달라도 허용**된다는 정적 언어와 정반대 동작.
> 브로가 "문화충격"이라 표현한 핵심.

오버로딩(↑ 위)과 대비되는, Python의 **오버라이드 시그니처 자유도**:

```python
class Function(ABC):
    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...]: ...   # 부모: 가변 인수

class Add(Function):
    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray: ... # 자식: 2개 고정
    # ★ 시그니처가 다름에도 오버라이드로 인식됨!
```

**Java/C++이었다면?** 컴파일 에러 ("method override must match parent signature").
**Python은?** 그냥 됨. 런타임엔 "이름으로 메서드 찾아서 호출"이라 시그니처 불일치를 검사하지 않음.

##### 왜 허용되는가 — duck typing의 귀결

Python은 **오리 타입(duck typing)** 언어. "오리처럼 걷고 오리처럼 울면 오리다."
메서드도 마찬가지 — 부모와 시그니처가 같은지가 아니라 **"그 이름의 메서드가 존재하고 호출 가능한가"** 만 본다.

```python
# 런타임에 일어나는 일 (Python의 실제 동작)
obj = Add()
obj.apply(x0, x1)          # ★ "Add에 apply라는 이름의 메서드 있나?" → 있음 → 호출
                           #    부모 시그니처(*xs)와 자식 시그니처(x0, x1) 비교 자체를 안 함
```

→ 시그니처 일치 검사는 **정적 타입 언어의 컴파일 타임 개념**. Python은 컴파일 단계에서 시그니처 검증하지 않으니 자연스럽게 "자유로운" 것.

##### ★ `@override` 데코레이션의 미묘한 한계

`@override`([REZERO_CHANGES 항목 004](../REZERO_CHANGES.md))는 "부모에 같은 이름 메서드가 있는지"는 검사하지만, **시그니처 일치는 약하게만 검사** (Pylance 설정에 따라 다름, 기본은 관대).

```python
class Add(Function):
    @override
    def apply(self, x0, x1): ...    # ★ 부모 apply(*xs)와 시그니처 다름 → Pylance가 "관대하게" 통과시킴
```

→ 정적 분석 도구가 "관대한 기본 설정"을 쓰기 때문에 `@override` 붙여도 경고가 안 난다.
엄격하게 검사하려면 Pylance `reportMethodSignatureMismatch` 설정 켜야 함 (현재 rezero엔 설정 없음 → step23 패키지화 때 검토).

##### 오버로딩(미지원) vs 오버라이드(시그니처 자유) — 정리

| | 오버로딩 | 오버라이드 |
|---|---|---|
| **정의** | 같은 이름, **다른 시그니처** 메서드 여러 개 | 자식이 부모 메서드 **재정의** |
| **Python 런타임** | ❌ 미지원 (나중 것이 덮어씀) | ✅ 지원 (이름만 같으면 됨) |
| **시그니처 일치 요구?** | (해당 없음) | **❌ 요구 안 함** ★ |
| **정적 분석(Pylance)** | `@overload`로 타입 힌트 제공 가능 | `@override`로 부모 존재 검사 (시그니처는 관대) |
| **Java/C++** | ✅ 지원 (시그니처로 구분) | ✅ 지원 (시그니처 **일치 필수**) |

→ Python: "오버로딩은 안 되지만, 오버라이드는 시그니처 자유". 정적 언어와 정반대되는 이 대비가 핵심 통찰.

##### ★ DeZero/rezero에서의 실제 영향

```python
class Function:
    def apply(self, *xs): ...          # 부모: 가변 인수 (step12 방향 B)

class Add(Function):
    def apply(self, x0, x1): ...       # 자식: 2개 고정 — 시그니처 다름에도 OK ★

class Square(Function):
    def apply(self, x): ...            # 자식: 1개 — 시그니처 다름에도 OK ★
```

→ 부모는 **"어떤 개수의 입력이든 받는다"** 는 일반 시그니처(`*xs`), 자식은 **"이 함수만의 고정 개수"** 로 구체화.
Java였으면 불가능한 이 패턴이 Python에선 자연스러움. DeZero가 `*args`로 다변수 함수를 일반화하면서 각 함수는 자기 시그니처대로 apply 구현하는 게 가능한 이유.

##### 학습 통찰 — 정적 타입 vs 오리 타입, 두 패러다임

| 패러다임 | 시그니처 | 대표 언어 |
|---|---|---|
| **정적 타입** | 컴파일 타임에 엄격 검사. 오버로딩/오버라이드 모두 시그니처 기반 | Java, C++, C#, Rust |
| **오리 타입** | 런타임에 "이름+호출 가능성"만 검사. 시그니처 자유 | Python, Ruby, JavaScript |

Python의 이 자유로움이 **"빠른 프로토타이핑 + 유연한 설계"** 를 가능케 하지만, 반대급부로 **"타입 안전성은 정적 분석 도구(mypy/Pylance)에 의존"** 해야 함.
→ `@override`, `@overload`, 타입 힌트가 "정적 분석용 메타데이터"로 존재하는 이유.

**키워드 추가**: `#오버라이드시그니처자유` `#duck-typing` `#오리타입` `#정적언어vs오리타입` `#문화충격` `#시그니처불일치허용` `#@override한계` `#reportMethodSignatureMismatch` `#Java오버라이드비교` `#step12추가` `#브로통찰`

> 🔗 **관련**: "시그니처가 달라도 된다"는 걸 가능케 하는 언어적 기반이 바로 **`*` 가변 인수**.
> 부모 apply를 `*xs`로 두면 어떤 자식 시그니처(고정/가변)든 호환됨 —
> 상세는 [A.7.5 "수집→언패킹 상쇄" 심화](#star는-역연산이라-상쇄--수집언패킹-상쇄와-무한-전달-step12-브로-질문에서-파생) 참조.

---

### A.2 f-string (포맷팅)

**요약**: f는 **f**ormat의 약자. Python 3.6+ (2016년) 도입. 중괄호 `{}` 안에 **파이썬 표현식**을 넣어 문자열에 값 끼워넣기. 현대 Python의 국룰.

#### C.2.1 기본 사용법

```python
name = "브로"
age = 30

# ❌ 일반 문자열 — {name}이 그냥 문자로 출력
"안녕 {name}"          # "안녕 {name}"

# ✅ f-string — {name}이 파이썬 코드로 실행되어 값 치환
f"안녕 {name}"         # "안녕 브로"

# 변수, 연산, 메서드 호출 전부 가능
x = 5
f"x² = {x**2}"                   # "x² = 25"
f"대문자: {name.upper()}"         # "대문자: 브로" (한글이라 변화 없음)
f"{x = }"                        # "x = 5"  (Python 3.8+ 디버깅 모드)

# 포맷 지정
pi = 3.14159265
f"π = {pi:.2f}"                  # "π = 3.14"          소수점 2자리
f"π = {pi:>10.4f}"               # "π =     3.1416"    폭 10, 소수점 4자리
```

#### C.2.2 정렬 기호 (`{값:정렬기호폭}` 형식)

```python
x = "abc"
f"[{x:>10}]"     # [       abc]  폭 10, 우측 정렬 (>)
f"[{x:<10}]"     # [abc       ]  폭 10, 좌측 정렬 (<, 기본)
f"[{x:^10}]"     # [   abc    ]  폭 10, 가운데 정렬 (^)
f"[{x:_>10}]"    # [_______abc]  폭 10, 우측 정렬, 빈칸을 _로 채움
```

| 기호 | 의미 |
|---|---|
| `>` | 우측 정렬 (right-align) |
| `<` | 좌측 정렬 (기본값) |
| `^` | 가운데 정렬 (center) |

#### C.2.3 역사 — JS 템플릿 리터럴과 비교

| | Python f-string | JS 템플릿 리터럴 |
|---|---|---|
| 문법 | `f"...{expr}..."` | `` `...${expr}...` `` |
| 도입 | Python 3.6 (2016) | ES6 (2015) |
| 표현식 | `{x + 1}` | `${x + 1}` |

```python
# Python
name = "브로"
f"안녕 {name}, 나이 {30 + 1}"        # "안녕 브로, 나이 31"
```
```javascript
// JavaScript
const name = "브로";
`안녕 ${name}, 나이 ${30 + 1}`        // "안녕 브로, 나이 31"
```

→ JS가 1년 먼저(ES6/2015) 도입, Python이 3.6(2016)에서 따라온 형태. 문법만 약간 다르고 **개념은 완전히 같음**.

#### C.2.4 역사적 순서 (왜 f-string이 국룰인지)

```python
# 1. %-formatting (C 스타일, 옛날)
"이름: %s" % name

# 2. str.format() (Python 2.6+)
"이름: {}".format(name)

# 3. f-string (Python 3.6+) ⭐ 현대 국룰, 가장 빠르고 읽기 쉬움
f"이름: {name}"
```

#### C.2.5 rezero 코드에서 사용

방금 브로가 짠 `rezero/steps/step01.py`의 `inspect()` 헬퍼:
```python
print(f"[{label:>10}] data={x.data!s:>10}  ndim={x.data.ndim}")
#     {label:>10}   → label 값, 우측 정렬, 폭 10
#     {x.data!s}    → !s는 str()로 변환 (ndarray를 문자열로)
```

**키워드**: `#f-string` `#format` `#포맷팅` `#중괄호표현식` `#Python36` `#PEP498` `#JS템플릿리터럴` `#ES6` `#정렬` `#폭지정`

---

### A.3 `==` vs `is`

**요약**: `==`는 **값 비교**, `is`는 **객체 식별(주소) 비교**. 혼동하면 버그 생김. 특히 작은 정수/문자열은 파이썬이 캐싱해서 `is`가 우연히 True가 되는 함정.

```python
a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)    # True   ← 값이 같음
print(a is b)    # False  ← 다른 객체 (다른 메모리)

# 작은 정수 함정 (-5 ~ 256은 캐싱됨)
x = 256
y = 256
print(x is y)    # True   ← 캐싱됨

x = 257
y = 257
print(x is y)    # False  ← 캐싱 안 됨 (PyPy 등 구현체 따라 다름)

# None 비교는 is 권장 (PEP 8)
if x is None:    # O
if x == None:    # X (비권장)
```

- DeZero에선 주로 `==` 사용. `is`는 `is None`, 타입 체크(`isinstance`)에 쓰임
- AGENTS.md에 언급된 `dezero/datasets.py`의 `is 'fine'` 버그 → 원래 `== 'fine'`이어야 함 (문자열은 `is` 금지!)
- NumPy에선 `array_equal`, `allclose` 사용 권장 (element-wise라서)

**키워드**: `#객체비교` `#값비교` `#캐싱함정` `#isNone` `#isinstance`

---

### A.4 "primitive"와 박싱 — Python의 객체 철학

**요약**: Python은 **모든 것이 객체**. Java/C# 같은 "primitive vs wrapper" 구분이 없음. `int`도 객체고, `float`도 객체. 단, **성능 최적화**를 위해 작은 정수(-5~256)는 캐싱됨.

```python
x = 5
print(type(x))         # <class 'int'>  →  int도 클래스
print(x.__add__(3))    # 8  →  dunder 호출 가능 (객체니까)

# Java int는 객체 아님. Python int는 객체. 근본적 차이.
# 이래서 Python엔 "박싱/언박싱" 개념이 명시적으론 없음.

# 하지만 NumPy는 C 기반이라 진짜 primitive 메모리 사용
import numpy as np
arr = np.array([1, 2, 3])
print(arr.dtype)       # int64  →  C의 int64_t 배열 (primitive)
```

- Python 레벨: `int`, `float`, `str` 전부 객체 (래퍼 개념 불필요)
- NumPy 레벨: C 배열 기반, 진짜 primitive. `dtype`으로 타입 명시.
- DeZero의 Variable은 **이미 객체인 ndarray를 한 번 더 감싸는** 2중 래핑. 메타정보 추가 목적.

**키워드**: `#객체지향` `#primitive` `#박싱` `#dtype` `#int객체` `#캐싱`

---

### A.5 파이썬은 진짜 편한가?

**요약**: Java/C# 하던 사람한테 첫인상은 "느슨하고 불안"해 보일 수 있음. 하지만 **학습/프로토타이핑/데이터 분석** 분야에선 진짜 편함.

#### C.5.1 편한 이유 5가지

**1. 컴파일/빌드 단계 없음 (인터프리터)**

```java
// Java: 컴파일 → 실행 2단계
$ javac Main.java && java Main
```
```python
# Python: 그냥 실행 1단계
$ python main.py
```

코드 고치고 바로 실행. 실험 사이클 짧음. DeZero도 `uv run python steps/step01.py` 한 줄.

**2. 타입 선언 안 해도 됨 (동적 타입)**

```java
// Java
List<Variable> list = new ArrayList<>();
Map<String, Integer> map = new HashMap<>();
```
```python
# Python
list = []
map = {}
```

타입 적는 시간 절약. 단점(모호함)도 있어서 최근엔 **type hints** 옵션 도입:
```python
def add(x: int, y: int) -> int:    # 선택적
    return x + y
```

**3. 표현력 높음 (적은 코드로 많은 표현)**

```python
# 리스트 컴프리헨션
squares = [x**2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]

# 동시 할당 + 한 줄 스왑
a, b, c = 1, 2, 3
x, y = y, x

# with 문 — 자원 자동 정리
with open('file.txt') as f:         # 끝나면 자동 close
    content = f.read()
```

**4. "배터리 포함" (표준 라이브러리 풍부)**

Python 설치만으로 JSON/정규표현식/HTTP/날짜/수학 등 다 내장. Java처럼 Maven에서 안 깔아도 됨.
```python
import json, re, datetime, urllib.request    # 전부 표준
```

**5. 에러가 빨리 드러남 (REPL + 동적)**

```python
$ python
>>> x = [1, 2, 3]
>>> x[10]                # 바로 IndexError
>>> import numpy as np   # 바로 설치/사용
```

→ Java의 "컴파일 에러 → 수정 → 컴파일 → 또 에러" 사이클 없음.

#### C.5.2 반대로 불편한 점도 (공감)

- **컴파일 타임 검사 없음**: 실행해봐야 에러 앎 → 테스트 중요
- **느슨한 캡슐화**: private가 관례라 마음대로 접근 가능
- **성능**: Java/C#보다 보통 느림 (NumPy는 C 호출이라 빠름)
- **대규모 프로젝트**: 동적 타입이 발목 잡을 수 있음

#### C.5.3 결론

| 상황 | 편한가? |
|---|---|
| 스크립트/프로토타입 | ✅ 진짜 편함 |
| 데이터 분석/ML | ✅ NumPy 생태계 압도적 |
| 학습/교육 | ✅ 문법 얇아서 빠른 시작 |
| 대규모 엔터프라이즈 | ❌ Java/C#이 나음 |
| 시스템 프로그래밍 | ❌ C/Rust/Go가 나음 |

→ DeZero가 Python 쓰는 이유: "프레임워크 배울 때 언어 디테일에 안 끌리게".

**키워드**: `#Python철학` `#인터프리터` `#동적타입` `#표현력` `#배터리포함` `#REPL`

#### C.5.1 보너스: 연산자 우선순위는 변경 불가

> 브로 질문: "연산자 오버로딩은 가능하지만, 연산자 우선순위를 변경할 수는 없는 게 맞지?"

**정답!** 연산자 우선순위는 파이썬 언어 스펙에 **고정**. 오버로딩으로 바꿀 수 없음.

```python
class Variable:
    def __add__(self, other): ...
    def __mul__(self, other): ...

x = Variable(2)
# 파이썬은 항상 *를 +보다 먼저 계산 — 오버로딩과 무관
y = x + x * x        # x * x 먼저 → x + (x*x)
# (x + x) * x로 하려면 괄호 필수
y = (x + x) * x
```

`__add__`, `__mul__`은 **"연산이 수행될 때 무슨 일이 일어날까"** 만 정의. **"어떤 순서로 연산할까"** 는 언어가 결정. C++도 마찬가지.

**키워드**: `#연산자우선순위` `#변경불가` `#언어스펙고정` `#괄호강제`

---

### A.6 `lambda` 표현식 — 제한적이지만 특정 용도에선 국룰

> 브로 질문: "파이썬에서도 람다 표현이 많이 사용되나?"

**결론**: **제한적으로 많이 씀**. 파이썬 lambda는 다른 언어(JS, C#)보다 약하지만, 짧은 용도론 진짜 자주 쓰임.

#### 파이썬 lambda의 제약 — 표현식 1개만

```python
# 단일 표현식만 가능 (statement 안 됨)
square = lambda x: x ** 2
print(square(5))   # 25

# 이런 건 안 됨:
# f = lambda x:
#     y = x + 1       # ❌ 할당 statement
#     return y * 2     # ❌ return statement
```

→ "표현식 하나" 제약이 진짜 큰 한계. 여러 줄 로직은 `def` 써야.

#### 다른 언어와 비교 — 파이썬이 약한 편

```javascript
// JavaScript — 여러 줄 가능!
const f = (x) => {
    const y = x + 1;
    return y * 2;
};
```
```python
# Python — 여러 줄 불가능, def 써야
def f(x):
    y = x + 1
    return y * 2
```

| 언어 | lambda/익명 함수 | 파워 |
|---|---|---|
| **Lisp/Scheme** | 완전한 lambda (여러 줄) | ⭐⭐⭐⭐⭐ |
| **JavaScript** | 화살표 함수 (여러 줄) | ⭐⭐⭐⭐⭐ |
| **C#** | `=>` 람다 (여러 줄) | ⭐⭐⭐⭐ |
| **Java** | lambda (한 줄 권장, 여러 줄 가능) | ⭐⭐⭐⭐ |
| **Python** | lambda (**표현식 1개만**) | ⭐⭐ |
| **C++** | lambda (여러 줄) | ⭐⭐⭐⭐⭐ |

#### 그래도 자주 쓰는 곳

**1. `sorted`/`min`/`max`의 `key=` 인자 (가장 흔함)**
```python
students = [("철수", 90), ("영희", 85), ("민수", 95)]
sorted(students, key=lambda s: s[1])   # 점수순 정렬
# [('영희', 85), ('철수', 90), ('민수', 95)]

words = ["banana", "apple", "cherry"]
sorted(words, key=lambda w: len(w))    # 길이순
```

**2. `map`, `filter` (함수형 패턴)**
```python
squares = list(map(lambda x: x**2, [1, 2, 3]))      # [1, 4, 9]
evens = list(filter(lambda x: x % 2 == 0, [1,2,3,4,5,6]))  # [2, 4, 6]
```

**3. DeZero에서 (미래)**
```python
# step28+: 수치 미분에서 간단 함수 전달
def numerical_diff(f, x):
    h = 1e-4
    return (f(x + h) - f(x - h)) / (2 * h)

result = numerical_diff(lambda x: x ** 2 + 1, 2.0)
```

#### lambda vs def 선택 기준

| 상황 | 추천 | 이유 |
|---|---|---|
| **1줄 짜리 단순 함수** | ✅ `lambda` | 간결 |
| **여러 줄 로직** | ❌ `def` | lambda는 표현식 1개만 |
| **재사용 여러 번** | ❌ `def` | 이름 붙여서 명확하게 |
| **`key=` 인자 등 콜백** | ✅ `lambda` | 자연스러운 패턴 |
| **직렬화(pickle)** | ❌ `def` | lambda는 pickle 안 됨 |

#### 파이썬 철학 — "왜 lambda가 약할까?"

PEP 20: "There should be one-- and preferably only one --obvious way to do it."

→ lambda를 제한적으로 만든 이유. **"여러 줄 함수는 `def`가 명백한 정답이니까, lambda는 짧은 것만"**.

C#/JS는 "표현성" 중시 → lambda/화살표 함수 풀어줌.
파이썬은 "단순함" 중시 → lambda 제한.

#### 함정 — 클로저 캡처 버그

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])   # [2, 2, 2] ← 0,1,2가 아니라 다 2!
# 이유: lambda가 i를 참조하지만, i는 루프 끝나면 2
```

→ lambda 많이 쓰면 디버깅 지옥 가능. 특히 클로저 캡처 주의.

**키워드**: `#lambda` `#람다표현식` `#표현식1개제약` `#sorted_key` `#map` `#filter` `#closure함정` `#PEP20` `#단일명확방식` `#JS화살표함수비교` `#def권장`

---

### A.7 언패킹(unpacking) — 리스트/튜플을 변수로 쪼개기

> **step11 학습 중 추가** (2026-07-30)
> 다변수 함수(Add) 구현에서 `x0, x1 = xs`가 등장. 언패킹의 본질과 `*` 심화까지 정리.

#### A.7.1 핵심 — "상자를 열어 내용물을 각자에게"

**언패킹**: 우측의 리스트/튜플(여러 값을 담은 상자)을 좌측 변수 여러 개에 **쪼개서** 담는 연산.

```python
xs = [2, 3]
x0, x1 = xs       # x0=2, x1=3 — 리스트 원소를 각 변수에 분배

point = (10, 20)
px, py = point    # 튜플도 동일. px=10, py=20
```

리스트든 튜플이든 **반복 가능한(iterable) 객체**면 다 언패킹 가능.

##### step11에서의 실제 사용 (Add 다변수 함수)

```python
class Add(Function):
    def apply(self, xs):       # xs = [x0_data, x1_data] (리스트로 들어옴)
        x0, x1 = xs            # ★ 언패킹 — 리스트를 2개 변수로 분해
        y = x0 + x1            # 이제 분리된 변수로 연산
        return (y,)
```

Add는 **2개 입력**을 받는 다변수 함수. 리스트로 묶여 들어온 입력을 실제 연산을 위해 개별 변수로 풀어야 함 → 언패킹이 필수.

#### A.7.2 변수 개수 불일치 — 엄격한 규칙

Python은 **변수 개수와 원소 개수가 정확히 맞아야 함**. 안 맞으면 에러.

```python
xs = [2, 3]

x0, x1 = xs          # ✅ 2개 = 2개 → OK. x0=2, x1=3

x0 = xs              # ✅ 언패킹 아님 — x0 = [2, 3] (리스트 통째로)

x0, x1, x2 = xs      # ❌ ValueError: not enough values to unpack (expected 3, got 2)
                      #   "3개 기대했는데 2개뿐이라 못 채워"
```

에러 메시지가 친절: **"expected N, got M"** — 변수 N개 기대, 원소 M개뿐.

##### 함정: 쉼표 하나의 차이

```python
x0 = xs,             # ⚠️ 쉼표 → x0 = ([2,3],) 튜플로 감쌈 (언패킹 아님!)
x0 = xs              #     쉼표 없음 → x0 = [2,3] (그냥 할당)
x0, = xs             # ✅ 우측이 1원소 리스트면 → x0 = 2 (1개 변수 언패킹)
```

쉼표 하나로 "튜플 생성" vs "언패킹"이 갈림. 단항 튜플 `(x,)`의 쉼표와 같은 문법.

#### A.7.3 `*` 스플래트 — "나머지 전부를 리스트로"

개수가 안 맞을 때, **남는 걸 하나의 리스트로 몰아담는** 연산자.

```python
xs = [1, 2, 3, 4, 5]

first, *rest = xs            # first=1, rest=[2, 3, 4, 5]
*init, last = xs             # init=[1, 2, 3, 4], last=5
first, *middle, last = xs    # first=1, middle=[2, 3, 4], last=5
```

→ `*변수`는 "내가 안 받은 나머지 전부를 리스트로 가져라". **유연성의 핵심**.

##### `*`는 양끝에서 몇 개든 고정 가능

```python
a, b, *middle, c, d = [1, 2, 3, 4, 5]
# a=1, b=2, middle=[3], c=4, d=5
# ★ 앞 2개, 뒤 2개 고정 → 남은 것(middle) 흡수
```

양끝에서 "고정할 만큼" 일반 변수를 적고, 남는 걸 `*`가 흡수. 가운데가 비면 `middle = []`.

#### A.7.4 `*`는 여러 개 불가 — 모호성 때문에 문법 금지

```python
*a, *b = [1, 2, 3, 4]
# ❌ SyntaxError: two starred expressions in assignment
```

**왜 금지?** 모호성(ambiguity). `[1, 2, 3, 4]`를 어디서 자를지 Python이 결정 못 함:
- `a=[1,2], b=[3,4]`?
- `a=[1], b=[2,3,4]`?
- `a=[], b=[1,2,3,4]`?

→ **Python 철학**: 모호한 건 문법 자체에서 막아버림 (PEP 20: *"Ambiguity is the enemy of correctness"*).
언패킹은 **`*` 최대 1개**라는 단순 규칙. 이게 "읽기 좋은 언어"인 이유 중 하나.

#### A.7.5 `*`의 이중성 — 함수 정의 vs 호출 (★ step12 핵심)

> **step12 학습 중 추가** (2026-07-30). `def f(*args)`와 `f(*xs)`의 `*`가 같은 기호인데 반대 방향.
> 가변 인수(`*inputs`) 다루면서 반드시 짚고 넘어가야 할 포인트.

지금까지 A.7.3/A.7.4에선 **대입문 좌측**에서의 `*`를 봤음 (`first, *rest = xs`).
그런데 `*`는 **함수 정의/호출**에서도 등장하는데, 여기선 **문맥에 따라 정반대 역할**을 함. 헷갈림의 원인.

##### 이중성 — 같은 기호, 반대 방향

| 문맥 | 코드 | 역할 | 결과 타입 |
|---|---|---|---|
| **함수 정의** | `def f(*args):` | 여러 위치 인수 **수집** (모아서) | `tuple` |
| **함수 호출** | `f(*xs)` | 리스트/튜플 **풀어서** 전달 (펼쳐서) | 개별 인수들 |
| **대입 좌측** | `a, *rest = xs` | 나머지 **수집** (모아서) | `list` |

→ "정의"와 "대입 좌측"은 **수집**(모으는 방향), "호출"은 **펼침**(푸는 방향).

##### 직접 확인

```python
# --- 함수 정의에서의 * : 수집 (여러 인수 → tuple) ---
def add_all(*args):
    print(type(args))         # <class 'tuple'>
    print(args)               # (2, 3, 4)
    return sum(args)

add_all(2, 3, 4)              # 9 — 여러 인수를 tuple로 수집

# --- 함수 호출에서의 * : 펼침 (리스트/tuple → 개별 인수) ---
nums = [2, 3, 4]
add_all(*nums)                # add_all(2, 3, 4)와 동일 — 리스트를 풀어서 전달

# 둘이 같음
add_all(2, 3, 4)  ==  add_all(*[2, 3, 4])
```

##### ★ 브로 통찰 — "파라미터 문맥은 가변인수, 파라미터명은 튜플 타입"

`def f(*args):`에서:
- **문맥상 의미**: "임의 개수의 위치 인수를 받겠다" (가변 인수 / variadic)
- **변수 `args`의 타입**: `tuple` (수집된 결과)

→ "가변인수"라고 해서 `args`가 리스트나 특별한 타입이 아니라, **그냥 tuple**.
브로 지적: "파람 쪽 문맥은 가변인수란 소리고, 해당 파람명은 튜플 타입의 객체를 참조한다" — 정확히 맞음.

★ **검증**: `isinstance(args, tuple) == True` — `*args`로 수집된 결과는 일반 `tuple` 타입 객체.
특수 타입이 아니라 일반 tuple이라 인덱싱/슬라이싱/`len()`/`for` 전부 tuple처럼 사용 가능.
"언패킹 안 하고 튜플 그대로 넘겨도 되나?" → 그냥 tuple 객체 넘기는 것과 동일 (받는 쪽 시그니처에 따라 결과 다름 — 아래 심화 참조).

##### step12에서의 실제 사용 (DeZero 가변 인수)

```python
class Function:
    # --- 정의 측: *inputs로 가변 인수 수집 (tuple) ---
    def __call__(self, *inputs: Variable):
        # inputs는 tuple[Variable, ...] — 여러 Variable을 수집
        xs = []
        for x in inputs:
            xs.append(x.data)

        # --- 호출 측: *xs로 리스트를 펼쳐서 전달 ---
        ys = self.forward(*xs)       # ★ 리스트 xs를 풀어서 개별 인수로

    # forward도 가변 인수로 수집
    def forward(self, *xs: np.ndarray):
        return self.apply(*xs)        # ★ 다시 펼쳐서 apply에 전달

class Add(Function):
    def apply(self, x0, x1):          # ★ 결국 위치 인수 2개로 도착
        return x0 + x1
```

→ `*`가 **수집→펼침→수집→펼침** 파도처럼 전달되며 최종 Add.apply엔 깔끔한 위치 인수 `x0, x1`로 도착.

##### 외우기 팁

- **정의(`def`)에서 `*`** = "**모**아라" (**모**=정의, 수**모**)
- **호출(call)에서 `*`** = "**펼**쳐라" (호출은 펼침)
- 같은 기호지만 **관점이 반대**. 이걸 몰라서 "왜 tuple이지?" 헷갈렸던 것.

##### ★ 심화 — "수집→언패킹 상쇄"와 무한 전달 (step12 브로 질문에서 파생)

> 브로 질문: "forward가 가변인수 받고 apply 호출할 때 튜플 언패킹 일어나는 거 맞아?
> 자식이 apply 안 오버라이드하면 어케 되는데? 자식이 다시 가변인수로 받으면?"

이중성의 자연스러운 귀결 — **"수집(정의) → 언패킹(호출)" 짝이 역연산이라 상쇄**된다.

```python
def forward(self, *xs):           # xs = (2, 3) tuple (수집)
    return self.apply(*xs)        # 언패킹 → apply(2, 3) 호출

# 부모 apply (가변 인수) — 자식이 오버라이드 안 한 경우
def apply(self, *xs):             # ★ 다시 (2, 3) tuple로 수집 (원상복구!)
    raise NotImplementedError(...)
```

→ "수집→언패킹→수집" 이면 맨 끝의 수집이 처음 상태로 돌아감. **역연산이라 상쇄**.

##### 3가지 자식 apply 시나리오 — 모두 정상 동작

```python
class Function:
    def forward(self, *xs): return self.apply(*xs)   # 언패킹 호출
    def apply(self, *xs): raise NotImplementedError  # 부모: 가변

# 1) 안 오버라이드 → 부모 apply(*xs)가 흡수, NotImplementedError 정상
class Bad(Function): pass

# 2) 고정 인수로 오버라이드 → 깔끔한 위치 인수로 도착
class Add(Function):
    def apply(self, x0, x1): return x0 + x1          # 2개 고정

# 3) 다시 가변 인수로 오버라이드 → ★ 언패킹→수집→언패킹→수집 무한 전달
class VarAdd(Function):
    def apply(self, *xs): return sum(xs)             # 몇 개든
```

##### ★ 핵심 통찰 — 부모 apply를 `*xs`로 둔 설계적 이점

부모 apply를 고정 인수(`def apply(self, x)`)로 뒀으면, forward에서 `self.apply(*xs)` 언패킹 시
xs 원소 개수가 안 맞으면 **TypeError**. 하지만 부모 apply를 `*xs` 가변으로 두면:

- 자식이 **고정 N개**로 오버라이드 → N개로 도착 (정상)
- 자식이 **다시 가변 `*xs`** 로 오버라이드 → 몇 개든 흡수 (정상)
- 자식이 **안 오버라이드** → 부모가 흡수 후 NotImplementedError (정상)

→ ★ 부모 apply를 가변으로 둔 게 **"어떤 자식 시그니처든 깨지지 않는 안전한 기본 구현"** 이 됨.
이게 rezero 방향 (B) "apply도 forward와 동일 시그니처(`*xs`)"를 택한 숨은 이점.

> 🔗 **관련**: "자식이 부모와 다른 시그니처로 apply 오버라이드해도 된다"는 Python의 유연함 —
> 상세는 [C.1.4 심화 "오버라이드 시그니처 자유"](#심화--오버라이드는-시그니처가-달라도-된다-문화충격-포인트) 참조.

##### 시각화 — "파도"는 무한히 이어질 수 있다

```
__call__(*inputs)   수집 → (x0, x1)
    ↓ *xs 언패킹
forward(*xs)        수집 → (x0, x1)
    ↓ *xs 언패킹
apply(*xs) [부모]   수집 → (x0, x1)   ← 가변이면 여기서도 (x0,x1) 유지
    ↓ (자식이 다시 *xs면) 언패킹→수집 반복... 무한 전달 가능
apply(x0, x1) [자식] 고정 2개 도착   ← 또는 가변이면 계속 (x0, x1)
```

→ "수집→언패킹" 짝이 몇 번이고 이어질 수 있음. 어디서 `*xs` 받든 **튜플 형태로 보존**되므로 깨지지 않는다.

**키워드 추가**: `#star이중성` `#정의vs호출` `#수집과펼침` `#variadic` `#가변인수` `#tuple수집` `#언패킹전달` `#step12추가` `#파라미터문맥` `#브로통찰` `#상쇄` `#역연산` `#무한전달` `#안전한기본구현` `#부모apply가변이점`

#### A.7.6 for 루프에서 동시 언패킹 — 자주 쓰는 이디엄

이게 실전에 제일 많이 쓰임. 리스트 안의 튜플/리스트를 순회하며 바로 분해:

```python
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]

# 방법 1: 튜플 통째로 → 매번 언패킹 (번거러움)
for pair in pairs:
    num, letter = pair        # 매번 한 번 더 풀어야
    print(num, letter)

# 방법 2: for에서 바로 언패킹 (★ Pythonic)
for num, letter in pairs:     # ★ 한 번에 분해!
    print(num, letter)
```

##### DeZero 코드에서의 사례

```python
# step08 fill_grad에서 이미 사용 중
f = worklist.pop()
x, y = f.input, f.output     # ★ 우측 (f.input, f.output) 튜플 → 좌측 언패킹

# 딕셔너리 순회 (나중에 자주 쓸 패턴)
for key, value in some_dict.items():
    ...
```

우측이 튜플 리터럴 `(a, b)`여도 좌측 언패킹이 됨. 리스트만 해당되는 게 아님.

#### A.7.7 head/tail 패턴 — 함수형 프로그래밍 연결 ★

`first, *rest = xs`는 **함수형 프로그래밍의 head/tail 분해**와 정확히 같은 패턴.

```python
# Python — 언패킹으로 head/tail
first, *rest = [1, 2, 3, 4]   # first=1 (head), rest=[2,3,4] (tail)

# Haskell — 같은 개념
-- head [1,2,3,4] = 1
-- tail [1,2,3,4] = [2,3,4]
```

Haskell/Elixir/ML 계열에선 리스트 처리의 기본 단위. 재귀적 리스트 순회의 뼈대:
```haskell
-- Haskell: 리스트의 합 (재귀)
sumList [] = 0
sumList (x:xs) = x + sumList xs   -- x=head, xs=tail로 분해 후 재귀
```

Python도 같은 패턴 가능:
```python
def sum_list(lst):
    if not lst:
        return 0
    head, *tail = lst             # head/tail 분해
    return head + sum_list(tail)  # 재귀
```

##### ★ 유틸 함수로 직접 만들어 쓰기도

브로가 "head, tail 유틸 함수 다 만드는 거 아니냐" — 맞음! FP 스타일 좋아하는 사람들은 직접 만듦:

```python
def head(lst): return lst[0]
def tail(lst): return lst[1:]

# 또는 튜플 반환 버전
def uncons(lst):
    """리스트를 (head, tail)로 분해. 빈 리스트면 None."""
    return (lst[0], lst[1:]) if lst else None
```

`uncons`는 Haskell `unzip`/Elixir `hd`+`tl`에 대응. 다만 Python에선 언패킹 문법(`first, *rest`)이 더 직관적이라 유틸 함수까지 만드는 건 취향. DeZero에선 언패킹 문법 그대로 쓰는 게 자연스러움.

##### pipe/compose와의 연결 (step23 복선)

`head/tail` 분해 + `pipe` 합성은 **FP 리스트 처리 파이프라인**의 기본 조립 블록.
step23에서 pipe 재도입할 때 "리스트 처리 + 합성" 패턴이 자연스럽게 이어질 수 있음 (Issue #13의 FP 화두와 연결).

#### A.7.8 DeZero에서 언패킹이 계속 등장할 곳 (복선)

| step | 사용 예상 | 패턴 |
|---|---|---|
| step11~12 (현재) | `x0, x1 = xs` (Add 입력 분해) / `*xs` 가변 인수 | 리스트/가변 인수 → 변수 |
| step13 | `gx0, gx1 = gys` (Add 역전파 출력 분해) | 튜플 → 2변수 |
| step14 | 같은 변수 반복 사용 시 gradient 누적 | 누적 로직에서 다변 처리 |
| step16 | generation 정렬, 다중 노드 처리 | 리스트 순회 + 언패킹 |
| step34+ | 행렬 연산 (MatMul)에서 shape 분해 | `rows, cols = shape` |

→ 언패킹은 **2고지~4고지 전반에 깔리는 기본 이디엄**. 지금 확실히 잡아두는 게 투자.

#### A.7.9 요약표

| 패턴 | 코드 | 결과 |
|---|---|---|
| 딱 맞게 | `x0, x1 = [2, 3]` | `x0=2, x1=3` ✅ |
| 너무 많음 | `x0, x1, x2 = [2, 3]` | `ValueError` ❌ |
| 너무 적음 | `x0 = [2, 3]` | `x0=[2,3]` (통째로) |
| 나머지 묶기 | `first, *rest = [1,2,3,4]` | `first=1, rest=[2,3,4]` ✅ |
| 양끝 고정 | `a, *m, z = [1,2,3]` | `a=1, m=[2], z=3` ✅ |
| `*` 2개 | `*a, *b = [1,2,3]` | `SyntaxError` ❌ |
| ★ **정의 `*args`** | `def f(*args):` | 여러 인수 **수집** → tuple |
| ★ **호출 `*xs`** | `f(*xs)` | 리스트/튜플 **펼쳐** 전달 → 개별 인수 |
| 우측 튜플 | `x, y = a, b` | `x=a, y=b` |
| for 동시 | `for k, v in items:` | 각 원소 언패킹 순회 |
| head/tail | `h, *t = lst` | FP의 head/tail 분해 |

**키워드**: `#언패킹` `#unpacking` `#튜플언패킹` `#리스트언패킹` `#스플래트` `#star연산자` `#나머지묶기` `#middle패턴` `#별표1개제한` `#모호성금지` `#star이중성` `#정의vs호출` `#수집과펼침` `#variadic` `#가변인수` `#tuple수집` `#언패킹전달` `#파라미터문맥` `#브로통찰` `#for동시언패킹` `#head-tail` `#함수형프로그래밍` `#FP연결` `#PEP20` `#step11추가` `#step12추가` `#2고지기본이디엄`

---

## 📝 노트 푸터

**학습 완료일**: A.1~A.6 (2026-07-21, step01 직후) / A.7 (2026-07-30, step11~12) / C.1.4 심화 (2026-07-30, step12)
**관련 링크**:
- 탐구 #1 (Python 클래스/캡슐화): [exploration_01_python_basics.md](./exploration_01_python_basics.md)
- 탐구 #5 (객체 모델): [exploration_05_python_object_model.md](./exploration_05_python_object_model.md)
- 이 탐구는 원래 탐구 #1의 C 섹션에서 분리됨
- A.7 언패킹은 step11~12 다변수 함수(Add) 구현에서 파생 — [LEARNING_NOTES.md step11](../LEARNING_NOTES.md), [step12](../LEARNING_NOTES.md)
- A.7.5 `*` 이중성 / C.1.4 심화 오버라이드 시그니처 자유 — [rezero/steps/step12.py](../rezero/steps/step12.py)에서 실증
- A.7.7 head/tail은 pipe/compose FP 화두(Issue #13, step23 재도입)와 연결
