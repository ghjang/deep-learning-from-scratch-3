"""
rezero.steps.step21 — [2고지] 연산자 오버로드(2)
===============================================

★ 책 공식 제목 "연산자 오버로드(2)". step20의 연장선.
  step20: Variable + Variable 만 지원. step21: ndarray/scalar와의 혼합 연산 지원.

★ 목표:
  이전: x + 3.0 → TypeError (float이 Variable을 모름)
  step21: x + 3.0 → Variable(5.0), 3.0 * x + 1.0 → Variable(7.0) ★ 자연스러움

이 step에서 배울 것:
  - `__radd__` / `__rmul__` — 역순 연산자 (reflected/swapped operator)
  - `as_variable(obj)` 헬퍼 — ndarray/scalar를 Variable로 변환 (Function.__call__ 도입부)

★★★ ★ rezero 결정 — `__array_priority__ = 200` 버림 (탐구 25번 결론):
  책 원본은 `class Variable: __array_priority__ = 200`을 클래스 속성으로 둠.
  "ndarray와 연산 시 Variable이 우선"을 보장하기 위한 NumPy 특수 메커니즘.

  하지만 **현대 NumPy (Python 3.12 + 최신 버전)에선 불필요**:
  - 과거 NumPy는 다른 타입을 만나도 NotImplemented를 안 반환하고 무식하게 삼킴 → __rmul__ 안 불림
  - 현대 NumPy는 표준 디스패치를 존중 → __rmul__ 정상 호출 → priority 불필요
  - 실험(NaiveVar, priority 없음)으로 증명: priority 없이도 ndarray * Variable이 Variable 유지됨

  따라서 rezero는 `200` 버림. "왜 버렸는지"는 notes/exploration_25_array_priority.md에 영구 기록.
  ★ 핵심 교훈: "책 코드도 검증하라" — 매직 넘버를 이유 없이 쓰지 말 것.

★★★ 핵심 1 — 파이썬 연산자 디스패치(dispatch) 규칙 (step20 복습 + 역순):

  step20: `a + b` → `a.__add__(b)` (좌변 우선)
  step21의 문제: `3.0 * x` → Python이 `(3.0).__mul__(x)` 시도
                → float은 Variable을 모름 → NotImplemented 반환
                → Python이 `x.__rmul__(3.0)` 시도 ★ (역순 연산자)
                → x.__rmul__ = mul 이므로 mul(x, 3.0) → 성공!

  ★ `__radd__`/`__rmul__` = "역순 연산자".
    좌변이 Variable을 모르는 타입(int/float/ndarray)일 때 Variable쪽이 대신 처리.
    - `__add__`: `a + b` → `a.__add__(b)` (정순)
    - `__radd__`: `b + a` → `a.__radd__(b)` (역순, b가 처리 못 할 때)

★★★ 핵심 2 — `as_variable(obj)` 헬퍼 (입력 정규화):

  ```python
  def as_variable(obj):
      if isinstance(obj, Variable):
          return obj
      return Variable(obj)
  ```

  Function.__call__ 도입부에서 모든 입력을 as_variable로 변환:
  ```python
  def __call__(self, *inputs):
      inputs = [as_variable(x) for x in inputs]   # ★ ndarray/scalar → Variable
      xs = [x.data for x in inputs]
      ...
  ```

  ★ as_array와의 역할 분담:
    - as_array: 스칼라 → ndarray (step09, 낮은 수준 변환)
    - as_variable: ndarray/scalar → Variable (step21, 높은 수준 변환)
    → "변환 헬퍼 2층 구조": as_variable이 as_array(Variable 생성자 내부) 위에 얹힘.

★ 이 코드의 가정/전제 (step20 전제 + step21 새 전제):
  step14~20 누적 전제 + 새 전제:

  | 새 전제 (step21)                                       | 의미                                              | 깨지면?                                       |
  |-------------------------------------------------------|---------------------------------------------------|-----------------------------------------------|
  | **좌변이 Variable을 모르는 타입이면 __radd__/__rmul__ 처리** | `3.0 + x` → float.__add__ 실패 → x.__radd__       | __r*__ 없으면 TypeError                        |
  | **모든 입력은 as_variable로 Variable화 가능해야 함**       | Function.__call__ 도입부 변환                      | list/dict 등은 as_variable 실패 → TypeError     |

  ★ 참고: `__array_priority__` 전제는 버림 (탐구 25번 — 현대 NumPy에선 __rmul__로 충분).

★★★ rezero 변형 포인트:
  | # | 포인트                  | 책 방식                | 우리 방향                                       |
  |---|------------------------|------------------------|-------------------------------------------------|
  | A | __radd__/__rmul__ 위치 | 클래스 밖에서 대입      | ★ 클래스 안 정의 (step20 항목 031 작업 원칙 자동 적용) |
  | B | __array_priority__     | 클래스 속성 = 200       | ★ ★ 버림 (탐구 25번 — 현대엔 불필요)             |
  | C | as_variable 헬퍼       | 모듈 함수               | 동일 (as_array와 짝)                             |
  | D | Function.__call__ 변환 | 도입부                  | 동일                                            |

  ★ A는 step20에서 확립한 작업 원칙("매직메서드는 클래스 안에")의 첫 자동 적용 사례.
  ★★ B가 이번 step의 핵심 변형 — 탐구 25번 결론을 코드로 반영.

참고 자료:
  - 원본 구현: steps/step21.py
  - 이전 step: rezero/steps/step20.py (연산자 오버로드(1) — 이번에 ndarray/scalar 혼합 연산 추가)
  - 이슈: #26 (step21 진행 추적)
  - 작업 원칙: AGENTS.md "★ 매직메서드는 클래스 안에 정의 (필수)" (step20 확립)
  - ★ 탐구 노트: notes/exploration_25_array_priority.md (__array_priority__ 200 불필요 교훈)

검증 포인트:
  - x + np.array(3.0) (ndarray) → Variable(5.0)
  - x + 3.0 (scalar) → Variable(5.0)
  - 3.0 * x + 1.0 (좌변 scalar) → Variable(7.0) (x=2.0일 때)
  - 역전파 정상 동작 확인

실행:
  uv run python rezero/steps/step21.py
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator
from typing import Optional, override

import numpy as np


# ★★★ step18 유지 — Config 전역 설정 + no_grad 컨텍스트 매니저 ---------------------
class Config:
    """★ step18 — 전역 설정 (역전파 on/off 플래그). 이번 step21은 그대로 유지."""
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


# ★★★ step21 신규 — as_variable 헬퍼 (ndarray/scalar → Variable 변환) ----------------
def as_variable(obj: object) -> "Variable":
    """★ step21 — 객체를 Variable로 변환. 이미 Variable이면 그대로 반환.

    Function.__call__ 도입부에서 모든 입력을 Variable로 정규화.
    ★ as_array와의 역할 분담:
      - as_array: 스칼라 → ndarray (낮은 수준 변환, step09)
      - as_variable: ndarray/scalar → Variable (높은 수준 변환, step21)
      → "변환 헬퍼 2층 구조": as_variable이 as_array(Variable 생성자 내부) 위에 얹힘.

    ★ 주의: list/dict 등은 Variable 생성자에서 TypeError 발생 (ndarray만 허용).
    """
    if isinstance(obj, Variable):
        return obj
    return Variable(as_array(obj))  # type: ignore[arg-type]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


# ★★★ step19 유지 + step20/21 연산자 오버로딩 — Variable ---------------------------
class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    ★ step19 추가: name 속성 + __len__/__repr__ 매직메서드 + shape/ndim/size/dtype property.
    ★ step20 추가: __add__/__mul__ 매직메서드 — 연산자 오버로딩 (+, *).
    ★ step21 추가: __radd__/__rmul__ — 역순 연산자 (ndarray/scalar와 혼합 연산).

    ★★ step21 결정: __array_priority__ = 200 버림 (탐구 25번).
      현대 NumPy에선 __rmul__만으로 충분. 과거 NumPy 호환용 핵.

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
    def __add__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """+ 연산자 오버로딩. add wrapper에 위임. ★ step21: 혼합 타입 허용."""
        return add(self, other)

    def __mul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """* 연산자 오버로딩. mul wrapper에 위임. ★ step21: 혼합 타입 허용."""
        return mul(self, other)

    # ===== step21: 역순 연산자 (__radd__, __rmul__) =========================
    # ★ 좌변이 Variable을 모르는 타입(int/float/ndarray)일 때 대신 처리.
    #   3.0 * x → float.__mul__(x) 실패 → x.__rmul__(3.0) 호출.
    # ★ 클래스 안 정의 (step20 항목 031 작업 원칙 자동 적용).
    def __radd__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 + 연산자. add는 교환법칙 성립 → add(self, other)와 동일."""
        return add(self, other)

    def __rmul__(self, other: "Variable | np.ndarray | float | int") -> "Variable":
        """역순 * 연산자. mul은 교환법칙 성립 → mul(self, other)와 동일."""
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

    ★ step21 변경: __call__ 도입부에 as_variable로 입력 정규화 (ndarray/scalar → Variable).
      이로써 x + 3.0, np.array(3.0) * x 같은 혼합 연산이 자연스럽게 동작.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: "Variable | np.ndarray | float | int") -> Variable:
        # --- ★ step21 핵심 — 모든 입력을 Variable로 정규화 -------------------
        # ndarray/scalar가 섞여 들어와도 as_variable이 Variable로 변환.
        # 이렇게 하면 Function 내부 로직은 항상 Variable만 다루면 됨 (일관성).
        inputs_vars = tuple(as_variable(x) for x in inputs)

        # --- 회수 + 가드를 한 루프로 (step11 패턴 유지) ---
        xs = []
        for x in inputs_vars:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        # --- 순전파: forward → 다시 Variable로 래핑 --------------------------------
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)

        assert len(ys) == 1, f"step13~21은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- ★ step18 유지 — Config.enable_backprop일 때만 그래프 구축 -------------
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


