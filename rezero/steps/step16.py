"""
rezero.steps.step16 — [2고지] 복잡한 계산 그래프(구현 편)
===============================================

★ step15(이론 편)에서 다룬 "분기/합류 복잡 그래프에서 역전파 순서 꼬임"을 코드로 해결.
  도구 = generation(순전파 깊이) + visited(같은 Function 중복 처리 방지).

이 step에서 배울 것:
  - generation — 순전파 깊이 기록. Function/Variable 양쪽에 부여.
  - visited (set) — 같은 Function이 worklist에 중복 push되는 것 방지.
  - worklist를 generation 내림차순 정렬 — 역방향 위상 정렬(topological sort) 구현.
  - schedule 클로저 — "미방문 Function을 worklist에 예약 (위상 순서 유지)" 묶음 처리.

★★★ step14 → step16 변화 (원본 4군데):
  | 위치                       | step14               | step16                                    |
  |---------------------------|----------------------|-------------------------------------------|
  | Variable.__init__         | (generation 없음)     | self.generation = 0 추가                   |
  | Variable.set_creator      | creator만 설정        | + self.generation = func.generation + 1   |
  | Function.__call__         | (generation 없음)     | self.generation = max(inputs' generation) |
  | fill_grad 역전파          | worklist LIFO만       | + visited(중복방지) + generation 정렬      |

★ 크로스 참조 네이밍 — 책 원본 이름 유지 (REZERO_CHANGES 항목 025 이력 참조):
  step16 진행 중 브로 통찰로 creator → creator_func 등 전면 개명을 시도했으나,
  "변수명과 타입 힌트의 중복(헝가리안 표기법 냄새)"을 자각하고 ★ 철회.
  → 현대 파이썬 철학 "이름은 역할, 타입은 힌트에 맡긴다"에 따라 책 원본 이름 유지.
  → 이 왔다 갔다 자체가 학습 가치. 상세: REZERO_CHANGES 항목 025 + notes/exploration_19_*.md.

★ 복선 회수 포인트 (이번 step의 하이라이트):
  1. REZERO_CHANGES 항목 012 회수 — step07에서 "왜 set_creator를 메서드로 뒀을까?" 의심한 것.
     답: set_creator에 generation 로직이 추가되는 순간이 바로 step16.
     step14 docstring에 "step16 generation 확장 포인트" 적어둔 복선이 드디어 회수됨.
  2. exploration_18 §4.4 회수 — 브로가 step15 탐구 때 "방문 기록(visited)이 왜 필요한가" 파고들었던 주제.
     책 원본의 seen_set이 바로 그 visited의 실체.

★ 이 코드의 가정/전제 (step14 전제 + step16 새 전제 2개):
  step13/14의 "스칼라 출력 가정" 표 참조 + 이번 step에서 추가된 가정:

  | 새 전제 (step16)                                  | 의미                                                        | 깨지면?                                              |
  |--------------------------------------------------|-------------------------------------------------------------|-----------------------------------------------------|
  | 계산 그래프는 DAG (역전파 위상순서 존재)           | generation 정렬이 가능한 전제. 사이클 있으면 위상정렬 불가   | Define-by-Run에선 사이클 안 생김 — 항상 성립          |
  | 같은 Function이 worklist에 중복 push 될 수 있다    | add(square(a), square(a)) 식에서 a.creator가 두 번 push됨    | visited 없으면 a.grad 두 번 누적 버그 → visited로 방어 |

  ★ 핵심 학습 포인트 — step14 누적 vs step16 visited (둘은 다른 문제!):
    - step14 누적(if None: 대입 else: +): "같은 Variable이 하나의 Function에 여러 입력으로" 다룸
      예: add(x, x) → f.inputs = (x, x). 같은 객체 2번 방문.
    - step16 visited(set): "같은 Function이 worklist에 여러 번 push" 다룸
      예: add(square(a), square(a)) → a.creator(square 함수)가 두 번 push됨.
    - 둘이 헷갈리기 쉬운데, 계산 그래프의 서로 다른 구조적 상황을 해결하는 서로 다른 방어막.

참고 자료:
  - 원본 구현: steps/step16.py
  - 이전 step: rezero/steps/step14.py (같은 변수 반복 — 이번에 generation + visited 추가)
  - rezero 변형: REZERO_CHANGES 항목 012 (set_creator 복선 회수), 014~017 (fill_grad/worklist),
    019 (output 단수), 025 (크로스 참조 네이밍 — 시도/철회/교훈 이력)
  - 이론 배경: notes/exploration_18_graph_traversal.md (DAG/위상정렬/generation = 표현식 중첩 깊이)
  - 네이밍 교훈: notes/exploration_19_naming_hungarian.md (헝가리안 vs 현대 Pythonic)

검증 포인트:
  - 분기/합류 그래프: x → square → a → square/square → add → y
    y = add(square(a), square(a)) where a = square(x), x = 2.0
    기대: y.data = 32.0, x.grad = 64.0
  - visited 없으면 x.grad가 잘못 누적됨 (square(a)의 두 역전파가 a.creator를 중복 push)

실행:
  uv run python rezero/steps/step16.py
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
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    ★ step16 추가: generation 필드 — 순전파 깊이 기록.
      역전파 시 worklist를 generation 내림차순 정렬 → 역방향 위상 정렬 보장.
    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).

    ★ 네이밍 (REZERO_CHANGES 항목 025 — 시도/철회 이력):
      creator는 "역할"을 말하고, 타입(Function)은 타입 힌트에 맡김 → 현대 Pythonic.
      (creator_func로 개명 시도했으나 "타입 힌트와 중복" 자각하여 철회)
    """

    def __init__(self, data: Optional[np.ndarray]):
        # 방어막 2번: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0                          # ★ step16 추가 — 순전파 깊이

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속.

        ★★★ step16 — REZERO_CHANGES 항목 012 복선 회수!
          step07에서 "왜 set_creator를 단순 할당 말고 메서드로 뒀을까?" 의심했음.
          답이 바로 이곳 — set_creator가 generation 로직까지 담당.
          "부모 Function의 generation + 1"을 자신의 generation으로 설정.

        generation 의미 (exploration_18 §6 "generation = 표현식 중첩 깊이"):
          - 순전파 시점에 런타임으로 결정되는 값 (Define-by-Run의 정수)
          - 출력에 가까울수록(=표현식이 깊게 중첩될수록) generation이 큼
          - 역전파는 generation 큰 순서(출력에 가까운 순)로 처리해야 올바른 누적 순서 보장
        """
        self.creator = func
        self.generation = func.generation + 1             # ★ step16 — 부모 gen + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021 (cleargrad → clear_grad 스네이크 일관성)."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. ★ step16: generation 필드 추가 + __call__에서 설정.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.

    ★ 네이밍 (REZERO_CHANGES 항목 025 — 시도/철회 이력):
      inputs/output은 "역할"을 말하고, 타입(Variable)은 타입 힌트에 맡김 → 현대 Pythonic.
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        # ★ step13: self.output 단수 (스칼라 출력 가정, REZERO_CHANGES 항목 019).
        # ★★★ step34+ 다출력 함수 등장 시 self.outputs 복수로 진화 필요 (복선 회수 지점).
        self.output: Optional[Variable] = None
        self.generation: int = 0                          # ★ step16 추가 — 순전파 깊이

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
        assert len(ys) == 1, f"step13/14/16은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- ★ step16: generation 설정 (입력들 중 가장 큰 generation 승계) -----------
        # 핵심: Function의 generation = "출력에서 가장 먼 입력의 깊이" = 순전파 깊이.
        # 여러 입력이 다른 깊이에서 왔을 수 있으니 max로 통일 (가장 깊은 쪽에 맞춤).
        self.generation = max([x.generation for x in inputs])

        # --- 계산 그래프 연결 (creator 설정 — 여기서 output.generation도 같이 설정됨) ---
        output.set_creator(self)
        self.inputs = inputs
        self.output = output
        return output

    # ===== 순전파 계열 (step11~14와 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13~14와 동일 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출). ★ step13~16 동일 (누적은 fill_grad 쪽).

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
        # 다출력(step34+)이면 각 입력마다 다른 upstream 곱해야 하지만, step13~16 시점엔 해당 없음.
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
        """도함수 hook. ★ step13~16과 동일 — 단일 OR 튜플 자유 (부모에서 정규화).

        ★ 스칼라 출력 전용 (브로 통찰):
          df(x) * gy 공식은 출력 y가 스칼라일 때만 성립.
          벡터/행렬 출력(step34+)은 backward 직접 오버라이드.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 (step13~14와 동일) =====
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
        return x0 + x1

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


