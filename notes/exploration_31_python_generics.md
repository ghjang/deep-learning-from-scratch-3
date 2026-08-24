# 탐구 31 — Python 제네릭: 타입 변수, Protocol, 그리고 반공변 사건

> **시점**: step32 직후 (2026-08-24)
> **상태**: ✅ 완료 (Pylance 96 errors 사건의 해결 과정에서 실전 습득)
> **트리거**: 브로 질문 — "우리 거 파이썬 제네릭 문법에 대해서 다룬 적 있나?"
> + 그 전에 브로가 VSCode에서 발견한 Pylance 오류 다발 (96 errors) — 그중 핵심이
> **반공변**(contravariance) 오류였고, 해결책이 제네릭(TypeVar)이었다.

## 📌 왜 이 탐구를 했나

step32에서 v2 브랜칭 + common 모듈을 만들며 `numerical_diff`를
`Callable[[VariableLike], VariableLike]` 시그니처로 옮겼더니 Pylance가 반발했다:

```
Argument of type "(x: Variable) -> Variable" cannot be assigned to parameter "f"
of type "(VariableLike) -> VariableLike"
```

이걸 해결하며 배운 제네릭 문법(TypeVar / Protocol / bound)을 정리.
기존 노트들(탐구 05의 typing 표, 탐구 06의 구조적 타이핑 철학)이 스치기만 한
빈 칸을 메우는 노트 — **전부 우리 코드에서 실제로 쓴 것만** 다룬다.

---

## 1. 타입 별칭 — `type X = ...` (Python 3.12 문법)

가장 가벼운 것부터. 긴 타입에 이름 붙이기:

```python
type Worklist = list["Function"]                                    # v1 core (step16~)
type DerivativeFn = Callable[["Variable"], "Variable | float"]     # v2 core (step32)
```

- 3.12의 `type` **문(statement)**. 예전 `Worklist = TypeAlias` 대비 깔끔
- 게으른 평가(lazy)라 전방 참조 문자열(`"Function"`)과 잘 맞음
- 런타임 영향 0 — pyright/Pylance만 읽는 **주석의 고급 형태**

## 2. TypeVar — "타입을 나중에 정하는 변수"

제네릭의 핵심. 함수가 **"같은 타입이라면"** 을 표현할 때 쓴다:

```python
VariableT = TypeVar("VariableT", bound=VariableLike)

def numerical_diff(
    f: Callable[[VariableT], VariableT],
    x: VariableT,
    eps: float = 1e-4,
) -> np.ndarray: ...
```

읽는 법: "어떤 타입 VariableT에 대해 — f는 VariableT를 먹고 VariableT를 뱉고,
x는 VariableT다". `numerical_diff(square, v1_Variable)`로 부르면 VariableT =
v1.Variable로 **호출부에서 결정**되고, `numerical_diff(cos, v2_Variable)`면
v2.Variable이 된다. common이 어느 버전도 import하지 않는 비결.

- `bound=VariableLike`: VariableT의 상한 — "최소한 이 모양은 갖춰야 한다"
- 리스트의 `list[T]`가 T를 채우는 것과 같은 원리 (list가 제네릭 클래스)

## 3. 반공변 사건 — 왜 그냥은 안 됐나

원래 시그니처는 이랬다:

```python
def numerical_diff(f: Callable[[VariableLike], VariableLike], x: VariableLike): ...
```

이때 `numerical_diff(square, x)` (square는 `Callable[[Variable], Variable]`)를
부르면 Pylance가 거부한다. 이유 — **함수 매개변수는 반공변(반대 방향)**:

| 위치 | 방향 | 의미 |
|---|---|---|
| 매개변수(parameter) | **반공변** | f가 받아들일 수 있는 타입은 **넓어도** OK (슈퍼타입) |
| 반환값(return) | 공변 | f가 반환하는 타입은 **좁아도** OK (서브타입) |

`square`는 Variable**만** 받는데, 시그니처는 "임의의 VariableLike를 받을
함수"를 요구 — VariableLike(넓음)를 Variable(좁음)에 못 넣는다. 즉
**호출부에서 VariableLike가 들어올 수 있는데 square는 처리를 못 할 수 있다**는
잠재 위반이다. (ArrayLike/Iterable 같은 표준 라이브러리 시그니처가 늘
`Callable[[T], T]` 꼴인 이유.)

**TypeVar가 해결책인 이유**: f와 x를 **같은 타입 변수로 묶으면** "넓냐 좁냐"
비교 자체가 사라진다 — 호출부에서 T가 한 번에 결정되므로 f와 x가 항상 정확히
맞기 때문. 반공변은 "서로 다른 타입끼리의 방향" 문제이고, 제네릭은 "같은
타입임을 보장"으로 문제를 없앤다.

## 4. Protocol과의 결합 — 구조적 타이핑 + 제네릭

`bound=VariableLike`의 VariableLike는 Protocol (탐구 06에서 배운 구조적 타이핑):

```python
class VariableLike(Protocol):
    data: Optional[np.ndarray]

    def __init__(self, data: Optional[np.ndarray]) -> None: ...
```

