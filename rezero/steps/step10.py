"""
rezero.steps.step10 — [1고지] 테스트 (pytest로 동작 검증)
===============================================

★ 1고지 마지막 step. step10 완료 = 1고지 전체 완료 (MINOR bump: 0.0.9 → 0.1.0).

이 step에서 배울 것:
  - pytest (파이썬 실무 국룰 테스트 프레임워크) 도입 — 책의 unittest 대신
  - gradient check — 역전파(해석적) vs 수치 미분 비교 → 역전파 구현 신뢰
  - numerical_diff (step04 재등장, 복선 회수)
  - ★ step01~09의 모든 구축을 독립적 방법으로 검증 → 1고지 "완결성 인증"

★ 브로 결정: 책이 unittest를 가르치지만, 실무 국룰인 pytest로 가자 (탐구 17번).
  이유: 책(2020년)의 교육적 선택 vs 파이썬 생태계(2026년)의 사실상 국룰.
  pytest는 unittest 코드도 역호환 실행하지만, 새로 짜는 step10은 pytest 스타일(함수 + assert)로.
  상세: notes/exploration_17_python_testing.md.

이전 step과의 연결:
  - step04: numerical_diff (수치 미분) — gradient check용으로 재등장 ★ 복선 회수
  - step01~09: 역전파 메커니즘 구축 → 이제 그게 "맞는지" 검증
  - ★ step09 베이스에서 확장 (원본도 step09 기반 — 브로 통찰 정확)
  - rezero 변형 유지: fill_grad 전역 함수(항목 14번), apply/derivative hook, pipe

★ 핵심 — gradient check 왜 중요한가:
  역전파(해석적)는 우리가 직접 미분 공식을 코드에 박은 것. "이게 맞나?"를
  **독립적인 방법(수치 미분)** 으로 검증:
  - 역전파 결과 == 수치 미분 결과 → 구현이 맞음 (신뢰)
  - 다르면 → 어디선가 버그
  → step01~09의 모든 backward/derivative 구현을 믿을 수 있는 근거. 1고지의 "품질 보증".

참고 자료:
  - 원본 구현: steps/step10.py (unittest + SquareTest)
  - 이전 step: rezero/steps/step09.py (사용성 개선 — 베이스)
  - step04 numerical_diff 재등장 (gradient check용 복선 회수)
  - rezero 변형: REZERO_CHANGES.md 항목 14번 (fill_grad — 테스트에서 검증)
  - 테스팅 패러다임: notes/exploration_17_python_testing.md (unittest vs pytest)

검증 포인트:
  - test_forward / test_backward / test_gradient_check 전부 통과
  - fill_grad(y) vs numerical_diff(square, x) 비교 — 값 일치 (np.allclose)
  - 우리 구조(apply/derivative hook)에서 gradient check 통과

실행 (pytest — 국룰):
  uv run pytest rezero/steps/step10.py -v          # 상세 출력
  uv run pytest rezero/steps/step10.py::test_square_gradient_check -v  # 개별 테스트

★ 책 원본은 unittest 스타일이지만, pytest 역호환 덕분에 둘 다 실행 가능:
  uv run python -m unittest rezero.steps.step10    # (unittest로도 실행되지만 pytest 권장)
"""

from abc import ABC
from functools import reduce
from typing import Callable, Optional, override

import numpy as np
import pytest

# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, step09~10 유지)
type Worklist = list["Function"]


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환 (삼항 1줄화, 항목 2)."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    step09에서 __init__에 isinstance 런타임 체크 + 방어막 3겹 도입.
    step10에선 변경 없음 — 테스트가 이 구조를 검증하는 대상.
    """

    def __init__(self, data: Optional[np.ndarray]):
        # 방어막 2번: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        # and 결합 (항목 3) — 단축 평가로 None이면 isinstance 호출 안 함.
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록. step16 generation 확장 포인트."""
        self.creator = func


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    step09에서 as_array 정규화 도입. apply/derivative hook 구조(항목 10~13번) 유지.
    step10에선 변경 없음 — 테스트가 이 구조를 검증하는 대상.
    """

    def __init__(self) -> None:
        self.input: Optional[Variable] = None
        self.output: Optional[Variable] = None

    def __call__(self, input_var: Variable) -> Variable:
        # 방어막 3번: None 가드 (Pylance Optional 경고 해소 + 런타임 방어).
        if input_var.data is None:
            raise RuntimeError(f"{input_var!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")

        x = input_var.data
        y = self.forward(x)
        output = Variable(as_array(y))           # step09: as_array로 스칼라→ndarray 정규화
        output.set_creator(self)
        self.input = input_var
        self.output = output
        return output

    def forward(self, x: np.ndarray) -> np.ndarray:
        """순전파: 기본 구현 (apply hook 호출). 자식은 apply 또는 forward 직접 오버라이드."""
        return self.apply(x)

    def apply(self, x: np.ndarray) -> np.ndarray:
        """함수 본문 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    def backward(self, upstream_grad: np.ndarray) -> np.ndarray:
        """역전파 (단일 노드): 기본 구현 (derivative hook × upstream). fold accumulator step."""
        assert self.input is not None, "self.input must be set (__call__ should have run)"

        # 방어막 3번: self.input.data가 Optional — None 가드.
        if self.input.data is None:
            raise RuntimeError(f"{self.input!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

        x = self.input.data
        df = self.derivative()
        local_deriv = df(x)
        return local_deriv * upstream_grad

    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        """도함수(함수 객체) 반환 hook. 자식이 채우거나 backward 직접 오버라이드."""
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Exp(Function):
    """지수 함수: x → e^x. 미분: f'(x) = e^x (자기 자신)."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return np.exp(x)

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: np.exp(x)


# ★ step09 wrapper 함수 (사용성 개선) — Function을 1단계로 쓰기.
def square(x: Variable) -> Variable:
    """제곱 함수 wrapper. Square 인스턴스 생성 + 호출을 한 번에."""
    return Square()(x)


def exp(x: Variable) -> Variable:
    """지수 함수 wrapper. Exp 인스턴스 생성 + 호출을 한 번에."""
    return Exp()(x)


# ★ pipe — 함수 합성 헬퍼 (step09 브로 제안, Haskell/Elixir 스타일).
def pipe(value: Variable, *funcs) -> Variable:
    """데이터 흐름 순서로 함수 합성. pipe(x, f, g, h) = h(g(f(x)))."""
    return reduce(lambda val, f: f(val), funcs, value)


# ★★★ step10 핵심 추가 — numerical_diff (step04 재등장, 복선 회수) ------------
# ★ gradient check의 "독립적 검증 방법" — 역전파와 비교할 기준.
def numerical_diff(f: Callable[[Variable], Variable], x: Variable, eps: float = 1e-4) -> np.ndarray:
    """수치 미분 (중앙 차분). f의 내부를 몰라도 미분 가능 — 블랙박스 관점.

    ★ gradient check용 — 역전파(해석적)와 비교해 구현이 맞는지 독립 검증.
    공식: f'(x) ≈ [f(x+h) - f(x-h)] / 2h  (중앙 차분, 오차 O(h²))

    Args:
        f: 미분할 함수 (square, exp, 또는 합성 함수)
        x: 미분 기준점 Variable
        eps: h (미세 차분 간격, 기본 1e-4)
    """
    # ★ 방어막 3번 (None 가드) — x.data가 Optional이라 None일 수 있음.
    # None - eps는 연산 불가 (Pylance reportOptionalOperand 경고 해소).
    # __call__/backward/fill_grad의 가드와 같은 결 (debugging.md 항목 3).
    if x.data is None:
        raise RuntimeError(f"{x!r}의 data가 None입니다 — 수치 미분에 사용할 수 없습니다.")

    # --- 차분점 생성 (x ± eps) — as_array로 스칼라 정규화 -----------------
    # ★ as_array — x.data ± eps가 스칼라(np.float64) 반환 방지 (방어막 2번 isinstance 통과 보조).
    # ★ 참고: step04 원본 numerical_diff엔 as_array가 없었음. 그 시점엔 isinstance 체크가 없었으니까.
    # step09에서 isinstance 도입하면서 이 코드가 암묵적으로 깨짐 → step10에서 as_array로 보강.
    # → "과거 코드(step04)는 그 시점 기록으로 보존, 현재 step(step10)에서 필요 수정 반영" 원칙.
    x0 = Variable(as_array(x.data - eps))
    x1 = Variable(as_array(x.data + eps))

    # --- f 평가 + 결과 회수 ----------------------------------------------
    y0 = f(x0)
    y1 = f(x1)

    # ★ y0/y1은 f가 반환한 Variable — data가 채워져 있음 (방금 forward로 생성됨).
    # assert로 타입 좁히기 (Pylance — f 반환 후 data Optional 풀기).
    # ★ assert (불변조건) vs 위쪽 x.data의 if/raise (사용자 오용) — 용도에 따른 도구 선택 (debugging.md 원칙).
    assert y0.data is not None and y1.data is not None

    return (y1.data - y0.data) / (2 * eps)


# fill_grad는 step08~09와 동일 (전역 함수, 반복문 worklist). step10 변경 없음.
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — 명시적 스택). step08 도입, step10 변경 없음.

    step10에선 이 함수의 결과가 numerical_diff와 일치하는지 gradient check로 검증.
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

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm) ----------
    worklist: Worklist = [start_var.creator]
    while worklist:
        f = worklist.pop()
        x, y = f.input, f.output          # 튜플 언패킹 (항목 5)

        assert x is not None and y is not None, "f.input/f.output must be set"
        assert y.grad is not None, "y.grad must be filled"

        x.grad = f.backward(y.grad)

        if x.creator is not None:
            worklist.append(x.creator)


# ★★★ step10 핵심 — pytest 스타일 테스트 (책의 unittest 대신 국룰) -------------
# 책 원본: class SquareTest(unittest.TestCase) + self.assertEqual
# 우리: 평범한 함수 + assert 문 (pytest 스타일 — exploration_17 통찰 반영)
#
# 3가지 테스트 (책과 동일한 검증 범위, 다른 스타일):
#   1. test_square_forward       — 순전파 값 검증 (x=2 → y=4)
#   2. test_square_backward      — 역전파 값 검증 (x=3 → grad=6, f'(x)=2x)
#   3. ★ test_square_gradient_check — 역전파 vs 수치 미분 비교 (이 step의 핵심)


def test_square_forward():
    """순전파: square(2.0) == 4.0. 기본 값 검증."""
    x = Variable(np.array(2.0))
    y = square(x)
    assert y.data == np.array(4.0)


def test_square_backward():
    """역전파: square의 미분은 2x. x=3 → grad=6. 해석적 공식 직접 검증."""
    x = Variable(np.array(3.0))
    y = square(x)
    fill_grad(y)                         # ★ 전역 함수 (책은 y.backward() — 항목 14번 변형)
    assert x.grad is not None            # ★ 불변조건 (Pylance 타입 좁히기 — 다른 테스트와 동일 패턴)
    assert x.grad == np.array(6.0)       # f'(3) = 2*3 = 6


def test_square_gradient_check():
    """★★★ gradient check — 역전파(해석적) vs 수치 미분 비교.

    이게 step10의 핵심. 우리가 구현한 역전파(derivative hook)가 맞는지
    독립적인 방법(numerical_diff)으로 검증. 일치하면 역전파 구현 신뢰.

    ★ 무작위 x로 검증 — 특정 값에만 우연히 맞는 버그 방지.
    """
    x = Variable(np.random.rand(1))      # 무작위 점 — 책과 동일 전략
    y = square(x)
    fill_grad(y)                         # 역전파 (해석적 미분)

    num_grad = numerical_diff(square, x)  # 수치 미분 (독립적 검증)
    assert x.grad is not None             # ★ 불변조건 — fill_grad 후엔 grad 채워져 있음 (Pylance 타입 좁히기)
    assert np.allclose(x.grad, num_grad)  # 두 값이 가까우면 통과 ★


# 추가 검증 — 합성 함수도 gradient check (선택, 책엔 없지만 우리 구조 검증)
def test_composite_gradient_check():
    """합성 함수 square(exp(square(x)))의 gradient check.

    단일 함수(Square)뿐 아니라 합성도 역전파가 맞는지 검증.
    step03~09의 chain rule 구현을 종합 검증. (★ 책엔 없는 우리 확장)
    """
    x = Variable(np.random.rand(1))
    y = square(exp(square(x)))           # 합성 — chain rule
    fill_grad(y)

    # numerical_diff에 합성 함수를 그대로 넘김 (블랙박스 관점)
    composite = lambda v: square(exp(square(v)))
    num_grad = numerical_diff(composite, x)
    assert x.grad is not None            # ★ 불변조건 (Pylance 타입 좁히기)
    assert np.allclose(x.grad, num_grad, atol=1e-4)


# 추가 검증 — pipe로 합성한 것도 동일 (step09 pipe 헬퍼 검증)
def test_pipe_gradient_check():
    """pipe 헬퍼로 합성한 함수도 gradient check 통과?

    pipe(x, square, exp, square) == square(exp(square(x))) —
    같은 그래프를 만들어야 하므로 gradient도 동일.
    """
    x = Variable(np.random.rand(1))
    y = pipe(x, square, exp, square)
    fill_grad(y)

    piped = lambda v: pipe(v, square, exp, square)
    num_grad = numerical_diff(piped, x)
    assert x.grad is not None            # ★ 불변조건 (Pylance 타입 좁히기)
    assert np.allclose(x.grad, num_grad, atol=1e-4)


# --- 데모: pytest 실행이 아닌 직접 실행 시 (uv run python rezero/steps/step10.py) ----
if __name__ == "__main__":
    # 책의 step10.py는 unittest.main() 이었지만, pytest에선 `uv run pytest`로 실행.
    # 직접 실행 시엔 gradient check 데모를 보여줌.
    print("=== gradient check 데모 (square) ===")
    x = Variable(np.array(0.5))
    y = square(x)
    fill_grad(y)
    assert x.grad is not None                # ★ 불변조건 (Pylance 타입 좁히기 — 테스트 3곳과 동일 패턴)
    num_grad = numerical_diff(square, x)
    print(f"x = 0.5")
    print(f"역전파(해석적)  x.grad = {x.grad}")
    print(f"수치 미분       num_grad = {num_grad}")
    print(f"두 값 일치 (np.allclose): {np.allclose(x.grad, num_grad)}")
    print()
    print("★ pytest 실행: uv run pytest rezero/steps/step10.py -v")
