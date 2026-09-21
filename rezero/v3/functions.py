"""rezero.v3.functions — 구체 함수들 (Square/Add/Mul/Neg/Sub/Div/Pow/Sin/Cos/Sum/Reshape/Transpose + wrapper).

rezero v3 (제 4고지 "신경망 만들기") 스코프의 구체 함수 모음.
v2에서 step37 브랜칭 — 고차 미분 지원 계승 + 텐서(다차원 ndarray) 1급 시민.
core.Function을 상속해 apply + derivative hook 구현.

★ 모듈 구조 (이슈 50 — 함수 3분류, A안 채택 2026-09-09):
    이 파일은 '펀더멘털' 분류 (단독 계층 X, 파라미터 X). activations.py는
    step40(활성함수 등장), layers.py는 step49(Layer 등장) 때 생성 —
    파일은 내용이 생기는 step에 만든다.

★ derivative hook 패턴 — 스칼라 출력 가정:
    부모 Function.backward가 chain rule fold step 일반화.
    자식은 apply(순수 수학) + derivative(도함수 hook)만 구현.

★ v2 계승 (step32): derivative가 Variable를 받는다 — 도함수 본문의 연산이
    Variable 연산이 되어, create_graph 컨텍스트에서 그래프를 남긴다.

★ 도함수 성분 유형 지도 (작업 4 — 탐구 노트 32 §5 분류를 코드에 반영):
    derivative hook이 "무엇에 의존하는가"로 유형화한 관습 지도.
    4고지(출력형 활성함수 sigmoid/relu 등 대거 등장) 전의 좌표.

    ① 상수형 (의존 없음)       — Add(1,1), Sub(1,-1), Neg(-1): 인자 무시 (lambda _:)
    ② 입력형 (자기 입력 x)     — Square(2x), Sin(cos), Cos(-sin), Pow(c·x^(c-1)):
                                "입력의 순수 함수" 관습 준수 — hook 인자만으로 계산.
                                ★ 변주 — Abs(np.sign(x.data)) / Sum(np.ones_like(x.data)):
                                **값 참조** (ndarray 반환, 그래프 무연결). Abs는 부호를,
                                Sum은 shape를 본다 (step37) — Sum의 ones * upstream이
                                곱셈 브로드캐스팅으로 0-dim upstream을 입력 shape로
                                자동 복원. dezero ReLU 관례 — 2계 미분이 이 갈래에서
                                소멸 (이슈 45).
    ③ 다른 입력형 (형제 입력)   — Mul(x1,x0), Div(1/x1, -x0/x1²): ★ 관습 위반 —
                                self.inputs에서 형제를 클로저 캡처. 수학적 필연
                                (곱셈 법칙 자체가 형제 값 요구). v2에선 형제도
                                그래프에 있어 2차 미분 자동 연결 — 실해는 없음.
    ④ 출력형 (forward 출력 y)   — Tanh: 미분식 1-y². 구현 2전략 (Config.reuse_output)
                                — 재호출(1-tanh(x)², 관습 준수) / 재사용(1-y·y,
                                self.output 참조). y가 weakref로 소멸 가능해 유일하게
                                "전략 선택"이 필요한 유형.
    (+ 입출력형 = ②+④ 조합)    — 미등장 (4고지 예고 — SiLU 등, 유형 아닌 조합)
    ★ ⑤ upstream형 (gy 자체)  — hook의 세계 밖: backward 직접 오버라이드.
                                 ★ 첫 사례 step38 Reshape/Transpose (2026-09-21) —
                                 gy를 입력 shape으로 되돌림 (곱셈 fold로 표현 불가:
                                 shape이 다른 배열은 곱 자체가 성립 안 함. Sum의
                                 "ones * 0-dim upstream" 트릭이 안 통하는 이유).
                                 본격 사례 MatMul: gx = gy·Wᵀ (step41, 탐구 노트 35 §5)
"""

from typing import override

import numpy as np

from rezero.v3.core import Config, DerivativeFn, Function, Variable, as_variable


