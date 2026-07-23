"""
rezero.steps.step03 — [1고지] 함수 연결
===============================================

이 step에서 배운 것:
  - 새 구상 클래스 Exp 추가 — step02 패턴(Template Method)의 확장력 체감
  - 함수 연쇄(chain): Square → Exp → Square 처럼 여러 Function을 잇기
  - "함수 연쇄 = 계산 그래프" 직감 — step06+ 역전파의 뼈대가 됨

이전 step과의 연결:
  - step02의 Variable / Function / Square 그대로 사용
  - Function을 ABC + @abstractmethod로 강화 (step02 탐구 exploration_09 실험 적용)
  - 자식 forward에는 @override 데코레이터로 재정의 명시 (Python 3.12+)

참고:
  - 패턴 정리: notes/design_patterns.md §2 Template Method
  - abc 심화: notes/exploration_09_abc_abstract.md

실행: uv run python rezero/steps/step03.py
"""

from abc import ABC, abstractmethod
from typing import override

import numpy as np


class Variable:
    """DeZero의 변수. 데이터를 담는 '상자' (step01~02와 동일).

    래퍼 패턴: ndarray를 감싸서 메타정보(grad, creator 등)를 붙일 토대.
    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data):
        self.data = data


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    Template Method 패턴:
      - __call__: "상자 까기 → forward → 상자 포장" 흐름 고정 (뼈대)
      - forward: 자식이 반드시 구현해야 하는 추상 메서드 (살)
    상세: notes/design_patterns.md §2 Template Method
    """

    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② Template Method: 자식이 구현한 forward 호출
        output = Variable(y)            # ③ 상자 포장
        return output

    @abstractmethod
    def forward(self, x):
        pass                            # 자식이 반드시 구현해야 함


class Square(Function):
    """제곱 함수: x → x²."""

    @override
    def forward(self, x):
        return x ** 2


class Exp(Function):
    """지수 함수: x → e^x. step02의 Square와 동일한 패턴으로 추가.

    Template Method의 확장력: forward() 한 줄만 정의하면 Function처럼 쓸 수 있음.
    새 함수 추가가 거의 공짜 — 기반 클래스 설계가 좋으면 확장이 쉽다.
    """

    @override
    def forward(self, x):
        return np.exp(x)


# --- 함수 연쇄 (chain) ---------------------------------------------
# x → A(Square) → a → B(Exp) → b → C(Square) → y
# 이 선형 연쇄가 곧 "계산 그래프". step06+ 역전파에서 이 그래프를
# 거꾸로 타고 미분값이 흘러감. 지금은 "연쇄가 자연스럽게 된다"만 체감.
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)                            # 0.5² = 0.25
b = B(a)                            # e^0.25 ≈ 1.2840
y = C(b)                            # 1.2840² ≈ 1.6487

print("연쇄 결과:")
print(f"  x = {x.data}")            # 0.5
print(f"  a = A(x) = {a.data:.4f}") # 0.25
print(f"  b = B(a) = {b.data:.4f}") # 1.2840
print(f"  y = C(b) = {y.data:.4f}") # 1.6487
