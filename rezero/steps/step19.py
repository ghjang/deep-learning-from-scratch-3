"""
rezero.steps.step19 — [2고지] 변수 사용성 개선
===============================================

★ 제목 주의: 여기서 **"변수" = Variable 클래스** (일반 명사 "변수" 아님).
  DeZero의 Variable을 더 파이썬스럽게 다루기 위한 매직메서드/property/이름 추가.

이전 step(step18)까지 Variable은 `data`, `grad`, `creator`, `generation`만 가진
순수 데이터 상자였음. 이번 step부턴 Variable을 **ndarray처럼 자연스럽게** 다루기 위한
표현/인터페이스를 추가. 역전파/그래프 로직은 건드리지 않음.

이 step에서 배울 것:
  - `name` 속성 — Variable에 이름 부여 (그래프 시각화 step09 utils에서 쓰임)
  - `__len__` — `len(x)` → 데이터 길이
  - `__repr__` — `print(x)` → 깔끔한 표현 (들여쓰기 처리 포함)
  - `@property` 4종 — `shape`, `ndim`, `size`, `dtype` (모두 data에 위임)

★★★ 핵심 — 위임(delegate) 패턴:
  Variable의 매직메서드/property는 **내부 ndarray(self.data)에 그대로 떠넘기는** 패턴.
    x.shape      →      self.data.shape
    len(x)       →      len(self.data)
    print(x)     →      'variable(' + str(self.data) + ')'

  ★ 위임 패턴(delegate pattern) = 한 객체가 다른 객체에게 작업을 떠넘기는 구조.
    Variable이 ndarray를 품고, ndarray가 이미 shape/ndim/size/dtype/__len__을 다 알고 있으니
    Variable이 다시 구현할 필요 없이 "data한테 물어봐" 하고 떠넘김.
  ★ 파이썬 매직메서드(__len__, __repr__)와 property가 이 위임을 자연스럽게 구현하는 도구.

★ Variable 정체성 — "순수 데이터 상자" 원칙 (항목 014) 유지되나?
  YES. name/len/repr/property는 모두 **데이터 자체에 대한 정보/표현**이지
  그래프 순회나 역전파 로직이 아님. 오히려 정체성 **강화** —
  "데이터 상자로서 사용성 좋은 데이터 상자"가 됨.

★ 이 코드의 가정/전제 (step18 누적 전제 + step19 새 전제):
  step14~18 누적 전제(Define-by-Run 매번 재생성 / DAG / weakref / Config 전역) + 새 전제:

  | 새 전제 (step19)                                   | 의미                                              | 깨지면?                                       |
  |----------------------------------------------------|---------------------------------------------------|-----------------------------------------------|
  | Variable의 표현/속성은 data ndarray에 **위임**된다  | 매직메서드/property가 data에 그대로 떠넘김         | data is None 시 property 접근 에러 → None 가드 |
  | Variable에 메타데이터(name) 추가해도 정체성 유지    | name은 데이터 본질 아닌 보조 정보                 | 보조 정보라 정체성 흐려지지 않음 — OK          |

★★★ rezero 변형 포인트:
  | # | 포인트                  | 책 방식                | 우리 방향                                       |
  |---|------------------------|------------------------|-------------------------------------------------|
  | A | name 속성              | __init__ 매개변수 추가 | ★ 키워드 전용(`*, name=None`) — 의미 명확성     |
  | B | __len__, __repr__      | 매직메서드 추가        | 동일                                            |
  | C | shape/ndim/size/dtype  | @property              | 동일                                            |
  | D | data is None 가드      | 책은 __repr__만 처리   | ★ 보강 — property/__len__에도 None 가드 (방어막 일관성) |

  A/D가 rezero 정체성 포인트. B/C는 책 방식 그대로.
  ★ A: step18 retain_grad 키워드 전용 패턴과 일관성 — "부가 속성은 키워드로" 원칙 형성 중.
  ★ D: step09 방어막 3겹 원칙 연장 — property 접근도 일관되게 가드.

참고 자료:
  - 원본 구현: steps/step19.py
  - 이전 step: rezero/steps/step18.py (Config/no_grad — 이번에 Variable 인터페이스만 개선)
  - 이슈: #24 (step19 진행 추적)

검증 포인트:
  - Variable(np.array([[1,2,3],[4,5,6]]), name='x') → x.name == 'x'
  - x.shape == (2, 3), x.ndim == 2, x.size == 6, x.dtype == dtype('int64')
  - len(x) == 2
  - print(x) → variable([[1 2 3] [4 5 6]]) (★ repr 들여쓰기 처리)
  - Variable(None): repr → 'variable(None)', property는 RuntimeError 가드 동작 확인

실행:
  uv run python rezero/steps/step19.py
"""

