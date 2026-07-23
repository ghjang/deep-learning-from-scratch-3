"""
rezero.steps.step02 — [1고지] 변수를 낳는 함수 (Function 도입)
===============================================

이 step에서 배운 것:
  - Function 기반 클래스: Variable(상자)을 받아 새 Variable을 낳는 "변환기"
  - Template Method 패턴: __call__이 뼈대, 자식의 forward()가 살
  - Square 구상 클래스: forward()만 정의하면 Function처럼 쓸 수 있음

이전 step과의 연결:
  - step01의 Variable(래퍼 패턴)을 그대로 사용
  - Function이 그 Variable을 입력/출력으로 다룸

참고:
  - 패턴 정리: notes/design_patterns.md (래퍼, 템플릿 메서드)

실행: uv run python rezero/steps/step02.py
"""

import numpy as np


class Variable:
    """DeZero의 변수. 데이터를 담는 '상자' (step01과 동일).

    래퍼 패턴: ndarray를 감싸서 메타정보(grad, creator 등)를 붙일 토대.
    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data):
        self.data = data


class Function:
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    Template Method 패턴:
      - __call__: "상자 까기 → forward → 상자 포장" 흐름을 고정 (뼈대)
      - forward: 자식이 반드시 구현해야 하는 추상 메서드 (살)
    상세: notes/design_patterns.md §2 Template Method
    """

    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기 (ndarray 꺼냄)
        y = self.forward(x)             # ② Template Method: 자식이 구현한 forward 호출
        output = Variable(y)            # ③ 상자 포장 (결과를 다시 Variable로)
        return output

    def forward(self, in_data):
        raise NotImplementedError()     # 자식이 반드시 구현해야 함


class Square(Function):
    """제곱 함수: x → x². Function을 상속해 forward만 정의."""

    def forward(self, x):
        return x ** 2


# --- 동작 확인 ------------------------------------------------------
x = Variable(np.array(10))
f = Square()
y = f(x)

print(type(y))   # <class '__main__.Variable'> — 상자가 새로 만들어짐
print(y.data)    # 100 — 10의 제곱
