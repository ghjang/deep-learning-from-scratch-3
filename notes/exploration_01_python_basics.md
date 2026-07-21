# 🧪 보충 탐구 #1 — Python 클래스 / NumPy / 프레임워크 기본기

> **step01 직후 보충 학습** (2026-07-21)
> step 진도 외에 파이썬/NumPy/프레임워크 등 깊이 파고 싶었던 주제 12개 정리.
> 형식: 핵심 요약 + 짧은 코드 예시. 자세한 건 키워드로 검색.

---

## 목차

- **Python 기본 (6)**
  - [1.1 `self`는 정확히 뭔가요?](#11-self는-정확히-뭔가요-)
  - [1.2 `__init__`은 왜 양쪽에 언더바가? (dunder)](#12-__init__은-왜-양쪽에-언더바가-dunder-)
  - [1.3 `class Variable:` vs `class Variable(object):`](#13-class-variable-vs-class-variableobject-)
  - [1.4 `__init__` 외에 어떤 dunder이 있나요?](#14-__init__-외에-어떤-dunder이-있나요-)
  - [1.5 `@staticmethod`, `@classmethod`가 뭔가요?](#15-staticmethod-classmethod가-뭔가요-)
  - [1.6 Python에 "primitive type"이 있나요? (박싱 비유 깊이)](#16-python에-primitive-type이-있나요-박싱-비유-깊이-)
- **NumPy (3)**
  - [1.7 `ndarray`는 내부적으로 어떻게 메모리를 쓰나요?](#17-ndarray는-내부적으로-어떻게-메모리를-쓰나요-)
  - [1.8 `shape` vs `size` vs `ndim` 헷갈림](#18-shape-vs-size-vs-ndim-헷갈림-)
  - [1.9 `np.array(1.0)`이 0차원인 이유](#19-nparray10이-0차원인-이유-)
- **프레임워크 (2)**
  - [1.10 왜 프레임워크들은 다 "Tensor"/"Variable" 래퍼를 쓸까?](#110-왜-프레임워크들은-다-tensorvariable-래퍼를-쓸까-)
  - [1.11 `is_simple_core` 스위치는 왜 만들어졌을까?](#111-is_simple_core-스위치는-왜-만들어졌을까-)
- **비교 (1)**
  - [1.12 Python에서 `==` vs `is` 차이](#112-python에서--vs-is-차이-)

---

## Python 기본 (6)

### 1.1 `self`는 정확히 뭔가요? 🐍

**요약**: `self`는 **"인스턴스 자기 자신"을 가리키는 참조**. 인스턴스 메서드의 첫 번째 인자로 필수이며, 파이썬이 호출 시 자동으로 넣어줌. 이름은 `self`가 아니어도 작동하지만 **관례**(PEP 8)이므로 무조건 `self` 쓸 것.

```python
class Variable:
    def __init__(self, data):     # self는 인스턴스 자신
        self.data = data          # 인스턴스 속성으로 저장

x = Variable(np.array(1.0))
# 실제로는 Variable.__init__(x, np.array(1.0)) 처럼 호출됨
# 파이썬이 x를 self 자리에 자동 바인딩
```

- Java/C#의 `this`와 같은 역할. 단, 파이썬은 **명시적**으로 적어야 함(Java/C#은 생략 가능).
- `self.data = data`는 "이 인스턴스의 `data` 속성에 `data`를 저장".

**키워드**: `#self` `#this` `#인스턴스참조` `#명시적` `#PEP8`

---

### 1.2 `__init__`은 왜 양쪽에 언더바가? (dunder) 🐍

**요약**: `__init__`은 **dunder**(double underscore) 메서드. 파이썬이 특정 상황에 자동 호출하도록 예약된 "매직 메서드". `__init__`은 인스턴스 생성 직후 초기화 용도로 자동 호출됨.

```python
x = Variable(np.array(1.0))
# 내부적으로:
#   1. Variable.__new__(Variable) → 빈 인스턴스 생성
#   2. Variable.__init__(x, np.array(1.0)) → 초기화 자동 호출
```

- 다른 주요 dunder들 (이후 step에서 계속 등장):
  - `__repr__`: `print(x)` 시 표시 형식
  - `__add__`, `__mul__`: 연산자 오버로딩 (step20+)
  - `__len__`, `__getitem__`: 컨테이너 인터페이스 (step21+)
  - `__call__`: 인스턴스를 함수처럼 호출 (step02에서 Function이 사용!)

**키워드**: `#dunder` `#매직메서드` `#__init__` `#__new__` `#자동호출`

---

### 1.3 `class Variable:` vs `class Variable(object):` 🐍

**요약**: Python 3에서는 **동일**. Python 2 시절엔 `object` 상속해야 "새 스타일 클래스"가 됐지만, Python 3는 모든 클래스가 암묵적으로 `object` 상속. 책은 간결함을 위해 `class Variable:` 사용.

```python
class Variable:        # Python 3 스타일 (권장)
    pass

class Variable(object):  # Python 2 호환 스타일 (구식)
    pass

# 둘 다 type(Variable) == <class 'type'> 동일
```

**키워드**: `#파이썬2vs3` `#새스타일클래스` `#object상속`

---

### 1.4 `__init__` 외에 어떤 dunder이 있나요? 🐍

**요약**: 파이썬은 클래스에 **수십 개의 dunder**를 정의할 수 있고, 각각 특정 상황에 자동 호출됨. DeZero에서 핵심적으로 쓰이는 것들만 정리.

```python
class Variable:
    def __init__(self, data):       # 생성/초기화
        self.data = data

    def __repr__(self):             # print(x) or x 출력 시
        return f"Variable(data={self.data})"

    def __add__(self, other):       # x + other
        return self.data + other

    def __len__(self):              # len(x)
        return len(self.data)

    def __mul__(self, other):       # x * other
        return self.data * other

x = Variable(np.array(2.0))
print(x)         # __repr__ 호출 → "Variable(data=2.0)"
print(x + 3)     # __add__ 호출 → 5.0
print(len(x))    # __len__ 호출
```

→ 책의 후반 step들에서 Variable에 dunder들이 점진적으로 추가됨. `__add__`/`__mul__`은 step20, `__len__`/`__getitem__`은 step21에서.

**키워드**: `#dunder목록` `#연산자오버로딩` `#__repr__` `#__add__` `#__call__`

#### 💡 1.4 보충: f-string `f"..."` 이 뭐예요? (질문에서 파생)

**요약**: f는 **f**ormat의 약자. Python 3.6+ 도입. 중괄호 `{}` 안에 **파이썬 표현식**을 넣어 문자열에 값 끼워넣기. 현대 Python의 국룰.

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

**역사적 순서** (왜 f-string이 국룰인지):
```python
# 1. %-formatting (C 스타일, 옛날)
"이름: %s" % name

# 2. str.format() (Python 2.6+)
"이름: {}".format(name)

# 3. f-string (Python 3.6+) ⭐ 현대 국룰, 가장 빠르고 읽기 쉬움
f"이름: {name}"
```

**rezero 코드에서 쓴 곳** (`rezero/steps/step01.py`의 `inspect()`):
```python
print(f"[{label:>10}] data={x.data!s:>10}  ndim={x.data.ndim}")
#     {label:>10}   → label 값, 우측 정렬, 폭 10
#     {x.data!s}    → !s는 str()로 변환 (ndarray를 문자열로)
```

**키워드**: `#f-string` `#format` `#포맷팅` `#중괄호표현식` `#Python36` `#PEP498`

---

### 1.5 `@staticmethod`, `@classmethod`가 뭔가요? 🐍

**요약**: 둘 다 "인스턴스 없이 호출 가능한 메서드"지만 차이가 있음. DeZero의 Function 구현(step02+)에서 `@staticmethod`가 자주 등장.

```python
class Variable:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def static_method(data):        # self, cls 안 받음. 그냥 함수와 동일
        return Variable(data)

    @classmethod
    def class_method(cls, data):    # cls = 클래스 자신 (Variable)
        return cls(data)

# 둘 다 인스턴스 없이 호출 가능
x1 = Variable.static_method(np.array(1.0))
x2 = Variable.class_method(np.array(1.0))
```

- **static**: 클래스/인스턴스 정보 불필요. 그냥 함수인데 클래스 네임스페이스에 묶어둔 것.
- **class**: 서브클래스에서 `cls`가 자동으로 서브클래스로 바뀜. 팩토리 메서드에 자주 사용.
- DeZero의 `Function.forward`는 종종 `@staticmethod`로 선언됨 (self 없이 입력만 받기 위해).

**키워드**: `#staticmethod` `#classmethod` `#데코레이터` `#self없음` `#팩토리`

#### 💡 1.5 보충: classmethod vs staticmethod — 오버라이드 관점 (질문에서 파생)

**브로 질문**: "classmethod는 하위 클래스에서 오버라이드 가능, staticmethod는 접근은 가능하지만 오버라이드 안 되는 형태?"

**요약**: 절반 맞고 절반 틀림. **둘 다 오버라이드 가능**. 핵심 차이는 **`cls`가 자동 교체되는지**. classmethod는 자식 클래스에서 호출 시 `cls`가 자식으로 자동 바뀜. staticmethod는 클래스 정보 자체를 모름.

```python
class Animal:
    name = "Animal"

    @classmethod
    def whoami(cls):               # cls = 호출한 클래스
        return f"나는 {cls.name}"

    @staticmethod
    def breathe():                 # 클래스 정보 안 받음
        return "숨 쉼"


class Dog(Animal):
    name = "Dog"                   # 오버라이드 (클래스 속성)

# Animal에서 호출
print(Animal.whoami())   # "나는 Animal"
print(Animal.breathe())  # "숨 쉼"

# Dog에서 호출 (Dog은 whoami/breathe 오버라이드 안 함)
print(Dog.whoami())      # "나는 Dog"  ← cls가 Dog로 자동 교체!
print(Dog.breathe())     # "숨 쉼"      ← 여전히 Animal 것 (클래스 정보 无)
```

**결정적 차이**:
| | classmethod | staticmethod |
|---|---|---|
| 오버라이드 가능? | ✅ | ✅ |
| 자식 호출 시 `cls` 자동 교체? | ✅ `cls`가 자식 클래스 | ❌ 클래스 정보 자체 不知 |
| 주 용도 | 팩토리 메서드, 서브클래스 인식 | 단순 유틸 함수 |

**classmethod가 빛나는 순간** (팩토리 메서드):
```python
class Variable:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_list(cls, lst):       # cls가 핵심!
        return cls(np.array(lst))  # 서브클래스여도 올바른 타입 생성

class TensorVariable(Variable):
    pass

t = TensorVariable.from_list([1, 2, 3])
print(type(t))   # <class 'TensorVariable'>  ← cls가 TensorVariable!
```

→ 만약 `from_list`가 `@staticmethod`였다면 항상 `Variable`만 만들었을 것.

**키워드**: `#classmethod` `#staticmethod` `#cls자동교체` `#팩토리메서드` `#상속` `#오버라이드`

---

### 1.6 Python에 "primitive type"이 있나요? (박싱 비유 깊이) 🐍

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

## NumPy (3)

### 1.7 `ndarray`는 내부적으로 어떻게 메모리를 쓰나요? 🔢

**요약**: `ndarray`는 **C 구조체 + 연속 메모리 블록** 기반. 파이썬 객체는 얇은 헤더(메타정보)만 가지고, 실제 데이터는 C 배열에. 이래서 빠름.

```python
arr = np.array([[1.0, 2.0], [3.0, 4.0]])
# 내부 구조 (단순화):
# ┌────────────────────┐
# │ ndarray 헤더        │  ← shape, dtype, strides 등 메타 (파이썬 객체)
# ├────────────────────┤
# │ 1.0 │ 2.0 │ 3.0 │ 4.0 │  ← 연속 C 메모리 (진짜 데이터)
# └────────────────────┘
print(arr.shape)     # (2, 2)  ← 헤더 정보
print(arr.dtype)     # float64
print(arr.strides)   # (16, 8)  ← 각 축 이동 시 바이트 수
```

- `strides`: 다음 요소로 가는 바이트 오프셋. (16, 8) = 행 이동 16바이트, 열 이동 8바이트
- 이 구조 덕분에 `reshape`, `transpose`가 **데이터 복사 없이** 메타만 바꿔서 O(1)로 동작
- 고차원 배열도 메모리는 **1차원 평탄화**되어 저장. shape/strides로 다차원 해석

**키워드**: `#ndarray` `#C기반` `#strides` `#연속메모리` `#dtype` `#헤더`

---

### 1.8 `shape` vs `size` vs `ndim` 헷갈림 🔢

**요약**: 셋 다 배열의 "형태"를 묘사하지만 다른 정보. 외워두면 NumPy 생활이 편해짐.

```python
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

print(arr.ndim)     # 2          ← 차원 수 (축 개수)
print(arr.shape)    # (2, 3)     ← 각 축의 크기 튜플
print(arr.size)     # 6          ← 전체 원소 수 = prod(shape)

# 관계: size == shape 원소들의 곱
# (2, 3) → 2 * 3 = 6
# (2, 3, 4) → 24

# 다른 예
np.array(5).shape          # ()      0차원
np.array([1,2,3]).shape    # (3,)    1차원 (길이 3)
np.array([[1],[2]]).shape  # (2, 1)  2차원
```

- `ndim` = `len(shape)` (항상)
- `size` = `prod(shape)` (항상)
- DeZero에선 보통 `shape`을 많이 씀 (레이어 출력 형태 맞출 때)

**키워드**: `#shape` `#size` `#ndim` `#형태정보` `#prod`

---

### 1.9 `np.array(1.0)`이 0차원인 이유 🔢

**요약**: 수학에서 **스칼라**는 0차원. "축"이 없는 단일 값. NumPy는 이 수학적 정의를 그대로 따름. 괄호를 하나 감쌀 때마다 차원이 1씩 증가.

```python
# 괄호 수 = 차원 수
np.array(5)             # 0차원, shape ()
np.array([5])           # 1차원, shape (1,)
np.array([[5]])         # 2차원, shape (1, 1)
np.array([[[5]]])       # 3차원, shape (1, 1, 1)
# 전부 "원소는 5 하나"지만 차원이 다름

# 수학 대응:
#   스칼라   → 0차원   5
#   벡터    → 1차원   [1, 2, 3]
#   행렬    → 2차원   [[1,2],[3,4]]
#   텐서    → 3차원+  이미지, 시계열 등
```

- DeZero 초반(step01~step40)은 스칼라/벡터(0~1차원) 위주
- step41+에서 텐서(2차원+) 다루기 시작. VGG16 같은 CNN은 4차원(N, C, H, W).

**키워드**: `#스칼라` `#0차원` `#괄호수` `#수학대응`

---

## 프레임워크 (2)

### 1.10 왜 프레임워크들은 다 "Tensor"/"Variable" 래퍼를 쓸까? 🏗

**요약**: 순수 ndarray엔 **"이 데이터가 어떤 연산에서 왔는지" 추적 기능이 없음**. 역전파/자동 미분을 위해 **메타정보를 붙일 그릇**이 필요 → 모든 주류 프레임워크가 래퍼 채택.

```python
# 순수 NumPy: 메타정보 추적 불가
x = np.array(2.0)
y = x ** 2
# y가 x로부터 어떻게 왔는지, 미분 어떻게 할지 정보가 없음

# Variable 래퍼: 메타정보 공간 있음
class Variable:
    def __init__(self, data):
        self.data = data      # 실제 데이터
        # 앞으로 추가될 메타정보:
        # self.grad = None    ← 미분 결과 (step07+)
        # self.creator = ...  ← 이 Variable을 만든 함수 (step07+)
        # self.generation = 0 ← 역전파 우선순위 (step16+)
```

- PyTorch `Tensor`, TF `Tensor`, JAX `Array`, Chainer `Variable`, DeZero `Variable` — 전부 같은 철학
- "데이터 + 계산 그래프 메타정보"를 함께 들고 다니는 것
- 이게 **Define-by-Run**(동적 계산 그래프)의 토대

**키워드**: `#래퍼패턴` `#메타정보` `#역전파` `#DefineByRun` `#자동미분`

---

### 1.11 `is_simple_core` 스위치는 왜 만들어졌을까? 🏗

**요약**: 책은 **학습 진도에 따라 같은 클래스의 다른 버전**을 보여줌. 초반(step01~22)은 단순 버전(`core_simple`), 후반(step33+)은 완전한 버전(`core`). `is_simple_core`는 어느 쪽을 import할지 선택하는 학습용 스위치.

```python
# rezero/__init__.py (향후 step23 쯤에 이런 식으로 만들 예정)
is_simple_core = False   # 학습 진도에 따라 True/False 토글

if is_simple_core:
    from rezero.core_simple import Variable, Function  # 단순 버전
else:
    from rezero.core import Variable, Function          # 완전 버전
```

- 실제 프로덕션 프레임워크엔 이런 스위치가 없음 (오직 완전 버전만 씀)
- 책만의 **교육적 장치** — 같은 인터페이스(Variable, Function)로 진화하는 모습을 보여주기 위해
- 브로는 step23 근처에서 rezero에 이 스위치를 직접 만들게 될 것

**키워드**: `#is_simple_core` `#학습용스위치` `#core_simple` `#교육장치`

---

## 비교 (1)

### 1.12 Python에서 `==` vs `is` 차이 🎯

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

**학습 완료일**: 2026-07-21
**총 주제 수**: 12개 (Python 기본 6, NumPy 3, 프레임워크 2, 비교 1)
**다음 step**: step02 (Function 도입) — 여기서 배운 `__call__`, `@staticmethod`가 바로 등장!

---

