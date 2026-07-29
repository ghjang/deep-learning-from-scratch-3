# rezero 개선 회계 (Changelog of Improvements)

> 책 원본(`dezero/`, `steps/`) 대비 **rezero에서 적용/고려하는 개선사항**을 추적하는 통.
>
> - **목적**: 학습하면서 떠오르는 "더 안전한 최신 파이썬 피처", "더 읽기 좋은 네이밍" 등의
>   개선 아이디어가 흩어지지 않게 한곳에 모으는 것.
> - **사용법**: 생각나는 대로 `### #NNN` 항목으로 **append**. 번호/위치/상태/한 줄 설명만으로 충분.
> - **★ 회수 분류**: step23(패키지화)에서 돌볼 때 **어디로 가나**가 항목마다 다름:
>
>   | 종류 | 예 | 회수처 |
>   |---|---|---|
>   | 🔵 **라이브러리성** | Variable/Function/Square/Exp 등 프레임워크 핵심 변경 | `rezero/core.py`, `functions.py`로 **승격** |
>   | 🟢 **step 한정** | 특정 step 검증/데모 코드의 네이밍, name shadowing 등 | **그 step에 머무름**, 안 옮김 (예: step04 `f` 재사용 수정) |
>   | 🟡 **유틸성** | `numerical_diff` 같은 독립 함수 | `utils.py` 후보 (책도 그렇게 함) |
>
> - **회수 시점**: 주로 **step23 (패키지화)**. 단, 당장 해당 step에서 적용 가능하면 그때그때 반영해도 OK.
> - **이슈와의 관계**: 이 파일은 **"생각 통"**. 아이디어가 구체화되어 작업 단위가 되면
>   그때 GitHub Issue로 분할. 즉 이슈 = 구체화된 것, 이 파일 = 막연한 것까지 포함.

---

## 📋 상태 범례

| 표시 | 의미 |
|---|---|
| 💡 | 아이디어만 (아직 미결정) |
| 🔄 | 고려 중 / 논의 중 |
| ✅ | 반영 완료 |
| ⏭ | 건너뜀 (포기, 또는 책과 크게 달라져 안 함) |

---

## 🗂 분류 (항목이 쌓이면 패턴 보고 채움)

> 지금은 분류 안 함. 어느 정도 쌓이면 주제별로 그룹화(예: 타입 힌트 / 네이밍 / 추상화 강제력 / ...).

---

## 📝 항목

### #001 — Variable.data + 전체 시그니처 타입 힌트 `np.ndarray` (세트 도입)
- **위치**: step01~ (★ **step07에서 세트로 반영 완료**)
- **상태**: ✅ 반영 (2026-07-29, step07에서 회수)
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본은 타입 힌트 없음. 우리는 Variable/Function 전체 시그니처에 `np.ndarray` 힌트 도입.
- **★ 확정 정보**: 책 step37 부터 Variable의 data는 **ndarray로 고정**이 확인됨.
  책 원본(`dezero/core.py:46-48`)은 **런타임 `isinstance` 체크**로 보장. 우리는 **정적 타입 힌트**로 보장.
