# 탐구 22 — weakref와 GC: 약한 참조의 마법과 CPython 내부

> **시점**: step17 진행 중 (2026-07-31)
> **상태**: 📚 학습용 심화 노트 (weakref 도입에서 파생)
> **트리거**: 브로 핵심 질문 —
>   1. "weakref 자체도 객체라고 하면, 그 자체는 참조카운트가 어떻게 되나?"
>   2. "참조하는 객체가 어떻게 파이썬 내부에서 관리하는 메모리(?)를 건드려서
>      참조카운트가 동작하지 않게 하는, 뭔가 파이썬 언어 내부적인 지원을 통해서 그렇게 할 수 있는 건가?"
>   3. "GC가 순환참조 결국 처리한다고 책에 적혀있는데, 그게 정확히 어떻게?"
> **관련**: step17 (rezero/steps/step17.py), REZERO_CHANGES 항목 026

## 📌 왜 이 탐구를 했나

step17에서 weakref 도입. 브로가 두 가지 깊은 질문:
1. **weakref 자체의 정체** — weakref도 객체인가? 그럼 참조 카운트는?
2. **"약한 참조"의 메커니즘** — 도대체 어떻게 refcount 안 올리는 게 가능한가?
3. **GC와 순환 참조** — 결국 회수된다면 weakref가 왜 필요한가?

이 세 질문은 weakref를 "사용"하는 걸 넘어 "이해"하는 데 필수. 본 노트에서 깊이 파자.

---

## 1. ★ 핵심부터 — weakref도 객체다 (브로 질문 1)

### 실험으로 확인

```python
import weakref
import sys

class A:
    pass

a = A()                          # a 생성, refcount = 1
r = weakref.ref(a)               # weakref 객체 r 생성
print(type(r))                   # <class 'weakref.ReferenceType'> ★ weakref도 객체
print(sys.getrefcount(a))        # 2 (a 자신 + getrefcount 인자) — ★ r은 refcount 안 올림!

# 비교: 강한 참조
b = a                            # 강한 참조
print(sys.getrefcount(a))        # 3 — b가 refcount +1 올림 ★
```

★ 핵심 관찰:
- `r = weakref.ref(a)` → `r`은 분명 **객체** (weakref.ReferenceType 인스턴스)
- 근데 `a`의 refcount는 **안 올림** (여전히 1)
- 반면 `b = a` (강한 참조)는 refcount를 +1 올림

→ 브로 직관 정확: **weakref는 객체이되, "참조 카운트를 올리지 않는 특별한 객체"**.

### weakref 객체 자체의 생애

`r`도 파이썬 객체라 자기 자체의 refcount가 있음:
```python
sys.getrefcount(r)   # r 자신의 refcount (보통 1~2)
```

`r`이 사라지는 건 `r`에 대한 참조가 없어질 때. `a`가 사라지는 것과는 별개.

★ 핵심: **"r이 a를 가리킨다"와 "r의 생존"은 별개 문제**.
- `a`가 죽어도 `r`은 살아있을 수 있음 (그럼 `r()`은 None 반환)
- `r`이 죽어도 `a`는 살아있을 수 있음 (그냥 weakref 구독자 하나 줄어들 뿐)

### ★★ weakref 객체 자체의 refcount — 두 층위 분리 (브로 추가 질문) 🔥

브로 핵심 질문:
> "weakref 자체도 객체인 것이라면, weakref 인스턴스에 대한 참조는 어떻게 되는 거지?"

→ ★ 날카로운 질문. weakref는 **"두 개의 refcount"를 다루는 특별한 객체**임.

실험으로 확인 (실행 결과):
```
[1] a = A()                    → a refcount = 1
[2] r = weakref.ref(a)         → a refcount = 1 (그대로!) / r refcount = 1
[3] r2 = r                     → r refcount = 2 (★ r 자체는 일반 객체처럼 증가!) / a refcount = 1 (그대로)
[4] del r2                     → r refcount = 1
[5] del a                      → a 회수됨 / r은 살아있음, r() = None
[6] del r                      → r 자체 회수
```

★ **결정적 관찰 [3]**: `r2 = r` 하면 **r 자체 refcount는 2가 됨** (일반 객체처럼).
근데 **a의 refcount는 여전히 1**. → r에 대한 참조와 a에 대한 참조가 **완전히 분리**돼 있음!

#### 두 층위 분리 (핵심)

