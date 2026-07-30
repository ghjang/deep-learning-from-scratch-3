"""
rezero.steps.step14 — [2고지] 같은 변수 반복 사용
===============================================

★ 가변 길이 인수 3부작(step11~13) 완결 후 새 패턴.
  같은 Variable이 계산 그래프에서 여러 번 사용될 때 gradient가 올바르게 **누적**되도록 수정.

이 step에서 배울 것:
  - gradient 누적 — x.grad = gx (대입) → if None: 대입 else: 누적(+)
  - Variable.clear_grad() 메서드 — grad 초기화 (Variable 재사용 시)
  - ★ ndarray in-place 부작용 방지 — += 대신 명시적 x.grad + gx

★ 핵심 문제 — 같은 변수 반복 사용 시 gradient 덮어쓰기 버그:
  ```python
  y = add(x, x)   # x가 x0, x1 양쪽에 사용
  # step13: x.grad = gx1 (마지막만 남음) → 버그
  # step14: x.grad = gx0 + gx1 = 2*gy (두 경로 합산) ★
  ```

★ 이 코드의 가정/전제 (step13 가정 + step14 새 가정):
  step13의 "스칼라 출력 가정" 표 참조 + 이번 step에서 추가된 가정:

  | 전제 | 의미 | 관련 |
  |---|---|---|
  | **계산 그래프는 순전파 시 매번 재생성** | Define-by-Run 핵심 가정. 같은 Variable 재사용해도 새 그래프 생성 → 이전 grad 잔류 가능 → clear_grad()로 초기화 필요 | 이 step |
  | **같은 Variable이 여러 입력으로 전달 가능** | `add(x, x)` → f.inputs = (x, x). zip 순회 시 같은 객체 2번 방문 → 누적 로직(if None) 필요 | 이 step |

  ★ Define-by-Run 가정의 의미 (clear_grad가 존재하는 이유):
    Define-by-Run은 순전파 실행 시점에 계산 그래프를 "생성"하는 패러다임.
    (cf. Define-and-Run은 그래프를 미리 정의해두고 데이터만 흘림)
    → 같은 Variable 객체로 두 번째 forward를 실행하면:
      1. 새 계산 그래프가 생성됨 (creator 링크 갱신)
      2. 하지만 Variable.grad는 이전 역전파 결과가 그대로 남음 ★
      3. 그 상태로 fill_grad 돌리면 이전 grad에 새 grad가 잘못 누적됨 (버그)
    → 그래서 사용자가 명시적으로 `x.clear_grad()`로 초기화해야 올바른 결과.
    상세: exploration_03 (Define-by-Run vs Define-and-Run), exploration_11 §7, exploration_16 §부작용

★ 왜 `+=`가 아니라 `x.grad = x.grad + gx`인가 (학습 포인트):
  - `+=`는 ndarray in-place 연산 → 부작용 가능 (다른 Variable이 같은 배열 참조 시)
  - 명시적 `x.grad + gx` → 새 배열 생성, 안전
  - 책의 선택이자 파이썬 ndarray 다룰 때 중요한 이디엄

참고 자료:
  - 원본 구현: steps/step14.py
  - 이전 step: rezero/steps/step13.py (가변 인수 역전파 — 이번에 누적 로직 추가)
  - rezero 변형: REZERO_CHANGES 항목 014~017 (fill_grad), 019 (output 단수)

검증 포인트:
  - add(x, x) → x.grad = 2 (gy+gy, 두 경로 합산)
  - add(add(x, x), x) → x.grad = 3 (x 세 번 사용)
  - clear_grad()로 이전 grad 초기화 후 재계산

실행:
  uv run python rezero/steps/step14.py
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

    ★ step14 추가: clear_grad() 메서드 — grad 초기화 (Variable 재사용 시).
    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
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

    def clear_grad(self) -> None:
        """★ step14 추가 — grad 초기화.

        같은 Variable을 두 번째 계산에 재사용하면 이전 grad가 남아서 잘못 누적됨.
        그래서 사용자가 명시적으로 clear_grad()로 초기화.
        cf. PyTorch의 `variable.grad.zero_()` / `variable.grad = None`과 같은 역할.

        ★★ 왜 필요한가 — Define-by-Run 가정:
          Define-by-Run은 순전파 시점에 계산 그래프를 "매번 생성"함.
          같은 Variable로 두 번째 forward → 새 그래프 생성 + 이전 grad 잔류 → 잘못 누적.
          그래서 재사용 전 clear_grad()로 초기화해야 올바른 역전파 결과.
          (cf. Define-and-Run은 그래프 고정이라 이 문제 없음 — 패러다임 차이)

        ★★ rezero 변형 — 책 원본은 `cleargrad` (언더스코어 없음).
        하지만 같은 클래스에 `set_creator` (언더스코어 있음)가 있어서 스네이크 케이스 불일치.
        rezero는 PEP 8 일관성 위해 `clear_grad`로 수정 (REZERO_CHANGES 항목 021).
        """
        self.grad = None


class Function(ABC):
    """DeZero의 함수. ★ step14: step13 구조 유지 + fill_grad에 누적 로직 추가.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        # ★ step13: self.output 단수 (스칼라 출력 가정, REZERO_CHANGES #019).
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
        assert len(ys) == 1, f"step13/14은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- 계산 그래프 연결 (creator 설정) ----------------------------------------
        output.set_creator(self)
        self.inputs = inputs
        self.output = output
        return output

    # ===== 순전파 계열 (step11~13과 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13과 동일 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출). ★ step13과 동일 (누적은 fill_grad 쪽).

        ★ rezero 변형 유지 (항목 007) — 매개변수명 gy → upstream_grad.
        ★ 스칼라 출력 가정 — 단일 upstream을 각 입력의 편도함수에 곱함.
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
        # 다출력(step34+)이면 각 입력마다 다른 upstream 곱해야 하지만, step13/14 시점엔 해당 없음.
        # ★ zip 동시 순회 (inputs, 편도함수들) — A.7.6 동시 언패킹
        downstream_grads = []
        for x, df in zip(self.inputs, partials):
            # 방어막 3번: x.data Optional — None 가드
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

            local_deriv = df(x.data)                   # ① 편도함수 평가 (현재 입력에서)
            downstream_grads.append(local_deriv * upstream_grad)  # ② fold step (곱해서 누적)

        return tuple(downstream_grads)

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. ★ step13과 동일 — 단일 OR 튜플 자유 (부모에서 정규화).

        ★ 스칼라 출력 전용 (브로 통찰):
          df(x) * gy 공식은 출력 y가 스칼라일 때만 성립.
          벡터/행렬 출력(step34+)은 backward 직접 오버라이드.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 (step13과 동일) =====
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
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
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:
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