# ===== 구체 함수 클래스 =========================================================
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** 2

    @override
    def derivative(self) -> DerivativeFn:
        # 본문은 v1과 동일 — x가 Variable이 되면 2 * x는 x.__rmul__ → mul() 호출.
        return lambda x: 2 * x


class Add(Function):
    """덧셈: (x0, x1) → x0 + x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 + x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        # 상수 1은 float 반환 — backward에서 1 * upstream 시 __rmul__로 Variable화.
        return (lambda _: 1, lambda _: 1)


class Mul(Function):
    """곱셈: (x0, x1) → x0 * x1. 미분: ∂y/∂x0 = x1, ∂y/∂x1 = x0."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 * x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        # ★ v2: .data를 꺼내지 않고 Variable 그대로 — gx가 그래프를 가진다.
        #   (v1: x1 = self.inputs[1].data — ndarray라 그래프 연결 상실)
        x0 = self.inputs[0]
        x1 = self.inputs[1]
        return (lambda _: x1, lambda _: x0)


class Neg(Function):
    """단항 부호: x → -x. 미분: f'(x) = -1 (상수).

    ★ step34 버그 수정 (2026-08-24): v1부터 `lambda x: -1.0 * x`였는데 이는
    도함수(-1)가 아니라 원 함수(-x) 반환 — y=-x의 미분이 -x가 되는 버그.
    sin 고차 미분 3차부터 발동 (Neg.backward 첫 호출 시점)해 발견.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return -x

    @override
    def derivative(self) -> DerivativeFn:
        # 도함수는 상수 -1 (float) — backward에서 -1.0 * upstream → __rmul__.
        return lambda _: -1.0


class Sub(Function):
    """뺄셈: (x0, x1) → x0 - x1. 미분: ∂y/∂x0 = 1, ∂y/∂x1 = -1. 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 - x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        return (lambda _: 1, lambda _: -1)


class Div(Function):
    """나눗셈: (x0, x1) → x0 / x1. 미분: ∂y/∂x0 = 1/x1, ∂y/∂x1 = -x0/x1². 비교환."""

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x0 / x1

    @override
    def derivative(self) -> tuple[DerivativeFn, ...]:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        # ★ v2: Variable 그대로 — 1/x1은 __rtruediv__, x1**2는 __pow__,
        #   -x0는 __neg__ → 전부 Variable 연산으로 그래프 생성.
        x0 = self.inputs[0]
        x1 = self.inputs[1]
        return (lambda _: 1 / x1, lambda _: -x0 / x1 ** 2)


class Pow(Function):
    """거듭제곱: x → x**c. 미분: f'(x) = c·x^(c-1).

    c는 상수 (Variable 아님, 미분 대상 아님).
    __init__(c)에서 c 저장, apply/derivative에서 self.c 참조.
    """

    def __init__(self, c: "int | float") -> None:
        self.c = c                     # 커스텀 — c만 이 클래스에서 저장
        super().__init__()             # inputs/output/generation은 부모가 초기화

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x ** self.c

    @override
    def derivative(self) -> DerivativeFn:
        # 본문 그대로 — c * x**(c-1)이 Variable 연산으로 자동 전환.
        c = self.c
        return lambda x: c * x ** (c - 1)

    @override
    def dot_label(self, show_param: bool = False) -> str:
        return f'Pow(c={self.c})' if show_param else 'Pow'


class Sin(Function):
    """사인: x → sin(x). 미분: f'(x) = cos(x).

    step27에서 v1 첫 수학 함수로 추가. ★ v2: derivative가 cos **함수**를
    호출 (np.cos가 아니라) — Variable 세계에서 그래프가 연결된다.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.sin(x)

    @override
    def derivative(self) -> DerivativeFn:
        return lambda x: cos(x)


class Cos(Function):
    """코사인: x → cos(x). 미분: f'(x) = -sin(x).

    ★ step32 신규 — Sin의 고차 미분을 위한 함수. sin의 1차 미분이 cos이므로,
    2차 미분(sin''= -sin)까지 그래프를 타고 내려가려면 cos가 Variable 연산이어야 함.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.cos(x)

    @override
    def derivative(self) -> DerivativeFn:
        return lambda x: -sin(x)