| 층위 | 대상 | refcount 동작 |
|---|---|---|
| **r 자체** | weakref 객체 r | **일반 파이썬 객체처럼** refcount 동작 (변수 할당/전달 시 ±) |
| **r이 가리키는 대상** | 객체 a | **refcount에 영향 X** ★ (약한 참조의 마법) |

#### weakref의 "이중성" (브로 통찰 정리)

- **r 자체는 평범한 파이썬 객체** — 자기 refcount 있고, 변수 할당/전달/삭제에 일반 객체처럼 반응
- **r이 가리키는 a는 특별 취급** — r을 통한 a 참조는 refcount에 영향 안 줌

→ 즉 **"r의 생존"과 "a의 생존"은 완전히 독립적**:
- a가 죽어도 r은 살 수 있음 ([5] 확인 — r()은 None)
- r이 죽어도 a는 살 수 있음 (a에 대한 강한 참조가 다른 데 있으면)

#### 비유 — "구독자 카드"

r은 **"구독자 카드"** 같은 존재:
- 카드 자체는 평범한 종이(객체) — 누가 카드를 들고 있나에 따라 카드의 refcount 변동
- 카드가 "구독 대상"에게 미치는 영향은 특별 — 구독 등록만 하고 대상에 부담(refcount) 안 줌
- 대상이 죽으면 카드에 "대상 사망" 도장만 찍힘 (카드 자체는 살아있음)

이 비유가 weakref의 "객체이되 특별"한 성격을 가장 잘 잡음.

---

## 2. ★★ "약한 참조"의 마법 — 어떻게 refcount 안 올리나 (브로 질문 2)

이게 가장 깊은 질문. 파이썬 내부 구조까지 가야 답이 보임.

### CPython의 모든 객체 — `PyObject` 구조체

CPython에서 모든 객체는 내부적으로 `PyObject` 구조체로 시작:
```c
// CPython 내부 (단순화)
typedef struct _object {
    int ob_refcnt;          // 참조 카운트 ★
    PyTypeObject *ob_type;  // 타입 정보
    // ... 이후 실제 데이터
} PyObject;
```

강한 참조가 생길 때마다 `Py_INCREF(obj)`가 `ob_refcnt`를 +1.
참조가 사라지면 `Py_DECREF(obj)`가 -1, 0 되면 메모리 해제.

### ★ weakref의 핵심 — `ob_refcnt`를 안 건드린다

`b = a` (강한 참조):
```c
// CPython 의사 코드
b = a;
Py_INCREF(a);   // ★ a->ob_refcnt++
```

`r = weakref.ref(a)` (약한 참조):
```c
// CPython 의사 코드
r = weakref_ref(a);
// ★ Py_INCREF(a) 호출 안 함! a->ob_refcnt 그대로
```

★ 브로 질문의 핵심 답: **`Py_INCREF`를 호출하지 않기 때문**. 이게 "파이썬 언어 내부적 지원"의 실체.

### ★ 그럼 어떻게 대상을 추적하나 — weakref 리스트

`Py_INCREF` 안 하면 `a`가 죽었을 때 weakref가 어떻게 아는가?
CPython은 지원하는 타입의 객체에 **별도 슬롯**을 둠:

```c
// 단순화 — 실제는 타입 슬롯(tp_weaklistoffset)으로 관리
typedef struct _object {
    int ob_refcnt;
    PyTypeObject *ob_type;
    // ...
    PyObject **ob_weakreflist;   // ★ weakref 관리용 슬롯 (지원 타입만)
} PyObject;
```

- `r = weakref.ref(a)` 호출 시:
  - `a->ob_weakreflist`에 `r`을 등록 (a의 refcount는 안 올림 ★)
  - `r`은 `a`의 메모리 주소를 알지만 refcount엔 영향 X
- `a`가 파괴될 때 (`ob_refcnt` 0 도달):
  - CPython이 `a->ob_weakreflist`를 순회하며 등록된 모든 weakref에게 알림
  - 각 weakref는 "대상이 죽었음" 상태로 전환 → 이후 `r()` 호출 시 None 반환

★ 이게 브로가 직감한 "파이썬 언어 내부적인 지원":
1. 모든 객체에 weakref용 슬롯이 있음 (지원 타입 한정)
2. weakref 생성 시 슬롯에 등록 (refcount 변동 없음)
3. 객체 파괴 시 슬롯 순회하며 weakref에게 통지

→ **"구독자(subscriber) 모델"**. weakref는 대상 객체의 소멸을 구독만 함.

