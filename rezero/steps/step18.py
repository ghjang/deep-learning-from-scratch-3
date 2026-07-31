"""
rezero.steps.step18 — [2고지] 메모리 절약 모드
===============================================

★ step17로 순환 참조는 해결했지만, 역전파 안 할 때도 계산 그래프를 만드는 낭비가 남아있음.
  추론(predict) 시엔 y.data만 필요한데 그래프까지 유지 → 큰 ndarray 시 메모리 폭발.
  Config 전역 플래그 + contextlib 컨텍스트 매니저로 "역전파 안 할 땐 그래프 안 만들기" 구현.

이 step에서 배울 것:
  - Config 클래스 — 전역 설정 (enable_backprop 플래그)
  - @contextlib.contextmanager + yield — with 블록으로 안전한 설정 변경/복구
  - no_grad() — "이 블록 안에서는 역전파 끔" 사용자 인터페이스
  - retain_grad — 역전파 후 중간 Variable grad 버리기 (최종 입력 grad만 필요할 때)

★★★ 핵심 문제 — 역전파 안 할 때도 그래프 만들면 메모리 낭비:
  step17까지는 순전파만 할 때도 역전파 대비 계산 그래프(creator, inputs, output weakref) 구축.
  추론(predict)은 순전파 값(y.data)만 필요한데 그래프까지 유지 → 큰 ndarray 시 메모리 폭발.

  예: 추론 루프에서 매번 큰 텐서로 순전파 → 역전파 안 하는데 그래프 쌓임 → OOM

★ 해법 — 전역 플래그 Config.enable_backprop:
  class Config:
      enable_backprop = True    # 전역 플래그 (기본: 역전파 ON)

  # Function.__call__:
  if Config.enable_backprop:           # ★ 역전파 할 때만 그래프 구축
      output.set_creator(self)
      self.inputs = inputs
      self.output = weakref.ref(output)
  return output                       # 역전파 안 하면 그래프 안 만듦

★ 사용자 인터페이스 — 컨텍스트 매니저 (with no_grad():):
  with no_grad():                  # ← 이 블록 안에서만 역전파 OFF
      x = Variable(np.array(2.0))
      y = square(x)                # 그래프 안 만듦
  # 블록 벗어나면 자동으로 역전파 다시 ON (finally에서 복구)

  매번 Config.enable_backprop = False 쓰기 귀찮고, 다시 True로 안 바꾸면 큰일.
  그래서 with 블록으로 안전하게. ★ 컨텍스트 매니저 이디엄 (PyTorch torch.no_grad()와 동일 패턴).

★ 추가 최적화 — retain_grad (역전파 후 중간 grad 버리기):
  보통 역전파는 최종 입력(x0.grad 등)만 필요. 중간 Variable(t.grad 등)의 grad은 안 씀.
  그래서 retain_grad=False(기본)로 두면, 역전파 후 중간 grad을 None으로 버림 → 메모리 절약.

  fill_grad(y)                   # retain_grad=False (기본): 중간 grad 버림
  fill_grad(y, retain_grad=True) # 중간 grad 유지 (디버깅 등特殊情况)

★★★ rezero 변형 포인트:
  | # | 포인트 | 책 방식 | 우리 방향 |
  |---|---|---|---|
  | A | Config 클래스 | 전역 클래스 | 동일 (Pythonic, PyTorch 방식) |
  | B | using_config / no_grad | @contextmanager + yield | 동일 — 컨텍스트 매니저 이디엄 그대로 |
  | C | __call__ 그래프 구축 조건부 | if Config.enable_backprop: | 동일 |
  | D | retain_grad 매개변수 | y.backward(retain_grad=False) | ★ fill_grad(y, retain_grad=False) (정체성 항목 014 유지) |

  A/B/C는 책 방식 그대로 (PyTorch 표준 패턴). D만 우리 정체성(항목 014) 적용.

★ 이 코드의 가정/전제 (step17 전제 + step18 새 전제):
  step17의 전제표 참조 + 이번 step에서 추가된 가정:

  | 새 전제 (step18)                                  | 의미                                     | 깨지면?                                              |
  |--------------------------------------------------|------------------------------------------|-----------------------------------------------------|
  | 전역 Config는 언제든 수정 가능                     | 전역 상태라 스레드 안전성 없음             | 멀티스레딩 시 위험 (PyTorch도 마찬가지)              |
  | 역전파 안 할 땐 그래프가 필요 없다                  | 추론(predict) 시 y.data만 필요            | no_grad 블록 안에서 y.backward() 호출하면 에러       |
  | retain_grad=False면 중간 grad는 버려도 된다        | 최종 입력 grad만 필요한 경우               | 중간 Variable grad 접근 시 None                     |

참고 자료:
  - 원본 구현: steps/step18.py
  - 이전 step: rezero/steps/step17.py (weakref — 이번에 Config/no_grad 추가)
  - rezero 변형: REZERO_CHANGES 항목 014 (fill_grad 전역 함수 — retain_grad 매개변수 확장)
  - 심화 배경: notes/exploration_23_contextmanager.md (contextlib/yield 마법)

검증 포인트:
  - no_grad 블록 안: 그래프 생성 안 됨 (creator/inputs/output 세팅 안 됨)
  - 일반 모드: 기존과 동일 (역전파 정상)
  - retain_grad=False (기본): 중간 Variable grad는 None (최종 입력만 grad 가짐)
  - retain_grad=True: 모든 Variable이 grad 가짐
  - 책 데모: y.grad/t.grad=None(None), x0.grad/x1.grad=2.0/1.0

실행:
  uv run python rezero/steps/step18.py
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator
from typing import Optional, override

import numpy as np


# ★★★ step18 핵심 — Config 전역 설정 + no_grad 컨텍스트 매니저 ---------------------
class Config:
    """★ step18 — 전역 설정 (역전파 on/off 플래그).

    클래스 변수 = 전역 상태. 모든 Function 인스턴스가 공유.
    enable_backprop=True (기본) → 역전파 대비 그래프 구축.
    enable_backprop=False       → 순전파 값만 (추론용, 메모리 절약).

    ★ cf. PyTorch torch.is_grad_enabled() / torch.set_grad_enabled() 와 같은 패턴.
    전역 상태라 스레드 안전성 없음 (PyTorch도 마찬가지 — 분산 학습시 별도 처리).
    """
    enable_backprop: bool = True


@contextlib.contextmanager
def using_config(name: str, value: object) -> Generator[None, None, None]:
    """★ step18 — Config 속성을 일시적으로 변경하는 컨텍스트 매니저.

    ★ 컨텍스트 매니저 핵심 마법 (탐구 노트 23번에서 깊이):
      @contextlib.contextmanager + yield 가 "with 블록 진입/탈출"을 구현.
      yield에서 일시정지 → with 블록 실행 → 블록 끝나면(또는 예외) finally에서 복구.

    ★ 반환 타입 Generator[None, None, None]:
      yield로 값을 안 내보내니 Generator의 첫 타입 인자는 None.
      send()로 안 받으니 두 번째도 None. 반환값(return)도 None.
      ★ 핵심: Generator 타입 힌트를 줘야 @contextmanager가 정상 인식 (-> None은 틀림).

    ★ 왜 컨텍스트 매니저인가 (수동 Config 변경보다 나은 점):
      수동: Config.enable_backprop = False; ...; Config.enable_backprop = True (까먹으면 큰일)
      with: with using_config('enable_backprop', False): ... (자동 복구, 예외에도 안전)
    """
    old_value = getattr(Config, name)
    setattr(Config, name, value)

    try:
        yield                        # ★ with 블록 본문 실행 (여기서 일시정지)
    finally:
        setattr(Config, name, old_value)   # ★ 블록 끝나면(예외 포함) 무조건 원래값 복구


def no_grad() -> contextlib._GeneratorContextManager[None]:
    """★ step18 — 역전파 끄기 사용자 인터페이스 (using_config의 특수 케이스).

    사용: with no_grad(): ...

    ★ cf. PyTorch torch.no_grad() 와 정확히 같은 패턴/이름.
    DeZero가 PyTorch 생태계 용어를 충실히 따름.
    """
    return using_config('enable_backprop', False)


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환 (삼항 1줄화, 항목 2)."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
    """

    def __init__(self, data: Optional[np.ndarray]):
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021 (cleargrad → clear_grad)."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. ★ step18: Config.enable_backprop으로 그래프 구축 조건부.

    ★ 박스 컨텍스트 3계층 (항목 011):
      __call__/forward/apply → 순전파 / fill_grad/backward/derivative → 역전파
    ★ derivative hook "선택적" (항목 010~013):
      단일/다변 스칼라 함수는 derivative로 도함수 제공, backward 직접은 탈출구.

    ★ 네이밍 (REZERO_CHANGES 항목 019 + 026):
      output 속성은 단수 정책(항목 019) 유지, step17부터 weakref로 잡음(항목 026).
    """

    def __init__(self) -> None:
        self.inputs: Optional[tuple[Variable, ...]] = None
        self.output: Optional[weakref.ref] = None
        self.generation: int = 0

    def __call__(self, *inputs: Variable) -> Variable:
        # --- 회수 + 가드를 한 루프로 (step11 패턴 유지) ---
        xs = []
        for x in inputs:
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 연산에 사용할 수 없습니다.")
            xs.append(x.data)

        # --- 순전파: forward → 다시 Variable로 래핑 --------------------------------
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)                                    # 단일값도 튜플로 정규화

        assert len(ys) == 1, f"step13~18은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- ★ step18 핵심 — Config.enable_backprop일 때만 그래프 구축 ----------------
        # 역전파 안 할 때(no_grad 블록 안)는 creator/inputs/output을 세팅하지 않음.
        # → 순전파 값(y.data)만 필요한 추론 시 메모리 대폭 절약.
        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            output.set_creator(self)
            self.inputs = inputs
            self.output = weakref.ref(output)            # 단수 + weakref (항목 019 + 026)

        return output

    # ===== 순전파 계열 (step11~17과 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13~17과 동일 — 스칼라 출력 가정) =====
    def backward(self, upstream_grad: np.ndarray) -> tuple[np.ndarray, ...]:
        """역전파 뼈대 (derivative hook 호출).

        ★ rezero 변형 유지 (항목 007) — 매개변수명 `gy` → `upstream_grad`.
        ★ 스칼라 출력 가정 — 단일 upstream을 각 입력의 편도함수에 곱함.
        """
        assert self.inputs is not None, "self.inputs must be set (__call__ should have run)"

        partials = self.derivative()
        if not isinstance(partials, tuple):
            partials = (partials,)

        downstream_grads = []
        for x, df in zip(self.inputs, partials):
            if x.data is None:
                raise RuntimeError(f"{x!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")

            local_deriv = df(x.data)
            downstream_grads.append(local_deriv * upstream_grad)

        return tuple(downstream_grads)

    def derivative(self) -> Callable[[np.ndarray], np.ndarray] | tuple[Callable, ...]:
        """도함수 hook. 단일 OR 튜플 자유 (부모에서 정규화).

        ★ 스칼라 출력 전용 (브로 통찰): df(x) * upstream_grad 공식은 출력이 스칼라일 때만 성립.
        """
        raise NotImplementedError(
            "도함수(derivative)를 구현하거나, backward()를 직접 오버라이드하세요."
        )


# ===== 구체 함수들 (step13~17과 동일) =====
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
        # ★ type: ignore[override] — 부모 apply(*xs)와 시그니처 불일치 (자식은 명시적 인자).
        #   의도적: 부모는 다형성(polymorphism) 위해 *xs, 자식은 가독성 위해 명시적 이름(x, x0, x1).
        #   책 원본도 이 패턴 — 학습용 프레임워크라 인간 가독성 우선 (브로 통찰, 2026-07-31).
        #   ★ 이 패턴은 step23 패키지화 시 core.py에서도 유지 — 그때 재평가.
        return x ** 2

    @override
    def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
        return lambda x: 2 * x


class Add(Function):
    """덧셈 함수: (x0, x1) → x0 + x1. ★ 다입력 함수.

    미분: ∂y/∂x0 = 1, ∂y/∂x1 = 1 (각 편도함수 = 상수함수, 브로 통찰).
    """

    @override
    def apply(self, x0: np.ndarray, x1: np.ndarray) -> np.ndarray:  # type: ignore[override]
        # ★ type: ignore[override] — 부모 apply(*xs)와 시그니처 불일치 (위 Square.apply 주석 참조).
        return x0 + x1

    @override
    def derivative(self) -> tuple[Callable, ...]:
        return (lambda _: 1, lambda _: 1)


# ===== wrapper 함수 (step12 스타일) =====
def add(x0: Variable, x1: Variable) -> Variable:
    """덧셈 wrapper."""
    result = Add()(x0, x1)
    assert isinstance(result, Variable), "Add는 단일 출력이므로 Variable이어야 함"
    return result


def square(x: Variable) -> Variable:
    """제곱 wrapper."""
    result = Square()(x)
    assert isinstance(result, Variable), "Square는 단일 출력이므로 Variable이어야 함"
    return result


# ★★★ step18 핵심 — fill_grad에 retain_grad 매개변수 추가 (항목 014 확장) ------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step18: retain_grad 매개변수 추가.

    step17과의 차이:
      - retain_grad=False (기본): 역전파 후 중간 Variable grad를 None으로 버림 → 메모리 절약.
      - retain_grad=True: 모든 Variable이 grad 유지 (디버깅 등特殊情况).

    ★ rezero 변형 (항목 014 유지): 책은 Variable.backward(retain_grad) 메서드.
      우리는 fill_grad(start_var, retain_grad) 전역 함수. 정체성 유지하며 자연스럽게 확장.

    ★ retain_grad의 의미:
      보통 역전파는 최종 입력(x0.grad 등)만 필요. 중간 Variable(t.grad 등)의 grad은 안 씀.
      그래서 기본으로 중간 grad을 버림 → 큰 ndarray 중간 grad이 메모리 잡아먹는 것 방지.
      retain_grad=True는 "모든 Variable grad 다 볼래" (주로 디버깅).

    ★ 키워드 전용 인자(*,)로 retain_grad 지정:
      fill_grad(y)                    # 기본 (retain_grad=False)
      fill_grad(y, retain_grad=True)  # 중간 grad 유지
      fill_grad(y, np.array(2.0), retain_grad=True)  # 시작 grad + retain
      → retain_grad를 키워드로만 받게 해 실수 방지 (위치 인자 헷갈림 방지).
    """
    # --- 도입부 guard (검증 A: 사용자 오용 — 항목 016 fail-fast 원칙) -------------
    if start_var.creator is None:
        raise RuntimeError(
            f"{start_var!r}에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다. "
            "입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요."
        )

    # --- 시작점 grad 초기화 (3단계 우선순위 — 항목 014) -------------------------
    if upstream_grad is not None:
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        if start_var.data is None:
            raise RuntimeError(f"{start_var!r}의 data가 None입니다 — 역전파에 사용할 수 없습니다.")
        start_var.grad = np.ones_like(start_var.data)

    # --- 메인 루프 상태 (worklist + visited + schedule 클로저 — step16과 동일) -----
    worklist: Worklist = []
    visited: set[Function] = set()

    def schedule(f: Function) -> None:
        """미방문 Function을 worklist에 예약 (generation 내림차순 정렬 유지)."""
        if f not in visited:
            worklist.append(f)
            visited.add(f)
            worklist.sort(key=lambda func: func.generation)

    schedule(start_var.creator)

    # --- 메인 루프: 계산 그래프 역방향 순회 (worklist algorithm + 위상 정렬) ------
    while worklist:
        f = worklist.pop()

        assert f.inputs is not None, "f.inputs must be set"
        assert f.output is not None, "f.output must be set"

        # --- weakref 역참조로 output Variable 획득 (step17) ----------------------
        output = f.output()
        if output is None:
            raise RuntimeError(
                f"{f!r}의 output Variable이 이미 회수되었습니다 — 역전파에 사용할 수 없습니다. "
                "역전파 대상 Variable을 사용자가 참조하고 있는지 확인하세요."
            )

        # --- output.grad 방어막 (항목 007 변수명 유지 + pylance 타입 좁히기) --------
        upstream_grad = output.grad
        assert upstream_grad is not None, "output.grad must be filled"

        # --- 역전파 호출 + 정규화 (step13~17과 동일) --------------------------------
        downstream_grads = f.backward(upstream_grad)
        if not isinstance(downstream_grads, tuple):
            downstream_grads = (downstream_grads,)

        # --- 다변 배분: 입력과 grad 짝지어 할당 (★ A.7.6 동시 언패킹) -------------
        # ★ step14 누적 (유지) — 같은 Variable이 여러 입력으로 와도 grad 합산
        for x, downstream_grad in zip(f.inputs, downstream_grads):
            if x.grad is None:
                x.grad = downstream_grad
            else:
                x.grad = x.grad + downstream_grad

            if x.creator is not None:
                schedule(x.creator)

        # --- ★ step18 핵심 — retain_grad=False면 중간 output grad 버리기 ----------
        # output(이번 Function의 출력 Variable)의 grad은 역전파 완료 후엔 더 안 씀.
        # (이미 upstream으로 전달됐으니까). retain_grad=False면 None으로 해제 → 메모리 절약.
        #
        # ★ 왜 output.grad를 버리나?
        #   중간 Variable들의 grad은 보통 필요 없음 (최종 입력 x0.grad 등만 사용).
        #   중간 grad이 큰 ndarray면 메모리 잡아먹음 → 버려서 절약.
        #   retain_grad=True면 디버깅 등으로 중간 grad 볼 때 사용.
        if not retain_grad:
            output.grad = None