import contextlib
import weakref
from abc import ABC
from collections.abc import Callable, Generator
from typing import Optional, override

import numpy as np


# ★★★ step18 유지 — Config 전역 설정 + no_grad 컨텍스트 매니저 ---------------------
class Config:
    """★ step18 — 전역 설정 (역전파 on/off 플래그). 이번 step19는 그대로 유지."""
    enable_backprop: bool = True


@contextlib.contextmanager
def using_config(name: str, value: object) -> Generator[None, None, None]:
    """★ step18 — Config 속성을 일시적으로 변경하는 컨텍스트 매니저."""
    old_value = getattr(Config, name)
    setattr(Config, name, value)

    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad() -> contextlib._GeneratorContextManager[None]:
    """★ step18 — 역전파 끄기 사용자 인터페이스. PyTorch torch.no_grad()와 동일 패턴."""
    return using_config('enable_backprop', False)


def as_array(x: object) -> np.ndarray:
    """★ step09 헬퍼 — 스칼라(예: np.float64)를 ndarray로 변환."""
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]


# ★ Worklist 타입 별칭 (step08 항목 17번에서 도입, 유지)
type Worklist = list["Function"]


# ★★★ step19 핵심 — Variable 사용성 개선 (name + 매직메서드 + property) --------------
class Variable:
    """DeZero의 변수. 순수 데이터 상자 — data + 미분값(grad) + 그래프 연결(creator + generation).

    ★ step19 추가: name 속성 + __len__/__repr__ 매직메서드 + shape/ndim/size/dtype property.
      모두 내부 ndarray(self.data)에 위임하는 패턴 (Variable을 ndarray처럼 다루게 함).
      역전파는 fill_grad 전역 함수가 담당 (rezero 정체성, 항목 014).
    """

    def __init__(self, data: Optional[np.ndarray], *, name: Optional[str] = None):
        # 방어막 2번: 동적 타입 보장 (isinstance 런타임 체크). 정적 힌트와 짝.
        if data is not None and not isinstance(data, np.ndarray):
            raise TypeError(f"{type(data)}는 지원하지 않습니다. ndarray만 허용.")

        self.data: Optional[np.ndarray] = data
        self.name: Optional[str] = name          # ★ step19 — 변수 이름 (그래프 시각화 등에서 사용)
        self.grad: Optional[np.ndarray] = None
        self.creator: Optional["Function"] = None
        self.generation: int = 0

    # ===== step19: data에 위임하는 property 4종 + __len__ ==================
    # 모두 _ensure_data() 헬퍼로 None 가드 → data의 대응 속성으로 위임.
    # ★ 방어막 일관성 (step09 방어막 3겹 연장): data가 None이면 명확한 에러.

    def _ensure_data(self) -> np.ndarray:
        """data가 None이면 RuntimeError, 아니면 data 반환.

        ★ step19 방어막 — property/__len__이 data에 위임하기 전 None 가드.
        __repr__은 None도 표현해야 하므로 이 헬퍼를 안 쓰고 자체 처리.
        """
        if self.data is None:
            raise RuntimeError(
                f"{self!r}의 data가 None입니다 — data에 접근하는 연산(shape/len/dtype 등)을 수행할 수 없습니다."
            )
        return self.data

    @property
    def shape(self) -> tuple[int, ...]:
        """데이터 형상. ★ 위임: self.data.shape."""
        return self._ensure_data().shape

    @property
    def ndim(self) -> int:
        """차원 수. ★ 위임: self.data.ndim."""
        return self._ensure_data().ndim

    @property
    def size(self) -> int:
        """원소 수. ★ 위임: self.data.size."""
        return self._ensure_data().size

    @property
    def dtype(self) -> np.dtype:
        """데이터 타입. ★ 위임: self.data.dtype."""
        return self._ensure_data().dtype

    def __len__(self) -> int:
        """len(x) → 데이터의 첫 번째 차원 크기. ★ 위임: len(self.data)."""
        return len(self._ensure_data())

    def __repr__(self) -> str:
        """print(x) → 'Variable(...)' 형태 (클래스명 그대로). data=None이면 'Variable(None)'.

        ★ rezero 변형 — 책 원본은 소문자 'variable(' 하드코딩이나, 우리는 클래스명 그대로 'Variable(' 사용.
          클래스명과 repr 출력이 일치하는 게 자연스럽고 혼란이 적음 (브로 결정).

        ★ 들여쓰기 처리(replace): 다중 행 ndarray 출력 시 'Variable(' 들여쓰기에 맞추기.
          예: Variable([[1 2 3]
                        [4 5 6]])   ← 두 번째 줄이 'Variable(' 너비(9칸)만큼 들여쓰기
          ('Variable('도 'variable('과 마찬가지로 9칸이라 숫자 그대로)
        """
        if self.data is None:
            return 'Variable(None)'

        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'Variable(' + p + ')'

    # ===== step07~18: 그래프 연결 (변경 없음) =============================
    def set_creator(self, func: "Function") -> None:
        """이 Variable을 만든 Function을 기록 + generation 상속."""
        self.creator = func
        self.generation = func.generation + 1

    def clear_grad(self) -> None:
        """grad 초기화 (Variable 재사용 시). 항목 021 (cleargrad → clear_grad)."""
        self.grad = None


