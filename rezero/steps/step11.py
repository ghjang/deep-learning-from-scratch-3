"""
rezero.steps.step11 — [2고지] 가변 길이 인수(순전파 편)
===============================================

★ 제2고지 "자연스러운 코드로" 의 첫 단추.
step11~13이 "가변 길이 인수" 3부작:
  - step11 (이번) — 순전파: 다변 입출력 Function 도입
  - step12        — 개선: 단일/다변을 하나의 API로 통합 (복선)
  - step13        — 역전파: 다변 버전 역전파 (derivative hook 시험대)

이 step에서 배울 것:
  - Function.__call__ 입출력을 Variable → list[Variable]로 일반화
  - forward(xs) → ys (리스트 언팩킹 x0, x1 = xs, 출력은 튜플)
  - Add 클래스 도입 (다입력 함수의 첫 사례)
  - ★ 방향 (B): step10의 apply hook 구조를 다변 인수로 일반화하는 실험

★ 방향 (B) — apply hook 다변 일반화:
  step07에서 세운 apply/derivative hook 구조(#010~#013)가 다변 일반화에 견고한지 검증.
  핵심: forward→apply hook 호출 라인은 `return self.apply(xs)`로 구조 그대로 살아남음.
  → 시그니처만 x → xs 로 바꾸면 hook 패턴이 안 깨진다는 실증.
  ★ 순전파 hook(apply)은 다변에서 살아남지만, 역전파 hook(derivative)은 step13 시험대.
    Add 역전파는 gy → (gx0, gx1) (1입력 2출력)이라 derivative 1줄 표현이 안 될 수 있음.

이전 step과의 연결:
  - step10: 1고지 완료 (gradient check로 검증). step11부턴 2고지.
  - step07~10: apply/derivative hook, fill_grad 전역 함수, 방어막, pipe 구축
  - ★ 책의 "구조 리셋": step11~13은 다변 인수로 Function을 다시 쌓아올리는 단계.
    - Variable.backward() 자동화 ❌ (step13에서 다변 버전으로 재도입)
    - fill_grad 전역 함수 ❌ (이번 step 사용 안 함 — 순전파에 집중)
    - pipe ❌ (다입력엔 단일 흐름 pipe가 안 맞음 — Issue #13, step23 재도입)

참고 자료:
  - 원본 구현: steps/step11.py (Add 도입, forward(xs)→ys)
  - 이전 step: rezero/steps/step10.py (apply/derivative hook 구조 — 이번 step의 베이스)
  - rezero 변형: REZERO_CHANGES.md 항목 010~013 (apply/derivative hook — 다변 일반화 대상)
  - pipe 보류: Issue #13 (step23 패키지화 시 재도입 + FP 화두)

검증 포인트:
  - Add([Variable(2), Variable(3)]) → [Variable(5)] (ys[0].data == 5)
  - apply hook이 다변 시그니처에서 자연스럽게 동작하는가?
  - creator 연결(set_creator)이 다변에서도 제대로 되는가?

실행:
  uv run python rezero/steps/step11.py
"""

from abc import ABC
from typing import Optional, override

