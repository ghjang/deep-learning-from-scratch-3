"""
rezero.steps.step09 — [1고지] 함수를 더 편리하게 (Function 클래스 사용성 개선)
===============================================

이 step에서 배울 것:
  - square(x) / exp(x) wrapper 함수 — Function을 1단계로 쓰기 (★ 이 step의 핵심)
  - as_array(x) 헬퍼 — 스칼라 연산 결과를 ndarray로 정규화
  - Variable.__init__에 isinstance 런타임 체크 — 잘못된 타입 입력 거부

★ 브로 통찰: "여기서 함수는 Function 클래스 — 더 편하게 = Function을 허들 없이 쓰자는 취지"
  번역 "함수를 더 편하게"는 애매 — "Function 클래스 사용성 개선"이 원 의미에 가까움.

이전 step과의 연결:
  - step07/08: 역전파 자동화 + 반복문(worklist) — 프레임워크 골격 완성
  - step09: 이제 그 골격을 **사용하는 쪽**의 경험 개선. "만든 다음엔 쓰기 편해야"
  - ★ 브로 직감 "이미 처리한 것 같기도, 구식 같기도" 검증 결과:
    · 타입 보장: 정적(힌트)은 있었으나 동적(isinstance)은 없었음 → step09에서 추가
    · "구식": 역순 — 책 원본이 구식. 우리 step08(fill_grad 전역, apply/derivative hook)이 더 진보됨
    · → 책 코드를 그대로 복붙하면 안 됨. 우리 step08 구조 위에 새 기능만 얹는 형태로.

★ step09 새 기능 4종 (책 원본 3종 + rezero 추가 pipe):
  - as_array(x) 헬퍼 — np.isscalar면 np.array로 변환. 왜 필요한가?
    np.exp(0.5)가 np.float64(스칼라) 반환 → Variable에 ndarray 아닌 값 들어감 → isinstance 체크에 걸림.
    apply hook의 np.exp(x) 반환값도 이 문제에 노출. as_array로 정규화.
  - square(x)/exp(x) wrapper — Square()(x) 2단계 → square(x) 1단계.
    합성: square(exp(square(x))) — 수학적 표기에 가까움. ★ 이게 "더 편하게"의 핵심.
  - Variable.__init__ isinstance 체크 — np.ndarray 아닌 입력 TypeError. (항목 1번 정정: step37→step09)
    ★ 정적 보장(타입 힌트) + 동적 보장(isinstance) + 동적 None 가드 = 방어막 3겹 (layered defense).
  - ★ pipe(value, *funcs) (브로 제안) — Haskell/Elixir 스타일 함수 합성 헬퍼.
    pipe(x, square, exp, square) = square(exp(square(x))). 평평 + 왼쪽→오른쪽 읽기 (데이터 흐름).
    단, step20+ 연산자 오버로딩 도입 후엔 출현 빈도 감소 — 스칼라 단항 합성(step09~19)에 주로 가치.

★ rezero 변형과의 상호작용 (검증 포인트):
  - square(x) wrapper가 apply hook(항목 10~13번)과 자연스럽게 어울리는지
  - fill_grad(y) (항목 14번) + square(x) — 둘 다 "사용성" 변형, 시너지
  - as_array 정규화 위치 — Function.__call__에서 (책 방식)

참고 자료:
  - 원본 구현: steps/step09.py
  - 이전 step: rezero/steps/step08.py (반복문 버전 — 베이스)
  - rezero 변형: REZERO_CHANGES.md 항목 1번 (isinstance 정정), 10~17번 (사용성 변형)

진행 순서 제안:
  1. steps/step09.py 펴서 책이 무엇을 추가했는지 확인 (as_array, wrapper, isinstance)
  2. rezero/steps/step08.py 베이스 위에 step09 새 기능 얹기 (복붙 아님 — 우리 구조 유지)
  3. 실행: uv run python rezero/steps/step09.py → 3.2974 나와야 함
  4. as_array 실증: np.exp(0.5)가 스칼라 반환하는지, as_array가 ndarray로 바꾸는지 확인

검증 포인트:
  - square(exp(square(x))) 결과가 step08의 C(B(A(x)))와 동일 (3.2974)
  - isinstance 체크: Variable(1.0) → TypeError 정상 발생
  - pyright: 환경성 에러만 (step08과 동일)

실행: uv run python rezero/steps/step09.py
"""

from abc import ABC
from functools import reduce
from typing import Callable, Optional, override

import numpy as np

# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, step09에서도 유지)
type Worklist = list["Function"]


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환.

    왜 필요한가? np.exp(0.5) 같은 연산이 np.float64(스칼라)를 반환할 수 있어서.
    스칼라를 그대로 Variable에 넣으면:
      1. Variable.data: np.ndarray 타입 힌트 위반 (정적 보장 깨짐)
      2. isinstance(data, np.ndarray) 런타임 체크에 걸려 TypeError (동적 보장)
    → as_array로 미리 ndarray로 정규화.

    np.isscalar: Python 숫자(int/float), numpy 스칼라(np.float64 등) 모두 True.
    ndarray (0차원 포함)는 False — 이미 배열이므로 그대로.

    ★ 삼항 연산자로 1줄화 — 단순 2-way 분기 + 각 갈래가 한 표현식이라 삼항이 더 Pythonic.
    (브로 제안: "3줄보다 1줄이 더 읽기 쉽지 않나?")
    # type: ignore — pyright가 스칼라/ndarray 두 갈래 리턴을 단일 타입으로 못 좁혀서.
    실제론 ndarray가 아닌 케이스는 __call__ 호출 흐름상 발생 안 함.
    """
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    ★ step09 변경: __init__에 isinstance 런타임 체크 추가.
      - 정적 보장(타입 힌트 data: np.ndarray)은 있었으나 동적 보장은 없었음.
      - 이제 둘 다 — 방어망 두 겹 (layered defense). 정적은 IDE/pyright, 동적은 런타임.
      - ★ 항목 1번 정정: "런타임 체크는 step37 도입 예정" → 실제론 step09에서 도입.
      - None은 허용 (미분값 계산 전 초기 상태, 책 step09 `x = Variable(None)` OK).

    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data: Optional[np.ndarray]):
        # ★ step09: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        # ★ cf. 항목 16번 — 런타임 데이터 검증엔 if/raise (assert 아님). 같은 결.
        # ★ and 결합 (브로 제안) — 중첩 if보다 평평하고 Pythonic.
        #   단축 평가로 data is None이면 isinstance 호출 안 함 (안전성 동일).
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 (순전파 시점에 __call__이 호출).

        ★ step09 변경: 없음. step07~08과 동일 (한 줄).
        step16 "복잡한 계산 그래프(generation)"에서 generation 설정 로직이 추가될 확장 포인트.
        """
        self.creator = func


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    ★ step09 변경: __call__에서 as_array로 출력 정규화.
      - apply hook 반환값이 스칼라(np.float64)일 수 있어 as_array로 ndarray 보장.
      - 이로써 Variable(as_array(y))가 안전 — isinstance 체크에 안 걸림.
      - apply/derivative hook 구조(항목 10~13번)는 그대로 유지.
    """

    def __init__(self) -> None:
        self.input: Optional[Variable] = None
        self.output: Optional[Variable] = None

    def __call__(self, input_var: Variable) -> Variable:
        # ★ None 가드 — input_var.data가 Optional이라 None일 수 있음.
        # 책 step09는 Variable(None) 생성은 허용하지만, 연산에 쓰는 건 금지.
        # Pylance Optional 경고 해소 + 런타임 방어 (항목 16번과 같은 결).
        if input_var.data is None:
            raise RuntimeError(f"{input_var!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")

        x = input_var.data
        y = self.forward(x)
        output = Variable(as_array(y))           # ★ step09: as_array로 스칼라→ndarray 정규화
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
        """역전파 (단일 노드): 기본 구현 (derivative hook × upstream). fold accumulator step.

        ★ 주의: 이건 **단일 노드**의 backward. 전체 그래프 순회는 전역 fill_grad()가 담당.
        """
        assert self.input is not None, "self.input must be set (__call__ should have run)"
        # ★ self.input.data가 Optional — None 가드 (Pylance + 런타임 방어).
        # __call__에서 이미 가드하므로 정상 흐름에선 도달 불가, but 타입 좁히기/방어.
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


# ★★★ step09 핵심 — wrapper 함수 (사용성 개선) ---------------------
# Square()(x) 2단계 → square(x) 1단계. 합성 표현이 수학적 표기에 가까워짐.
# square(exp(square(x))) ← (e^(x²))², step03~08의 C(B(A(x)))를 직관적으로.
def square(x: Variable) -> Variable:
    """제곱 함수 wrapper. Square 인스턴스 생성 + 호출을 한 번에."""
    return Square()(x)


def exp(x: Variable) -> Variable:
    """지수 함수 wrapper. Exp 인스턴스 생성 + 호출을 한 번에."""
    return Exp()(x)


# ★ pipe — 함수 합성 헬퍼 (브로 제안, Haskell/Elixir 스타일).
# 파이썬엔 기본 제공 함수 합성 연산자가 없지만, functools.reduce로 "껌" 수준 구현 가능.
# 데이터 흐름 순서(왼쪽→오른쪽)로 읽히는 게 핵심 — Unix 파이프 `cat | grep | sort`와 같은 철학.
#
# ★ 주의 — 장기 관점: step20+에서 __add__/__mul__ 연산자 오버로딩 도입 후엔
# 다변수 함수(sphere(x,y)=x²+y²)가 중위 연산자로 표현되어 pipe 출현 빈도 감소.
# → pipe는 스칼라 단항 함수 합성(step09~19)에 주로 가치. (브로 통찰: "step24는 연산자 오버로딩이라 pipe 안 낌")
def pipe(value: Variable, *funcs) -> Variable:
    """데이터 흐름 순서로 함수 합성. pipe(x, f, g, h) = h(g(f(x))).

    예: pipe(x, square, exp, square)  # x → square → exp → square (왼쪽→오른쪽 읽기)
        vs square(exp(square(x)))     # 괄호 중첩 (안쪽→바깥쪽 읽기)

    같은 결과지만 pipe가 평평하고 읽기 순서 = 실행 순서. 깊은 합성에서 가독성 유리.
    """
    return reduce(lambda val, f: f(val), funcs, value)


# fill_grad는 step08과 동일 (전역 함수, 반복문 worklist). step09에선 변경 없음.
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — 명시적 스택). step08 도입, step09 변경 없음.

    step09에선 square(x)/exp(x) wrapper가 자연스럽게 어울리는지만 확인.
    상세는 rezero/steps/step08.py 참고.
    """
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        # ★ start_var.data가 Optional — None 가드 (Pylance + 런타임 방어).
        if start_var.data is None:
            raise RuntimeError(f"{start_var!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")
        start_var.grad = np.ones_like(start_var.data)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm) ----------
    worklist: Worklist = [start_var.creator]
    while worklist:
        f = worklist.pop()
        x, y = f.input, f.output          # ★ 튜플 언패킹 — "input/output 짝 회수" 의도가 구조로 드러남 (브로 제안)

        assert x is not None and y is not None, "f.input/f.output must be set (__call__ should have run)"
        assert y.grad is not None, "y.grad must be filled (start or previous iteration sets it)"

        x.grad = f.backward(y.grad)

        if x.creator is not None:
            worklist.append(x.creator)