# ★★★ step16 핵심 — fill_grad에 generation 정렬 + visited(중복방지) 추가 -----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step16: generation 정렬 + visited 추가.

    step14까진 worklist LIFO만 썼지만, 복잡한(분기/합류) 그래프에선 순서가 꼬일 수 있음.
    step16 해법:
      1. visited (set) — 같은 Function이 worklist에 중복 push되는 것 방지.
      2. generation 내림차순 정렬 — 역방향 위상 정렬(topological sort) 보장.
         (출력에 가까운 = generation 큰 Function부터 처리)

    ★ 역전파 순서가 왜 중요한가 (exploration_18 §6 "문제 — DFS 순서 꼬임"):
      분기/합류 그래프에서 단순 LIFO는 "아직 grad가 다 안 모인 Function"을 먼저 처리할 위험.
      generation 정렬이 이걸 막음 — 모든 입력의 grad가 모이는 순서(=위상 정렬)를 강제.

    ★ schedule 클로저 (rezero 변형 — 책의 add_func에서 리네임):
      "아직 방문 안 한 Function을 worklist에 예약(위상 순서 유지하며)"을 한 번에 처리.
      - visited 체크 → worklist append → generation 정렬을 하나의 동작으로 캡슐화.
      - schedule + worklist + visited = 그래프 순회 알고리즘의 CS 학술 용어 셋트
        (탐구 18번과 네이밍 일치 → 코드만 봐도 "역방향 위상 정렬 중"이 드러남).
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

    # --- 메인 루프 상태 (step16 핵심 — worklist + visited + schedule 클로저) -------
    worklist: Worklist = []
    visited: set[Function] = set()                       # ★ step16 — 중복 push 방지

    def schedule(f: Function) -> None:
        """★ 미방문 Function을 worklist에 예약 (generation 내림차순 정렬 유지).

        책 원본 add_func에서 리네임 — "위상 순서에 맞춰 처리 예약" 의미 명시.
        schedule + worklist + visited = 그래프 순회 알고리즘의 학술 용어 셋트.

        ★ 왜 매번 sort가 필요한가:
          새 Function이 push되면 기존 worklist의 위상 순서가 깨질 수 있음.
          (예: gen 3인 f 처리 중 gen 1인 g가 push → g는 gen 3보다 나중에 와야 함)
          가장 단순한 구현 = 매 push마다 전체 sort. (heapq로 최적화 가능 — step16+ 탐구 후보)
        """
        if f not in visited:
            worklist.append(f)
            visited.add(f)
            worklist.sort(key=lambda func: func.generation)  # ★ gen 오름차순 → pop()이 큰 것부터

    schedule(start_var.creator)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm + 위상 정렬) ------
    while worklist:
        f = worklist.pop()                               # ★ gen 큰 것(=출력에 가까운 것)부터 pop

        # ★ 방어막: 불변조건 (f.inputs/f.output은 __call__ 후 존재)
        assert f.inputs is not None and f.output is not None, "f.inputs/f.output must be set"

        # --- 단일 출력의 grad 회수 (스칼라 출력 가정 — step13 시점) ----------------
        # ★ self.output 단수 (REZERO_CHANGES 항목 019). 다출력(step34+)에선 outputs로 진화.
        output = f.output
        assert output.grad is not None, "output.grad must be filled"
        upstream_grad = output.grad

        # --- 역전파 호출 (단일 upstream_grad) + 정규화 (책 패턴) --------------------
        downstream_grads = f.backward(upstream_grad)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)      # 단일값도 튜플로 정규화

        # --- 다변 배분: 입력과 grad 짝지어 할당 (★ A.7.6 동시 언패킹) -------------
        # ★★★ step14 핵심 (유지) — gradient 누적 (같은 변수 반복 사용 대응)
        #
        # ★ 왜 if None 체크가 필요한가? (step14 학습 포인트)
        #   같은 Variable 객체가 하나의 Function에 여러 입력으로 전달될 수 있음:
        #     y = add(x, x)   # f.inputs = (x, x) — ★ 같은 객체 2번!
        #   이때 zip(f.inputs, downstream_grads)는 같은 x를 2번 순회:
        #     1차: (x, gx0) → x.grad = gx0 (처음엔 None이니 대입)
        #     2차: (x, gx1) → x.grad 이미 채워져 있음 → ★ 여기서 누적하지 않으면 gx0 덮어쓰기!
        #   그래서 if x.grad is None: 대입 else: 누적 — "같은 객체 두 번째 방문엔 더해라"
        #
        # ★ step14 누적 vs step16 visited (둘은 다른 문제! — 헷갈림 주의):
        #   - step14 누적(if None): "같은 Variable이 하나의 Function에 여러 입력으로" 다룸
        #   - step16 visited(set) : "같은 Function이 worklist에 여러 번 push" 다룸
        #   - 계산 그래프의 서로 다른 구조적 상황을 해결하는 서로 다른 방어막.
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad                # 최초 방문: 대입
            else:
                x.grad = x.grad + downstream_grad       # ★ 재방문: 누적 (+= 아님, 명시적 +)

            if x.creator is not None:
                schedule(x.creator)                     # ★ step16 — visited + 정렬 묶어 처리


