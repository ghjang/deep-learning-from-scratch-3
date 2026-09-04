"""rezero.v0.core — NumPy 없는 DeZero (순수 Python 학습 실험실).

rezero v0 — 이슈 43 작업 3 (브로 아이디어, RESEARCH_QUEUE 후보 9번).
v1을 기반으로 NumPy를 걷어낸 패키지. 스코프는 v1과 동일 (1차 미분).

★ 왜 v0인가 (v1이 먼저 있는데 역방향 착공 — 자연수에 나중에 0을 추가한 격):
  NumPy의 벡터화가 감추는 구조를 드러내는 학습 실험실.
  - Variable.data가 개별 float — ndarray 없음
  - "여러 점 계산"이 필요하면 원소 순회 루프를 직접 씀
    → 데이터축(배치/성분)이 코드에 명시적으로 드러남 (두 축의 물리적 분리,
      노트 34 "배치 = 독립 스칼라 실험의 묶음"의 구현판)
  - v1에서 NumPy가 하던 일의 목록이 걷어내면서 보임:
      as_array (스칼라→배열 승격), VariableDataPropertyMixin (shape/ndim/
      size/dtype/__len__ 위임), np.ones_like (씨앗), 브로드캐스팅 없는 순수 곱.

rezero 정체성 (v1과 동일): fill_grad 전역 함수, 매직메서드 클래스 안 정의.
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator, Iterator
from typing import Optional, cast, override


# ===== Config — 전역 설정 (역전파 on/off) ======================================
class Config:
    """전역 설정. 클래스 변수 = 전전 상태.

    enable_backprop=True (기본) → 역전파 대비 그래프 구축.
    enable_backprop=False       → 순전파 값만 (추론용, 메모리 절약).
    """

    enable_backprop: bool = True


@contextlib.contextmanager
def using_config(name: str, value: object) -> Generator[None, None, None]:
    """Config 속성을 일시적으로 변경하는 컨텍스트 매니저.

    with 블록 진입 시 변경, 탈출 시(예외 포함) 원래값 복구.
    """
    old_value = getattr(Config, name)
    setattr(Config, name, value)

    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad() -> contextlib._GeneratorContextManager[None]:
    """역전파 끄기 사용자 인터페이스. PyTorch torch.no_grad()와 동일 패턴."""
    return using_config('enable_backprop', False)


# ===== 변환 헬퍼 ================================================================
def as_float(x: object) -> float:
    """숫자(int/float)를 float로 변환. v1의 as_array(스칼라→ndarray) 대응.

    NumPy가 없으니 승격은 없음 — int만 float로 (bool은 의도적 배제).
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        raise TypeError(f"{type(x)}는 지원하지 않습니다. int/float만 허용.")
    return float(x)


def as_variable(obj: object) -> "Variable":
    """객체를 Variable로 변환. 이미 Variable이면 그대로 반환.

    Function.__call__ 도입부에서 모든 입력을 Variable로 정규화.
    """
    if isinstance(obj, Variable):
        return obj
    return Variable(as_float(obj))


# ===== Worklist 타입 별칭 =====================================================
type Worklist = list["Function"]


# ===== VariableArithmeticMixin — 산술 연산자 ==================================
class VariableArithmeticMixin:
    """Variable의 산술 연산자 9종 — 지연 import + functions 위임.

    ★ 지연 import (lazy import) — core.py ↔ functions.py 모듈 참조 순환 회피.
    타입 어노테이션은 전부 문자열 ("Variable") — 믹스인이 Variable보다 먼저
    정의되므로 클래스 정의 시점에 이름이 없어서.
    """

    def __add__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import add
        return add(cast("Variable", self), other)

    def __mul__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import mul
        return mul(cast("Variable", self), other)

    def __radd__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import add
        return add(cast("Variable", self), other)

    def __rmul__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import mul
        return mul(cast("Variable", self), other)

    # 단항 -, 비교환 (-, /), 거듭제곱
    def __neg__(self) -> "Variable":
        from rezero.v0.functions import neg
        return neg(cast("Variable", self))

    def __sub__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import sub
        return sub(cast("Variable", self), other)

    def __rsub__(self, other: "Variable | float | int") -> "Variable":
        """역순 뺄셈: other - x. 비교환 → rsub가 순서 뒤집기 처리."""
        from rezero.v0.functions import rsub
        return rsub(cast("Variable", self), other)

    def __truediv__(self, other: "Variable | float | int") -> "Variable":
        from rezero.v0.functions import div
        return div(cast("Variable", self), other)

    def __rtruediv__(self, other: "Variable | float | int") -> "Variable":
        """역순 나눗셈: other / x. 비교환 → rdiv가 순서 뒤집기 처리."""
        from rezero.v0.functions import rdiv
        return rdiv(cast("Variable", self), other)

    def __pow__(self, c: "int | float") -> "Variable":
        """거듭제곱: x ** c. c는 상수 (Variable 아님, 미분 대상 아님)."""
        from rezero.v0.functions import pow
        return pow(cast("Variable", self), c)


