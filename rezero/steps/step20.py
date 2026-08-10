"""
rezero.steps.step20 — [2고지] 연산자 오버로드(1)
===============================================

★ 책 공식 제목 "연산자 오버로드(1)". 여기서 "오버로드" = 연산자 오버로딩(operator overloading).
  파이썬 매직메서드(__add__, __mul__)로 `+`, `*` 연산자를 가로채서 Variable에 적용.

★ 2고지 "자연스러운 코드로"의 핵심 달성:
  이전까지: y = add(mul(a, b), c)   ← 함수 호출 중첩, 수학 식과 달라 어색
  step20:   y = a * b + c            ← 수학 식처럼 자연스러움 ★

이 step에서 배울 것:
  - `Mul` 클래스 — 곱셈 함수 (x0, x1) → x0 * x1
  - `mul(x0, x1)` wrapper — Mul 인스턴스 생성 + 호출
  - `Variable.__add__` / `Variable.__mul__` — `+`, `*` 연산자 가로채기

★★★ 핵심 1 — 파이썬 데이터 모델 (연산자 내부 동작):
  `a + b` 는 사실 `a.__add__(b)` 로 해석됨.
  `a * b` 는 `a.__mul__(b)`.
  즉 연산자(`+`, `*`)는 매직메서드의 **신택스 슈가(syntactic sugar)**.
  → 클래스에 __add__/__mul__ 정의하면 그 클래스의 객체에 `+`/`*` 연산자 사용 가능.

  ★ __add__ 호출 규칙:
    `a + b` → Python이 먼저 `a.__add__(b)` 시도.
    → a의 타입이 __add__ 없거나 NotImplemented 반환 시, `b.__radd__(a)` 시도 (역순).
    → 둘 다 없으면 TypeError.
    ★ step20은 "첫 번째 피연산자가 Variable"인 케이스만 고려. `1 + a` (역순)은 step21+ 화두.

★★★ 핵심 2 — 매직메서드 위치: "클래스 안 정의" vs "클래스 밖 대입":

  방식 A (일반적 — 우리 채택):
    ```python
    class Variable:
        def __add__(self, other): return add(self, other)
    ```
    장점: 클래스 정의만 보고 지원 연산자 파악 가능, IDE/Pylance 자동완성 지원.

  방식 B (책 원본 방식 — 클래스 밖 대입):
    ```python
    class Variable: ...
    def add(x0, x1): ...
    Variable.__add__ = add      # 클래스 정의 밖에서 대입
    ```
    파이썬에선 클래스도 객체라 속성(메서드 포함)을 밖에서 대입 가능.
    두 방식은 **기능적으로 완전히 동일**.

  ★ 왜 책이 방식 B를 택했나 (가설):
    1. wrapper(add/mul)를 먼저 정의한 뒤 연결하는 순서가 자연스러워서
    2. "함수 → 연산자" 연결을 분리해 보여주려는 설명 목적
  ★ 언제 "클래스 안"이 (사실상) 필수인가:
    - IDE/Pylance 정적 분석 지원 (클래스 밖 대입은 Pylance가 인식 못 함)
    - 서브클래싱 시 super().__add__() 패턴이 자연스러움
    - "이 클래스가 지원하는 연산자"를 클래스 정의만 보고 파악 가능
  → 우리는 방식 A(클래스 안)로 본체 구현, 데모에서 방식 B도 동일 동작함을 시연.

★★★ 핵심 3 — Mul의 derivative hook (★ 항목 013 재평가 첫 테스트):
  Mul: (x0, x1) → x0 * x1
  미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0

  ★ Add(step13)와의 차이 — "다른 입력값에 의존" 케이스:
    - Add: 편도함수가 둘 다 1 (상수함수). 입력값 안 봄.
    - Mul: 편도함수가 **다른 입력값**. x0의 편도함수 = x1, x1의 편도함수 = x0.
    → derivative() 안에서 self.inputs를 참조해야 함. rezero 정체성(항목 013) 유지 가능?

  ★ 해법 — self.inputs를 capture(닫아넣는, closure)하는 lambda:
    ```python
    class Mul(Function):
        def derivative(self):
            x0 = self.inputs[0].data    # ★ self.inputs 참조
            x1 = self.inputs[1].data
            return (lambda _: x1, lambda _: x0)   # 상수함수 형태 (입력 무시)
    ```
    핵심: 편도함수값이 상수(1)가 아니라 "다른 입력값"이지만, **derivative() 호출 시점에 이미 값이 고정**되므로
    상수함수(lambda _: x1)로 표현 가능. 브로 통찰(Add 상수함수)의 자연스러운 확장.
    ★ derivative hook은 이 케이스까지 커버 — 항목 013 "최종 반영 여부 보류" 첫 재평가 통과.
    행렬 미분(step34+)에서 야코비안 전치 곱이 필요해지면 그때 재평가.

★ 이 코드의 가정/전제 (step19 전제 + step20 새 전제):
  step14~19 누적 전제 + 새 전제:

  | 새 전제 (step20)                                     | 의미                                              | 깨지면?                                       |
  |-----------------------------------------------------|---------------------------------------------------|-----------------------------------------------|
  | **연산자 양변은 모두 Variable** (현재 단계)           | `a + b`서 a, b 둘 다 Variable. `a + 1` 안 됨       | ndarray/scalar와 연산 시 TypeError (step21 화두) |
  | **매직메서드는 첫 번째 피연산자의 메서드로 호출**      | `a + b` → `a.__add__(b)`. `1 + a` → int의 __add__ | 오른쪽이 Variable 아닌 경우 (나중에 __radd__)     |

★★★ rezero 변형 포인트:
  | # | 포인트                    | 책 방식                | 우리 방향                                       |
  |---|--------------------------|------------------------|-------------------------------------------------|
  | A | __add__/__mul__ 위치     | 클래스 밖에서 대입      | ★ 클래스 안에 정의 (IDE/정적 분석 친화적)         |
  | B | Mul 클래스               | forward/backward 직접  | ★ 우리 패턴(apply/derivative hook) 유지          |
  | C | __add__/__mul__ 내부     | wrapper 호출           | 동일 (wrapper 두는 패턴 유지)                    |

참고 자료:
  - 원본 구현: steps/step20.py
  - 이전 step: rezero/steps/step19.py (변수 사용성 개선 — 이번에 연산자 오버로딩 추가)
  - 이슈: #25 (step20 진행 추적)
  - rezero 변형: REZERO_CHANGES 항목 013 (derivative hook — Mul로 첫 재평가 통과)

검증 포인트:
  - a=3.0, b=2.0, c=1.0 (Variable)
  - y = a * b + c = (3*2) + 1 = 7.0
  - a.grad = 2.0 (∂y/∂a = b), b.grad = 3.0 (∂y/∂b = a), c.grad = 1.0 (∂y/∂c = 1)

실행:
  uv run python rezero/steps/step20.py
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator
from typing import Optional, override

import numpy as np


# ★★★ step18 유지 — Config 전역 설정 + no_grad 컨텍스트 매니저 ---------------------
class Config:
    """★ step18 — 전역 설정 (역전파 on/off 플래그). 이번 step20은 그대로 유지."""
    enable_backprop: bool = True


@contextlib.contextmanager
def using_config(name: str, value: object) -> Generator[None, None, None]:
    """★ step18 — Config 속성을 일시적으로 변경하는 컨텍스트 매니저."""
    old_value = getattr(Config, name)
    setattr(Config, name, value)

    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad() -> contextlib._GeneratorContextManager[None]:
    """★ step18 — 역전파 끄기 사용자 인터페이스. PyTorch torch.no_grad()와 동일 패턴."""
    return using_config('enable_backprop', False)


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


# ★★★ step19 유지 + step20 핵심 추가 (연산자 오버로딩) — Variable -------------------
class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    ★ step19 추가: name 속성 + __len__/__repr__ 매직메서드 + shape/ndim/size/dtype property.
    ★ step20 추가: __add__/__mul__ 매직메서드 — 연산자 오버로딩 (+, *).

      역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
    """

    def __init__(self, data: Optional[np.ndarray], *, name: Optional[str] = None):
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.name: Optional[str] = name
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    # ===== step19: data에 위임하는 property 4종 + __len__ ==================
    def _ensure_data(self) -> np.ndarray:
        """data가 None이면 RuntimeError, 아니면 data 반환. step19 방어막."""
        if self.data is None:
            raise RuntimeError(
                f"{self!r}의 data가 None입니다 — data에 접근하는 연산(shape/len/dtype 등)을 수행할 수 없습니다."
            )
        return self.data

    @property
    def shape(self) -> tuple[int, ...]:
        return self._ensure_data().shape

    @property
    def ndim(self) -> int:
        return self._ensure_data().ndim

    @property
    def size(self) -> int:
        return self._ensure_data().size

    @property
    def dtype(self) -> np.dtype:
        return self._ensure_data().dtype

    def __len__(self) -> int:
        return len(self._ensure_data())

    def __repr__(self) -> str:
        if self.data is None:
            return 'Variable(None)'
        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'Variable(' + p + ')'

    # ===== step20: 연산자 오버로딩 (+, *) ==================================
    # ★ __add__/__mul__을 클래스 안에 정의 (일반적/권장 방식).
    #   본문에서 add/mul wrapper 호출 — 이들은 클래스 정의 **뒤에** 정의되지만,
    #   메서드 본문은 호출 시점에 평가되므로 실행 시엔 이미 정의되어 있음. 문제 없음.
    #   (pyright도 모듈 전체 분석이라 add/mul을 찾음 — 전방 참조 경고 안 남)
    #
    # ★★ "클래스 밖 대입" 방식도 존재하지만 비권장 (★ 작업 원칙 — coding_style.md 참조):
    #   책 원본 step20은 `Variable.__add__ = add` 식으로 클래스 정의 **밖에서** 대입.
    #   파이썬은 클래스도 객체라 속성 대입이 가능하므로 런타임 동작은 동일함.
    #   그러나 정적 분석기(pyright/Pylance)가 클래스 밖 대입을 인식 못 함 →
    #   "Variable에 __add__ 없음" 에러 + 11곳 type: ignore 필요 → 비생산적.
    #   게다가 "이 클래스가 지원하는 연산자"를 클래스 정의만 보고 파악하려면
    #   클래스 안에 정의하는 게 압도적으로 가독성 좋음.
    #   → 따라서 rezero는 클래스 안 정의가 기본 (★ coding_style.md 항목 7).
    def __add__(self, other: "Variable") -> "Variable":
        """+ 연산자 오버로딩. add wrapper에 위임."""
        return add(self, other)

    def __mul__(self, other: "Variable") -> "Variable":
        """* 연산자 오버로딩. mul wrapper에 위임."""
        return mul(self, other)

    # ===== step07~18: 그래프 연결 (변경 없음) =============================
    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021 (cleargrad → clear_grad)."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. step18 Config.enable_backprop으로 그래프 구축 조건부.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: Variable) -> Variable:
        xs = []
        for x in inputs:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)

        assert len(ys) == 1, f"step13~20은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            output.set_creator(self)
            self.inputs = inputs
            self.output = weakref.ref(output)

        return output

    # ===== 순전파 계열 (step11~18과 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출)."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13~18과 동일 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출)."""
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        partials = self.derivative()
        if not isinstance(partials, tuple):
            partials = (partials,)

        downstream_grads = []
        for x, df in zip(self.inputs, partials):
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

            local_deriv = df(x.data)
            downstream_grads.append(local_deriv * upstream_grad)

        return tuple(downstream_grads)

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. 단일 OR 튜플 자유 (부모에서 정규화)."""
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 (step13 Add 유지 + step20 Mul 신규) =====
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. ★ 다입력 함수.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1 (각 편도함수 = 상수함수, 브로 통찰).
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """★ step20 신규 — 곱셈 함수: (x0, x1) → x0 * x1.

    미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0.
    ★ 항목 013 재평가 첫 테스트 케이스 — "다른 입력값에 의존"하는 편도함수.
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        # ★ 항목 013 재평가 통과 — Mul의 편도함수는 "다른 입력값"에 의존하지만
        #   derivative() 호출 시점에 이미 값이 고정되므로 상수함수로 표현 가능.
        #   - Add: (lambda _: 1, lambda _: 1)  — 입력 무시, 상수 1
        #   - Mul: (lambda _: x1, lambda _: x0) — 입력 무시, 다른 입력값(x1/x0)을 캡처
        #   브로 통찰(Add 상수함수)의 자연스러운 확장. derivative hook 유지.
        # ★ assert는 정적 분석(pyright)용 타입 좁히기 — 부모 backward()에서도 같은 가드가
        #   있어 런타임엔 중복이지만, pyright가 Mul.derivative() 안에서 self.inputs가
        #   Optional임을 좁히려면 이 지점에서 다시 한번 가드가 필요.
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        return (lambda _: x1, lambda _: x0)


