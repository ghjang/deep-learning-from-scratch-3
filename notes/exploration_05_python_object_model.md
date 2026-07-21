# 🧪 보충 탐구 #5 — Python 객체 모델 (내부 구조부터 메타클래스까지)

> **step01 직후 보충 학습 #5** (2026-07-21)
> 브로 통찰에서 출발: "`__dict__`가 있다는 건 내부가 딕셔너리 기반이고, 문법이 그걸 위한 syntactic sugar라는 뜻?"
> → **정답!** 파이썬 객체 모델의 근본을 파는 탐구. 향후 확장 가능한 큰 주제.

---

## 목차

- [A. CPython 내부 구조 — 딕셔너리 기반 객체 모델](#a-cpython-내부-구조--딕셔너리-기반-객체-모델)
- [B. 런타임 클래스 검사 (리플렉션) — `__mro__`, `__bases__`, `__dict__`](#b-런타임-클래스-검사-리플렉션--__mro__-__bases__-__dict__)
- [C. (향후 추가) Descriptor와 `@property` 내부](#c-향후-추가-descriptor와-property-내부)
- [D. `__new__` vs `__init__` — 생성과 초기화의 분리](#d-__new__-vs-__init__--생성과-초기화의-분리)
- [E. 함수도 객체, 클래스도 객체 — "모든 것이 객체"의 진짜 의미](#e-함수도-객체-클래스도-객체--모든-것이-객체의-진짜-의미)

---

## A. CPython 내부 구조 — 딕셔너리 기반 객체 모델

> 브로 통찰: "파이썬 객체는 내부적으로 딕셔너리 자료구조 기반이고, `self.x` 같은 문법은 그 딕셔너리 접근의 syntactic sugar인가?"
>
> **결론: 100% 정답.** 파이썬 객체는 `__dict__`라는 dict 객체로 속성을 저장. `self.x`는 `self.__dict__['x']`의 syntactic sugar.

### A.1 직접 증명해보기

```python
class Variable:
    def __init__(self, data):
        self.data = data
        self.grad = None

x = Variable(42)

# x.data는 사실...
print(x.data)                  # 42
print(x.__dict__['data'])      # 42  ← 같은 결과!

# __dict__가 진짜 딕셔너리인지 확인
print(type(x.__dict__))        # <class 'dict'>  ← 진짜 dict!
print(x.__dict__)              # {'data': 42, 'grad': None}
```

→ `x.data`는 `x.__dict__['data']`에 대한 syntactic sugar. 점 표기법이 더 읽기 쉬워서 쓰는 것.

### A.2 CPython 내부 구조

CPython에서 모든 파이썬 객체는 C 구조체 `PyObject` 기반. 인스턴스의 내부엔 실제로 `__dict__`라는 dict 객체를 가리키는 포인터가 있음:

```c
// CPython 단순화 (실제보다 단순)
typedef struct {
    PyObject_HEAD           // 참조 카운트, 타입 포인터 등
    PyObject *dict;         // ← __dict__ — 이게 속성 저장소!
} PyBaseObject_Object;
```

→ 즉 `self.data = 42`는 내부적으로 `dict.__setitem__('data', 42)` 호출. **속성 할당 = 딕셔너리 연산**.

### A.3 다른 동적 언어와의 비교

**JavaScript도 완전히 같은 패턴**:

```javascript
// JavaScript
const obj = { data: 42 };
console.log(obj.data);          // 42
console.log(obj['data']);       // 42  ← bracket notation = __dict__['data']와 동일!
```

| | Python | JavaScript | Ruby | Lua |
|---|---|---|---|---|
| 속성 저장 | `__dict__` (dict) | 내부 해시맵 | 내부 테이블 | 테이블 |
| 점 접근 | `obj.x` (sugar) | `obj.x` (sugar) | `obj.x` (sugar) | `obj.x` (sugar) |
| 괄호 접근 | `obj.__dict__['x']` (우회) | `obj['x']` (직접!) | `obj[:x]` | `obj['x']` (직접!) |
| 동적 속성 추가 | ✅ | ✅ | ✅ | ✅ |

→ 이래서 Python, JavaScript, Ruby, Lua 같은 동적 타입 언어를 **"dict-based object model"** 이라고도 부름. 모두 "객체 = 해시 테이블 + syntactic sugar" 패턴.

**JS가 좀 더 일관된 점**: 괄호 접근(`obj['x']`)을 언어 차원에서 직접 지원. Python은 `__dict__`로 우회해야 함. (하지만 `getattr(obj, 'x')`라는 내장 함수로 비슷하게 가능)

### A.4 동적 속성 — 딕셔너리 기반의 자연스러운 결과

```python
class Variable:
    def __init__(self, data):
        self.data = data

x = Variable(42)

# 클래스에 정의되지 않은 속성도 런타임에 추가 가능
x.new_attr = "동적 추가"        # ✅ __dict__['new_attr'] = "동적 추가"
x.tags = ["a", "b"]            # ✅
print(x.__dict__)
# {'data': 42, 'new_attr': '동적 추가', 'tags': ['a', 'b']}
```

→ Java/C#에선 불가능한 일. 클래스에 정의된 필드만 쓸 수 있으니까. Python은 딕셔너리 기반이라 **언제든 새 키 추가** 가능.

### A.5 `getattr`, `setattr`, `hasattr` — 딕셔너리 연산의 공식 인터페이스

```python
x = Variable(42)

# 점 접근과 동일
getattr(x, 'data')            # == x.data == x.__dict__['data']
setattr(x, 'grad', 0.0)       # == x.grad = 0.0 == x.__dict__['grad'] = 0.0
hasattr(x, 'data')            # == 'data' in x.__dict__

# 동적 속성 이름 (문자열로 접근) — 메타프로그래밍의 기초
attr_name = "da" + "ta"
print(getattr(x, attr_name))  # 42 — 런타임에 속성 이름 결정!
```

→ DeZero의 Layer 클래스(step49+)에서 `self.__dict__`를 순회하며 Parameter를 자동 수집하는 게 이 매커니즘 활용이야.

### A.6 `__slots__` — 딕셔너리 안 쓰는 최적화

딕셔너리 기반의代价: **메모리/속도 비용**. 이걸 최적화하려면 `__slots__`:

```python
# 일반적 (딕셔너리 기반)
class Variable:
    def __init__(self, data):
        self.data = data

x = Variable(42)
x.new_attr = "동적 추가 가능"   # ✅ 언제든 새 속성 추가 OK
print(x.__dict__)               # {'data': 42, 'new_attr': '...'}

# __slots__ (최적화 — 딕셔너리 안 씀)
class FastVariable:
    __slots__ = ('data', 'grad')   # 허용된 속성만 고정
    def __init__(self, data):
        self.data = data

y = FastVariable(42)
# y.new_attr = "추가"           # ❌ AttributeError!
print(hasattr(y, '__dict__'))    # False! ← 딕셔너리 자체가 없음
```

→ `__slots__`를 쓰면 속성을 C 구조체의 **고정 필드**로 저장해서 메모리 절약 + 속도 향상. 대신 동적 속성 추가 불가.

### A.7 성능 함정 — 왜 딥러닝 프레임워크는 다르게 만들까?

딕셔너리 기반의代价:
- **메모리**: 속성마다 dict entry (키+값+해시) — int 하나 저장하는데도 수 배 메모리
- **속도**: 속성 접근 시마다 해시 계산 → C 구조체 직접 접근보다 느림
- **수백만 객체**: 딥러닝처럼 엄청 많은 인스턴스 만들면 비용 누적

→ 이래서 실제 성능 중요 클래스는 다르게 구현:

| 클래스 | 구현 방식 | 이유 |
|---|---|---|
| DeZero `Variable` | 파이썬 dict 기반 | 학습 목적, 단순함 우선 |
| NumPy `ndarray` | C 확장, 고정 구조체 | 성능 critical |
| PyTorch `Tensor` | C 확장 (ATen), `__slots__` | 성능 critical |

→ DeZero는 학습 목적이라 `__slots__` 안 씀. 하지만 실전 프레임워크는 다 최적화돼 있음.

### A.8 상속과 `__dict__` — "평평한 구조"의 함의

> 브로 통찰에서 출발: "파이썬은 private 없다며? 그럼 상위 클래스의 인스턴스 변수는 하위 인스턴스의 `__dict__`에 다 들어 있나?"
>
> **결론: `super().__init__()` 호출하면 들어감.** 상속 자체가 아니라 `__init__` 실행 여부가 결정. 그리고 출처 구분 없이 **평평하게 한 dict에 몰빵.**

#### 핵심: 상속 ≠ 자동 속성 복사

```python
class A:
    def __init__(self):
        self.x = 1       # A의 __init__이 self.x를 세팅하는 코드

class B(A):
    def __init__(self):
        super().__init__()   # ← A의 __init__을 호출 → 이때 self.x = 1 실행
        self.y = 2

b = B()
print(b.__dict__)
# {'x': 1, 'y': 2}  ← 둘 다 b의 dict에 들어감
```

→ `b.x`가 생긴 건 **A의 `__init__`이 실행돼서**. "A를 상속하니까 자동으로"가 **아님**.

#### `super().__init__()` 안 하면?

```python
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        self.y = 2
        # super().__init__() 안 함!

b = B()
print(b.__dict__)        # {'y': 2} ← x 없음!
print(hasattr(b, 'x'))   # False
# b.x  # ❌ AttributeError
```

→ 상속만 하고 `__init__` 안 부르면 `b.x`는 안 생김. **실행 여부가 전부.**

#### Python vs Java/C# — 평평함의 차이

**Java/C# (슬롯 기반)**:
```
b → ┌─────────────────┐
    │ A 영역: x = 1    │ ← 상위 클래스 영역 (private 접근 통제 가능)
    ├─────────────────┤
    │ B 영역: y = 2    │ ← 하위 클래스 영역
    └─────────────────┘
    (출처 구분 가능)
```

**Python (평평한 dict)**:
```
b → __dict__: { 'x': 1, 'y': 2 }
    (출처 구분 없음, 다 같은 dict)
```

→ 이래서 파이썬엔 진짜 private가 없음. **"이 속성은 어느 클래스에서 왔나"를 안 추적**하니까.

#### 이름 충돌? 그냥 덮어쓰기

```python
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        super().__init__()   # A가 self.x = 1
        self.x = 999         # B가 self.x = 999 (덮어쓰기!)

b = B()
print(b.__dict__)   # {'x': 999} ← 하나뿐, 출처 흔적 없음
```

→ Java/C#이면 `A.x`와 `B.x`를 구분할 수 있지만, 파이썬은 **평평한 dict라서 그냥 덮어씀.**

#### DeZero에서의 실전 (미래 예고)

```python
class Variable:
    def __init__(self, data):
        self.data = data
        self.grad = None
        self.creator = None

class Parameter(Variable):    # step50+
    def __init__(self, data):
        super().__init__()    # Variable의 속성들이 self.__dict__로 옴
        self.requires_grad = True

p = Parameter(np.array(1.0))
print(p.__dict__)
# {'data': ..., 'grad': None, 'creator': None, 'requires_grad': True}
# ← Variable 것이든 Parameter 것이든 한 평면에
```

→ 상속 구조가 복잡해져도 인스턴스 변수는 **하나의 dict**로 관리. 그래서 탐색도 단순하고 빠름.

#### A.8.1 실수 함정과 정적 분석 도구

평평한 구조는 유연하지만 **실수하기 좋은 구조**이기도 함. 브로 직관 정답 — 진짜 골때리는 함정들이 있음.

##### 함정 1: `super().__init__()` 까먹기 (제일 흔함)

```python
class Variable:
    def __init__(self, data):
        self.data = data
        self.grad = None

class Parameter(Variable):
    def __init__(self, data):
        # super().__init__() 까먹음!
        self.requires_grad = True

p = Parameter(np.array(1.0))
print(p.requires_grad)   # True ✅
# p.data                  # ❌ AttributeError!
# p.grad                  # ❌ AttributeError!
```

→ 에러 메시지가 `"'Parameter' has no attribute 'data'"`라서 **원인이 super 누락이라는 걸 바로 알기 어려움**.

##### 함정 2: 부모의 `__init__`을 늦게 호출 (순서 함정)

```python
class Base:
    def __init__(self):
        self.items = []    # 부모가 초기화

class Child(Base):
    def __init__(self):
        self.items.append(1)   # ❌ 먼저 쓰려고 함!
        super().__init__()      # 여기서야 items 생성

c = Child()
# AttributeError: 'Child' object has no attribute 'items'
```

→ **초기화 순서**가 진짜 함정. 부모가 세팅하는 걸 자식이 먼저 쓰면 죽음.

##### 함정 3: 이름 충돌 덮어쓰기 (조용함, 더 위험)

```python
class NamedVariable(Variable):
    def __init__(self, data, name):
        super().__init__(data)
        self.name = name       # 의도함 ✅
        # 근데 실수로 self.data를 잘못된 값으로 덮어쓰면?
        # self.data = name     # ← ndarray여야 하는데 문자열 들어감
```

→ **에러 안 나고 조용히 잘못됨.** 이게 제일 무서움. 정적 분석도 잡기 어려움.

##### 정적 분석 도구 — 함정을 잡아주는 도구들

브로가 "정적 분석 툴이 경고를 때려줄 것 같다"고 한 거 정답. 주요 도구:

| 도구 | 역할 | 특징 |
|---|---|---|
| **mypy** | 타입 체커 | 타입 힌트 기반으로 버그 사전catch. 가장 강력 |
| **pylint** | 전통 린터 | `W0231: __init__ from base class is not called` 등 명시적 경고 |
| **ruff** | 요즘 대세 린터 | mypy+pylint 부분집합인데 진짜 빠름. 최근 국룰 |
| **pyright** (VSCode Pylance) | 타입 체커 | 브로가 쓰는 것! 일부 함정 잡아줌 |

```python
# mypy/pylint가 잡아주는 예
class Parameter(Variable):
    def __init__(self, data):
        self.requires_grad = True
        # mypy/pylint: "W0231: __init__ method from base class is not called"
```

→ 브로가 앞서 Pylance 언급했는데, 진짜 이런 함정을 잡아주는 도구가 Pylance(pyright 기반).

##### 왜 파이썬이 메모리 구조를 "신경 안 쓰는" 언어인가

브로 통찰 정답. 파이썬 철학: **"사람이 신경 쓸 일 아니다"**

```
C/C++:     메모리 구조 직접 관리 (포인터, malloc/free, vtable...)
Java/C#:   VM이 관리하지만 슬롯 구조는 컴파일 타임에 결정
Python:    "메모리? 그냥 dict에 넣어둘게. 넌 로직에 집중해"
```

→ 런타임에 동적으로 결정하는 걸 우선. **메모리 효율보다 개발자 편의**. 그래서:
- ✅ 빠른 코딩, 유연함, 프로토타이핑 강함
- ❌ 메모리 낭비, 성능 손실, 실수하기 좋은 구조

**"관대한 언어"의 양면성**:

| 장점 | 단점 |
|---|---|
| 동적 속성 추가 | 실수해도 조용히 넘어감 |
| 타입 안 가림 | 잘못된 타입 들어가도 실행 |
| 런타임에 클래스 수정 | 정적 분석 제한적 |
| 빠른 프로토타이핑 | 대규모 코드에선 위험 |

→ **"신뢰할 수 있는 어른"** 에게 맞는 언어. PEP 20 (Zen of Python):
> "명시적이 함축적보다 낫다" (Explicit is better than implicit)

##### DeZero 학습 중 실전 팁

1. **상속받으면 무조건 `super().__init__(...)` 쓰기** (습관)
2. **VSCode Pylance 경고 잘 보기** (super 누락 잡아줌)
3. **단위 테스트 작성** (이름 충돌 같은 조용한 버그 잡기)
4. (선택) 나중에 타입 힌트 + mypy 도입

##### 도구 선택 가이드 — 4개 도구가 전부 다르다

브로 직감 정답: 4개 도구는 전부 서드파티(파이썬 표준 아님). 2개 카테고리로 나뉨.

```
┌─ 타입 체커 (Type Checker) ────────┐
│  mypy    (파이썬 진영 원조, 느림)  │
│  pyright (MS제, 빠름, VSCode 통합) │
└───────────────────────────────────┘

┌─ 린터 (Linter) ───────────────────┐
│  pylint (전통, 잔소리 많음, 느림)   │
│  ruff   (신세대, Rust제, 빠름, 대세)│
└───────────────────────────────────┘
```

**각 도구 상세**:

| 도구 | 종류 | 특징 | 비고 |
|---|---|---|---|
| **ruff** | 린터 | Rust로 작성, 진짜 빠름 (10~100배). pylint+flake8+isort 통합. 요즘 대세 | Astral 사 (uv와 같은 회사) |
| **pyright** | 타입 체커 | MS제. **VSCode Pylance의 엔진**. mypy보다 빠르고 정확 | 브로가 이미 쓰고 있음 |
| **mypy** | 타입 체커 | 타입 힌트 검사 원조. Guido 관여. 안정적 | 느림, 엄격 모드 아니면 허술 |
| **pylint** | 린터 | 2003년부터. 상세 분석. super 누락에 강함 | 잔소리 과다, 최근 ruff로 대체 추세 |

**요즘 국룰 조합**: ruff + pyright (FastAPI, Pydantic, Hugging Face 등 메이저 프로젝트 대부분)

##### 우리 프로젝트 추천: Pylance(pyright) + (필요시 ruff)

브로 상황 분석:
- VSCode + Pylance 이미 사용 → **pyright는 이미 충족**
- 학습용 프로젝트 → 너무 엄격하면 질림
- uv 기반 환경 → ruff와 같은 회사라 통합 자연스러움

**결정 트리**:
```
VSCode 쓰나요? ─── 네 ───→ Pylance(pyright) 이미 충족 ✅
        │
        아니요 ───→ mypy 또는 pyright 별도 설치

추가로 린터 필요?
   안 함 ──── 학습 단계라 충분할 수 있음
   도입 ──── ruff 추천 (uv와 같은 회사, 빠름)
```

##### 우리 프로젝트에 ruff 도입한다면 (참고용)

```bash
# ruff 설치 (uv로, 개발 의존성으로)
uv add --dev ruff
```

```toml
# pyproject.toml에 추가
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "W", "I"]  # 기본 린트 규칙
# E: pycodestyle errors
# F: pyflakes (잘못된 import, 미사용 변수 등)
# W: warnings
# I: isort (import 정렬)
```

→ **지금 당장은 Pylance만으로 충분**. 학습 진행하면서 필요해지면 ruff 도입 검토.

**키워드**: `#상속` `#__dict__평평함` `#super().__init__` `#출처무관` `#이름충돌덮어쓰기` `#Java슬롯비교` `#private없음연결` `#Parameter상속` `#실수함정` `#린터` `#mypy` `#pylint` `#ruff` `#pyright` `#Pylance` `#정적분석` `#PEP20` `#관대한언어` `#도구선택가이드` `#ruff추천` `#uv와같은회사` `#결정트리`

---

### A.9 핵심 통찰 요약

1. **브로 통찰 정답** — 파이썬 객체는 딕셔너리 기반, `self.x`는 `__dict__['x']`의 sugar
2. **CPython 내부** — `PyObject` 구조체가 `dict` 포인터 보유
3. **다른 동적 언어와 동일** — JS, Ruby, Lua도 "객체 = 해시맵 + sugar" 패턴
4. **동적 속성 추가** — 딕셔너리라서 언제든 새 키 추가 가능 (Java/C# 불가)
5. **`__slots__` 예외** — 딕셔너리 안 쓰는 최적화 (성능 중요 클래스)
6. **상속도 평평하게** — 출처 구분 없이 한 dict에 몰빵 (`super().__init__` 실행 시)
7. **DeZero vs 실전 프레임워크** — DeZero는 dict 기반, 실전은 C 확장 최적화

**키워드**: `#CPython` `#PyObject` `#__dict__` `#딕셔너리기반` `#syntacticSugar` `#동적속성` `#__slots__` `#getattr` `#객체모델` `#JavaScript비교` `#성능함정` `#상속평평함`

---

## B. 런타임 클래스 검사 (리플렉션) — `__mro__`, `__bases__`, `__dict__`

> 브로 통찰에서 출발: "`__mro__`의 반환값이 튜플? 내용이 클래스 리스트? 메타적인 느낌?"
> → 정답! 런타임에 클래스 계층을 검사할 수 있는 능력 = **리플렉션(Reflection)**.

> 💡 **기본 자료형(list/tuple/str/레퍼런스)은 분리됨**: [exploration_06_data_types.md](./exploration_06_data_types.md)
> 이 섹션은 **리플렉션/메타 속성**에 집중.

### B.1 리플렉션 — 런타임에 클래스 계층 순회

#### B.1.1 `__mro__` 정의 — Method Resolution Order

**다중 상속 시 어떤 부모 클래스부터 찾을지 결정하는 순서**. C3 알고리즘으로 계산.

```python
class A:
    def hi(self): return "A"
class B(A):
    def hi(self): return "B"
class C(A):
    def hi(self): return "C"
class D(B, C):       # 다중 상속
    pass

mro = D.__mro__
print(mro)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

print(type(mro))     # <class 'tuple'>   ← 튜플!
print(type(mro[0]))  # <class 'type'>    ← 요소는 클래스 객체!
```

→ 브로가 발견한 3가지 정답: 튜플이다 / 클래스를 담았다 / 메타적인 느낌 (순회 가능).

**튜플인 이유**: MRO는 **클래스 정의 시점에 결정된 불변의 순서**. 런타임에 바뀌면 안 돼 (메서드 탐색이 흐트러짐).
```python
D.__mro__[0] = SomeOtherClass   # ❌ TypeError — MRO는 절대 바뀌면 안 됨
```

**C3 규칙**:
- 자식이 부모보다 먼저, 부모는 선언 순서대로, 충돌 시 TypeError
- DeZero는 단일 상속만 쓰므로 MRO 단순 (`Variable → object`)
- C3 알고리즘의 자세한 내용은 [exploration_01 용어 안내](./exploration_01_python_basics.md#📖-자주-인용하는-용어-안내) 참조

#### B.1.2 리플렉션 — 런타임 순회

`__mro__`를 순회하면 **런타임에 클래스 계층 검사** 가능. 이게 **리플렉션(Reflection)**.

```python
# 1. MRO 순회하며 모든 조상 클래스 이름 출력
for cls in D.__mro__:
    print(f"- {cls.__name__}")
# - D
# - B
# - C
# - A
# - object

# 2. 특정 조상이 있는지 확인
print(any(cls.__name__ == 'A' for cls in D.__mro__))   # True

# 3. 모든 조상의 메서드 수집
all_methods = set()
for cls in D.__mro__:
    for name, attr in cls.__dict__.items():
        if callable(attr):
            all_methods.add(name)
print(all_methods)
```

→ 브로의 "메타적인 느낌"이 진짜 정확했어. 이게 메타프로그래밍의 시작점.

### B.2 다른 메타 속성들

```python
class D(B, C): pass

# 1. 직계 부모들만 (튜플)
print(D.__bases__)
# (<class 'B'>, <class 'C'>)

# 2. 클래스 이름 (문자열)
print(D.__name__)        # 'D'
print(D.__qualname__)    # 'D' (중첩 클래스면 경로 포함)

# 3. 클래스가 정의된 모듈
print(D.__module__)      # '__main__'

# 4. 클래스의 모든 속성 (읽기 전용 딕셔너리)
print(D.__dict__)
# mappingproxy({...}) ← 읽기 전용 dict (수정 불가)

# 5. 어떤 클래스의 서브클래스들
print(A.__subclasses__())
# [<class 'B'>, <class 'C'>]

# 6. 인스턴스가 어느 클래스에서 왔는지
x = D()
print(x.__class__)       # <class '__main__.D'>
print(x.__class__.__name__)  # 'D'
```

### B.3 리플렉션의 실전 활용 — getattr/setattr/hasattr

속성 이름을 **문자열로** 다루는 내장 함수. 런타임에 속성 결정 가능.

```python
x = Variable(42)

# 점 접근과 동일
getattr(x, 'data')            # == x.data
setattr(x, 'grad', 0.0)       # == x.grad = 0.0
hasattr(x, 'data')            # == 'data' in dir(x) or hasattr

# 동적 속성 이름 (런타임에 결정) — 메타프로그래밍 기초
attr_name = "da" + "ta"       # 런타임에 문자열 조합
print(getattr(x, attr_name))  # 42 — 동적 접근!
```

### B.4 DeZero에서의 실전 활용 (step49+ 예고)

DeZero의 **Layer 클래스**가 리플렉션을 진짜로 활용:

```python
class Layer:
    def params(self):
        """이 Layer가 가진 모든 Parameter를 자동 수집."""
        for name, attr in self.__dict__.items():    # 인스턴스 속성 순회
            if isinstance(attr, Parameter):
                yield attr
            elif isinstance(attr, Layer):           # 중첩 Layer도 순회
                yield from attr.params()
```

→ `__dict__`를 순회하며 Parameter를 자동 수집! 브로가 "순회할 수 있다"고 한 직관이 DeZero 핵심 코드에 실제로 쓰임.

### B.5 핵심 통찰 요약

1. **리스트 vs 튜플**: 가변/불변 차이. 튜플은 "안 바뀐다는 약속"
2. **`__mro__`** = `tuple` of `class` objects (불변 순서)
3. **리플렉션**: 런타임에 자기 구조를 검사하는 능력
4. **메타 속성 모음**: `__mro__`, `__bases__`, `__dict__`, `__name__`, `__subclasses__()`, `__class__`
5. **getattr/setattr/hasattr**: 문자열로 속성 다루는 메타프로그래밍 기초
6. **DeZero Layer.params()**: 리플렉션의 실전 활용 (step49+)

**키워드**: `#리플렉션` `#Reflection` `#__mro__` `#__bases__` `#__dict__` `#__name__` `#__subclasses__` `#__class__` `#getattr` `#setattr` `#hasattr` `#tuple` `#list` `#mutable` `#immutable` `#C3선형화` `#메타프로그래밍` `#Layerparams`

### B.6 룩업 체계 전체 지도 — 파이썬엔 5가지가 있다 (★ 공식 참조)

> ⭐ **이 섹션은 룩업 체계의 공식 참조점**. 다른 탐구(exploration_01 A.2.4 등)에서
> 룩업을 다룰 때 핵심만 요약하고 여기로 링크.

> 브로 질문: "LEGB 룩업이랑 MRO 룩업 2개만 있는 거 아냐?"
> → **아니요, 5가지!** 일상 코딩에선 2개가 90%라 그렇게 느껴질 뿐.

#### 용어 정리 — "MRO 룩업"은 정확한 표현이 아님

엄밀히 말해 MRO는 **"속성 룩업의 일부 단계"** 야. 전체 체계는 이렇게:

| 브로 표현 | 공식/관용 명칭 | 발동 상황 |
|---|---|---|
| "LEGB 룩업" | **이름 룩업 (Name Lookup)** | `x` (점 없는 이름) |
| "MRO 룩업" | **속성 룩업 (Attribute Lookup)**, MRO는 그 일부 | `obj.x`, `self.x`, `ClassName.x` |

속성 룩업의 전체 단계:
```
self.x를 찾을 때:
  1. 인스턴스 __dict__ 확인
  2. 클래스 __dict__ 확인
  3. 부모 클래스들 확인 ← 여기서 MRO 순서 사용!
  4. 데이터 디스크립터 확인 (심화)
  5. __getattr__ 정의돼 있으면 호출 (심화)
```

→ MRO는 3번 단계에서 부모를 탐색하는 순서. 그래서 "MRO 룩업"보다는 **"속성 룩업(MRO 사용)"** 이 정확.

#### 파이썬의 5가지 룩업 체계

**1️⃣ 이름 룩업 (Name Lookup) = LEGB**

점(`.`) 없이 이름만 쓸 때. exploration_01 A.2.4 참조.
```python
def foo():
    x = 1            # L에서 찾음
    print(x)         # LEGB 순서
```

**2️⃣ 속성 룩업 (Attribute Lookup) = 인스턴스→클래스→MRO**

점(`.`)으로 접근할 때. 위에서 설명한 5단계.
```python
obj.x
# 1. obj.__dict__
# 2. type(obj).__dict__ + MRO 순회
# 3. (심화) descriptor 확인
# 4. (심화) __getattr__ 호출
```
→ DeZero의 `self.data` 접근이 여기 해당.

**3️⃣ 인덱스 룩업 (Index Lookup)**

대괄호 `obj[key]`로 접근할 때. `__getitem__` 메서드가 발동.
```python
lst = [1, 2, 3]
lst[0]              # 내부적으로 lst.__getitem__(0) 호출

d = {"a": 1}
d["a"]              # __getitem__("a")
```
→ DeZero step21의 `F.get_item(x, 0)`이 결국 이거.

**4️⃣ 임포트 룩업 (Import Lookup)** — 모듈 시스템

`import numpy` 할 때 파이썬이 모듈을 찾는 과정.
```python
import numpy        # 파이썬이:
                    # 1. sys.modules에 있나? (캐시)
                    # 2. sys.path의 각 디렉토리에 있나?
                    # 3. 없으면 ModuleNotFoundError
```

**5️⃣ (심화) 디스크립터 룩업 (Descriptor Lookup)**

`@property`, `@staticmethod` 등이 동작하는 핵심 메커니즘. 클래스 레벨에서 속성 접근을 가로챔.
```python
class C:
    @property
    def x(self):           # 이건 일반 메서드가 아니라 descriptor
        return self._x

c = C()
c.x                        # 단순 속성 룩업처럼 보이지만
                            # 실제론 C.x.__get__(c, C) 호출
```
→ 이 탐구 C 섹션(향후 추가)에서 다룰 주제. `@property`의 진실.

#### 한눈에 정리

| 룩업 종류 | 발동 상황 | 예 | 관련 __dunder__ |
|---|---|---|---|
| **이름 (LEGB)** | 점 없는 이름 | `x` | (없음) |
| **속성 (MRO 사용)** | 점으로 접근 | `obj.x`, `self.x` | `__getattribute__`, `__getattr__` |
| **인덱스** | 대괄호 접근 | `obj[key]` | `__getitem__` |
| **임포트** | import 문 | `import numpy` | (모듈 시스템) |
| **디스크립터** | 속성이 descriptor일 때 | `@property`, `@staticmethod` | `__get__`, `__set__` |

#### 핵심 통찰

- 일상 코딩에선 **1번(이름) + 2번(속성)** 이 90% → 그래서 2개로 느껴짐
- DeZero를 끝까지 배우면 **3번(인덱스, step21) + 5번(디스크립터, @property)** 까지 다 다루게 됨
- "파이썬은 사실 복잡한 룩업 체계를 가진 언어" — 브로가 직감한 게 정답

**키워드**: `#룩업체계` `#NameLookup` `#AttributeLookup` `#IndexLookup` `#ImportLookup` `#DescriptorLookup` `#__getitem__` `#__getattribute__` `#__getattr__` `#5가지룩업`

---

## C. (향후 추가) Descriptor와 `@property` 내부

> `@property`가 실제로 어떻게 동작하는지 (descriptor protocol: `__get__`, `__set__`).
> exploration_01 B.2의 심화.

예정 주제:
- `property()` 함수의 정체 (descriptor 반환)
- `__get__`, `__set__`, `__delete__` 프로토콜
- 커스텀 descriptor 만들기
- DeZero의 Layer가 `__dict__` 순회하는 원리와 연결

---

## D. `__new__` vs `__init__` — 생성과 초기화의 분리

> 브로 통찰에서 출발: "private 없다며? 그럼 `__new__` 같은 내부 함수도 호출 가능?"
> → **정답! 호출 가능.** "private 없다"와 "매직 메서드 접근 가능"은 같은 맥락.

### D.1 `__new__` 직접 호출 — 진짜 된다

```python
class Foo:
    def __new__(cls, *args, **kwargs):
        print("__new__ 호출됨")
        instance = super().__new__(cls)   # 진짜 인스턴스 생성
        return instance

    def __init__(self, x):
        print("__init__ 호출됨")
        self.x = x

# 1. 보통 방식
f = Foo(42)
# __new__ 호출됨
# __init__ 호출됨

# 2. __new__만 직접 호출!
g = Foo.__new__(Foo)
# __new__ 호출됨
print(type(g))         # <class 'Foo'>  ← 인스턴스 생김!
print(hasattr(g, 'x')) # False ← __init__ 안 돌아서 x 없음
```

→ **진짜 호출 가능**. `__new__`만 부르면 `__init__` 없이 인스턴스가 만들어짐.

### D.2 생성 vs 초기화 — 역할 분담

```python
f = Foo(42)
# 실제로 일어나는 일:
# 1. Foo.__new__(Foo, 42) → 인스턴스 생성 (메모리 할당)
# 2. Foo.__init__(f, 42)  → 인스턴스 초기화 (self.x = 42)
```

| 메서드 | 역할 | 반환 | 자주 쓰나? |
|---|---|---|---|
| `__new__` | **생성** (메모리 할당, 객체 만들기) | 인스턴스 객체 | ❌ 거의 안 오버라이드 |
| `__init__` | **초기화** (속성 세팅 등) | None | ✅ 매번 오버라이드 |

→ Java/C#의 `new ClassName()`이 **두 단계를 합친 것**. 파이썬은 명시적으로 분리.

### D.3 "private 없다"의 극단적 예시 — 매직 메서드 전부 직접 호출

```python
class MyClass:
    def __init__(self):
        self.data = 42

    def __str__(self):
        return f"MyClass({self.data})"

x = MyClass()
print(x)              # MyClass(42) — 보통 호출 (print가 __str__ 자동 호출)
print(x.__str__())    # MyClass(42) — 직접 호출도 가능!
print(x.__init__())   # None — 다시 초기화 호출도 가능! (data 다시 42로)
print(x.__class__)    # <class 'MyClass'> — 내부 속성 노출
print(x.__dict__)     # {'data': 42} — 내부 딕셔너리 노출
```

→ **전부 접근 가능**. Java/C#이었다면 private/internal로 막혔을 내부가 다 열려있음.

### D.4 왜 이렇게 개방적일까?

#### 이유 1: "consenting adults" (어른들의 합의)

파이썬 철학: **"숨길 수는 있지만, 막지는 않는다"**.
- `_name` (밑줄 1개): "내부용이야, 건드리지 마" (관례)
- `__name` (밑줄 2개): 이름을 좀 비틀어 (`_ClassName__name`) 접근 어렵게 함
- 하지만 둘 다 **기술적으로는 접근 가능**

#### 이유 2: 리플렉션/메타프로그래밍의 힘

이 개방성이 진짜 유용할 때가 있음. DeZero의 `Layer` 클래스:

```python
class Layer:
    def params(self):
        """이 Layer가 가진 모든 Parameter 자동 수집."""
        for name, attr in self.__dict__.items():    # __dict__ 직접 접근!
            if isinstance(attr, Parameter):
                yield attr
```

→ `__dict__` 같은 "내부"에 직접 접근할 수 있어서 **런타임에 객체 구조 검사/조작**이 가능. 이게 파이썬 메타프로그래밍의 기반.

#### 이유 3: 데코레이터/컨텍스트 매니저의 동작

```python
@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)        # getattr로 내부 접근
    setattr(Config, name, value)             # setattr로 설정
    try:
        yield
    finally:
        setattr(Config, name, old_value)     # 복구
```

→ DeZero의 `no_grad` (step18+)가 이 패턴 사용. 개방성 없이는 불가능.

### D.5 "할 수 있다" ≠ "해야 한다" — pythonic 관례

```python
obj._internal_method()    # ⚠️ 관례상 하지 말 것 (밑줄 1개)
obj.__private_method()    # ❌ 직접 호출 안 됨 (이름 맹글링)
obj._ClassName__private_method()   # 기술적으론 가능하지만 비권장

# 매직 메서드는 보통 직접 호출 안 함:
len(x)        # ✅ 이렇게 (len()이 __len__ 호출)
x.__len__()   # ⚠️ 직접 호출은 비관용적
```

→ **"pythonic"한 코드는 매직 메서드를 직접 부르지 않음.** `len(x)`, `str(x)`, `repr(x)` 같은 내장 함수 쓰기.

### D.6 파이썬 개방성 스펙트럼

```
완전 공개      권장하지 않음      기술적으로 막힘 (우회 가능)
   │              │                    │
 public      _protected          __private (네임 맹글링)
data, x    _internal_var      __really_private
__init__   _helper_method     __secret_method
__new__
__dict__
```

→ 전부 "호출/접근 가능"하지만, **관례**로 접근 자제를 합의한 것뿔.

### D.7 언제 `__new__`를 직접 오버라이드할까?

거의 안 함. 다음 예외적 상황에만:

1. **불변(immutable) 타입 상속** — `int`, `str`, `tuple` 등
   ```python
   class PositiveInt(int):
       def __new__(cls, value):
           if value < 0:
               raise ValueError("음수 안 됨")
           return super().__new__(cls, value)   # int는 __init__ 못 쓰니 __new__에서 검증
   ```
   → `int`는 불변이라 `__init__`으로 값 못 바꿈. `__new__`에서 처리.

2. **싱글톤 패턴** — 인스턴스 하나만 만들기
   ```python
   class Singleton:
       _instance = None
       def __new__(cls):
           if cls._instance is None:
               cls._instance = super().__new__(cls)
           return cls._instance

   a = Singleton()
   b = Singleton()
   print(a is b)   # True — 같은 인스턴스
   ```

3. **메타클래스** — 클래스 생성 가로채기 (심화)

→ DeZero에선 **이런 거 안 함**. 학습 목적이라 `__init__`만 쓰는 단순 구조.

### D.8 핵심 통찰 요약

1. **`__new__`와 `__init__`은 분리됨** — 생성 vs 초기화
2. **매직 메서드 전부 직접 호출 가능** (private 없음의 결과)
3. **개방성의 이유**: consenting adults 철학 + 리플렉션/메타프로그래밍
4. **하지만 pythonic 관례**: 매직 메서드는 내장 함수로 (`len(x)` 등)
5. **`__new__` 오버라이드**: 불변 타입 상속/싱글톤 등 예외적 상황에만
6. **DeZero는 안 씀** — 학습 목적이라 `__init__` 중심

**키워드**: `#__new__` `#__init__` `#생성vs초기화` `#매직메서드직접호출` `#private없음` `#consentingadults` `#리플렉션` `#pythonic관례` `#싱글톤` `#불변타입상속` `#개방성스펙트럼`

---

## E. 함수도 객체, 클래스도 객체 — "모든 것이 객체"의 진짜 의미

> 브로 통찰에서 출발: "cls로 '클래스 참조'라는 건, 타입 정보 자체를 특수 메타객체처럼 취급한다는 거?"
> → **정답!** 클래스 자체도 객체야. 이게 파이썬 철학 "모든 것이 객체"의 진짜 의미.

### E.1 클래스 자체도 객체 (메타객체)

```python
class Variable:
    pass

x = Variable()         # x는 Variable의 인스턴스 (일반 객체)

print(type(x))         # <class 'Variable'>  ← x의 타입은 Variable
print(type(Variable))  # <class 'type'>      ← Variable의 타입은 type!
```

→ `Variable` 클래스 자체가 **`type`이라는 메타클래스의 인스턴스**. 그래서 "특수 메타객체"라는 브로 표현이 진짜 정확함.

### E.2 클래스가 객체라는 증거 (직접 실험)

```python
class Variable:
    count = 0
    def __init__(self, data):
        self.data = data

# 1. 클래스를 변수에 담을 수 있음 (일급 객체)
ClsRef = Variable
x = ClsRef(np.array(1.0))     # Variable()과 동일!
print(type(x))                 # <class 'Variable'>

# 2. 클래스를 함수 인자로 전달
def create_instance(cls, *args):
    return cls(*args)

y = create_instance(Variable, np.array(2.0))
print(type(y))                 # <class 'Variable'>

# 3. 클래스의 속성 접근 (객체니까)
print(Variable.__name__)       # 'Variable'   ← 클래스의 속성
print(Variable.__bases__)      # (<class 'object'>,)
print(Variable.__dict__)       # {'count': 0, '__init__': ...}
print(id(Variable))            # 4316873984   ← 고유 식별자

# 4. 클래스를 리스트에 담기
classes = [Variable, int, str, list]
print(classes)                 # [<class '__main__.Variable'>, <class 'int'>, ...]
```

→ **전부 객체로서의 행위**. 변수에 담기, 인자로 전달, 속성 접근, 컬렉션에 담기. 다 가능.

### E.3 시각화 — 메타클래스 체인

```
인스턴스         클래스          메타클래스
─────────       ───────         ─────────
x       ─→    Variable   ─→     type
y       ─→    Variable   ─→     type
42      ─→    int        ─→     type
"hi"    ─→    str        ─→     type
[1,2]   ─→    list       ─→     type

특이점: type ─→ type (자기 자신의 인스턴스!)
```

→ 모든 클래스의 타입은 `type`. 그리고 `type` 자체도 `type`의 인스턴스 (재귀적!).

```python
print(type(type))   # <class 'type'>  ← type도 type의 인스턴스
```

### E.4 `cls`가 바로 이 메타객체

브로가 짚은 "cls로 클래스 참조"가 바로 이 이야기:

```python
class Variable:
    count = 0

    @classmethod
    def from_list(cls, lst):       # cls = 클래스 자체 (메타객체)
        print(f"cls = {cls}")             # <class '__main__.Variable'>
        print(f"cls.__name__ = {cls.__name__}")  # 'Variable'
        return cls(np.array(lst))         # cls()로 인스턴스 생성!
```

→ `cls`는 단순한 "참조"가 아니라 **실제 조작 가능한 클래스 객체**. 인스턴스 생성(`cls()`), 속성 접근(`cls.attr`), 심지어 클래스 자체 수정까지 가능.

### E.5 메타클래스의 마법 — 클래스 동적 생성

```python
# 보통: class 키워드로 정의
class Variable: ...

# 동적 생성: type() 호출로 런타임에 클래스 만들기!
Variable2 = type('Variable', (object,), {'count': 0, 'data': None})
# 인자: (이름, 부모 튜플, 속성 딕셔너리)

print(Variable2)             # <class '__main__.Variable'>
print(Variable2.__name__)    # 'Variable'
print(Variable2.count)       # 0
```

→ `type(...)` 호출로 **런타임에 새 클래스를 생성** 가능. 이게 메타프로그래밍의 극한.

### E.6 함수도 객체 (callable 객체)

함수도 마찬가지로 객체야:

```python
def foo(x):
    return x * 2

print(type(foo))              # <class 'function'>  ← 함수 객체

# 일급 객체 (first-class object)의 특성:
# 1. 변수에 담기
bar = foo
print(bar(3))                 # 6

# 2. 인자로 전달
def apply(f, x):
    return f(x)
print(apply(foo, 5))          # 10

# 3. 반환값
def get_multiplier():
    return foo
f = get_multiplier()
print(f(7))                   # 14

# 4. 컬렉션에 담기
funcs = [foo, str, int]
print(funcs[0](10))           # 20
```

→ 함수도 변수/인자/반환/컬렉션 모두 가능. 일반 객체와 동일한 취급.

### E.7 "callable" — 호출 가능한 객체의 공통점

함수, 클래스, 그리고 `__call__` 정의한 인스턴스 전부 **callable**:

```python
# 1. 함수는 callable
def foo(): return 42
foo()                # 42

# 2. 클래스는 callable (인스턴스 생성)
class Foo: pass
Foo()                # <Foo 객체> ← 호출하면 인스턴스 생성

# 3. __call__ 정의한 인스턴스도 callable
class Doubler:
    def __call__(self, x):
        return x * 2

d = Doubler()
print(d(5))          # 10 ← 인스턴스를 함수처럼 호출!
```

→ DeZero의 Function 클래스가 이 패턴 사용! `f = Square(); y = f(x)` 형태 (step02+).

### E.8 다른 언어와의 비교

| 언어 | 클래스의 정체 | 동적 생성 |
|---|---|---|
| **Python** | `type`의 인스턴스 (객체) | ✅ `type(...)`로 런타임 생성 가능 |
| **Java** | `Class<T>` 객체로 존재하지만 제한적 | 리플렉션으로 일부 가능 |
| **C#** | `Type` 객체, 리플렉션 지원 | 리플렉션으로 가능 |
| **C++** | 런타임 객체 아님 (컴파일 타임 개념) | ❌ 불가 |

→ 파이썬이 극단적으로 "클래스도 객체"를 관철한 언어.

### E.9 핵심 통찰 요약

1. **클래스도 객체** — `type` 메타클래스의 인스턴스 (브로 "메타객체" 통찰 정답)
2. **`cls`는 메타객체 참조** — 실제 조작 가능 (인스턴스 생성, 속성 접근, 수정)
3. **함수도 객체** — 변수/인자/반환/컬렉션 전부 가능 (일급 객체)
4. **callable의 공통점** — 함수, 클래스, `__call__` 인스턴스 전부 호출 가능
5. **메타클래스** — `type(...)`으로 런타임에 클래스 자체 생성
6. **DeZero 연결** — Function 클래스가 `__call__` 사용 (step02+ 핵심)

**키워드**: `#클래스도객체` `#메타객체` `#type` `#메타클래스` `#cls` `#classmethod` `#일급객체` `#callable` `#__call__` `#동적클래스생성` `#Java비교` `#firstclass` `#function객체`

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- exploration_01 A.2 (멤버 접근 규칙): [exploration_01_python_basics.md](./exploration_01_python_basics.md)
- exploration_01 B.2 (@property): 같은 파일
- CPython 공식: https://docs.python.org/3/c-api/
- 향후 브로가 "메타클래스", "descriptor", "__new__" 등 질문하면 B/C/D/E 섹션 채우기
