"""rezero.v0 — NumPy 없는 DeZero (순수 Python 학습 실험실).

이슈 43 작업 3 (브로 아이디어, RESEARCH_QUEUE 후보 9번) — 2026-09-04 창설.
v1에서 NumPy를 걷어내어 "두 축(그래프축/데이터축)의 물리적 분리"를 체감하는 실험실.

  - data가 float 하나 — shape/dtype/브로드캐스팅 없음
  - 여러 점 계산 = 원소 순회 루프 직접 작성 (데이터축이 코드에 드러남)
  - 노트 34 "배치 = 독립 스칼라 실험의 묶음"의 구현판

사용법 (v1과 동일한 인터페이스 — 배열만 스칼라로):
    from rezero.v0 import Variable, fill_grad
    x = Variable(2.0)
    y = x ** 2 + 1
    fill_grad(y)
    print(x.grad)  # 4.0
"""

from rezero.v0.core import (
    Config,
    Function,
    Variable,
    VariableArithmeticMixin,
    as_float,
    as_variable,
    backprop,
    fill_grad,
    iter_reverse_topo,
    no_grad,
    using_config,
)
from rezero.v0.functions import (
    Add,
    Cos,
    Div,
    Mul,
    Neg,
    Pow,
    Sin,
    Square,
    Sub,
    add,
    cos,
    div,
    mul,
    neg,
    pow,
    rdiv,
    rsub,
    sin,
    square,
    sub,
)
from rezero.v0.utils import numerical_diff

__all__ = [
    # core
    "Config",
    "Function",
    "Variable",
    "VariableArithmeticMixin",
    "as_float",
    "as_variable",
    "backprop",
    "fill_grad",
    "no_grad",
    "using_config",
    # functions (wrapper)
    "add",
    "cos",
    "div",
    "mul",
    "neg",
    "pow",
    "rdiv",
    "rsub",
    "sin",
    "square",
    "sub",
    # functions (클래스)
    "Add",
    "Cos",
    "Div",
    "Mul",
    "Neg",
    "Pow",
    "Sin",
    "Square",
    "Sub",
    # utils
    "numerical_diff",
]