# ===== wrapper 함수 (step12 스타일 + step20 mul 신규) =====
def add(x0: Variable, x1: Variable) -> Variable:
    """덧셈 wrapper."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: Variable, x1: Variable) -> Variable:
    """★ step20 신규 — 곱셈 wrapper."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


# ★★★ step20 핵심 — 연산자 오버로딩은 Variable 클래스 안에 정의됨 (위쪽) ============
# ★ cf. 책 원본 step20은 클래스 밖에서 대입하는 방식 사용:
#     Variable.__add__ = add
#     Variable.__mul__ = mul
#   파이썬은 클래스도 객체라 속성 대입이 가능하므로 런타임 동작은 동일하지만,
#   정적 분석기(pyright/Pylance)가 인식 못 함 → type: ignore 남발해야 함 → 비권장.
#   rezero는 클래스 안 정의 기본 (★ coding_style.md 작업 원칙 — "매직메서드는 클래스 안에").


# ★★★ step18 유지 — fill_grad 전역 함수 (retain_grad 매개변수 포함) ----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step18 retain_grad 매개변수 유지.

    ★ rezero 변형 (항목 014 유지): 책은 Variable.backward(retain_grad) 메서드.
      우리는 fill_grad(start_var, retain_grad) 전역 함수. 정체성 유지.
    """
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        if start_var.data is None:
            raise RuntimeError(f"{start_var!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")
        start_var.grad = np.ones_like(start_var.data)

    worklist: Worklist = []
    visited: set[Function] = set()

    def schedule(f: Function) -> None:
        if f not in visited:
            worklist.append(f)
            visited.add(f)
            worklist.sort(key=lambda func: func.generation)

    schedule(start_var.creator)

    while worklist:
        f = worklist.pop()

        assert f.inputs is not None, "f.inputs must be set"
        assert f.output is not None, "f.output must be set"

        output = f.output()
        if output is None:
            raise RuntimeError(
                f"{f!r}의 output Variable이 이미 회수되었습니다 — 역전파에 사용할 수 없습니다. "
                "역전파 대상 Variable을 사용자가 참조하고 있는지 확인하세요."
            )

        upstream = output.grad
        assert upstream is not None, "output.grad must be filled"

        downstream_grads = f.backward(upstream)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)

        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

            if x.creator is not None:
                schedule(x.creator)

        if not retain_grad:
            output.grad = None


# --- 데모: step20 연산자 오버로딩 효과 검증 ----------------------------------------
if __name__ == "__main__":
    print("=== step20 연산자 오버로드(1) 데모 ===")
    print()

    # --- 케이스 1: 핵심 — 수학 식처럼 자연스럽게! ---
    print("[1] 핵심: 수학 식처럼 자연스럽게 — y = a * b + c")
    print("    (이전까지: y = add(mul(a, b), c) — 함수 호출 중첩)")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    c = Variable(np.array(1.0))

    y = a * b + c                          # ★ 수학 식처럼!
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 7.0 = (3*2)+1)")
    print(f"    a.grad = {a.grad}  (기대: 2.0 = ∂y/∂a = b)")
    print(f"    b.grad = {b.grad}  (기대: 3.0 = ∂y/∂b = a)")
    print(f"    c.grad = {c.grad}  (기대: 1.0 = ∂y/∂c, Add 미분)")
    print()

    # --- 케이스 2: 복잡한 식 — 연산자 우선순위 적용되는지 확인 ---
    print("[2] 복잡한 식 — y = a * b + c * a  (같은 Variable 재사용, 누적 gradient)")
    print("    (파이썬 연산자 우선순위: *가 +보다 먼저. 오버로딩과 무관하게 언어 스펙 고정)")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    c = Variable(np.array(1.0))

    y = a * b + c * a                      # (a*b) + (c*a) = 6 + 3 = 9. a 두 번 사용!
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 9.0 = (3*2)+(1*3))")
    print(f"    a.grad = {a.grad}  (기대: 3.0 = b + c = 2+1, 두 경로 누적)")
    print(f"    b.grad = {b.grad}  (기대: 3.0 = a)")
    print(f"    c.grad = {c.grad}  (기대: 3.0 = a)")
    print()

    # --- 케이스 3: 연산자 vs wrapper — 동일 동작 확인 ---
    print("[3] 연산자 vs wrapper — a * b == mul(a, b) 동일 동작 확인")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    y1 = a * b                             # 연산자
    y2 = mul(a, b)                         # wrapper
    print(f"    a * b       = {y1.data}  (연산자)")
    print(f"    mul(a, b)   = {y2.data}  (wrapper)  → 동일")
    print()

    # --- 케이스 4: 매직메서드 직접 호출 — a + b == a.__add__(b) ---
    print("[4] 매직메서드 직접 호출 — a + b == a.__add__(b) 동일")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    y1 = a + b                             # 연산자 (신택스 슈가)
    y2 = a.__add__(b)                      # 매직메서드 직접 호출
    print(f"    a + b           = {y1.data}")
    print(f"    a.__add__(b)    = {y2.data}  → 동일")
    print(f"    (즉 '+' 연산자는 __add__ 매직메서드의 신택스 슈가)")
    print()

    # --- 케이스 5: Mul의 derivative hook (★ 항목 013 재평가) ---
    print("[5] Mul derivative hook — 항목 013 재평가 (다른 입력값 의존 케이스)")
    print("    Mul: ∂y/∂x0 = x1, ∂y/∂x1 = x0  (Add와 달리 입력값에 의존)")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    y = a * b
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 6.0 = 3*2)")
    print(f"    a.grad = {a.grad}  (기대: 2.0 = b)")
    print(f"    b.grad = {b.grad}  (기대: 3.0 = a)")
    print(f"    → derivative hook (lambda _: x1, lambda _: x0) 정상 동작 ★")
    print()

    print("=== step20 완료 — 연산자 오버로딩으로 수학 식처럼 자연스러운 코드 ===")