class Function(ABC):
    """DeZero의 함수. step18 Config.enable_backprop으로 그래프 구축 조건부.

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

        assert len(ys) == 1, f"step13~19은 출력 1개(스칼라) 가정. got {len(ys)} outputs"
        output = Variable(as_array(ys[0]))

        # --- ★ step18 유지 — Config.enable_backprop일 때만 그래프 구축 -------------
        if Config.enable_backprop:
            self.generation = max([x.generation for x in inputs])
            output.set_creator(self)
            self.inputs = inputs
            self.output = weakref.ref(output)            # 단수 + weakref (항목 019 + 026)

        return output

    # ===== 순전파 계열 (step11~18과 동일) =====
    def forward(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순전파 뼈대 (apply hook 호출). 박스 컨텍스트 없는 단계 — ndarray만."""
        return self.apply(*xs)

    def apply(self, *xs: np.ndarray) -> tuple[np.ndarray, ...] | np.ndarray:
        """순수 수학 계산 hook. 자식이 채우거나 forward 직접 오버라이드."""
        raise NotImplementedError(
            "함수 본문(apply)을 구현하거나, forward()를 직접 오버라이드하세요."
        )

    # ===== 역전파 계열 (step13~18과 동일 — 스칼라 출력 가정) =====
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


# ===== 구체 함수들 (step13~18과 동일) =====
class Square(Function):
    """제곱 함수: x → x². 미분: f'(x) = 2x."""

    @override
    def apply(self, x: np.ndarray) -> np.ndarray:  # type: ignore[override]
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


