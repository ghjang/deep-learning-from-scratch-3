"""
rezero.steps.step07 — [1고지] 역전파 자동화 (재귀적 right fold)
===============================================

이 step에서 배울 것:
  - Variable.creator 속성 — "나를 만든 함수" 역방향 링크
  - Variable.set_creator(func) — creator 설정 헬퍼
  - 전역 backward(start_var) ★ — 재귀로 creator 연쇄 (자동 역전파 핵심)
  - Function.__call__에서 output.set_creator(self) — 순전파 시점에 연결

이전 step과의 연결:
  - step06 수동 역전파 → step07 자동화
    · step06: right fold를 손으로 한 스텝씩 unfold (C/B/A.backward 직접 호출)
    · step07: creator 연쇄로 backward(y) 한 번에 자동 펼침 (재귀)
  - step05 통찰 회수: 역전파 = right fold (foldr)의 **재귀적 구현**
  - Define-by-Run 완성: 순전파 시점에 그래프를 자동 기록 (output.set_creator)

★ step07 변형 (REZERO_CHANGES.md 항목 1, 10~14번 — step06 변형에 이어 5개 추가):
  - #010: derivative hook (backward에 Template Method 재적용 — DRY)
  - #011: apply hook (forward에도 동일 구조 — 대칭 완성)
  - #012: set_creator 메서드 유지 (generation 복선 발견)
  - #013: derivative callable 반환 (도함수 객체 — 노트 13번 §4 구현)
  - #014: ★★★ backward를 Variable 메서드 → 전역 함수로 분리 (JAX 스타일, rezero 정체성)
  - #001: 전체 시그니처 타입 힌트 세트 도입 (교훈: 부분 도입 금물)

참고 자료:
  - 원본 구현: steps/step07.py
  - right fold 통찰: notes/exploration_13_derivative_notation.md §8
  - step07 변형 전체: REZERO_CHANGES.md 항목 10~14번

검증 포인트:
  - backward(y) 한 번으로 step06과 같은 결과(3.2974) 나오는지 확인
  - 합성 y=(e^(x²))², x=0.5 → 해석적 정답 ≈ 3.2974

주의:
  - 전역 backward(start_var) vs Function.backward(gy) 이름 같은데 역할 완전 다름
    · backward(start_var)         : 전역 함수, 전체 역전파 연쇄 (#014 변형)
    · Function.backward(self, gy) : 단일 노드의 국소적 미분 (step06 구현)
  - 재귀는 깊은 그래프에서 스택 오버플로 위험 → step08 반복문으로 해결 (예고)

실행: uv run python rezero/steps/step07.py
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional, override

import numpy as np


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    래퍼 패턴: ndarray를 감싸서 메타정보를 붙이는 토대.
    ★ step07 변경:
      - creator 속성 추가 — "이 Variable을 만든 Function" 역방향 링크. 역전파 자동화의 핵심.
      - set_creator() 메서드 추가 — creator 설정 헬퍼 (캡슐화 의도; 현재는 단순 할당이지만
        미래 로직 추가를 대비한 확장 포인트로 책이 택한 관례).
      - ★★ 역전파 순회(backward)는 Variable 메서드가 아니라 전역 함수로 분리 (#014).
        Variable은 "순수 데이터 상자"로 회귀 — 그래프 순회 로직은 갖지 않음 (관심사 분리).
    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data: np.ndarray):
        self.data: np.ndarray = data
        # ★ data는 항상 ndarray (DeZero의 고정 — 책 step37 부턴 런타임 isinstance 체크로 보장,
        # 우리는 타입 힌트로 정적 보장. 런타임 체크는 추후 step37 시점에 도입 예정).
        self.grad: Optional[np.ndarray] = None
        # ★ 미분값(그래디언트). 라이프사이클: 역전파 전 None → 역전파 후 ndarray.
        self.creator: Optional["Function"] = None
        # ★ "나를 만든 Function" 역방향 링크.
        # None이면 이 Variable은 사용자가 직접 만든 입력(그래프의 원점).
        # Function 인스턴스가 오면, backward()에서 그 Function을 타고 이전 노드로 거슬러 감.
        # 타입: Optional["Function"] — string annotation (전방 참조, Variable이 Function보다 먼저 정의됨).

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 (순전파 시점에 __call__이 호출).

        ★ 메서드인 이유 (단순 속성 할당 아닌가?):
        현재(step07)는 `self.creator = func` 한 줄. `output.creator = self` 직접 할당과 동일.
        하지만 책 최종 코드(dezero/core.py:81-83)에선 **generation 설정**이 추가됨:
            self.creator = func
            self.generation = func.generation + 1   # ★ step16 "복잡한 계산 그래프(generation)" 복선
        → 책이 메서드로 둔 건 "generation 도입(step16)을 미리 대비한 확장 포인트".
        우리도 step07 시점에선 한 줄이지만, step16 진입 시 자연스럽게 generation 로직 추가 예정.
        """
        self.creator = func

    # ★ step07 변형: backward()는 Variable의 메서드가 아니라 전역 함수로 분리 (#014).
    # Variable은 "순수 데이터 상자" (data, grad, creator)로 회귀. 그래프 순회 로직은
    # 전역 backward() 함수로 이동 → 관심사 분리 (SoC). 자세한 건 파일 하단 backward() 참고.


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    ★★ step07 변형 구조 — Template Method with Hook (대칭 완성):
      - __call__: "상자 까기 → forward → 상자 포장" 흐름 고정 (최상위 뼈대)
      - forward(x): 기본 구현 제공 → "함수 본문" hook 인 apply(x) 호출
      - backward(gy): 기본 구현 제공 → "도함수" hook 인 derivative(x) 호출
      - apply(x): ★ 선택적 hook. 자식이 채우거나 forward 직접 오버라이드 (순전파)
      - derivative(x): ★ 선택적 hook. 자식이 채우거나 backward 직접 오버라이드 (역전파)

    forward/backward 대칭: 둘 다 "기본 구현 + 선택적 hook + 직접 오버라이드 탈출구".
    자식(Square 등)은 apply + derivative만 1줄씩 구현하면 순전파/역전파 모두 자동 작동.

    ★ 직접 인스턴스화 방지: 추상 메서드(@abstractmethod)가 없으므로 기술적으로
    Function() 생성 가능. 단, apply/derivative 미구현 상태로 forward/backward 호출하면
    NotImplementedError 발생. "추상 강제는 호출 시점" 전략 (선택적 hook 패턴의 특성).

    ★ step07 핵심 변경: __call__이 output.set_creator(self) 호출.
       → 순전파 시점에 역방향 링크(creator)를 기록. Define-by-Run의 핵심.
       역전파(backward) 시 creator 링크를 따라 자동 연쇄 가능해짐.

    ★ step07 변형 (apply/derivative hook 구조 — REZERO_CHANGES #010/#011/#013):
       forward/backward는 기본 구현(뼈대) 제공, apply/derivative는 선택적 hook.
       자식은 apply + derivative만 1줄씩 구현. derivative는 callable(도함수 객체) 반환.
       자세한 건 각 메서드 docstring + REZERO_CHANGES.md 항목 10~14번 참고.
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

    def __init__(self) -> None:
        # ★ 인스턴스 속성을 __init__에서 미리 선언 (타입 힌트 + pyright 추론 명확화).
        # 실제 값은 __call__에서 할당됨. 여기선 타입만 선언 (Optional, 호출 전엔 None).
        self.input: Optional[Variable] = None
        self.output: Optional[Variable] = None

    def __call__(self, input_var: Variable) -> Variable:
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② Template Method: 자식이 구현한 forward 호출
        output = Variable(y)            # ③ 상자 포장
        output.set_creator(self)        # ★ step07: 순전파 시점에 역방향 링크 기록 (Define-by-Run 핵심)
        self.input = input_var          # 입력 기억 (역전파용 — backward에서 쓰임, step04 복선 회수)
        self.output = output            # ★ step07: 출력 기억 (step08 반복문에서 실사용; 현재는 미사용 복선)
        return output

    def forward(self, x: np.ndarray) -> np.ndarray:
        """순전파: 입력 데이터 x를 연산해 출력 데이터 y를 반환.

        ★ 기본 구현 (Template Method 뼈대) — "함수 본문(apply)" hook을 호출.
        자식은 **둘 중 하나**로 순전파를 제공:
          (a) `apply()` 만 오버라이드 → 이 기본 forward가 자동으로 쓰임 (대부분의 경우)
          (b) forward 자체를 오버라이드 → 단순 apply 한 줄로 안 되는 특수한 연산

        ★ 왜 `forward`가 아니라 `apply`인가? — `forward`는 "어딘가로 포워딩(전달)한다"는
        뉘앙스가 있어 이 클래스가 표현하는 '함수 본문 실행'이라는 실제 역할과 어색했음.
        `apply`는 수학의 f(x) "함수 적용"과 정확히 일치 (Python 2 내장함수 apply와도 같은 의미).
        """
        return self.apply(x)

    def apply(self, x: np.ndarray) -> np.ndarray:
        """이 Function이 표현하는 함수의 본문. 선택적 hook — 자식이 채우거나 forward를 직접 오버라이드.

        ★ 이 메서드는 forward()의 기본 구현에서 호출됨. 자식이 제공하지 않으면
        forward()가 이 메서드를 호출하는 순간 NotImplementedError 발생.
        해결책 2가지:
          (a) 이 메서드만 오버라이드 (함수 본문 1줄) → forward 기본 구현 사용
          (b) forward 자체를 오버라이드 → 이 메서드 구현 불필요 (특수한 연산)

        참고: derivative와 동일한 "선택적 hook" 패턴. forward/backward 대칭 구조.
        """
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    def backward(self, upstream_grad: np.ndarray) -> np.ndarray:
        """역전파: 상류에서 접어 내려온 누적 미분값을 받아 자기 도함수를 곱해 한 번 더 접고,
        하류로 내려보낼 새 누적값을 반환. (★ step05 통찰: fold accumulator step)

        ★ 기본 구현 (Template Method 뼈대) — "도함수 × 상류 누적값" 이라는 가장 흔한 fold step.
        자식은 **둘 중 하나**로 역전파를 제공:
          (a) `derivative()` 만 오버라이드 → 이 기본 backward가 자동으로 쓰임 (대부분의 경우)
          (b) backward 자체를 오버라이드 → 도함수 한 줄로 안 되는 복잡한 연산
              (전치/브로드캐스팅/다입력 등, step34+ 행렬 미분에서 등장 예정)

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
        assert self.input is not None, "self.input must be set (__call__ should have run)"
        x = self.input.data             # 순전파 시 저장해둔 입력 회수 (step04 복선 회수)
        df = self.derivative()                       # ① 도함수(함수 객체) 획득 — 자식이 제공
        local_deriv = df(x)                          # ② 도함수를 현재 입력에서 평가 (df/dx 값)
        return local_deriv * upstream_grad           # ③ fold step (곱해서 누적) + ④ 다음 노드로 전달

    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        """도함수(함수 객체)를 반환. 선택적 hook — 자식이 채우거나 backward를 직접 오버라이드.

        ★ 브로 통찰 (노트 13번 §4 "도함수 = 고차 함수"의 코드 구현):
        derivative는 "도함수값(숫자)"이 아니라 **"도함수(함수 객체)"**를 반환.
        backward()가 그 함수 객체를 받아 현재 입력에서 평가 (df(x)).
        수학적으로: f'는 함수(f: X→Y를 미분한 새 규칙), f'(x)는 값(평가 결과).
        이 둘을 분리하면 여러 점에서 평가 가능, 이계도함수(f'') 확장도 자연스러움.

        ★ 이 메서드는 backward()의 기본 구현에서 호출됨. 자식이 제공하지 않으면
        backward()가 이 메서드를 호출하는 순간 NotImplementedError 발생.
        해결책 2가지:
          (a) 이 메서드만 오버라이드 (도함수 함수 반환 1줄) → backward 기본 구현 사용
          (b) backward 자체를 오버라이드 → 이 메서드 구현 불필요 (복잡한 연산)
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return x ** 2                   # ★ 함수 본문 1줄만 — forward는 부모의 기본 구현 사용

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x          # ★ 도함수 f'(x)=2x를 "함수 객체"로 반환 — backward는 부모 기본 구현 사용


class Exp(Function):
    """지수 함수: x → e^x. 미분: f'(x) = e^x (자기 자신)."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return np.exp(x)                # ★ 함수 본문 1줄만 — forward는 부모의 기본 구현 사용

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: np.exp(x)      # ★ 도함수 f'(x)=e^x를 "함수 객체"로 반환 — backward는 부모 기본 구현 사용


def backward(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (재귀적 right fold). step07 핵심. (전역 함수 — #014 변형)

    ★ 브로 통찰 (Q4 → RESEARCH_QUEUE #6 실증):
    원래 책/PyTorch에선 Variable.backward() 메서드. 하지만 "그래프 순회" 로직이
    "데이터 상자"인 Variable에 붙어 있으면 관심사 혼재.
    → Variable은 순수 데이터 상자(data, grad, creator)로 두고, 그래프 순회는
      이 전역 함수로 분리. (JAX의 jax.grad(f)(x) 함수형 패턴과 같은 철학)

    Args:
        start_var: 역전파를 시작할 Variable (보통 최종 출력 y). 역전파의 출발점.
            이름은 `input_var` (Function.__call__)과 같은 `_var` 접미사 관례 — Variable 타입 암시.
        upstream_grad: start_var에서 시작할 때의 초기 누적 미분값 (fold accumulator init).
            보통 1.0 (스칼라) 또는 np.ones_like(start_var.data) (텐서).
            None이면 자동으로 np.ones_like(start_var.data) 사용 (★ 책 step09의 복선을
            우리는 step07 시점에서 이미 함수 시그니처로 해결 — 사용자가 매번 grad 설정 안 해도 됨).

    ★ backward() vs Function.backward(gy) 이름 같은데 역할 완전 다름:
      - backward(start_var)            : 전역 함수, 전체 역전파 연쇄 (이 함수).
                                        start_var에서 시작해 creator 링크 따라 입력 쪽으로 재귀.
      - Function.backward(self, gy)    : 단일 노드의 국소적 미분 (step06 구현).
                                        gy(상류 누적값)를 받아 자기 도함수를 곱해 반환.

    동작 흐름 (step05 통찰: 역전파 = right fold의 재귀 구현):
      1. start_var에서 시작할 upstream 결정 (인자 or 자동 ones_like)
      2. start_var를 만든 함수(creator) 찾기
      3. creator가 None이면 → start_var는 입력 변수(원점), 연쇄 종료 (재귀 base case)
      4. creator의 backward(gy) 호출 → 단일 노드 fold step (자기 도함수 곱함)
      5. 그 결과를 이전 변수의 grad에 저장
      6. 이전 변수에 대해 backward() 재귀 호출 → 다음 노드로 연쇄 계속

    주의: 재귀라 깊은 그래프에선 스택 오버플로 위험 → step08에서 반복문으로 개선 (예고).
    패키지화(step23) 후엔 rezero.backward(y) 형태로 호출 (jax.grad(f)(x)와 같은 패턴).
    """
    # ★ 시작 upstream 결정 — 세 가지 우선순위:
    #   1. 사용자가 명시적으로 준 upstream_grad (최상위 호출에서 커스텀)
    #   2. 이미 설정된 start_var.grad (재귀 호출 — 이전 노드가 Function.backward로 채움)
    #   3. 둘 다 없으면 np.ones_like(start_var.data) (최초 시작점 자동 초기화)
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        start_var.grad = np.ones_like(start_var.data)
    # (start_var.grad가 이미 있으면 그대로 사용 — 재귀 시 이 경로. 덮어쓰기 금지 ★)
    f = start_var.creator                        # 1. start_var를 만든 함수 찾기
    if f is not None:                            # 2. creator가 None이면 입력(원점) → 종료
        x = f.input                              # 3. 그 함수의 입력(=이전 변수) 찾기
        assert x is not None, "f.input must be set (Function.__call__ should have run)"
        x.grad = f.backward(start_var.grad)      # 4. Function.backward로 fold step (자기 도함수 곱함)
        backward(x)                              # 5. ★ 재귀 — 이전 변수의 backward 또 호출 (연쇄)


# --- 순전파: x → A(Square) → a → B(Exp) → b → C(Square) → y -------------
# ★ step07 핵심: __call__이 output.set_creator(self)를 자동 호출하므로,
#    아래처럼 함수 연쇄만 해도 그래프(creator 링크)가 자동으로 기록된다. (Define-by-Run)
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# --- 역전파: backward(y) 한 번에 자동 연쇄 (step07 핵심, 전역 함수 #014) ----
# step06은 손으로 한 스텝씩 unfold (C/B/A.backward 직접 호출 5줄).
# step07은 backward(y) 한 줄이면 끝 — upstream_grad 기본값(None→ones_like)이 자동 적용.
# (필요시 backward(y, upstream_grad=np.array(2.0)) 식으로 커스텀 가능)
backward(y)                             # ★ 자동 역전파 (전역 함수) — 내부적으로 C → B → A 재귀 호출
print(f"역전파 결과 x.grad: {x.grad}")
print(f"step06 결과와 동일: 3.297442541400256 (수동 역전파)")
print(f"해석적 정답: e^0.5 · 2 ≈ 3.2974")
