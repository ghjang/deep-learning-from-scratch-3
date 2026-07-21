# 🧪 보충 탐구 #6 — Python 기본 자료형 (시퀀스와 참조 모델)

> **step01 직후 보충 학습 #6** (2026-07-21)
> 탐구 #5(B.1)에서 다루던 "리스트/튜플/문자열/레퍼런스" 주제를 분리.
> 브로 질문들에서 파생: "튜플 원소가 mutable이면?", "레퍼런스가 포인터?", "문자열도 immutable?"

---

## 목차

- [A. 시퀀스 자료형 3종 — list, tuple, str](#a-시퀀스-자료형-3종--list-tuple-str)
- [B. 접근 문법은 동일 — 오리 타이핑](#b-접근-문법은-동일--오리-타이핑)
- [C. immutable의 함정 — 튜플 원소가 mutable이면](#c-immutable의-함정--튜플-원소가-mutable이면)
- [D. 파이썬 레퍼런스의 정체 — "전부 참조"](#d-파이썬-레퍼런스의-정체--전부-참조)
- [E. 얕은 복사 vs 깊은 복사](#e-얕은-복사-vs-깊은-복사)
- [F. 문자열 — 특수 취급되는 immutable 객체](#f-문자열--특수-취급되는-immutable-객체)

---

## A. 시퀀스 자료형 3종 — list, tuple, str

파이썬의 대표적인 시퀀스 자료형 3종. 메타 속성(`__mro__`, `shape` 등)이 튜플로 표현되는 이유를 이해하려면 기본 필수.

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

**키워드**: `#list` `#tuple` `#str` `#mutable` `#immutable` `#해시가능` `#딕셔너리키` `#다중반환` `#언패킹`

---

## B. 접근 문법은 동일 — 오리 타이핑

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

### B.1 오리 타이핑의 깊은 의미 — 구조적 타이핑 (C++ TMP와 비교)

> 브로 통찰: "오리 타이핑, 간만에 C++ TMP를 생각나게 하기도"

정확한 비교! 둘 다 **"타입 이름이 아니라 구조로 동작"** 한다는 공통점. 하지만 실행 모델은 완전 반대.

#### 명목적 vs 구조적 타이핑

- **명목적 (nominal)**: "이 클래스가 `Iterable`을 **상속받았**나?" (Java, C#)
- **구조적 (structural)**: "`iter()` 메서드가 **있**나?" (Python, TypeScript, Go)

→ C++ TMP, Python Protocol, TypeScript, Go interface 전부 **구조적 타이핑**의 예.

#### C++ TMP vs Python Protocol — 비교

**C++ TMP (컴파일 타임 검증)**:
```cpp
template <typename T>
auto process(T container) {
    return container.size();  // T에 size() 있어야 함
}
process(std::vector<int>{1,2,3});  // OK
// process(int{42});               // ❌ 컴파일 에러! int에 size() 없음
```

**Python Protocol (런타임 시도)**:
```python
def process(container):
    return container.size()   # 그냥 호출, 없으면 죽음

process(MyContainer())  # ✅ size() 있으면 OK
process(42)             # ❌ RuntimeError — int엔 size() 없음 (실행해봐야 앎)
```

#### 본질적 차이 — 컴파일 타임 vs 런타임

| | C++ TMP | Python 오리 타이핑 |
|---|---|---|
| **검증 시점** | 컴파일 타임 | 런타임 |
| **오류 발견** | 빌드 실패 (빨리/정확) | 실행 중 (늦게/모호) |
| **유연성** | 낮음 (엄격) | 높음 (관대) |
| **철학** | "미리 다 검증" | "일단 해봐, 책임은 너" |

#### C++20 concepts / Python typing.Protocol — 명시적 구조적 타이핑

둘 다 "구조적 타이핑을 명시적으로" 만드는 도구:

```cpp
// C++20 concepts
template <typename T>
requires requires(T t) { t.size(); }
auto process(T container) { return container.size(); }
```

```python
# Python typing.Protocol (PEP 544)
from typing import Protocol

class Sized(Protocol):
    def size(self) -> int: ...

def process(container: Sized) -> int:
    return container.size()

# pyright가 에디터에서 정적 검증!
process(MyContainer())   # ✅ pyright OK
process(42)              # ⚠️ pyright 경고
```

→ **`typing.Protocol`이 사실상 C++20 concepts의 파이썬 버전**. 런타임은 관대하지만 pyright가 정적으로 검증.

#### C++ TMP의 진짜 이질성 — 컴파일 타임 연산

C++ TMP는 단순한 구조적 타이핑을 넘어 **"컴파일 타임에 실행되는 프로그래밍"** 이야:

```cpp
// 컴파일 타임에 팩토리얼 계산!
template <int N>
struct Factorial {
    static constexpr int value = N * Factorial<N - 1>::value;
};
constexpr auto x = Factorial<5>::value;   // 컴파일 타임에 120으로 결정
```

→ 파이썬엔 이런 게 아예 없음 (런타임에 전부 실행). Python Protocol은 메타프로그래밍이 아니라 그냥 "런타임에 메서드 있나 확인"일 뿐.

#### DeZero와의 연결

DeZero의 모든 오리 타이핑이 사실 이거야:

```python
class Function:
    def __call__(self, input):
        x = input.data            # input.data만 있으면 됨 (프로토콜)
        y = self.forward(x)
        output = Variable(y)
        return output
```

→ `input`이 `Variable`인지 **검사 안 함**. `.data` 있으면 됨. 이게 **오리 타이핑 = 구조적 타이핑**.

**키워드**: `#오리타이핑` `#ducktyping` `#접근문법동일` `#EAFP` `#isinstance` `#구조적타이핑` `#명목적타이핑` `#C++TMP` `#C++20concepts` `#typing.Protocol` `#PEP544` `#컴파일타임vs런타임` `#Go인터페이스` `#TypeScript`

---

## C. immutable의 함정 — 튜플 원소가 mutable이면

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

→ 이게 D(레퍼런스 정체)와 직접 연결됨. **immutability는 "참조만 못 바꾼다"**는 게 핵심.

**키워드**: `#튜플원소mutable함정` `#참조레벨불변` `#immutability` `#포인터모델`

---

## D. 파이썬 레퍼런스의 정체 — "전부 참조"

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

**키워드**: `#레퍼런스` `#객체참조` `#id함수` `#참조복사` `#불변값처럼` `#ReferenceSemantics` `#C포인터비교`

---

## E. 얕은 복사 vs 깊은 복사

레퍼런스 모델을 이해하면 자연스럽게 이어지는 주제. 중첩 구조에서 복사가 어떻게 동작하는지.

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

| 방식 | 코드 | 동작 |
|---|---|---|
| 참조 복사 | `y = x` | 같은 객체 가리킴 |
| 얕은 복사 | `copy.copy(x)` | 외부 컨테이너만 새로, 원소는 참조 공유 |
| 깊은 복사 | `copy.deepcopy(x)` | 전부 재귀적으로 새로 복사 |

→ DeZero에선 `grad` 초기화(`np.zeros_like`) 등에서 이 개념이 숨어있음.

**키워드**: `#얕은복사` `#깊은복사` `#copy.copy` `#copy.deepcopy` `#중첩복사`

---

## F. 문자열 — 특수 취급되는 immutable 객체

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

**키워드**: `#문자열immutable` `#새인스턴스반환` `#인턴` `#join` `#성능함정` `#JavaString비교`

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- 탐구 #1 (Python 기본): [exploration_01_python_basics.md](./exploration_01_python_basics.md)
- 탐구 #5 (객체 모델, A. CPython 내부): [exploration_05_python_object_model.md](./exploration_05_python_object_model.md)
- 이 탐구는 원래 탐구 #5의 B.1에서 분리됨
