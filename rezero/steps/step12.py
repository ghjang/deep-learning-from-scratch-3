"""
rezero.steps.step12 — [2고지] 가변 길이 인수(개선 편)
===============================================

★ step11~13 3부작 중 2번째. step11의 "거시기한" API를 자연스럽게 개선.
  - step11 — 순전파: 다변 입출력 도입 (리스트 기반, 어색)
  - step12 (이번) — 개선: *inputs 가변 인수로 자연스럽게 ★ "거시기함" 해소
  - step13 — 역전파: 다변 버전 역전파

이 step에서 배울 것:
  - `*inputs` 가변 위치 인수 — 리스트 감싸기 제거
    `Add()([x0, x1])` → `Add()(x0, x1)` (자연스러운 위치 인수)
  - 출력 단일화 — 1개일 땐 Variable 직접, 2개 이상일 땐 리스트
  - ★ apply hook 시그니처를 가변 인수로 통일 (브로 통찰)

★ 핵심 변화 (step11 vs step12):
  | | step11 (리스트) | step12 (가변 인수) |
  |---|---|---|
  | __call__ 인자 | `inputs: list[Variable]` | `*inputs: Variable` |
  | forward 시그니처 | `forward(xs: list)` | `forward(*xs)` |
  | apply 시그니처 | `apply(xs: list)` | `apply(*xs)` ★ (브로 통찰로 통일) |
  | Add.apply | `x0, x1 = xs` (언팩) | `def apply(self, x0, x1):` (직접 위치) |
  | 반환값 | 항상 튜플 | 단일값 OK, __call__에서 정규화 |

★ `*` 이중성 (헷갈리는 포인트 — exploration_07 A.7 참조):
  같은 `*` 기호인데 문맥에 따라 반대 방향으로 작동:
  - 함수 정의 `def f(*args):` — 여러 인수 **수집** → tuple
  - 함수 호출 `f(*xs)` — 리스트/튜플 **풀어서** 전달 → 개별 인수

★ 박스 컨텍스트 3계층 (REZERO_CHANGES 항목 011, step11에서 정립):
  | 메서드   | 역할                                    | 박스 컨텍스트 |
  |----------|-----------------------------------------|---------------|
  | __call__ | 값 전달/흐름 관리 (Variable 회수→래핑)  | O (Variable)  |
  | forward  | 순전파 뼈대 (hook 호출)                 | X (ndarray만) |
  | apply    | 순수 수학 계산                          | X (순수 ndarray) |

참고 자료:
  - 원본 구현: steps/step12.py
  - 이전 step: rezero/steps/step11.py (리스트 기반 — 이번에 가변 인수로 개선)
  - rezero 변형: REZERO_CHANGES 항목 010~013 (apply/derivative hook)
  - 언패킹 + `*` 이중성: exploration_07 A.7

검증 포인트:
  - `add(x0, x1)` → Variable(5) (리스트 아닌 직접 Variable)
  - 단일 함수(square)도 가변 인수 체계에서 자연스럽게 동작?
  - 출력이 1개일 때 리스트가 아닌 Variable 직접 반환?

실행:
  uv run python rezero/steps/step12.py
"""

from abc import ABC
from typing import Optional, override

import numpy as np


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환 (삼항 1줄화, 항목 2)."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    step11과 동일. 역전파는 fill_grad 전역 함수(step08~10)가 담당했으나,
    이번 step(개선 편)에선 여전히 순전파에 집중.
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
    """DeZero의 함수. ★ step12: 가변 위치 인수(*inputs)로 자연스러운 API.

    ★ 박스 컨텍스트 3계층 (REZERO_CHANGES 항목 011):
      __call__ → Variable 흐름 관리 / forward → 순전파 뼈대 / apply → 순수 수학 계산
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.outputs: Optional[list[Variable]] = None

    def __call__(self, *inputs: Variable) -> Variable | list[Variable]:
        # ★ step12: 가변 위치 인수 — inputs는 tuple (리스트 감싸기 불필요)
        # --- 회수 + 가드를 한 루프로 (step11 패턴 유지) ---
        xs = []
        for x in inputs:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        # --- 순전파: forward → 다시 Variable로 래핑 --------------------------------
        # ★ `*xs` 언패킹 호출 — 리스트를 풀어서 개별 인수로 forward에 전달
        ys = self.forward(*xs)

        # ★ 반환값 정규화 — 단일값도 튜플로 맞춤 (일관된 처리 위해)
        if not isinstance(ys, tuple):
            ys = (ys,)

        outputs = [Variable(as_array(y)) for y in ys]

        # --- 계산 그래프 연결 (creator 설정) ----------------------------------------
        for output in outputs:
            output.set_creator(self)
        self.inputs = inputs                            # tuple 그대로 저장 (가변 인수)
        self.outputs = outputs
        return outputs if len(outputs) > 1 else outputs[0]

    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). ★ step12: 가변 인수 시그니처.

        ★ 박스 컨텍스트 없는 단계 — ndarray만 다룸.
        """
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. ★ step12: 가변 인수 (브로 통찰 — forward와 통일).

        자식이 채우거나 forward 직접 오버라이드. 단일값 반환도 OK (__call__에서 튜플 정규화).
        """
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # --- 역전파 계열: step13에서 다변 버전으로 재설계 예정 -----------------------
    def backward(self, *gys: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 (다변): step13에서 구현 예정."""
        raise NotImplementedError("역전파는 step13에서 다변 버전으로 구현합니다.")

    def derivative(self) -> tuple:
        """도함수 hook: step13에서 다변 역전파 설계 시 재검토."""
        raise NotImplementedError("도함수 hook은 step13에서 다변 역전파와 함께 재설계합니다.")


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. ★ 다입력 함수의 첫 사례.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1. 역전파는 step13에서.
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:
        # ★ step12: 리스트 언팩 필요 없이 직접 위치 인수로 받음 (step11 대비 개선)
        y = x0 + x1

        return y                       # 단일값 반환 — __call__에서 튜플로 정규화


class Square(Function):
    """제곱 함수: x → x². ★ step12: 단일 함수도 가변 인수 체계로.

    단일 입력 함수지만 *xs 가변 인수 시그니처에 맞춤 (일관성).
    미분: f'(x) = 2x. 역전파는 step13에서.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return x ** 2


# ★ step12 wrapper 함수 — 가변 인수로 자연스러운 호출
def add(x0: Variable, x1: Variable) -> Variable:
    """덧셈 wrapper. Add 인스턴스 생성 + 호출을 한 번에."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def square(x: Variable) -> Variable:
    """제곱 wrapper. Square 인스턴스 생성 + 호출을 한 번에."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


# --- 데모: step12 개선 효과 확인 ----------------------------------------------
if __name__ == "__main__":
    print("=== Add 데모 (가변 인수 — 리스트 감싸기 불필요) ===")
    x0 = Variable(np.array(2))
    x1 = Variable(np.array(3))

    # ★ step11: ys = Add()([x0, x1]); y = ys[0]  (리스트 + 인덱싱 번거로움)
    # ★ step12: y = add(x0, x1)                   (자연스러운 위치 인수!)
    y = add(x0, x1)
    print(f"add(x0, x1) → {y.data}  (기대: 5, 타입: Variable 직접)")

    # ★ 합성 함수도 자연스럽게
    print()
    print("=== 합성 데모 (square + add) ===")
    x = Variable(np.array(2.0))
    y = square(add(x, x))             # (x + x)² = (2+2)² = 16
    print(f"square(add(x, x)) → {y.data}  (기대: 16.0)")