# ★★★ step14 핵심 — fill_grad 다변 버전 + gradient 누적 (step13 fill_grad 진화) -------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step14: gradient 누적 추가.

    step08~13에선 x.grad = gx (대입) → 같은 변수 반복 시 덮어쓰기 버그.
    step14: if None: 대입 else: 누적(+) → 같은 변수 여러 경로 grad 합산 ★

    step13과의 차이점 (유일):
      - zip 배분 루프에서 x.grad = downstream_grad (대입)
        → if x.grad is None: 대입 else: x.grad = x.grad + downstream_grad (누적)
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
        downstream_grads = f.backward(upstream_grad)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)      # 단일값도 튜플로 정규화

        # --- 다변 배분: 입력과 grad 짝지어 할당 (★ A.7.6 동시 언패킹) -------------
        # ★★★ step14 핵심 — gradient 누적 (같은 변수 반복 사용 대응)
        #
        # ★ 왜 if None 체크가 필요한가? (핵심 학습 포인트)
        #   같은 Variable 객체가 하나의 Function에 여러 입력으로 전달될 수 있음:
        #     y = add(x, x)   # f.inputs = (x, x) — ★ 같은 객체 2번!
        #   이때 zip(f.inputs, downstream_grads)는 같은 x를 2번 순회:
        #     1차: (x, gx0) → x.grad = gx0 (처음엔 None이니 대입)
        #     2차: (x, gx1) → x.grad 이미 채워져 있음 → ★ 여기서 누적하지 않으면 gx0 덮어쓰기!
        #   그래서 if x.grad is None: 대입 else: 누적 — "같은 객체 두 번째 방문엔 더해라"
        #
        # 이전(step13): x.grad = downstream_grad (무조건 대입 → 두 번째가 첫 번째 덮어쓰기 버그)
        # 이후(step14): if None: 대입 else: 누적 → 같은 Variable이 여러 입력으로 와도 grad 합산
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad                # 최초 방문: 대입
            else:
                x.grad = x.grad + downstream_grad       # ★ 재방문: 누적 (+= 아님, 명시적 +)

            if x.creator is not None:
                worklist.append(x.creator)


# --- 데모: step14 gradient 누적 검증 (정답지 step14.py와 동일) ------------------
if __name__ == "__main__":
    print("=== step14 gradient 누적 데모 ===")
    print()

    # --- 케이스 1: 같은 변수 2회 사용 ---
    print("[1] y = add(x, x)  (x=3.0) — x가 양쪽에 사용")
    x = Variable(np.array(3.0))
    y = add(x, x)
    fill_grad(y)
    print(f"    y = {y.data}  (기대: 6.0 = 3+3)")
    print(f"    x.grad = {x.grad}  (기대: 2.0 = gy+gy, 두 경로 합산)")
    print(f"    ★ step13이었다면 x.grad=1.0 (덮어쓰기 버그). 누적 덕분에 2.0 ✅")
    print()

    # --- 케이스 2: 같은 변수 3회 사용 ---
    print("[2] y = add(add(x, x), x)  (x=3.0) — x 세 번 사용")
    x = Variable(np.array(3.0))   # 새 객체 (또는 x.clear_grad())
    y = add(add(x, x), x)
    fill_grad(y)
    print(f"    y = {y.data}  (기대: 9.0 = (3+3)+3)")
    print(f"    x.grad = {x.grad}  (기대: 3.0 = gy+gy+gy, 세 경로 합산)")
    print()

    # --- 케이스 3: clear_grad() 효과 ---
    print("[3] clear_grad()로 이전 grad 초기화 후 재계산")
    x = Variable(np.array(3.0))
    y = add(x, x)
    fill_grad(y)
    print(f"    1차: x.grad = {x.grad}  (기대: 2.0)")
    x.clear_grad()                                    # ★ 명시적 초기화
    print(f"    clear_grad 후: x.grad = {x.grad}")
    y2 = square(x)
    fill_grad(y2)
    print(f"    2차 (square): x.grad = {x.grad}  (기대: 6.0 = 2*3, 이전 grad 영향 없음)")