### weakref를 지원하는 타입

모든 파이썬 객체가 weakref를 지원하는 건 아님. 지원 조건:
- 사용자 정의 클래스 (`class A:`) — 지원 O (기본)
- `list`, `dict`, `set` 등 내장 컨테이너 — 지원 O
- `int`, `str`, `tuple` 등 — 지원 X (변경 불가능 객체는 보통 미지원)
- `__slots__`에 `__weakref__` 안 넣은 클래스 — 지원 X

```python
class NoWeakRef:
    __slots__ = ['x']           # __weakref__ 슬롯 없음

weakref.ref(NoWeakRef())        # TypeError: cannot create weak reference
```

→ weakref 지원 여부도 `ob_weakreflist` 슬롯 유무로 결정됨.

---

## 3. ★ GC와 순환 참조 — 결국 회수되지만 (브로 질문 3)

### 파이썬 GC의 두 단계 메커니즘

| 메커니즘 | 작동 시점 | 순환 참조 잡나? | 속도 |
|---|---|---|---|
| **참조 카운팅 (Reference Counting)** | 참조 0 되는 즉시 | ❌ 순환 못 잡음 | 매우 빠름 |
| **순환 감지 GC (Cyclic GC)** | 주기적 (세대별) | ✅ 잡음 | 느림 |

### 참조 카운팅의 한계 — 순환 참조

```python
class Node:
    def __init__(self):
        self.partner = None

a = Node()              # a refcount = 1
b = Node()              # b refcount = 1
a.partner = b           # b refcount = 2
b.partner = a           # a refcount = 2 ★

del a                   # a refcount = 1 (b.partner가 아직 참조)
del b                   # b refcount = 1 (a.partner가 아직 참조)
# ★ 둘 다 refcount 1로 남음 → 참조 카운팅이 못 잡음!
# 메모리에 계속 남아있음 (순환 감지 GC가 올 때까지)
```

★ DeZero의 Variable↔Function 순환도 동일한 구조:
```
Variable.creator → Function
Function.inputs → Variable
→ 서로 참조, refcount 0 안 됨
```

### 순환 감지 GC (Cyclic GC) — 결국 잡는다

CPython은 순환 참조를 잡기 위한 별도 GC를 가짐. **세대별 GC (Generational GC)**:

| 세대 | 대상 | 수집 빈도 |
|---|---|---|
| 0세대 | 새로 만들어진 객체 | 자주 (수백 번 할당마다) |
| 1세대 | 0세대 수집에서 살아남은 객체 | 가끔 |
| 2세대 | 1세대 수집에서 살아남은 객체 | 드물게 |

알고리즘 (단순화):
1. 객체들의 참조 그래프를 추적
2. 외부에서 도달 불가능한 순환 그룹 식별
3. 그룹 전체를 회수

★ 핵심: **순환 참조는 결국 회수됨**. 단, GC 사이클이 돌아야 (지연).

### `gc` 모듈로 확인

```python
import gc

gc.collect()           # 강제 순환 GC 실행 (반환값 = 회수된 객체 수)
gc.get_threshold()     # 세대별 GC 임계값 (보통 (700, 10, 10))
gc.disable()           # 순환 GC 비활성화 (참조 카운팅만)
```

브로가 "책에 결국 처리한다고 적혀있다"고 한 게 바로 이 **순환 감지 GC**.

---

## 4. ★★ 그럼 왜 weakref가 필요한가? (핵심 질문)

브로의 날카로운 질문: "결국 회수된다면 weakref가 왜 필요한가?"

답: **결국 회수되지만, '결국'이 언제인지 모르고, 딥러닝은 기다릴 여유가 없다**.

### 이유 1 — GC 타이밍 예측 불가

순환 감지 GC는 세대별 임계값 도달 시 발동. 정확히 언제 돌지 모름.
- `gc.get_threshold()` 기본 (700, 10, 10): 0세대는 700번 할당마다
- 근데 실제 메모리 압력에 따라 다름

→ "이 순환 참조 그래프가 언제 회수될지" 예측 불가. 메모리 사용량 예측 어려움.

### 이유 2 — 즉시 회수해야 하는 딥러닝 특수성

DeZero Variable은 **큰 ndarray**를 들고 있음:
```python
x = Variable(np.random.randn(10000))    # 10000 float = ~80KB
# 신경망은 수백만~수십억 원소 텐서 다룸 → GB 단위
```

