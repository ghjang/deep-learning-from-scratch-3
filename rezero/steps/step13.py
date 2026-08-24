"""
rezero.steps.step13 — [2고지] 가변 길이 인수(역전파 편)
===============================================

★ step11~13 "가변 길이 인수" 3부작의 대미. 역전파 다변 버전 완결.
  - step11 — 순전파: 다변 입출력 도입 (리스트)
  - step12 — 개선: *inputs 가변 인수로 자연스럽게
  - step13 (이번) — 역전파: 다변 버전 역전파 ★ 3부작 완결

이 step에서 배울 것:
  - fill_grad 다변 진화 — output_grads 회수 + 언패킹 호출 + zip 배분
  - Function.backward(upstream_grad) 단일 인자 (스칼라 출력 가정, 책 step13 충실)
  - Add 역전파: derivative (lambda _: 1) 상수함수 × upstream — "들어온 걸 그대로 양쪽에"
  - ★★★ derivative hook의 결정적 시험대 — 다변 함수에서 살아남는가?

★★★ 핵심 설계 결정 — derivative hook "선택적" 패턴 확정 (브로 철학):
  step07부터 "derivative OR backward override 두 경로"를 열어뒀음 (#010~#013).
  이 step에서 그 설계가 시험받고, "스칼라 출력 전용" 유효 범위가 확정됨.

  ★ 브로 통찰 1 — "출력 스칼라일 때까지만 의미 있다":
    derivative hook의 `df(x) * gy` 공식은 출력 y가 스칼라일 때만 성립.
    벡터/행렬 출력(step34+)은 야코비안 전치 곱(J^T @ gy)이라 스칼라 곱이 붕괴.
    → derivative 유효 범위 = step01~33 (스칼라 회로). step34+는 backward 직접.

  ★ 브로 통찰 2 — "Add 도함수는 상수함수!":
    Add 편도함수 ∂y/∂x_i = 1 = "입력 무시하고 항상 1 반환" = FP의 const(1) 상수함수!
    → derivative가 (lambda _: 1, lambda _: 1) 튜플 반환으로 Add 표현 가능.

  ★ 브로 철학 — "derivative hook 버리지 않는다":
    backward 완전 오버라이드해야 하는 상황(step34+)이 오면 그때 그때 오버라이드.
    hook 자체를 없애지 않음. "선택적 hook" 원칙(#010)이 빛을 발하는 지점.

  ★ 책 패턴 확장 — derivative도 단일/튜플 자유 + 부모 정규화:
    책은 backward가 단일값/튜플 자유롭게 반환 (부모에서 정규화).
    우리는 derivative에도 같은 패턴 적용:
      - Square: return lambda x: 2*x          (단일 도함수)
      - Add:    return (lambda _: 1, lambda _: 1)  (튜플 — 2개 입력)
    부모 backward에서 isinstance 체크로 정규화 후 zip 처리.

★★★ 이 코드의 가정/전제 (다른 세션 혼동 방지 위해 명시):
  이 소스는 다음 전제 위에서 작성됨. 어느 전제가 깨지면 해당 부분을 진화시켜야 함.

  | 전제 | 깨지는 시점 | 진화 필요 항목 | 관련 |
  |---|---|---|---|
  | **출력은 스칼라 1개** | step34+ (벡터/행렬 출력, Split 함수) | self.output → outputs 복수, backward(*gys) 가변, derivative hook 폐기 | #019 |
  | **입력 수 = derivative 튜플 길이** | 자식이 잘못 구현할 때 | NotImplementedError 대신 명확한 에러 메시지 | 이 파일 |
  | **출력 1개 → upstream 1개** | step34+ 다출력 시 | f.output.grad → output_grads 리스트 회수 | #019 |
  | **derivative는 스칼라 곱 공식** (df(x)*gy) | step34+ 야코비안 필요 | backward 직접 오버라이드로 전환 | #013 |

  ★ 이 전제들이 다 성립하는 한, 현재 구조(self.output 단수, backward 단일 인자,
    derivative 단일/튜플 자유)가 유효. 어느 하나라도 깨지면 REZERO_CHANGES #019의
    "step34+ 진화 체크리스트"를 참조하여 진화시킬 것.

★ 박스 컨텍스트 3계층 (REZERO_CHANGES 항목 011):
  __call__ → Variable 흐름 / forward → 순전파 뼈대 / apply → 순수 계산
  역전파도 같은 3계층: fill_grad → 그래프 순회 / backward → 뼈대 / derivative → 도함수

참고 자료:
  - 원본 구현: steps/step13.py
  - 이전 step: rezero/steps/step12.py (가변 인수 개선 — 이번에 역전파 추가)
  - rezero 변형: REZERO_CHANGES 항목 010~017 (derivative hook, fill_grad 등)
  - 동시 언패킹(zip): exploration_07 A.7.6

검증 포인트:
  - z = add(square(x), square(y)); fill_grad(z) → x.grad=2x, y.grad=2y
  - Add 역전파: derivative (lambda _: 1) × upstream → 각 입력에 동일 upstream 전달
  - derivative hook이 단일(Square)/다변(Add) 모두에서 동작?

실행:
  uv run python rezero/steps/step13.py
"""

