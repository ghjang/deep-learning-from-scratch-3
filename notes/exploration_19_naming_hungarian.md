# 탐구 19 — 네이밍과 헝가리안 표기법: 변수명에 타입을 박을 것인가?

> **시점**: step16 진행 중 (2026-07-31)
> **트리거**: 브로 통찰 — "변수명 자체와 타입 힌트가 중복 느낌은 있는데, 이게 파이썬닉한가?"
> **결론**: 크로스 참조 네이밍 전면 개명(`creator` → `creator_func` 등) 시도 → **철회**.
>   현대 파이썬 철학 "이름은 역할, 타입은 힌트에 맡긴다" 채택.

## 📌 왜 이 탐구를 했나

step16에서 Variable/Function 크로스 참조 속성에 타입이 드러나게 개명하려 했다:

```python
# 시도한 개명
class Variable:
    creator_func: Function        # ← "Function"이라는 뜻
class Function:
    input_vars: tuple[Variable]   # ← "Variable"이라는 뜻
    output_var: Variable
```

이때 브로가 핵심 자각:
> "변수명 자체와 타입 힌트가 중복 느낌은 있다"

이 자각이 맞는지 검증하려고 이 탐구를 시작. 결론부터 말하면 **브로 직관이 현대 파이썬 철학과 정확히 일치**.

---

## 1. 헝가리안 표기법 (Hungarian Notation) — 역사

### 기원

1970년대 마이크로소프트의 Charles Simonyi(헝가리 출신)가 제안한 네이밍 컨벤션.
**변수명에 타입이나 용도를 접두사/접미사로 인코딩**하는 방식.

### 두 종류의 헝가리안

| 종류 | 예 | 의미 |
|---|---|---|
| **Systems Hungarian** | `int nCount`, `str sName`, `bool bIsValid` | 변수 **타입**을 인코딩 (n=int, s=str, b=bool) |
| **Apps Hungarian** | `usafeUserName`, `unsafeInput` | 변수 **의미/용도**를 인코딩 (unsafe=검증 안 됨) |

### 왜 유행했나

C나 구형 언어는 **타입을 코드에서 바로 알기 어려움**:
- C: `int x;` 선언이 파일 위에 있으면 함수 본문에서 타입이 안 보임
- 동적 타입 언어 초창기: IDE 지원 부족 → 이름에 단서 필요

→ 이름에 타입을 박아 **가독성** 확보. 당시엔 실용적.

### 왜 사라졌나

1. **IDE 발전** — 마우스 오버/자동완성으로 타입 즉시 확인 가능
2. **정적 타입 언어 발전** — 타입 선언이 더 명확해지고 가까이 위치
3. **타입 힌트 도입** — 파이썬도 3.5부터 타입 힌트로 타입 정보 명시 가능

→ 이름에 타입 박는 게 **중복**이 됨. 헝가리안은 구식으로 취급.

---

## 2. 파이썬과 헝가리안 — 반Pythonic

### PEP 8과 파이썬 철학

PEP 8은 변수명에 타입 접두사/접미사를 권장하지 않음.

```python
# ❌ 반Pythonic (Systems Hungarian)
age_int: int = 30
name_str: str = "bro"
user_list: list = []

# ✅ Pythonic
age: int = 30
name: str = "bro"
users: list = []
```

### Pythonic 네이밍 원칙

> **"이름은 데이터의 역할/의미를 말한다. 타입은 타입 힌트에 맡긴다."**

```python
# 좋은 예 — 이름이 "무엇인지(역할)" 말함
user_count: int              # "사용자 수" — 역할
elapsed_seconds: float       # "경과 시간(초)" — 역할 + 단위
is_valid: bool               # "유효한가?" — 역할

# 나쁜 예 — 이름이 "어떤 타입인지"만 말함 (타입 힌트와 중복)
count_int: int               # "_int"는 중복
time_float: float            # "_float"는 중복
```

### 예외: 역할과 타입이 우연히 일치할 때

```python
df: pd.DataFrame             # "DataFrame" — pandas 관례, 역할=타입
xs: list[np.ndarray]         # "xs" — 수학적 관례 (복수 x들)
df_sales, df_users           # 접두사 df가 DataFrame 강조 (역할+구분)
```

이건 헝가리안이 아님. **역할/식별**을 위한 것. 경계가 모호하지만 의도가 중요.

---

## 3. 우리 코드에 적용 — 판단 기준

### 시도한 개명 재검토

```python
# 시도 (Systems Hungarian 냄새)
self.creator_func: Optional["Function"] = None
#     ^^^^^^^^^^^                ^^^^^^^^^
#     "Function" 의미             "Function" 타입
#     ↑ 이름에 타입 인코딩         ↑ 타입 힌트로 또 인코딩
```

→ **정보가 두 번 들어감**. 브로 자각 정확.

