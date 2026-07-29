"""
rezero.steps.step08 — [1고지] 재귀에서 반복문으로 역전파 고속화
===============================================

이 step에서 배울 것:
  - step07의 재귀적 backward()를 **반복문(while + 리스트 스택)**으로 전환
  - 재귀 vs 반복문: 동작 등가성 (같은 결과 3.2974), 하지만 스택 오버플로 안전성 차이
  - 명시적 스택(list)으로 그래프를 역방향 순회하는 패턴

이전 step과의 연결:
  - step07 역전파 자동화 (재귀) → step08 반복문 전환
    · step07: backward(x) 재귀 호출로 creator 연쇄 (Python 호출 스택 사용)
    · step08: worklist 리스트를 스택으로 써서 while 루프로 순회 (힙에 리스트)
  - 수학적 구조는 동일 (right fold). 단지 펼치는 방식이 다를 뿐.

★ 핵심 동기: 왜 재귀에서 반복문으로?
  - Python 재귀 한계 (기본 sys.getrecursionlimit() ≈ 1000)
  - 깊은 계산 그래프(예: 긴 RNN 시퀀스)에선 재귀 깊이 = 그래프 깊이 → 스택 오버플로 위험
  - 반복문 + 명시적 스택(list)은 힙에 저장되어 깊이 제한에서 자유로움

★ rezero 변형 (항목 14번)의 힘 — step08이 거의 공짜인 이유:
  step07에서 backward를 Variable 메서드가 아니라 **전역 함수**로 뺐기 때문에,
  step08은 그 전역 함수의 **내부 구현**만 바꾸면 끝. Variable/Function/Square/Exp는
  한 줄도 안 바뀜.
  ★ 주의: "외부 API 유지"는 **내부 순회 방식에 한함**. 함수명 자체는 #015로 fill_grad로 바뀜 (아래).
  → 관심사 분리(SoC)가 "다음 step으로의 확장 비용"까지 낮추는 실증 사례.

★ step07 복선 회수: Function.__call__의 self.output 저장.
  step07에선 "저장만 하고 미사용, step08 반복문에서 실사용"이라고 복선 예고했음.
  반복문에선 재귀와 달리 "현재 노드의 출력 grad"를 호출 컨텍스트로 못 받으니,
  Function에 저장해둔 output(y)에서 y.grad를 직접 읽어와야 함. 여기서 회수.

참고 자료:
  - 원본 구현: steps/step08.py (Variable.backward를 while 루프로)
  - 이전 step: rezero/steps/step07.py (재귀 버전 — 이걸 반복문으로 바꾼 게 step08)
  - rezero 변형: REZERO_CHANGES.md 항목 14번 (전역 backward) + 항목 15~17번 (step08 추가 변형)

검증 포인트:
  - fill_grad(y) 결과가 step07과 동일 (3.297442541400256)
  - pyright: 환경성 에러 2개(override/numpy) + type 문 버전 에러 1개 (step23 설정 시 해결 예정)

★ upstream_grad 로직 단순화 (예고했던 검증 포인트, 결과):
  step07 재귀: 매 재귀 호출마다 3단계 우선순위 로직 실행 (upstream 결정)
  step08 반복문: 루프 **진입 전 한 번만** 실행. 루프 내부에선 y.grad를 그대로 읽음
  (이전 반복이 직접 x.grad=f.backward(...)로 설정했으니 이미 채워져 있음).
  → 재귀의 복잡했던 로직이 반복문에선 자연스럽게 단순화. 부수 이점.

★ step08 추가 변형 3종 (브로 코드 리뷰 6연타에서 파생):
  - 항목 15번: 전역 함수명 backward → fill_grad. "grad 채우기"가 핵심 동작 명시.
    역방향은 grad 연산의 유일한 방식이라 이름에 안 넣어도 암시. JAX jax.grad와 정신적 유사.
  - 항목 16번: assert → RuntimeError 전환 (검증 A) + 도입부 이동 (fail-fast).
    "creator 없는 변수에 fill_grad 호출"은 사용자 오용 → if/raise(런타임 검증)가 맞음.
    debugging.md 교훈 2 적용 — ★ -O 모드에서도 검증이 살아있음을 실증.
    ★ 도입부 이동으로 부작용(grad 설정) 회피 + fail-fast 동시 달성.
  - 항목 17번: funcs → worklist 리네임 + Worklist 타입 별칭.
    CS 학술 패턴 "Worklist Algorithm" 인식. work item = Function 인스턴스.
    design_patterns.md 패턴 4 등록.
  - ★★★ 변형 3종의 emergent design 시너지: guard(#016)가 start_var.creator를
    Optional→Function으로 좁혀줘서 Worklist 타입(#017)이 안전해짐.
    좋은 설계 결정들은 emergent하게 서로 강화함.

실행: uv run python rezero/steps/step08.py
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional, override

import numpy as np

# ★ Worklist 타입 별칭 (항목 17번 연장) — "work item = Function 인스턴스"를 타입 수준에서 명시.
# 브로 통찰: "work item이 Function 인스턴스" → 그러면 타입 힌트로 명확히 할 수 있지 않나?
# 단순 list가 아니라 "Function 인스턴스들의 처리 대기열"이라는 의미까지 타입으로 선언.
# Python 3.12+ `type` 문 (우리 환경 3.12 지원). 상세: design_patterns.md 패턴 4.
type Worklist = list[Function]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator).

    ★ step08 변경: **없음**. Variable은 step07과 완전히 동일.
    역전파 순회 로직은 전역 함수에 있고(step07 변형 항목 14번; step08에서 fill_grad로 개명, 항목 15번),
    그 함수의 내부만 재귀→반복문으로 바뀔 뿐 Variable 자체는 무관하다.
    이게 관심사 분리(SoC)의 힘 — 순회 방식이 바뀌어도 데이터 상자는 흔들리지 않음.

    상세: notes/design_patterns.md §1 Wrapper 패턴
    """

    def __init__(self, data: np.ndarray):
        self.data: np.ndarray = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 (순전파 시점에 __call__이 호출).

        ★ step08 변경: 없음. step07과 동일 (한 줄).
        step16 "복잡한 계산 그래프(generation)"에서 generation 설정 로직이 추가될 확장 포인트.
        """
        self.creator = func


class Function(ABC):
    """DeZero의 함수. Variable을 Variable로 변환하는 기반 클래스.

    ★ step08 변경: **없음**. Function, Square, Exp 모두 step07과 완전히 동일.
    apply/derivative hook 구조(항목 10~13번)도 그대로. step08이 건드리는 건
    오직 전역 fill_grad()의 **순회 방식**뿐. (★ step08에서 backward → fill_grad로 개명, 항목 15번)

    ★ step07 복선 회수 — self.output 저장:
      __call__이 `self.output = output`으로 출력을 저장해둠.
      step07에선 "미사용, step08에서 실사용" 복선이었음.
      → step08 반복문 fill_grad에서 `y = f.output; f.backward(y.grad)`로 회수.
      재귀에선 y를 호출 컨텍스트로 넘겼지만, 반복문에선 객체에 저장된 값을 읽어와야 함.
    """

    def __init__(self) -> None:
        self.input: Optional[Variable] = None
        self.output: Optional[Variable] = None

    def __call__(self, input_var: Variable) -> Variable:
        x = input_var.data
        y = self.forward(x)
        output = Variable(y)
        output.set_creator(self)
        self.input = input_var
        self.output = output            # ★ step08에서 실사용 (반복문 fill_grad가 f.output.grad를 읽음)
        return output

    def forward(self, x: np.ndarray) -> np.ndarray:
        """순전파: 기본 구현 (apply hook 호출). 자식은 apply 또는 forward 직접 오버라이드."""
        return self.apply(x)

    def apply(self, x: np.ndarray) -> np.ndarray:
        """함수 본문 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    def backward(self, upstream_grad: np.ndarray) -> np.ndarray:
        """역전파 (단일 노드): 기본 구현 (derivative hook × upstream). fold accumulator step.

        ★ 주의: 이건 **단일 노드**의 backward (자기 도함수 × 상류 누적값 반환).
        전체 그래프 순회는 아래 전역 fill_grad()가 담당. (★ step08에서 전역 함수명을 backward→fill_grad로
        바꿔, step07의 "이름 같고 역할 다름" 혼란이 해소됨 — 부수 효과.)
        """
        assert self.input is not None, "self.input must be set (__call__ should have run)"
        x = self.input.data
        df = self.derivative()
        local_deriv = df(x)
        return local_deriv * upstream_grad

    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        """도함수(함수 객체) 반환 hook. 자식이 채우거나 backward 직접 오버라이드."""
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Exp(Function):
    """지수 함수: x → e^x. 미분: f'(x) = e^x (자기 자신)."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:
        return np.exp(x)

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: np.exp(x)


def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
) -> None:
    """★ 자동 역전파 (반복문 — 명시적 스택). step08 핵심. (전역 함수 — 항목 14번 + ★ 항목 15번 작명)

    step07 재귀 버전을 반복문으로 전환. step07까지는 `backward`라 했으나,
    ★ step08에서 **`fill_grad`로 개명** (항목 15번 변형).
    이유: 이 함수가 실제로 하는 일은 "그래프 순회하며 각 변수 노드에 누적 미분값(grad)을 채우는 것".
    `backward`는 방향(역방향)만 말하고 결과(grad 채움)는 암시만 됨. `fill_grad`가 의미가 더 투명.
    (역방향은 어차피 grad 연산의 유일한 방식이라 암시돼도 OK — grad는 역전파로만 채워지므로.)

    Args:
        start_var: 역전파 시작점 Variable (보통 최종 출력 y).
        upstream_grad: 시작 누적 미분값. None이면 np.ones_like(start_var.data) 자동 사용.
            (★ 책 step09 복선을 우리는 step07 시점에서 시그니처로 해결)

    ★ 반복문 구조 (책 steps/step08.py Variable.backward와 동일 패턴, 전역 함수화 + 개명만 차이):
        worklist = [start_var.creator]   # 워크리스트 초기화 (시작점의 creator)
        while worklist:
            f = worklist.pop()           # 1. 노드 하나 꺼내기
            x, y = f.input, f.output     # 2. 입력/출력 회수 (★ y=f.output이 step07 복선 회수)
            x.grad = f.backward(y.grad)  # 3. 단일 노드 fold step (Function.backward)
            if x.creator is not None:    # 4. 입력이 원점이 아니면 다음 노드 워크리스트에 push
                worklist.append(x.creator)

    ★ upstream_grad 로직 단순화 (step07 대비):
      step07 재귀: 매 재귀 호출마다 3단계 우선순위(upstream 인자 / 기존 grad / ones_like) 실행.
      step08 반복문: **루프 진입 전 한 번만**. 루프 내부에선 y.grad를 그대로 읽음.
      이유 — 반복문에선 직전 반복이 `x.grad = f.backward(y.grad)`로 다음 y.grad를 채워둠.
      재귀의 "호출마다 upstream 결정"이 무의미해지는 구조적 차이.

    동작 흐름 (step05 통찰: 역전파 = right fold의 반복문 구현):
      [y] ─pop C→ b.grad=C.backward(y.grad) ─pop B→ a.grad=B.backward(b.grad) ─pop A→ x.grad=A.backward(a.grad)
      스택이 빌 때까지 입력 쪽으로 fold 누적. 재귀와 수학적으로 동일.

    ★ 왜 재귀에서 반복문으로? (이 step의 존재 이유):
      - Python 재귀 한계: sys.getrecursionlimit() 기본 ≈ 1000
      - 깊은 그래프(긴 RNN 시퀀스 등)에선 재귀 깊이 = 그래프 깊이 → RecursionError 위험
      - 반복문 + 리스트 스택은 힙에 저장 → 깊이 제한에서 자유로움
      (단, Python 리스트에도 메모리 한계는 있으나 호출 스택보다 훨씬 큼)

    ★ 검증 설계 (step08 개선 — debugging.md 교훈 2 + fail-fast 적용):
      - (A) start_var.creator None → RuntimeError (사용자 오용, -O에서도 살아남아야)
            ★ **함수 도입부 맨 앞**에서 검사 — fail-fast 원칙 (잘못된 입력이면 즉시 실패,
               부작용인 start_var.grad 설정조차 일으키지 않음 — transactional semantics).
            cf. debugging.md "런타임 데이터 검증엔 if/raise, assert 금지"
      - (B)(C) f.input/f.output/y.grad None → assert (프로그래먘 불변조건, -O에서 사라져도 안전)
            cf. debugging.md "프로그래먘 논리 가정은 assert"

    주의:
      - fill_grad(start_var) (전역, 전체 순회) vs Function.backward(self, gy) (단일 노드).
        전역 함수 이름은 `fill_grad`로 바꿨지만, Function.backward는 단일 노드 역할이라 이름 유지.
        (이름이 다르므로 step07의 "이름 같고 역할 다름" 혼란도 해소 — 부수 효과.)
    """
    # ★ 검증 (A) — ★★ 함수 도입부 맨 앞 (fail-fast / guard clause).
    # 잘못된 입력(creator 없는 변수)이면 부작용(grad 설정)도 일으키지 않고 즉시 실패.
    # (이전엔 upstream 설정 **후**에 검사했으나, 그러면 에러 내기 전에 start_var.grad를 변경해버림.
    #  브로 지적: "오류 체크는 메서드 도입부 초반에 바로 해주는 게 나은 것 아니냐" — 정확함.)
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    # ★ 시작 upstream 결정 — 루프 진입 전 한 번만 (step07의 3단계 우선순위, 반복문에선 단순화)
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        start_var.grad = np.ones_like(start_var.data)
    # (start_var.grad가 이미 있으면 그대로 사용 — 재귀와 달리 매 호출마다 다시 결정할 필요 없음)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm) ----------
    # ★ worklist (항목 17번 리네임): "역전파 처리 대기 Function들의 스택".
    #   work item = Function 인스턴스 (Square/Exp 등). worklist 알고리즘에서 "work item이 무엇인가"가
    #   알고리즘의 정체를 결정 — 우리는 work item이 Function 인스턴스 → 역전파가 됨.
    #   이 구조는 CS 학술 패턴 "Worklist Algorithm"의 인스턴스 — 컴파일러 데이터플로우 분석,
    #   가비지 컬렉션 mark phase, 그래프 순회 등 전반에 쓰이는 "처리할 work item 대기열 + while pop" 패턴.
    #   상세: design_patterns.md 패턴 4 "Worklist Algorithm".
    # ★ 왜 리스트(=스택)인가? — 현재(step08 선형 체인)은 길이 1뿐이지만, step14(같은 변수 반복)/
    #   step16(DAG 분기 그래프)에서 복수 노드 push를 대비한 복선 (design_patterns 패턴 3 참고).
    #   선형에선 단일 변수 루프와 동일하지만, 분기 그래프에선 pop 1개 → push 2개 식으로 커짐.
    worklist: Worklist = [start_var.creator]   # ★ 타입 힌트 (항목 17번 연장) — work item = Function 인스턴스.
    # guard(#016)가 start_var.creator를 Optional[Function] → Function으로 좁혀줘서 list[Function] 안전.
    # → #016(fail-fast)과 #017(worklist)의 시너지: guard가 단순 빠른 실패가 아니라 타입 안전성까지 보너스.
    while worklist:
        f = worklist.pop()                 # 1. 처리할 노드 하나 꺼내기 (LIFO)
        # (검증 A에서 start_var.creator 보장 + x.creator push 전 None 체크하므로 f는 항상 Function)
        x = f.input                        # 2. 그 노드의 입력(=이전 변수)
        y = f.output                       # ★ 2b. 그 노드의 출력 — step07 복선 회수 (저장해둔 self.output)

        # ★ 검증 (B)(C): 불변조건 (프로그래먘 논리 가정) — assert 적절. -O에서 사라져도
        # 로직 자체는 안전 (이 조건 위반은 __call__/이전 반복의 구현 버그이지 런타임 데이터 문제가 아님).
        assert x is not None and y is not None, "f.input/f.output must be set (__call__ should have run)"
        assert y.grad is not None, "y.grad must be filled (start or previous iteration sets it)"

        x.grad = f.backward(y.grad)        # 3. 단일 노드 fold step (Function.backward — 자기 도함수 곱함)

        if x.creator is not None:          # 4. 입력이 그래프 원점이 아니면 다음 노드 워크리스트에 push
            worklist.append(x.creator)
        # x.creator가 None이면 x는 사용자 입력(원점) → 더 이상 거슬러 갈 곳 없음 → push 안 함


# --- 순전파: x → A(Square) → a → B(Exp) → b → C(Square) → y -------------
# step07과 동일 — 그래프 구축 코드는 순회 방식과 무관.
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)
b = B(a)
y = C(b)

# --- 역전파: fill_grad(y) 한 번에 자동 연쇄 (반복문 버전) ----------------
# ★ step08 변경: 함수명 backward → fill_grad (항목 15번).
#   "grad 채우기"가 핵심 동작. 역방향은 grad 연산의 유일한 방식이라 이름에 안 넣어도 암시됨.
# 외부 API 변경: fill_grad(y) 호출 (step07의 backward(y)와 같은 자리).
# 차이점: 스택오버플로 안전 (깊은 그래프에서도 RecursionError 안 남).
fill_grad(y)                            # ★ 자동 역전파 (반복문) — while 루프로 C → B → A 순회
print(f"역전파 결과 x.grad: {x.grad}")
print(f"step07 (재귀) 결과와 동일: 3.297442541400256")
print(f"해석적 정답: e^0.5 · 2 ≈ 3.2974")