from abc import ABC
from collections.abc import Callable
from typing import Optional, override

import numpy as np


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환 (삼항 1줄화, 항목 2)."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    step12와 동일. 역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
    """

    def __init__(self, data: Optional[np.ndarray]):
        # 방어막 2번: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록. step16 generation 확장 포인트."""
        self.creator = func


class Function(ABC):
    """DeZero의 함수. ★ step13: 역전파 다변 버전 + derivative hook 시험대.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        # ★ step13: self.output 단수 (스칼라 출력 가정).
        # 책은 self.outputs 리스트(복수형)로 미래 확장(다출력) 대비하지만,
        # step13 시점엔 다출력 함수가 없으므로 스칼라 명시적으로 단수화 (REZERO_CHANGES #019).
        # ★★★ step34+ 다출력 함수 등장 시 self.outputs 복수로 진화 필요 (복선 회수 지점).
        self.output: Optional[Variable] = None

    def __call__(self, *inputs: Variable) -> Variable:
        # --- 회수 + 가드를 한 루프로 (step11 패턴 유지) ---
        xs = []
        for x in inputs:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        # --- 순전파: forward → 다시 Variable로 래핑 --------------------------------
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)                                    # 단일값도 튜플로 정규화

        # ★ 스칼라 출력 가정 — 출력 1개만 처리 (step13 시점)
        # 책은 리스트로 여러 개 담지만, 우린 단일 Variable로 직접 저장.
        # 다출력 함수(step34+) 오면 여기서 outputs 리스트로 진화.
        assert len(ys) == 1, f"step13은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- 계산 그래프 연결 (creator 설정) ----------------------------------------
        output.set_creator(self)
        self.inputs = inputs
        self.output = output
        return output

    # ===== 순전파 계열 (step11~12와 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (★ step13 핵심 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출). ★ step13: 단일 upstream (스칼라 출력 가정).

        ★ rezero 변형 유지 (항목 007) — 매개변수명 gy → upstream_grad:
          책 원본은 gy (역전파 입력 grad). 우리는 의미 투명하게 upstream_grad 사용.
          (step06에서 도입, step13에서도 유지 — rezero 정체성)

        ★ 책 step13 충실 — backward(self, upstream_grad) 단일 인자:
          step13 시점에선 출력이 스칼라 1개 → upstream도 1개. 다출력(step34+)은 아직 아님.
          (이전 초안에서 *gys 가변으로 너무 앞서감 — 수정)

        ★ 책 패턴 확장 — derivative는 단일/튜플 자유 + 부모 정규화:
          자식 derivative가 단일 도함수(Square) or 튜플(Add) 자유롭게 반환.
          부모에서 isinstance 체크로 튜플 정규화 후 zip 처리.

        ★ 스칼라 출력 가정 — 단일 upstream을 각 입력의 편도함수에 곱함:
          derivative hook의 df(x)*upstream 공식은 출력 y가 1개(스칼라)일 때 성립.
          그 1개의 upstream을 각 입력의 편도함수에 곱함. (브로 통찰 "스칼라 전용" 실증)
        """
        # ★ 방어막: inputs는 __call__ 후 반드시 존재 (불변조건)
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        # --- 도함수 획득 + 정규화 (단일/튜플 → 튜플) --------------------------------
        # ★ partials = 편도함수(partial derivatives)들. 정규화 후엔 무조건 튜플(복수).
        partials = self.derivative()
        if not isinstance(partials, tuple):
            partials = (partials,)                     # 단일 도함수도 튜플로 정규화

        # --- 다변 fold step — 각 입력별로 편도함수 평가 × 동일한 upstream -------------
        # ★ 가정: 출력이 1개(스칼라) → upstream_grad도 1개 → 각 입력에 동일 upstream 곱함.
        # 다출력(step34+)이면 각 입력마다 다른 upstream 곱해야 하지만, step13 시점엔 해당 없음.
        # ★ zip 동시 순회 (inputs, 편도함수들) — A.7.6 동시 언패킹
        input_grads = []
        for x, df in zip(self.inputs, partials):
            # 방어막 3번: x.data Optional — None 가드
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

            local_deriv = df(x.data)                   # ① 편도함수 평가 (현재 입력에서)
            input_grads.append(local_deriv * upstream_grad)  # ② fold step (곱해서 누적)

        return tuple(input_grads)

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. ★ step13: 단일 OR 튜플 자유 (부모에서 정규화).

        ★ 스칼라 출력 전용 (브로 통찰):
          df(x) * gy 공식은 출력 y가 스칼라일 때만 성립.
          벡터/행렬 출력(step34+)은 backward 직접 오버라이드.
        ★ 다변 다입력 함수(Add)는 튜플 반환 — 각 편도함수 제공.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 =====
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        # ★ 단일 입력 → 단일 도함수 반환 (부모에서 튜플로 정규화)
        return lambda x: 2 * x


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. ★ 다입력 함수.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1 (각 편도함수 = 상수함수, 브로 통찰).
    역전파: derivative (lambda _: 1) × upstream → 각 입력에 동일 upstream 전달.
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        # --- 연산 + 포장 ---
        y = x0 + x1

        return y

    @override
    def derivative(self) -> tuple[Callable, ...]:
        # ★★★ 브로 통찰 — Add 편도함수 = 상수함수 (FP의 const(1))!
        # ∂y/∂x_i = 1 = "입력 무시하고 항상 1 반환" = lambda _: 1
        # 각 입력별 편도함수를 튜플로 반환 (부모 zip 처리용)
        return (lambda _: 1, lambda _: 1)


