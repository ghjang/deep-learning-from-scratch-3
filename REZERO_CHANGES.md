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

## 🗂 분류 (주제별 색인 — 항목 번호순 물리 배치는 유지, 이 표로 그룹 탐색)

> ★ 2026-07-31 그룹화 — 36개 항목 쌓여 주제별 색인 추가 (step23 완료 후 정리).
> 항목 자체는 append-only 정책 존중 — **번호순 물리 배치는 유지 + 이 표로 그룹 탐색**.
> 한 항목이 여러 그룹에 걸칠 수 있으나 "주된 결" 하나로 분류. 상세는 각 항목 본문 참조.

### 항목 번호 → 그룹 매핑

| 그룹 | 항목 | 개수 | 핵심 |
|---|---|---|---|
| **타입 힌트 / 정적 분석** | #001, #008 | 2 | ndarray 힌트 세트, Optional grad |
| **네이밍 (의미 투명성)** | #002, #007, #015, #017, #019, #021, #022, #023, #025 | 9 | input_var, upstream_grad, fill_grad, worklist, output 단수, clear_grad, visited, schedule, 크로스참조 시도/철회 |
| **구조 / 추상화 (Function 핵심 설계)** | #003, #004, #010, #011, #013, #014, #037 | 7 | ABC, @override, derivative/apply hook 대칭, backward→fill_grad 전역 함수, iter_reverse_topo 순회 제너레이터 |
| **검증 / 방어막** | #016, #029 | 2 | assert vs RuntimeError 구분, property/len None 가드 |
| **메모리 관리** | #026, #027, #033 | 3 | weakref 순환 끊기, Config/no_grad 절약 모드, __array_priority__ 버림 |
| **API 설계 (매개변수/표현/연산자)** | #028, #030, #031, #034, #035 | 5 | name 키워드 전용, Variable( 대문자 repr, 매직메서드 클래스 안 정의, __radd__/wrapper 정리, 3원칙 자동 적용 + Pow DRY + Neg 단순화 |
| **패키지 구조** | #036, #038 | 2 | 버전 폴더(v1/v2/v3) + 순환 참조 해결(지연 import), ★v2 브랜칭 + grad Variable화 + common 모듈 |
| **유틸 / step 한정 / 문서 정비** | #005, #006, #009, #012, #018, #020, #024, #032, #040 | 9 | name shadowing, numerical_diff docstring, backward docstring, set_creator 복선, pipe(FP), 주석 정비, fill_grad 통합, Mul derivative hook 재평가 |

### 회수 분류와의 관계 (step23 패키지화 시)

위 "주제별 그룹"과 헤더(L8)의 "회수 분류"(`🔵 라이브러리성` / `🟢 step 한정` / `🟡 유틸성`)는 **직교**:
- **주제별 그룹**: "무엇에 대한 변경인가" (네이밍? 구조? 메모리?)
- **회수 분류**: "어디로 가나" (core.py? 그 step에? utils.py?)

step23 회수 시: 각 항목마다 "주제별 그룹 + 회수 분류" 둘 다 보고 승격 결정.

### 상태 분포 (2026-08-10 기준)