# --- 데모: square(x)/exp(x) wrapper로 합성 (★ step09 핵심) -----------------
# step03~08: C(B(A(x))) (인스턴스 3개 직접)
# step09:    square(exp(square(x)))  ← 수학적 표기에 가까움, 훨씬 직관적
x = Variable(np.array(0.5))
y = square(exp(square(x)))               # ★ wrapper로 한 줄 합성 — (e^(x²))²
fill_grad(y)                              # 전역 함수 (항목 14번)
print(f"역전파 결과 x.grad: {x.grad}")
print(f"step08 결과와 동일: 3.297442541400256 (해석적 정답)")
print()

# --- isinstance 런타임 체크 실증 (★ 방어막 — 정적/동적/None) ---------------
print("=== isinstance 런타임 체크 실증 ===")

# OK: ndarray — 정상 케이스
x_ok = Variable(np.array(1.0))
print(f"Variable(np.array(1.0)): OK (ndarray) → x_ok.data = {x_ok.data}")

# OK: None — 허용 (미계산 초기 상태, 책 step09 호환)
x_none = Variable(None)
print(f"Variable(None): OK (None 허용) → x_none.data = {x_none.data}")

# NG: Python float — 방어막 2번(isinstance) 작동 실증
try:
    Variable(1.0)  # type: ignore[call-arg]  # NG — Python float, ndarray 아님 (의도적 위반)
    print("ERROR: 예외 안 남!")
except TypeError as e:
    print(f"Variable(1.0): TypeError 정상 발생 → {e}")

print()
# --- as_array 실증: np.exp(0.5)가 스칼라, as_array가 ndarray로 ----------
print("=== as_array 헬퍼 실증 ===")
scalar_result = np.exp(0.5)               # np.float64 (스칼라)
print(f"np.exp(0.5): type={type(scalar_result).__name__}, isscalar={np.isscalar(scalar_result)}")
arr = as_array(scalar_result)
print(f"as_array(np.exp(0.5)): type={type(arr).__name__}, isscalar={np.isscalar(arr)}, shape={arr.shape}")

print()
# --- pipe 실증: 함수 합성 두 스타일 비교 (브로 제안, Haskell/Elixir 스타일) ----
# ★ 같은 결과, 다른 가독성. 깊은 합성에선 pipe(평평, 왼→오 읽기)가 괄호(깊음, 안→밖 읽기)보다 유리.
print("=== pipe 헬퍼 실증 (함수 합성 두 스타일) ===")
x_pipe = Variable(np.array(0.5))

# 스타일 A: 괄호 중첩 (현재 — 안쪽→바깥쪽 읽기)
y_parens = square(exp(square(x_pipe)))        # = square(exp(square(x)))
print(f"괄호: square(exp(square(x))) → x.grad 후보 y.data = {y_parens.data}")
fill_grad(y_parens)
print(f"  → x_pipe.grad = {x_pipe.grad}")

# 스타일 B: pipe (평평, 왼쪽→오른쪽 읽기 = 데이터 흐름)
x_pipe2 = Variable(np.array(0.5))              # 별도 Variable (grad 덮어쓰기 방지)
y_pipe = pipe(x_pipe2, square, exp, square)    # x → square → exp → square
print(f"pipe: pipe(x, square, exp, square) → y.data = {y_pipe.data}")
fill_grad(y_pipe)
print(f"  → x_pipe2.grad = {x_pipe2.grad}")

print(f"★ 두 스타일 결과 동일: {x_pipe.grad == x_pipe2.grad} (둘 다 3.2974...)")