학습 루프 한 번에 수십~수백 Variable 생성. 순환 참조로 쌓이면:
```
루프 1회차: 그래프 N개 (GB 단위) 쌓임
루프 2회차: 또 N개 쌓임 (이전 것은 순환 참조라 GC 주기까지 안 사라짐)
...
메모리 폭발 → OOM (Out of Memory)
```

★ 핵심: **참조 카운팅의 "즉시 회수"는 GC보다 수십~수백 배 빠름**.
weakref로 순환 끊으면 즉시 회수 → 메모리 폭발 방지.

### 이유 3 — 예측 가능한 메모리 프로파일

weakref 사용 시:
- 순전파 끝나면 output Variable은 사용자 손에서 곧 버려짐
- weakref라 참조 카운트 0 → 즉시 회수
- → 메모리 사용량이 **예측 가능** (사용 중인 그래프만 남음)

→ 딥러닝 프레임워크(PyTorch, JAX, DeZero)가 전부 weakref 쓰는 이유.

### 책 step17 데모로 실증

```python
for i in range(10):
    x = Variable(np.random.randn(10000))    # big data
    y = square(square(square(x)))
    # 루프 끝나면 x, y는 다음 반복에서 버려짐
```

- **step16 (weakref 없음)**: 각 반복의 계산 그래프(3개 Function + Variable)가 순환 참조로 안 사라짐. 10회 누적 → GC 주기까지 수십 MB~GB 잔류.
- **step17 (weakref)**: 매 반복 끝나면 이전 그래프 즉시 회수. 메모리 안정.

★ 이게 "결국 회수됨"이지만 "결국"을 기다릴 수 없는 현실적 이유.

---

## 5. ★ weakref의 변형들 — 용도별 도구

### `weakref.ref(obj)` — 기본 약한 참조

```python
r = weakref.ref(obj)
r()        # obj 반환 (또는 None)
```
가장 기본. `r()` 호출로 실제 객체 획득.

### `weakref.proxy(obj)` — 투명 프록시

```python
p = weakref.proxy(obj)
p.method()    # ★ () 없이 직접 접근 (obj에 위임)
```
`r()`처럼 호출 안 해도 됨. 근데 obj 죽으면 접근 시 `ReferenceError`.

### `weakref.WeakKeyDictionary` / `weakref.WeakValueDictionary`

키 또는 값을 weakref로 잡는 딕셔너리. 캐시 구현에 유용.

### `weakref.finalize(obj, callback)` — 소멸 콜백

```python
weakref.finalize(obj, lambda: print("obj 죽음"))
del obj    # "obj 죽음" 출력
```
객체 파괴 시 콜백. weakref.ref와 달리 콜백 자체가 살아있음.

### 우리 step17 선택 — `weakref.ref`

```python
self.output_ref = weakref.ref(output)
...
output = self.output_ref()    # () 호출로 역참조
```
가장 단순하고 명시적. DeZero/PyTorch도 기본 ref 사용.

---

## 6. ★ 다른 언어는 어떨까 — 약한 참조의 보편성

약한 참조는 파이썬만의 개념이 아님. 대부분의 GC 지원 언어에 있음:

| 언어 | 약한 참조 |
|---|---|
| **Java** | `WeakReference`, `SoftReference`, `PhantomReference` (4단계) |
| **C#** | `WeakReference` |
| **JavaScript** | `WeakRef`, `WeakMap`, `WeakSet` |
| **C++** | `std::weak_ptr` (스마트 포인터와 짝) |
| **Rust** | `Weak<T>` (`Rc`/`Arc`와 짝) |

★ 핵심: **약한 참조는 GC와 참조 카운팅을 다루는 모든 언어의 공통 도구**.
"강한 참조 vs 약한 참조" 구분이 메모리 관리의 핵심 기법.

### C++ std::weak_ptr과의 비교 (가장 비슷)

C++의 `shared_ptr` (강한 참조, 참조 카운팅) + `weak_ptr` (약한 참조):
```cpp
auto sp = std::make_shared<int>(42);    // strong, refcount=1
std::weak_ptr<int> wp = sp;             // weak, refcount 안 올림 ★
auto locked = wp.lock();                // shared_ptr로 승격 (refcount +1)
```

★ C++의 순환 참조 문제도 동일:
```cpp
struct Node {
    std::shared_ptr<Node> partner;      // ★ 이러면 순환 발생!
};
// 해결: std::weak_ptr<Node> partner; 로 잡기
```