import numpy as np


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환 (삼항 1줄화, 항목 2)."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    step10과 동일. ★ 역전파는 fill_grad 전역 함수(step08~10)가 담당했으나,
    이번 step(순전파 편)에선 사용 안 함. Variable은 순수 데이터 상자로만 역할.
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
    """DeZero의 함수. ★ step11: 다변 입출력으로 일반화 (Variable → list[Variable]).

    방향 (B): step10의 apply hook 구조를 다변으로 일반화.
    forward→apply hook 호출은 `return self.apply(xs)`로 구조 그대로 살아남음.
    역전파(backward/derivative)는 step13에서 다변 버전으로 재설계 — 여기선 빈칸.

    ★ 관점 분리 — "박스 컨텍스트" 3계층 (REZERO_CHANGES 항목 011):
      | 메서드     | 역할                                    | 박스 컨텍스트 |
      |------------|-----------------------------------------|---------------|
      | __call__   | 값 전달/흐름 관리 (Variable 회수→래핑→creator 연결) | O (Variable)  |
      | forward    | 순전파 뼈대 (hook 호출 or 직접 계산)    | X (ndarray만) |
      | apply      | 순수 수학 계산 (x², x0+x1)              | X (순수 ndarray) |

    "forward"는 '전달(forwarding)' 뉘앙스지만 실제 전달은 __call__이 담당.
    forward는 그 파이프라인 안의 "순수 계산 단계" → apply가 실제 함수 적용 ($f(x)$).
    ★ 책/PyTorch는 생태계 관례(forward pass/backward pass)를 따르나,
      rezero는 학습용이라 더 정확한 apply 이름 실험. 이중 용어 인식 필요.
    """

    def __init__(self) -> None:
        # ★ step11: 단수 input/output → 복수 inputs/outputs
        self.inputs: Optional[list[Variable]] = None
        self.outputs: Optional[list[Variable]] = None

    def __call__(self, inputs: list[Variable]) -> list[Variable]:
        # --- 회수 + 가드를 한 루프로 (컴프리헨션 분리 시 타입 좁히기 안 됨) ----------
        # ★ raise 다음 줄에서 Pylance가 x.data를 np.ndarray로 좁혀줌 → xs도 list[np.ndarray].
        xs = []
        for x in inputs:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)                           # 방어막 통과 → np.ndarray 보장

        # --- 순전파: forward → 다시 Variable로 래핑 --------------------------------
        ys = self.forward(xs)                           # ★ hook 호출 (다변)
        outputs = [Variable(as_array(y)) for y in ys]   # 각 출력을 Variable로 래핑

        # --- 계산 그래프 연결 (creator 설정) ----------------------------------------
        for output in outputs:
            output.set_creator(self)
        self.inputs = inputs                            # ★ 복수형
        self.outputs = outputs                          # ★ 복수형
        return outputs

    def forward(self, xs: list[np.ndarray]) -> tuple[np.ndarray, ...]:
        """순전파 뼈대 (apply hook 호출). 자식은 apply 또는 forward 직접 오버라이드.

        ★ 박스 컨텍스트 없는 단계 — ndarray만 다룸 (Variable 회수/래핑은 __call__이 담당).
        ★ step11 다변 일반화: 시그니처 x → xs. hook 호출 구조는 그대로.
        """
        return self.apply(xs)

    def apply(self, xs: list[np.ndarray]) -> tuple[np.ndarray, ...]:
        """순수 수학 계산 hook (다변). 자식이 채우거나 forward 직접 오버라이드.

        ★ 박스 컨텍스트 없는 순수 계산 — 수학의 f(x) "함수 적용" 단계.
        ★ 다변 일반화: 단일 apply(x) → apply(xs). 리스트 언팩킹으로 입력 회수.
        """
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # --- 역전파 계열: step13에서 다변 버전으로 재설계 예정 -----------------------
    # 순전파 편인 이번 step에선 빈칸(NotImplementedError)으로 둠.
    # ★ derivative hook은 다변 역전파에서 깨질 가능성 (Add: gy → (gx0, gx1)).
    #   step13 진입 시점에서 재평가 (REZERO_CHANGES 항목 010~013 "최종 반영 보류" 참조).
    def backward(self, gys: tuple[np.ndarray, ...]) -> tuple[np.ndarray, ...]:
        """역전파 (다변): step13에서 구현 예정. 지금은 순전파만 집중."""
        raise NotImplementedError("역전파는 step13에서 다변 버전으로 구현합니다.")

    def derivative(self):
        """도함수 hook: step13에서 다변 역전파 설계 시 재검토."""
        raise NotImplementedError("도함수 hook은 step13에서 다변 역전파와 함께 재설계합니다.")


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. ★ 다입력 함수의 첫 사례.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1 (각 입력에 대해). 역전파는 step13에서.
    """

    @override
    def apply(self, xs: list[np.ndarray]) -> tuple[np.ndarray, ...]:
        # --- 회수: 리스트 언팩킹으로 2개 입력 분해 ---
        x0, x1 = xs

        # --- 연산 + 포장: 덧셈 후 튜플로 반환 (길이 1이어도 다변 시그니처 유지) ---
        y = x0 + x1

        return (y,)


# --- 데모: Add 실행 (정답지 step11.py와 동일 검증) ----------------------------
if __name__ == "__main__":
    print("=== Add 데모 (다입력 함수 순전파) ===")
    xs = [Variable(np.array(2)), Variable(np.array(3))]
    ys = Add()(xs)
    y = ys[0]
    print(f"Add([2, 3]) → {y.data}  (기대: 5)")

    # ★ apply hook 다변 일반화 검증 — 그래프 연결(creator)이 다변에서도 제대로 되는가?
    print()
    print("★ 계산 그래프 연결 확인 (다변):")
    creator = y.creator
    assert creator is not None, "creator should be set after __call__"
    assert creator.inputs is not None, "inputs should be set after __call__"
    print(f"  y.creator is Add 인스턴스: {creator is not None}")
    print(f"  creator.inputs = {[v.data for v in creator.inputs]}")
