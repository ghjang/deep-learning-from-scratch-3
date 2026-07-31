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

> ★ 2026-07-31 그룹화 — 27개 항목 쌓여 주제별 색인 추가 (step23 회수 전 정리).
> 항목 자체는 append-only 정책 존중 — **번호순 물리 배치 유지 + 이 표로 그룹 탐색**.
> 한 항목이 여러 그룹에 걸칠 수 있으나 "주된 결" 하나로 분류. 상세는 각 항목 본문 참조.

### 항목 번호 → 그룹 매핑

| 그룹 | 항목 | 개수 | 핵심 |
|---|---|---|---|
| **타입 힌트 / 정적 분석** | #001, #008 | 2 | ndarray 힌트 세트, Optional grad |
| **네이밍 (의미 투명성)** | #002, #007, #015, #017, #019, #021, #022, #023, #025 | 9 | input_var, upstream_grad, fill_grad, worklist, output 단수, clear_grad, visited, schedule, 크로스참조 시도/철회 |
| **구조 / 추상화 (Function 핵심 설계)** | #003, #004, #010, #011, #013, #014 | 6 | ABC, @override, derivative/apply hook 대칭, backward→fill_grad 전역 함수 |
| **검증 / 방어막** | #016 | 1 | assert vs RuntimeError 구분 |
| **메모리 관리** | #026, #027 | 2 | weakref 순환 끊기, Config/no_grad 절약 모드 |
| **유틸 / step 한정 / 문서 정비** | #005, #006, #009, #012, #018, #020, #024 | 7 | name shadowing(step04), numerical_diff docstring, backward docstring, set_creator 복선, pipe(FP), 주석 정비, fill_grad 통합 |

### 회수 분류와의 관계 (step23 패키지화 시)

위 "주제별 그룹"과 헤더(L8)의 "회수 분류"(`🔵 라이브러리성` / `🟢 step 한정` / `🟡 유틸성`)는 **직교**:
- **주제별 그룹**: "무엇에 대한 변경인가" (네이밍? 구조? 메모리?)
- **회수 분류**: "어디로 가나" (core.py? 그 step에? utils.py?)

step23 회수 시: 각 항목마다 "주제별 그룹 + 회수 분류" 둘 다 보고 승격 결정.

### 상태 분포 (2026-07-31 기준)

| 상태 | 항목 수 | 비고 |
|---|---|---|
| ✅ 반영 | 24 | 대부분 |
| 🔄 보류 | 2 | #018 (pipe, step23 재도입), #020 (주석 정비, step23 회수) |
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
  | (B) f.input/f.output None | __call__ 미실행 = 프로그래먘 논리 버그 | assert | assert 유지 |
  | (C) y.grad None | 이전 반복 미충족 = 프로그래먘 논리 버그 | assert | assert 유지 |
- **★ 핵심 원칙 (debugging.md 교훈 2 직접 적용)**:
  - **사용자 오용 / 런타임 데이터** → `if ...: raise` (★ `-O` 모드에서도 살아남아야)
  - **프로그래먘 불변조건** → `assert` (`-O`에서 사라져도 로직 안전)
  - (A)는 "creator 없는 변수에 역전파 호출" — 이건 프로그래먘 논리 버그가 아니라 **사용자 오용**.
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
- **위치**: step13 도입 / **step23 회수 예정**
- **상태**: 🔄 보류 (2026-07-30, step13 진행 중 결정)
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
