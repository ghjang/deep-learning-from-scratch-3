"""rezero.v1.core — DeZero 핵심 (Variable, Function, Config, fill_grad).

rezero v1 — 『밑바닥부터 시작하는 딥러닝 3』 제 1~2고지 (step01~22) 구현.
스칼라 Variable + 자동 역전파 (Define-by-Run).

rezero 정체성 (dezero와의 차이):
  - 역전파가 Variable.backward() 메서드가 아니라 전역 fill_grad() 함수 (관심사 분리).
  - 매직메서드(__add__ 등)를 클래스 안에 정의 (클래스 밖 대입 비권장).
  - __array_priority__ = 200 버림 (현대 NumPy에선 __rmul__로 충분).

이 패키지는 step23에서 step01~22 코드를 승격한 결과.
학습 흔적(주석, step 번호 참조 등)은 rezero/steps/stepNN.py에 남아있음.
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator, Iterator
from typing import Optional, cast, override

import numpy as np


# ===== Config — 전역 설정 (역전파 on/off) ======================================
class Config:
    """전역 설정. 클래스 변수 = 전역 상태.

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


# ===== 변환 헬퍼 (2층 구조) ====================================================
def as_array(x: object) -> np.ndarray:
    """스칼라를 ndarray로 변환. 낮은 수준 변환."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


def as_variable(obj: object) -> "Variable":
    """객체를 Variable로 변환. 이미 Variable이면 그대로 반환. 높은 수준 변환.

    Function.__call__ 도입부에서 모든 입력을 Variable로 정규화.
    """
    if isinstance(obj, Variable):
        return obj
    return Variable(as_array(obj))  # type: ignore[arg-type]


# ===== Worklist 타입 별칭 =====================================================
type Worklist = list["Function"]


# ===== Variable — 순수 데이터 상자 =============================================
# ===== VariableDataPropertyMixin — data에 위임하는 property (이슈 46 확장) ====
class VariableDataPropertyMixin:
    """data(ndarray)에 위임하는 property 4종 + __len__ — "순수 위임" 관심사.

    Variable.data가 None이면 _ensure_data가 RuntimeError 방어 (Step10의
    방어막 None 가드 원칙). Variable 본체는 "데이터 상자" 정의만 남음.
    """

    # 믹스인 계약 — 호스트(Variable)가 __init__에서 채울 속성 선언 (pyright용)
    data: Optional[np.ndarray]

    def _ensure_data(self) -> np.ndarray:
        """data가 None이면 RuntimeError, 아니면 data 반환."""
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


# ===== VariableArithmeticMixin — 산술 연산자 (이슈 46, 믹스인 분리) ============
class VariableArithmeticMixin:
    """Variable의 산술 연산자 9종 — 지연 import + functions 위임.

    ★ 지연 import (lazy import) — core.py ↔ functions.py **모듈 참조 순환** 회피.
      core.py 로드 시점엔 functions.py를 안 부르고, 실제 연산 시점에 로드.
      Python 모듈 캐싱으로 최초 1회만 실행 (성능 영향 없음).
      cf. dezero는 setup_variable()로 클래스 밖 대입해서 해결 — 우린 클래스 안 정의 원칙 유지.

    ★ 타입 어노테이션은 전부 문자열 ("Variable") — 믹스인이 Variable보다 먼저
      정의되므로 클래스 정의 시점에 이름이 없어서 (정적 분석 순환 회피).
    """

    def __add__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import add
        return add(cast("Variable", self), other)

    def __mul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import mul
        return mul(cast("Variable", self), other)

    def __radd__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import add
        return add(cast("Variable", self), other)

    def __rmul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import mul
        return mul(cast("Variable", self), other)

    # 단항 -, 비교환 (-, /), 거듭제곱
    def __neg__(self) -> "Variable":
        from rezero.v1.functions import neg
        return neg(cast("Variable", self))

    def __sub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import sub
        return sub(cast("Variable", self), other)

    def __rsub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 뺄셈: other - x. 비교환 → rsub가 순서 뒤집기 처리."""
        from rezero.v1.functions import rsub
        return rsub(cast("Variable", self), other)

    def __truediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import div
        return div(cast("Variable", self), other)

    def __rtruediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 나눗셈: other / x. 비교환 → rdiv가 순서 뒤집기 처리."""
        from rezero.v1.functions import rdiv
        return rdiv(cast("Variable", self), other)

    def __pow__(self, c: "int | float") -> "Variable":
        """거듭제곱: x ** c. c는 상수 (Variable 아님, 미분 대상 아님)."""
        from rezero.v1.functions import pow
        return pow(cast("Variable", self), c)


class Variable(VariableDataPropertyMixin, VariableArithmeticMixin):
    """DeZero의 변수. 순수 데이터 상자.

    data + 미분값(grad) + 그래프 연결(creator + generation).
    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성 — 관심사 분리).

    name 속성 + __repr__.
    data에 위임하는 property 4종 + __len__ → VariableDataPropertyMixin.
    산술 연산자 9종 → VariableArithmeticMixin.
    """

    def __init__(self, data: Optional[np.ndarray], *, name: Optional[str] = None):
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.name: Optional[str] = name
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    def __repr__(self) -> str:
        if self.data is None:
            return 'Variable(None)'
        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'Variable(' + p + ')'

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
    """DeZero의 함수 베이스.

    박스 컨텍스트 3계층:
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파

    자식은 apply (순수 수학) + derivative (도함수 hook) 구현.
    복잡한 연산(행렬 미분 등)은 backward를 직접 오버라이드하는 탈출구 사용 가능.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: "Variable | np.ndarray | float | int") -> Variable:
        # 모든 입력을 Variable로 정규화 (ndarray/scalar 허용)
        inputs_vars = tuple(as_variable(x) for x in inputs)

        xs = []
        for x in inputs_vars:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)

        assert len(ys) == 1, f"v1은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs_vars])
            output.set_creator(self)
            self.inputs = inputs_vars
            self.output = weakref.ref(output)

        return output

    # ===== 순전파 계열 =====================================================
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출)."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 구현."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (스칼라 출력 가정) ==================================
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
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

    def derivative(self) -> Callable[[np.ndarray], "np.ndarray | float"] | tuple[Callable, ...]:
        """도함수 hook. 단일 OR 튜플 자유 (부모에서 정규화).

        반환은 ndarray 또는 float 상수 — Add/Neg/Sub처럼 도함수가 상수인
        함수들이 float를 반환한다 (step34 버그 수정에서 타입 정직화).

        스칼라 출력 전용 — df(x) * upstream_grad 공식은 출력이 스칼라일 때만 성립.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )

    def dot_label(self, show_param: bool = False) -> str:
        """시각화(graphviz)용 라벨. 기본: 클래스명 (구조만 볼 때 — 책 방식).

        show_param=True면 파라미터 포함 — 파라미터를 가진 자식(Pow의 c 등)은
        오버라이드해서 파라미터를 포함할 것. 예: Pow(c=3).
        호출 측(_dot_func)이 verbose or show_value 조건으로 결정해 전달.
        """
        return type(self).__name__


# ===== iter_reverse_topo — 역방향 위상 정렬 순회 제너레이터 ====================
# fill_grad(역전파), fold_dot_graph(시각화)가 공유하는 순회 알고리즘.
# 순회 알고리즘을 분리함으로써 두 소비자가 동일한 "어떻게 순회할까" 로직을 공유 (DRY).
#
# ★ 리팩터 배경 (이슈 32번 — step25 이후 회수):
#   step25에서 fold_dot_graph가 fill_grad와 거의 동일한 worklist + visited 패턴을
#   사용함을 발견. 탐구 노트 20번 섹션 4/5에서 제안된 옵션 I (이터레이터 추출) 회수.
#   노트 20번 초안(step16 시점)에서 3가지 조정 — None 가드, visited 표시 시점(append
#   시점으로 통일), f.inputs None 가드. 자세한 내용은 이슈 32번 / 노트 20번 참조.
def iter_reverse_topo(start_var: Variable) -> Iterator[Function]:
    """start_var에서 역방향으로 계산 그래프를 위상 정렬 순회하는 제너레이터.

    output Variable에서 creator를 따라 역방향으로 Function들을 generation 내림차순으로
    yield. fill_grad(역전파)와 fold_dot_graph(시각화)가 공유하는 순회 알고리즘.

    순회만 담당 — 역전파 계산/grad 누적/retain_grad 등의 부작용은 소비자가 처리.
    Function.output weakref 역참조도 소비자 책임 (순회 자체는 output 안 씀).

    Args:
        start_var: 순회 시작점 (보통 최종 출력 Variable).

    Yields:
        Function: 역방향 위상 정렬 순서대로 (generation 큰 것부터 = 루트에 가까운 것부터).
    """
    if start_var.creator is None:
        # 역전파할 계산 그래프 없음 — 빈 순회 (소비자가 시작 전 None 체크로 에러 처리)
        return

    worklist: Worklist = [start_var.creator]
    visited: set[Function] = {start_var.creator}  # append 시점에 표시 (중복 append 방지)

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
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """자동 역전파 (iter_reverse_topo 제너레이터 + chain rule fold).

    Variable은 순수 데이터 상자로 두고, 그래프 순회는 iter_reverse_topo 제너레이터가
    담당. 이 함수는 순회하며 grad를 전파하는 역전파 계산만 담당 (관심사 분리).

    Args:
        start_var: 역전파 시작점 (보통 최종 출력 Variable).
        upstream_grad: 시작 grad 명시 (기본 None → np.ones_like 자동 초기화).
        retain_grad: True면 중간 Variable grad도 유지 (기본 False — 버림, 메모리 절약).
    """
    # 도입부 guard (사용자 오용 — 입력 변수에 fill_grad 호출 방지)
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    # 시작점 grad 초기화 (3단계 우선순위)
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        if start_var.data is None:
            raise RuntimeError(f"{start_var!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")
        start_var.grad = np.ones_like(start_var.data)

    # 역전파 메인 루프 — iter_reverse_topo가 순회를 담당 (worklist + visited 알고리즘 캡슐화)
    for f in iter_reverse_topo(start_var):
        assert f.output is not None, "f.output must be set"

        # weakref 역참조로 output Variable 획득
        output = f.output()
        if output is None:
            raise RuntimeError(
                f"{f!r}의 output Variable이 이미 회수되었습니다 — 역전파에 사용할 수 없습니다. "
                "역전파 대상 Variable을 사용자가 참조하고 있는지 확인하세요."
            )

        upstream = output.grad
        assert upstream is not None, "output.grad must be filled"

        # 역전파 호출 + 정규화
        downstream_grads = f.backward(upstream)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)

        # 다변 배분: 입력과 grad 짝지어 할당 (누적 — 같은 Variable 여러 입력와도 합산)
        assert f.inputs is not None, "f.inputs must be set"
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

        # retain_grad=False면 중간 output grad 버리기 (메모리 절약)
        if not retain_grad:
            output.grad = None


def backprop(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """fill_grad의 업계 표준 이름 별칭 — 역전파 수행 (이슈 49, REZERO_CHANGES 항목 041).

    fill_grad는 "grad를 채운다"(결과 관점) 이름이라 역전파 연산임이 코드에서
    즉시 드러나지 않는다는 이유로, 명시적 이름의 진입점을 추가 (구현은 위임).
    backprop이 표준(업계 관례·발견성 — 새 코드 기본) — fill_grad도 공존하는
    정식 이름(FP적 fill/fold 관점, step07의 right-fold 통찰을 담은 이름).
    관점을 강조하고 싶을 땐 fill_grad를 계속 써도 정당한 선택.

    Args:
        fill_grad와 동일 — start_var, upstream_grad, retain_grad.

    See Also:
        fill_grad — 실제 구현 (iter_reverse_topo + chain rule fold).
    """
    fill_grad(start_var, upstream_grad, retain_grad=retain_grad)
