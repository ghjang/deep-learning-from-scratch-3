"""
rezero.steps.step22 — [2고지] 연산자 오버로드(3)
===============================================

★ 책 공식 제목 "연산자 오버로드(3)". 연산자 오버로딩 3부작의 대미.
  step20: +, * (Add, Mul). step21: ndarray/scalar 혼합 (as_variable, __radd__, __rmul__).
  step22: 나머지 산술 연산자 전부 (-x, x-y, x/y, x**c).

★ 목표:
  이전: +, * 만 자연스럽게. (-, /, **는 못 씀)
  step22: `-x`, `2.0 - x`, `x - 1.0`, `3.0 / x`, `x ** 3` 전부 자연스럽게 ★

이 step에서 배울 것:
  - `Neg` 클래스 — 단항 부호 `-x` (피연산자 1개)
  - `Sub` 클래스 — 뺄셈 (비교환)
  - `Div` 클래스 — 나눗셈 (비교환, 역전파에 제곱 항)
  - `Pow` 클래스 — 거듭제곱 (★ 지수 c는 상수, 미분 대상 아님)
  - 대응 매직메서드: `__neg__`, `__sub__`, `__rsub__`, `__truediv__`, `__rtruediv__`, `__pow__`

★★★ rezero 변형 원칙 자동 적용 (★ "원칙 수립 → 준수" 사이클 점검):
  이번 step은 step20/21에서 확립한 3가지 원칙이 **대량(7개 매직메서드)** 으로 적용되는 첫 사례.
  원칙이 시스템으로 작동하는지 검증 = 이번 step의 메타 화두.

  | # | 원칙 | 위치 | 자동 적용 |
  |---|---|---|---|
  | A | 매직메서드는 클래스 안 정의 | 항목 031 (step20 확립) | ★ 7개 매직메서드 전부 클래스 안 |
  | B | __array_priority__ 버림 | 항목 033 (step21 확립, 탐구 25) | ★ 안 넣음 |
  | C | wrapper as_array 제거 | 항목 034 (step21 확립) | ★ wrapper는 단순하게 |

★★★ 핵심 특징 4가지 (4개 함수 클래스):

  1. **Pow는 특수** — `Pow(c)` 생성자가 `c`(지수)를 받음. c는 Variable이 아니라 상수.
     → `x ** 3`에서 3은 미분 대상 아님. 오직 밑(x)만 미분.
     → derivative: `lambda x: self.c * x**(self.c-1)` (★ c를 self에서 참조)

  2. **Sub/Div는 비교환** — Add/Mul과 달리 교환법칙 안 됨.
     → `__rsub__`/`__rtruediv__`는 단순 sub/div가 아니라 **인자 순서 뒤집기**.
     → `rsub(x0, x1) = sub(x1, x0)` — 좌변이 x1이니 순서 바꿔라.

  3. **Neg는 단항** — 피연산자 1개. `__neg__(self)`에 other 없음.
     → derivative: `lambda x: -1` (단일 상수함수)

  4. **역전파 수학** (derivative hook으로 표현):
     | 함수 | 순전파 | derivative hook | 복잡도 |
     |---|---|---|---|
     | Neg | -x | `lambda x: -1` | 단순 (상수) |
     | Sub | x0 - x1 | `(lambda _: 1, lambda _: -1)` | Add 변형 |
     | Div | x0 / x1 | `(lambda _: 1/x1, lambda _: -x0/x1**2)` | ★ 가장 복잡 (제곱) |
     | Pow | x**c | `lambda x: self.c * x**(self.c-1)` | c 참조 + 입력 의존 |

  ★ Div가 항목 013(derivative hook 재평가)의 또 다른 테스트. Mul(step20)보다 복잡한데도 hook으로 표현 가능.

★ 이 코드의 가정/전제 (step21 전제 + step22 새 전제):
  step14~21 누적 전제 + 새 전제:

  | 새 전제 (step22)                            | 의미                                       | 깨지면?                                       |
  |---------------------------------------------|--------------------------------------------|-----------------------------------------------|
  | **Pow의 지수 c는 상수(Variable 아님)**       | x ** 3에서 3은 미분 대상 아님               | c에 Variable 전달 시 에러/무시                 |
  | **Sub/Div는 비교환**                         | 순서 바뀌면 결과/미분 다름                   | __rsub__/__rtruediv__에서 순서 뒤집기 처리      |
  | **Neg는 단항**                               | 피연산자 1개, other 인자 없음                | Function 다변 패턴에 단항 끼워넣기 조정         |

참고 자료:
  - 원본 구현: steps/step22.py
  - 이전 step: rezero/steps/step21.py (연산자 오버로드(2) — 이번에 neg/sub/div/pow 추가)
  - 이슈: #28 (step22 진행 추적)
  - ★ 작업 원칙 자동 적용: 항목 031 (매직메서드 클래스 안), 033 (__array_priority__ 버림), 034 (wrapper as_array 제거)
  - ★ 탐구 노트: notes/exploration_26_numbers_complex.md (__truediv__ 역사, 파이썬 숫자 계보, 오일러 공식)

검증 포인트:
  - -x → Variable(-2.0)
  - 2.0 - x → Variable(0.0) (__rsub__)
  - x - 1.0 → Variable(1.0) (__sub__)
  - 3.0 / x → Variable(1.5) (__rtruediv__)
  - x ** 3 → Variable(8.0), x.grad = 12.0 (= 3*x², 역전파)

실행:
  uv run python rezero/steps/step22.py
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator
from typing import Optional, override

import numpy as np


# ★★★ step18 유지 — Config 전역 설정 + no_grad 컨텍스트 매니저 ---------------------
class Config:
    """★ step18 — 전역 설정 (역전파 on/off 플래그)."""
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
    """★ step18 — 역전파 끄기 사용자 인터페이스."""
    return using_config('enable_backprop', False)


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라를 ndarray로 변환."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


def as_variable(obj: object) -> "Variable":
    """★ step21 — 객체를 Variable로 변환. 이미 Variable이면 그대로 반환."""
    if isinstance(obj, Variable):
        return obj
    return Variable(as_array(obj))  # type: ignore[arg-type]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


# ★★★ step19~21 + step22 연산자 오버로드(3) — Variable -----------------------------
class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    ★ step19: name + __len__/__repr__ + property 4종
    ★ step20: __add__/__mul__ (연산자 오버로드 1)
    ★ step21: __radd__/__rmul__ + as_variable (연산자 오버로드 2)
    ★ step22: __neg__/__sub__/__rsub__/__truediv__/__rtruediv__/__pow__ (연산자 오버로드 3, 대미)

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

    # ===== step20~22: 연산자 오버로딩 전부 (클래스 안 정의) =================
    # ★ 항목 031 자동 적용 — 모든 매직메서드를 클래스 안에 정의 (책은 밖에서 대입).

    # --- step20: +, * (교환법칙 O) ---
    def __add__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        return add(self, other)

    def __mul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        return mul(self, other)

    # --- step21: __radd__, __rmul__ (역순, 교환법칙이라 정순과 동일) ---
    def __radd__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        return add(self, other)

    def __rmul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        return mul(self, other)

    # --- ★ step22 신규: 단항 -, 비교환 연산자 (-, /), 거듭제곱 ---
    def __neg__(self) -> "Variable":
        """단항 부호 연산자: -x. ★ other 인자 없음 (단항)."""
        return neg(self)

    def __sub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """뺄셈: x - other."""
        return sub(self, other)

    def __rsub__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 뺄셈: other - x. ★ 비교환 → 순서 뒤집기 필요 (rsub가 처리)."""
        return rsub(self, other)

    def __truediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """나눗셈: x / other. ('true' = 파이썬 3 진짜 수학 나눗셈, 탐구 26번 참조)"""
        return div(self, other)

    def __rtruediv__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 나눗셈: other / x. ★ 비교환 → 순서 뒤집기 (rdiv가 처리)."""
        return rdiv(self, other)

    def __pow__(self, c: "int | float") -> "Variable":
        """거듭제곱: x ** c. ★ c는 상수 (Variable 아님, 미분 대상 아님)."""
        return pow(self, c)

    # ===== step07~18: 그래프 연결 (변경 없음) =============================
    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. step21 as_variable로 입력 정규화. step22는 변경 없음.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: "Variable | np.ndarray | float | int") -> Variable:
        # --- ★ step21 — 모든 입력을 Variable로 정규화 -------------------
        inputs_vars = tuple(as_variable(x) for x in inputs)

        xs = []
        for x in inputs_vars:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)

        assert len(ys) == 1, f"step13~22은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs_vars])
            output.set_creator(self)
            self.inputs = inputs_vars
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


# ===== 구체 함수들 (step13~21 유지 + step22 신규 4종) ============================
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """곱셈 함수: (x0, x1) → x0 * x1. 미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        return (lambda _: x1, lambda _: x0)


