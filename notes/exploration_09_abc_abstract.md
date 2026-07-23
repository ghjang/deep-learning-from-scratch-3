# 🧪 탐구 노트 #9 — Python 추상 클래스: `abc.ABC` vs `raise NotImplementedError()`

> **시점**: step02 직후 (Function 클래스의 추상 메서드 구현 방식에서 출발), step03에서 `@override`까지 확장
> **동기**: step02에서 `forward()`를 추상 메서드로 만들 때 `raise NotImplementedError()`를 썼다. "더 깔끔한 공식 방법(`abc.ABC`)이 있다"는 언급이 나와서, 둘의 차이와 선택 기준을 깊이 파봄. step03에서 `@override` 데코레이터를 추가 도입하며, abc와의 강제력 차이를 §8에서 다룸.

---

## 📋 목차

1. [TL;DR — 한 줄 요약](#tldr)
2. [도입: 왜 "추상 메서드"가 필요한가?](#도입)
3. [`raise NotImplementedError()` — 파이썬 전통 관용구](#notimpl)
4. [`abc.ABC` + `@abstractmethod` — 공식 추상 클래스](#abc)
5. [★ 우리 step02 코드를 둘로 비교](#비교)
6. [왜 DeZero(책)는 `NotImplementedError`를 택했나?](#선택이유)
7. [실전: 다른 라이브러리는 어떻게 하나?](#실전)
8. [심화: `@abstractmethod`는 어떻게 작동하나? (메타클래스)](#심화)
9. [보너스: `@override` 데코레이터 (Python 3.12+) — abc와 짝을 이루는 친구](#override)
10. [요약 / 결론](#결론)

---

<a id="tldr"></a>
## 🎯 TL;DR

| 항목 | `raise NotImplementedError()` | `abc.ABC` + `@abstractmethod` |
|---|---|---|
| **종류** | 파이썬 전통적 **관용구** (runtime check) | 표준 라이브러리 **공식 기능** (instantiation check) |
| **에러 시점** | **호출할 때** (runtime) | **인스턴스 생성할 때** (instantiation) |
| **코드 길이** | 1줄 | 데코레이터 + import 2줄 |
| **강제력** | 약함 (자식이 안 덮어써도 객체는 만들어짐) | 강함 (자식이 안 덮어쓰면 인스턴스 생성 자체가 에러) |
| **교육용** | 직관적, 본질 한눈에 | 기능적으론 더 정확하나 장치가 숨어있음 |

**결론**: DeZero(책)는 학습 명확성을 위해 `NotImplementedError` 택. 실전 코드/라이브러리에선 보통 `abc` 사용.

---

<a id="도입"></a>
## 1. 도입: 왜 "추상 메서드"가 필요한가?

step02의 `Function` 클래스를 보자.

```python
class Function:
    def __call__(self, input_var):
        x = input_var.data
        y = self.forward(x)          # 자식이 반드시 구현해야 하는 메서드
        return Variable(y)

    def forward(self, x):
        ???  # ← 여기에 뭘 써야 할까?
```

**핵심 고민**: `Function` 자체는 "추상적인 개념"이지, 실제로 계산을 수행하는 구체 클래스가 아니다. 제곱을 할지(`Square`), 지수함수를 할지(`Exp`), 행렬곱을 할지(`MatMul`)는 자식이 정할 일. 즉 **`forward`의 본문은 "자식이 채워야 할 빈 칸"**이다.

이런 "자식이 반드시 구현해야 하는 메서드"를 **추상 메서드(abstract method)** 라고 부른다. 파이썬에선 이걸 표현하는 두 가지 방법이 있다.

---

<a id="notimpl"></a>
## 2. `raise NotImplementedError()` — 파이썬 전통 관용구

가장 단순한 방법: 본문에서 예외를 던진다.

```python
class Function:
    def forward(self, x):
        raise NotImplementedError()
```

### 작동 원리

- 자식이 `forward`를 **안 덮어쓰면** → 부모의 메서드 그대로 상속 → 호출 시점에 `NotImplementedError` 발생
- 자식이 `forward`를 **덮어쓰면** → 자식 메서드가 호출 → 정상 동작

### 특징

✅ **장점**
- 코드가 직관적. "아직 구현 안 됨"이라는 의미가 한눈에
- 별도 import 없음
- 교육적 — 의도가 명확히 드러남

❌ **단점**
- **에러가 늦게 터짐**. 인스턴스 생성은 성공하고, 막상 `forward()`를 호출할 때야 에러
- 인터페이스를 "강제"하는 게 아님 — 실수로 빼먹어도 객체는 만들어짐

```python
# NotImplementedError의 한계 예시
f = Function()          # ← 이 시점엔 아무 에러 안 남 (정상적으로 객체 생성됨)
f.forward(10)           # ← 이제야 NotImplementedError 발생
```

"설계 오류"를 **가능한 한 빨리** 잡고 싶으면 부족함.

---

<a id="abc"></a>
## 3. `abc.ABC` + `@abstractmethod` — 공식 추상 클래스

파이썬 표준 라이브러리 [`abc`](https://docs.python.org/3/library/abc.html) (Abstract Base Class) 모듈이 제공하는 공식 방법.

```python
from abc import ABC, abstractmethod

class Function(ABC):                    # ← ABC 상속
    def __call__(self, input_var):
        x = input_var.data
        y = self.forward(x)
        return Variable(y)

    @abstractmethod                     # ← 데코레이터로 추상 메서드 표시
    def forward(self, x):
        pass                            # 본문은 보통 pass (어차피 자식이 구현)
```

### 작동 원리

- `ABC`를 상속한 클래스는 **"추상 메서드가 하나라도 있으면 인스턴스화 불가"**
- 자식이 모든 추상 메서드를 구현해야 비로소 인스턴스 생성 가능

### 특징

✅ **장점**
- **에러가 빨리 터짐** — 인스턴스 생성 시점에 바로 검사
- 인터페이스 강제력이 강함 (실수 방지)
- 타입 힌트/IDE 지원과 잘 맞음 (pyright, mypy 등이 추상 메서드로 인식)

❌ **단점**
- `import` 한 줄 추가 + 데코레이터 한 줄 추가 (장황함 증가)
- 메커니즘이 눈에 안 보임 (메타클래스 기반 — §8 참조)
- 초보자에겐 "이게 왜 저렇게 작동하지?" 혼란 가능

```python
# abc의 강제력 예시
f = Function()
# TypeError: Can't instantiate abstract class Function
# with abstract method forward
# ← 인스턴스 생성 자체가 거부됨. forward 호출하기도 전에!
```

---

<a id="비교"></a>
## 4. ★ 우리 step02 코드를 둘로 비교

현재 `rezero/steps/step02.py`에 있는 코드 (NotImplementedError 방식):

```python
import numpy as np


class Variable:
    def __init__(self, data):
        self.data = data


class Function:
    def __call__(self, input_var):
        x = input_var.data
        y = self.forward(x)
        output = Variable(y)
        return output

    def forward(self, in_data):
        raise NotImplementedError()         # ← 여기


class Square(Function):
    def forward(self, x):
        return x ** 2


x = Variable(np.array(10))
y = Square()(x)
print(y.data)   # 100
```

**만약 `abc.ABC`를 적용한다면?** (★ 이렇게 바뀜 — diff 포인트만 찝어줌):

```python
import numpy as np
from abc import ABC, abstractmethod          # ← 추가: abc 모듈 임포트


class Variable:
    def __init__(self, data):
        self.data = data


class Function(ABC):                         # ← 변경: ABC 상속
    def __call__(self, input_var):
        x = input_var.data
        y = self.forward(x)
        output = Variable(y)
        return output

    @abstractmethod                          # ← 추가: 데코레이터
    def forward(self, in_data):
        pass                                 # ← 변경: raise → pass (본문이 의미 없음)


class Square(Function):
    def forward(self, x):
        return x ** 2


x = Variable(np.array(10))
y = Square()(x)
print(y.data)   # 100
```

### 🔍 변경 포인트 3곳 요약

| 위치 | 변경 전 | 변경 후 | 효과 |
|---|---|---|---|
| `import` | (없음) | `from abc import ABC, abstractmethod` | 모듈 임포트 |
| `class Function:` | (그냥 클래스) | `class Function(ABC):` | 추상 클래스로 선언 |
| `def forward` | `raise NotImplementedError()` | `@abstractmethod` + `pass` | 추상 메서드로 명시 |

### 💡 바뀐 결과 — 에러 시점이 달라진다!

**`NotImplementedError` 방식** (현재 코드):
```python
>>> f = Function()        # ✅ 객체 생성 성공 (에러 없음)
>>> f.forward(10)         # ❌ 여기서야 NotImplementedError
```

**`abc.ABC` 방식** (대안):
```python
>>> f = Function()
# ❌ TypeError: Can't instantiate abstract class Function
#    with abstract method forward
# → forward 호출은커녕 객체 생성부터 거부!
```

→ **"설계 오류를 조기에 잡는다"**는 게 핵심 차이.

---

<a id="선택이유"></a>
## 5. 왜 DeZero(책)는 `NotImplementedError`를 택했나?

브로 통찰이 핵심: **"이건 파이썬 책이 아니라 딥러닝 프레임워크 책이니까"**.

구체적 이유 추측:

1. **교육적 명확성** — `raise NotImplementedError()`는 "아직 구현 안 했다"는 의미가 직관적으로 드러남. `@abstractmethod`는 장치(데코레이터, 메타클래스)가 숨어 있어 "왜 이게 추상 메서드지?" 한 번 더 생각해야 함.

2. **본질 우선, 장치 최소** — step02의 본질은 "Template Method 패턴으로 관심사 분리". 추상 메서드 구현 디테일은 부차적. 추가 장치(`import`, 데코레이터)가 본질 흐름을 가리지 않게.

3. **코드 길이** — 학습 예제는 짧을수록 좋음. `abc`는 2줄이 더 들어감.

4. **점진적 복잡도** — 책은 step01→60으로 점진 복잡도를 설계. `abc` 같은 "부가 기능"은 나중에도 언제든 추가 가능. step02 단계에선 최소 장치로 핵심 개념(추상 메서드의 존재)만 전달.

> 💡 이건 디자인 철학과도 연결 — **"가장 간단한 것으로 본질을 전달한다"**. (PEP 20 Zen of Python: *Simple is better than complex.*)

---

<a id="실전"></a>
## 6. 실전: 다른 라이브러리는 어떻게 하나?

### PyTorch `torch.nn.Module`

```python
import torch.nn as nn

class MyModel(nn.Module):
    def forward(self, x):           # forward는 추상 메서드 아님 (NotImplementedError도 안 쓰는 특이 케이스)
        return x @ self.weight

# forward를 안 정의해도 에러 안 남 → 호출할 때 "미구현" AttributeError 발생
```

PyTorch는 `forward`를 강제 안 함. 관례(convention)로만 작동. DeZero보다 더 느슨한 접근.

### Django `BaseCommand`

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):    # Django는 NotImplementedError 방식
        ...
```

`handle`은 부모에서 `raise NotImplementedError`. DeZero와 동일한 접근.

### 표준 라이브러리 `collections.abc`

```python
from collections.abc import Mapping

class MyDict(Mapping):                     # abc 방식
    def __getitem__(self, key): ...
    def __iter__(self): ...
    def __len__(self): ...
# 이 3개 다 구현 안 하면 인스턴스 생성 안 됨
```

파이썬 자체는 "인터페이스 강제"가 필요한 곳엔 `abc`를 적극 사용.

### 관찰

- **프레임워크/교육용** 코드: `NotImplementedError` 잦음 (단순/직관)
- **라이브러리/인터페이스 정의**: `abc` 잦음 (강제력 중요)
- DeZero는 "프레임워크를 만드는 과정을 가르치는 책"이니 전자에 가까움

---

<a id="심화"></a>
## 7. 심화: `@abstractmethod`는 어떻게 작동하나? (메타클래스)

> 이 섹션은 흥미 위주. 이해 안 가도 스킵 OK.

`@abstractmethod`가 왜 "인스턴스 생성을 막는" 강제력을 가질까? 비밀은 **메타클래스(metaclass)** 에 있다.

```python
# ABC의 실제 정의 (단순화)
class ABCMeta(type):                        # type을 상속한 메타클래스
    def __call__(cls, *args, **kwargs):     # 인스턴스 생성(__new__ 전)에 끼어듦
        if getattr(cls, '__abstractmethods__', frozenset()):
            raise TypeError(
                f"Can't instantiate abstract class {cls.__name__} "
                f"with abstract methods {', '.join(cls.__abstractmethods__)}"
            )
        return super().__call__(*args, **kwargs)


class ABC(metaclass=ABCMeta):               # ABC가 이 메타클래스를 사용
    pass
```

**흐름**:
1. `@abstractmethod`가 붙은 메서드는 `__isabstractmethod__ = True` 속성을 가짐
2. `ABCMeta`가 클래스 생성 시 `__abstractmethods__`를 자동 수집 (자식에서 구현되면 제거)
3. `ABCMeta.__call__`이 인스턴스 생성 시점에 `__abstractmethods__`가 비어있는지 검사
4. 하나라도 남아있으면 `TypeError`

→ 즉 `abc`의 강제력은 **객체 지향의 일반적인 상속 메커니즘이 아니라, 메타클래스가 끼어들어서 만든 "규칙"**. 그래서 좀 "매직"스러움. (초보자에겐 이 숨은 장치가 혼란의 원인)

자세한 건 [Python 데이터 모델 공식 문서](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation) 참조.

---

<a id="override"></a>
## 9. 보너스: `@override` 데코레이터 (Python 3.12+) — abc와 짝을 이루는 친구

> step03에서 `@override`를 도입하면서 자연스럽게 부딪힌 주제.
> `abc`와 함께 쓰면 "추상 메서드 정의 + 자식에서 재정의 명시"의 짝꿍이 되지만,
> **강제력은 완전히 다르다**.

### 📖 `@override`란?

[PEP 698](https://peps.python.org/pep-0698/) (Python 3.12+)에서 추가. 부모 클래스에 있는 메서드를 **재정의(override)** 한다는 것을 명시적으로 표시.

```python
from typing import override

class Square(Function):
    @override                              # ← "부모의 forward를 재정의하는 거야"
    def forward(self, x):
        return x ** 2
```

### 🎯 C++/Java 배경 — 익숙한 개념

브로가 C++을 했다면 익숙:

| 언어 | override 표시 | 강제력 |
|---|---|---|
| **C++** | `virtual`, `override` 지정자 | 컴파일러 경고 |
| **Java** | `@Override` 애노테이션 | IDE 적극 권장 (컴파일 에러 가능) |
| **C#** | `override` 키워드 | 강제 |
| **파이썬 (3.12+)** | `@override` 데코레이터 | **런타임엔 없음** (정적 분석 도구 필요) |
| **파이썬 (전통)** | (없음) | (관행 없음) |

### 🔑 핵심 — `@override` vs `@abstractmethod` 강제력 차이

이게 **가장 중요한 통찰**. 둘 다 데코레이터지만 **강제력이 완전히 다름**.

| 데코레이터 | 목적 | 런타임 강제 | 정적 분석 필요 | 비고 |
|---|---|---|---|---|
| `@abstractmethod` | "자식이 반드시 구현해야 함" | ✅ **강제** | ❌ | Python 인터프리터 자체가 인스턴스 생성 거부 |
| `@override` | "부모에 있는 거 재정의함" | ❌ **없음** | ✅ mypy/pyright 필수 | 런타임엔 조용히 통과 |

### 🧪 직접 검증 (step03 학습 중 실험)

```python
from abc import ABC, abstractmethod
from typing import override

# --- 실험 1: @override는 런타임엔 강제력 없음 ---
class Base:
    def hello(self): pass

class Bad(Base):
    @override
    def typo_method(self):     # ← 부모에 없는 이름인데 @override 붙임
        pass

Bad()                          # ✅ 조용히 성공 (Python 인터프리터는 못 잡음)
# → mypy/pyright를 돌려야 "typo_method는 부모에 없다"며 에러로 잡아줌

# --- 실험 2: @abstractmethod는 런타임에도 강제 ---
class Function(ABC):
    @abstractmethod
    def forward(self, x): pass

class IncompleteSub(Function):
    pass   # forward 안 구현

IncompleteSub()
# ❌ TypeError: Can't instantiate abstract class IncompleteSub
#    without an implementation for abstract method 'forward'
```

### 💡 왜 `@override`는 런타임 강제력이 없나?

`@override`는 **타입 체커(mypy, pyright, pyright 등)를 위한 힌트**로 설계됨. Python은 **동적 타이핑 언어**라, 런타임에 부모 클래스의 모든 메서드를 조사하긴 너무 비싸고 파이썬 철학(런타임 비용 최소)에 안 맞음.

→ 정적 분석 도구 없이 `@override`만 쓰면 **장식용**에 그침. 하지만 IDE(PyCharm, VS Code의 Pylance)에선 자동 검사해주니, 현업에선 실질적 효과 있음.

### 🤔 그럼 왜 쓰는가? — 오타/실수 방지

```python
class Square(Function):
    @override
    def forwrad(self, x):       # ← 오타! (forward → forwrad)
        return x ** 2
# (런타임엔 조용함)
# mypy/pyright: "forwrad는 부모에 없는데 @override 붙임 → 진짜 재정의 맞음?" → 에러로 잡아줌!
```

이게 `@override`의 진짜 가치. **"내가 진짜 부모 거 재정의하려는 거 맞아?" 자동 검증**.

### 📊 abc + @override 함께 쓰는 이상적인 조합

```python
from abc import ABC, abstractmethod
from typing import override

class Function(ABC):
    @abstractmethod                # 부모: "이거 자식이 무조건 구현해야 해" (강제)
    def forward(self, x):
        pass

class Square(Function):
    @override                      # 자식: "이거 부모 거 재정의하는 거야" (명시)
    def forward(self, x):
        return x ** 2
```

- 부모에 `@abstractmethod`: **"구현 강제"** (런타임 보장)
- 자식에 `@override`: **"재정의 명시"** (정적 분석으로 검증)
- 둘이 함께 쓰면 **안전망 이중화** — abc가 런타임 방어, override가 정적 분석 방어.

### 🎯 DeZero/rezero에서의 입장

- **책 원본 (steps/*.py)**: 둘 다 안 씀. 가장 단순한 형태 (`raise NotImplementedError()`)
- **step02 학습 시**: `NotImplementedError` 유지 (책 충실성)
- **step03 학습 시**: 브로 선택 → **abc + @override 도입 실험** ✅
  - "abc와 override의 강제력 차이"를 직접 체감하기 위한 변형. 학습 목적으론 훌륭한 실험.
- **`rezero/core.py` (향후)**: 정적 분석 도구 설정(pyproject.toml에 mypy/pyright)이 전제되면 `@override` 의미 있음. 없으면 장식용이라 선택적.

### 🔗 관련 링크

- [PEP 698: Override Decorator](https://peps.python.org/pep-0698/)
- [Python 공식: typing.override](https://docs.python.org/3/library/typing.html#typing.override)
- [mypy: override 지원](https://mypy.readthedocs.io/en/stable/error_code-list.html)

---

<a id="결론"></a>
## 10. 요약 / 결론

### 핵심 한 줄
> **`NotImplementedError`는 "관례"**, **`abc.ABC`는 "장치"**. 같은 목적(추상 메서드 표현)이지만, 강제력과 에러 시점이 다르다.

### 선택 가이드

| 상황 | 추천 |
|---|---|
| 학습 예제 / 프로토타입 | `raise NotImplementedError()` — 단순 명확 |
| 본질 흐름에 집중해야 할 때 | `raise NotImplementedError()` — 장치 최소 |
| 공개 라이브러리 / 인터페이스 정의 | `abc.ABC` — 강제력 중요 |
| 타입 힌트/IDE 지원이 중요 | `abc.ABC` — 도구가 잘 인식 |
| 여러 협업자가 구현해야 할 때 | `abc.ABC` — 빼먹으면 바로 에러 |

### DeZero/rezero에서의 입장

- **step별 학습 스크립트** (`rezero/steps/*.py`): 책 원본 방식(`NotImplementedError`) 유지. 학습 충실성 우선.
- **`rezero/core.py` (향후 프레임워크 코드)**: 브로 선택. 둘 다 합리적. (의견: 점진 복잡도를 고려하면 step09+에서 도입도 자연스러움)

### 🔗 관련 링크

- [Python 공식: abc 모듈](https://docs.python.org/3/library/abc.html)
- [PEP 3119: Abstract Base Classes](https://peps.python.org/pep-3119/)
- 🎨 [notes/design_patterns.md](./design_patterns.md) §2 Template Method — 본 탐구의 모태
- step02 노트 — 본 탐구의 출발점

**키워드**: `#abc` `#ABC` `#abstractmethod` `#추상클래스` `#추상메서드` `#abstract` `#NotImplementedError` `#메타클래스` `#ABCMeta` `#TemplateMethod` `#파이썬표준라이브러리` `#PEP3119` `#에러시점` `#강제력` `#교육명확성`
