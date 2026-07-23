# 🎨 디자인 패턴 노트 — DeZero에 등장하는 패턴들

> DeZero(및 `rezero`) 구현에 등장하는 **소프트웨어 디자인 패턴**을 정리하는 누적형 레퍼런스.
> step 진행 중 패턴이 발견될 때마다 이 파일에 추가/업데이트.
>
> - 일반적인 패턴 설명 (GoF 23패턴 등 표준 정의)
> - DeZero/rezero의 **어느 부분**에 등장하는지 (step별 위치)
> - 코드 스니펫은 최소, 핵심 구조만

---

## 📋 인덱스

| # | 패턴 | 최초 등장 | 분류 |
|---|---|---|---|
| 1 | Wrapper (래퍼 / 박싱) | step01 | 구조 (GoF: Decorator/Adapter 근원) |
| 2 | Template Method | step02 | 행동 (GoF) |

> 📖 하단에 [용어집(Glossary)](#📖-용어집-glossary--번역이-어색한-oop패턴-용어-모음) 섹션 있음 — 한국어 OOP/패턴 용어 중 원어 모르면 이해 어려운 것들.

---

## 1. Wrapper 패턴 (래퍼 / 박싱)

### 📖 일반 설명

**한 객체를 다른 객체로 감싸서(Wrap)** 새로운 인터페이스를 제공하거나 기능을 확장하는 패턴.
원본 객체의 동작은 그대로 보존하면서, 겉에 "상자"를 씌워 메타정보/추가 동작을 덧붙임.

- **Java의 예**: `int`(원시) → `Integer`(객체) 박싱. `BufferedReader`가 `Reader`를 감쌈.
- **Python의 예**: `functools.wraps`가 함수를 감쌈, `collections.deque`가 리스트를 감쌈.
- **표준 분류**: GoF의 **Decorator**(기능 추가)와 **Adapter**(인터페이스 변환)의 근원이 되는 더 원초적 개념. "래퍼"는 패턴 언어에서 구조적 관용구로 널리 쓰임.

### 🎯 DeZero 등장 지점

#### step01 — `Variable`이 `ndarray`를 감쌈

```python
class Variable:
    def __init__(self, data):
        self.data = data   # ndarray를 상자 안에 넣음
```

- **왜 감싸는가?**: `ndarray` 자체엔 "이 데이터가 어떤 연산에서 왔는지" 추적 기능이 없음.
- **감싸서 얻는 것**: `grad`(미분값), `creator`(어떤 Function이 만들었는지) 등 역전파 메타정보를 붙일 공간 확보.
- **PyTorch/TensorFlow 동일 철학**: `Tensor` 클래스가 ndarray 대신 감싸는 구조.

#### (예정) 이후 step에서 래퍼 재등장
- step50: `Parameter`가 `Variable`을 다시 감쌈 (가중치 표현용)
- step51: `Model`이 여러 `Layer`/`Parameter`를 감쌈

### 🔑 핵심 키워드

`#래퍼` `#박싱` `#박스(Box)` `#메타정보추가` `#관심사분리`

---

## 2. Template Method 패턴

### 📖 일반 설명

**기반 클래스(base class)가 알고리즘의 뼈대(골격)를 정의**하고,
**구상 클래스(concrete subclass)가 살(특정 단계의 구현)을 붙이는** 행동 패턴.

- "무엇을 할지는 고정, 어떻게 할지는 자식에게 위임"
- GoF 23패턴 중 **행동(Behavioral)** 분류
- **전형적 예**: 프레임워크에서 흔히 보는 "여기는 우리가 정해둠, 너희는 이 메서드만 구현해"

### 🎯 DeZero 등장 지점

#### step02 — `Function.__call__`이 뼈대, `forward()`가 살

```python
class Function:
    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② 핵심: 자식이 구현한 forward 호출 ← 패턴의 정수
        return Variable(y)              # ③ 상자 포장

    def forward(self, x):
        raise NotImplementedError()     # 자식이 반드시 구현해야 함


class Square(Function):                 # 자식은 forward()만 정의하면 OK
    def forward(self, x):
        return x ** 2
```

- **뼈대(`__call__`)**: "상자 까기 → 계산 → 상자 포장" 흐름. 이 알고리즘은 모든 Function에 동일.
- **살(`forward`)**: `x ** 2`냐 `np.exp(x)`냐 `x + y`냐 — 함수마다 다름. 자식이 채움.
- **`raise NotImplementedError()`**: "자식이 안 구현하면 바로 에러"라는 강제. 파이썬 전통적 추상 메서드 관용구.

### 💡 통찰

- **"상자는 기반 클래스가, 공은 자식이"** — 관심사 분리(SoC, Separation of Concerns).
  - `Function.__call__`: Variable 상자 언팩/패킹 (프레임워크 관심사)
  - `Square.forward`: 순수 수학 연산 (도메인 관심사)
- **PyTorch와의 연결**: `torch.nn.Module.__call__` → `forward()` 구조가 동일. DeZero가 PyTorch 스타일인 이유가 여기에.
- **`abc.ABC`와 비교** (탐구 후보): `raise NotImplementedError()` 대신 `@abstractmethod` 데코레이터를 쓰면 인스턴스화 자체를 막을 수 있음. DeZero는 전통적 방식 택함 (나중에 깊이 파볼 주제).

> 🔬 **심화 탐구**: [exploration_09_abc_abstract.md](./exploration_09_abc_abstract.md) — `abc.ABC` vs `NotImplementedError` 비교, 우리 step02 코드를 abc로 바꿨을 때의 변화, 왜 책은 전통 방식을 택했는지 분석

### 🔑 핵심 키워드

`#TemplateMethod` `#GoF` `#행동패턴` `#기반클래스` `#추상메서드` `#NotImplementedError` `#관심사분리` `#SoC` `#PyTorch스타일`

---

## 📌 참고: 패턴 간 구분 (자주 헷갈리는 포인트)

### Wrapper vs Template Method

두 패턴은 **다른 레벨**의 관심사:

| | Wrapper | Template Method |
|---|---|---|
| **무엇을?** | 객체를 객체로 감쌈 | 알고리즘 뼈대를 고정 |
| **DeZero 사례** | `Variable`이 `ndarray`를 감쌈 | `Function.__call__`이 호출 흐름 고정 |
| **등장 step** | step01 | step02 |
| **GoZ 분류** | 구조 (Decorator/Adapter 근원) | 행동 |

→ `Variable`(래퍼)을 `Function.__call__`(템플릿)이 다루는 구조. 두 패턴이 **협력**해서 DeZero의 기본 골격을 이룸.

---

## 📖 용어집 (Glossary) — 번역이 어색한 OOP/패턴 용어 모음

> 한국어 OOP/패턴 용어 중 **원어를 모르면 이해하기 어려운** 것들 정리.
> 일상어와 의미가 충돌하거나, 번역이 어색해 헷갈리는 경우 위주.

| 한국어 | 원어 | 실제 의미 | 비고 |
|---|---|---|---|
| **구상 클래스** | Concrete class | "구체화된 클래스" — 실제 구현을 가진 자식 클래스 | ⚠️ 일상어 "구상(구상하다=생각하다)"과 충돌. OOP에선 "abstract(추상) ↔ concrete(구체)" 대척 개념 |
| **추상 클래스** | Abstract class | "추상적인 클래스" — 구현 없이 개념만 정의한 부모 클래스 | 비교적 직관적이라 헷갈림 적음 |
| **래퍼** | Wrapper | "감싸는 것" — 객체를 다른 객체로 감싸는 구조 | 일상어와 일치, 헷갈림 없음 |
| **데코레이터** | Decorator | (1) **패턴**: 기능 추가를 위해 객체를 감쌈. (2) **파이썬 기능**: `@` 구문으로 함수/클래스 장식 | ⚠️ 두 의미 혼동 주의. GoF 패턴 vs 파이썬 `@decorator` |
| **디스크립터** | Descriptor | 속성 접근을 커스터마이징하는 객체 (`__get__`, `__set__`) | 번역 없이 음차. `property`가 대표적 디스크립터 |
| **메타클래스** | Metaclass | "클래스의 클래스" — 클래스 생성을 커스터마이징 | `type`이 최상위 메타클래스. abc.ABCMeta 등 |
| **인스턴스** | Instance | 클래스로부터 생성된 구체적 객체 | 번역 없이 음차. 일상어 혼동 적음 |
| **인스턴스화** | Instantiation | 클래스 → 인스턴스를 만드는 행위 | "instantiation"의 번역. "객체 생성"과 거의 동의어 |
| **상속** | Inheritance | 부모 클래스의 속성/메서드를 자식이 물려받음 | 직관적 |
| **오버로딩** | Overloading | 같은 이름의 함수/연산자를 여러 정의로 쓰는 것 | ⚠️ 파이썬에선 진짜 오버로딩 없음. 연산자 오버로딩은 `__add__` 등 매직 메서드 정의 |
| **오버라이딩** | Overriding | 부모의 메서드를 자식이 **재정의**하는 것 | Square.forward가 Function.forward를 오버라이딩 |
| **매직 메서드** | Magic method (dunder) | `__init__`, `__call__` 등 밑줄 2개로 둘러싼 특수 메서드 | "dunder" = double underscore. "스페셜 메서드"라고도 |
| **메서드** | Method | 클래스 내부에 정의된 함수 | ⚠️ C++에서는 "멤버 함수(member function)"라 부름. Python/Java/C#/Ruby 등은 "메서드". 사실상 동일 개념, 언어 전통만 다름 (C++: 함수 중심 / Smalltalk: 메시지 전달 패러다임) |
| **@override** | Override 데코레이터 (Python 3.12+) | 부모 메서드를 재정의함을 명시 | ⚠️ 런타임 강제력 ❌ (정적 분석 도구 mypy/pyright 필수). C++ `override`/Java `@Override`와 비슷하지만 강제력 약함. 상세: exploration_09 §9 |

### 💡 자주 헷갈리는 쌍

- **추상(abstract) ↔ 구상(concrete)**: 개념 ↔ 구현. GoF 책의 기본 대척.
- **오버로딩(overloading) ↔ 오버라이딩(overriding)**: 이름 같은 여러 함수 ↔ 부모 메서드 재정의. **파이썬에선 오버라이딩만 진짜 기능**.
- **인스턴스(instance) ↔ 객체(object)**: 거의 동의어. 엄밀히는 "클래스로부터 만든 객체"가 인스턴스.
- **매개변수(parameter) ↔ 인자(argument)**: 정의부 변수 ↔ 호출부 값 (step02 결정 기록에서 정리)
- **메서드(method) ↔ 함수(function)**: 클래스 내부 정의 ↔ 독립 함수. C++ "멤버 함수" = "메서드". 파이썬에선 실제로 "첫 인자 self 자동 바인딩" 설명자로 함수를 감싼 것뿐
- **@override ↔ @abstractmethod**: 재정의 명시 (정적 분석) ↔ 구현 강제 (런타임). 강제력과 검사 시점이 다름. 상세: exploration_09 §9

---