class Tanh(Function):
    """하이퍼볼릭 탄젠트: x → tanh(x). 미분: f'(x) = 1 - tanh(x)².

    ★ step35 신규 — 도함수가 **자기 자신을 참조**하는 특이 구조.
    4고지 신경망 활성함수 예습이기도 함.

    ★ derivative 구현 전략 2종 (Config.reuse_output — 브로 제안, step18 철학 계승):
    - False (기본): tanh(x) **재호출** — 도함수 식이 그래프에 self-contained로
      명시 (1-tanh² 구조가 노드로 보임). Tanh 노드가 미분마다 추가되어 지수 폭증
      (그래프 3형태 '폭증'의 교재 — 탐구 노트 32).
    - True: forward **출력 y 재사용** (dezero 방식) — 계산 이득 (tanh 재계산 없음)
      + Tanh 노드 1개 유지 (폭증 완화). 실증: 재호출 2→4→8 vs 재사용 1→1→1.
    ★ 읽히는 시점 = 역전파 (derivative는 fill_grad 중 호출) — 순전파가 아니라
      using_config 블록이 fill_grad를 감싸야 효과가 있다.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.tanh(x)

    @override
    def derivative(self) -> DerivativeFn:
        if Config.reuse_output:
            # forward 출력 재사용 — weakref 역참조를 클로저로 캡처 (브로 발견).
            output_ref = self.output
            assert output_ref is not None, "self.output must be set (__call__ should have run)"
            y = output_ref()
            assert y is not None, "output Variable이 이미 회수됨 — 역참조 불가"
            return lambda _: 1 - y * y

        # 재호출 — tanh(x)가 새 Tanh 노드를 만들며 그래프에 추가 (명시형).
        # 1 - ...은 __rsub__, **2는 __pow__ — 전부 Variable 연산으로 2차 미분 연결.
        return lambda x: 1 - tanh(x) ** 2

    @override
    def dot_label(self, show_param: bool = False) -> str:
        if show_param and Config.reuse_output:
            return 'Tanh(reuse)'
        return 'Tanh'


class Abs(Function):
    """절댓값: x → |x|. 미분: f'(x) = sign(x).

    ★ 부호 참조형 (노트 32 '입력형'의 순수 표본, 이슈 45 투어용) —
    도함수가 출력 z가 아니라 **입력 x의 부호**를 본다.

    ★ 값 참조 방식 (dezero ReLU 관례, 지도 ②의 변주): np.sign(x.data)를
    ndarray로 반환 — x의 그래프와 **무연결**인 상수 ±1. 따라서 2계 백프롭
    시 이 경로는 그래프를 남기지 않는다 (소멸 관찰 대상).
    심볼릭 버전 (gy * (x / |x|) — 그래프 유지) 과의 비교는 투어에서.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return np.abs(x)

    @override
    def derivative(self) -> DerivativeFn:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        data = self.inputs[0].data
        assert data is not None, "inputs[0].data must be set (apply should have run)"

        # np.sign(data) — ndarray 값 (그래프 없음). backward가 upstream과 곱하면
        # 리프 Variable(±1)로 참여 → 2계 미분은 이 갈래에서 상수 취급.
        return lambda _: np.sign(data)


