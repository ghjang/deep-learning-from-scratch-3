"""rezero.v3 — 제 4고지 "신경망 만들기" (step37~51) 패키지.

v2 (제 3고지 고차 미분)를 step37에서 브랜칭 — 고차 미분 지원을 그대로 계승하며
텐서(다차원 ndarray)를 1급 시민으로 승격. 이후 Layer/Parameter/Model 등
신경망 구축 요소가 이 패키지에 추가된다.

사용:
    from rezero.v3 import Variable, fill_grad, sum

    x = Variable(np.array([[1., 2., 3.], [4., 5., 6.]]))   # 2x3 텐서
    y = sum(x * x)
    fill_grad(y, retain_grad=True)
    print(x.grad.data)   # [[2. 4. 6.] [8. 10. 12.]] ← 2x (element-wise)

★ 모듈 구조 (이슈 50 — 함수 3분류, A안 채택 2026-09-09):
    functions.py   펀더멘털 (add, mul, sum 등 — 단독 계층 X, 파라미터 X)
    activations.py 활성함수 (relu, sigmoid 등 — step40 등장 시 생성)
    layers.py      계층 (Linear 등 — step49 등장 시 생성)
    원칙: 파일은 내용이 생기는 step에 만든다 (빈 파일 사전 생성 안 함).
    장난감(sin, square 등)은 steps/ 소속 유지 — 승격 없음 (기존 원칙).

★★★ v3 사용 전제 (v2 전제에서 계승 + step37 변경분):

  0. ★ 텐서 1급 시민 (step37 "텐서를 다루다") — data에 다차원 ndarray 허용.
     기존 연산(Add/Mul/Pow/Sin/...)은 전부 element-wise라 v2 구조에서 무수정
     통과. sum()으로 텐서→0-dim 축소 (신경망 손실 loss = 오차들의 합의 원형).
  1. ★ grad 타입 — Variable (v2 계승). 값 접근은 x.grad.data. 재미분 가능.
  2. ★ create_graph — fill_grad(y, create_graph=True)로 역전파가 미분 계산
     그래프(2층)를 구성. 기본 False (lean).
     gx = x.grad는 Variable이므로 fill_grad(gx) 재호출이 2차 미분.
     ★ 재미분 결과가 **None이면 상수 도함수** 신호 — gx 그래프에서 x로 가는
     간선이 사라져 x.grad는 0이 아니라 None (수학적으론 dⁿy/dxⁿ = 0).
  3. ★ derivative hook — Callable[[Variable], Variable | float | ndarray].
     ndarray 반환은 '값 참조' 변주 (Abs/Sum — 그래프 무연결 상수).
  4. 출력 1개 — v2 계승. 다출력은 후속 step에서.
  5. Define-by-Run — 순전파 실행 시 그래프 자동 생성. 재사용 시 clear_grad().
  6. 그래프 구조 — DAG. 같은 Variable 다중 입력 허용, visited set 방어.
  7. 메모리/GC — Function.output은 weakref, inputs는 강한 참조.
  8. 모드/설정 — Config.enable_backprop / no_grad() / retain_grad /
     Config.reuse_output (Tanh 등 출력형 도함수의 전략 스위치).
  9. 연산자 — +, -, *, /, **, 단항 -, abs 지원.
 10. 수학 함수 — sin, cos, ★ sum (step37 — 전체 합. axis/keepdims는 뒷 스텝).

  ★ 전제가 깨지면? — RuntimeError/TypeError로 방어. core.py 각 가드 참조.
  ★ 브랜칭 경위: step37 (텐서를 다루다) — 구조 변경 없이 v2를 계승 (element-wise
    중심 구조가 텐서를 무수정 통과함을 확인하는 step). 고지 전환 = 버전 전환
    원칙 (step32 v1→v2 선례와 평행). Sum은 데모 동작에 필요한 최소분(전체 합만) —
    책은 37단계 본문에서 구현을 설명하지 않고 sum_to/broadcast_to 등과 함께
    뒷 스텝에서 상세화 (책의 스텝바이스텝이 슬슬 대충이 되는 지점, 브로 지적).
"""

from rezero.v3.core import (
    Config,
    DerivativeFn,
    Function,
    Variable,
    as_array,
    as_variable,
    backprop,
    fill_grad,
    no_grad,
    using_config,
)
from rezero.v3.functions import (
    Abs,
    Add,
    Cos,
    Div,
    Identity,
    Mul,
    Neg,
    Pow,
    Reshape,
    Sin,
    Square,
    Sub,
    Sum,
    Tanh,
    Transpose,
    abs,
    add,
    cos,
    div,
    identity,
    mul,
    neg,
    pow,
    rdiv,
    rsub,
    reshape,
    sin,
    square,
    sub,
    sum,
    tanh,
    transpose,
)
from rezero.v3.utils import (
    derive,
    fold_dot_graph,
    numerical_diff,
    plot_derivatives,
    plot_dot_graph,
)

__all__ = [
    # core
    "Config",
    "DerivativeFn",
    "Function",
    "Variable",
    "as_array",
    "as_variable",
    "backprop",
    "fill_grad",
    "no_grad",
    "using_config",
    # functions (wrapper)
    "abs",
    "add",
    "cos",
    "div",
    "identity",
    "mul",
    "neg",
    "pow",
    "rdiv",
    "rsub",
    "reshape",
    "sin",
    "square",
    "sub",
    "sum",
    "tanh",
    "transpose",
    # functions (클래스 — 고급 사용자용)
    "Abs",
    "Add",
    "Cos",
    "Div",
    "Identity",
    "Mul",
    "Neg",
    "Pow",
    "Reshape",
    "Sin",
    "Square",
    "Sub",
    "Sum",
    "Tanh",
    "Transpose",
    # utils
    "derive",
    "fold_dot_graph",
    "numerical_diff",
    "plot_derivatives",
    "plot_dot_graph",
]
