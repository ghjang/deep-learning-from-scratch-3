# 🧪 보충 탐구 #8 — 런타임 클래스 조작 (Monkey Patching / 메타프로그래밍)

> **step01 직후 보충 학습 #8** (2026-07-21)
> 원래 탐구 #5의 E.9 섹션이었으나, 05가 비대해져서 분리.
> 파이썬의 런타임 클래스 조작 — Monkey Patching, 메타프로그래밍, 동적 수정 등을 다룸.

---

## 목차

- [E.9.1 메서드 교체/추가 (Monkey Patching)](#e91-메서드-교체추가-monkey-patching)
- [E.9.2 런타임에 새 메서드/속성 추가](#e92-런타임에-새-메서드속성-추가)
- [E.9.3 독스트링 동적 변경](#e93-독스트링-동적-변경)
- [E.9.4 메서드 후크 — 데코레이터의 본질](#e94-메서드-후크--데코레이터의-본질)
- [E.9.5 상속 구조까지 런타임에 변경](#e95-상속-구조까지-런타임에-변경-극단적)
- [E.9.6 용어 정리](#e96-용어-정리)
- [E.9.7 "할 수 있다" ≠ "해야 한다"](#e97-할-수-있다--해야-한다")
- [E.9.8 다른 언어와 비교](#e98-다른-언어와-비교)
- [E.9.9 네임스페이스와 C# Partial Class](#e99-네임스페이스와-c-partial-class)
- [E.9.10 객체→소스 역직렬화](#e910-동적으로-수정한-클래스를-소스-코드로-출력할-수-있나)

---

## E.9 런타임 클래스 조작 — Monkey Patching의 세계

> 브로 통찰: "클래스 자체 수정이라... 메서드 코드 후크 넣거나 독스트링 달거나, 생각할 수 있는 모든 조작이 가능하단 소리?"
> → **정답! 거의 모든 조작이 런타임에 가능.** 이게 파이썬 "동적(dynamic)"의 진짜 의미.

#### E.9.1 메서드 교체/추가 (Monkey Patching)

```python
class Foo:
    def bar(self):
        return "원래 동작"

f = Foo()
print(f.bar())   # "원래 동작"

# 런타임에 메서드를 완전히 교체!
def new_bar(self):
    return "🔥 바꿨다!"

Foo.bar = new_bar           # 클래스 자체를 수정
print(f.bar())              # "🔥 바꿨다!" ← 기존 인스턴스도 영향!
```

→ 이걸 **Monkey Patching** 이라고 함.

#### E.9.2 런타임에 새 메서드/속성 추가

```python
class Foo: pass
f = Foo()

# 클래스에 없던 메서드를 런타임에 추가
def greet(self, name):
    return f"안녕 {name}"

Foo.greet = greet
print(f.greet("브로"))      # "안녕 브로"

# 클래스 변수도 추가 가능
Foo.version = "0.0.13"
print(f.version)             # "0.0.13"
```

#### E.9.3 독스트링 동적 변경

```python
class Foo:
    """원래 독스트링"""

Foo.__doc__ = "🔥 런타임에 바꾼 독스트링"
print(Foo.__doc__)          # "🔥 런타임에 바꾼 독스트링"
help(Foo)                   # help()도 변경된 독스트링 표시!
```

→ 독스트링도 그냥 속성(`__doc__`)이라서 변경 가능.

#### E.9.4 메서드 후크 (전/후 가로채기) — 데코레이터의 본질

```python
class Foo:
    def bar(self):
        return "원래 동작"

original = Foo.bar

def with_logging(self):
    print(f"[LOG] bar() 호출")
    result = original(self)
    print(f"[LOG] bar() 결과: {result}")
    return result

Foo.bar = with_logging      # 래핑된 버전으로 교체

f = Foo()
f.bar()
# [LOG] bar() 호출
# [LOG] bar() 결과: "원래 동작"
```

→ 이게 진짜 **데코레이터의 본질**. 데코레이터가 결국 함수/메서드를 래핑하는 작업이니까.

#### E.9.5 상속 구조까지 런타임에 변경 (극단적)

```python
class Base1:
    def whoami(self): return "Base1"
class Base2:
    def whoami(self): return "Base2"

class Foo(Base1): pass

f = Foo()
print(f.whoami())           # "Base1"

Foo.__bases__ = (Base2,)    # 런타임에 부모를 바꿈!
print(f.whoami())           # "Base2" ← 부모가 바뀜!
```

→ Java/C#에선 상상도 못 할 일.

#### E.9.6 용어 정리

| 용어 | 의미 |
|---|---|
| **Monkey Patching** | 런타임에 클래스/모듈의 코드를 교체/추가 |
| **Metaprogramming** | 프로그램이 자기 자신의 코드를 조작 |
| **Reflection** | 런타임에 구조 검사 + 조작 |

#### E.9.7 "할 수 있다" ≠ "해야 한다"

이런 조작은 **강력하지만 위험**:

```python
# 위험한 예시
import some_library

def hacked_method(self):
    return "해킹!"

some_library.SomeClass.method = hacked_method
# 이제 some_library 전체가 해킹된 메서드 사용! 디버깅 지옥
```

**파이썬 커뮤니티 태도**:
- ✅ **장점**: 긴급 버그 패치, 테스트 mock, 라이브러리 확장
- ❌ **단점**: 디버깅 어려움, 의도치 않은 부작용, "마법" 코드
- 📖 **PEP 20**: "명시적이 함축적보다 낫다" — 너무 마법 같은 코드는 피해

**실전에서 진짜 유용한 예**:
1. **테스트 Mock**: `Database.query = fake_query`
2. **라이브러리 확장**: `np.my_helper = my_helper`
3. **데코레이터**: 표준적이고 권장되는 메타프로그래밍

#### E.9.8 다른 언어와 비교

| 언어 | 런타임 클래스 조작 |
|---|---|
| **Python** | ✅ 거의 모든 것 가능 |
| **JavaScript** | ✅ prototype 조작으로 가능 |
| **Ruby** | ✅ "Open Class"로 가능 |
| **Java** | ❌ 제한적 (리플렉션 일부, 바이트코드 조작 필요) |
| **C++** | ❌ 불가능 (컴파일 타임 결정) |

→ 동적 언어(Python/JS/Ruby)의 공통 능력.

#### E.9.9 네임스페이스와 C# Partial Class

> 브로 질문: "파이썬에 '네임스페이스'란 개념이 있나? 그리고 C# partial class 같은 게 가능한가?"
> 브로 자답: "동적 타이핑이니 런타임에 넣어도 되겠네?" → **정답!**

##### 파이썬의 네임스페이스 = 딕셔너리

파이썬에 네임스페이스는 **공식 개념**. 그리고 모두 **딕셔너리로 구현**돼 있음.

```python
# 4가지 네임스페이스
# 1. Built-in (내장) — 인터프리터 시작 시
print, len, int, str        # builtins 모듈

# 2. Global/Module (모듈) — 모듈 로드 시
PI = 3.14                   # 이 모듈의 전역
import numpy as np          # np도 전역

# 3. Class (클래스) — class 정의 실행 시
class Variable:
    count = 0               # Variable.count

# 4. Local (함수) — 함수 호출 시 생성, 종료 시 소멸
def foo():
    x = 1                   # foo의 local
```

**핵심**: 각 네임스페이스는 딕셔너리로 구현.
```python
print(type(Variable.__dict__))   # <class 'mappingproxy'> (읽기 전용 dict)
print(type(globals()))           # <class 'dict'>
```

**LEGB 룰 = 네임스페이스 탐색 순서** (exploration_01 A.2.4 참조):
```
L - Local → E - Enclosing → G - Global → B - Built-in
```

##### C# Partial Class vs 파이썬 — 런타임으로 흉내

**C#은 컴파일 타임 partial**:
```csharp
// File1.cs
public partial class Foo {
    public void Method1() { ... }
}
// File2.cs
public partial class Foo {
    public void Method2() { ... }
}
// 컴파일 시 하나로 합쳐짐
```

**파이썬은 런타임에 그냥 추가** (Monkey Patching과 같은 메커니즘):
```python
# file1.py
class Foo:
    def method1(self):
        return "method1"

# file2.py
from file1 import Foo

def method2(self):
    return "method2"

Foo.method2 = method2      # ← 런타임에 추가!

f = Foo()
print(f.method1())         # "method1"
print(f.method2())         # "method2" ← partial처럼 동작!
```

→ 브로 자답 정답: "동적 타이핑이니 런타임에 넣어도 되겠네" → 정확함!

##### 더 세련된 방법 — Mixin으로 확장

```python
class VariableCore:
    def __init__(self, data):
        self.data = data

class VariableOpsMixin:
    def square(self):
        return self.data ** 2

# 런타임에 Mixin의 메서드들을 추가
for name, method in VariableOpsMixin.__dict__.items():
    if not name.startswith('_'):
        setattr(VariableCore, name, method)

v = VariableCore(3)
print(v.square())          # 9
```

##### 가장 pythonic한 방법 — 다중 상속

```python
class VariableCore:
    def __init__(self, data):
        self.data = data

class VariableOps:
    def square(self):
        return self.data ** 2

class Variable(VariableCore, VariableOps):
    pass

v = Variable(3)
print(v.square())          # 9
```

→ 파이썬에선 partial이 **필요 없음**. 다중 상속이나 Mixin으로 자연스럽게 같은 효과.

##### "언제든 어디든 추가/수정 가능"의 함정

```python
# 모듈 전역 네임스페이스
globals()['new_var'] = 42
print(new_var)             # 42

# 클래스 네임스페이스
class Foo: pass
setattr(Foo, 'new_method', lambda self: "새 메서드")

# 인스턴스 네임스페이스
f = Foo()
setattr(f, 'new_attr', 100)
print(f.new_attr)          # 100
```

→ 전부 가능. 하지만 **위험**:
```python
import numpy as np
np.array = lambda x: "해킹!"   # ← 전역 수정, numpy 전체 망가짐!
```

이래서 **"consenting adults"** 원칙이 중요. "기술적으로 가능은 하지만 하지 마".

##### 다른 언어와 비교

| 언어 | 네임스페이스 | Partial Class | 런타임 변경 |
|---|---|---|---|
| **Python** | 딕셔너리 (`__dict__`) | ❌ 없음 (Monkey Patching/Mixin으로 대체) | ✅ 자유로움 |
| **C#** | 컴파일 타임 구조 | ✅ `partial` 키워드 | ❌ 제한적 |
| **Java** | 컴파일 타임 패키지 | ❌ 없음 | ❌ 제한적 |
| **C++** | 컴파일 타임 namespace | ❌ 없음 | ❌ 불가능 |

→ C#이 `partial`이라는 **안전한 컴파일 타임** 도구를 제공하는 반면, 파이썬은 **런타임 자유**를 대신 줌.

**키워드**: `#네임스페이스` `#__dict__` `#딕셔너리구현` `#LEGB` `#PartialClass` `#C#비교` `#Mixin` `#다중상속` `#런타임추가` `#globals()` `#setattr` `#consentingadults`

#### E.9.10 동적으로 수정한 클래스를 소스 코드로 출력할 수 있나?

> 브로 질문: "동적으로 수정한 클래스 객체를 소스 코드 파일로 출력 가능? 코드 포맷팅된 형태로?"
> → **완전 자동은 어렵지만 부분적 추출은 가능.** 도구들 있음.

##### 핵심 어려움: 런타임 객체 ≠ 소스 코드

파이썬은 런타임에 **바이트코드(bytecode)**로 실행돼. 원래 소스 코드 형태(텍스트)를 항상 보존하지 않음.

```
소스 코드 (.py 파일)
    ↓ 컴파일
바이트코드 (.pyc 파일)
    ↓ 실행
런타임 객체 (메모리)

← 역방향(객체 → 소스)은 정보 손실이 큼!
```

→ 컴파일 과정에서 포맷팅(들여쓰기, 빈 줄, 주석)이 날아감. 그래서 완벽한 역직렬화는 어려움.

##### 도구 1: `inspect.getsource` — 원래 소스 추출

```python
import inspect

class Foo:
    def bar(self):
        """Bar 메서드"""
        return self.data + 1

print(inspect.getsource(Foo.bar))
# def bar(self):
#     """Bar 메서드"""
#     return self.data + 1
```

→ 원본 소스 파일이 있으면 추출 가능. 파이썬이 소스 파일을 읽을 때 어디서 왔는지 기억해둬서 가능.

**한계**: 소스 파일이 있어야 함.
- `exec("class Dynamic: pass")`로 만든 클래스 → ❌
- `type('Dynamic', (), {'x': 1})`로 만든 클래스 → ❌
- REPL에서 입력한 코드 → ❌

##### 도구 2: `ast` (추상 구문 트리)

```python
import inspect
import ast

source = inspect.getsource(Foo.method)
tree = ast.parse(source)
print(ast.dump(tree, indent=2))   # 트리 구조 출력

# 다시 소스로 변환 (Python 3.9+)
print(ast.unparse(tree))
# def method(self):
#     x = 1
#     return x + 2
```

→ 소스 → AST → 소스 변환 가능. 하지만 **원본 포맷(들여쓰기, 빈 줄)은 보존 안 됨**.

> 💡 **`astor` vs `ast.unparse`**: 둘 다 AST→소스 변환 도구.
> - `astor`: 서드파티 (`pip install astor`). 2013년부터. 예전 국룰.
> - `ast.unparse`: 파이썬 **표준** (Python 3.9+, 2020). 설치 불필요.
> - 요즘은 `ast.unparse`가 표준이라 `astor`는 레거시로 추세 하락.
> - 우리 프로젝트(3.13)에선 `ast.unparse` 바로 쓰면 됨.
> - 파이썬 진영의 **"좋은 서드파티 → 표준 흡수"** 전통적 패턴 (`pathlib`, `enum`, `dataclasses` 등도 같은 사례).

##### 도구 3: `black`/`ruff` 조합 (반자동 포맷팅)

```python
import inspect
import subprocess

source = inspect.getsource(Foo)
# (가상) black/ruff로 포맷팅
# formatted = subprocess.run(['ruff', 'format', '-'], input=source, ...)
```

→ 런타임 정보 → 소스 추출 → 포맷팅 도구 조합. 완전 자동화는 아님.

##### 도구 4: 객체 상태 직렬화 (소스는 아님)

```python
import pprint

class Foo:
    def __init__(self):
        self.x = 1
        self.y = "hello"

f = Foo()
pprint.pprint(f.__dict__)
# {'x': 1, 'y': 'hello'}
```

→ 상태는 쉽게 출력 가능. 하지만 "소스 코드"는 아님.

##### JavaScript가 진짜 신기한 케이스

```javascript
function foo() {
    return 42;
}

console.log(foo.toString());
// function foo() {
//     return 42;
// }
```

→ JS는 **함수를 문자열로 변환**하는 게 정말 잘 됨. `toString()` 한 방이면 소스가 나옴. 파이썬보다 훨씬 깔끔.

##### 다른 언어와 비교

| 언어 | 런타임 → 소스 역직렬화 | 방법 |
|---|---|---|
| **JavaScript** | ✅ 매우 잘 됨 | `Function.toString()` |
| **Python** | ⚠️ 부분적 | `inspect.getsource` (소스 파일 있을 때만) |
| **Java** | ⚠️ 디컴파일 | 바이트코드 디컴파일러 (JD-GUI 등) |
| **C#** | ⚠️ 가능 | 리플렉션 + Roslyn (코드 생성) |
| **C++** | ❌ 불가능 | 컴파일 타임 정보만 |

##### 실전 가치 — 언제 유용할까?

1. **코드 생성기** — 템플릿 기반 소스 생성 (ORM, API 클라이언트)
2. **문서화 도구** — Sphinx, pdoc 등이 클래스 정보로 문서 생성
3. **리팩토링 도구** — AST 조작 후 소스 재작성
4. **테스트 생성** — 모형 객체에서 테스트 코드 자동 생성

→ DeZero 학습에선 진짜 안 쓰임. 하지만 실전 메타프로그래밍에선 종종 등장.

##### 핵심 통찰

1. **완벽한 자동 역직렬화는 어려움** — 런타임 객체 ≠ 소스 코드
2. **`inspect.getsource`** — 원본 소스 파일이 있을 때만 추출 가능
3. **`ast` 모듈** — AST 조작으로 변환은 가능하지만 포맷 손실
4. **JS가 가장 잘 됨** — `Function.toString()` 한 방
5. **실전 가치**: 코드 생성, 문서화, 리팩토링 도구 등

**키워드**: `#소스코드출력` `#역직렬화` `#inspect.getsource` `#ast` `#ast.unparse` `#바이트코드` `#JavaScript.toString` `#코드생성` `#문서화` `#리팩토링` `#메타프로그래밍`


**학습 완료일**: 2026-07-21
**관련 링크**:
- 탐구 #5 (객체 모델): [exploration_05_python_object_model.md](./exploration_05_python_object_model.md)
- 이 탐구는 원래 탐구 #5의 E.9 섹션에서 분리됨