class Identity(Function):
    """항등함수: x → x. 미분: f'(x) = 1 (모든 지점).

    ★ 상수형 도함수의 순수 표본 (지도 ①) — derivative가 입력/출력 무관 상수 1.
    abs(부호 참조)와 한 쌍: 그래프 구조는 동일 패턴(리프 상수 + Mul)이나
    상수의 값이 x에 의존하지 않음 — 3영역(x>0/x<0/x=0) 전부 gx = 1.

    ★ 실전 선례 torch.nn.Identity — ResNet 스킵 연결의 자리표시자.
    노트 36 §8 조사 리스트 4번 회수 (2026-08-31 브로 작성).
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x

    @override
    def derivative(self) -> DerivativeFn:
        # 상수 1 (float) — backward에서 1 * upstream → __rmul__ → 리프 1과 Mul.
        return lambda _: 1


class Sum(Function):
    """전체 원소 합: x → x.sum(). 미분: ∂y/∂x_i = 1 (모든 원소).

    ★ step37 신규 — "텐서를 다루다" (4고지 개막). 텐서(다차원 ndarray)를
    0-dim으로 축소 — 신경망 손실 함수(loss = 오차들의 합)의 원형.

    역전파 — 도함수는 ones (값 참조 ndarray, Abs 관례의 shape판):
    backward 뼈대의 local_deriv * upstream이 곱셈 브로드캐스팅으로
    0-dim upstream을 입력 shape로 자동 복원한다.
    ★ "브로드캐스팅 = 미분의 shape 복원 장치" (이 step의 심장).
    dezero는 backward 직접 오버라이드(np.broadcast_to) — rezero는 hook 유지.

    ★ 페이스 주의 — 책 37단계 본문은 Sum 구현을 설명하지 않고 정답지가 미리
    만들어진 dezero 패키지를 사용만 함 (책의 스텝바이스텝 추가가 '대충'이
    되는 지점 — 브로 지적). sum_to/broadcast_to, axis/keepdims는 뒷 스텝에서
    상세화 — 여기선 데모 동작에 필요한 최소분(전체 합만).
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x.sum()

    @override
    def derivative(self) -> DerivativeFn:
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        data = self.inputs[0].data
        assert data is not None, "inputs[0].data must be set (apply should have run)"

        # np.ones_like(data) — 그래프와 무연결인 상수 (값 참조, Abs 관례).
        # backward에서 ones * upstream → 브로드캐스팅 → 입력 shape의 grad.
        return lambda _: np.ones_like(data)


class Reshape(Function):
    """형상 변환: x → x.reshape(shape). 미분: gy를 입력 shape으로 되돌림.

    ★ step38 신규 — "형상 변환 함수". 값은 하나도 바꾸지 않고 shape만 이동.
    신경망(행렬 곱) 시대의 인프라 — MatMul(step41 예고)을 앞두고 shape 관리
    도구를 먼저 확보하는 step. 브로드캐스팅(간접)과 달리 "명시적" shape 제어.

    ★★ backward 직접 오버라이드 — 도함수 성분 유형 지도 ⑤ upstream형의 첫 사례:
        rezero의 backward 뼈대는 df(x) * upstream **곱셈 fold**인데, reshape는
        곱셈으로 표현 불가 — 도함수는 입력 shape, upstream은 출력 shape라
        브로드캐스팅 자체가 성립 안 함 (Sum의 "ones * 0-dim" 트릭이 안 통함).
        역전파의 본체는 "upstream을 입력 shape으로 되돌리는 것" — 곱이 아니라 이동.
        derivative()는 미구현 (⑤형은 hook의 세계 밖).
        (선형대수 관점: reshape은 치환행렬 P인 선형 사상이고 미분은 P⁻¹ 되돌림 —
        P를 실체화하는 대신 희소 구조만 이용하는 게 autograd의 관례)

    ★ x_shape은 apply(순전파) 시점 스냅샷 — backward에서 self.inputs를 다시 읽지
        않음: "미분은 (순전파 시점의) 형상을 기억한다". backward 시점 상태에
        의존하지 않는 스냅샷이 더 견고 (PyTorch도 forward에서 입력 shape 저장).
        (변형 포인트 3 — 브로 위임 결정, 2026-09-21)

    ★★ NumPy 경고 — np.reshape은 가능하면 **view**를 반환 (메모리 공유!):
        y.data와 x.data가 같은 버퍼를 볼 수 있음. rezero 전제(data를 불변처럼
        사용)에서는 안전하지만, in-place 연산이 미래에 등장하면 함경 지점.
        실수 방지 문서화 (브로 요청, 2026-09-21).
    """

    def __init__(self, shape: tuple[int, ...]) -> None:
        self.shape = shape                             # 커스텀 — 목표 shape 저장
        self.x_shape: tuple[int, ...] | None = None    # apply에서 채움 (backward 재료)
        super().__init__()                             # inputs/output/generation은 부모가 초기화

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        self.x_shape = x.shape  # 순전파 시점 스냅샷 — backward가 기억하는 "그 형상"

        return x.reshape(self.shape)

    @override
    def backward(self, upstream_grad: "Variable") -> tuple["Variable", ...]:
        """⑤ upstream형 — gy 자체를 입력 shape으로 되돌려 반환 (곱셈 없음).

        모듈 레벨 reshape()를 호출 (raw np.reshape 금지) — backward가 fill_grad의
        using_config('enable_backprop', create_graph) 컨텍스트 안에서 실행되므로,
        모듈 함수여야 2계 미분 그래프까지 자연 연결된다.
        """
        assert self.x_shape is not None, "self.x_shape must be set (apply should have run)"

        return (reshape(upstream_grad, self.x_shape),)


