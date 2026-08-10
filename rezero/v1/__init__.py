"""rezero.v1 — 제 1~2고지 (step01~22) 패키지.

사용:
    from rezero.v1 import Variable, fill_grad
    from rezero.v1 import square, add, mul, neg, sub, div, pow

    x = Variable(np.array(2.0))
    y = x ** 2 + 1
    fill_grad(y)
    print(x.grad)  # 4.0

★★★ v1 사용 전제 (이 패키지가 가정하는 상황):
  v1은 "스칼라 Variable + 자동 역전파" 스코프. 다음 전제들이 성립할 때 사용 가능.

  ┌──────────────────────────────────────────────────────────────────────┐
  │ 카테고리          │ 전제 (가정)                                        │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 1. 스칼라 출력     │ Variable.data는 0차원 스칼라 ndarray.               │
  │                   │ Function은 출력 1개만 반환 (다출력 불가).            │
  │                   │ → 벡터/행렬/다출력은 v2(step34+)에서.               │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 2. Define-by-Run  │ 순전파 실행 시 계산 그래프가 자동 생성됨.             │
  │                   │ 같은 Variable로 두 번째 forward → 이전 grad 잔류      │
  │                   │ → 명시적 clear_grad()로 초기화 필요.                │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 3. 그래프 구조    │ 계산 그래프는 DAG (사이클 없음).                     │
  │                   │ 같은 Variable이 여러 입력으로 전달 가능 (add(x,x)).   │
  │                   │ 같은 Function이 worklist에 중복 push 가능 → visited │
  │                   │ set으로 방어.                                        │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 4. 메모리/GC      │ Function.output은 weakref (순환 참조 방지).          │
  │                   │ Function.inputs는 강한 참조 (역전파 시 data 필요).    │
  │                   │ output Variable이 사용자 손에서 떠나면 자동 회수.     │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 5. 모드/설정      │ Config.enable_backprop 전역 플래그 (스레드 안전 X).  │
  │                   │ no_grad() 블록: 역전파 그래프 구축 생략 (추론용).     │
  │                   │ retain_grad=False (기본): 중간 Variable grad 버림.   │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 6. 역전파         │ fill_grad(start_var) 전역 함수로 역전파 시작.        │
  │                   │ derivative hook: df(x) * upstream 공식 (스칼라만).   │
  │                   │ → 행렬 미분(야코비안)은 v2에서 backward 직접.       │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 7. 연산자         │ +, -, *, /, **, 단항 - 지원.                         │
  │                   │ 좌변이 scalar/ndarray여도 OK (__radd__/__rmul__).    │
  │                   │ __array_priority__ 없이도 현대 NumPy에서 동작.       │
  │                   │ Pow의 지수 c는 상수 (Variable 아님, 미분 대상 X).    │
  ├───────────────────┼─────────────────────────────────────────────────────┤
  │ 8. 미지원          │ 벡터/행렬/텐서 연산 (v2+).                          │
  │                   │ 복소수 미분.                                         │
  │                   │ sin/cos/exp/log 등 수학 함수 (step27+에서 추가).     │
  │                   │ 다출력 함수 (Split 등, step34+).                    │
  └──────────────────────────────────────────────────────────────────────┘

  ★ 전제가 깨지면? — RuntimeError/TypeError로 방어. 상세는 core.py 각 가드 참조.
  ★ v1→v2 진화 시점: step34 (행렬 미분). 항목 013(derivative hook) 붕괴 지점.
"""

from rezero.v1.core import (
    Config,
    Function,
    Variable,
    as_array,
    as_variable,
    fill_grad,
    no_grad,
    using_config,
)
from rezero.v1.functions import (
    Add,
    Div,
    Mul,
    Neg,
    Pow,
    Square,
    Sub,
    add,
    div,
    mul,
    neg,
    pow,
    rdiv,
    rsub,
    square,
    sub,
)
from rezero.v1.utils import numerical_diff

__all__ = [
    # core
    "Config",
    "Function",
    "Variable",
    "as_array",
    "as_variable",
    "fill_grad",
    "no_grad",
    "using_config",
    # functions (wrapper)
    "add",
    "div",
    "mul",
    "neg",
    "pow",
    "rdiv",
    "rsub",
    "square",
    "sub",
    # functions (클래스 — 고급 사용자용)
    "Add",
    "Div",
    "Mul",
    "Neg",
    "Pow",
    "Square",
    "Sub",
    # utils
    "numerical_diff",
]