→ 우리 DeZero의 Variable↔Function 순환과 **정확히 같은 패턴**. 언어가 달라도 메모리 관리 문제는 보편.

---

## 7. ★ PyTorch의 사례 — autograd에서 weakref

PyTorch의 autograd 엔진도 비슷한 문제를 겪음. Variable(Tensor) ↔ Function(grad_fn) 순환.

PyTorch 접근:
- 역전파 후 **계산 그래프를 자동 해제** (`retain_graph=False` 기본)
- weakref는 아니지만, "역전파 후 그래프 버리기"로 순환 자체를 제거

→ DeZero가 weakref로 푼 방식과 다른 접근이지만, **목적은 동일** (순환 참조로 인한 메모리 누수 방지).

---

## 8. 요약 — 브로 세 질문에 대한 최종 답

| 질문 | 답 |
|---|---|
| **weakref 자체도 객체인가?** | ★ **객체다.** `weakref.ReferenceType` 인스턴스. 자기 자체 refcount도 있음. |
| **근데 대상 refcount는 어떻게 안 올리나?** | ★ CPython이 `Py_INCREF`를 호출하지 않기 때문. 대신 대상 객체의 `ob_weakreflist` 슬롯에 등록만 함. 대상 파괴 시 슬롯 순회하며 weakref에게 통지. **구독자 모델**. |
| **GC가 순환 참조 결국 처리하지 않나?** | ★ **처리함.** 순환 감지 GC(세대별)가 주기적으로 순환 그룹 회수. 근데 GC 타이밍 예측 불가, 딥러닝 큰 ndarray는 기다릴 여유 없음 → weakref로 즉시 회수 확보. |

### 핵심 키워드 세 줄 요약

- **weakref = "참조 카운트 안 올리는 구독자"** (CPython `Py_INCREF` 스킵 + `ob_weakreflist` 등록)
- **순환 감지 GC = "결국 회수하지만 느리고 예측 불가"** (세대별 주기 실행)
- **weakref 도입 이유 = "즉시 회수로 딥러닝 메모리 폭발 방지"** (GC 주기 못 기다림)

---

## 9. 🔓 더 파고 싶으면 (확장 후보)

| 주제 | 키워드 | 방향 |
|---|---|---|
| **CPython `ob_weakreflist` 내부** | `tp_weaklistoffset`, type slots | 타입마다 weakref 슬롯 어떻게 정의되나 |
| **세대별 GC 알고리즘** | mark-and-sweep, generational hypothesis | 왜 세대별이 효율적인가 (작은 객체 자주 죽음) |
| **`__del__`와 순환 참조** | finalizer, resurrection | `__del__` 정의된 객체는 순환 GC가 못 잡던 과거 (PEP 442 해결) |
| **tracemalloc** | 메모리 프로파일링 | 실제 메모리 누수 탐지 도구 |
| **Rust ownership vs weak** | `Rc`/`Weak`, `Arc`/`Weak` | 컴파일 타임 메모리 안전 vs 런타임 약한 참조 |
| **PyTorch retain_graph** | 역전파 후 그래프 해제 | weakref 대신 "명시적 해제" 접근 비교 |

### 회수 시그널

- step18 (메모리 절약 모드, Config/no_grad) → 본 노트 §4 (왜 즉시 회수가 중요한가)
- 다른 언어 메모리 관리 논의 → 본 노트 §6
- `gc.collect()` 마주칠 때 → 본 노트 §3

---

## 🔑 핵심 키워드

`#weakref` `#약한참조` `#weak-reference` `#참조카운팅` `#reference-counting` `#순환참조` `#circular-reference` `#가비지컬렉션` `#GC` `#순환감지GC` `#세대별GC` `#generational-GC` `#CPython` `#PyObject` `#ob_refcnt` `#Py_INCREF` `#ob_weakreflist` `#구독자모델` `#메모리누수` `#딥러닝특수성` `#큰ndarray` `#즉시회수` `#WeakKeyDictionary` `#C++-weak_ptr` `#Rust-Weak` `#step17파생` `#브로세질문`

## 📝 학습 완료일 / 관련 링크

- **완료일**: 2026-07-31 (step17 진행 중)
- **트리거**: 브로 세 질문 — weakref 객체 정체, 약한 참조 메커니즘, GC 순환 처리
- **관련 코드**: rezero/steps/step17.py (output_ref weakref 도입)
- **REZERO_CHANGES**: 항목 026 (weakref 도입)
- **관련 노트**: (없음 — 첫 GC/weakref 심화)