class Transpose(Function):
    """전치: x → x.transpose() — 모든 축을 역순으로. 미분: transpose (자기 역함수).

    ★ step38 신규 — 최소분 (axes=None, 전체 축 역순만). 책 38단계 데모 범위.
        2차원: 행/열 교환. 1차원: 역순이 없어 identity.

    ★ 미분이 자기 자신 — involution (전치의 전치 = 항등). Neg과 같은 "자기 역"
        부류: backward가 forward와 같은 호출. Reshape과 함께 ⑤ upstream형 —
        gy를 전치해 반환 (곱셈 fold로 표현 불가).

    ★ 상태 없는 함수 — __init__ 없음 (Reshape는 shape/x_shape를 저장하지만
        Transpose는 기억할 것이 없음). forward와 backward가 대칭인 무상태 함수.

    ★ 확장 포인트 (기록만 — 현재 step 스코프 밖, 브로 방침 2026-09-21):
        axes 지정 전치 (transpose(x, (1, 0)))와 역치환 계산
        (inv_axes = tuple(np.argsort([ax % n for ax in axes]))) —
        정답지 최종형 dezero/functions.py 참조. 합성곱(5고지) 언저리에서 필요 예정.
    """

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        return x.transpose()

    @override
    def backward(self, upstream_grad: "Variable") -> tuple["Variable", ...]:
        # 전치의 역전파 = 전치 (involution). 모듈 함수 호출로 2계 미분 연결 유지.
        return (transpose(upstream_grad),)


# ===== wrapper 함수 ============================================================
# wrapper는 단순하게 (Function.__call__ 도입부의 as_variable이 변환 처리).
def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


