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

★ 도함수 성분 유형 지도 (작업 4 — 탐구 노트 32 §5 분류를 코드에 반영):
    derivative hook이 "무엇에 의존하는가"로 유형화한 관습 지도.
    4고지(출력형 활성함수 sigmoid/relu 등 대거 등장) 전의 좌표.

    ① 상수형 (의존 없음)       — Add(1,1), Sub(1,-1), Neg(-1): 인자 무시 (lambda _:)
    ② 입력형 (자기 입력 x)     — Square(2x), Sin(cos), Cos(-sin), Pow(c·x^(c-1)):
                                "입력의 순수 함수" 관습 준수 — hook 인자만으로 계산
    ③ 다른 입력형 (형제 입력)   — Mul(x1,x0), Div(1/x1, -x0/x1²): ★ 관습 위반 —
                                self.inputs에서 형제를 클로저 캡처. 수학적 필연
                                (곱셈 법칙 자체가 형제 값 요구). v2에선 형제도
                                그래프에 있어 2차 미분 자동 연결 — 실해는 없음.
    ④ 출력형 (forward 출력 y)   — Tanh: 미분식 1-y². 구현 2전략 (Config.reuse_output)
                                — 재호출(1-tanh(x)², 관습 준수) / 재사용(1-y·y,
                                self.output 참조). y가 weakref로 소멸 가능해 유일하게
                                "전략 선택"이 필요한 유형.
    ⑤ 입출력형 (x와 y 동시)     — 미등장 (4고지 예고 — SiLU 등)
"""

from typing import override

import numpy as np

from rezero.v2.core import Config, DerivativeFn, Function, Variable


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
    """단항 부호: x → -x. 미분: f'(x) = -1 (상수).

    ★ step34 버그 수정 (2026-08-24): v1부터 `lambda x: -1.0 * x`였는데 이는
    도함수(-1)가 아니라 원 함수(-x) 반환 — y=-x의 미분이 -x가 되는 버그.
    sin 고차 미분 3차부터 발동 (Neg.backward 첫 호출 시점)해 발견.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> DerivativeFn:
        # 도함수는 상수 -1 (float) — backward에서 -1.0 * upstream → __rmul__.
        return lambda _: -1.0


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


class Tanh(Function):
    """하이퍼볼릭 탄젠트: x → tanh(x). 미분: f'(x) = 1 - tanh(x)².

    ★ step35 신규 — 도함수가 **자기 자신을 참조**하는 특이 구조.
    4고지 신경망 활성함수 예습이기도 함.

    ★ derivative 구현 전략 2종 (Config.reuse_output — 브로 제안, step18 철학 계승):
    - False (기본): tanh(x) **재호출** — 도함수 식이 그래프에 self-contained로
      명시 (1-tanh² 구조가 노드로 보임). Tanh 노드가 미분마다 추가되어 지수 폭증
      (그래프 3형태 '폭증'의 교재 — 탐구 노트 32).
    - True: forward **출력 y 재사용** (dezero 방식) — 계산 이득 (tanh 재계산 없음)
      + Tanh 노드 1개 유지 (폭증 완화). 실증: 재호출 2→4→8 vs 재사용 1→1→1.
    ★ 읽히는 시점 = 역전파 (derivative는 fill_grad 중 호출) — 순전파가 아니라
      using_config 블록이 fill_grad를 감싸야 효과가 있다.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.tanh(x)

    @override
    def derivative(self) -> DerivativeFn:
        if Config.reuse_output:
            # forward 출력 재사용 — weakref 역참조를 클로저로 캡처 (브로 발견).
            output_ref = self.output
            assert output_ref is not None, "self.output must be set (__call__ should have run)"
            y = output_ref()
            assert y is not None, "output Variable이 이미 회수됨 — 역참조 불가"
            return lambda _: 1 - y * y

        # 재호출 — tanh(x)가 새 Tanh 노드를 만들며 그래프에 추가 (명시형).
        # 1 - ...은 __rsub__, **2는 __pow__ — 전부 Variable 연산으로 2차 미분 연결.
        return lambda x: 1 - tanh(x) ** 2

    @override
    def dot_label(self, show_param: bool = False) -> str:
        if show_param and Config.reuse_output:
            return 'Tanh(reuse)'
        return 'Tanh'


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


def tanh(x: Variable) -> Variable:
    """하이퍼볼릭 탄젠트 wrapper: tanh(x). ★ step35 신규 — 자기 참조 도함수.

    derivative 전략은 Config.reuse_output (전역 스위치)로 선택 —
    using_config('reuse_output', True) 블록이 fill_grad를 감싸면 효율형.
    """
    result = Tanh()(x)
    assert isinstance(result, Variable), "Tanh는 단일 출력이므로 Variable이어야 함"
    return result