- **★ 반영 범위 (세트)**:
  | 시그니처 | 힌트 |
  |---|---|
  | `Variable.__init__(data: np.ndarray)` | `self.data: np.ndarray` |
  | `Variable.grad: Optional[np.ndarray]` | (step06에서 이미) |
  | `Variable.creator: Optional["Function"]` | string annotation (전방 참조) |
  | `Variable.set_creator(func: "Function") -> None` | |
  | `Variable.backward() -> None` | |
  | `Function.__call__(input_var: Variable) -> Variable` | |
  | `Function.forward(x: np.ndarray) -> np.ndarray` | |
  | `Function.apply(x: np.ndarray) -> np.ndarray` | hook |
  | `Function.backward(upstream_grad: np.ndarray) -> np.ndarray` | |
  | `Function.derivative() -> Callable[[np.ndarray], np.ndarray]` | hook (#013) |
  | Square/Exp.apply/derivative | @override로 부모 시그니처 상속 + 명시 |
- **★ 회수 과정 (이전 실패 → 성공)**:
  1. step06에서 `data: np.ndarray`만 넣었다 **취소** — `forward` 반환 타입 미정의로 Pyright 오류
  2. step07에서 derivative의 `Callable` 힌트 넣으면서 Function 전체 시그니처를 **세트로** 도입
  3. ★ **교훈 증명**: 세트로 넣으니 통과! 부분 도입은 정적 분석 정합성 깸 (#001 원래 교훈)
- **★ 부수 발견 (Pyright가 잡아준 실제 버그)**:
  세트 도입 중 `Variable.backward()`에서 `f.backward(self.grad)` 호출이
  `self.grad: Optional` → None 가능한데 `Function.backward(upstream: np.ndarray)`는 None 안 받음.
  → `Variable.backward()` 시작에 `if self.grad is None: raise RuntimeError` 가드 추가.
  (이건 책 step09 "자동 초기화(np.ones_like)"의 복선이기도 함)
- **★ 추가 보강 (속성 + 불변조건)**:
  - `Function.__init__` 추가 — `self.input: Optional[Variable]`, `self.output: Optional[Variable]` 선언.
    원래 `__call__`에서 처음 할당돼 pyright 추론이 어려웠는데, `__init__`에서 미리 선언으로 해결.
  - **assert 가드 추가** (불변조건 명시):
    - `Variable.backward`: `assert x is not None` (f.input은 __call__ 후 반드시 존재)
    - `Function.backward`: `assert self.input is not None` (backward는 __call__ 후에만 의미)
  - 이 assert들은 단순 타입 좁히기(type narrowing)용이 아니라 **실제 런타임 불변조건 검증** —
    잘못된 사용 순서(__call__ 없이 backward)를 명확한 에러로 방어.
- **검증**: `pyright rezero/steps/step07.py` → `0 errors, 0 warnings` ✅
- **회수**: step23 → `rezero/core.py` Variable/Function 승격 시 유지

### #002 — `input` 매개변수명 → `input_var` (빌트인 섀도잉 회피)
- **위치**: step02~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `Function.__call__(self, input)`에서 `input`은 Python 빌트인(콘솔 입력)을 섀도잉.
  `input_var`로 변경 — "입력 변수" 역할 명확 + 빌트인 충돌 회피.
- **결정 기록**: LEARNING_NOTES.md step02 "결정 기록: __call__ 매개변수 이름" 참고.
- **회수**: step23 → `rezero/core.py` Function.__call__ 승격 시 (이름 최종 결정: `input_var` 유지? `downstream`?)

### #003 — `raise NotImplementedError` → `abc.ABC` + `@abstractmethod`
- **위치**: step03~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본은 `raise NotImplementedError()`로 "자식이 안 구현하면 런타임 에러".
  `abc.ABC` + `@abstractmethod`로 변경 → **인스턴스 생성 시점**에 강제 (더 빠른 실패).
- **상세**: notes/exploration_09_abc_abstract.md (abc vs NotImplementedError 심화 비교)
- **회수**: step23 → `rezero/core.py` Function 승격 시 유지

### #004 — `@override` 데코레이터로 자식 재정의 명시 (Python 3.12+)
- **위치**: step03~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 자식의 `forward`/`backward`에 `@override` 부착 → 부모 메서드 재정의임을 명시.
  정적 분석 도구(mypy/pyright)가 "부모에 없는 메서드를 @override 했는지" 검증 가능.
  단, **런타임 강제력은 없음** (정적 분석 도구 필요).
- **주의**: `@override` 효과를 보려면 mypy/pyright 설정 필요. 현재 rezero엔 설정 없음 —
  step23 패키지화 시점에 `pyproject.toml`에 정적 분석 도구 설정 추가 검토.
- **상세**: notes/exploration_09_abc_abstract.md §9
- **회수**: step23 → `rezero/core.py` Function + `functions.py` 자식들 승격 시

### #005 — name shadowing 제거 (step04 `f` 변수 재사용)
- **위치**: step04
- **상태**: ✅ 반영
- **종류**: 🟢 step 한정 ★ (라이브러리성 아님)
- **내용**: 책 원본 step04.py에서 `f = Square()` 후 `def f(x):`로 같은 이름 재사용 → IDE 워닝.
  `sq`, `composite_f`로 이름 분리. name shadowing은 실행 순서 의존적이라 순서 바뀌면 깨짐.
- **파생 탐구**: notes/exploration_12_language_binding.md (언어 바인딩/타이핑까지 확장)
- **회수**: ❌ **옮기지 않음** — step04 검증 스크립트 한정 변경이라 step23 패키지화와 무관.
  step04 파일에 머무름. (이런 "step 한정" 변경이 브로가 짚은 핵심 케이스)

### #006 — `numerical_diff` docstring + 블랙박스 관점 주석
- **위치**: step04
- **상태**: ✅ 반영
- **종류**: 🟡 유틸성
- **내용**: 책 원본은 주석 거의 없음. docstring으로 공식/eps 트레이드오프/블랙박스 관점 명시.
  "f의 내부를 몰라도 f(x+h)/f(x-h) 호출로 미분 가능 → autograd 철학" 서술.
- **회수**: step23 → `rezero/utils.py` 승격 후보 (책도 dezero/utils.py에 넣음)

### #007 — 역전파 변수명 `gy`/`gx` → `upstream_grad`/`downstream_grad` + `local_deriv` 분리
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `gx = 2 * x * gy` 한 줄을 두 단계로 분해:
  ```python
  local_deriv = 2 * x                          # ① 자기 도함수 (df/dx) 평가
  downstream_grad = local_deriv * upstream_grad # ② fold step (곱해서 누적)
  ```
  → step05 통찰("역전파 = right fold", "국소적 미분 = df/dx")이 **코드 구조로 드러남**.
- **상세**: notes/exploration_13_derivative_notation.md §8 (gy/gx 헷갈림 분석 + fold 통찰)
- **회수**: step23 → `rezero/core.py` Function.backward 승격 시

### #008 — `Variable.grad` 타입 힌트 `Optional[np.ndarray]`
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `self.grad = None`은 정적 분석(VSCode Pylance)에서
  `y.grad = np.array(1.0)` 시 "None에 ndarray 대입" 경고.
  `self.grad: Optional[np.ndarray] = None`로 타입 힌트 → 경고 제거 + **라이프사이클 명시**
  (역전파 전 None → 역전파 후 ndarray). PyTorch의 `grad: Optional[Tensor]`와 같은 패턴.
- **검증**: `mypy rezero/steps/step06.py` → `Success: no issues found` ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시

### #009 — `Function.backward` docstring에 fold 흐름 명시
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: `backward(upstream_grad)`의 의미를 docstring으로 풀어 서술.
  - `upstream_grad`: 상류에서 접어 내려온 누적 미분값 (최종 출력에서부터의 fold)
  - 반환값: 자기 도함수 곱해 한 번 더 접은 새 누적값 (하류로 전달)
  cf. PyTorch `grad_output`/`grad_input`, 학술 용어 upstream/downstream gradient.
- **회수**: step23 → `rezero/core.py` Function.backward 승격 시

### #010 — ★★ backward에 Template Method 재적용 + `derivative` hook (브로 제안)
- **위치**: step07
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★ (구조적 변형, REZERO_CHANGES 최대 성과 후보)
- **내용**: 책 원본은 `backward`를 `@abstractmethod`로 두고 자식이 **전체 backward 5줄**을 구현.
  → Square/Exp의 backward 5줄 중 **4줄이 완전 중복** (fold step `local_deriv * upstream_grad`).
  자식마다 달라지는 건 `local_deriv` 1줄뿐.

  ★ 브로 제안 구조 (Template Method with Hook 패턴):
  ```python
  class Function(ABC):
      def backward(self, upstream_grad):
          # 기본 구현 (공통 fold step)
          x = self.input.data
          local_deriv = self.derivative(x)     # 자식이 채우는 hook
          return local_deriv * upstream_grad

      def derivative(self, x):
          # ★ NotImplementedError — @abstractmethod가 아님 (선택적 hook)
          raise NotImplementedError("도함수 구현하거나 backward 직접 오버라이드")

  class Square(Function):
      @override
      def derivative(self, x): return 2 * x      # ★ 도함수 1줄만!
  ```
- **★ 핵심 설계 결정들** (브로 통찰):
  1. **Template Method 대칭 완성** — step02에서 forward에 Template 적용했던 걸 backward에도.
     `__call__`이 forward 호출하듯, backward가 derivative 호출. 프레임워크 설계의 대칭성.
  2. **`derivative`를 `@abstractmethod`가 아닌 `NotImplementedError`로** — 브로 제안의 핵심.
     이유: 도함수로 표현 안 되는 연산(전치/브로드캐스팅/다입력, step34+ 행렬 미분)은
     backward 자체를 직접 오버라이드하는 게 자연스러움.
     → **"derivative OR backward override" 두 가지 구현 경로 인정** = 선택적 hook.
     `@abstractmethod`였으면 무조건 derivative 구현 강제라 확장성 떨어짐.
  3. **맞춤 에러 메시지** — "도함수 구현하거나 backward 직접 오버라이드하세요"
     (`@abstractmethod`의 "abstract method"보다 훨씬 친절)
- **이점**: DRY (fold step 중복 제거) + step02 패턴과 대칭 + 자식 구현량 5줄→1줄
- **주의**: 책과 구조가 다름. step09 "Function 기반 클래스화"에서 책이 비슷한 리팩토링을
  다룰 수 있음 — 그때 책 방식과 비교하며 학습. 현재 변형은 우리 설계 철학(대칭성 + 확장성) 반영.
- **⚠️ 최종 반영 여부 보류 (2026-07-29)**: 이 패턴은 **step01~12 스칼라 연산 단계에서 최적**이지만,
  step13+ (가변 길이 인수) / step14 (누적 gradient) / step34+ (행렬 미분·전치·야코비안) 에서는
  `derivative` 1줄로 표현이 안 되어 `backward` 직접 오버라이드로 전환될 것.
  실제 PyTorch도 `backward`를 통째로 정의 (`derivative` hook 없음).
  → **이 패턴을 최종 rezero(core.py)에 반영할지는 step 진행하며 step13/step34 진입 시점에서
  재평가.** 현재(step07)는 실험적으로 도입해두고, 복잡도가 올라가면 검증하는 전략. (브로 & AI 합의)
- **데코레이터 정리**:
  | 메서드 | 데코레이터 | 이유 |
  |---|---|---|
  | `Function.forward` | `@abstractmethod` | 자식 무조건 구현 |
  | `Function.backward` | (없음, 기본 구현) | 부모가 fold step 뼈대 제공 |
  | `Function.derivative` | (없음, NotImplementedError) | 선택적 hook |
  | `Square/Exp.forward` | `@override` | 부모 forward 재정의 |
  | `Square/Exp.derivative` | `@override` | 부모 derivative 재정의 |
  | Square/Exp의 backward | (구현 안 함) | 부모 기본 구현 상속 |
- **검증**: `pyright rezero/steps/step07.py` → `0 errors, 0 warnings` ✅
- **회수**: step23 → `rezero/core.py` Function + `functions.py` 자식들 승격 시 (★ 핵심 구조라 반드시 유지)

### #011 — ★★ forward에도 동일 hook 패턴 + `apply` hook (브로 제안 — 대칭 완성)
- **위치**: step07
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★ (#010과 한 쌍, 대칭 완성)
- **내용**: 책 원본은 `forward`를 `@abstractmethod`로 두고 자식이 forward 전체를 구현.
  → 브로 불편감: "`forward`는 '어딩가로 포워딩(전달)' 뉘앙스인데, 실제론 **함수 본문 실행**잖아.
  derivative에서 한 것과 똑같이 forward도 hook 패턴으로 가자."

  ★ 브로 제안 구조 (derivative와 대칭):
  ```python
  class Function(ABC):
      def forward(self, x):
          return self.apply(x)                  # 기본 구현 → hook 호출

      def apply(self, x):
          raise NotImplementedError("apply 구현하거나 forward 직접 오버라이드")

  class Square(Function):
      @override
      def apply(self, x): return x ** 2         # ★ 함수 본문 1줄만!
  ```
- **★ 네이밍 `apply` 선택 이유** (브로 직관 + 분석):
  - 수학의 $f(x)$ "함수 적용"과 정확히 일치
  - Python 2 내장함수 `apply(func, args)`와 같은 의미 (Python 3에선 빌트인 제거라 충돌 없음)
  - `__call__` 매직메서드와 혼동 없음 (`call` 후보의 단점 회피)
  - `forward`의 "포워딩" 어색함 제거 — 실제 역할(함수 본문 실행)과 이름 일치
- **★ 대칭 완성 (이게 진짜 핵심)**:
  | | 기본 구현 | hook 메서드 | 의미 |
  |---|---|---|---|
  | 순전파 | `forward(x)` | `apply(x)` | 함수 본문 |
  | 역전파 | `backward(gy)` | `derivative(x)` | 도함수 |
  완벽한 대칭 — 둘 다 "기본 구현 + 선택적 hook + 직접 오버라이드 탈출구".
- **ABC 강제 방식**: `@abstractmethod` 없음 (apply/derivative 모두 선택적 hook).
  → 기술적으로 `Function()` 인스턴스화 가능하지만, apply/derivative 미구현 시
  forward/backward 호출 순간 NotImplementedError. "추상 강제는 호출 시점" 전략 (브로 합의, B안).
- **이점**: 자식 구현량 forward/backward 각 5줄 → **apply/derivative 각 1줄**. DRY + 대칭 + 가독성.
- **주의 / 최종 반영 보류**: #010과 동일 — step13/step34 진입 시점에서 재평가.
  복잡한 연산은 apply/derivative 1줄로 안 되어 forward/backward 직접 오버라이드로 전환.
- **데코레이터 정리** (최종):
  | 메서드 | 데코레이터 | 이유 |
  |---|---|---|
  | `Function.forward` | (없음, 기본 구현) | 부모가 apply hook 호출 뼈대 제공 |
  | `Function.backward` | (없음, 기본 구현) | 부모가 derivative hook 호출 뼈대 제공 |
  | `Function.apply` | (없음, NotImplementedError) | 선택적 hook (순전파) |
  | `Function.derivative` | (없음, NotImplementedError) | 선택적 hook (역전파) |
  | `Square/Exp.apply` | `@override` | 부모 apply 재정의 |
  | `Square/Exp.derivative` | `@override` | 부모 derivative 재정의 |
- **검증**: `pyright rezero/steps/step07.py` → `0 errors, 0 warnings` ✅
- **회수**: step23 → `rezero/core.py` Function + `functions.py` 자식들 승격 시 (#010과 쌍으로 유지)

### #012 — `set_creator` 메서드 유지 결정 (브로 검증 — generation 복선 발견)
- **위치**: step07
- **상태**: ✅ 메서드 유지 결정 (2026-07-29, 변형 아님 — 책 충실)
- **종류**: 🟢 step 한정 결정 (라이브러리성 변형 아님 — 책 방식 존중)
- **브로 의심 흐름** (이 결정의 가치):
  1. "set_creator는 단순 속성 할당인데 왜 메서드?" (의심)
  2. "최종 DeZero 코드에서 추가 로직 있나?" (검증 질문 ★)
  3. 답: **있다** — `dezero/core.py:81-83`의 set_creator는 2줄:
     ```python
     def set_creator(self, func):
         self.creator = func
         self.generation = func.generation + 1   # ★ step16 복선!
     ```
- **★ 발견: step16 "복잡한 계산 그래프(generation)" 복선** — set_creator가 `generation` 설정까지 담당.
  step07 시점에선 한 줄이지만, step16 진입 시 자동으로 generation 로직이 자연스럽게 추가되는 구조.
  책이 메서드로 둔 건 "미래 확장 포인트 예약" 의도.
- **결정**: 책 충실(메서드 유지). 이유:
  - step16이 금방 옴 (9스텝 뒤) — 직접 할당 변형하면 step16에서 다시 메서드로 리팩터링해야 (이중 작업)
  - 책의 "미래 확장 포인트" 설계 의도 존중 = 학습에 좋음
  - @property/@setter도 검토했으나 추가 로직 없으면 과잉 → set_creator가 의미 갖는 건 generation 때문
- **docstring 보강**: set_creator docstring에 "generation 설정(step16 복선)" 명시하여 미래 브로/AI가 맥락 파악 가능.
- **★ 교훈 (영구 기록 가치)**: "왜 이렇게 했을까?" 의심 → "최종 코드 확인" 검증 → "아, 미래 확장 때문" 납득.
  이 3단계가 좋은 설계 리뷰의 핵심. 코드를 의심하고 검증으로 답 찾는 브로 스타일의 승리.
- **회수**: ❌ 옮기지 않음 — step07 한정 결정. 책 충실이라 step23 패키지화와 무관.

### #013 — ★★ `derivative`가 callable(도함수 객체) 반환 (브로 통찰 — 노트 13번 §4 코드 구현)
- **위치**: step07
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★ (#010과 짝, 수학적 정확성 추구)
- **내용**: #010에서 도입한 derivative가 원래 "도함수값(숫자)"을 반환했음.
  브로 통찰: "실제 구현 클래스에서 도함수의 apply까지 하는 건 오바.
  derivative가 callable(함수 객체)을 반환하고, backward에서 평가(call)하는 게 맞지 않나?"

  ★ 핵심 — 수학적 의미 분리 (노트 13번 §4 "도함수 = 고차 함수"):
  | 개념 | 수학 | 현재 코드 |
  |---|---|---|
  | 도함수 | $f' = 2x$ (함수/규칙) | `derivative()` → callable 반환 |
  | 도함수값 | $f'(3) = 6$ (평가 결과) | `df(x)` 별도 평가 |

  구조:
  ```python
  class Function(ABC):
      def backward(self, upstream_grad):
          x = self.input.data
          df = self.derivative()              # ① 도함수(함수 객체) 획득
          local_deriv = df(x)                 # ② 현재 입력에서 평가
          return local_deriv * upstream_grad

      def derivative(self) -> Callable[[np.ndarray], np.ndarray]:
          raise NotImplementedError(...)

  class Square(Function):
      @override
      def derivative(self):
          return lambda x: 2 * x              # ★ 도함수 f'=2x를 "함수"로 반환
  ```
- **★ 이점** (수학과의 일치):
  1. **도함수 vs 도함수값 분리** — `f'`(함수)와 `f'(x)`(값)이 코드로 구분됨
  2. **여러 점 평가 가능** — `df = sq.derivative(); df(3); df(5)` 여러 점에서 재사용
  3. **이계도함수 확장 자연스러움** — `df.derivative()` 가능 (f'' = 미분의 미분)
  4. **노트 13번 §4 "고차 함수" 통찰 구현** — 미분 = 함수를 받아 함수 반환 (정확한 타입 시그니처)
- **★ 리턴 타입 힌트 `Callable[[np.ndarray], np.ndarray]`**:
  - "ndarray를 받아 ndarray 반환하는 함수" = 수학의 $f': \mathbb{R} \to \mathbb{R}$ (함수→함수) 대응
  - 노트 13번 §4 통찰이 타입 시그니처로 드러남
  - lambda엔 타입 힌트 못 붙이지만, 메서드 시그니처 힌트로 충분
- **구현 형태**: `lambda x: 2 * x` (간결). 복잡해지면 내부 def로 전환 고려.
- **주의 / 최종 반영 보류**: #010/#011과 동일 — step13/step34 진입 시점에서 재평가.
  행렬 미분(step34+)은 도함수가 단순 callable로 표현 안 될 수 있음 (전치 등) → backward 직접 오버라이드로 전환.
- **검증**: `pyright rezero/steps/step07.py` → `0 errors, 0 warnings` ✅
- **회수**: step23 → `rezero/core.py` Function + `functions.py` 자식들 승격 시 (#010/#011과 함께 유지)

### #014 — ★★★ `backward`를 Variable 메서드 → 전역 함수로 분리 (브로 Q4 통찰 — JAX 스타일)
- **위치**: step07
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★★ (step07 최대 구조 변형, rezero 정체성)
- **브로 통찰** (Q4 — RESEARCH_QUEUE #6 실증):
  > "backward가 Variable 메서드로 붙은 거 불편. 걍 전역 함수로 이터레이션하게 하는 게 나았지 않나?"
  → Variable은 "데이터 상자"인데 "그래프 순회"까지 담당하면 관심사 혼재.
  Variable.backward()를 제거하고 전역 `backward(output)`로 분리.
- **내용**:
  ```python
  # 이전 (책/PyTorch — 메서드 방식)
  y.backward()                    # Variable의 메서드

  # 이후 (rezero — 전역 함수, JAX 스타일)
  backward(y)                     # 전역 함수, y를 시작점으로 받음
  ```
  전역 backward 구조:
  ```python
  def backward(output: Variable) -> None:
      if output.grad is None: raise RuntimeError(...)
      f = output.creator
      if f is not None:
          x = f.input
          assert x is not None
          x.grad = f.backward(output.grad)    # Function.backward (단일 노드) — 그대로
          backward(x)                         # 재귀도 전역 함수로
  ```
- **★ 핵심 가치 — 관심사 분리 (SoC)**:
  | 역할 | 이전 (메서드) | 이후 (전역 함수) |
  |---|---|---|
  | Variable | 데이터 + grad + creator + **순회** | **순수 데이터 상자** (data, grad, creator만) ★ |
  | 그래프 순회 | Variable.backward() | 전역 `backward(output)` ★ |
  | Function.backward (단일 노드) | 그대로 | 그대로 (역할 안 겹침) |
- **★ JAX 패러다임과의 일치**:
  - JAX: `jax.grad(f)(x)` — 그래프 순회가 별도 함수, Variable 자체 없음
  - rezero: `backward(y)` — Define-by-Run은 유지하되, 순회만 별도 함수로 (JAX 철학 일부 수용)
  - cf. PyTorch/DeZero: `y.backward()` — 순회가 Variable에 흡수 (Q3 "DAG 흡수" 문제)
- **★ 시작점 명시성**: `backward(y)`는 "이 변수에서부터 역전파 시작"이 인자로 드러남.
  메서드 방식(`y.backward()`)보다 시작점이 명시적.
- **★ 파라미터 네이밍 `start_var`** (브로 제안):
  - `output`보다 의미 정확 — 역전파의 **시작점**이지 단순 "출력"이 아님
  - `input_var` (Function.__call__)과 같은 `_var` 접미사 관례 — Variable 타입 암시, 코드 베이스 일관성
- **★ `upstream_grad` 기본값 `None` → 자동 `ones_like`** (브로 제안):
  - 사용자가 매번 `y.grad = np.array(1.0)` 안 해도 됨 → `backward(y)` 한 줄이면 충분
  - 책 step09 "자동 초기화(np.ones_like)"의 복선을 우리는 **step07 시점에서 시그니처로 해결**
  - 커스텀 가능: `backward(y, upstream_grad=np.array(2.0))` 식으로 다른 시작값 지정
- **★★ 버그 교훈 (기본값 + 재귀의 위험)**:
  단순히 `upstream_grad=np.ones_like` 기본값을 넣었더니 **재귀마다 grad 덮어쓰기 버그** 발생
  (재귀 호출 backward(x)에서도 또 ones_like로 초기화 → 결과 3.2974 → 1.0 으로 잘못됨).
  해결: **3단계 우선순위** 도입 —
    1. 사용자 명시적 인자 (최상위 호출 커스텀)
    2. 이미 설정된 start_var.grad (재귀 시 — 이전 노드가 Function.backward로 채움)
    3. 둘 다 없으면 ones_like (최초 시작점 자동 초기화)
  ★ **교훈**: 재귀 구조에 기본값 매개변수 쓸 땐 "재귀 호출에서도 기본값 적용되는지" 검증 필수.
  pyright는 잡아주지 못하는 런타임 논리 버그 — 실행 검증이 최종 방어선.
- **★ 패키지화 후 호출**: step23 이후 `from rezero import backward` 또는 `rezero.backward(y)`.
  `jax.grad(f)(x)`와 같은 패턴. (브로가 "rezero.backward처럼 호출하게 되나?" → 정답 맞음)
- **주의 / 최종 반영 보류**:
  - PyTorch/DeZero 표준에서 벗어남 → 나중에 PyTorch 쓸 때 혼란 가능 (학습용 실험으로 명시)
  - 하지만 **관심사 분리**와 **JAX 철학 수용**이라는 구조적 가치가 큼
  - step08(반복문)에서도 전역 함수 구조 유지 가능 (재귀→반복문 전환도 전역 함수 내부에서)
  - RESEARCH_QUEUE #6 (DAG 흡수 vs 분리, 3가지 autograd 패러다임) 회수 시 실증 자료로 활용
- **검증**: `pyright rezero/steps/step07.py` → `0 errors, 0 warnings` ✅
- **회수**: step23 → `rezero/core.py` 또는 `rezero/__init__.py`에 전역 backward 승격 (★★★ rezero 정체성)

---

## 💡 대기 중 아이디어 (구체화 안 됨)

> 생각나는 대로 한 줄씩. 구체화되면 위 항목으로 승격.

- (아직 없음 — 떠오르는 대로 추가)

---

## 🔗 관련 링크

- `AGENTS.md` — rezero 학습 원칙 (dezero 복붙 금지, 변형 실험 환영)
- `LEARNING_NOTES.md` — step별 핵심 통찰 (변형 결정 기록도 여기)
- `notes/exploration_09_abc_abstract.md` — abc vs NotImplementedError 심화 (#003, #004 관련)
- `notes/exploration_13_derivative_notation.md` §8 — gy/gx + fold 통찰 (#007 관련)
- 책 step23 — `dezero/` 패키지화 (회수 시점의 원본 참고)