# ===== ★ step22 신규 — Neg, Sub, Div, Pow (4개 함수 클래스) ======================

class Neg(Function):
    """★ step22 — 단항 부호: x → -x. 미분: f'(x) = -1.

    단항 연산자 (피연산자 1개). 다른 다입력 함수들과 구조가 약간 다름.
    derivative hook은 단일 상수함수 (-1).
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        # 단일 입력 → 단일 도함수 (tuple 아님). 부모에서 정규화.
        # np.float64(-1.0) * x 로 float64 승격 — NumPy 브로드캐스팅이 스칼라/배열 처리.
        return lambda x: np.float64(-1.0) * x


class Sub(Function):
    """★ step22 — 뺄셈: (x0, x1) → x0 - x1. 비교환.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = -1 (★ Add와 두 번째 항이 다름).
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 - x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        # Add: (1, 1). Sub: (1, -1). ★ 두 번째가 -1.
        return (lambda _: 1, lambda _: -1)


class Div(Function):
    """★ step22 — 나눗셈: (x0, x1) → x0 / x1. 비교환.

    미분: ∂y/∂x0 = 1/x1, ∂y/∂x1 = -x0/x1² (★ 제곱 항, Mul보다 복잡).
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 / x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        # ★ 가장 복잡한 derivative hook — 제곱 항 + 다른 입력값 의존.
        # 항목 013 재평가 통과 (Mul에 이어 Div도 hook으로 표현 가능).
        # ★ assert는 정적 분석(pyright)용 타입 좁히기 — 부모 backward()와 런타임 중복이지만
        #   pyright가 Div.derivative() 안에서 self.inputs/data가 Optional임을 좁히려면 필요.
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        assert x0 is not None and x1 is not None, "inputs' data must not be None"
        return (lambda _: 1 / x1, lambda _: -x0 / x1 ** 2)


class Pow(Function):
    """★ step22 — 거듭제곱: x → x**c. ★★ c는 상수 (Variable 아님, 미분 대상 아님).

    미분: f'(x) = c·x^(c-1) (지수 미분 공식).
    ★ 특수 구조: __init__(c)에서 c를 self에 저장. apply/derivative에서 self.c 참조.
    ★ c 저장 외에 inputs/output/generation은 부모에게 위임 (DRY).
    """

    def __init__(self, c: "int | float") -> None:
        self.c = c                     # ★ 커스텀 — c만 이 클래스에서 저장
        super().__init__()             # inputs/output/generation은 부모가 초기화

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** self.c

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        # ★ c·x^(c-1) — c는 self.c에서, x는 입력에서.
        # Mul처럼 "다른 입력값 의존"이 아니라 "self의 상수 의존" 형태.
        c = self.c
        return lambda x: c * x ** (c - 1)


# ===== wrapper 함수 (step12 스타일, 항목 034 — as_array 제거) ====================
def add(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """덧셈 wrapper."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """곱셈 wrapper."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def square(x: "Variable") -> "Variable":
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


