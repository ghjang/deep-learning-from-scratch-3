# 🧪 보충 탐구 #5 — Python 객체 모델 (내부 구조부터 메타클래스까지)

> **step01 직후 보충 학습 #5** (2026-07-21)
> 브로 통찰에서 출발: "`__dict__`가 있다는 건 내부가 딕셔너리 기반이고, 문법이 그걸 위한 syntactic sugar라는 뜻?"
> → **정답!** 파이썬 객체 모델의 근본을 파는 탐구. 향후 확장 가능한 큰 주제.

---

## 목차

- [A. CPython 내부 구조 — 딕셔너리 기반 객체 모델](#a-cpython-내부-구조--딕셔너리-기반-객체-모델)
- [B. (향후 추가) `type()`과 메타클래스](#b-향후-추가-type과-메타클래스)
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

## B. (향후 추가) `type()`과 메타클래스

> 클래스 자체도 객체. `type()`은 클래스의 클래스 (메타클래스).
> 브로가 관심 가지면 확장 예정.

예정 주제:
- `type(X)` vs `type(X).__name__`
- 메타클래스로 클래스 동적 생성
- `__class__` 속성
- DeZero에서 메타클래스 쓸 일 (거의 없음, 학습 목적)

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
