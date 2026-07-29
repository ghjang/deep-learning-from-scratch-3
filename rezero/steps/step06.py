"""
rezero.steps.step06 — [1고지] 수동 역전파 (Variable.grad, Function.backward)
===============================================

이 step에서 배울 것:
  - Variable.grad 속성 도입 — 각 변수가 자기 미분값(그래디언트)을 기억
  - Function.backward() 메서드 도입 — 각 노드의 국소적 미분 (df/dx)
  - 수동 역전파 — right fold를 손으로 한 스텝씩 unfold

이전 step과의 연결:
  - step04 복선 회수: self.input이 backward()에서 쓰임
    (순전파 시점에 입력을 저장해둔 이유가 드디어 밝혀짐)
  - step05 통찰 회수: "역전파 = right fold (foldr)" 직관을 코드로 펼침
    y.grad → C.backward → B.backward → A.backward (오른쪽→왼쪽 ∏ 누적)

참고 자료:
  - 원본 구현: steps/step06.py
  - 역전파 이론: step05 (이미 학습)
  - Template Method 패턴: notes/design_patterns.md §2 (backward로 패턴 확장)

검증 포인트:
  - step04 수치 미분 결과와 비교 (둘이 일치해야 함)
  - 합성 y=(e^(x²))², x=0.5 → 해석적 정답 ≈ 3.2974
    · step04 수치 미분: 3.297443 (오차 0.00004)
    · step06 역전파:   정확히 3.2974...  (오차 0, 해석적 정답)
  - → 역전파가 수치 미분보다 정확하고 빠름을 체감

실행: uv run python rezero/steps/step06.py
"""

from abc import ABC, abstractmethod
from typing import Optional, override

import numpy as np


class Variable:
    """DeZero의 변수. 데이터를 담는 '상자' + 이제 미분값도 기억.

    래퍼 패턴: ndarray를 감싸서 메타정보를 붙이는 토대.
    ★ step06 변경: grad 속성 추가. 역전파로 구한 미분값(그래디언트)을 저장.
    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data):
        self.data = data
        # data는 항상 ndarray가 될 예정 (DeZero의 고정 — 책 step37 부턴 런타임 isinstance 체크로 보장).
        # 타입 힌트(data: np.ndarray)는 forward 반환 타입 힌트와 함께 다음 step 적절한 시점에 도입 예정 —
        # 지금 data에만 힌트 넣고 forward 반환 타입을 안 넣으면 Pyright가 정적 오류를 냄.
        self.grad: Optional[np.ndarray] = None
        # ★ 미분값(그래디언트)을 담을 그릇.
        # 라이프사이클: 역전파 전 None → 역전파 후 ndarray 채워짐.
        # 타입 힌트(Optional)로 "둘 중 하나"임을 명시 — 책 원본은 None만으로 두어
        # 정적 분석에 ndarray 대입 경고가 뜨지만, 우리는 타입 정합성 추구.


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    Template Method 패턴:
      - __call__: "상자 까기 → forward → 상자 포장" 흐름 고정 (뼈대)
      - forward:  자식이 반드시 구현해야 하는 추상 메서드 (순전파의 살)
      - backward: 자식이 반드시 구현해야 하는 추상 메서드 (역전파의 살) ★ step06 추가
    ★ step06 변경: backward() 추상 메서드 추가.
       → 각 노드는 자기 함수의 국소적 미분 (df/dx)을 계산하는 책임을 짐.
    상세: notes/design_patterns.md §2 Template Method

    역전파 흐름 (★ step05 통찰: 역전파 = right fold):
      최종 출력 y에서 출발해, 각 노드의 backward()를 거치며 미분값이
      "접어져서(fold)" 누적되며 입력 쪽으로 흘러간다.

        [출력 y] ─upstream→ [C].backward ─downstream→ [B].backward ─downstream→ [A].backward ─downstream→ [입력 x]

      - 각 backward()는 **상류에서 접어 내려온 누적 미분값** (upstream_grad)을 받아,
      - 자기 도함수 (df/dx) 를 곱해 **한 번 더 접고** (이게 이 노드가 기여하는 fold step),
      - 그 결과를 **하류의 다음 노드에게 넘겨** 마저 접히게 한다 (downstream_grad 반환).
      - 즉 backward는 "fold accumulator step" — 받은 누적값에 자기 몫을 곱해 다음 타자에게 전달.
    """

    def __call__(self, input_var):
        x = input_var.data              # ① 상자 깐기
        y = self.forward(x)             # ② Template Method: 자식이 구현한 forward 호출
        output = Variable(y)            # ③ 상자 포장
        self.input = input_var          # ★ 입력 기억 (역전파용 — backward에서 쓰임, 복선 회수)
        return output

    @abstractmethod
    def forward(self, x):
        """순전파: 입력 데이터 x를 연산해 출력 데이터 y를 반환. 자식이 구현."""

    @abstractmethod
    def backward(self, upstream_grad):
        """역전파: 상류에서 접어 내려온 누적 미분값을 받아 자기 도함수를 곱해 한 번 더 접고,
        하류로 내려보낼 새 누적값을 반환. 자식이 구현. (★ step05 통찰: fold accumulator step)

        Args:
            upstream_grad: 상류(출력 쪽)에서 접어 내려온 미분 누적값.
                최종 출력 y에서 시작해, 역방향으로 지나온 노드들의 도함수가
                차례로 곱해진(fold된) 값. None이면 안 됨.
                cf. PyTorch의 grad_output, 학술 용어 upstream gradient.

        Returns:
            downstream_grad: 이 노드의 도함수 (df/dx) 를 upstream_grad에 곱해
                한 번 더 접은 누적값. 하류(입력 쪽)의 다음 노드 backward()로 전달됨.
                cf. PyTorch의 grad_input, 학술 용어 downstream gradient.
        """