### 판단 기준 — "이름이 질문에 답하는가?"

| 이름 | 답하는 질문 | 평가 |
|---|---|---|
| `creator_func` | "무엇이 이걸 만들었나? → 함수(Function)" | 답 명확하지만, 타입 힌트가 같은 답 제공 |
| `creator` | "무엇이 이걸 만들었나? → 창작자" | 역할 명확, 타입은 힌트에 맡김 ★ |
| `age_int` | "몇 살? → 정수" | 타입 힌트랑 중복, 역할 약함 |

→ `creator`가 `creator_func`보다 **Pythonic**. 역할(creator)은 말하되 타입(Function)은 힌트에 맡김.

### 크로스 참조 구조는 어떻게 가시화할까?

개명 없이도 **타입 힌트**로 충분히 가시화됨:

```python
class Variable:
    creator: Optional["Function"] = None      # ← 타입 힌트가 Function 명시

class Function:
    inputs: Optional[tuple[Variable, ...]]    # ← 타입 힌트가 Variable 명시
    output: Optional[Variable]               # ← 마찬가지
```

→ IDE/pyright로 마우스 오버하면 타입 바로 보임. 이름에 또 박을 필요 없음.

---

## 4. 그럼 언제 이름에 타입을 박는 게 허용되나?

### 생태계 관례 — 허용되는 경우

| 경우 | 예 | 이유 |
|---|---|---|
| **타입 힌트 없는 동적 코드** | `df = pd.DataFrame()`, `xs = [...]` | 힌트 없으니 이름이 유일한 정보원 |
| **여러 타입 가능성 있을 때** | `user_id: int \| str` | "id가 int인지 str인지" 의미 있음 |
| **프레임워크/관례** | PyTorch `grad_fn` | "역전파 함수" 강조 (단, `_fn`은 타입이 아닌 '역할'에 가까움) |
| **모호성 회피** | `name_str` vs `name_bytes` | 같은 개념의 다른 표현 구분 |

### 우리 코드는?

```python
self.creator: Optional["Function"] = None
```

- 타입 힌트 있음 ✅ → 이름에 타입 안 박아도 정보 손실 없음
- 모호성 없음 (creator가 Function 외에 다른 타입일 일 없음) ✅
- → **허용 경우에 해당 안 함. 철회가 맞음.**

---

## 5. 핵심 통찰 — "역할" vs "타입" 인코딩

이게 헝가리안 판별의 핵심.

### 역할 인코딩 (Pythonic)
```python
def process(users: list[User]) -> int: ...
#         ^^^^^                       ^^^
#         "사용자들" (역할)            "정수" (타입) — 분리됨
```
- 이름: 데이터가 **무엇을** 의미하는지
- 타입 힌트: 데이터가 **어떤** 구조인지
- → 두 정보가 독립적. 중복 아님.

### 타입 인코딩 (반Pythonic, Systems Hungarian)
```python
def process(user_list: list[User]) -> int: ...
#         ^^^^^^^^^                ^^^^^^^^
#         "사용자_리스트"           "리스트[사용자]"
#         ↑ 타입 인코딩             ↑ 타입 힌트 — 중복!
```
- 이름에 이미 타입(list) 박음
- 타입 힌트가 같은 정보 반복
- → 중복. 안 함.

### 경계 케이스 (판단 어려울 때)

```python
# df_sales vs sales
df_sales: pd.DataFrame    # 접두사 df — DataFrame 강조. 헝가리안? 관례?
sales: pd.DataFrame       # 접두사 없음. 더 Pythonic?
```

이 경계는 **컨텍스트/관례**에 따라 다름. pandas 커뮤니티에선 `df` 접두사가 널리 쓰임.
강하게 금지할 수는 없지만, 새 코드에선 접두사 없는 쪽이 더 Pythonic.

---

## 6. ★ 실제 프레임워크 사례 비교

### PyTorch

```python
# PyTorch Tensor
tensor.grad_fn        # "gradient function" — _fn 접미사
tensor.grad           # 단순 이름
tensor.requires_grad  # 불리언 속성인데 _bool 안 붙임
```

`grad_fn`은 `_fn`이 붙어있지만, 이건 **타입이 아니라 역할**(역전파 함수) 강조.
"어떤 함수냐? → 역전파 함수"를 이름으로 말함. 헝가리안보다는 역할 인코딩에 가까움.

### JAX

```python
jax.grad(f)(x)        # 단순한 이름. 타입 힌트도 거의 없는 편
```

### NumPy

```python
np.ndarray.shape      # tuple. shape_tuple 안 붙임
np.ndarray.dtype      # dtype 객체. dtype_obj 안 붙임
```

→ 메이저 파이썬 프레임워크는 **역할 중심 네이밍**. 타입 인코딩 회피.

---

## 7. ★ 우리 코드에 돌아와서 — 최종 결정