class Variable(VariableArithmeticMixin):
    """DeZero의 변수 (v0 — data가 float). 순수 데이터 상자.

    data + 미분값(grad) + 그래프 연결(creator + generation).
    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성 — 관심사 분리).

    ★ v1과의 차이: data가 float 하나 (ndarray 아님) — shape/dtype/size/
    __len__ 같은 "배열이 주던 것"이 아예 없다 (그게 v0의 요점 중 하나).
    """

    def __init__(self, data: Optional[float], *, name: Optional[str] = None):
        if data is not None:
            data = as_float(data)

        self.data: Optional[float] = data
        self.name: Optional[str] = name
        self.grad: Optional[float] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    def __repr__(self) -> str:
        if self.data is None:
            return 'Variable(None)'
        return f'Variable({self.data})'

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속.

        Define-by-Run의 핵심 — 순전파가 실행되는 순간 이 메서드가 불려
        계산 그래프가 동적으로 자란다. creator가 채워져야 fill_grad가
        역방향으로 순회할 수 있음 (creator 없는 Variable = 그래프의 리프).
        """
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시)."""
        self.grad = None


# ===== Function — 함수 베이스 클래스 ===========================================
class Function(ABC):
    """DeZero의 함수 베이스 (v0 — float in/out).

    자식은 apply (순수 수학) + derivative (도함수 hook) 구현.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: "Variable | float | int") -> Variable:
        # 모든 입력을 Variable로 정규화 (스칼라 허용)
        inputs_vars = tuple(as_variable(x) for x in inputs)

        xs = []
        for x in inputs_vars:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)

        assert len(ys) == 1, f"v0은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_float(ys[0]))

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs_vars])
            output.set_creator(self)
            self.inputs = inputs_vars
            self.output = weakref.ref(output)

        return output

    # ===== 순전파 계열 =====================================================
    def forward(self, *xs: float) -> tuple[float, ...] | float:
        """순전파 뼈대 (apply hook 호출)."""
        return self.apply(*xs)

    def apply(self, *xs: float) -> tuple[float, ...] | float:
        """순수 수학 계산 hook. 자식이 구현."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계산 (스칼라 출력 가정) ==================================
    def backward(self, upstream_grad: float) -> tuple[float, ...]:
        """역전파 뼈대 (derivative hook 호출). chain rule fold step 일반화."""
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

    def derivative(self) -> "Callable[[float], float] | tuple[Callable, ...]":
        """도함수 hook. 단일 OR 튜플 자유 (부모에서 정규화).

        반환은 float 상수 또는 x로 계산한 float — NumPy가 없으니 전부 스칼라.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )

    def dot_label(self, show_param: bool = False) -> str:
        """시각화용 라벨 (v0은 시각화 스코프 아님 — v1 인터페이스 호환 흔적)."""
        return type(self).__name__


# ===== iter_reverse_topo — 역방향 위상 정렬 순회 제너레이터 ====================
def iter_reverse_topo(start_var: Variable) -> Iterator[Function]:
    """start_var에서 역방향으로 계산 그래프를 위상 정렬 순회하는 제너레이터.

    output Variable에서 creator를 따라 역방향으로 Function들을 generation 내림차순으로
    yield. fill_grad(역전파)가 소비하는 순회 알고리즘 (v1과 동일 — NumPy 무관).

    Yields:
        Function: 역방향 위상 정렬 순서대로 (generation 큰 것부터).
    """
    if start_var.creator is None:
        return

    worklist: Worklist = [start_var.creator]
    visited: set[Function] = {start_var.creator}

    while worklist:
        worklist.sort(key=lambda f: f.generation)
        f = worklist.pop()

        assert f.inputs is not None, "f.inputs must be set"
        yield f

        for x in f.inputs:
            if x.creator is not None and x.creator not in visited:
                visited.add(x.creator)
                worklist.append(x.creator)


# ===== fill_grad — 자동 역전파 (전역 함수, rezero 정체성) ======================
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[float] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """자동 역전파 (iter_reverse_topo + chain rule fold) — v0 스칼라판.

    ★ v1과의 차이: 시작 씨앗이 np.ones_like(data)가 아니라 그냥 1.0 —
    "dy/dy = 1"이 스칼라 하나라는 게 여기서는 코드 그대로 보임.

    Args:
        start_var: 역전파 시작점 (보통 최종 출력 Variable).
        upstream_grad: 시작 grad 명시 (기본 None → 1.0 자동 초기화).
        retain_grad: True면 중간 Variable grad도 유지 (기본 False — 버림).
    """
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    # 시작점 grad 초기화 — 스칼라 씨앗 1.0 (dy/dy = 1)
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        start_var.grad = 1.0

    # 역전파 메인 루프
    for f in iter_reverse_topo(start_var):
        assert f.output is not None, "f.output must be set"

        output = f.output()
        if output is None:
            raise RuntimeError(
                f"{f!r}의 output Variable이 이미 회수되었습니다 — 역전파에 사용할 수 없습니다."
            )

        upstream = output.grad
        assert upstream is not None, "output.grad must be filled"

        downstream_grads = f.backward(upstream)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)

        assert f.inputs is not None, "f.inputs must be set"
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

        if not retain_grad:
            output.grad = None


def backprop(
    start_var: Variable,
    upstream_grad: Optional[float] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """fill_grad의 업계 표준 이름 별칭 (v1과 동일 — REZERO_CHANGES 항목 041).

    See Also:
        fill_grad — 실제 구현 (iter_reverse_topo + chain rule fold).
    """
    fill_grad(start_var, upstream_grad, retain_grad=retain_grad)
