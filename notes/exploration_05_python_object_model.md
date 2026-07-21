# 🧪 보충 탐구 #5 — Python 객체 모델 (내부 구조부터 메타클래스까지)

> **step01 직후 보충 학습 #5** (2026-07-21)
> 브로 통찰에서 출발: "`__dict__`가 있다는 건 내부가 딕셔너리 기반이고, 문법이 그걸 위한 syntactic sugar라는 뜻?"
> → **정답!** 파이썬 객체 모델의 근본을 파는 탐구. 향후 확장 가능한 큰 주제.

---

## 목차

- [A. CPython 내부 구조 — 딕셔너리 기반 객체 모델](#a-cpython-내부-구조--딕셔너리-기반-객체-모델)
- [B. 런타임 클래스 검사 (리플렉션) — `__mro__`, `__bases__`, `__dict__`](#b-런타임-클래스-검사-리플렉션--__mro__-__bases__-__dict__)
- [C. (향후 추가) Descriptor와 `@property` 내부](#c-향후-추가-descriptor와-property-내부)
- [D. (향후 추가) `__new__` vs `__init__`](#d-향후-추가-__new__-vs-__init__)
- [E. (향후 추가) 함수도 객체, 클래스도 객체](#e-향후-추가-함수도-객체-클래스도-객체)

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

**키워드**: `#상속` `#__dict__평평함` `#super().__init__` `#출처무관` `#이름충돌덮어쓰기` `#Java슬롯비교` `#private없음연결` `#Parameter상속`

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

## D. (향후 추가) `__new__` vs `__init__`

> 진짜 인스턴스 생성 단계. `__init__`은 초기화일 뿐, 생성은 `__new__`.

예정 주제:
- `__new__`가 반환하는 것 (인스턴스)
- 왜 보통 안 쓰는지 (immutable 타입 상속할 때만)
- `Variable()` 호출 시 내부 순서: `__new__` → `__init__`

---

## E. (향후 추가) 함수도 객체, 클래스도 객체

> "Python은 모든 것이 객체"의 진짜 의미.

예정 주제:
- 함수도 callable 객체 (`def foo` → `foo`는 `function` 타입 객체)
- 클래스도 callable 객체 (`class Foo` → `Foo`는 `type` 타입 객체)
- `__call__` 메서드 (이후 step02 Function에서 핵심!)
- 일급 객체 (first-class object)의 의미

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- exploration_01 A.2 (멤버 접근 규칙): [exploration_01_python_basics.md](./exploration_01_python_basics.md)
- exploration_01 B.2 (@property): 같은 파일
- CPython 공식: https://docs.python.org/3/c-api/
- 향후 브로가 "메타클래스", "descriptor", "__new__" 등 질문하면 B/C/D/E 섹션 채우기