- v1.Variable도 v2.Variable도 **상속 없이** 이 모양이면 통과 (구조적 타이핑)
- ★ `__init__`을 선언한 이유: 함수 안에서 `type(x)(...)` 생성자 호출의 시그니처를
  정적 분석에 알려주기 위함 — 없으면 "Expected 0 positional arguments" 오탐.
  Protocol은 속성/메서드뿐 아니라 **생성자 계약**도 표현할 수 있다는 실전 팁.

### "인터페이스 같은 느낌" — 맞다, 그리고 두 진영 (브로 질문에서 도출)

계약을 정의한다는 **목적**은 인터페이스와 같다. 다른 건 **성립 방식**:

| | 명목적 (nominal) | 구조적 (structural) |
|---|---|---|
| 대표 | Java/C# `interface` | Go interface, TypeScript, **Python Protocol** |
| 계약 성립 | `implements` 선언 필요 | **모양만 맞으면 자동 통과** (선언 불필요) |

제네릭 bound와의 결합은 Java와 거의 1:1 평행:

```
Java:    <T extends Comparable<T>>          ← bound가 명목적 인터페이스
Python:  TypeVar("T", bound=VariableLike)   ← bound가 구조적 Protocol
```

런타임 차이도 하나: Java/Go 인터페이스는 런타임에 존재 (instanceof 등),
TypeScript/Python Protocol은 정적 분석 후 **소거** (5절 참조).

### 계보 지도 — 덕타이핑 / C++ 템플릿 / Haskell (브로 질문 3연타에서 도출)

"Protocol이 (1) 덕타이핑 (2) C++ 템플릿 (3) Haskell 같은 느낌 아닌가?" —
셋 다 맞는데 **각각 다른 축**에서:

| 비교 대상 | Protocol과 공유 | 갈리는 지점 |
|---|---|---|
| 덕타이핑 | **성립 방식** — 모양 판정, 선언 불필요. PEP 544 공식 용어가 "static duck typing" | 런타임 판정 vs 정적 검사 |
| C++ 템플릿 (+concepts) | **다형성 메커니즘** — 임의 T 한 벌의 코드. concepts는 구조적 제약이라 Protocol+bound와 철학 일치 | 코드 생성 (T마다 여러 벌) vs 소거 (한 벌) |
| Haskell 타입클래스 / Rust trait | **계약+제약 스타일** — `Ord a => ...`의 bound 발상 | 명시 instance 선언 필요 / 런타임 딕셔너리로 실존 |

→ Python Protocol = "덕타이핑의 정적 버전"에 "C++ 템플릿의 소거형"을 얹고
"타입클래스식 계약"을 구조적으로 만든 것 — 세 전통의 교집합적 후손.

## 5. 런타임에는 전부 소거된다

제네릭 전체(별칭/TypeVar/Protocol/bound)는 **런타임에 흔적 없이 사라진다**.
`type(x)(np.asarray(...))`가 실제로 하는 일은 그냥 `Variable(np.asarray(...))` —
타입 인자는 존재조차 안 함. 그래서:

- 성능 비용 0
- 틀려도 실행은 됨 (96 errors가 실행에는 영향 없었던 이유)
- 대가: 틀렸는지는 pyright/Pylance가 봐줘야 안다 → **"힌트를 달았으면 계약을
  지켜라"** — 이번 사건의 교훈과 직결

## 6. 우리 코드에서의 제네릭 지도

| 코드 | 제네릭 요소 | 역할 |
|---|---|---|
| `v1/core.py` — `type Worklist` | 타입 별칭 | `list["Function"]`에 이름 |
| `v2/core.py` — `type DerivativeFn` | 타입 별칭 | derivative hook 시그니처 재사용 |
| `common/utils.py` — `VariableT` + `VariableLike` | TypeVar + Protocol + bound | 버전 독립 numerical_diff (반공변 해결) |
| 표준 라이브러리 `list[T]`, `np.ndarray` | 제네릭 클래스 | 우리가 매일 쓰는 소비자 |

다음 단계(아직 안 씀): 제네릭 **클래스** 정의 `class Box(Generic[T])` — v3에서
Parameter/DataLoader 같은 컨테이너가 나오면 자연스럽게 등장할 후보.

---

## 관련 링크

- [탐구 노트 06 — 데이터 타입과 구조적 타이핑](./exploration_06_data_types.md) — Protocol의 철학 (C++ concepts 비교)
- [탐구 노트 05 — 파이썬 객체 모델](./exploration_05_python_object_model.md) — typing 모듈 개관
- `rezero/common/utils.py` — 이 노트의 전부가 실제로 살아있는 코드
- `REZERO_CHANGES.md` 항목 038 — 96 errors 사건 기록

## 키워드

`#제네릭` `#TypeVar` `#type문법-3.12` `#타입별칭` `#Protocol` `#구조적타이핑` `#static-duck-typing` `#bound` `#반공변` `#공변` `#변성` `#Callable매개변수반공변` `#런타임소거` `#제네릭은계약` `#Worklist` `#DerivativeFn` `#VariableLike` `#common모듈` `#96errors사건` `#인터페이스두진영` `#C++concepts` `#Haskell타입클래스` `#Rust-trait` `#계보지도`
