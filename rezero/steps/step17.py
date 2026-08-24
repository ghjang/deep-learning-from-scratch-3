"""
rezero.steps.step17 — [2고지] 메모리 관리와 순환 참조
===============================================

★ step16의 계산 그래프 역전파는 완성됐지만, 메모리 누수 문제가 남아있음.
  순환 참조(Variable ↔ Function)를 weakref(약한 참조)로 끊어 해결.

이 step에서 배울 것:
  - 순환 참조(circular reference) — Variable.creator ↔ Function.output이 서로 강하게 참조
  - weakref.ref() — 참조 카운트 올리지 않는 "약한 참조"
  - Function.output을 weakref로 잡아 순환 끊기 (★ 단수 정책 항목 019 유지)

★★★ 핵심 문제 — 순환 참조로 인한 메모리 누수:
  계산 그래프의 객체 연결 구조:
    Variable ──creator──→ Function ──inputs──→ Variable
       ↑                                        │
       └────────────────────────────────────────┘
       ★ 순환! Function이 Variable을 알고, Variable이 Function을 앎

  파이썬의 참조 카운팅 GC는 순환 참조를 못 잡음 (서로 참조 카운트 0 안 됨).
  → 계산 그래프가 메모리에 계속 남음. 대규모 계산 시 메모리 누수.

★ 해법 — weakref (약한 참조):
  weakref.ref(x)는 x를 참조 카운트 올리지 않고 가리킴.
  → x가 다른 곳에서 안 쓰이면 (참조 카운트 0되면) 즉시 회수됨.
  Function이 output을 weakref로 잡으면, output Variable이 다른 곳에서 안 쓰이면 자동 회수.
  순환 끊김 → 참조 카운팅 GC가 정상 동작.

★ 책의 선택 — outputs만 weakref, inputs는 강한 참조 유지:
  | 참조                       | step16     | step17          | 이유                              |
  |---------------------------|------------|-----------------|-----------------------------------|
  | Function.inputs → Variable | 강한 참조   | 강한 참조 (유지) | 역전파 시 inputs.data 필요         |
  | Function.output → Variable | 강한 참조   | 약한 참조 (weakref) | 역전파 후엔 output 필요 없음 → 회수 허용 |

  비대칭: inputs는 살려두고, output만 약하게 잡음. 이게 핵심 설계 결정.

★★★ ★ 정정 — weakref는 출력 다변화와 별개 (브로 통찰):
  weakref는 순환 참조 끊기용이지, 출력 개수와 무관.
  - 순환 참조: 단일 출력이든 복수 출력이든 발생
  - 출력 다변화: step34+ 진짜 다출력 함수(Split 등)와 무관

  우리 rezero는 항목 019(self.output 단수)를 유지한 채 **단수 + weakref** 조합으로 진행.
  항목 019 회수는 step34+ 진정한 다출력 함수 등장 시점으로 유지.

  책이 self.outputs(복수)를 쓰는 건 원래 step13부터 복수였기 때문 (전진 설계).
  우리는 단수를 택했으니 단수에 weakref 얹는 게 자연스러움.

★ 브로 통찰 — GC는 순환 참조를 결국 잡지만:
  파이썬 GC는 두 단계:
    1. 참조 카운팅 (즉시, 순환 못 잡음)
    2. 세대별 순환 감지 GC (주기적, 순환 잡음)
  즉 순환 참조는 결국 회수됨. 근데 딥러닝의 큰 ndarray는 GC 주기까지 기다리면
  메모리 폭발 → weakref로 즉시 회수 확보.
  상세: notes/exploration_22_weakref_gc.md (브로 질문 — weakref 객체 동작 메커니즘 포함)

★ 이 코드의 가정/전제 (step16 전제 + step17 새 전제):
  step16의 전제표 참조 + 이번 step에서 추가된 가정:

  | 새 전제 (step17)                                       | 의미                                     | 깨지면?                              |
  |--------------------------------------------------------|------------------------------------------|-------------------------------------|
  | Function은 자신의 출력 Variable을 약한 참조로 알아야 한다 | 역전파 시 grad 회수용                     | weakref로 잡되, 순환 참조 회피       |
  | 순전파 후 출력 Variable은 사용자 손에서 곧 버려질 수 있다 | 대규모 계산에서 y를 다시 안 씀            | weakref가 회수 허용 → 메모리 절약    |
  | inputs는 역전파 때까지 살아있어야 한다                  | 역전파에 inputs.data 필요                 | 강한 참조 유지                       |

참고 자료:
  - 원본 구현: steps/step17.py
  - 이전 step: rezero/steps/step16.py (generation/visited — 이번에 weakref 추가)
  - rezero 변형: REZERO_CHANGES 항목 019 (output 단수 — 유지), 026 (weakref 도입)
  - 심화 배경: notes/exploration_22_weakref_gc.md (weakref/GC/CPython 내부)

검증 포인트:
  - 메모리 누수 테스트: for i in range(10): x = big_data; y = square(square(square(x)))
    step16 방식: 메모리 누수 (순환 참조 안 끊김, GC 주기까지 잔류)
    step17 방식: 메모리 안정 (weakref로 순환 끊김, 즉시 회수)
  - 정상 역전파: weakref 역참조(output())로 grad 회수 정상 동작

실행:
  uv run python rezero/steps/step17.py
"""

