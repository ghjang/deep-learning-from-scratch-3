"""
rezero.steps.step04 — [1고지] 수치 미분
===============================================

이 step에서 배운 것:
  - numerical_diff: 중앙 차분(central difference)으로 미분 근사
  - Function.__call__에 self.input/self.output 추가 (★ step07 역전파 복선)
  - 합성 함수 f(x) = (e^(x²))² 의 수치 미분

이전 step과의 연결:
  - step03의 Variable / Function(ABC) / Square / Exp 그대로 사용
  - Function.__call__ 확장: 입력/출력을 기억 (backward를 위해)

참고:
  - 미분 본질: notes/exploration_10_what_is_derivative.md
  - autodiff 모드: notes/exploration_11_autodiff_modes.md

실행: uv run python rezero/steps/step04.py
"""

from abc import ABC, abstractmethod
from typing import override

import numpy as np


class Variable:
    """DeZero의 변수. 데이터를 담는 '상자' (step01~03과 동일).

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
    ★ step04 변경: __call__이 self.input / self.output을 저장.
       → step07 역전파 구현을 위한 복선 (입력을 기억해야 backward 가능).
    상세: notes/design_patterns.md §2 Template Method
    """

    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② Template Method: 자식이 구현한 forward 호출
        output = Variable(y)            # ③ 상자 포장
        self.input = input_var          # ★ 입력 기억 (역전파용, step07+)
        self.output = output            # ★ 출력 기억 (역전파용, step07+)
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
    """지수 함수: x → e^x."""

    @override
    def forward(self, x):
        return np.exp(x)


def numerical_diff(f, x, eps=1e-4):
    """수치 미분 (중앙 차분, central difference).

    f'(x) ≈ [f(x+h) - f(x-h)] / 2h

    - f: 미분 대상 함수 (Function 인스턴스이거나, Variable을 받아 Variable을 반환하는 호출 가능 객체)
    - x: Variable (미분을 구할 지점)
    - eps: 미소 변화량 h. 1e-4는 부동소수점 오차와 근사 오차의 트레이드오프 점.

    ★ 블랙박스 관점: f의 내부를 몰라도, f(x+h)/f(x-h)를 호출해서 출력 차이를 보면 됨.
       → 코드로 짠 함수(if/for/신경망)도 미분 가능. autograd의 철학.
       상세: notes/exploration_10_what_is_derivative.md §3
    """
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)


# --- 검증 1: 단일 함수 미분 -----------------------------------------
# f(x) = x² 의 x=2 에서의 미분값.
# 해석적 정답: f'(x) = 2x → f'(2) = 4. 수치 미분이 4에 가까운지 확인.
sq = Square()
x = Variable(np.array(2.0))
dy = numerical_diff(sq, x)
print(f"[단일] d/dx(x²) at x=2: {dy:.6f}  (정답: 4.0)")


# --- 검증 2: 합성 함수 미분 -----------------------------------------
# y = (e^(x²))² 의 x=0.5 에서의 수치 미분.
# 주의: 원본 step04.py는 위에서 쓴 'f'와 같은 이름을 재사용하여 IDE 워닝을 유발.
#       우리는 이름을 분리하여 코드 악취(name shadowing)를 제거함.
def composite_f(x):
    """y = (e^(x²))² = C(B(A(x))). step03의 함수 연쇄."""
    A = Square()
    B = Exp()
    C = Square()
    return C(B(A(x)))


x = Variable(np.array(0.5))
dy = numerical_diff(composite_f, x)
# 해석적 정답: y = e^(2x²) → y' = e^(2x²)·4x → x=0.5: e^0.5 · 2 ≈ 3.2974
print(f"[합성] d/dx((e^(x²))²) at x=0.5: {dy:.6f}  (해석적 정답 ≈ 3.2974)")
