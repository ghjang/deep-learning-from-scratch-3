"""rezero.v1.functions — 구체 함수들 (Square/Add/Mul/Neg/Sub/Div/Pow/Sin + wrapper).

rezero v1 스코프의 구체 함수 모음.
core.Function을 상속해 apply + derivative hook 구현.

★ derivative hook 패턴 — 스칼라 출력 가정:
    부모 Function.backward가 chain rule fold step 일반화.
    자식은 apply(순수 수학) + derivative(도함수 hook)만 구현.

★ 도함수 성분 유형 지도 (작업 4 — 탐구 노트 32 §5 분류를 코드에 반영):
    derivative hook이 "무엇에 의존하는가"로 유형화한 관습 지도.
    4고지(출력형 활성함수 대거 등장) 전의 좌표.

    ① 상수형 (의존 없음)       — Add(1,1), Sub(1,-1), Neg(-1): 인자 무시 (lambda _:)
    ② 입력형 (자기 입력 x)     — Square(2x), Sin(cos), Pow(c·x^(c-1)):
                                "입력의 순수 함수" 관습 준수 — hook 인자만으로 계산
    ③ 다른 입력형 (형제 입력)   — Mul(x1,x0), Div(1/x1, -x0/x1²): ★ 관습 위반 —
                                self.inputs에서 형제를 클로저 캡처. 수학적 필연
                                (곱셈 법칙 자체가 형제 값 요구). v1은 1차 미분
                                스코프라 실해 없음 (v2는 형제를 Variable로 캡처).
    ④ 출력형 (forward 출력 y)   — v1 미등장 (v2의 Tanh부터 — 재호출/재사용 전략)
    ⑤ 입출력형 (x와 y 동시)     — 4고지 예고 (SiLU 등)
"""

from collections.abc import Callable
from typing import override

import numpy as np

from rezero.v1.core import Function, Variable


# ===== 구체 함수 클래스 =========================================================
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Add(Function):
    """덧셈: (x0, x1) → x0 + x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """곱셈: (x0, x1) → x0 * x1. 미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        return (lambda _: x1, lambda _: x0)


class Neg(Function):
    """단항 부호: x → -x. 미분: f'(x) = -1 (상수).

    ★ step34 버그 수정 (2026-08-24): 이전 `lambda x: np.float64(-1.0) * x`는
    도함수(-1 상수)가 아니라 원 함수(-x)를 반환하는 버그였다. y = -x의 미분이
    -x가 되어버림. sin 고차 미분(step34)에서 3차부터 발동해 발견 — v1~v2 공통.
    은신 이유: 기존 테스트는 순전파 값만 검사 (역전파 테스트 부재).
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> Callable[[np.ndarray], "np.ndarray | float"]:
        # 도함수는 상수 -1 (float) — Add의 lambda _: 1과 같은 상수 패턴.
        # 반환 타입에 float 허용 (상수 도함수) — backward에서 ndarray와 곱해짐.
        return lambda _: -1.0


class Sub(Function):
    """뺄셈: (x0, x1) → x0 - x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = -1. 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 - x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        return (lambda _: 1, lambda _: -1)


class Div(Function):
    """나눗셈: (x0, x1) → x0 / x1. 미분: ∂y/∂x0 = 1/x1, ∂y/∂x1 = -x0/x1². 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 / x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        assert x0 is not None and x1 is not None, "inputs' data must not be None"
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
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        c = self.c
        return lambda x: c * x ** (c - 1)

    @override
    def dot_label(self, show_param: bool = False) -> str:
        return f'Pow(c={self.c})' if show_param else 'Pow'


class Sin(Function):
    """사인: x → sin(x). 미분: f'(x) = cos(x).

    v1의 첫 수학 함수 (step27). np.sin/np.cos 사용 — C 구현이라 빠르고 정확.
    책은 backward를 직접 구현하지만, rezero는 derivative hook 한 줄로 끝
    (chain rule 곱셈은 부모 Function.backward가 담당).
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.sin(x)

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: np.cos(x)


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