import weakref
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

    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
    """

    def __init__(self, data: Optional[np.ndarray]):
        # 방어막 2번: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021 (cleargrad → clear_grad)."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. ★ step17: output을 weakref로 잡아 순환 참조 끊기.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.

    ★ 네이밍 (REZERO_CHANGES 항목 019 + 026):
      output 속성은 단수 정책(항목 019)을 유지하되, step17부터 weakref로 잡음(항목 026).
      이름은 output 그대로, 타입 힌트만 Variable → weakref.ref로 진화.
      ★ 일관성 — step16에서 `creator_func` 시도/철회한 원칙(탐구 19번) 준수.
        "이름은 역할, 타입은 힌트에" — `output_ref`(output+ref 타입 인코딩)는 헝가리안.
      (cf. 책은 self.outputs = [weakref.ref(o)] 복수 리스트 — 우리는 단수 + weakref)
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        # ★ step17 — output을 weakref로 잡음 (순환 참조 끊기, 항목 026).
        # ★ step13 단수 정책(항목 019)은 유지 — output 하나 (복수 리스트 아님).
        # ★★★ step34+ 다출력 함수 등장 시에만 outputs 복수로 진화 (항목 019 회수 지점).
        # ★ 네이밍 — output 이름 유지, 타입 힌트만 Variable → weakref.ref로 진화.
        #   (`output_ref` 시도했다가 헝가리안 자각으로 철회 — 탐구 노트 19번 원칙 준수)
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

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

        # ★ 스칼라 출력 가정 — 출력 1개만 처리 (step13 시점, 항목 019)
        assert len(ys) == 1, f"step13~17은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- ★ step16: generation 설정 (입력들 중 가장 큰 generation 승계) -----------
        self.generation = max([x.generation for x in inputs])

        # --- 계산 그래프 연결 (creator 설정) ----------------------------------------
        output.set_creator(self)
        self.inputs = inputs
        # ★★★ step17 핵심 — output을 weakref로 잡아 순환 참조 끊기 ★★★
        # 이전(step16): self.output = output       (강한 참조 → 순환 참조 발생)
        # 이후(step17): self.output = weakref.ref(output)  (약한 참조 → 순환 끊김)
        #
        # ★ 왜 output만 weakref이고 inputs는 강한 참조인가?
        #   inputs는 역전파 시 inputs.data 접근에 반드시 필요 → 강한 참조 유지.
        #   output은 역전파 시 grad 회수용으로만 필요, 그 후엔 안 씀 → weakref로 회수 허용.
        #   이 비대칭이 메모리 효율과 역전파 정합성을 동시에 잡는 핵심 설계.
        self.output = weakref.ref(output)
        return output

    # ===== 순전파 계열 (step11~16과 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13~16과 동일 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출). ★ step13~17 동일.

        ★ rezero 변형 유지 (항목 007) — 매개변수명 `gy` → `upstream_grad`.
        ★ 스칼라 출력 가정 — 단일 upstream을 각 입력의 편도함수에 곱함.
        """
        # ★ 방어막: inputs는 __call__ 후 반드시 존재 (불변조건)
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        partials = self.derivative()
        if not isinstance(partials, tuple):
            partials = (partials,)                     # 단일 도함수도 튜플로 정규화

        downstream_grads = []
        for x, df in zip(self.inputs, partials):
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

            local_deriv = df(x.data)                   # ① 편도함수 평가 (현재 입력에서)
            downstream_grads.append(local_deriv * upstream_grad)  # ② fold step (곱해서 누적)

        return tuple(downstream_grads)

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. ★ step13~17과 동일 — 단일 OR 튜플 자유 (부모에서 정규화).

        ★ 스칼라 출력 전용 (브로 통찰):
          df(x) * upstream_grad 공식은 출력 y가 스칼라일 때만 성립.
          벡터/행렬 출력(step34+)은 backward 직접 오버라이드.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 (step13~16과 동일) =====
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