# --- 데모: step18 Config/no_grad/retain_grad 효과 검증 (정답지 step18.py와 동일 시나리오) -
if __name__ == "__main__":
    print("=== step18 메모리 절약 모드 데모 ===")
    print()

    # --- 케이스 1: retain_grad=False (기본) — 중간 grad 버리기 ---
    # 그래프: x0, x1 → add → t → add → y
    #         (x0가 두 번 쓰임: x0 + (x0+x1))
    # retain_grad=False (기본): y.grad, t.grad는 None (중간이라 버려짐).
    #                           x0.grad, x1.grad는 최종 입력이라 유지.
    print("[1] fill_grad(y) 기본 (retain_grad=False) — 중간 grad 버리기")
    x0 = Variable(np.array(1.0))
    x1 = Variable(np.array(1.0))
    t = add(x0, x1)
    y = add(x0, t)
    fill_grad(y)
    print(f"    y.grad = {y.grad}  (기대: None — 최종 출력도 retain_grad=False면 버려짐)")
    print(f"    t.grad = {t.grad}  (기대: None — 중간이라 버려짐)")
    print(f"    x0.grad = {x0.grad}  (기대: 2.0 — x0가 두 경로에 쓰여 1+1=2)")
    print(f"    x1.grad = {x1.grad}  (기대: 1.0 — x1은 한 경로만)")
    print()

    # --- 케이스 2: retain_grad=True — 중간 grad 유지 ---
    print("[2] fill_grad(y, retain_grad=True) — 중간 grad 유지 (디버깅용)")
    x0 = Variable(np.array(1.0))
    x1 = Variable(np.array(1.0))
    t = add(x0, x1)
    y = add(x0, t)
    fill_grad(y, retain_grad=True)
    print(f"    y.grad = {y.grad}  (기대: 1.0 — 유지됨)")
    print(f"    t.grad = {t.grad}  (기대: 1.0 — 유지됨)")
    print(f"    x0.grad = {x0.grad}  (기대: 2.0)")
    print(f"    x1.grad = {x1.grad}  (기대: 1.0)")
    print()

    # --- 케이스 3: no_grad — 역전파 그래프 구축 생략 ---
    print("[3] with no_grad(): — 역전파 끄기 (추론 전용, 메모리 절약)")
    print("    (그래프 구축 안 함: creator/inputs/output이 세팅 안 됨)")
    with no_grad():
        x = Variable(np.array(2.0))
        y = square(x)
    print(f"    y.data = {y.data}  (기대: 4.0 — 순전파 값은 나옴)")
    print(f"    y.creator = {y.creator}  (기대: None — no_grad라 그래프 안 만듦)")
    print(f"    Config.enable_backprop (블록 밖) = {Config.enable_backprop}  (기대: True — 자동 복구)")
    print()

    # --- 케이스 4: using_config 일반형 (no_grad는 특수 케이스) ---
    print("[4] with using_config('enable_backprop', False): — 일반형 (no_grad와 동일)")
    with using_config('enable_backprop', False):
        x = Variable(np.array(3.0))
        y = square(x)
    print(f"    y.data = {y.data}  (기대: 9.0)")
    print(f"    y.creator = {y.creator}  (기대: None)")
    print(f"    Config.enable_backprop = {Config.enable_backprop}  (기대: True)")
    print()

    print("=== step18 완료 — Config/no_grad로 추론 시 메모리 절약, retain_grad로 중간 grad 관리 ===")
