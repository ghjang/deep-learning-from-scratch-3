"""rezero.v2.functions — 구체 함수들 (Square/Add/Mul/Neg/Sub/Div/Pow/Sin/Cos + wrapper).

rezero v2 스코프의 구체 함수 모음.
core.Function을 상속해 apply + derivative hook 구현.

★ derivative hook 패턴 — 스칼라 출력 가정:
    부모 Function.backward가 chain rule fold step 일반화.
    자식은 apply(순수 수학) + derivative(도함수 hook)만 구현.

★ v2 (step32): derivative가 Variable를 받는다 — 도함수 본문의 연산이
    Variable 연산이 되어, create_graph 컨텍스트에서 그래프를 남긴다.
    본문 코드는 v1과 거의 동일 (연산자 오버로딩이 ndarray → Variable 전환을
    자동 처리) — 달라진 건 "흐르는 데이터의 타입"뿐.

    복잡도 순 (★ = v2에서 실제 수정 발생):
    - Neg: lambda x: -1.0 * x                (단일, 단항. ★ np.float64 제거)
    - Add: (lambda _: 1, lambda _: 1)         (다변, 상수 — 그대로)
    - Sub: (lambda _: 1, lambda _: -1)        (다변, Add 변형 — 그대로)
    - Mul: (lambda _: x1, lambda _: x0)       (다변, ★ inputs에서 Variable 꺼내기)
    - Div: (lambda _: 1/x1, lambda _: -x0/x1**2)  (★ Variable 꺼내기)
    - Pow: lambda x: self.c * x**(self.c-1)   (단일, 그대로 — __pow__/__rmul__ 활용)
    - Sin: lambda x: cos(x)                   (★ np.cos → cos 함수 — Cos로 연결)
    - Cos: lambda x: -sin(x)                  (step32 신규 — sin의 고차 미분용)
"""

from typing import override

import numpy as np

from rezero.v2.core import DerivativeFn, Function, Variable


# ===== 구체 함수 클래스 =========================================================
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> DerivativeFn:
        # 본문은 v1과 동일 — x가 Variable이 되면 2 * x는 x.__rmul__ → mul() 호출.
        return lambda x: 2 * x


class Add(Function):
    """덧셈: (x0, x1) → x0 + x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        # 상수 1은 float 반환 — backward에서 1 * upstream 시 __rmul__로 Variable화.
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """곱셈: (x0, x1) → x0 * x1. 미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        # ★ v2: .data를 꺼내지 않고 Variable 그대로 — gx가 그래프를 가진다.
        #   (v1: x1 = self.inputs[1].data — ndarray라 그래프 연결 상실)
        x0 = self.inputs[0]
        x1 = self.inputs[1]
        return (lambda _: x1, lambda _: x0)


class Neg(Function):
    """단항 부호: x → -x. 미분: f'(x) = -1."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> DerivativeFn:
        # ★ v2: np.float64 제거 — float * Variable도 __rmul__로 처리되고,
        #   Variable 그래프가 유지됨 (np.float64가 좌변이면 NumPy가 개입 위험).
        return lambda x: -1.0 * x


class Sub(Function):
    """뺄셈: (x0, x1) → x0 - x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = -1. 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 - x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        return (lambda _: 1, lambda _: -1)


