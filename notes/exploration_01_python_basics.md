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

#### 💡 1.1 보충: 멤버 변수 용어 + 접근 룩업 규칙 (질문에서 파생)

##### A. 파이썬 멤버 변수 용어 정리

파이썬은 **여러 용어가 혼용**됨. 공식 용어는 **attribute (속성)**.

```python
class Variable:
    count = 0                          # ① 클래스 변수 (class variable / class attribute)
                                       #   모든 인스턴스가 공유

    def __init__(self, data):
        self.data = data               # ② 인스턴스 변수 (instance variable / instance attribute)
        self.grad = None               # ② 인스턴스 변수 — 인스턴스마다 따로
```

| 개념 | 파이썬 공식 용어 | 동의어/타 언어 |
|---|---|---|
| `self.x = ...` | **instance attribute** | field, member, instance variable |
| `x = ...` (클래스 바디) | **class attribute** | static variable, class variable |
| 포괄적 | **attribute** | member, field |

→ 가장 정확한 표현: **"attribute (속성)"**. "variable"은 관행적 표현.

##### B. 인스턴스 메서드에서의 멤버 접근 룩업 규칙

**파이썬은 Java/C#과 달리 `self.` 없이 인스턴스 변수 접근 불가능**. 이게 가장 큰 차이.

```python
# Java/C# — 암묵적 this (생략 가능)
class Foo {
    int data;
    void show() {
        System.out.println(data);      // ← this. 생략 OK
    }
}

# Python — 명시적 self (생략 불가)
class Foo:
    def __init__(self):
        self.data = 0

    def show(self):
        print(self.data)               # ✅ self. 필수
        # print(data)                  # ❌ NameError
```

**읽을 때 룩업 순서** (`self.x`를 읽으면):
```
1. self.__dict__ (인스턴스 고유 변수)에서 'x' 찾기
2. 없으면 type(self) (클래스)에서 'x' 찾기 → 클래스 변수
3. 없으면 부모 클래스로 올라감 (MRO 순서)
4. 없으면 AttributeError
```

**할당할 때** (`self.x = ...`):
- **무조건 인스턴스 변수** 생성/수정 (클래스 변수 수정 아님!)

##### C. 핵심 케이스 — 클래스 변수와 인스턴스 변수 충돌 ⚠️

```python
class Variable:
    count = 0                          # 클래스 변수

    def __init__(self):
        self.count = 100               # ⚠️ 인스턴스 변수가 클래스 변수를 가림!

x = Variable()
print(x.count)                         # 100 (인스턴스 변수)
print(Variable.count)                  # 0   (클래스 변수 — 안 바뀜)
```

→ `self.count = 100`은 인스턴스 변수를 새로 만드는 것. 클래스 변수 안 건드림. 진짜 함정.

##### D. `__dict__` 로 확인

```python
x = Variable(np.array(1.0))
print(x.__dict__)                      # {'data': array(1.0)} — 인스턴스 변수들
print(Variable.__dict__['count'])      # 0 — 클래스 변수
```

##### E. 핵심 규칙 3가지

