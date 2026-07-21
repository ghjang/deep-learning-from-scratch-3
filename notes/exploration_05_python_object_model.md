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

### A.8 핵심 통찰 요약

1. **브로 통찰 정답** — 파이썬 객체는 딕셔너리 기반, `self.x`는 `__dict__['x']`의 sugar
2. **CPython 내부** — `PyObject` 구조체가 `dict` 포인터 보유
3. **다른 동적 언어와 동일** — JS, Ruby, Lua도 "객체 = 해시맵 + sugar" 패턴
4. **동적 속성 추가** — 딕셔너리라서 언제든 새 키 추가 가능 (Java/C# 불가)
5. **`__slots__` 예외** — 딕셔너리 안 쓰는 최적화 (성능 중요 클래스)
6. **DeZero vs 실전 프레임워크** — DeZero는 dict 기반, 실전은 C 확장 최적화

**키워드**: `#CPython` `#PyObject` `#__dict__` `#딕셔너리기반` `#syntacticSugar` `#동적속성` `#__slots__` `#getattr` `#객체모델` `#JavaScript비교` `#성능함정`

---

## B. 런타임 클래스 검사 (리플렉션) — `__mro__`, `__bases__`, `__dict__`

> 브로 통찰에서 출발: "`__mro__`의 반환값이 튜플? 내용이 클래스 리스트? 메타적인 느낌?"
> → 정답! 런타임에 클래스 계층을 검사할 수 있는 능력 = **리플렉션(Reflection)**.

### B.1 보충: 리스트 vs 튜플 기본 (메타 속성 이해的前提)

먼저 파이썬 시퀀스 자료형 3종 정리. 메타 속성들이 튜플/리스트로 돼 있어서 필수.

```python
# 1. 리스트 (list) — 대괄호 [], 가변 (mutable)
lst = [1, 2, 3]
lst[0] = 99           # ✅ 수정 가능
lst.append(4)         # ✅ 추가 가능

# 2. 튜플 (tuple) — 소괄호 (), 불변 (immutable)
tup = (1, 2, 3)
# tup[0] = 99        # ❌ TypeError! 수정 불가
# tup.append(4)      # ❌ AttributeError!

# 3. 문자열 (str) — 따옴표, 불변 (immutable)
s = "hello"
# s[0] = "H"         # ❌ TypeError!
```

| 자료형 | 문법 | 가변? | 용도 |
|---|---|---|---|
| **list** | `[1, 2, 3]` | ✅ mutable | 동적 데이터, 추가/삭제 |
| **tuple** | `(1, 2, 3)` | ❌ immutable | 고정된 값, 다중 반환, **딕셔너리 키** |
| **str** | `"hello"` | ❌ immutable | 텍스트 |

**핵심 용어**:
- **mutable (가변)**: 생성 후 내용 변경 가능 — list, dict, set
- **immutable (불변)**: 생성 후 변경 불가 — tuple, str, int, float, bool

**왜 튜플이 필요한가?** — 불변 = "안 바뀐다는 약속"
1. **해시 가능** → 딕셔너리 키로 사용
   ```python
   d[(1, 2)] = "점"          # ✅ 튜플 키 OK
   # d[[1, 2]] = "점"        # ❌ 리스트는 키 불가 (가변이라)
   ```
2. **안전한 전달**: 함수 인자로 넘겨도 수정 못 함
3. **다중 반환**: 파이썬 함수는 사실 튜플 반환
   ```python
   def min_max(lst):
       return min(lst), max(lst)   # (min, max) 튜플
   low, high = min_max([3, 1, 4])  # 언패킹
   ```

→ `__mro__`, `shape`, `strides` 등이 튜플인 이유: **"이 값은 불변"이라는 약속**.

#### B.1.1 접근 문법이 같다 — 오리 타이핑과 type 체크

파이썬은 리스트/튜플/문자열의 **접근 문법이 동일**. `[0]`, 슬라이스, 이터레이션 전부 같음.

```python
lst = [1, 2, 3]
tup = (1, 2, 3)
s = "abc"

print(lst[0], tup[0], s[0])      # 1 1 a
print(lst[1:3], tup[1:3], s[1:3]) # [2, 3] (2, 3) bc
for x in lst: pass                # 전부 이터레이션 가능
for x in tup: pass
for x in s: pass
```

→ "오리처럼 걷고 오리처럼 울면 오리" = **오리 타이핑(duck typing)**. `[0]`로 인덱싱 가능하면 시퀀스처럼 쓰면 됨.

**type 체크는 거의 안 함**. 정말 필요할 때만:
```python
if isinstance(x, tuple):
    print("튜플 — 딕셔너리 키로 OK")

# 파이썬 권장 패턴 (EAFP — 일단 해보고 예외 잡기)
try:
    x[0] = 99
    print("mutable")
except TypeError:
    print("immutable")
```

#### B.1.2 튜플 원소가 mutable이면 내부 수정 가능 ⚠️

튜플 자체는 immutable이지만, 원소가 가변 객체(list 등)면 **그 원소의 내부는 수정 가능**. 미묘한 함정.

```python
tup = ([1, 2, 3], [4, 5, 6])
# tup[0] = [99]           # ❌ TypeError — 튜플의 참조 자체는 못 바꿈
tup[0].append(99)          # ✅ 원소 리스트 내부는 수정 가능
print(tup)                 # ([1, 2, 3, 99], [4, 5, 6])
```

**왜?** — immutability는 **"참조 레벨"**:
- 튜플이 immutable = 튜플이 들고 있는 **참조(포인터)**를 못 바꿈
- 참조가 가리키는 객체의 **내부**는 그 객체의 규칙을 따름

```
tup → [포인터A, 포인터B]    ← 튜플은 이 포인터들 못 바꿈 (immutable)
          ↓        ↓
        [1, 2]   [3, 4]      ← 이 리스트 내부는 바꿀 수 있음 (mutable)

tup[0].append(99)  →  포인터A가 가리키는 리스트의 내부 변경 (가능)
tup[0] = [...]     →  포인터A 자체를 다른 객체로 교체 (불가)
```

→ 이게 B.1.3(레퍼런스 정체)와 직접 연결됨.

#### B.1.3 파이썬 레퍼런스의 정체 — C 포인터와 비슷하지만 더 추상

파이썬 변수는 값을 담는 게 아니라 **객체를 가리키는 이름표(참조)**. C 포인터와 유사하지만 역참조(`*p`) 문법이 없이 자동 역참조.

```python
x = [1, 2, 3]
y = x                    # 대입 = 참조 복사 (얕은 복사)

print(id(x) == id(y))    # True — 같은 객체 (CPython에선 메모리 주소)
print(x is y)            # True

y.append(4)
print(x)                 # [1, 2, 3, 4] ← x도 바뀜! 같은 객체니까
```

**변수 모델 비교**:

| 언어 | 변수 모델 | `x = y` 의미 |
|---|---|---|
| C | 값/포인터 구분 | 값 복사 or 포인터 복사 (문법 구분) |
| Java | primitive=값, 객체=참조 | 타입마다 다름 |
| **Python** | **전부 참조** | **항상 참조 복사** |

→ 파이썬은 "모든 것이 객체"라 모든 변수가 사실 객체 참조. primitive/reference 구분 자체가 없음.

**`id()` 함수** — 객체 고유 식별자 (CPython에선 메모리 주소와 일치, 다른 구현체에선 다를 수 있음):
```python
x = [1, 2, 3]
z = [1, 2, 3]             # 새 리스트
print(x == z)             # True — 값 같음
print(x is z)             # False — 다른 객체
print(id(x) == id(z))     # False — 다른 식별자
```

**불변 객체는 "값처럼" 보임**:
```python
a = 5
b = a
b = 10                    # b가 새 int(10) 가리키게 됨
print(a)                  # 5 — 그대로 (a는 여전히 원래 5)

a = [1, 2]
b = a
b.append(3)               # 같은 리스트 내부 수정
print(a)                  # [1, 2, 3] — a도 바뀜!
```

→ 불변 객체는 재할당만 가능해서 값처럼 보이고, 가변 객체는 내부 수정이 드러나서 참조가 명확히 보임.

**얕은 복사 vs 깊은 복사**:
```python
import copy
x = [[1, 2], [3, 4]]
y = x                     # 참조 복사 (같은 객체)
z = copy.copy(x)          # 얕은 복사 (외부 리스트만 새로, 원소는 참조)
w = copy.deepcopy(x)      # 깊은 복사 (전부 새로)

x[0].append(99)
print(y)                  # [[1, 2, 99], [3, 4]] — 바뀜
print(z)                  # [[1, 2, 99], [3, 4]] — 바뀜 (원소 공유)
print(w)                  # [[1, 2], [3, 4]] — 안 바뀜 (완전 복사)
```

#### B.1.4 문자열 — 특수 취급되는 immutable 객체

문자열은 너무 자주 써서 별도 문법/최적화가 있는 immutable 객체. 수정 메서드는 전부 **새 문자열 반환**.

```python
s = "hello"
# s[0] = "H"             # ❌ TypeError — 직접 수정 불가

new_s = s.upper()
print(s)                  # "hello" — 원본 그대로
print(new_s)              # "HELLO" — 새 인스턴스

new_s2 = s.replace("l", "L")
print(s)                  # "hello" — 여전히
print(new_s2)             # "heLLo" — 새 인스턴스
```

**왜 특수 취급?**
1. **사용 빈도**: 전용 문법(`"..."`)과 최적화
2. **해시 캐싱**: 딕셔너리 키로 자주 써서, 한 번 해시 계산하면 캐싱 (불변이니까 가능)
3. **보안**: 모듈 이름, 속성 이름, 딕셔너리 키 등 바뀌면 안 되는 곳에 많이 쓰임
4. **인턴(intern)**: 짧은 문자열은 공유
   ```python
   a = "hello"; b = "hello"
   print(a is b)          # True — 같은 객체 (인턴됨)
   ```

**다른 언어와 비교**: Java `String`, C# `string`, JS `String` 전부 immutable. 현대 언어의 국룰.

**성능 함정 — 반복 결합**:
```python
# ❌ O(n²) — 매번 새 문자열 생성 + 복사
s = ""
for i in range(1000):
    s = s + str(i)

# ✅ O(n) — 한 번에 결합
parts = [str(i) for i in range(1000)]
s = "".join(parts)
```

→ 문자열 반복 결합 피하고 `"".join()` 쓰기.

**키워드**: `#튜플원소mutable함정` `#참조레벨불변` `#레퍼런스` `#객체참조` `#id함수` `#얕은복사` `#깊은복사` `#copy.deepcopy` `#문자열immutable` `#인턴` `#join` `#오리타이핑` `#EAFP`

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

### B.3 리플렉션 — 런타임에 클래스 계층 순회

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

### B.4 다른 메타 속성들

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

### B.5 리플렉션의 실전 활용 — getattr/setattr/hasattr

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

### B.6 DeZero에서의 실전 활용 (step49+ 예고)

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

### B.7 핵심 통찰 요약

1. **리스트 vs 튜플**: 가변/불변 차이. 튜플은 "안 바뀐다는 약속"
2. **`__mro__`** = `tuple` of `class` objects (불변 순서)
3. **리플렉션**: 런타임에 자기 구조를 검사하는 능력
4. **메타 속성 모음**: `__mro__`, `__bases__`, `__dict__`, `__name__`, `__subclasses__()`, `__class__`
5. **getattr/setattr/hasattr**: 문자열로 속성 다루는 메타프로그래밍 기초
6. **DeZero Layer.params()**: 리플렉션의 실전 활용 (step49+)

**키워드**: `#리플렉션` `#Reflection` `#__mro__` `#__bases__` `#__dict__` `#__name__` `#__subclasses__` `#__class__` `#getattr` `#setattr` `#hasattr` `#tuple` `#list` `#mutable` `#immutable` `#C3선형화` `#메타프로그래밍` `#Layerparams`

### B.8 룩업 체계 전체 지도 — 파이썬엔 5가지가 있다

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