# ----- ★ step22 신규 wrapper (neg, sub, rsub, div, rdiv, pow) -------------------
def neg(x: "Variable") -> "Variable":
    """★ 단항 부호 wrapper: -x."""
    result = Neg()(x)
    assert isinstance(result, Variable), "Neg는 단일 출력이므로 Variable이어야 함"
    return result


def sub(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """★ 뺄셈 wrapper: x0 - x1."""
    result = Sub()(x0, x1)
    assert isinstance(result, Variable), "Sub는 단일 출력이므로 Variable이어야 함"
    return result


def rsub(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """★ 역순 뺄셈 wrapper: x1 - x0 (비교환 → 순서 뒤집기).

    `2.0 - x` → Python이 x.__rsub__(2.0) 호출 → rsub(x, 2.0) → sub(2.0, x).
    ★ 좌변이 x1이므로 sub(x1, x0)로 순서를 뒤집어야 수학적으로 맞음.
    """
    result = Sub()(x1, x0)   # ★ 순서 뒤집기 (sub의 x0 자리에 x1, x1 자리에 x0)
    assert isinstance(result, Variable), "rsub는 단일 출력이므로 Variable이어야 함"
    return result


def div(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """★ 나눗셈 wrapper: x0 / x1."""
    result = Div()(x0, x1)
    assert isinstance(result, Variable), "Div는 단일 출력이므로 Variable이어야 함"
    return result


def rdiv(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """★ 역순 나눗셈 wrapper: x1 / x0 (비교환 → 순서 뒤집기).

    `3.0 / x` → Python이 x.__rtruediv__(3.0) 호출 → rdiv(x, 3.0) → div(3.0, x).
    ★ 좌변이 x1이므로 div(x1, x0)로 순서를 뒤집어야 수학적으로 맞음.
    """
    result = Div()(x1, x0)   # ★ 순서 뒤집기
    assert isinstance(result, Variable), "rdiv는 단일 출력이므로 Variable이어야 함"
    return result


def pow(x: "Variable", c: "int | float") -> "Variable":
    """★ 거듭제곱 wrapper: x ** c. ★ c는 상수 (Variable 아님)."""
    result = Pow(c)(x)
    assert isinstance(result, Variable), "Pow는 단일 출력이므로 Variable이어야 함"
    return result


# ★★★ step18 유지 — fill_grad 전역 함수 (retain_grad 매개변수 포함) ----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step18 retain_grad 매개변수 유지."""
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


# --- 데모: step22 연산자 오버로드(3) 검증 — neg/sub/div/pow ----------------------
if __name__ == "__main__":
    print("=== step22 연산자 오버로드(3) 데모 — neg/sub/div/pow ===")
    print()

    # --- 케이스 1: 단항 부호 (-x) ---
    print("[1] -x — 단항 부호 (__neg__)")
    x = Variable(np.array(2.0))
    y = -x
    print(f"    y = {y}  (기대: Variable(-2.0))")
    print()

    # --- 케이스 2: 뺄셈 (비교환) ---
    print("[2] 뺄셈 — __sub__ (x - 1.0), __rsub__ (2.0 - x)")
    x = Variable(np.array(2.0))
    y1 = 2.0 - x                    # __rsub__ → rsub(x, 2.0) → sub(2.0, x)
    y2 = x - 1.0                    # __sub__
    print(f"    2.0 - x = {y1}  (기대: Variable(0.0))  ← __rsub__ (역순, 순서 뒤집기)")
    print(f"    x - 1.0 = {y2}  (기대: Variable(1.0))  ← __sub__")
    print()

    # --- 케이스 3: 나눗셈 (비교환) ---
    print("[3] 나눗셈 — __truediv__ (x / 2), __rtruediv__ (3.0 / x)")
    x = Variable(np.array(2.0))
    y1 = 3.0 / x                    # __rtruediv__ → rdiv(x, 3.0) → div(3.0, x)
    y2 = x / 2.0                    # __truediv__
    print(f"    3.0 / x = {y1}  (기대: Variable(1.5))  ← __rtruediv__ (역순)")
    print(f"    x / 2.0 = {y2}  (기대: Variable(1.0))  ← __truediv__")
    print()

    # --- 케이스 4: 거듭제곱 (★ c는 상수) ---
    print("[4] 거듭제곱 — x ** 3 (__pow__, c=3 상수)")
    x = Variable(np.array(2.0))
    y = x ** 3
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 8.0 = 2³)")
    print(f"    x.grad = {x.grad}  (기대: 12.0 = 3·x² = 3·4)")
    print()

    # --- 케이스 5: 복합 식 (전 연산자 조합) ---
    print("[5] 복합 식 — y = 2.0 / x + x ** 2 - 1.0 (x=3.0)")
    x = Variable(np.array(3.0))
    y = 2.0 / x + x ** 2 - 1.0      # (2/3) + 9 - 1 = 8.667
    fill_grad(y)
    print(f"    y      = {y.data:.4f}  (기대: 8.6667 = 2/3 + 9 - 1)")
    # dy/dx = -2/x² + 2x = -2/9 + 6 = 5.778
    print(f"    x.grad = {x.grad:.4f}  (기대: 5.7778 = -2/x² + 2x = -2/9 + 6)")
    print()

    # --- 케이스 6: 부호 + 거듭제곱 조합 ---
    print("[6] -x ** 2 (x=3.0) — 부호와 거듭제곱의 우선순위")
    x = Variable(np.array(3.0))
    # ★ 파이썬 연산자 우선순위: **가 -보다 먼저. 즉 -(x**2) = -9.
    # (단항 -가 **보다 우선이면 (-x)**2 = 9가 될 텐데, 파이썬은 **가 먼저)
    y = -x ** 2
    print(f"    -x ** 2 = {y.data}  (기대: -9.0 = -(x²), **가 -보다 우선)")
    print(f"    ★ 파이썬 연산자 우선순위: ** > 단항 - (탐구 26번 연장)")
    print()

    # --- 케이스 7: Sub/Div 역전파 (비교환 검증) ---
    print("[7] Sub/Div 역전파 — 비교환 연산의 미분 검증")
    x = Variable(np.array(4.0))
    y = Variable(np.array(2.0))
    z = x - y                       # z = 4 - 2 = 2
    fill_grad(z)
    print(f"    z = x - y = {z.data}  (기대: 2.0)")
    print(f"    x.grad = {x.grad}  (기대: 1.0, ∂z/∂x = 1)")
    print(f"    y.grad = {y.grad}  (기대: -1.0, ∂z/∂y = -1) ★ Sub는 두 번째가 -1")
    print()

    x = Variable(np.array(6.0))
    y = Variable(np.array(2.0))
    z = x / y                       # z = 6 / 2 = 3
    fill_grad(z)
    print(f"    z = x / y = {z.data}  (기대: 3.0)")
    print(f"    x.grad = {x.grad}  (기대: 0.5, ∂z/∂x = 1/y = 1/2)")
    print(f"    y.grad = {y.grad}  (기대: -1.5, ∂z/∂y = -x/y² = -6/4) ★ Div 제곱 항")
    print()

    print("=== step22 완료 — 연산자 오버로딩 3부작 대미 (2고지 사실상 점령) ===")