1. **읽을 때**: `self.x` → 인스턴스 → 클래스 순서로 찾음
2. **쓸 때 (할당)**: `self.x = ...` → **무조건 인스턴스 변수** (클래스 변수 아님)
3. **`self.` 없이**: 인스턴스 변수 접근 **불가능** (Java/C#과 반대)

##### F. DeZero 예시

```python
# 미래의 Variable (step07+ 예고)
class Variable:
    def __init__(self, data):
        self.data = data               # 인스턴스 변수
        self.grad = None               # 인스턴스 변수
        self.creator = None            # 인스턴스 변수
        self.generation = 0            # 인스턴스 변수

    def backward(self):
        # 전부 self. 접두어 필수!
        ...

# 클래스 변수 사용 예 (안 가르쳐주지만 실제 프레임워크에선 자주 씀)
class Variable:
    _global_count = 0                  # 클래스 변수: 인스턴스 생성 추적용
    def __init__(self, data):
        self.data = data
        Variable._global_count += 1    # ClassName.attr 로 접근 (명확)
```

**키워드**: `#attribute` `#속성` `#instancevariable` `#classvariable` `#룩업규칙` `#self필수` `#__dict__` `#네임스페이스` `#명시적self`

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

#### 💡 1.4 보충 2: f-string vs JS 템플릿 리터럴 + 정렬 기호 (질문에서 파생)

**브로 질문**: "f문자열은 JS의 템플레이티드 스트링 따라온 건가? `>`는 우측 정렬?"

**요약**: 둘 다 정확히 맞음. JS 템플릿 리터럴(ES6/2015)이 1년 먼저 도입, Python f-string(3.6/2016)이 형태만 약간 바꿔 따라옴.

**비교표**:
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

**정렬 기호** (`{값:정렬기호폽}` 형식):
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

→ 브로가 `inspect()`에서 쓴 `{label:>10}` = "label을 폭 10에 우측 정렬"

**키워드**: `#f-string` `#JS템플릿리터럴` `#ES6` `#정렬` `#폭지정` `#포맷팅`

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

#### 💡 1.5 보충 2: 3종 메서드 — "무엇에 접근할 수 있는가" (질문에서 파생)

**브로 질문**: "둘 다 인스턴스 레퍼런스는 받지 않는데, 한 놈은 클래스 자체에 대한 참조를 받는다?"

→ **정확한 통찰**. 이걸 "접근 권한" 관점으로 명확히 정리.

**3종 메서드 비교**:
```python
class MyClass:
    name = "MyClass"      # 클래스 변수 (인스턴스가 공유)

    def __init__(self, data):
        self.data = data  # 인스턴스 변수 (각자 따로)

    # 1. 인스턴스 메서드 (기본) - self로 인스턴스 참조
    def instance_method(self):
        return f"data={self.data}, name={self.name}"   # 둘 다 접근 OK

    # 2. 클래스 메서드 - cls로 클래스 참조
    @classmethod
    def class_method(cls):
        return f"name={cls.name}"
        # cls.name OK, 하지만 cls.data는 의미 없음 (어느 인스턴스?)

    # 3. 스태틱 메서드 - 아무 참조도 안 받음
    @staticmethod
    def static_method(data):
        return isinstance(data, int)
        # self/cls 불가, 입력(data)만으로 일함
```

**접근 권한 한눈에 보기**:

| 메서드 종류 | 첫 인자 | 접근 가능 | 비유 |
|---|---|---|---|
| 인스턴스 메서드 | `self` | 인스턴스 변수 + 클래스 변수 | "나(this)에 대해 물어봐" |
| 클래스 메서드 | `cls` | 클래스 변수만 | "우리 반(클래스)에 대해 물어봐" |
| 스태틱 메서드 | (없음) | 둘 다 접근 불가, 입력만 | "난 그냥 여기 붙어있는 함수야" |

**왜 스태틱 메서드를 쓰는가?** — "논리적 소속감" 때문
```python
# 스태틱 안 쓰면 (모듈 함수):
def is_valid_variable_data(data): ...      # ❌ 어디 소속인지 모호
is_valid_variable_data(some_data)

# 스태틱으로 클래스에 넣으면:
class Variable:
    @staticmethod
    def is_valid_data(data): ...           # ✅ "Variable 관련 검사" 명확
Variable.is_valid_data(some_data)
```

→ 실제 동작은 일반 함수와 동일. "Variable과 관련 있다"는 것을 코드로 표현.

**DeZero 실례** (앞으로 step02+에서 등장 예정):
```python
class Function:
    def __call__(self, input):     # 인스턴스 메서드 (self로 상태 관리)
        x = input.data
        y = self.forward(x)        # forward 호출
        ...

    @staticmethod
    def forward(x):                # 스태틱 (self/cls 불필요, 순수 변환)
        return x ** 2              # Square에서 오버라이드
```

→ Function은 forward를 "입력 → 출력의 순수 변환"으로 모델링했기 때문에 스태틱 사용.

**키워드**: `#3종메서드` `#접근권한` `#self` `#cls` `#논리적소속감` `#순수함수`

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

### 1.13 데코레이터(`@`) — 왜 DeZero 책엔 `@staticmethod`가 없을까? 🐍

**브로 질문**: "책 속 코드에 `@staticmethod` 안 나와. 설마 파이썬에 없었나? 일부러 뺀 건가?"

**요약**: **3가지 다 맞음**. `@staticmethod`는 **데코레이터**. DeZero 책이 안 쓴 건 (a) 코드 단순화, (b) 학습 곡선 완화, (c) 동작 차이 없기 때문.

#### 데코레이터란?

`@`로 시작하는 것들. "함수를 인자로 받아 새로운 함수를 반환하는 함수"를 간결하게 적용하는 문법. PEP 318 (2004년, Python 2.4)에서 도입.

```python
@staticmethod
def forward(x):
    return x ** 2

# 위는 아래의 설탕(syntactic sugar) — 의미 동일
def forward(x):
    return x ** 2
forward = staticmethod(forward)
```

#### DeZero 원본 확인 (브로가 발견한 것 검증)

```bash
$ grep -E "@staticmethod|@classmethod" dezero/core.py dezero/core_simple.py
# (결과 없음 — 전부 인스턴스 메서드로 구현됨)
```

원본 `steps/step02.py`의 Function:
```python
class Function:
    def __call__(self, input):       # 인스턴스 메서드 (self 받음)
        x = input.data
        y = self.forward(x)
        ...

    def forward(self, in_data):      # 인스턴스 메서드 (self 받음)
        raise NotImplementedError()

class Square(Function):
    def forward(self, x):            # 인스턴스 메서드로 오버라이드
        return x ** 2
```

#### 왜 책이 안 썼을까?

| 이유 | 설명 |
|---|---|
| **A. 코드 단순화** | 학습서 목적상 "Function 구조"가 핵심이지 "데코레이터 활용"이 아님 |
| **B. 학습 곡선** | 데코레이터는 "함수를 인자로 받는 함수" 개념 필요. 초중급에게 가파름 |
| **C. 동작 차이 없음** | `forward(self, x)`나 `@staticmethod forward(x)`나 결과 동일 |

#### rezero는?

**추천: 책 스타일 그대로 (전부 인스턴스 메서드)**. 책 비교하며 읽기 좋고, 이해한 뒤 변형 실험은 언제든 가능.

```python
# 책 스타일 (rezero 추천)
class Function:
    def forward(self, x): ...     # self 받음

# 현대 Pythonic 스타일 (변형 실험용)
class Function:
    @staticmethod
    def forward(x): ...           # self 안 받음, 순수 함수
```

**키워드**: `#데코레이터` `#@staticmethod` `#PEP318` `#설탕` `#Python24` `#학습서철학`

---

### 1.14 Python의 접근 권한 — public/protected/private 🐍

**브로 질문**: "파이썬에서 멤버 액세스 접근 권한 제어도 하낙? public/protected/private?"

**요약**: **Python엔 진짜 접근 제어자가 없음**. 관례(밑줄 개수)로 표현. "consenting adults" (어른들의 합의) 원칙.

#### 3단계 관례

```python
class MyClass:
    def __init__(self):
        self.public_var = "누구나 접근 OK"              # public
        self._protected_var = "살짝 숨김 (관례)"          # protected
        self.__private_var = "이름으로 숨김 (맹글링)"     # private

    def public_method(self): ...                        # public
    def _protected_method(self): ...                    # protected
    def __private_method(self): ...                     # private
```

#### 동작 차이

```python
obj = MyClass()

# 1. public — 막 접근 가능
print(obj.public_var)         # ✅ OK

# 2. protected (밑줄 1개) — "관례상" 접근 자제, 문법적 강제 없음
print(obj._protected_var)     # ✅ 동작은 함 (경고 없음)
                              # "이건 내부용이야"라는 암묵적 합의

# 3. private (밑줄 2개) — 실제로 이름이 변조됨 (네임 맹글링)
print(obj.__private_var)      # ❌ AttributeError
print(obj._MyClass__private_var)  # ✅ 이렇게는 접근 가능 (비권장)
```

#### "consenting adults" 원칙

Python 철학: "우리 모두 어른이니까, 밑줄 보고 알아서 하자". 강제하지 않고 관례에 맡김.

```python
# Java/C#처럼 캡슐화 강제 안 됨
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance     # private 시도 (네임 맹글링)

account = BankAccount(1000)
# account.__balance = 9999999999    # 의도: 막아야 함
# 실제: _BankAccount__balance로 접근 우회 가능 (관례만 지킬 뿐)
```

#### 비교표 — Java/C# vs Python

| | Java/C# | Python |
|---|---|---|
| `public` | 문법적 키워드 | (밑줄 없음, 기본값) |
| `protected` | 문법적 키워드 | `_변수명` (밑줄 1개, 관례) |
| `private` | 문법적 키워드 | `__변수명` (밑줄 2개, 네임 맹글링) |
| 강제력 | 컴파일러가 강제 | 없음, 전적으로 관례 |
| 접근 방지 | 불가능 (리플렉션 제외) | 관례 안 지키면 접근 가능 |

#### rezero Variable에 적용?

지금은 전부 public:
```python
class Variable:
    def __init__(self, data):
        self.data = data       # public
```

책도 이대로 가. PyTorch 실제 구현은 `_data`, `__grad` 등으로 내부 변수 관리하지만,
학습 단계에선 public이 읽기 편함. 나중에 (step16+ 메모리 관리 쯤) `_` 관례 시도해볼 수 있음.

**키워드**: `#접근권한` `#public` `#protected` `#private` `#네임맹글링` `#consentingadults` `#관례`

---

**학습 완료일**: 2026-07-21
**총 주제 수**: 14개 (Python 기본 8, NumPy 3, 프레임워크 2, 비교 1)
**다음 step**: step02 (Function 도입) — 여기서 배운 `__call__`, `@staticmethod`가 바로 등장!

---