# --- 데모: step16 분기/합류 그래프 검증 (정답지 step16.py와 동일 시나리오) ----------
if __name__ == "__main__":
    print("=== step16 복잡한 계산 그래프(구현 편) 데모 ===")
    print()

    # --- 케이스 1: 책 step16의 핵심 데모 — 분기/합류 그래프 ---
    # 그래프 구조 (★ a에서 분기 → 합류):
    #   x(2.0) → square → a(4.0)
    #                     ├── square → b(16.0) ┐
    #                     └── square → c(16.0) ┘ add → y(32.0)
    #
    # ★ 핵심: square(a)가 두 번 호출 → 두 Square의 입력이 같은 a.
    #   역전파 시 두 Square 각각이 a.creator(첫 square 함수)를 schedule → 같은 square가 2번 push됨.
    #   visited 없으면 a.creator를 2번 처리 → x.grad 2번 누적 → 잘못된 결과.
    print("[1] y = add(square(a), square(a))  where a = square(x), x = 2.0")
    print("    (분기/합류 그래프 — visited + generation 정렬의 시험대)")
    x = Variable(np.array(2.0))
    a = square(x)
    y = add(square(a), square(a))
    fill_grad(y)
    print(f"    y.data = {y.data}  (기대: 32.0)")
    print(f"    x.grad = {x.grad}  (기대: 64.0)")
    print()

    # --- x.grad = 64 인 역전파 추적 (손계산 검증) ---
    # 순전파: a = x² = 4, b = c = a² = 16, y = b + c = 32 ✓
    # 역전파:
    #   y 시드 = 1
    #   add:       b.grad = 1, c.grad = 1                       (upstream 1을 양쪽에 그대로)
    #   square(b): db/da = 2a = 8 × b.grad(1) = 8 → a
    #   square(c): dc/da = 2a = 8 × c.grad(1) = 8 → a
    #   a.grad = 8 + 8 = 16                                     (★ 두 경로 누적)
    #   square(a): da/dx = 2x = 4 × a.grad(16) = 64 → x
    #   x.grad = 64 ✓
    print("[역전파 추적] a.grad = 16 (8+8, 두 경로 누적) → x.grad = 64 (4×16)")
    print()

    # --- 케이스 2: visited 없으면 어떻게 되나 (개념 설명 — 현재 코드엔 토글 없음) ---
    print("[2] 왜 visited가 필요한가 — 같은 Function 중복 push 문제")
    print("    add(square(a), square(a)) 역전파 시:")
    print("    - 두 Square 각각이 a.creator를 schedule 시도 → 같은 square가 2번 push됨")
    print("    - visited 없으면 a.creator를 2번 처리 → x.grad 2번 누적 → 128 (잘못)")
    print("    - visited 있으면 2번째 schedule은 no-op → x.grad = 64 (정확) ✓")
    print()

    # --- 케이스 3: generation 값 확인 (step16 학습 포인트 — 순전파 깊이 기록) ---
    print("[3] generation 값 확인 — 순전파 깊이 기록 (= 표현식 중첩 깊이)")
    x = Variable(np.array(2.0))
    a = square(x)
    y = add(square(a), square(a))
    # 각 단계의 generation:
    #   x(입력)              → gen 0 (기본)
    #   square(x)            → gen 0 (max(x.gen)=0).      a.gen = 0+1 = 1
    #   square(a) #1, #2     → gen 1 (max(a.gen)=1).      그 출력들 gen = 1+1 = 2
    #   add                  → gen 2 (max(입력들 gen 2)=2). y.gen = 2+1 = 3
    print(f"    x.generation = {x.generation}  (기대: 0)")
    print(f"    a.generation = {a.generation}  (기대: 1)")
    print(f"    y.generation = {y.generation}  (기대: 3)")
    print()

    print("=== step16 완료 — 분기/합류 그래프 역전파 올바르게 동작 ===")