class Div(Function):
    """나눗셈: (x0, x1) → x0 / x1. 미분: ∂y/∂x0 = 1/x1, ∂y/∂x1 = -x0/x1². 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 / x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        # ★ v2: Variable 그대로 — 1/x1은 __rtruediv__, x1**2는 __pow__,
        #   -x0는 __neg__ → 전부 Variable 연산으로 그래프 생성.
        x0 = self.inputs[0]
        x1 = self.inputs[1]
        return (lambda _: 1 / x1, lambda _: -x0 / x1 ** 2)


class Pow(Function):
    """거듭제곱: x → x**c. 미분: f'(x) = c·x^(c-1).

    c는 상수 (Variable 아님, 미분 대상 아님).
    __init__(c)에서 c 저장, apply/derivative에서 self.c 참조.
    """

    def __init__(self, c: "int | float") -> None:
        self.c = c                     # 커스텀 — c만 이 클래스에서 저장
        super().__init__()             # inputs/output/generation은 부모가 초기화

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** self.c

    @override
    def derivative(self) -> DerivativeFn:
        # 본문 그대로 — c * x**(c-1)이 Variable 연산으로 자동 전환.
        c = self.c
        return lambda x: c * x ** (c - 1)

    @override
    def dot_label(self, show_param: bool = False) -> str:
        return f'Pow(c={self.c})' if show_param else 'Pow'


class Sin(Function):
    """사인: x → sin(x). 미분: f'(x) = cos(x).

    step27에서 v1 첫 수학 함수로 추가. ★ v2: derivative가 cos **함수**를
    호출 (np.cos가 아니라) — Variable 세계에서 그래프가 연결된다.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.sin(x)

    @override
    def derivative(self) -> DerivativeFn:
        return lambda x: cos(x)


class Cos(Function):
    """코사인: x → cos(x). 미분: f'(x) = -sin(x).

    ★ step32 신규 — Sin의 고차 미분을 위한 함수. sin의 1차 미분이 cos이므로,
    2차 미분(sin''= -sin)까지 그래프를 타고 내려가려면 cos가 Variable 연산이어야 함.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.cos(x)

    @override
    def derivative(self) -> DerivativeFn:
        return lambda x: -sin(x)


# ===== wrapper 함수 ============================================================
# wrapper는 단순하게 (Function.__call__ 도입부의 as_variable이 변환 처리).
def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


def add(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """덧셈 wrapper. x1은 Variable/ndarray/scalar 모두 가능."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """곱셈 wrapper."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def neg(x: Variable) -> Variable:
    """단항 부호 wrapper: -x."""
    result = Neg()(x)
    assert isinstance(result, Variable), "Neg는 단일 출력이므로 Variable이어야 함"
    return result


def sub(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """뺄셈 wrapper: x0 - x1."""
    result = Sub()(x0, x1)
    assert isinstance(result, Variable), "Sub는 단일 출력이므로 Variable이어야 함"
    return result


def rsub(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """역순 뺄셈 wrapper: x1 - x0 (비교환 → 순서 뒤집기).

    `2.0 - x` → Python이 x.__rsub__(2.0) 호출 → rsub(x, 2.0) → Sub()(2.0, x).
    """
    result = Sub()(x1, x0)
    assert isinstance(result, Variable), "rsub는 단일 출력이므로 Variable이어야 함"
    return result


def div(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """나눗셈 wrapper: x0 / x1."""
    result = Div()(x0, x1)
    assert isinstance(result, Variable), "Div는 단일 출력이므로 Variable이어야 함"
    return result


def rdiv(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """역순 나눗셈 wrapper: x1 / x0 (비교환 → 순서 뒤집기).

    `3.0 / x` → Python이 x.__rtruediv__(3.0) 호출 → rdiv(x, 3.0) → Div()(3.0, x).
    """
    result = Div()(x1, x0)
    assert isinstance(result, Variable), "rdiv는 단일 출력이므로 Variable이어야 함"
    return result


def pow(x: Variable, c: "int | float") -> Variable:
    """거듭제곱 wrapper: x ** c. c는 상수 (Variable 아님)."""
    result = Pow(c)(x)
    assert isinstance(result, Variable), "Pow는 단일 출력이므로 Variable이어야 함"
    return result


def sin(x: Variable) -> Variable:
    """사인 wrapper: sin(x)."""
    result = Sin()(x)
    assert isinstance(result, Variable), "Sin은 단일 출력이므로 Variable이어야 함"
    return result


def cos(x: Variable) -> Variable:
    """코사인 wrapper: cos(x). ★ step32 신규 — Sin 고차 미분용."""
    result = Cos()(x)
    assert isinstance(result, Variable), "Cos는 단일 출력이므로 Variable이어야 함"
    return result
