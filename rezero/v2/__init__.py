"""rezero.v2 — 제 3고지 "고차 미분 계산" (step25~36) 패키지.

v1 (제 1~2고지 스코프)을 step32에서 브랜칭 — 고차 미분(double backprop) 지원.

사용:
    from rezero.v2 import Variable, fill_grad

    x = Variable(np.array(2.0))
    y = x ** 2
    fill_grad(y, create_graph=True)   # 역전파가 그래프를 남기며 수행

    gx = x.grad          # gx는 Variable (2x라는 "식" — 그래프 소유)
    x.clear_grad()
    fill_grad(gx)        # gx에 다시 역전파 = 2차 미분
    print(x.grad.data)   # 2.0 ← f''(2)

★★★ v2 사용 전제 (v1과의 차이 중심 — v1 전제에서 계승하는 항목도 많음):

  1. ★ grad 타입 — Variable.grad는 Variable (v1: ndarray).
     값 접근은 x.grad.data. 재미분 가능 = 미분 결과가 "값"이 아니라 "식".
  2. ★ create_graph — fill_grad(y, create_graph=True)로 역전파가 미분 계산
     그래프(2층)를 구성. 기본 False (lean — step18 철학 연장).
     gx = x.grad는 Variable이므로 fill_grad(gx) 재호출이 2차 미분.
  3. ★ derivative hook — Callable[[Variable], Variable | float].
     도함수 계산이 Variable 연산으로 수행됨 (Mul/Div/Pow 등이 그래프 생성).
  4. 스칼라 출력 — v1 계승. data는 0차원 스칼라 ndarray, 출력 1개만.
     벡터/행렬/다출력은 후속 step에서.
  5. Define-by-Run — 순전파 실행 시 그래프 자동 생성. 재사용 시 clear_grad().
  6. 그래프 구조 — DAG. 같은 Variable 다중 입력 허용 (add(x,x)), visited set 방어.
  7. 메모리/GC — Function.output은 weakref, inputs는 강한 참조 (v1 계승).
  8. 모드/설정 — Config.enable_backprop / no_grad() / retain_grad (v1 계승).
  9. 연산자 — +, -, *, /, **, 단항 - 지원 (v1 계승).
 10. 수학 함수 — sin, cos (★ step32: cos 신규 — sin 고차 미분용).

  ★ 전제가 깨지면? — RuntimeError/TypeError로 방어. core.py 각 가드 참조.
  ★ 브랜칭 경위: step32 (고차 미분(구현 편)) — grad ndarray→Variable은 API
    호환성이 깨지는 대개편이라 v2로 분기 (책의 core_simple/core 이분법과 평행).
"""

from rezero.v2.core import (
    Config,
    DerivativeFn,
    Function,
    Variable,
    as_array,
    as_variable,
    fill_grad,
    no_grad,
    using_config,
)
from rezero.v2.functions import (
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
from rezero.v2.utils import fold_dot_graph, numerical_diff, plot_dot_graph

__all__ = [
    # core
    "Config",
    "DerivativeFn",
    "Function",
    "Variable",
    "as_array",
    "as_variable",
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
    # functions (클래스 — 고급 사용자용)
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
    "fold_dot_graph",
    "numerical_diff",
    "plot_dot_graph",
]