### 채택한 원칙

> **"이름은 역할을 말하고, 타입은 힌트에 맡긴다."** (현대 파이썬 철학)

### 적용 결과 (step16)

```python
class Variable:
    creator: Optional["Function"] = None        # creator (역할) + Function (타입 힌트)
    generation: int = 0                          # generation (역할) + int (타입 힌트)
    grad: Optional[np.ndarray] = None            # grad (역할) + ndarray (타입 힌트)

class Function:
    inputs: Optional[tuple[Variable, ...]]       # inputs (역할) + tuple[Variable] (타입)
    output: Optional[Variable]                   # output (역할) + Variable (타입)
    generation: int = 0
```

→ 모든 속성이 **역할(이름) + 타입(힌트)** 분리. 헝가리안 냄새 제거.

### 예외적으로 `_var`/`_func`를 쓰는 곳 (step16 기준)

| 경우 | 이름 | 이유 |
|---|---|---|
| `Function.__call__(input_var)` | `input_var` | 항목 002 — 빌트인 `input` 섀도잉 회피 (네이밍 문제 아닌 충돌 회피) |
| `fill_grad(start_var)` | `start_var` | 항목 014 — Variable 타입 명시적 + `output`과 구분 |
| `as_array(x)` | `x` (내부) | 제네릭, 타입 힌트로 충분 |

→ 이 예외들은 **충돌 회피/구분 목적**이지 타입 인코딩이 아님. 헝가리안과 다름.

---

## 8. ★ 학습 사이클의 자연스러움 — 왔다 갔다 하는 것의 가치

이번 결정의 흐름:

```
1. "creator가 모호하다" (브로 불만)
   → creator_func로 개명 시도 (의미 투명성 추구)
2. "변수명과 타입 힌트 중복이다" (브로 자각)
   → 헝가리안 냄새 자각
3. 현대 파이썬 철학 학습
   → "이름은 역할, 타입은 힌트에 맡긴다"
4. 책 원본 이름(creator)으로 회귀
   → "책이 그렇게 한 건 Pythonic한 선택이었다" 납득
```

★ 핵심: **이 왔다 갔다 자체가 학습 가치**.
- 그냥 책을 따라갔으면 "왜 creator지?" 의문만 남았을 것
- 개명 시도 + 철회를 거치며 **"왜 Pythonic한가"** 깊이 이해
- 결과적으로 책 원본으로 돌아가지만, **이유를 아는 상태**로 돌아감

→ 브로 학습 스타일("쌩짜 재현 ❌, 이해 + 변형/개선 시도 ✅")의 정수.
  실험하고, 자각하고, 원칙을 발견하는 과정 자체가 rezero 프로젝트의 존재 이유.

---

## 9. 🔓 더 파고 싶으면 (확장 후보)

| 주제 | 키워드 | 방향 |
|---|---|---|
| **Apps Hungarian** (의미 인코딩) | `unsafe_x`, `validated_input` | Systems Hungarian과의 차이. XSS 방어 코드 등에서 여전히 유효 |
| **타입 힌트와 IDE 협력** | hover, jump-to-def | 타입 힌트가 가독성에 미치는 영향. "이름에 타입 안 박아도 되는 이유" |
| **domain-driven 네이밍** | bounded context, ubiquitous language | "역할"의 깊은 의미. 도메인 지식이 이름에 어떻 스며드는가 |
| **변수명 길이와 스코프** | 짧은 이름(루프 변수 i,j) vs 긴 이름(전역) | 스코프가 좁을수록 짧은 이름 허용. 라인 수와 이름 길이의 관계 |

### 회수 시그널

- 다른 step에서 "이 변수명 타입 같은 느낌인데?" → 본 노트 §3, §5 복습
- 프레임워크 코드 읽다 네이밍 패턴 발견 → §6 사례 비교에 추가

---

## 🔑 핵심 키워드

`#네이밍` `#naming` `#헝가리안` `#hungarian-notation` `#Systems-Hungarian` `#Apps-Hungarian` `#파이써닉` `#pythonic` `#타입힌트` `#type-hints` `#역할인코딩` `#타입인코딩` `#PEP8` `#변수명` `#크로스참조` `#creator` `#step16파생` `#시도철회` `#학습사이클`

## 📝 학습 완료일 / 관련 링크

- **완료일**: 2026-07-31 (step16 진행 중)
- **트리거**: step16 크로스 참조 네이밍 개명 시도 → 브로 "중복 느낌" 자각
- **결정**: REZERO_CHANGES 항목 025 (시도/철회 이력)
- **LEARNING_NOTES**: step16 "현대 Pythonic 네이밍" 통찰
- **관련 코드**: rezero/steps/step16.py (Variable/Function 속성)
- **관련 항목**: REZERO_CHANGES 항목 002 (`input` → `input_var`, 충돌 회피 예외 케이스)