# ===== 구체 함수들 (step13~20과 동일) =====
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
    """곱셈 함수: (x0, x1) → x0 * x1.

    미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0.
    ★ 항목 013 재평가 통과 (step20) — "다른 입력값에 의존" 케이스.
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"
        x0 = self.inputs[0].data
        x1 = self.inputs[1].data
        return (lambda _: x1, lambda _: x0)


# ===== wrapper 함수 (step12 스타일) ============================================
# ★ step21 — wrapper 안의 as_array는 제거.
#   이유: Function.__call__ 도입부의 as_variable이 이미 ndarray/scalar → Variable 변환을 처리.
#   wrapper 안에서 또 as_array 하는 건 중복 (브로 "중복은 없애는 게 좋다" + 실험으로 검증).
#   책 원본은 wrapper에 as_array를 두지만, 이는 step20까지의 잔재 (Function.__call__에 as_variable 없던 시절).
#   step21에서 as_variable 도입으로 Function.__call__이 변환 책임을 떠안으며 wrapper는 단순해짐.
def add(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """덧셈 wrapper. x1은 Variable/ndarray/scalar 모두 가능 (Function.__call__에서 정규화)."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: "Variable", x1: "Variable | np.ndarray | float | int") -> "Variable":
    """곱셈 wrapper. x1은 Variable/ndarray/scalar 모두 가능 (Function.__call__에서 정규화)."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def square(x: "Variable") -> "Variable":
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


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


# --- 데모: step21 ndarray/scalar 혼합 연산 검증 ----------------------------------
if __name__ == "__main__":
    print("=== step21 연산자 오버로드(2) 데모 — ndarray/scalar 혼합 연산 ===")
    print()

    # --- 케이스 1: ndarray와 연산 (step21 핵심) ---
    print("[1] x + np.array(3.0) — ndarray와 연산")
    x = Variable(np.array(2.0))
    y = x + np.array(3.0)
    print(f"    y = {y}  (기대: Variable(5.0))")
    print(f"    ★ ndarray가 as_variable로 Variable화되어 연산 → 결과도 Variable")
    print()

    # --- 케이스 2: 스칼라와 연산 ---
    print("[2] x + 3.0 — 파이썬 스칼라와 연산")
    x = Variable(np.array(2.0))
    y = x + 3.0
    print(f"    y = {y}  (기대: Variable(5.0))")
    print()

    # --- 케이스 3: 좌변이 스칼라/ndarray (역순 연산자 __radd__/__rmul__) ---
    print("[3] 3.0 * x + 1.0 — 좌변이 스칼라 (__rmul__/__radd__ 동작)")
    x = Variable(np.array(2.0))
    y = 3.0 * x + 1.0
    print(f"    y = {y}  (기대: Variable(7.0) = 3*2+1)")
    print(f"    ★ 3.0 * x → float.__mul__(x) 실패 → x.__rmul__(3.0) → mul(x, 3.0)")
    print()

    # --- 케이스 4: ndarray * Variable (좌변이 ndarray) ---
    print("[4] np.array(3.0) * x — 좌변이 ndarray (__rmul__ 동작, __array_priority__ 없이)")
    x = Variable(np.array(2.0))
    y = np.array(3.0) * x
    print(f"    y = {y}  (기대: Variable(6.0))")
    print(f"    ★ __array_priority__ 없이도 현대 NumPy는 Variable.__rmul__ 호출 (탐구 25번)")
    print()

    # --- 케이스 5: 역전파 정상 동작 (혼합 타입 연산에서도) ---
    print("[5] 역전파 정상 동작 — y = 2.0 * x + 1.0 (혼합 타입)")
    x = Variable(np.array(3.0))
    y = 2.0 * x + 1.0                    # y = 2*3+1 = 7, dy/dx = 2
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 7.0)")
    print(f"    x.grad = {x.grad}  (기대: 2.0 = dy/dx)")
    print()

    # --- 케이스 6: 복잡한 혼합 식 ---
    print("[6] 복잡한 혼합 식 — y = a * b + np.array(2.0) (a=Variable, b=Variable, +ndarray)")
    a = Variable(np.array(3.0))
    b = Variable(np.array(2.0))
    y = a * b + np.array(2.0)            # (3*2) + 2 = 8
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 8.0)")
    print(f"    a.grad = {a.grad}  (기대: 2.0 = b)")
    print(f"    b.grad = {b.grad}  (기대: 3.0 = a)")
    print()

    print("=== step21 완료 — ndarray/scalar와 자유롭게 섞어 쓰는 수학 식 ===")