def add(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """덧셈 wrapper. x1은 Variable/ndarray/scalar 모두 가능."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def mul(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """곱셈 wrapper."""
    result = Mul()(x0, x1)
    assert isinstance(result, Variable), "Mul은 단일 출력이므로 Variable이어야 함"
    return result


def neg(x: Variable) -> Variable:
    """단항 부호 wrapper: -x."""
    result = Neg()(x)
    assert isinstance(result, Variable), "Neg는 단일 출력이므로 Variable이어야 함"
    return result


def sub(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """뺄셈 wrapper: x0 - x1."""
    result = Sub()(x0, x1)
    assert isinstance(result, Variable), "Sub는 단일 출력이므로 Variable이어야 함"
    return result


def rsub(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """역순 뺄셈 wrapper: x1 - x0 (비교환 → 순서 뒤집기).

    `2.0 - x` → Python이 x.__rsub__(2.0) 호출 → rsub(x, 2.0) → Sub()(2.0, x).
    """
    result = Sub()(x1, x0)
    assert isinstance(result, Variable), "rsub는 단일 출력이므로 Variable이어야 함"
    return result


def div(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """나눗셈 wrapper: x0 / x1."""
    result = Div()(x0, x1)
    assert isinstance(result, Variable), "Div는 단일 출력이므로 Variable이어야 함"
    return result


def rdiv(x0: Variable, x1: "Variable | np.ndarray | float | int") -> Variable:
    """역순 나눗셈 wrapper: x1 / x0 (비교환 → 순서 뒤집기).

    `3.0 / x` → Python이 x.__rtruediv__(3.0) 호출 → rdiv(x, 3.0) → Div()(3.0, x).
    """
    result = Div()(x1, x0)
    assert isinstance(result, Variable), "rdiv는 단일 출력이므로 Variable이어야 함"
    return result


def pow(x: Variable, c: "int | float") -> Variable:
    """거듭제곱 wrapper: x ** c. c는 상수 (Variable 아님)."""
    result = Pow(c)(x)
    assert isinstance(result, Variable), "Pow는 단일 출력이므로 Variable이어야 함"
    return result


def sin(x: Variable) -> Variable:
    """사인 wrapper: sin(x)."""
    result = Sin()(x)
    assert isinstance(result, Variable), "Sin은 단일 출력이므로 Variable이어야 함"
    return result


def cos(x: Variable) -> Variable:
    """코사인 wrapper: cos(x). ★ step32 신규 — Sin 고차 미분용."""
    result = Cos()(x)
    assert isinstance(result, Variable), "Cos는 단일 출력이므로 Variable이어야 함"
    return result


def tanh(x: Variable) -> Variable:
    """하이퍼볼릭 탄젠트 wrapper: tanh(x). ★ step35 신규 — 자기 참조 도함수.

    derivative 전략은 Config.reuse_output (전역 스위치)로 선택 —
    using_config('reuse_output', True) 블록이 fill_grad를 감싸면 효율형.
    """
    result = Tanh()(x)
    assert isinstance(result, Variable), "Tanh은 단일 출력이므로 Variable이어야 함"
    return result


def abs(x: Variable) -> Variable:
    """절댓값 wrapper: |x|. ★ 이슈 45 투어용 — 부호 참조형 (미분 = sign(x)).

    Python 내장 abs()와 1:1 — Variable의 __abs__ 던더가 이 wrapper를 호출.
    """
    result = Abs()(x)
    assert isinstance(result, Variable), "Abs는 단일 출력이므로 Variable이어야 함"
    return result


def identity(x: Variable) -> Variable:
    """항등함수 wrapper: x → x. ★ 이슈 45 투어용 — 상수형 도함수 (미분 = 1).

    출력이 곧 입력 — 그래프에 '아무 일도 안 하는' 노드를 남길 때 사용.
    """
    result = Identity()(x)
    assert isinstance(result, Variable), "Identity는 단일 출력이므로 Variable이어야 함"
    return result


def sum(x: Variable) -> Variable:
    """전체 합 wrapper: 모든 원소를 더해 0-dim으로. ★ step37 신규 — 텐서→스칼라 축소.

    역전파는 도함수 ones와 곱셈 브로드캐스팅으로 shape 복원 (Sum 클래스 참조).
    axis/keepdims 지원은 뒷 스텝 — 여기선 전체 합만.
    """
    result = Sum()(x)
    assert isinstance(result, Variable), "Sum은 단일 출력이므로 Variable이어야 함"
    return result


def reshape(x: Variable, shape: tuple[int, ...]) -> Variable:
    """형상 변환 wrapper: x → x.reshape(shape). ★ step38 신규 — 값 불변, shape만.

    no-op 최적화 (변형 포인트 2 채택, dezero 관례): 이미 같은 shape이면
    노드를 만들지 않고 x 자체를 반환 — 그래프에 항등 Reshape 노드가 쌓이지
    않는다. 수학적으로도 손실 0 (reshape의 미분은 shape 되돌림뿐, 값 변화 없음).
    """
    if x.shape == shape:
        return as_variable(x)

    result = Reshape(shape)(x)
    assert isinstance(result, Variable), "Reshape는 단일 출력이므로 Variable이어야 함"
    return result


def transpose(x: Variable) -> Variable:
    """전치 wrapper: x → x.T (모든 축 역순). ★ step38 신규.

    미분이 자기 자신 (involution) — backward도 transpose 호출 (Transpose 클래스).
    axes 지정은 최소분에서 제외 (확장 포인트 — 클래스 docstring 참조).
    """
    result = Transpose()(x)
    assert isinstance(result, Variable), "Transpose는 단일 출력이므로 Variable이어야 함"
    return result