# ★★★ step18 유지 — fill_grad 전역 함수 (retain_grad 매개변수 포함) ----------------
def fill_grad(
    start_var: Variable,
    upstream_grad: Optional[np.ndarray] = None,
    *,
    retain_grad: bool = False,
) -> None:
    """★ 자동 역전파 (반복문 — worklist). step18 retain_grad 매개변수 유지.

    ★ rezero 변형 (항목 014 유지): 책은 Variable.backward(retain_grad) 메서드.
      우리는 fill_grad(start_var, retain_grad) 전역 함수. 정체성 유지.
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
        upstream = output.grad
        assert upstream is not None, "output.grad must be filled"

        # --- 역전파 호출 + 정규화 (step13~18과 동일) --------------------------------
        downstream_grads = f.backward(upstream)
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

        # --- ★ step18 유지 — retain_grad=False면 중간 output grad 버리기 ----------
        if not retain_grad:
            output.grad = None


# --- 데모: step19 Variable 사용성 개선 효과 검증 ----------------------------------
if __name__ == "__main__":
    print("=== step19 변수(Variable) 사용성 개선 데모 ===")
    print()

    # --- 케이스 1: name + property 4종 + __len__ + __repr__ (정상 데이터) ---
    print("[1] name 속성 + property 4종 + __len__ + __repr__ (정상 데이터)")
    x = Variable(np.array([[1, 2, 3], [4, 5, 6]]), name='x')
    print(f"    x.name  = {x.name!r}")
    print(f"    x.shape = {x.shape}")
    print(f"    x.ndim  = {x.ndim}")
    print(f"    x.size  = {x.size}")
    print(f"    x.dtype = {x.dtype}")
    print(f"    len(x)  = {len(x)}")
    print(f"    print(x):")
    print(f"    {x!r}")
    print()

    # --- 케이스 2: name을 키워드 전용으로 (★ rezero 변형 A) ---
    print("[2] name은 키워드 전용 — Variable(data, *, name='x')")
    y = Variable(np.array([1.0, 2.0, 3.0]), name='y')
    print(f"    y.name = {y.name!r}  (키워드로 전달)")
    print()

    # --- 케이스 3: __repr__ 들여쓰기 처리 (다중 행 ndarray) ---
    print("[3] __repr__ 들여쓰기 처리 (다중 행 ndarray)")
    z = Variable(np.array([[1, 2], [3, 4], [5, 6]]))
    print(f"    print(z):")
    print(f"    {z!r}")
    print()

    # --- 케이스 4: 역전파도 여전히 동작 (step18 로직 건드리지 않음) ---
    print("[4] 역전파도 여전히 동작 (step18 로직 건드리지 않음 — name/property만 추가)")
    a = Variable(np.array(2.0))
    b = Variable(np.array(3.0))
    c = add(square(a), square(b))       # c = a² + b² = 4 + 9 = 13
    fill_grad(c)
    print(f"    c.data  = {c.data}  (기대: 13.0)")
    print(f"    a.grad  = {a.grad}  (기대: 4.0 = 2a)")
    print(f"    b.grad  = {b.grad}  (기대: 6.0 = 2b)")
    print()

    # --- 케이스 5: data=None 케이스 — __repr__은 None 표현, property는 가드 동작 ---
    print("[5] data=None: __repr__은 'Variable(None)', property는 RuntimeError 가드")
    n = Variable(None, name='n')
    print(f"    n.name   = {n.name!r}")
    print(f"    repr(n)  = {n!r}  (★ None도 표현)")
    try:
        _ = n.shape
        print(f"    n.shape  = (에러 없음 — 이상함!)")
    except RuntimeError as e:
        print(f"    n.shape  → RuntimeError ★ 방어막 동작")
        print(f"               메시지: {e}")
    print()

    print("=== step19 완료 — Variable이 ndarray처럼 다루기 쉬워짐 (위임 패턴) ===")
