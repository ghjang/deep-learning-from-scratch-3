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
from collections.abc import Callable, Generator
from typing import Optional, override

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
class Variable:
    """DeZero의 변수. 순수 데이터 상자.

    data + 미분값(grad) + 그래프 연결(creator + generation).
    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성 — 관심사 분리).

    name 속성 + data에 위임하는 property 4종(shape/ndim/size/dtype) +
    __len__/__repr__ + 산술 연산자 7종(+, -, *, /, **, 단항 -) 지원.
    """

    def __init__(self, data: Optional[np.ndarray], *, name: Optional[str] = None):
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.name: Optional[str] = name
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    # ===== data에 위임하는 property 4종 + __len__ ==========================
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

    def __repr__(self) -> str:
        if self.data is None:
            return 'Variable(None)'
        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'Variable(' + p + ')'

    # ===== 산술 연산자 (전부 클래스 안에 정의) ==============================
    # ★ 지연 import (lazy import) — core.py ↔ functions.py 순환 참조 회피.
    #   core.py 로드 시점엔 functions.py를 안 부르고, 실제 연산 시점에 로드.
    #   Python 모듈 캐싱으로 최초 1회만 실행 (성능 영향 없음).
    #   cf. dezero는 setup_variable()로 클래스 밖 대입해서 해결 — 우린 클래스 안 정의 원칙 유지.
    def __add__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import add
        return add(self, other)

    def __mul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import mul
        return mul(self, other)

    def __radd__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import add
        return add(self, other)

    def __rmul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import mul
        return mul(self, other)

    # 단항 -, 비교환 (-, /), 거듭제곱
    def __neg__(self) -> "Variable":
        from rezero.v1.functions import neg
        return neg(self)

    def __sub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import sub
        return sub(self, other)

    def __rsub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 뺄셈: other - x. 비교환 → rsub가 순서 뒤집기 처리."""
        from rezero.v1.functions import rsub
        return rsub(self, other)

    def __truediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        from rezero.v1.functions import div
        return div(self, other)

    def __rtruediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 나눗셈: other / x. 비교환 → rdiv가 순서 뒤집기 처리."""
        from rezero.v1.functions import rdiv
        return rdiv(self, other)

    def __pow__(self, c: "int | float") -> "Variable":
        """거듭제곱: x ** c. c는 상수 (Variable 아님, 미분 대상 아님)."""
        from rezero.v1.functions import pow
        return pow(self, c)

    # ===== 그래프 연결 =====================================================
    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
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

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. 단일 OR 튜플 자유 (부모에서 정규화).

        스칼라 출력 전용 — df(x) * upstream_grad 공식은 출력이 스칼라일 때만 성립.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== fill_grad — 자동 역전파 (전역 함수, rezero 정체성) ======================
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """자동 역전파 (반복문 — worklist algorithm + 위상 정렬).

    Variable은 순수 데이터 상자로 두고, 그래프 순회는 이 전역 함수가 담당.

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

    # 메인 루프 상태 (worklist + visited)
    worklist: Worklist = []
    visited: set[Function] = set()

    def schedule(f: Function) -> None:
        """미방문 Function을 worklist에 예약 (generation 내림차순 정렬 유지)."""
        if f not in visited:
            worklist.append(f)
            visited.add(f)
            worklist.sort(key=lambda func: func.generation)

    schedule(start_var.creator)

    # 메인 루프: 계산 그래프 역방향 순회
    while worklist:
        f = worklist.pop()

        assert f.inputs is not None, "f.inputs must be set"
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
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

            if x.creator is not None:
                schedule(x.creator)

        # retain_grad=False면 중간 output grad 버리기 (메모리 절약)
        if not retain_grad:
            output.grad = None
