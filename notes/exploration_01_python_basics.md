# 🧪 보충 탐구 #1 — Python 클래스 / NumPy / 프레임워크 기본기

> **step01 직후 보충 학습** (2026-07-21)
> step 진도 외에 파이썬/NumPy/프레임워크 등 깊이 파고 싶었던 주제들 정리.
> 형식: 핵심 요약 + 짧은 코드 예시. 자세한 건 키워드로 검색.

---

## 목차

- **A. Python 클래스 기본**
  - [A.1 `self`와 인스턴스 메서드](#a1-self와-인스턴스-메서드-)
  - [A.2 멤버 변수(속성) 용어와 접근 룩업 규칙](#a2-멤버-변수속성-용어와-접근-룩업-규칙)
  - [A.3 `__init__`과 dunder 메서드](#a3-__init__과-dunder-메서드)
  - [A.4 `class Foo:` vs `class Foo(object):`](#a4-class-foo-vs-class-fooobject)
  - [A.5 메서드 3종류: 인스턴스/클래스/스태틱](#a5-메서드-3종류-인스턴스클래스스태틱)
- **B. Python 캡슐화와 접근 제어**
  - [B.1 `public`/`protected`/`private` 관례](#b1-publicprotectedprivate-관례-)
  - [B.2 게터/세터와 `@property`](#b2-게터세터와-property)
- **C. Python 문법과 이디엄**
  - [C.1 데코레이터(`@`)](#c1-데코레이터-)
  - [C.2 f-string (포맷팅)](#c2-f-string-포맷팅)
  - [C.3 `==` vs `is`](#c3--vs-is)
  - [C.4 "primitive"와 박싱 — Python의 객체 철학](#c4-primitive와-박싱--python의-객체-철학)
  - [C.5 파이썬은 진짜 편한가?](#c5-파이썬은-진짜-편한가)
- **D. NumPy 기본**
  - [D.1 `ndarray` 내부 구조](#d1-ndarray-내부-구조)
  - [D.2 `shape` vs `size` vs `ndim`](#d2-shape-vs-size-vs-ndim)
  - [D.3 0차원 스칼라 — `np.array(1.0)`이 0차원인 이유](#d3-0차원-스칼라--nparray10이-0차원인-이유)
- **E. 프레임워크 디자인**
  - [E.1 왜 프레임워크들은 다 Variable/Tensor 래퍼를 쓸까](#e1-왜-프레임워크들은-다-variabletensor-래퍼를-쓸까)
  - [E.2 `is_simple_core` 학습용 스위치](#e2-is_simple_core-학습용-스위치)

---

## A. Python 클래스 기본

### A.1 `self`와 인스턴스 메서드 🐍

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

### A.2 멤버 변수(속성) 용어와 접근 룩업 규칙

#### A.2.1 용어 정리

파이썬은 **여러 용어가 혼용**됨. 공식 용어는 **attribute (속성)**.

```python
class Variable:
    count = 0                          # ① 클래스 속성 (class attribute)
                                       #   모든 인스턴스가 공유

    def __init__(self, data):
        self.data = data               # ② 인스턴스 속성 (instance attribute)
        self.grad = None               # ② 인스턴스 속성 — 인스턴스마다 따로
```

| 개념 | 파이썬 공식 용어 | 동의어/타 언어 |
|---|---|---|
| `self.x = ...` | **instance attribute** | field, member, instance variable |
| `x = ...` (클래스 바디) | **class attribute** | static variable, class variable |
| 포괄적 | **attribute** | member, field |

→ 가장 정확한 표현: **"attribute (속성)"**. "variable"은 관행적 표현.

#### A.2.2 인스턴스 메서드에서의 멤버 접근 룩업

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

#### A.2.3 핵심 케이스 — 클래스 변수와 인스턴스 변수 충돌 ⚠️

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

#### A.2.4 `__dict__` 로 내부 확인

```python
x = Variable(np.array(1.0))
print(x.__dict__)                      # {'data': array(1.0)} — 인스턴스 변수들
print(Variable.__dict__['count'])      # 0 — 클래스 변수
```

#### A.2.5 핵심 규칙 3가지

1. **읽을 때**: `self.x` → 인스턴스 → 클래스 순서로 찾음
2. **쓸 때 (할당)**: `self.x = ...` → **무조건 인스턴스 변수** (클래스 변수 아님)
3. **`self.` 없이**: 인스턴스 변수 접근 **불가능** (Java/C#과 반대)

**키워드**: `#attribute` `#속성` `#instancevariable` `#classvariable` `#룩업규칙` `#self필수` `#__dict__` `#네임스페이스` `#명시적self`

---

### A.3 `__init__`과 dunder 메서드

**요약**: `__init__`은 **dunder**(double underscore) 메서드. 파이썬이 특정 상황에 자동 호출하도록 예약된 "매직 메서드". `__init__`은 인스턴스 생성 직후 초기화 용도로 자동 호출됨.

```python
x = Variable(np.array(1.0))
# 내부적으로:
#   1. Variable.__new__(Variable) → 빈 인스턴스 생성
#   2. Variable.__init__(x, np.array(1.0)) → 초기화 자동 호출
```

#### A.3.1 주요 dunder 목록 (DeZero에서 자주 쓰임)

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

    def __call__(self, *args):      # x(args) — 인스턴스를 함수처럼 호출
        ...

x = Variable(np.array(2.0))
print(x)         # __repr__ 호출 → "Variable(data=2.0)"
print(x + 3)     # __add__ 호출 → 5.0
print(len(x))    # __len__ 호출
```

→ 책의 후반 step들에서 Variable에 dunder들이 점진적으로 추가됨:
- `__add__`/`__mul__`은 step20
- `__len__`/`__getitem__`은 step21
- `__call__`은 step02에서 Function이 사용! (검증됨, step02.py:10에 실제 있음)

**키워드**: `#dunder` `#매직메서드` `#__init__` `#__new__` `#__repr__` `#__add__` `#__call__` `#자동호출`

---

### A.4 `class Foo:` vs `class Foo(object):`

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

### A.5 메서드 3종류: 인스턴스/클래스/스태틱

**요약**: 3종 메서드는 **첫 인자가 뭘 받는가**가 핵심. DeZero 책 본문(steps/)은 **전부 인스턴스 메서드**로 구현되며, `@staticmethod`/`@classmethod`는 **한 번도 안 나옴** (검증 완료). `dezero/` 완성 프레임워크에만 일부 사용.

#### A.5.1 3종 비교

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

#### A.5.2 접근 권한 한눈에 보기

| 메서드 종류 | 첫 인자 | 접근 가능 | 비유 |
|---|---|---|---|
| 인스턴스 메서드 | `self` | 인스턴스 변수 + 클래스 변수 | "나(this)에 대해 물어봐" |
| 클래스 메서드 | `cls` | 클래스 변수만 | "우리 반(클래스)에 대해 물어봐" |
| 스태틱 메서드 | (없음) | 둘 다 접근 불가, 입력만 | "난 그냥 여기 붙어있는 함수야" |

#### A.5.3 classmethod vs staticmethod — 오버라이드 관점

**둘 다 오버라이드 가능**. 핵심 차이는 **`cls`가 자동 교체되는지**.

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

# Dog에서 호출 (Dog은 whoami/breathe 오버라이드 안 함)
print(Dog.whoami())      # "나는 Dog"  ← cls가 Dog로 자동 교체!
print(Dog.breathe())     # "숨 쉼"      ← 여전히 Animal 것 (클래스 정보 X)
```

#### A.5.4 classmethod가 빛나는 순간 — 팩토리 메서드

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

#### A.5.5 왜 스태틱 메서드를 쓰는가? — "논리적 소속감"

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

#### A.5.6 DeZero에서의 현실 (검증)

```bash
$ grep -E "@staticmethod|@classmethod" dezero/core.py dezero/core_simple.py
# (결과 없음 — 전부 인스턴스 메서드로 구현됨)

$ grep -rE "@staticmethod|@classmethod" steps/
# (결과 없음 — 책 본문에는 아예 안 나옴)

$ grep -rE "@staticmethod|@classmethod" dezero/
# dezero/models.py:103, dezero/datasets.py:120,180,230,248  ← 완성 프레임워크엔 5곳
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

**rezero 추천**: 책 스타일 그대로 (전부 인스턴스 메서드). 책 비교하며 읽기 좋고, 이해한 뒤 변형 실험은 언제든 가능.

**키워드**: `#인스턴스메서드` `#classmethod` `#staticmethod` `#self` `#cls` `#cls자동교체` `#팩토리메서드` `#논리적소속감` `#DeZero검증`

---

## B. Python 캡슐화와 접근 제어

### B.1 `public`/`protected`/`private` 관례

**요약**: **Python엔 진짜 접근 제어자가 없음**. 관례(밑줄 개수)로 표현. "consenting adults" (어른들의 합의) 원칙.

#### B.1.1 3단계 관례

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

#### B.1.2 동작 차이

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

#### B.1.3 "consenting adults" 원칙

Python 철학: "우리 모두 어른이니까, 밑줄 보고 알아서 하자". 강제하지 않고 관례에 맡김.

#### B.1.4 비교표 — Java/C# vs Python

| | Java/C# | Python |
|---|---|---|
| `public` | 문법적 키워드 | (밑줄 없음, 기본값) |
| `protected` | 문법적 키워드 | `_변수명` (밑줄 1개, 관례) |
| `private` | 문법적 키워드 | `__변수명` (밑줄 2개, 네임 맹글링) |
| 강제력 | 컴파일러가 강제 | 없음, 전적으로 관례 |
| 접근 방지 | 불가능 (리플렉션 제외) | 관례 안 지키면 접근 가능 |

#### B.1.5 rezero Variable에 적용?

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

### B.2 게터/세터와 `@property`

**요약**: 파이썬에도 게터/세터 있음. 하지만 철학이 다름 — **"처음엔 public으로 시작, 검증 필요해지면 그때 `@property`로 전환"**.

#### B.2.1 방식 1: 처음엔 그냥 public (가장 흔함)

```python
class Variable:
    def __init__(self, data):
        self.data = data               # 그냥 public

x = Variable(np.array(1.0))
print(x.data)                          # ✅ 직접 접근
x.data = np.array(2.0)                 # ✅ 직접 할당
```

→ Java/C#이면 `getData()`/`setData()` 만들겠지만, 파이썬은 이렇게 안 함.

#### B.2.2 방식 2: 검증/계산이 필요해지면 `@property` 도입

```python
class Variable:
    def __init__(self, data):
        self.data = data

    @property
    def shape(self):                   # ← getter 역할
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

# 사용:
x = Variable(np.array([[1, 2], [3, 4]]))
print(x.shape)                         # (2, 2) ← 메서드인데 () 없이!
print(x.ndim)                          # 2
# x.shape = (5, 5)                     # ❌ setter 없으면 AttributeError
```

→ `x.shape()` 아니고 `x.shape`. **마치 속성처럼 보이지만 실제론 메서드 호출**. 이게 `@property`의 마법.

#### B.2.3 방식 3: getter + setter 둘 다 (검증 필요시)

```python
class Variable:
    def __init__(self, data):
        self._data = data              # 내부적으론 _data

    @property
    def data(self):                    # getter
        return self._data

    @data.setter
    def data(self, value):             # setter — 검증/부작용 가능
        if not isinstance(value, np.ndarray):
            raise TypeError("data는 ndarray여야 함")
        self._data = value

# 사용:
x = Variable(np.array(1.0))
x.data = np.array(2.0)                 # ✅ setter 호출 (검증됨)
# x.data = "문자열"                    # ❌ TypeError
```

#### B.2.4 DeZero 실제 사용 (step19에서 등장, 검증 완료)

```python
# steps/step19.py의 Variable
class Variable:
    def __init__(self, data):
        self.data = data
        ...

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    @property
    def size(self):
        return self.data.size

    @property
    def dtype(self):
        return self.data.dtype
```

→ 전엔 `x.data.shape`로 접근했는데, 이제 `x.shape`로 바로 접근. Variable이 "ndarray 같은 느낌"으로 확장됨.

#### B.2.5 비교표

| 관점 | Java/C# | 파이썬 |
|---|---|---|
| 기본 접근 | private + getter/setter | public |
| 검증 필요시 | getter/setter 유지 | `@property`로 전환 |
| 문법 | `getData()` / `setData()` | `x.data` (속성처럼) |
| 철학 | "미리 막자" | "어른이니까 자유롭게, 필요시 막자" |

**키워드**: `#property` `#게터` `#세터` `#캡슐화` `#descriptor` `#Python철학`

---

## C. Python 문법과 이디엄

### C.1 데코레이터(`@`)

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

**키워드**: `#데코레이터` `#@staticmethod` `#@property` `#PEP318` `#설탕` `#Python24` `#학습서철학`

---

### C.2 f-string (포맷팅)

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

### C.3 `==` vs `is`

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

### C.4 "primitive"와 박싱 — Python의 객체 철학

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

### C.5 파이썬은 진짜 편한가?

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

---

## D. NumPy 기본

### D.1 `ndarray` 내부 구조

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

### D.2 `shape` vs `size` vs `ndim`

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

### D.3 0차원 스칼라 — `np.array(1.0)`이 0차원인 이유

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

## E. 프레임워크 디자인

### E.1 왜 프레임워크들은 다 Variable/Tensor 래퍼를 쓸까

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

### E.2 `is_simple_core` 학습용 스위치

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

**학습 완료일**: 2026-07-21
**총 주제 수**: 16개
- A. Python 클래스 기본: 5개 (self, 멤버변수/룩업, dunder, class 상속, 메서드 3종)
- B. 캡슐화: 2개 (접근권한, @property)
- C. 문법/이디엄: 5개 (데코레이터, f-string, == vs is, 박싱, 파이썬 철학)
- D. NumPy: 3개 (ndarray 내부, shape/size/ndim, 0차원)
- E. 프레임워크: 2개 (래퍼 패턴, is_simple_core)