class Square(Function):
    """제곱 함수: x → x². 미분: 2x."""

    @override
    def forward(self, x):
        y = x ** 2
        return y

    @override
    def backward(self, upstream_grad):
        x = self.input.data             # 순전파 시 저장해둔 입력 회수 (step04 복선 회수)
        local_deriv = 2 * x             # ① 자기 도함수 (df/dx) 평가 — Square의 미분은 2x
        downstream_grad = local_deriv * upstream_grad  # ② fold step (곱해서 누적)
        return downstream_grad          # ③ 다음 노드로 전달


class Exp(Function):
    """지수 함수: x → e^x. 미분: e^x (자기 자신)."""

    @override
    def forward(self, x):
        y = np.exp(x)
        return y

    @override
    def backward(self, upstream_grad):
        x = self.input.data
        local_deriv = np.exp(x)         # ① 자기 도함수 (df/dx) 평가 — Exp의 미분은 e^x
        downstream_grad = local_deriv * upstream_grad  # ② fold step
        return downstream_grad          # ③ 다음 노드로 전달


# --- 순전파: x → A(Square) → a → B(Exp) → b → C(Square) → y -------------
# step03과 동일한 합성: y = (e^(x²))²
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# --- 수동 역전파: right fold를 손으로 한 스텝씩 unfold ---------------------
# step05 통찰: 역전파 = right fold (최종 출력 y에서 시작, 오른쪽→왼쪽으로 ∏ 누적)
y.grad = np.array(1.0)                  # fold 시작점 (최종 출력 y에서, upstream = 1)
b.grad = C.backward(y.grad)             # fold step 1: C 노드 (y → b)
a.grad = B.backward(b.grad)             # fold step 2: B 노드 (b → a)
x.grad = A.backward(a.grad)             # fold step 3: A 노드 (a → x, 입력에 도달)

print(f"역전파 결과 x.grad: {x.grad}")
print(f"step04 수치 미분 결과: 3.297443 (오차 0.00004)")
print(f"해석적 정답: e^0.5 · 2 ≈ 3.2974 (역전파는 오차 0, 정확히 일치)")