| 상태 | 항목 수 | 비고 |
|---|---|---|
| ✅ 반영 | 34 | 대부분 (#028~#030 step19, #031~#032 step20, #033~#034 step21, #035 step22, #036 step23 신규 추가, #020 step23 회수 완료) |
| 🔄 보류 | 1 | #018 (pipe, step23 재도입 검토 → step24+로 연기) |
| ⏭ 철회 | 1 | #025 (크로스참조 네이밍 시도/철회, 교훈은 영구 보존) |

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
- **★ 관점 분리 (step11 브로 통찰 보강 — "박스 컨텍스트" 계층)**:
  apply가 **"박스 컨텍스트 없는 순수 계산"** 만 담당한다는 관점이 apply 네이밍의 가장 명확한 근거:
  | 메서드 | 역할 | 박스 컨텍스트 |
  |---|---|---|
  | `__call__` | **값 전달/흐름 관리** (Variable 회수→래핑→creator 연결) | O (Variable 다룸) |
  | `forward` | 순전파 뼈대 (hook 호출 or 직접 계산) | X (ndarray만) |
  | `apply` | **순수 수학 계산** (`x²`, `x0+x1`) | X (순수 ndarray) |
  → 브로 지적: "forward"는 '전달(forwarding)' 뉘앙스인데 **실제 전달은 `__call__`** 이 함.
  forward는 전달 파이프라인 안의 "순수 계산 단계"일 뿐 → "함수 적용"엔 **apply가 정확**.
- **★ 왜 책은 forward를 고집하는가 (생태계 관례 vs 미스리딩)**:
  - **이유**: 딥러닝 생태계 표준 용어 — 신경망 순전파 = **forward pass**, 역전파 = **backward pass**
  - PyTorch도 `forward()`/`backward()` 이命名. DeZero가 이 관례를 그대로 준수
  - 책은 "생태계 관례 준수"를 선택 → 브로가 느끼는 **"전달 뉘앙스 미스리딩"은 관례의 부작용**
  - rezero는 학습용이라 **apply로 더 정확한 이름 실험** (#011).
    단, PyTorch/DeZero 생태계 코드 읽을 땐 forward가 쓰이므로 이중 용어 인식 필요
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
- **★★ step13 검증 결과 (2026-07-30) — "스칼라 출력 전용" 확정**:
  브로 통찰: *"derivative hook은 함수 출력이 스칼라일 때까지만 의미 있는 짓 아닌가?"*
  → ★ 정확함. 실증 검증 완료:
  | 출력 형태 | 역전파 공식 | derivative hook 유효? |
  |---|---|---|
  | **스칼라** (Square, Add 등 step01~33 전 범위) | `df(x) * gy` (스칼라×스칼라) | ✅ 유효 |
  | **벡터/행렬** (step34+ 행렬 미분, step41+ 텐서) | `J^T @ gy` (야코비안 전치 곱) | ❌ 붕괴 — backward 직접 필수 |
  - 핵심: derivative hook의 `df(x) * gy` 공식은 **"출력 y가 스칼라"** 일 때만 성립.
    출력이 벡터/행렬이면 역전파가 야코비안 전치행렬 곱(`J^T @ gy`)이 되어 스칼라 곱 공식이 붕괴.
  - ★ 즉 derivative hook의 유효 범위 = **step01~33 (스칼라 회로)**. step34+부턴 backward 직접 오버라이드가 표준.
- **★ step13 옵션 2-α 선택 (브로 통찰 + 상수함수 아이디어)**:
  브로 아이디어: *"Add의 도함수는 입력 무시하는 '1'이란 상수를 리턴하는 상수함수!"*
  → ★ 수학적으로 정확. Add 편도함수 $\partial y/\partial x_i = 1$ = **FP의 const(1) 상수함수**.
  - 이걸 살리기 위해 **derivative가 "각 입력별 도함수 리스트" 반환** 구조 채택 (옵션 2-α):
    ```python
    class Add(Function):
        def derivative(self):
            return [lambda _: 1, lambda _: 1]   # ★ 각 편도함수 = 상수함수 (브로 통찰)
    class Square(Function):
        def derivative(self):
            return [lambda x: 2 * x]             # 단일도 리스트 (일관성)
    ```
  - 부모 backward가 `zip(inputs, dfs, gys)` 로 다변 처리 (복잡도↑ but 학습 가치↑)
  - ★ Issue #14 "FP 유틸"의 `const` 함수가 **실제 용도 발견** — Add 편도함수 표현.
  - trade-off: 부모 backward 복잡도 증가. 실용적이라면 옵션 2-β(단일 derivative/다변 backward 직접)가 단순.
    학습용 프로젝트이므로 브로 아이디어 살리는 2-α 선택.
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

### #015 — ★★★ 전역 함수명 `backward` → `fill_grad` (브로 작명 통찰 — 의미 투명성)
- **위치**: step08
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★★ (#014의 자연스러운 연장, 작명 정제)
- **브로 통찰**:
  > "전역 backward 함수는 계산 그래프를 순회하면서 각 노드의 변수에 누적국소미분값을 저장해주는 것인데,
  >  함수 이름이 좀 거시기 하지 않냐? `fill_grad` 따위가 좀 더 나은 작명 아닌지?"
  → `backward`는 **방향**(역방향)만 말하고 **결과**(grad 채움)는 암시만 됨.
  실제 하는 일이 이름에 안 드러남. `fill_grad`가 의미 투명.
- **내용**:
  ```python
  # 이전 (step07, 책/PyTorch 관례)
  def backward(start_var): ...        # 방향만 이름에
  backward(y)

  # 이후 (step08, 의미 투명)
  def fill_grad(start_var): ...       # ★ "grad 채우기" = 핵심 동작 명시
  fill_grad(y)
  ```
- **★ 왜 fill_grad인가** (후보 비교):
  | 이름 | 평가 |
  |---|---|
  | `backward` | 방향만. 결과 암시. 책/PyTorch 관례 |
  | `fill_grad` ★ | "grad 채우기" 명시. 역방향은 grad의 유일한 방식이라 암시돼도 OK. JAX `jax.grad`와 정신적 유사 |
  | `fill_grad_backward` | 방향+결과 둘 다 명시하나 verbose (브로 원안) |
  | `compute_grads` | 복수형, 어색 |
- **★ 부수 이점 — 혼란 해소**: step07에선 "전역 backward vs Function.backward(단일 노드) 이름 같고 역할 다름"
  혼란이 있었음. fill_grad로 개명하면 이름이 다르게 되어 혼란 자동 해소.
  (Function.backward는 단일 노드의 국소적 미분 역할이라 이름 유지 — 이건 PyTorch 관례와도 일치.)
- **★ JAX 철학 강화**: #014에서 "전역 함수 = JAX 스타일"이라 했는데, JAX는 `jax.grad(f)(x)`로
  "grad 계산"이 이름에 드러남. `fill_grad`도 같은 결 — "grad"가 이름에 들어가 JAX 정신과 더 가까워짐.
- **★ 패키지화 후 호출**: step23 이후 `from rezero import fill_grad` 또는 `rezero.fill_grad(y)`.
  `jax.grad(f)(x)`와 같은 패턴 (Define-by-Run 버전).
- **⚠️ 최종 반영 여부 보류 (#014와 동일)**:
  - PyTorch/DeZero 표준에서 더 벗어남 (backward → fill_grad). 학습용 실험으로 명시.
  - step09+ 에서 책이 `backward`를 계속 쓰면, 우리 문서가 책과 용어 안 맞을 수 있음
  - 하지만 **의미 투명성** 가치가 큼 — "하는 일이 이름에 드러나야"라는 브로 철학 반영
  - step13/step34 진입 시점에서 #014와 함께 재평가
- **검증**:
  - `pyright rezero/steps/step08.py` → 환경성 에러 2개만 (step07과 동일, 코드 결함 아님) ✅
  - 실행: `fill_grad(y)` → `x.grad = 3.297442541400256` (step07 backward와 동일) ✅
- **회수**: step23 → `rezero/core.py` 또는 `rezero/__init__.py`에 `fill_grad` 승격 (#014와 함께 유지)
- **관련**: debugging.md 항목 1 (assert + `-O`), 항목 2 (RecursionError) — step08 검증 설계 맥락

### #016 — assert → RuntimeError 전환 (검증 A: 사용자 오용 구분) — debugging.md 교훈 2 적용
- **위치**: step08
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 (검증 설계 원칙 적용)
- **브로 질문**:
  > "assert가 다분히 디버깅 상황의 언어 제공 도구라면, 저런 제약 체크를 지금 저렇게 assert로 하는 게 맞냐?
  >  그리고 점검 위치가 저기가 맞아?"
  → 두 부분 모두 적중. (1) assert 종류 잘못됨, (2) 위치도 잘못됨.
- **내용**: step08 fill_grad의 검증 3종 중 **(A)만 if/raise로 전환**, 위치도 초기화 시점으로 이동:
  | 검증 | 상황 | 이전(step08 초안) | 이후(step08 개선) |
  |---|---|---|---|
  | (A) start_var.creator None | 입력 변수에 fill_grad 호출 = **사용자 오용** | pop 후 assert | **if/raise RuntimeError**, 초기화 시점 ★ |
  | (B) f.input/f.output None | __call__ 미실행 = 프로그래머 논리 버그 | assert | assert 유지 |
  | (C) y.grad None | 이전 반복 미충족 = 프로그래머 논리 버그 | assert | assert 유지 |
- **★ 핵심 원칙 (debugging.md 교훈 2 직접 적용)**:
  - **사용자 오용 / 런타임 데이터** → `if ...: raise` (★ `-O` 모드에서도 살아남아야)
  - **프로그래머 불변조건** → `assert` (`-O`에서 사라져도 로직 안전)
  - (A)는 "creator 없는 변수에 역전파 호출" — 이건 프로그래머 논리 버그가 아니라 **사용자 오용**.
    따라서 assert 부적절. RuntimeError가 맞음.
- **★ 위치 개선**: pop **이후**에 검사하면 이미 None을 스택에 넣은 뒤. 더 근본 위치는 **함수 도입부 맨 앞**.
  → (A)를 맨 앞으로 옮김 (fail-fast / guard clause). **브로 2차 지적** — upstream 설정 후 검사하면
  에러 내기 전에 `start_var.grad`를 변경하는 부작용이 발생. 도입부에서 검사하면
  **실패한 연산은 부작용을 남기지 않음**(transactional semantics)까지 보장.
- **★ fail-fast + 부작용 회피 실증** (도입부 이동 후):
  ```
  정상:    fill_grad(y) → x.grad = 3.2974...  ✅
  오용:    fill_grad(x) [입력 변수]
           호출 전 x.grad = None
           RuntimeError 발생 (fail-fast)
           호출 후 x.grad = None  ← ★ 부작용 없음 (transactional)
  ```
- **★ -O 모드 실증** (debugging.md 교훈의 코드 증명):
  ```
  정상:    fill_grad(y) → x.grad = 3.2974...  ✅
  오용:    fill_grad(x) [입력 변수] → RuntimeError ✅
  -O 모드: fill_grad(x) → ★ RuntimeError 여전히 발생 ✅ (assert였으면 사라졌을 것!)
  ```
  → assert였다면 `-O` 모드에서 조용히 통과했을 위험을 RuntimeError로 방어.
- **★ 친절한 에러 메시지**:
  ```
  RuntimeError: <Variable>에 creator가 없습니다 — 역전파할 계산 그래프가 없습니다.
  입력 변수(원점)가 아닌, 함수의 출력에 대해 fill_grad를 호출하세요.
  ```
  (책의 assert 메시지보다 훨씬 친절 — "왜 잘못됐는지" + "어떻게 고치는지" 둘 다.)
- **검증**:
  - 정상/오용/-O 3케이스 전부 의도대로 동작 ✅
  - 도입부 이동 후: 잘못된 호출이 `x.grad`를 변경시키지 않음(transactional) 실증 ✅
  - `pyright` → 환경성 에러만 ✅
- **회수**: step23 → `rezero/core.py` fill_grad 승격 시 검증 로직 함께 유지

### #017 — ★★ `funcs` → `worklist` 리네임 (브로 작명 통찰 — CS 학술 패턴 인식)
- **위치**: step08
- **상태**: ✅ 반영 (2026-07-29)
- **종류**: 🔵 라이브러리성 ★★ (#015 fill_grad 개명과 같은 결 — 의미 투명성)
- **브로 질문**:
  > "funcs란 변수명을 이것이 의미하는 것에 맞도록 변수명 리팩터링 가능할까? 좀 느낌있게?"
  → `funcs`는 "functions" 축약이라 **무엇의 스택인지** 안 드러남. 단순 리네임인 줄 알았더니
  **CS 학술 패턴 "Worklist Algorithm"** 인식으로 이어짐 (브로 "이게 학술 용어야?" 놀람).
- **내용**:
  ```python
  # 이전 (step08 초안, 책 관례)
  funcs = [start_var.creator]     # "functions" 축약 — 무슨 함수들인지 암시만
  while funcs: ...
      funcs.append(x.creator)

  # 이후 (step08 개선)
  worklist = [start_var.creator]  # ★ "역전파 처리 대기 Function 스택" 의미 명시
  while worklist: ...
      worklist.append(x.creator)
  ```
- **★ 왜 worklist인가** (후보 비교):
  | 이름 | 평가 |
  |---|---|
  | `funcs` (책 관례) | 축약만. 의미 안 드러남 |
  | `worklist` ★ | CS 학술 용어. 그래프 순회/데이터플로우/GC 등 정확한 패턴 이름 |
  | `func_stack` | 직관적이나 학술적 깊이 없음 |
  | `pending` | 제네릭. 무엇이 pending인지 안 드러남 |
- **★ 핵심 — 코드가 속한 학술 전통 인식**:
  `while worklist: pop → 처리 → push` 구조는 **Worklist Algorithm**이라는 정식 CS 패턴.
  Dragon Book(컴파일러 데이터플로우), GC handbook(mark phase), CLRS(그래프 순회) 등
  CS 전반에 깔린 "처리 대기열 + while pop" 골격. 우리 역전파는 이 패턴의 인스턴스.
  → 변수명 worklist는 **단순 리네임이 아니라 코드의 학술적 뿌리 인식**.
  상세: design_patterns.md 패턴 4 "Worklist Algorithm" (브로 질문에서 파생된 새 패턴 등록).
- **★ 매핑 (DeZero 역전파 ↔ 일반 worklist 골격)**:
  | 일반 골격 | DeZero 역전파 |
  |---|---|
  | 초기 노드 | `start_var.creator` |
  | 처리(n) | `f.backward(y.grad)` (fold step) |
  | 후속(n) | `x.creator` |
  | 종료 | worklist 빈 경우 (원점 도달) |
  | 방향 | 역방향 + LIFO(pop) = **DFS** |
- **★ 패턴 3(점진적 설계)과의 시너지**:
  브로의 연달은 두 질문 ("왜 리스트?", "funcs 말고 worklist로?")이 **같은 코드의 두 층위**를 파냄:
  - 패턴 3: worklist가 리스트형인 이유 (step14/16 DAG 복선)
  - 패턴 4: 그 리스트가 worklist algorithm 골격을 따름
- **★ 연장 — Worklist 타입 별칭 (브로 2차 통찰)**:
  브로: *"work item이 Function 인스턴스면 타입 힌트로 명확히할 수 있지 않나?"*
  → `type Worklist = list[Function]` (Python 3.12+ `type` 문) + `worklist: Worklist = [...]`
  → work item = Function 인스턴스가 **타입 수준에서 명시**됨.
- **★★ 시너지 — guard clause(#016)와 타입 힌트 협력 (emergent design)**:
  - `start_var.creator: Optional[Function]` → 그냥 `list[Function]`에 넣으면 pyright 에러
  - 근데 도입부 guard(`if creator is None: raise`)가 **타입 좁히기** 수행 → 아래부턴 `Function` (Optional 풀림)
  - → #016(fail-fast)이 #017(worklist 타입)에 타입 안전성을 제공
  - 실증: guard 없음 `error "list[Function | None]" is not assignable`, guard 있음 ★ 에러 없음
  - **★ 교훈**: step08 변형 3종(#015/#016/#017)이 독립이 아니라 서로 강화하는 세트.
    guard clause가 단순 "빠른 실패"가 아니라 "타입 좁히기"까지 보너스. 좋은 결정들은 강화된다.
- **검증**:
  - `fill_grad(y)` 실행 → `x.grad = 3.297442541400256` (리네임/타입 힌트 전후 동일) ✅
  - pyright → 환경성 에러 2개(override/numpy) + type 문 버전 에러 1개 (Python 3.12+ 기능, step23 설정 시 해결 예정)
- **회수**: step23 → `rezero/core.py` fill_grad 내부 worklist + Worklist 타입 별칭 함께 유지

### #018 — ★★ `pipe` 헬퍼 (FP 합성) — step11~22 보류, step23 재도입 예정
- **위치**: step09 도입 / step10 검증 / **step11~22 보류** / step23 재도입 예정
- **상태**: 🔄 보류 (2026-07-30, step11 진입 시 결정)
- **종류**: 🔵 라이브러리성 ★★ (rezero FP 철학 — Haskell/Elixir 스타일 데이터 흐름 합성)
- **추적**: [Issue #13](https://github.com/ghjang/deep-learning-from-scratch-3/issues/13)
- **내용**: step09에서 도입한 `pipe(value, *funcs)` 헬퍼 (FP 합성).
  ```python
  def pipe(value, *funcs):
      """데이터 흐름 순서로 함수 합성. pipe(x, f, g, h) = h(g(f(x)))."""
      return reduce(lambda val, f: f(val), funcs, value)
  ```
  step10에서 `pipe(x, square, exp, square)`로 합성 함수 gradient check까지 검증 완료.
- **★ 왜 보류하나 (step11~22)**:
  step11부터 **가변 길이 인수**(2고지) 도입 → `Add(x0, x1)` 같은 **다입력 함수** 등장.
  pipe는 **단일 흐름 합성**만 표현하므로 다입력 함수엔 구조가 안 맞음:
  ```
  pipe(x, square, exp)             # ✅ 단일 흐름 — pipe 잘 맞음
  pipe(???, add(x0, x1), square)   # ❌ 다입력 — pipe 구조로 표현 안 됨
  ```
  → 2고지(step11~24) 동안은 step 소스에서 **pipe 제외**. 단일 함수 wrapper(square/exp)는 유지.
- **★ 재도입 시점 — step23 패키지화**:
  `rezero/core.py` 등으로 승격할 때 pipe도 재도입. 핵심 화두: **다입력 함수를 pipe에 어떻게 끼워넣나?**
- **★ step23에서 풀어볼 FP 화두** (Issue #13에 상세):
  | 화두 | 키워드 | 방향 |
  |---|---|---|
  | `compose` vs `pipe` | 방향(데이터 순서 vs 수학적 합성) | 둘 다 제공? 일반화? |
  | partial binding | `functools.partial`, 커링 | 다입력 → 단일 흐름 변환 |
  | `bind` (모나드) | Haskell `>>=`, Variable 문맥 | 심화(오버엔지니어링 위험) |
- **★ 학습 가치**: 단순 "합성 헬퍼"가 아니라 **FP 패러다임과의 접점**.
  pipe/compose/partial/curry/bind는 함수형 프로그래밍의 핵심 개념들.
  step23에서 DeZero(Define-by-Run)과 FP(합성)가 어떻게 만나는지 실험할 자리.
- **회수**: step23 → `rezero/__init__.py` 또는 utils성 모듈에 재도입 (★ FP 화두와 함께 논의)

### #019 — ★★★ `self.outputs` (리스트) → `self.output` (단수) — 스칼라 출력 명시 (step13)
- **위치**: step13~
- **상태**: ✅ 반영 (2026-07-30)
- **종류**: 🔵 라이브러리성 ★★★ (책과 다른 구조적 선택, rezero 정체성 + 학습 명시성)
- **내용**:
  책 원본 step13은 `self.outputs = outputs` (리스트, 복수형)로 출력을 저장.
  이유: 미래 다출력 함수(step34+) 대비 "미리 나간" 구조.
  rezero는 **step13 시점(출력 스칼라 1개)에 충실하게 단수 `self.output`로 단순화**:
  ```python
  # 책 (복수형, 미래 확장 대비)
  self.outputs = outputs                              # list[Variable]
  return outputs if len(outputs) > 1 else outputs[0]  # 반환만 단일화

  # rezero (단수, 스칼라 명시)
  assert len(ys) == 1, "step13은 출력 1개(스칼라) 가정"
  output = Variable(as_array(ys[0]))
  self.output = output                                # Variable 1개
  return output                                       # 항상 단일
  ```
- **★ 왜 단수화했는가 (3가지 이유)**:
  1. **step13 시점 정확성** — 다출력 함수가 step34+까지 안 나옴. 굳이 복수 구조 유지할 이유 없음
  2. **Pylance 만족** — 책의 리스트 언패킹(`f.backward(*gys)`)은 단일 인자 backward와 불일치 경고.
     단수화하면 `f.backward(f.output.grad)` 직접 회수로 깔끔.
  3. **"스칼라 출력 전용" 명시** — derivative hook의 유효 범위(step01~33)가 코드 구조로 드러남.
     self.output 단수 = "이 프레임워크는 출력 1개만 다룬다" 선언.
- **★★★ 핵심 — step34+ 진화 지점 (다른 세션 반드시 인지)**:
  step34+에서 **다출력 함수(벡터/행렬 출력)** 가 등장하면 `self.output` → `self.outputs` (복수)로 **되돌려야 함**.

  ★ 다출력 함수의 예 — **Split** (책 step13 그림에 복선으로 등장, 브로 발견):
  하나의 입력을 여러 출력으로 쪼개는 함수 (Add와 정반대 방향):
  ```
  입력 1개        출력 N개
   [x]  ──Split──→  [y0], [y1], ...
  ```
  실제 사례: multi-head attention (특징 벡터 → 여러 head 분기),
  multi-task 분기 (은닉층 → classification + regression), PyTorch `torch.split`/`torch.chunk`.
  책은 코드엔 안 내면서 **그림으로만 살짝 예고** (미래 복선 전략). step34+ 또는 신경망 응용(step40+)에서 실제 등장 예상.
  → 이 Split 같은 다출력 함수가 등장하는 시점이 바로 self.output → self.outputs 진화가 필요한 순간.
  그때 함께 바꿔야 할 것들:
  | 변경 항목 | step13 (현재) | step34+ (진화) |
  |---|---|---|
  | `self.output` | 단수 Variable | `self.outputs` list[Variable] (복수) |
  | `__call__` 반환 | `Variable` | `Variable \| list[Variable]` (책처럼 len으로 분기) |
  | `fill_grad` 회수 | `f.output.grad` 직접 | `output_grads = [out.grad for out in f.outputs]` |
  | `backward` 시그니처 | `(self, upstream_grad)` 단일 | `(self, *gys)` 가변 (다출력 대응) |
  | derivative hook | 유효 (스칼라 곱) | ★ 붕괴 — backward 직접 오버라이드 필수 (야코비안) |
  → 이 표가 **"step34 진입 체크리스트"** 임. step34 이슈 생성 시 이 항목 참조.
- **★ 책과의 차이 — 학습 서사**:
  - 책: "미리 다출력 대비 구조" → 독자가 "왜 복수지?" 혼란 (브로 경험)
  - rezero: "step13 시점 스칼라 명시" → step34에서 자연스럽게 복수로 진화 (복선의 회수)
  - 즉 책은 **전진 설계(forward design)**, rezero는 **점진적 진화(evolutionary)**.
    학습용에선 후자가 "왜 이 구조가 필요한지"를 단계별로 체감하게 함.
- **★ 브로 철학 반영**:
  > "리제로의 정체성을 유지하고 싶고, 이건 학습이니 우리 의도대로 진행해보자.
  >  그 길이 잘못됐으면 '아! 그래서 그랬군!' 하며 뒷목 잡겠지만,
  >  실수로 인해 많이 배우지 않겠냐?"
  → 이 변형은 그 철학의 실현. "책과 다른 길을 가되, 그 근거와 회수 지점을 명시한다."
- **★ 관련 혼동 교훈 (LEARNING_NOTES step13에 상세)**:
  "다변 역전파 ≠ 다출력 역전파" — step13은 **입력은 다변(Add: x0,x1)** 이지만 **출력은 스칼라 1개**.
  이 혼동에서 비롯된 3가지 수정 연쇄 (이전 초안 → 최종):
  1. `backward(*gys)` 가변 → `backward(upstream_grad)` 단일
  2. `gy` → `upstream_grad` (#007 정체성 회복)
  3. `f.outputs` 리스트 언패킹 → `f.output.grad` 직접 (이 항목)
- **검증**: `z = add(square(x), square(y)) → x.grad=4, y.grad=6` 정상 동작 ✅
- **회수**: step23 → `rezero/core.py` Function 승격 시 self.output 단수 유지.
  단, **step34 진입 시 반드시 self.outputs 복수로 진화** (위 표 참조).

### #020 — ★★ step23 패키지화 시 역전파 주석/docstring 정비 (학습 관점 트레이드오프 서술)
- **위치**: step13 도입 / **step23 회수 완료**
- **상태**: ✅ 반영 (2026-08-10, step23에서 주석 정리 기준 수립 + v1 패키지에 적용)
- **종류**: 🟢 step 한정 → step23 회수 (문서화 작업)
- **내용**:
  derivative hook 구조(step07~13)는 **역전파의 일반적 구조(chain rule fold step)를 부모 한 곳에 집중**시킴.
  장점: 수학 구조 명확, 네이밍 투명 (partials, upstream_grad 등).
  단점: 말단 함수(Square/Add)의 `derivative` 1줄만 보면 **"이 함수의 역전파"가 안 보임**.
  책 방식(backward 직접)은 반대 — 각 함수가 `return 2*x*gy` 식으로 역전파 직접 체감 강함.
- **★ 트레이드오프 (브로 통찰)**:
  | 관점 | 우리 방식 (derivative hook) | 책 방식 (backward 직접) |
  |---|---|---|
  | 역전파 일반 구조 체감 | ★ 강함 (부모 fold step 집중) | 약함 (각 함수마다分散) |
  | 각 함수 역전파 직접 체감 | 약함 (derivative 1줄만) | ★ 강함 (`2*x*gy` 직접 작성) |
  | 수학 구조 드러남 | ★ 강함 (partials, chain rule) | 약함 |
  | DRY (중복 제거) | ★ 강함 | 약함 (자식마다 fold step 중복) |
  브로 의견: *"추상화 관점에선 상위 클래스 메인 동작 보는 게 덜 헷갈린다"*
  → 역전파 일반 구조 이해엔 우리 방식이 유리. 각 함수 직접 체감엔 책 방식이 유리.
- **★ step23 회수 시 할 일 (구체적)**:
  `rezero/core.py` Function + `functions.py` 자식들 승격할 때:
  1. **Function.backward docstring** — "이 메서드가 chain rule fold step의 일반 구조" 명시
  2. **Square/Add docstring** — "이 함수의 역전파는 derivative()로 표현, 부모 backward가 fold" 안내
  3. **(선택) 비교 주석** — Square에 책 방식(`# def backward(self, gy): return 2*x*gy`)을 주석으로 남겨
     "이렇게도 할 수 있지만 우린 derivative hook 택함" 비교 가시화
  → 학습자가 core.py 읽을 때 "왜 이 구조인지 + 책과 어떻게 다른지" 한번에 파악 가능
- **★ 까먹지 않게 하는 장치**:
  이 항목 자체가 "step23 회수 예정" 항목. 항목 018(pipe), 019(output 단수)와 같은 패턴.
  step23 진입 시 REZERO_CHANGES에서 항목 020 보고 "아, 역전파 주석 정비 있었지" 회수.
- **회수**: step23 → `rezero/core.py` + `functions.py` 승격 시 docstring/주석 정비

### #021 — `cleargrad` → `clear_grad` — 스네이크 케이스 일관성 (step14)
- **위치**: step14~
- **상태**: ✅ 반영 (2026-07-30)
- **종류**: 🔵 라이브러리성 (네이밍 일관성)
- **브로 지적** (step14):
  > "cleargrad가 Variable 클래스에 들어간 건데, 'clear_grad'가 아니라 걍 붙여쓴 거,
  >  잘 보면 알겠지만. 그리고 set_creator가 떡하니 _를 쓰고 있는데."
  → 같은 클래스 안에서 `set_creator` (언더스코어 O) vs `cleargrad` (언더스코어 X) 불일치 발견.
- **내용**:
  책 원본 step14는 `cleargrad` (언더스코어 없음). 하지만 같은 Variable 클래스에
  `set_creator` (언더스코어 있음)가 있어서 **PEP 8 스네이크 케이스 불일치**.
  rezero는 일관성 위해 `clear_grad`로 수정:
  ```python
  # 책 원본 (불일치)
  def set_creator(self, func): ...    # 언더스코어 O
  def cleargrad(self): ...            # 언더스코어 X ★ 불일치

  # rezero (일관성)
  def set_creator(self, func): ...    # 언더스코어 O
  def clear_grad(self): ...           # ★ 언더스코어 O로 통일
  ```
- **★ 왜 책이 이렇게 됐을까 (추측)**:
  책의 `set_creator`는 step02에서, `cleargrad`는 step14에서 도입.
  각각 다른 시점에 추가되면서 일관성 검사가 누락된 것으로 보임.
  자바/루비 배경의 개발자라 `clearGrad` (카멜)에 익숙해서 `cleargrad` (소문자 통일)로 쓴 뒤
  파이썬 스네이크 케이스 규칙을 부분 적용한 흔적일 수 있음.
- **★ 이 변형의 가치**:
  네이밍 일관성은 "읽을 때 거슬리지 않는" 핵심. 같은 클래스의 메서드들이
  같은 케이스 규칙을 따르면 인지 부하 ↓. rezero 정체성 (네이밍 투명성, 항목 007/015와 같은 결).
- **★ 향후 다른 비슷한 메서드들 검토 (step 진행하며)**:
  step16 `backward` (이미 단어 1개라 해당 없음), step19 `cleargrad` 확장 등.
  새 메서드 추가 시 "이 클래스의 다른 메서드와 케이스 일치?" 항상 체크.
- **검증**: `clear_grad()` 실행 정상, grad None으로 초기화 확인 ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 `clear_grad` 유지

### #022 — ★★ `seen_set` → `visited` (CS 학술 표준, 탐구 18번과 일치) (step16)
- **위치**: step16~
- **상태**: ✅ 반영 (2026-07-31)
- **종류**: 🔵 라이브러리성 ★★ (네이밍 투명성, #007/#015/#017과 같은 결)
- **내용**: 책 원본은 중복 push 방지용 set을 `seen_set`으로 명명.
  rezero는 CS 그래프 순회 알고리즘의 학술 표준 용어 **`visited`** 로 교체:
  ```python
  # 책 (관례적)
  seen_set = set()       # "본 적 있는" — 무엇을? 암시만
  def add_func(f):
      if f not in seen_set: ...

  # rezero (학술 표준)
  visited: set[Function] = set()    # ★ "방문한" — DFS/BFS/위상정렬 필수 용어
  def schedule(f):
      if f not in visited: ...
  ```
- **★ 왜 visited인가** (후보 비교):
  | 이름 | 평가 |
  |---|---|
  | `seen_set` (책) | 의미는 통하나 "본 적 있는"이 암시적. set 자료형도 이름에 중복 인코딩 |
  | `visited` ★ | CS 학술 표준 (CLRS, DFS/BFS, 위상정렬 Kahn's algorithm 어디서나). 타입 힌트로 set임 명시 가능 |
- **★ 코드 ↔ 탐구 노트 일관성** (핵심 가치):
  `notes/exploration_18_graph_traversal.md`에서 그래프 순회 알고리즘 설명 시 **`visited`** 용어 사용.
  코드도 같은 단어 쓰면 학습자가 "코드 ↔ 노트" 대응이 즉시 됨.
  ★ 이게 브로가 추천을 수락한 결정적 이유 — 일관성 있는 어휘가 학습 가치 ↑.
- **★ 타입 힌트 부수 이점**:
  `seen_set`은 set 자료형을 이름에 박아넣어 타입 힌트(`: set[Function]`)와 중복.
  `visited`는 추상적이라 타입 힌트로 구체화하는 게 자연스러움.
- **★ 관련 네이밍 셋트** (이번 step에서 완성):
  `worklist`(항목 017) + `visited`(이 항목) + `schedule`(항목 023) = **그래프 순회 알고리즘 CS 학술 용어 3총사**.
  → 코드만 봐도 "역방향 위상 정렬 수행 중"이 한눈에 드러남.
- **검증**: `visited` 도입 후 데모 `x.grad = 64.0` (정답지와 일치) ✅
- **회수**: step23 → `rezero/core.py` fill_grad 승격 시 `visited` 유지

### #023 — ★★ `add_func` → `schedule` (위상 순서 예약 의미 명시) (step16)
- **위치**: step16~
- **상태**: ✅ 반영 (2026-07-31)
- **종류**: 🔵 라이브러리성 ★★ (#022 visited, #017 worklist와 한 쌍)
- **브로 지적** (step16 변형 포인트 C 토론):
  > "개인적으로 'add_func'라는 함수명이 마음에 들지 않는데... visited로 변수명도 우리 바꿀 것이잔아?
  > 뭔가 좀 더 와닿는 의미에 맞는 네이밍 없나?"
  → `add_func`은 "함수 추가"라 너무 제네릭. **무슨 조건으로? 어디에? 어떤 순서로?** 안 드러남.
- **내용**:
  ```python
  # 책 (관례적)
  def add_func(f):
      funcs.append(f); seen_set.add(f); funcs.sort(key=...)   # 3가지 동작 묶음인데 이름엔 "추가"만

  # rezero (위상 순서 예약 명시)
  def schedule(f):
      worklist.append(f); visited.add(f); worklist.sort(key=...)  # "순서 있게 처리 예약" 의미
  ```
- **★ 왜 schedule인가** (후보 비교 — 브로와 토론):
  | 이름 | 평가 |
  |---|---|
  | `add_func` (책) | "함수 추가". 제네릭. visited 체크/정렬까지 묶었다는 게 안 드러남 |
  | `enqueue` | "큐에 넣기" worklist 뉘앙스. 근데 정확히 큐(LIFO)가 아니라 정렬 리스트라 어색 |
  | `push` | "스택에 밀어 넣기". 정렬까지 한다는 게 안 드러남 |
  | `schedule` ★ | "순서 있게 처리 예약" ★ 가장 정확. 위상 정렬/워크플로우 뉘앙스. 브로 선택 |
  | `register` | "등록하다" 깔끔하나 "순서" 뉘앙스 약함 |
- **★ 브로 선택 근거** (schedule 결정):
  > "schedule이 일단 깔끔한 느낌? worklist와도 잘 맞는 것 같고?"
  → `worklist`(대기열) + `schedule`(예약하다)는 자연어에서도 짝을 이루는 단어 조합.
  "worklist에 schedule 한다" = "대기열에 순서대로 예약한다". 코드가 문장처럼 읽힘.
- **★ 핵심 가치 — 클로저 3가지 동작을 이름에 인코딩**:
  `schedule(f)`는 사실 **3가지 동작**을 묶은 클로저:
    1. visited 체크 (중복 push 방지)
    2. worklist append (대기열 추가)
    3. generation 정렬 (위상 순서 유지)
  책의 `add_func`은 이 중 1,2번만 암시. **3번 "정렬"이 이름에 안 드러남**.
  `schedule`은 "순서 있는 예약"이므로 3번까지 암시 — 3가지 동작 모두 이름에 인코딩.
- **★ 클로저 유지 결정 (변형 포인트 C — 책 방식 채택)**:
  schedule은 **모듈 수준 함수가 아니라 fill_grad 내부 클로저**로 둠 (책 방식 존중).
  이유: worklist + visited 두 상태를 캡처하는 클로저가 자연스러움. 모듈 함수로 빼면
  인자로 worklist/visited 둘 다 넘겨야 해서 시그니처가 길어짐. step16만의 특수 로직이라
  재사용성 낮음 → 굳이 빼지 않음.
- **★ heapq 변형은 보류 (변형 포인트 D — 책 충실)**:
  schedule 내부의 매 `sort`는 O(n log n)을 n번 = O(n² log n)으로 비효율적.
  heapq 우선순위 큐로 O(n log n) 최적화 가능하지만, "step16 본 목적은 generation 개념 도입이지
  성능 최적화가 아님" + "worklist 단순 스택 구조가 흔들림" 이유로 **책 충실(sort) 채택**.
  heapq는 별도 탐구 후보로 큐에 등록 (동작 확인 후 재논의 가능).
- **검증**: `schedule` 도입 후 데모 `x.grad = 64.0` (정답지와 일치) ✅
- **회수**: step23 → `rezero/core.py` fill_grad 승격 시 `schedule` 클로저 유지

### #024 — ★★ `fill_grad`에 generation 정렬 + visited 통합 (전역 함수 구조 유지) (step16)
- **위치**: step16~
- **상태**: ✅ 반영 (2026-07-31)
- **종류**: 🔵 라이브러리성 ★★ (항목 014/015의 자연스러운 확장, rezero 정체성 유지)
- **내용**: 책 원본은 `Variable.backward()` 메서드 안에 generation 정렬 로직을 통째로 넣음.
  rezero는 **전역 `fill_grad` 함수 안에 generation 정렬 + visited를 통합** (항목 014 정체성 유지):
  ```python
  # 책 (Variable 메서드 — generation 로직이 Variable에 흡수)
  class Variable:
      def backward(self):
          funcs, seen_set = [], set()
          def add_func(f): ...
          # generation 정렬 + 역전파 + 누적 모두 Variable 메서드 안

  # rezero (전역 함수 — Variable은 순수 데이터 상자 유지)
  def fill_grad(start_var, upstream_grad=None):
      worklist, visited = [], set()
      def schedule(f): ...                    # ★ generation 정렬 클로저
      # 역전파 순회 로직은 전역 함수에. Variable은 data/grad/creator/generation만.
  ```
- **★ 핵심 가치 — 관심사 분리(SoC) 유지 (항목 014 연장)**:
  step07에서 "Variable은 순수 데이터 상자, 그래프 순회는 별도 함수" 원칙 수립.
  step16에서 generation 정렬이 추가되도록 **이 원칙 유지**.
  - Variable: data + grad + creator + generation (순전파 깊이) — 여전히 순수 데이터
  - fill_grad: 그래프 순회 + generation 정렬 + visited 중복 방지 — 순회 알고리즘 총괄
  → 책은 "generation 정렬까지 Variable에 흡수"하지만, rezero는 "순회 로직은 전역 함수에" 일관성 유지.
- **★ generation 필드는 Variable/Function 양쪽에 (데이터는 Variable에, 계산은 fill_grad에)**:
  generation **값 자체**는 Variable/Function의 속성 (순전파 깊이 = 데이터).
  generation **정렬 활용**은 fill_grad의 알고리즘. 이 분리가 SoC의 핵심.
- **★ REZERO_CHANGES 항목 012 복선 회수** 🔥:
  step07에서 "왜 set_creator를 단순 할당 말고 메서드로 뒀을까?" 의심 → "미래 확장 포인트 예약" 납득.
  ★ 그 미래가 바로 step16 — set_creator에 `self.generation = func.generation + 1` 한 줄이 추가되는 순간.
  항목 012의 복선이 회수됨. 이게 브로가 step07에서 의심을 품은 것의 진짜 가치.
  step14 docstring에 "step16 generation 확장 포인트" 적어둔 것도 같이 회수.
- **★ rezero 정체성 정립 — step07~16 변형 흐름**:
  | step | 변형 | rezero 정체성 기여 |
  |---|---|---|
  | step07 (항목 014) | backward → 전역 `fill_grad` | Variable 순수 데이터 상자 원칙 수립 |
  | step08 (항목 015/017) | `fill_grad` 개명 + `worklist` 리네임 | 의미 투명성 + Worklist Algorithm 인식 |
  | step16 (이 항목) | generation 정렬 + visited 통합 | SoC 원칙 유지하며 복잡 그래프 대응 |
  → rezero는 "책의 알고리즘은 따르되, 구조는 Variable/Function/전역함수 관심사 분리 원칙 유지".
- **★ 가정/전제 2종 (step14 전제에 추가)**:
  | 새 전제 (step16) | 의미 | 깨지면? |
  |---|---|---|
  | 계산 그래프는 DAG (위상순서 존재) | generation 정렬 가능한 전제 | Define-by-Run에선 사이클 안 생김 — 항상 성립 |
  | 같은 Function이 worklist에 중복 push 가능 | `add(square(a), square(a))`에서 a.creator 두 번 push | visited로 방어 (이 항목) |
- **검증**:
  - 분기/합류 데모: `y.data=32.0, x.grad=64.0` (정답지와 일치) ✅
  - generation 값: x=0, a=1, y=3 (표현식 중첩 깊이와 일치) ✅
- **회수**: step23 → `rezero/core.py` 또는 `rezero/__init__.py`에 fill_grad 승격 (★★★ rezero 정체성)

### #025 — ★★★ 크로스 참조 네이밍 — 개명 시도/철회 + 현대 Pythonic 교훈 (step16)
- **위치**: step16
- **상태**: ⏭ 시도 후 철회 (2026-07-31) — 책 원본 이름 유지
- **종류**: 🟢 step 한정 + ★ 학습 가치 영구 보존 (탐구 노트 19번으로 승격)
- **브로 통찰 1** (개명 시도 트리거):
  > "우리가 사용하고 있는 Variable의 'creator'라는 속성명을 왠지 creator_func로 바꾸고 싶은 충동이...
  > 왠지 좀 더 명시적으로 설명을 해주는 게 나을 것 같다는 느낌은?"
  → `creator`만 보면 "사람? 객체? 함수?" 타입이 `Function`이라는 게 이름에 안 드러남.
  `creator_func`라면 즉시 "이걸 만든 함수"가 드러남. → 4종 전면 개명 시도.
- **브로 통찰 2** (철회 트리거) ★★★:
  > "변경 후 코드를 보니, 변수명 자체와 타입 힌트가 중복 느낌은 있는데...
  > 이렇게 보통 우리 코드처럼 코딩해도 이게 파이쏘닉한가 어쩐가?"
  → ★ 정확한 자각. `creator_func: Function`은 **이름에 타입 인코딩 + 타입 힌트로 또 인코딩** = 중복.
  이건 **Systems Hungarian** (변수명에 타입 박는 구식 관행)의 냄새.
- **내용** — 시도했다가 철회한 개명:
  ```python
  # 시도 (2026-07-31, 약 30분 유지)          # 철회 후 (책 원본 이름 유지)
  class Variable:
      creator_func: Function      →           creator: Optional["Function"]
      set_creator_func(func)      →           set_creator(func)
  class Function:
      input_vars: tuple[Variable] →           inputs: Optional[tuple[Variable, ...]]
      output_var: Variable        →           output: Optional[Variable]
  ```
- **★ 최종 결정 — 책 원본 이름 유지 + 타입 힌트로 보완** (현대 Pythonic):
  ```python
  self.creator: Optional["Function"] = None    # creator (역할) + Function (타입 힌트)
  self.inputs: Optional[tuple[Variable, ...]]  # inputs (역할) + tuple[Variable] (타입)
  self.output: Optional[Variable]             # output (역할) + Variable (타입)
  ```
  → "이름은 역할, 타입은 힌트에 맡긴다" (현대 파이썬 철학).
  크로스 참조 구조는 타입 힌트로 충분히 가시화됨 (IDE hover/pyright로 즉시 확인).
- **★★★ 핵심 교훈 — Systems Hungarian vs 현대 Pythonic**:
  | 관점 | 평가 |
  |---|---|
  | `creator_func: Function` | 이름에 타입(Function) 박음 + 타입 힌트로 또 박음 = **중복** (Systems Hungarian 냄새) |
  | `creator: Function` | 이름은 역할(creator), 타입은 힌트(Function) = **독립적 정보** (Pythonic) |
  → 판별 기준: **"이름이 역할을 말하는가, 타입을 말하는가?"**. 역할 OK, 타입 중복 NG.
  상세: notes/exploration_19_naming_hungarian.md (헝가리안 역사, PEP 8, PyTorch 사례, 판별 기준)
- **★ 예외적으로 `_var`/`_func`를 쓰는 곳** (이건 헝가리안 아님 — 충돌 회피/구분 목적):
  - `Function.__call__(input_var)` (항목 002) — 빌트인 `input` 섀도잉 회피
  - `fill_grad(start_var)` (항목 014) — `output`과 구분 + Variable 타입 명시적
  - → 충돌/구분이 필요할 때만. 타입 인코딩이 동기가 아님.
- **★★★ 부수 산물 1 — AGENTS.md "최우선 규칙 2" 하위 항목 신설** (영구 보존):
  브로 핵심 지적:
  > "과거의 스텝 소스코드 파일을 수정하는 것은 말이 안 돼잖아?
  > 그 시점의 우리의 학습의 흔적인데... 그게 틀리든 맞든..."
  → step01~15 파일은 그대로 보존. 이 결정이 **개명 시도 → 철회 과정에서 자연스럽게 도출**.
  이번 항목(025) 자체가 "step16에만 머무르고 과거 step은 안 건드림" 원칙의 첫 적용 사례.
- **★ 부수 산물 2 — "시도/철회"도 가치 있는 학습 이력**:
  단순히 "책 따라감"이 아니라 "개명 시도 → 자각 → 원칙 발견 → 회귀(단 이유를 알고)" 사이클.
  결과적으로 책 원본으로 돌아갔지만, **왜 Pythonic한지 이해한 상태**로 회귀.
  이게 브로 학습 스타일("쌩짜 재현 ❌, 이해 + 변형 시도 ✅")의 정수.
- **★ PyTorch `grad_fn`와의 관계** (참고):
  PyTorch는 `tensor.grad_fn`으로 "역전파 함수"를 이름에 박음. 우리 `creator_func`와 비슷해 보였으나,
  `grad_fn`의 `_fn`은 **역할**(역전파 함수) 강조지 단순 타입 인코딩이 아님.
  우리 `creator_func`는 순수 타입 인코딩이라 이 기준에서도 철회가 맞음.
- **검증**:
  - 개명 시도 후: `y.data=32.0, x.grad=64.0` (정답지와 일치) ✅
  - 철회 후 재실행: `y.data=32.0, x.grad=64.0` (동일) ✅ — 로직 안 건드림 확인
  - (★ AGENTS.md 신규 "수정 후 재실행" 체크리스트 준수)
- **회수**: ⏭ 철회 항목. step23 → `rezero/core.py` Variable/Function 승격 시 **책 원본 이름** 사용.
  단, 교훈(탐구 노트 19번)은 영구 보존.

### #026 — ★★ weakref 도입 — output을 약한 참조로 (순환 참조 끊기) (step17)
- **위치**: step17~
- **상태**: ✅ 반영 (2026-07-31)
- **종류**: 🔵 라이브러리성 ★★ (메모리 관리 핵심, 책 방식을 단수에 맞게 변형)
- **내용**: Function.output을 weakref로 잡아 순환 참조 끊기.
  ```python
  # 이전 (step16, 강한 참조 — 순환 발생)
  self.output: Optional[Variable] = None
  self.output = output                  # refcount +1 → 순환 참조

  # 이후 (step17, 약한 참조 — 순환 끊김)
  self.output_ref: Optional[weakref.ref] = None
  self.output_ref = weakref.ref(output) # refcount 변동 X → 순환 끊김 ★
  ```
  fill_grad 회수도 weakref 역참조로 조정:
  ```python
  # 이전: output = f.output (직접)
  # 이후: output = f.output_ref() (weakref 역참조, None 가드 추가)
  ```
- **★ 네이밍 — output 이름 유지, 타입 힌트만 진화 (브로 일관성 테스트 통과)**:
  초기엔 `output_ref`라 명명했으나(AI 제안), 브로가 "파이써닉하지 않은 건 아니냐?" 짚음.
  → ★ 정확한 지적. `output_ref`는 `_ref` 접미사로 타입(weakref.ref)을 인코딩 = **헝가리안**.
  step16 #025(creator_func 철회)와 **정확히 같은 패턴** — 탐구 노트 19번 원칙 위반.
  → 철회. 이름은 `output` 그대로, 타입 힌트만 `Variable` → `weakref.ref`로 진화:
  ```python
  # step16: self.output: Optional[Variable] = None      (강한 참조, 역할=출력)
  # step17: self.output: Optional[weakref.ref] = None   (약한 참조, 역할=출력 그대로)
  #         ↑ 이름은 동일, 타입 힌트만 진화 — "이름은 역할, 타입은 힌트에"
  ```
  ★ 학습 가치: step16에서 세운 원칙을 **바로 다음 step에서 AI가 위반**, 브로가 캐치.
  "원칙 수립 ≠ 원칙 준수" — 일관성 테스트의 중요성 증명. (cf. 책은 self.outputs = [weakref.ref(o)] 복수 리스트 — 우리는 단수 + weakref)
- **★★★ 핵심 — 항목 019(self.output 단수)는 유지** (브로 통찰으로 정정):
  AI가 처음에 "step17에서 self.outputs(복수)로 진화 = 항목 019 회수 시점"이라 잘못 연결.
  브로가 정확히 정정:
  > "weakref의 도입이랑, 함수의 출력을 다변화하는 것과는 아무 상관없지 않아?
  >  다변화하지 않고도, 현재 순환참조 문제는 있는 것 아니냐?"
  → ★ 정확함. weakref는 순환 참조 끊기용이지 출력 개수와 무관.
  - 순환 참조: 단일 출력이든 복수 출력이든 발생
  - 출력 다변화: step34+ 진짜 다출력 함수(Split 등)와 무관
  → 항목 019(self.output 단수)는 **step34+ 진정한 다출력 함수 등장 시까지 유지**.
    step17은 단수에 weakref 얹는 `self.output_ref` 조합으로 진행.
- **★ 책의 비대칭 설계 유지 — output만 weakref, inputs는 강한 참조**:
  | 참조 | step17 | 이유 |
  |---|---|---|
  | Function.inputs → Variable | 강한 참조 (유지) | 역전파 시 inputs.data 접근 필요 |
  | Function.output → Variable | 약한 참조 (weakref) | 역전파 후엔 output 필요 없음 → 회수 허용 |
  이 비대칭이 메모리 효율과 역전파 정합성 동시 확보의 핵심.
- **★ weakref 역참조 None 가드 추가** (우리 보강):
  `f.output_ref()`가 None 반환 가능 (output 이미 회수된 경우).
  정상 흐름에선 일어나지 않지만 (사용자가 start_var 들고 있으니 경로상 Variable 살아있음),
  방어막으로 RuntimeError 가드 추가. 친절한 에러 메시지 포함.
- **★ 브로 통찰 — GC와 순환 참조** (탐구 노트 22번으로 심화):
  > "GC가 순환참조 결국 처리한다고 책에 적혀있어"
  → 정확함. 파이썬 GC는 두 단계:
  1. 참조 카운팅 (즉시, 순환 못 잡음)
  2. 순환 감지 GC (주기적 세대별, 순환 잡음)
  즉 순환 참조는 결국 회수됨. 근데 딥러닝 큰 ndarray는 GC 주기까지 기다리면 폭발 → weakref로 즉시 회수 확보.
  상세: notes/exploration_22_weakref_gc.md (CPython 내부 Py_INCREF 스킵, ob_weakreflist 구독자 모델 포함)
- **검증**:
  - 정상 역전파: y.data=32.0, x.grad=64.0 (step16과 동일, 정합성 유지) ✅
  - 메모리 누수 시나리오: for 루프 10회 big_data 정상 완료 (정답지와 동일 동작) ✅
  - (★ AGENTS.md "수정 후 재실행" 체크리스트 준수)
- **회수**: step23 → `rezero/core.py` Function 승격 시 `output` (단수 weakref, 타입 힌트로 `Optional[weakref.ref]`) 유지.
  단, step34+ 진정한 다출력 함수 등장 시 `outputs` 복수로 진화 (항목 019 회수와 동기화).

### #027 — ★ Config + no_grad + retain_grad 도입 (메모리 절약 모드) (step18)
- **위치**: step18~
- **상태**: ✅ 반영 (2026-07-31)
- **종류**: 🔵 라이브러리성 ★ (PyTorch 표준 패턴, 책 방식 충실 + 정체성 한 곳 적용)
- **내용**: 역전파 안 할 때(no_grad 블록) 계산 그래프 구축 생략 + 역전파 후 중간 grad 버리기(retain_grad).
  ```python
  # 신규: Config 전역 플래그 + 컨텍스트 매니저
  class Config:
      enable_backprop: bool = True

  @contextlib.contextmanager
  def using_config(name, value):
      old_value = getattr(Config, name)
      setattr(Config, name, value)
      try:
          yield                          # with 블록 본문에 제어 넘김
      finally:
          setattr(Config, name, old_value)   # 자동 복구 (예외에도)

  def no_grad():
      return using_config('enable_backprop', False)

  # Function.__call__ — 그래프 구축 조건부
  if Config.enable_backprop:
      output.set_creator(self); self.inputs = inputs; self.output = weakref.ref(output)
  return output
  ```
- **★ A/B/C는 책 방식 그대로 (PyTorch 표준 패턴)**:
  | 변형 | 책 방식 | 우리 방향 | 이유 |
  |---|---|---|---|
  | A: Config 클래스 | 전역 클래스 | 동일 | Pythonic, PyTorch 방식 |
  | B: using_config/no_grad | @contextmanager + yield | 동일 | 컨텍스트 매니저 이디엄 |
  | C: __call__ 그래프 조건부 | if Config.enable_backprop: | 동일 | |
  | D: retain_grad | y.backward(retain_grad=False) | ★ fill_grad(y, retain_grad=False) | 정체성 항목 014 유지 |
- **★ D 핵심 — 항목 014(fill_grad 전역 함수) 유지하며 자연스럽게 확장**:
  책은 `y.backward(retain_grad=False)` (Variable 메서드 방식).
  우리는 `fill_grad(start_var, ..., *, retain_grad=False)` (전역 함수, 항목 014).
  - 키워드 전용 인자(`*`)로 retain_grad 받음 — 위치 인자 헷갈림 방지
  - fill_grad 시그니처: `(start_var, upstream_grad=None, *, retain_grad=False)`
  - 정체성 유지 + 자연스러운 매개변수 확장 (과거 호환성도 유지)
- **★ retain_grad 구현 — output.grad 해제**:
  ```python
  # fill_grad 메인 루프 안, 각 Function 처리 후:
  if not retain_grad:
      output.grad = None    # 이번 Function 출력의 grad은 역전파 후 안 쓰므로 버림
  ```
  - 중간 Variable grad은 보통 필요 없음 (최종 입력 x0.grad 등만 사용)
  - 큰 ndarray 중간 grad이 메모리 잡아먹는 것 방지
- **★★ 핵심 학습 포인트 — 컨텍스트 매니저 마법** (탐구 노트 23번으로 심화):
  `@contextlib.contextmanager` + `yield`가 어떻게 `with`를 지원하는가.
  - yield 본질 = "실행 일시정지 지점" (값 내보내기가 본질 아님)
  - yield 이전 = `__enter__`, yield 이후 = `__exit__` (try/finally로 예외 안전)
  - 탐구 21번(yield/코루틴)의 자연스러운 후속 — yield의 제어 양보 능력 활용
- **★ 이번 step의 깔끔함 — step17 교훈 적용**:
  step17에선 정체성 원칙 4연속 위반 사태. step18은 변형 최소 (D 한 곳만 정체성 적용).
  "원칙 준수"가 잘 지켜짐 — 책 표준 패턴(A/B/C) 충실히 따르되, 우리 정체성(D) 한 곳만 명확히.
- **★ 가정/전제 추가 (step17 전제에)**:
  | 새 전제 (step18) | 의미 | 깨지면? |
  |---|---|---|
  | 전역 Config는 언제든 수정 가능 | 스레드 안전성 없음 | 멀티스레딩 시 위험 (PyTorch도 마찬가지) |
  | 역전파 안 할 땐 그래프가 필요 없다 | 추론(predict) 시 y.data만 필요 | no_grad 블록 안에서 y.backward() 호출하면 에러 |
  | retain_grad=False면 중간 grad 버려도 된다 | 최종 입력 grad만 필요 | 중간 Variable grad 접근 시 None |
- **검증**:
  - retain_grad=False (기본): y.grad=None, t.grad=None, x0.grad=2.0, x1.grad=1.0 (정답지와 일치) ✅
  - retain_grad=True: 모든 Variable grad 유지 (y=1.0, t=1.0, x0=2.0, x1=1.0) ✅
  - no_grad 블록: y.data는 나오지만 y.creator=None (그래프 안 만듦), 블록 벗어나면 자동 복구 ✅
  - (★ AGENTS.md "수정 후 재실행" 체크리스트 준수)
- **회수**: step23 → `rezero/core.py`에 Config + using_config + no_grad + fill_grad(retain_grad) 승격.
  Config는 별도 모듈(`rezero/core.py` 또는 `rezero/config.py`)로 둘지 core에 넣을지 그때 결정.

### #028 — ★ name 매개변수 키워드 전용 (`*, name=None`) (step19)
- **위치**: step19~
- **상태**: ✅ 반영 (2026-08-07)
- **종류**: 🔵 라이브러리성 ★ (API 설계 — 매개변수 전달 방식)
- **브로 결정**:
  > "name 인자의 경우 흠,.... 추후를 생각하면,.... 걍,... 키워드 인자 방식이 나을듯,...."
  → `name`을 키워드 전용(`*` 뒤)으로 둬서 `Variable(data, name='x')` 식으로만 호출 가능하게.
- **내용**:
  ```python
  # 책 원본 — 일반 매개변수 (위치/키워드 둘 다 OK)
  class Variable:
      def __init__(self, data, name=None):
          ...
  Variable(data, 'x')        # 위치 전달 허용 (애매)
  Variable(data, name='x')   # 키워드 전달

  # rezero — 키워드 전용 (★ `*` 사용)
  class Variable:
      def __init__(self, data: Optional[np.ndarray], *, name: Optional[str] = None):
          ...
  Variable(data, 'x')        # ❌ TypeError (위치 안 됨)
  Variable(data, name='x')   # ✅ 키워드만 가능
  ```
- **★ 왜 키워드 전용인가 (3가지 이유)**:
  1. **호출부 가독성** — `Variable(data, name='x')`는 `name='x'`가 눈에 보임.
     `Variable(data, 'x')`는 `'x'`가 뭔지 코드만 보면 모름. 문서 봐야 앎.
  2. **위치 인자 실수 방지** — 나중에 `__init__` 매개변수 늘어나면 헷갈림 방지.
     `Variable(data, True, 'x')` ← `True`가 뭔지 `'x'`가 뭔지 모름.
  3. **API 진화에 안전** — 키워드 전용 매개변수는 순서 바꿔도 호출 코드 안 깨짐.
- **★ step18 retain_grad와의 일관성 (패턴 관찰)**:
  step18 fill_grad에서 이미 키워드 전용 매개변수 채택:
  ```python
  def fill_grad(start_var, upstream_grad=None, *, retain_grad=False): ...
  ```
  step19 name도 같은 패턴 → 2사례 누적. **★ 하지만 아직 "원칙"은 아님** (브로 결정):
  > "키워드 전용 매개변수 원칙은,..... 흠,.... 근데,.... 이게 원칙까지 갈지는,....ㅍㅋㅋㅋ
  >  근데 뭐 나중에 코드가 진화하면서 그런 문법을 적용해도 괜춘한 부분들은 도출될 수 있을 것 같기는하네,...."
  → 관찰 수준으로 보류. "부가 속성은 키워드로" 패턴이 3~4곳 쌓이면 그때 원칙화 검토.
- **Python 3 문법 — `*` 매개변수**:
  `*` 뒤에 오는 매개변수는 반드시 키워드로만 전달. PEP 3102 (Python 3.0+).
  자주 쓰는 예: `sorted(iterable, *, key=None, reverse=False)` 도 같은 패턴.
- **검증**: `Variable(data, name='x')` 정상, `Variable(data, 'x')` TypeError ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 name 키워드 전용 유지.

### #029 — ★ property/`__len__` data=None 가드 (방어막 일관성) (step19)
- **위치**: step19~
- **상태**: ✅ 반영 (2026-08-07)
- **종류**: 🔵 라이브러리성 ★ (검증/방어막 — step09 방어막 3겹 연장)
- **브로 결정**:
  > "프라퍼티 가드는 '방어막 일관성'이 있게 이전 세션의 코드처럼 진행을 해주는게 좋을 듯,...."
  → 책 원본은 `__repr__`만 None 처리. 우리는 property/len에도 None 가드 넣어 일관성 확보.
- **내용**:
  책 원본 step19.py는 `__repr__`에서만 `if self.data is None: return 'variable(None)'`.
  `shape`/`ndim`/`size`/`dtype`/`__len__`은 가드 없이 `self.data.shape` 직접 접근.
  → `data=None`인 Variable에서 `x.shape` 호출하면 ndarray가 아니라 NoneType이라 애매한 에러.
  rezero는 `_ensure_data()` 헬퍼로 모두 가드:
  ```python
  def _ensure_data(self) -> np.ndarray:
      if self.data is None:
          raise RuntimeError(
              f"{self!r}의 data가 None입니다 — data에 접근하는 연산(shape/len/dtype 등)을 수행할 수 없습니다."
          )
      return self.data

  @property
  def shape(self) -> tuple[int, ...]:
      return self._ensure_data().shape      # ★ None 가드 후 위임

  def __len__(self) -> int:
      return len(self._ensure_data())       # ★ 마찬가지
  ```
- **★ 방어막 일관성 원칙 (step09 방어막 3겹 연장)**:
  step09에서 "as_array + wrapper + isinstance" 방어막 3겹 도입. 이후 step들에서 일관되게:
  - Function.backward: `assert self.inputs is not None`
  - fill_grad: `if start_var.creator is None: raise RuntimeError` (항목 016)
  - weakref 역참조: `if output is None: raise RuntimeError`
  - 이번: property/len도 같은 결 — data가 None이면 명확한 RuntimeError.
  → 핵심: **None이 될 수 있는 속성에 접근할 땐 항상 가드**. 케이스별로 뒀다 안 뒀다 하면 안 됨.
- **★ RuntimeError 메시지 구조 (항목 016 친절 에러 메시지 패턴 준수)**:
  - "무슨 문제인지" (data가 None)
  - "무엇을 하려 했는지" (shape/len/dtype 등 연산)
  - f-string의 `{self!r}`로 Variable repr → `Variable(None)`으로 자연스럽게 식별 가능
- **★ `__repr__`은 헬퍼 안 쓰는 비대칭 (자연스러움)**:
  repr은 "데이터가 없다"는 상태 자체를 표현해야 함 → `'Variable(None)'`으로 출력.
  property/len은 "데이터에 접근"이 목적이라 None이면 에러.
  → 역할이 달라서 비대칭이 자연스러움 (repr=표현, property=접근).
- **★ `_ensure_data` 네이밍** (브로 & AI 합의):
  "ensure" = "보장하다" — 이 연산을 하려면 data가 있음을 보장해야 한다. 가드 역할에 정확.
  ★ 후보 검토 토론 (브로가 "무난한 거 맞냐?" 재질문 → 재검토):
  | 후보 | 평가 |
  |---|---|
  | `_require_data` | "요구하다" — 동작은 맞으나 require가 강한 뉘앙스. data 타입 인코딩 느낌 |
  | `_data_or_raise` | 동작 정확히 서술하나 verbose |
  | `_check_data` | "체크"가 뭘 하는지 애매 (에러? 반환?) |
  | `_ensure_data` ★ | "보장한다" — data 있음을 보장. require보다 가드 역할에 정확. 브로 & AI 합의 |
  | `_get_data` | 일반 getter처럼 보여 "없으면 에러"가 안 드러남 |
  | `_validated_data` | 일회성인데 과거분사 `-ed` 어색 |
  → `_ensure_` 접두사는 다른 곳에서도 재사용 가능한 패턴 (예: `_ensure_grad()`).
- **검증**:
  - 정상 데이터: `x.shape=(2,3)`, `x.ndim=2`, `x.size=6`, `len(x)=2` ✅
  - data=None: repr → `'Variable(None)'` ✅, `x.shape` → RuntimeError ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 `_ensure_data` 헬퍼와 가드 함께 유지.

### #030 — ★ `__repr__` 소문자 → 대문자 (`'variable(' → 'Variable('`) (step19)
- **위치**: step19
- **상태**: ✅ 반영 (2026-08-07)
- **종류**: 🟢 step 한정 ★ (사소하지만 브로 결정에 따른 변형, 학습 흔적 기록)
- **브로 결정**:
  AI: "repr이 `variable(...)` (소문자)로 표시되는데, 브로 느낌엔 어때? (a) Variable(...) 클래스명 그대로 / (b) variable(...) 책 방식"
  브로: "'Variable(...) 로 클래스명 그대로 표시'하는 것으로 하자,...."
  → 클래스명(`Variable`)과 repr 출력(`Variable(...)`)을 일치시키는 게 자연스럽고 혼란이 적음.
- **내용**:
  ```python
  # 책 원본 — 소문자 'variable(' 하드코딩 (클래스명 Variable과 불일치)
  def __repr__(self):
      p = str(self.data).replace('\n', '\n' + ' ' * 9)
      return 'variable(' + p + ')'

  # rezero — 클래스명 그대로 'Variable(' 사용
  def __repr__(self) -> str:
      p = str(self.data).replace('\n', '\n' + ' ' * 9)
      return 'Variable(' + p + ')'
  ```
- **★ 왜 책은 소문자인가 (추측)**:
  책 원본의 dezero 최종 버전(`dezero/core.py:80`)도 `'variable(' + p + ')'` 소문자 사용.
  PyTorch의 `repr(tensor)`는 클래스명 안 나옴 (`tensor([...])` 로 표시).
  chainer (DeZero의 레퍼런스) 는 `variable(...)` 소문자 — 책이 chainer 관례를 따랐을 가능성.
  즉 생태계/관례를 따른 선택. rezero는 학습용이라 **"클래스명 일치" 우선**.
- **★ 우연의 일치 — 들여쓰기 숫자 안 바뀜**:
  `'variable('`도 9글자, `'Variable('`도 9글자라서 들여쓰기 숫자(`' ' * 9`)는 그대로.
  우연이지만, 만약 `MyVar` 같은 짧은 클래스명이었다면 숫자도 바뀌어야 했을 것.
  → 이 디테일이 문서화 가치 있는 이유: "들여쓰기 매직 넘버가 클래스명 길이에 의존한다"는 사실 기록.
- **★ data=None 케이스 일관성 (항목 029 헬퍼 에러 메시지와 시너지)**:
  `__repr__`에서 `'Variable(None)'` 반환 → 항목 029 `_ensure_data` 에러 메시지의 `{self!r}`가
  자동으로 `Variable(None)`로 표시 → "이 Variable의 data가 None" 즉시 식별 가능.
  대소문자 통일한 덕분에 repr과 에러 메시지가 일관되게 연결됨.
- **검증**:
  - `repr(Variable(np.array([1,2,3])))` → `'Variable([1 2 3])'` ✅
  - `repr(Variable(None))` → `'Variable(None)'` ✅
  - 들여쓰기 9칸 정답지와 동일 (대소문자만 다름) ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 `Variable(` 대문자 유지.
  단, 최종 dezero와 출력이 달라지는 점 인식 필요 (학습용 변형 명시).

### #031 — ★★ `__add__`/`__mul__` 클래스 안 정의 (책은 클래스 밖 대입) (step20)
- **위치**: step20~
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★★ (클래스 설계 — 정적 분석 호환성)
- **내용**:
  책 원본 step20은 `Variable.__add__ = add` 식으로 **클래스 정의 밖에서** 매직메서드 대입.
  rezero는 **클래스 안에 정의** (일반적/권장 방식):
  ```python
  # 책 (클래스 밖 대입 — 비권장)
  class Variable: ...
  def add(x0, x1): ...
  Variable.__add__ = add      # 클래스 정의 밖에서 속성 대입

  # rezero (클래스 안 정의 — 권장)
  class Variable:
      def __add__(self, other: "Variable") -> "Variable":
          return add(self, other)
  ```
- **★ 핵심 — 왜 클래스 안이 원칙인가 (4가지 이유)**:
  1. **정적 분석 호환성** ★ — pyright/Pylance/mypy는 클래스 정의를 정적으로 분석. 클래스 밖 대입은 인식 못 함.
  2. **가독성** — "이 클래스가 지원하는 연산자"를 클래스 정의만 보고 파악 가능.
  3. **서브클래싱** — `super().__add__()` 패턴이 자연스러움.
  4. **관행** — NumPy/PyTorch/pandas 등 파이썬 생태계 표준.
- **★ step20 실증 — pyright 11 에러 (클래스 밖 대입의 치명적 단점)**:
  1차 코드에서 책 원본 방식(`Variable.__add__ = add`)을 그대로 따랐더니 **pyright 11 에러** 발생:
  ```
  Attribute "__add__" is unknown (reportAttributeAccessIssue)
  Operator "*" not supported for types "Variable" and "Variable" (reportOperatorIssue)
  ```
  → 클래스 밖 대입은 pyright가 "Variable에 __add__ 없다"고 판단 → `a * b`를 에러로 봄.
  → 11곳에 `# type: ignore` 달아야 하는데, 이건 rezero 원칙("정적 분석과 협력")에 정면 위반.
  **해결**: 클래스 안 정의로 전환 → pyright **0 errors**.
- **★ 브로 결정 흐름 (초기 → 실증 → 확정)**:
  - 초기: "간단한 경우 책 방식(클래스 밖 대입)으로 가자. 보통은 내부에 넣는다는 설명 OK"
  - 실증: pyright 11 에러 폭발 → "비추라는 소리군, 공식 가이드란 소리잖아? 괜히 깰 필요 없겠지"
  - 확정: "1. 본체 클래스 안쪽에 정의 / 2. 밖 정의 방법도 존재한다는 기록 / 3. 작업 원칙 추가"
  → 코드 짜보고 나서야 가시화된 트레이드오프. "원칙 수립 ≠ 원칙 준수"의 또 다른 사례.
- **★ 부산물 1 — coding_style.md 섹션 7 신설** (영구 보존):
  "매직메서드는 클래스 안에 정의 — 클래스 밖 대입 비권장" 작업 원칙 문서화.
  4가지 이유 + step20 실증(pyright 11 에러) + 책이 밖 대입 택한 가설.
- **★ 부산물 2 — AGENTS.md 작업 원칙 추가** (모든 세션 적용):
  "★ 매직메서드는 클래스 안에 정의 (필수)" — 빈 줄 자동 적용과 같은 형식.
  향후 모든 AI 세션이 매직메서드 작성 시 자동 클래스 안 정의.
- **★ 부산물 3 — 교훈**: "책 원본이 택한 방식이 항상 권장 방식은 아니다" (AGENTS.md 배경에 명시).
  책은 설명/저자 스타일 목적으로 클래스 밖 대입 택했으나, 실용적으론 클래스 안이 압도적.
- **검증**:
  - 실행: `y = a * b + c` → `y=7.0, a.grad=2.0, b.grad=3.0, c.grad=1.0` ✅
  - pyright: 11 errors (클래스 밖) → 0 errors (클래스 안) ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 __add__/__mul__ 클래스 안 정의 유지.
  ★ 모든 후속 매직메서드(__neg__, __sub__ 등 step22)도 클래스 안 정의로 진행.

### #032 — ★ Mul derivative hook 확장 (항목 013 재평가 통과 — 다른 입력값 의존) (step20)
- **위치**: step20~
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★ (항목 013 재평가 — derivative hook 유효 범위 확인)
- **내용**:
  step07에서 도입한 derivative hook (항목 013)의 "최종 반영 여부 보류"를 **첫 테스트 케이스에서 통과**.
  Mul은 Add와 달리 편도함수가 "다른 입력값"에 의존 → derivative hook으로 표현 가능한지가 관건.
  ```python
  class Mul(Function):
      def derivative(self) -> tuple[Callable, ...]:
          # ★ Add는 (lambda _: 1, lambda _: 1) — 상수 (입력 무시)
          # ★ Mul은 (lambda _: x1, lambda _: x0) — 다른 입력값 캡처
          assert self.inputs is not None    # 정적 분석용 타입 좁히기
          x0 = self.inputs[0].data
          x1 = self.inputs[1].data
          return (lambda _: x1, lambda _: x0)
  ```
- **★ 핵심 — Add에서 Mul로의 자연스러운 확장**:
  | 함수 | 편도함수 | derivative() 표현 | 입력값 의존? |
  |---|---|---|---|
  | Add | ∂y/∂x0 = 1, ∂y/∂x1 = 1 | `(lambda _: 1, lambda _: 1)` | X (상수) |
  | Mul | ∂y/∂x0 = x1, ∂y/∂x1 = x0 | `(lambda _: x1, lambda _: x0)` | O (다른 입력값) |
  → Add의 "상수함수" 통찰(브로, step13)이 Mul로 자연스럽게 확장.
  핵심: 편도함수값이 derivative() **호출 시점**에 이미 고정되므로 상수함수(lambda _: x1)로 표현 가능.
- **★ 항목 013 "최종 반영 여부 보류" 재평가**:
  step07에서 "step13/step34 진입 시점에서 재평가"로 보류했던 조건:
  - step13 (다변 입력): ✅ 통과 (Add 편도함수 = 상수)
  - step20 (Mul, 다른 입력값 의존): ✅ 통과 (이 항목)
  - step34+ (행렬 미분, 야코비안 전치 곱): ⏳ 미래 화두 — derivative hook 붕괴 예상
  → 현재(step20)까지 derivative hook은 유효. step34+에서 backward 직접 오버라이드로 전환 예상.
- **★ `assert self.inputs is not None` (정적 분석용 타입 좁히기)**:
  부모 Function.backward()에서 같은 가드가 있어 **런타임엔 중복**이지만,
  pyright가 Mul.derivative() 안에서 self.inputs가 Optional임을 좁히려면 이 지점에서 다시 가드 필요.
  Square/Add.derivative()엔 없음 (self.inputs 안 참조하므로).
  → "self.inputs를 참조하는 derivative에만 가드" 패턴으로 일관.
- **검증**:
  - `y = a * b` (a=3, b=2) → `y=6.0, a.grad=2.0(=b), b.grad=3.0(=a)` ✅
  - pyright: 0 errors (assert 추가로 타입 좁히기 해결) ✅
- **회수**: step23 → `rezero/core.py` Function + `functions.py` Mul 승격 시 derivative hook 유지.

### #033 — ★★★ `__array_priority__ = 200` 버림 (탐구 25번 — "책 코드도 검증하라") (step21)
- **위치**: step21
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★★★ (메커니즘 이해 + 매직 넘버 제거 — 이번 step 최대 성과)
- **브로 트리거**:
  > "200이란 매직스러운 숫자값의 의미도 잘 모르겠고, 어떻게 저렇게 돼는 것인지에 대한 설명이 전혀없으니"
  > "200을 사용하는 부분이 뭔가 굉장히 부자연스럽게 느껴지기도"
  → 브로 직감("찜찜함")이 파낸 진실: **200은 과거 NumPy 핵, 현대엔 불필요**.
- **내용**:
  책 원본 step21은 `class Variable: __array_priority__ = 200`을 클래스 속성으로 둠.
  "ndarray와 연산 시 Variable이 우선"을 보장하는 NumPy 특수 메커니즘.
  rezero는 **이 줄을 버림** — 현대 NumPy에선 `__rmul__`만으로 충분함을 실험으로 증명.
  ```python
  # 책 (과거 NumPy 핵)
  class Variable:
      __array_priority__ = 200    # ← rezero는 버림

  # rezero (현대 NumPy — __rmul__만으로 충분)
  class Variable:
      def __rmul__(self, other): return mul(self, other)
  ```
- **★ 세 가지 메커니즘 역사적 계층** (탐구 25번에서 깊이):
  | 세대 | 메커니즘 | 시대 | 역할 |
  |---|---|---|---|
  | 1세대 | `__rmul__`/`__radd__` (Python 표준) | 파이썬 태초 | 좌변이 NotImplemented 반환 → 역순 |
  | 2세대 | `__array_priority__` | NumPy 고대 (~2017) | 과거 NumPy가 NotImplemented 안 반환해서 필요했던 핵 |
  | 3세대 | `__array_ufunc__` (NEP 13, 2017) | 현대 | ufunc 통째로 가로채기. PyTorch/JAX 사용 |
- **★ 핵심 — 왜 불필요해졌나**:
  과거 NumPy는 다른 타입을 만나도 NotImplemented를 안 반환하고 무식하게 삼킴 → `__rmul__` 안 불림.
  `__array_priority__`는 "NumPy야, 다른 타입 만나면 일단 내비둬"라는 협상 카드.
  ★ 현대 NumPy는 표준 디스패치 존중 → `__rmul__` 정상 호출 → priority 불필요.
  참고: [NumPy issue 27348](https://github.com/numpy/numpy/issues/27348) — 최신 NumPy의 NotImplemented 처리 개선 이력.
- **★ 실험으로 증명** (3케이스 비교):
  | 케이스 | `ndarray * obj` 결과 | 의미 |
  |---|---|---|
  | NaiveVar (`__rmul__`만, priority 없음) | **NaiveVar 유지** ✅ | 현대에선 `__rmul__`만으로 충분 |
  | PriorityOnly (priority=200만, `__rmul__` 없음) | TypeError | priority만 있다고 역순 안 불림 |
  | UfuncTest (`__array_ufunc__` 정의) | ufunc 가로채짐 | 3세대 정상 동작 |
- **★ step21 데모 케이스 4로 코드 실증**:
  `np.array(3.0) * x` (`__array_priority__` 없이) → `Variable(6.0)` 정상 동작. ★ 탐구 25번 결론을 코드로 확인.
- **★★★ 핵심 교훈 — "책 코드도 검증하라"**:
  1. 매직 넘버를 이유 없이 쓰지 말 것 — "왜 200이지?" 의심 → 학습 시작.
  2. 책/교과서도 시대 지나면 구식 — `__array_priority__`는 과거엔 필수, 현대엔 불필요.
  3. "왜?" 묻는 습관이 코드 투명하게 만듦 — 브로 "찜찜함" → 실험 → 가설 틀림 인정 → NEP 13 조사 → 진실 파악.
- **★ AI 가설 틀림 인정 (성실 보고 원칙)**:
  AI가 처음에 "NumPy가 Variable을 무식하게 삼킨다"고 설명했으나 실험 1로 틀림 증명.
  → 솔직히 인정하고 재조사 → 진짜 원인(과거 NotImplemented 미반환) 파악. (AGENTS.md "보고 성실성" 원칙 실증)
- **검증**: 데모 6 케이스 전부 `__array_priority__` 없이 정상 동작 + pyright 0 errors ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시 `__array_priority__` **포함 안 함**.
  ★ 단, 구버전 NumPy 환경에서 rezero를 돌린다면 이 속성이 다시 필요할 수 있음 (탐구 25번에 명시).

### #034 — ★ `__radd__`/`__rmul__` 클래스 안 정의 + wrapper as_array 중복 제거 (step21)
- **위치**: step21~
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★ (step20 작업 원칙 첫 자동 적용 + 점진적 설계 잔재 정리)
- **내용 (두 가지 결합)**:

  **(A) `__radd__`/`__rmul__` 클래스 안 정의** — step20 항목 031 작업 원칙 자동 적용:
  ```python
  # 책 (클래스 밖 대입 — 비권장)
  Variable.__radd__ = add
  Variable.__rmul__ = mul

  # rezero (클래스 안 정의 — 권장, pyright 0 에러)
  class Variable:
      def __radd__(self, other): return add(self, other)
      def __rmul__(self, other): return mul(self, other)
  ```
  ★ step20에서 만든 AGENTS.md 작업 원칙("★ 매직메서드는 클래스 안에 정의 (필수)")이
    step21에서 자동으로 적용된 첫 사례. "원칙 수립 ≠ 원칙 준수"에서 드디어 **준수** 단계.

  **(B) wrapper의 as_array 중복 제거**:
  ```python
  # 책 원본 (step20까지의 잔재 — step21에서 정리 누락)
  def add(x0, x1):
      x1 = as_array(x1)    # ★ Function.__call__의 as_variable과 중복
      return Add()(x0, x1)

  # rezero (중복 제거)
  def add(x0, x1):
      result = Add()(x0, x1)   # x1 변환은 Function.__call__ 도입부 as_variable이 처리
      assert isinstance(result, Variable)
      return result
  ```
- **★ 핵심 — 점진적 설계의 잔재를 우리가 정리**:
  책 전체가 60 step에 걸쳐 조금씩 기능 추가하는 점진적 설계 방식.
  장점: 독자가 변화 추적 쉬움. 단점: **리팩터링이 불완전해질 수 있음**.
  step21에서 as_variable이 Function.__call__ 도입부로 올라갔을 때,
  작성자는 기존 wrapper의 as_array를 정리하지 않음 (변환 책임 이동 미인식이나 안전망 의도).
  rezero는 "중복 제거 > 혼란 방지" 원칙(브로)으로 제거.
- **★ 브로 통찰 — 책의 서사 구조 짚기**:
  > 브로: "책은 불편한 함수 직접 호출 방식과 연산자 오버로딩 방식을 혼합해서 보여준다"
  → 이 서사 때문에 "wrapper도 보호해야 할 것 같다"고 착각하기 쉬움.
  실험으로 증명: 어느 방식으로 호출해도 Function.__call__ 도입부가 처리 → wrapper 중복.
- **★ 실험으로 검증**:
  | 케이스 | wrapper as_array 있을 때 | 없을 때 |
  |---|---|---|
  | `add(x, 3.0)` (wrapper 직접 호출) | 정상 | ★ 정상 (Function.__call__ 처리) |
  | `add(x, np.float64(3.0))` | 정상 | ★ 정상 |
- **검증**: 데모 6 케이스 전부 wrapper as_array 없이 정상 동작 + pyright 0 errors ✅
- **회수**: step23 → `rezero/core.py`/`functions.py` 승격 시:
  - `__radd__`/`__rmul__`은 Variable 클래스 안 정의 유지
  - wrapper(`add`/`mul`)는 as_array 없이 단순한 형태 유지

### #035 — ★★ 3원칙 자동 적용 검증 + Pow super().__init__ DRY + Neg 단순화 (step22)
- **위치**: step22~
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★★ (메타 — 원칙 준수 사이클 검증 + DRY + 브로드캐스팅)
- **내용 (3가지 결합)**:

  **(A) ★★★ 3원칙 자동 적용 검증** — step20/21에서 확립한 원칙들이 대량 적용:
  | 원칙 | 확립 step | step22 적용 |
  |---|---|---|
  | 항목 031: 매직메서드 클래스 안 정의 | step20 | ★ 7개 매직메서드 전부 클래스 안 |
  | 항목 033: `__array_priority__` 버림 | step21 (탐구 25) | ★ 안 넣음 |
  | 항목 034: wrapper as_array 제거 | step21 | ★ wrapper는 단순하게 |

  ★ 핵심 가치 — "원칙 수립 ≠ 원칙 준수"에서 드디어 **대량 준수** 단계:
  - step15~18: 브로가 4연속 원칙 위반 캐치 (AGENTS.md 학습 시 반복 실수 방지 배경)
  - step20: 항목 031 확립 (pyright 11 에러 실증)
  - step21: 항목 031 첫 자동 적용 (`__radd__`/`__rmul__` 2개)
  - step22: 항목 031 대량 적용 (7개 매직메서드) + 033/034도 자동
  → 사전에 세운 원칙이 시스템으로 작동함을 증명. AGENTS.md "사전 의무 체크리스트"의 가치 실증.

  **(B) Pow `super().__init__()` 호출 (DRY)** — 브로 리뷰에서 파생:
  ```python
  # 브로 지적: ".c 설정 외엔 Function init과 중복 아닌가? 베이스 호출하라"
  # Before (중복)
  class Pow(Function):
      def __init__(self, c):
          self.c = c
          self.inputs = None       # ← 부모와 중복
          self.output = None       # ← 중복
          self.generation = 0      # ← 중복

  # After (DRY)
  class Pow(Function):
      def __init__(self, c):
          self.c = c               # 커스텀 — c만 이 클래스에서
          super().__init__()       # inputs/output/generation은 부모가
  ```
  ★ "커스텀은 c만, 나머지는 베이스가" — 부모-자식 역할 분담 원칙 (브로).

  **(C) Neg derivative 단순화 (브로드캐스팅에 위임)** — 브로 리뷰에서 파생:
  ```python
  # 브로 지적: "자동 브로드캐스팅 되면 코드 단순화가 좋겠지"
  # Before (과잉 브랜치)
  return lambda x: np.array(-1.0) if np.isscalar(x) or x.ndim == 0 else -np.ones_like(x)

  # After (NumPy 브로드캐스팅에 위임)
  return lambda x: np.float64(-1.0) * x
  ```
  ★ 핵심 — NumPy 브로드캐스팅이 스칼라/배열 관계없이 알아서 처리.
  실험으로 검증: 스칼라/1d/2d 입력 전부 동일 결과.
  ★ pyright 시그니처 엄격성 때문에 `np.float64(-1.0) * x` 형태 (단순 `-1`은 int로 추론돼 에러).

- **★ 부수 발견 — pyright 시그니처 엄격성**:
  - `Callable[[ndarray], ndarray]` 단일 반환형은 **엄격** (int/float 반환 시 에러)
  - `tuple[Callable, ...]` 튜플 반환형은 **관대** (Add/Sub의 `lambda _: 1` 통과)
  - Square는 `2 * x`가 자동 float64 승격돼서 우연히 통과한 거였음
  - 향후 단일 입력 함수(Neg/Pow/Square 스타일) 작성 시 주의점
- **검증**:
  - 실행: 7 케이스 전부 기대 일치 (neg/sub/div/pow + 복합 식 + 연산자 우선순위 + 비교환 역전파)
  - pyright: 0 errors, 0 warnings ✅
- **회수**: step23 → `rezero/core.py`/`functions.py` 승격 시:
  - 4개 클래스(Neg/Sub/Div/Pow) + wrapper 7종 함께 승격
  - Pow는 `super().__init__()` DRY 패턴 유지
  - 3원칙(031/033/034)은 여기서도 자동 적용

### #036 — ★★★ 버전 폴더 전략 (v1/v2/v3) + 순환 참조 해결 + 주석 정리 기준 (step23)
- **위치**: step23~
- **상태**: ✅ 반영 (2026-08-10)
- **종류**: 🔵 라이브러리성 ★★★ (패키지 구조 전면 재설계 — rezero 프로젝트 구조의 전환점)
- **브로 제안**:
  > "이 책은 총 60스텝인데, 뒤쪽을 보면 기존 코드를 재활용이라기보다 뜯어고치는 느낌.
  >  추후에 기억이 날아간 상태로 돌아오면 아무 기억도 안 날 것 같다.
  >  현재 폴더 내 rezero 하위에 v1 같은 폴더를 더 두어, 제2고지까지의 작업 결과를 프리징하자."
  → "최종 버전" 개념을 버리고, **고지별 스코프 패키지** 유지.
- **내용 (3가지 결합)**:

  **(A) ★★★ 버전 폴더 전략 — v1/v2/v3 고지별 스냅샷**:
  ```
  rezero/
  ├── v1/              ← 제 1~2고지 (step01~22) — 스칼라 Variable + 자동 역전파
  │   ├── core.py      ← Variable, Function, Config, fill_grad, as_array, as_variable
  │   ├── functions.py ← Square/Add/Mul/Neg/Sub/Div/Pow + wrapper 9종
  │   └── __init__.py  ← re-export
  ├── v2/              ← (미래) 제 3고지 — 고차 미분
  ├── v3/              ← (미래) 제 4고지+ — 신경망
  ├── steps/           ← 학습 흔적 전부 (step01~60). 과거 step 수정 금지.
  └── tests/           ← 원본 테스트 1:1 mirror (전부 @skip)
  ```
  - 각 고지 완료 시점에 새 vN 폴더 생성 (복사 후 진화)
  - v1은 영구히 남아 언제든 import 가능 — "박제"가 아니라 **사용 가능한 패키지**
  - "v1 버전의 사용특징이 있는 문제 상황" — 고지별로 다루는 스코프가 다름 (스칼라/고차미분/신경망)
  - ★ git tag가 아니라 폴더인 이유 — 파일 시스템에서 바로 보임. 학습자가 즉시 탐색 가능.
  - 사용: `from rezero.v1 import Variable, fill_grad`

  **(B) ★★ 순환 참조 해결 — 지연 import (lazy import)**:
  - 문제: core.py의 Variable 매직메서드가 functions.py의 wrapper 호출. functions.py는 core.py import → 순환 참조.
  - 해결: 매직메서드 안에서 지연 import.
    ```python
    class Variable:
        def __add__(self, other):
            from rezero.v1.functions import add  # ★ 호출 시점에 로드
            return add(self, other)
    ```
  - ★ dezero의 해법 vs rezero의 해법:
    | | dezero | rezero |
    |---|---|---|
    | 방식 | `setup_variable()`에서 클래스 밖 대입 | 매직메서드 안에서 지연 import |
    | 배경 | 클래스 밖 대입이라 순환 참조 안 남 | 클래스 안 정의 원칙(항목 031)이라 순환 참조 발생 |
    | pyright | 클래스 밖 대입이라 인식 못 함 (항목 031 경고) | ★ 0 에러 (클래스 안이라 인식) |
  - ★ 항목 031(매직메서드 클래스 안)의 패키지화 시점 복병이었으나, 지연 import로 우아하게 해결.
  - 성능: Python 모듈 캐싱으로 최초 1회만 실행. 영향 없음.

  **(C) ★ 주석 정리 기준 (API화)**:
  - step 파일(학습 흔적)은 상세 주석. v1/ 패키지는 API라 간결.
  - 제거 대상: step 번호 참조(`step19:`), 항목 참조(`항목 014`), "브로 통찰" 서사, 탐구 노트 상세 참조.
  - 유지 대상: 핵심 아키텍처 설명(fill_grad 정체성 등), docstring.
  - 원칙: "모르면 steps/에서 뒤지기" — 학습 흔적은 steps/에 영구 보존.
- **★ 부산물 — 빈 템플릿 11개 삭제**:
  기존 rezero/core.py 등 11개 빈 파일이 헷갈림 유발. v1/이 진짜 패키지니까 과감히 삭제.
  (core.py, core_simple.py, cuda.py, dataloaders.py, datasets.py, functions.py, functions_conv.py, layers.py, models.py, optimizers.py, transforms.py, utils.py)
- **★ 회수 항목들**:
  이 step에서 대부분의 라이브러리성 항목이 v1/ 패키지로 회수됨:
  - 항목 014 (fill_grad 전역 함수) → core.py
  - 항목 031 (매직메서드 클래스 안) → core.py Variable
  - 항목 033 (__array_priority__ 버림) → core.py Variable (안 넣음으로)
  - 항목 034 (wrapper as_array 제거) → functions.py wrapper
  - 항목 035 (3원칙 자동 적용 + Pow DRY + Neg 단순화) → core.py + functions.py
- **검증**:
  - 실행: 4 케이스 전부 기대 일치 (정답지 동일 시나리오, 전 연산자, no_grad, 혼합 연산)
  - pyright: 0 errors, 0 warnings (지연 import로 순환 참조 해결 후)
  - `from rezero.v1 import Variable, fill_grad` 정상 동작
- **회수**: ★ 이 항목 자체가 "회수" 작업의 결과. v1/ 패키지가 향후 v2/v3의 기반이 됨.

---

### #037 — ★★★ 순회 제너레이터 `iter_reverse_topo` 추출 — fill_grad/fold_dot_graph 공통화 (step25 리팩터, 이슈 32번)

**카테고리**: 구조 (관심사 분리 + DRY)

**배경**:
step25에서 `fold_dot_graph`(시각화)를 구현하다가, `fill_grad`(역전파)와 **거의 동일한 worklist + visited 순회 패턴**을 사용함을 발견. 탐구 노트 20번 섹션 5에서 예측한 "step25 = 순회 일반화 계기" 회수 시그널 도달.

**변경**:
- `rezero/v1/core.py`에 `iter_reverse_topo(start_var)` 제너레이터 신설.
  - 역방향 위상 정렬 순회 (generation 내림차순, visited 중복 방지).
  - 순회 알고리즘만 담당 — 역전파 계산/grad 누적/retain_grad/output weakref 역참조는 소비자 책임.
- `fill_grad`가 `iter_reverse_topo`를 소비 (`for f in iter_reverse_topo(start_var)`).
  - 기존 `schedule` 클로저 + `while worklist` 루프 제거.
  - 역전파 계산 로직만 남음 (grad 전파, 다변 배분, retain_grad).
- `fold_dot_graph`도 같은 제너레이터 소비.
  - 기존 `fold_func` 클로저 + `while funcs` 루프 제거.
  - DOT 텍스트 누적 로직만 남음.

**vs 탐구 노트 20번 초안 (step16 시점) — 3가지 조정**:
노트 20번 섹션 4의 초안 코드를 그대로 못 쓰고, 현행 v1 안전장치와 맞추어 조정:

| # | 초안 (노트 20번) | 조정 후 (현행) | 이유 |
|---|---|---|---|
| 1 | None 가드 없음 | `start_var.creator is None`이면 빈 순회 | 역전파/시각화 소비자가 시작 전 에러 처리 |
| 2 | `if f not in visited: visited.add(f); yield f` (yield 직전) | append 시점에 visited 표시 | 중복 append 방지 (v1 패턴과 일관) |
| 3 | `f.inputs` None 가드 없음 | `assert f.inputs is not None` | pyright (정적 분석 협력 원칙) |

**결과**:
- fill_grad 본문이 단순해짐 (`schedule` 클로저 사라짐, 명시적 루프 → `for` 문).
- fold_dot_graph도 마찬가지 (`fold_func` 클로저 사라짐).
- 순회 알고리즘 변경 시 한 곳(`iter_reverse_topo`)만 고치면 됨 (DRY).

**검증**:
- 테스트 99개 전부 통과 (회귀 없음).
- Goldstein 그래프 구조 100% 동일 (노드 109개, 엣지 108개, Function 분포 Mul 17/Add 10/Pow 6/Sub 5 — 리팩터 전후 id 정규화 diff 0).
- pyright 0 errors.

**추가 결정 사항**:
- `iter_reverse_topo` 위치: `core.py` (graph.py 별도 모듈 아님). 순환 참조 회피 + 현재 알고리즘 1개뿐이라 YAGNI. 미래에 순회 알고리즘 여러 개 생기면 그때 graph.py로 분리 (지연 import 한 줄로 순환 참조 해결 가능).
- re-export 안 함 (공개 API 아님). `from rezero.v1.core import iter_reverse_topo` 풀 경로로만 접근. 추후 성숙 후 결정.

**관련**:
- 이슈 32번 (본 리팩터 추적 — 이것으로 회수 완료)
- 이슈 33번 (fold 스냅샷 아이디어 — 본 제너레이터 위에서 자연스럽게 구현 가능)
- 탐구 노트 20번 섹션 4/5/9 (설계 + 회수)
- 탐구 노트 21번 (yield/제너레이터 심화)

### #038 — ★★★ v2 브랜칭 + grad의 Variable화 + common 모듈 (step32 — 고차 미분(구현 편))

**배경**:
- step31 이론 (double backprop — 탐구 노트 30)의 구현 단계.
- grad ndarray→Variable은 API 호환성이 깨지는 대개편 (`x.grad` → `x.grad.data`).
- ★ 브로 논리로 결정: "A안(v1 안 수정)이어도 함수 클래스 전부 수정해야 하는 구조라면
  스냅샷을 남기는 쪽이 합리적" → v2 브랜칭. 책의 core_simple/core 이분법과 평행
  ("고차 미분 전(v1)/후(v2)" 나란히 보존).

**내용**:

1. `rezero/v2/` 신설 — v1 전체 복사 후 step32 구현:
   - `Variable.grad`: `Optional[np.ndarray]` → `Optional["Variable"]`
     (미분 결과가 "값"에서 "식"으로 — 재미분 가능 = 기억 상실 해소)
   - `fill_grad(..., create_graph=False)` 파라미터 추가:
     - 시작 grad를 `Variable(np.ones_like(...))`로 — 상수 1도 그래프의 리프
     - backward 호출 + grad 누적을 `with using_config('enable_backprop', create_graph):`
       로 래핑 — ★ 새 메커니즘 0, step18 Config 스위치의 재활용 (탐구 노트 30의
       "기존 설계를 backward에도 일관 적용"이 코드로 증명된 지점)
   - `derivative` hook 시그니처: `Callable[[ndarray], ndarray]` →
     `type DerivativeFn = Callable[[Variable], Variable | float]`
     (본문 코드는 거의 그대로 — 연산자 오버로딩이 ndarray→Variable 자동 전환.
     `2 * x`가 `x.__rmul__` → `mul()` 호출)
   - Mul/Div derivative: `self.inputs[i].data` → `self.inputs[i]` (Variable 그대로
     꺼내기 — ★ gx가 그래프를 가지느냐의 분기점. ndarray 꺼내면 연결 상실)
   - Neg: `np.float64(-1.0)` 제거 → `-1.0` (float * Variable → `__rmul__`)
   - Sin derivative: `np.cos(x)` → `cos(x)` — ★ **Cos 클래스 + wrapper 신규**
     (sin의 2차 미분 -sin 경로. np.cos이면 ndarray 세계로 추락)
2. `rezero/common/` 신설 — numerical_diff 이관:
   - ★ 판별 기준 (브로 합의): "grad 타입/그래프 구조에 의존하는가?"
     — 무관 → common / 의존 → 각 vX 소유 (시각화는 vX 소유)
   - `type(x)(...)` + `Protocol`(VariableLike)로 common이 특정 버전을
     import하지 않음 — 진짜 공통 (v1/v2 어느 Variable에도 동작)
   - v1/v2 utils는 common을 re-export (API 하위 호환 유지)
3. ★ 구조 생존 원칙: apply/derivative hook + fill_grad 전역 함수 +
   iter_reverse_topo 순회 **100% 생존** — 바뀐 건 "흐르는 데이터의 타입"뿐.
   (v2는 rezero 정체성을 유지하며 고차 미분을 얻음)

**검증**:
- v1 105 + v2 114 = **219 passed** (v2 = 복제 105 + double backprop 신규 9)
- 데모 5종 (steps/step32.py): y=x² → f''(2)=2 / y=x⁴ → f'''(2)=48 (3층) /
  sin → y''=-sin(1) (Cos 경유) / 기본 lean (gx.creator=None) /
  dezero 대조 (`variable(2.0)` = `Variable(2.0)`)
- step27 스모크 → ★ 브로 요청으로 **step01~32 전수 실행 점검 OK**로 확대
  (v1 수정 파급 전수 확인 — common 전환으로 기존 step 파일 전부 무사)

**시행착오 (재발 방지)**:
- v2 복사 시 core.py의 **매직메서드 지연 import 10곳이 v1.functions를 그대로
  참조** → v2 Variable이 v1 연산을 타서 77 failed. ★ 복사 브랜칭 시 지연 import
  전수 확인 필수 (grep "from rezero.v1").
- 테스트 일괄 변환(sed)은 isclose/산술/`allclose(x.grad, y.grad)` 중첩 패턴을
  놓치기 쉬움 — 변환 후 **전수 grep** `.grad[^.]`으로 잔여 확인 필수.

### #039 — ★★★ Tanh + Config.reuse_output — 도함수 구현 2전략 (step35 — 고차 미분 계산 그래프)

**배경**:
- step35에서 tanh' = 1−tanh² (자기 참조 도함수) 구현 — 미분 반복 시 그래프 지수 폭증
  (Tanh 2→4→8→... / Function ≈3배) 실증. dezero는 backward에서 forward 출력 y를
  재사용 (`self.outputs[0]()`)해 Tanh 1개 유지 — 구현 방식이 그래프 운명을 가름.

**내용**:
1. `Tanh` 신규 (v2) — 기본 전략은 **재호출형**: `lambda x: 1 - tanh(x) ** 2`.
   도함수 식이 그래프에 self-contained로 명시 (교재적 가치).
2. ★ 브로 발견 — "rezero에도 self.output이 있는데 왜 안 써?": 클로저 캡처로
   재사용형 가능 (`y = self.output(); return lambda _: 1 - y * y`) —
   실증: Tanh 1개 유지 (2→4→8 vs 1→1→1). 안 쓴 건 불가가 아니라 관습
   (hook은 "입력의 순수 함수" 관습 + v1 도함수가 전부 입력형).
3. ★ 설계 변천 (브로 주도): 인스턴스 옵션 `Tanh(reuse_output=...)` 제안 →
   "wrapper 시그니처 오염, Config는?" 재제안 → **`Config.reuse_output` 전역 스위치**
   채택 (step18 철학 "역전파 동작 전환은 Config 스위치"와 일관).
4. ★ 시점 디테일: derivative는 **역전파 중 호출** — `using_config('reuse_output', True)`
   블록이 **fill_grad를 감싸야** 효과 (순전파 시점 아님).
5. 단독 사용성 차이: 재호출형만 `Tanh().derivative()`로 f'를 일급 객체로 획득
   (항목 013의 완성형). 재사용형은 self.output 의존 — 순전파 없이 존재 불가.

**검증**:
- 227 passed (Tanh 5종: 순전파/gradient check/2차/전략 수치 동일/그래프 1개 유지)
- pyright 0 errors / 그래프 10장 (재호출·재사용 각 1~5차)
- 파일 크기 관찰: gx5 2740KB vs gx5_reuse 2330KB — 폭증의 주 범인은 Tanh보다
  mul/sub 구조 복제 (Function ≈3배 > Tanh 2배)

**관련**:
- 이슈 41번 / 탐구 노트 32 (미분식 해부 — 총정리) / 후보 8번 회수 (큐 첫 완주)
- 항목 013 (derivative callable — 일급 도함수), 027 (Config 철학), 038 (v2 브랜칭)

---

### #040 — ★ v1/v2 리뷰 보류 항목 기록 — utils 복제(C1) + wrapper 반복(C2) (이슈 43 작업 4-C)

> 2026-08-28 등록 (브로 승인 후). 이슈 43 작업 4 (v1/v2 리뷰)에서 **검토했으나 보류** 결정된
> 2건의 기록 — 나중에 재검토할 수 있게 판정 이유를 남김. 코드 변경 없음.

**C1 — v1/v2 `utils.py` 232줄 완전 복제**:

- `diff` 결과: 차이는 import 경로 (`rezero.v1` ↔ `rezero.v2`)와 docstring 첫 줄뿐,
  코드 본문 100% 동일 (시각화 파이프라인 전체)
- 순수 부분(`_format_value`, 포맷 검증)만 common 이관 가능하나 이득 ~40줄
- ★ 보류 사유: "그래프 구조 의존 시 vX 소유" 판별 기준과 충돌 — `_dot_var`/`_dot_func`/
  `fold_dot_graph`는 Variable/iter_reverse_topo에 의존하므로 vX 소유가 맞음.
  부분 이관은 파이프라인 분리로 복잡도 증가 > 40줄 절약.

**C2 — wrapper 9종 동일 패턴 반복**:

```python
def square(x):
    result = Square()(x)
    assert isinstance(result, Variable), "..."
    return result
```

- 팩토리/데코레이터로 압축 가능하나 **명시성 손해** — 각 wrapper가 6줄이지만
  읽는 사람에게 "무슨 일을 하는지" 바로 보이는 것이 학습 프로젝트에서 우선.
- dezero도 같은 패턴 (책 관례 유지).

**관련**:
- 이슈 43 작업 4 (v1/v2 리뷰 — A1~A3, B1, D1은 완료. C만 이 기록으로 종결)
- [이슈 46](https://github.com/ghjang/deep-learning-from-scratch-3/issues/46) — Variable 던더 믹스인 분리 (같은 리뷰에서 파생된 후속 제안)

---

### #041 — ★ backprop 별칭 추가 — fill_grad의 업계 표준 이름 진입점 (이슈 49)

> 2026-08-31 등록 (브로 제안+승인). 이슈 49 "fill_grad 함수명 재검토"의 결론 —
> 전면 개명 대신 **별칭 전략**: `backprop`을 표준 이름으로 추가하고
> fill_grad(항목 015)는 공존하는 정식 이름으로 유지. v1/v2 양쪽에 추가.

**배경**:

- 노트 36 §10 네이밍 성찰에서 후보 5종 재검토 → 브로 판단: "fold_grad 계열 이름이
  틀린 건 아니나, 역전파 연산임이 코드에서 즉시 드러나지 않는다"
- 전면 개명은 과거 step·v1/v2 코드·노트 전부를 깨는 과잉 (과거 step 수정 금지 원칙과
  충돌) — 두 관점(FP적 fold vs 연산적 backprop)이 다 생존하는 별칭이 실용주의 최적해

**변경**:

- `rezero/v1/core.py`·`rezero/v2/core.py` — `backprop()` 포워딩 함수 추가
  (구현은 fill_grad에 위임, 자기 docstring 보유 — v2는 create_graph 전달)
- `v1/__init__.py`·`v2/__init__.py` — re-export + `__all__`
- `v1/tests/test_backprop_alias.py`·`v2/tests/test_backprop_alias.py` —
  동일 grad 생산 + upstream_grad 전달 + v2 create_graph(double backprop) 경로 검증

**결과**: pytest v1+v2 **241 passed** / `uvx pyright rezero/` **0 errors**

**이후 코드 규칙**: 새 코드는 `backprop` 권장(발견성) — 단 `fill_grad`는 폐기 대상이
아니라 **공존하는 정식 이름** (FP적 fill/fold 관점을 강조할 땐 그대로 정당한 선택)

**관련**: [이슈 49](https://github.com/ghjang/deep-learning-from-scratch-3/issues/49) /
항목 015 (fill_grad 최초 채택, step08) / 노트 36 §10 (네이밍 성찰)

---

> 생각나는 대로 한 줄씩. 구체화되면 위 항목으로 승격.

- (아직 없음 — 떠오르는 대로 추가)

---

## 🔗 관련 링크

- `AGENTS.md` — rezero 학습 원칙 (dezero 복붙 금지, 변형 실험 환영)
- `LEARNING_NOTES.md` — step별 핵심 통찰 (변형 결정 기록도 여기)
- `notes/exploration_09_abc_abstract.md` — abc vs NotImplementedError 심화 (#003, #004 관련)
- `notes/exploration_13_derivative_notation.md` §8 — gy/gx + fold 통찰 (#007 관련)
- 책 step23 — `dezero/` 패키지화 (회수 시점의 원본 참고)