# ===== wrapper 함수 (step12 스타일) =====
def add(x0: Variable, x1: Variable) -> Variable:
    """덧셈 wrapper."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


# ★★★ step13 핵심 — fill_grad 다변 버전 (step08 fill_grad 진화) -----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step13: 다변 "입력" + 스칼라 "출력" 버전.

    step08~10에선 단일 입출력이었으나, step11~13의 가변 인수에 맞춰 진화:
      - 출력은 여전히 1개(스칼라) 가정 → f.output.grad 직접 회수 (단일 upstream, REZERO_CHANGES #019)
      - 역전파 호출: f.backward(upstream_grad) — 단일 인자 (★ 책 step13 충실)
      - 정규화: backward 반환 단일값도 튜플로 (책 패턴)
      - zip 배분: for x, input_grad in zip(f.inputs, input_grads) (★ A.7.6 동시 언패킹)
    """
    # --- 도입부 guard (검증 A: 사용자 오용 — 항목 016 fail-fast 원칙) -------------
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    # --- 시작점 grad 초기화 (3단계 우선순위 — 항목 014) -------------------------
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        if start_var.data is None:
            raise RuntimeError(f"{start_var!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")
        start_var.grad = np.ones_like(start_var.data)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm) ----------------
    worklist: Worklist = [start_var.creator]
    while worklist:
        f = worklist.pop()

        # ★ 방어막: 불변조건 (f.inputs/f.output은 __call__ 후 존재)
        assert f.inputs is not None and f.output is not None, "f.inputs/f.output must be set"

        # --- 단일 출력의 grad 회수 (스칼라 출력 가정 — step13 시점) ----------------
        # ★ self.output 단수 (REZERO_CHANGES #019). 다출력(step34+)에선 outputs로 진화.
        output = f.output
        assert output.grad is not None, "output.grad must be filled"
        upstream_grad = output.grad

        # --- 역전파 호출 (단일 upstream_grad) + 정규화 (책 패턴) --------------------
        input_grads = f.backward(upstream_grad)
        if not isinstance(input_grads, tuple):
            input_grads = (input_grads,)                # 단일값도 튜플로 정규화

        # --- 다변 배분: 입력과 grad 짝지어 할당 (★ A.7.6 동시 언패킹) -------------
        for x, input_grad in zip(f.inputs, input_grads):
            x.grad = input_grad

            if x.creator is not None:
                worklist.append(x.creator)


# --- 데모: step13 다변 역전파 검증 (정답지 step13.py와 동일) -------------------
if __name__ == "__main__":
    print("=== step13 다변 역전파 데모 ===")
    print("z = add(square(x), square(y))  (x=2, y=3)")
    print("기대: z = 2² + 3² = 13, x.grad = 2x = 4, y.grad = 2y = 6")
    print()

    x = Variable(np.array(2.0))
    y = Variable(np.array(3.0))

    z = add(square(x), square(y))
    fill_grad(z)

    print(f"z      = {z.data}  (기대: 13.0)")
    print(f"x.grad = {x.grad}  (기대: 4.0 = 2*2)")
    print(f"y.grad = {y.grad}  (기대: 6.0 = 2*3)")
    print()

    # ★ derivative hook 검증 — Add가 상수함수로 역전파 잘 하는지
    print("★ derivative hook 다변 동작 확인:")
    print(f"  Add.derivative() = {Add().derivative()}")
    print(f"  → 2개 상수함수 (lambda _: 1) 튜플 — 브로 통찰!")