# ★★★ step17 핵심 — fill_grad에서 weakref 역참조로 output.grad 회수 -----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step17: weakref 역참조로 output.grad 회수.

    step16과의 차이 (유일):
      - f.output (직접 Variable 참조) → f.output() (weakref 역참조 호출)
        f.output 타입: weakref.ref → f.output() 반환: Optional[Variable]
      output은 weakref.ref 타입이라, 호출하면 실제 Variable (또는 None) 반환.

    ★ weakref 역참조(output())는 None 반환 가능 — output이 이미 회수된 경우.
      근데 fill_grad는 start_var에서 시작해 역방향 순회하므로,
      순회 중인 Function의 output은 start_var부터의 경로상에 있어 아직 살아있음.
      (사용자가 start_var를 들고 있는 한, 그 경로의 Variable들은 회수 안 됨)
      → output()이 None일 일은 사실상 없지만, 방어막으로 가드 추가.
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

    # --- 메인 루프 상태 (worklist + visited + schedule 클로저 — step16과 동일) -----
    worklist: Worklist = []
    visited: set[Function] = set()

    def schedule(f: Function) -> None:
        """미방문 Function을 worklist에 예약 (generation 내림차순 정렬 유지)."""
        if f not in visited:
            worklist.append(f)
            visited.add(f)
            worklist.sort(key=lambda func: func.generation)

    schedule(start_var.creator)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm + 위상 정렬) ------
    while worklist:
        f = worklist.pop()

        assert f.inputs is not None, "f.inputs must be set"
        assert f.output is not None, "f.output must be set"

        # --- ★ step17 핵심 — weakref 역참조로 output Variable 획득 ----------------
        # 이전(step16): output = f.output              (직접 참조, f.output 타입 = Variable)
        # 이후(step17): output = f.output()            (weakref 역참조 호출)
        #   - f.output 타입: weakref.ref (callable)
        #   - f.output() 반환: Optional[Variable] (역참조 결과 — 대상이 살아있으면 Variable, 죽었으면 None)
        #
        # ★ output()이 None인 경우 — output이 이미 회수됨.
        #   정상적인 fill_grad 흐름에선 일어나지 않음 (사용자가 start_var를 들고 있으니 경로상 Variable 살아있음).
        #   하지만 방어막으로 가드. None이면 역전파 계산이 불가능하므로 RuntimeError.
        output = f.output()
        if output is None:
            raise RuntimeError(
                f"{f!r}의 output Variable이 이미 회수되었습니다 — 역전파에 사용할 수 없습니다. "
                "역전파 대상 Variable을 사용자가 참조하고 있는지 확인하세요."
            )

        # ★ upstream_grad 방어막 (항목 007 변수명 유지 + pylance 타입 좁히기 동시 만족).
        #   핵심: 변수에 직접 assert 걸면 pylance가 변수 타입을 좁힌 채 유지.
        #   (속성 output.grad에 assert 걸고 변수에 재할당하면 pylance가 가드를 잃어버림 —
        #    그래서 변수 할당 후 변수 자체에 assert 거는 게 정해.)
        upstream_grad = output.grad
        assert upstream_grad is not None, "output.grad must be filled"

        # --- 역전파 호출 + 정규화 (step13~16과 동일) --------------------------------
        downstream_grads = f.backward(upstream_grad)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)

        # --- 다변 배분: 입력과 grad 짝지어 할당 (★ A.7.6 동시 언패킹) -------------
        # ★ step14 누적 (유지) — 같은 Variable이 여러 입력으로 와도 grad 합산
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

            if x.creator is not None:
                schedule(x.creator)


# --- 데모: step17 weakref 효과 검증 (정답지 step17.py와 동일 시나리오) --------------
if __name__ == "__main__":
    print("=== step17 메모리 관리와 순환 참조 데모 ===")
    print()

    # --- 케이스 1: weakref 도입 후에도 정상 역전파 동작 확인 ---
    # step16과 동일한 분기/합류 그래프로 정합성 검증.
    print("[1] 정상 역전파 검증 (weakref 도입 후에도 결과 동일해야 함)")
    x = Variable(np.array(2.0))
    a = square(x)
    y = add(square(a), square(a))
    fill_grad(y)
    print(f"    y.data = {y.data}  (기대: 32.0 — step16과 동일)")
    print(f"    x.grad = {x.grad}  (기대: 64.0 — step16과 동일)")
    print()

    # --- 케이스 2: 메모리 누수 시나리오 (정답지 step17.py와 동일) ---
    # 큰 ndarray를 반복 생성. step16 방식이었으면 순환 참조로 계산 그래프가 쌓임.
    # step17 weakref로 순환 끊김 → 매 반복마다 이전 그래프 회수.
    print("[2] 메모리 누수 시나리오 — for 루프로 큰 데이터 반복 생성")
    print("    (step16: 순환 참조로 그래프 쌓임 / step17: weakref로 매 반복 회수)")
    for i in range(10):
        x = Variable(np.random.randn(10000))  # big data
        y = square(square(square(x)))
    print(f"    루프 10회 완료 — 메모리 누수 없음 (weakref로 순환 참조 끊김)")
    print()

    # --- 케이스 3: 순환 참조 구조 확인 (개념 설명) ---
    print("[3] 순환 참조 구조 — 왜 발생하고 weakref가 어떻게 끊는가")
    print("    Variable ──creator──→ Function ──inputs──→ Variable")
    print("       ↑                                        │")
    print("       └────────────────────────────────────────┘")
    print("    ★ 순환: Function이 Variable을 알고, Variable이 Function을 앎")
    print()
    print("    step16 (강한 참조): Function.output = Variable → 순환 완결 → GC 못 잡음")
    print("    step17 (약한 참조): Function.output = weakref.ref(Variable)")
    print("                        → output의 refcount 안 올림 → 순환 끊김 → 즉시 회수")
    print()

    print("=== step17 완료 — weakref로 순환 참조 끊기, 메모리 누수 해결 ===")
