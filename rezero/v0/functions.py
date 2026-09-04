"""rezero.v0.functions — 구체 함수들 (NumPy 없는 순수 스칼라 판).

rezero v0 — v1 functions에서 NumPy를 걷어낸 결과.
인벤토리는 v1과 동일 (Square/Add/Mul/Neg/Sub/Div/Pow/Sin) + sin용 Cos.

★ 걷어내기 관찰 포인트:
  - np.sin → math.sin — "배열 함수"가 "스칼라 함수"로 (math는 표준 라이브러리)
  - derivative가 반환하는 것: float 상수 또는 float 계산 — ndarray가 사라져
    타입이 전부 균일해짐 (v1에서의 "ndarray | float" 이중 타입이 여기선 float 하나)
  - 브로드캐스팅이 없음 — `1 * upstream`가 오직 스칼라×스칼라
"""

import math
from collections.abc import Callable
from typing import override

from rezero.v0.core import Function, Variable


# ===== 함수 클래스 =============================================================
class Square(Function):
    """제곱: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: float) -> float:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> Callable[[float], float]:
        return lambda x: 2 * x


class Add(Function):
    """덧셈: (x0, x1) → x0 + x1. 미분: (∂y/∂x0, ∂y/∂x1) = (1, 1)."""

    @override
    def apply(self, x0: float, x1: float) -> float:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> "tuple[Callable[[float], float], ...]":
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """곱셈: (x0, x1) → x0 * x1. 미분: (x1, x0) — 각 입력의 도함수는 형제 값."""

    @override
    def apply(self, x0: float, x1: float) -> float:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> "tuple[Callable[[float], float], ...]":
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        x0, x1 = self.inputs
        d0 = x0.data
        d1 = x1.data
        assert d0 is not None and d1 is not None

        return (lambda _: d1, lambda _: d0)


class Neg(Function):
    """부호 반전: x → -x. 미분: -1 (상수)."""

    @override
    def apply(self, x: float) -> float:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> Callable[[float], float]:
        return lambda _: -1


class Sub(Function):
    """뺄셈: (x0, x1) → x0 - x1. 미분: (1, -1). 비교환."""

    @override
    def apply(self, x0: float, x1: float) -> float:  # type: ignore[override]
        return x0 - x1

    @override
    def derivative(self) -> "tuple[Callable[[float], float], ...]":
        return (lambda _: 1, lambda _: -1)


class Div(Function):
    """나눗셈: (x0, x1) → x0 / x1. 미분: (1/x1, -x0/x1²). 비교환."""

    @override
    def apply(self, x0: float, x1: float) -> float:  # type: ignore[override]
        return x0 / x1

    @override
    def derivative(self) -> "tuple[Callable[[float], float], ...]":
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        x0, x1 = self.inputs
        d0 = x0.data
        d1 = x1.data
        assert d0 is not None and d1 is not None

        return (lambda _: 1 / d1, lambda _: -d0 / d1 ** 2)


class Pow(Function):
    """거듭제곱: x → x**c. 미분: f'(x) = c·x^(c-1). c는 상수 (미분 대상 아님)."""

    def __init__(self, c: "int | float") -> None:
        self.c = c
        super().__init__()

    @override
    def apply(self, x: float) -> float:  # type: ignore[override]
        return x ** self.c

    @override
    def derivative(self) -> Callable[[float], float]:
        c = self.c
        return lambda x: c * x ** (c - 1)

    @override
    def dot_label(self, show_param: bool = False) -> str:
        return f'Pow(c={self.c})' if show_param else 'Pow'


class Sin(Function):
    """사인: x → sin(x). 미분: f'(x) = cos(x) — math.sin (배열 아님, 스칼라)."""

    @override
    def apply(self, x: float) -> float:  # type: ignore[override]
        return math.sin(x)

    @override
    def derivative(self) -> Callable[[float], float]:
        return lambda x: math.cos(x)


class Cos(Function):
    """코사인: x → cos(x). 미분: f'(x) = -sin(x)."""

    @override
    def apply(self, x: float) -> float:  # type: ignore[override]
        return math.cos(x)

    @override
    def derivative(self) -> Callable[[float], float]:
        return lambda x: -math.sin(x)


# ===== wrapper 함수 ===========================================================
def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


def add(x0: Variable, x1: "Variable | float | int") -> Variable:
    """덧셈 wrapper."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: Variable, x1: "Variable | float | int") -> Variable:
    """곱셈 wrapper."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def neg(x: Variable) -> Variable:
    """부호 반전 wrapper."""
    result = Neg()(x)
    assert isinstance(result, Variable), "Neg는 단일 출력이므로 Variable이어야 함"
    return result


def sub(x0: Variable, x1: "Variable | float | int") -> Variable:
    """뺄셈 wrapper."""
    result = Sub()(x0, x1)
    assert isinstance(result, Variable), "Sub는 단일 출력이므로 Variable이어야 함"
    return result


def rsub(x0: Variable, x1: "Variable | float | int") -> Variable:
    """역순 뺄셈 wrapper: x1 - x0."""
    result = Sub()(x1, x0)
    assert isinstance(result, Variable), "rsub는 단일 출력이므로 Variable이어야 함"
    return result


def div(x0: Variable, x1: "Variable | float | int") -> Variable:
    """나눗셈 wrapper."""
    result = Div()(x0, x1)
    assert isinstance(result, Variable), "Div는 단일 출력이므로 Variable이어야 함"
    return result


def rdiv(x0: Variable, x1: "Variable | float | int") -> Variable:
    """역순 나눗셈 wrapper: x1 / x0."""
    result = Div()(x1, x0)
    assert isinstance(result, Variable), "rdiv는 단일 출력이므로 Variable이어야 함"
    return result


def pow(x: Variable, c: "int | float") -> Variable:
    """거듭제곱 wrapper."""
    result = Pow(c)(x)
    assert isinstance(result, Variable), "Pow는 단일 출력이므로 Variable이어야 함"
    return result


def sin(x: Variable) -> Variable:
    """사인 wrapper — math.sin."""
    result = Sin()(x)
    assert isinstance(result, Variable), "Sin은 단일 출력이므로 Variable이어야 함"
    return result


def cos(x: Variable) -> Variable:
    """코사인 wrapper — math.cos (Sin 고차 미분용)."""
    result = Cos()(x)
    assert isinstance(result, Variable), "Cos는 단일 출력이므로 Variable이어야 함"
    return result
