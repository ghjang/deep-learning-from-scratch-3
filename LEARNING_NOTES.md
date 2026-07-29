# 📝 LEARNING_NOTES.md

『밑바닥부터 시작하는 딥러닝 ❸』 학습 노트 (자유 형식)
======================================================

> 이 파일은 **개인 학습 노트**. 질문, 통찰, 아이디어, 막힌 점, 수식, 코드 조각,
> 그림 등 뭐든 자유롭게 기록. 각 step별 헤딩 아래에 작성.
>
> - 진척도 요약은 `LEARNING_PROGRESS.md`에서.
> - 특정 질문/토론은 GitHub Issue로 (💬 학습 질문 템플릿).
>
> 작성 팁:
> - 완벽하게 쓰지 않아도 됨. 생각 흐름 보존이 목적.
> - 모르는 건 ❓로 표시하고 나중에 채우기.
> - 통찰은 💡, 이슈 링크는 🔗로 표시.
> - 코드 예시는 삼중 백틱으로.

---

## 🎲 학습 전 메모 (시작 전)

- (여기에 학습 시작 전 목표, 우려, 기대 등을 자유롭게 적어보세요)
- 예: "역전파 수학이 제일 걱정", "MLX 포팅까지 가보고 싶다", 등

---

## 🔧 rezero 개선 회계

> 책 원본(`dezero/`) 대비 **rezero에서 적용/고려하는 개선사항** (타입 힌트, 네이밍, 추상화 강제력 등).
> 생각나는 대로 append → step23(패키지화) 시점에 회수해서 `rezero/core.py`에 반영.

👉 [REZERO_CHANGES.md](./REZERO_CHANGES.md)

---

## 🧪 보충 탐구 노트 인덱스

> step 진도 외에 깊이 파고 싶은 주제들은 `notes/` 디렉터리에 **주제별 개별 파일**로 정리.
> 상세 내용은 각 파일로. 여기는 링크만.

| # | 시점 | 주제 | 파일 |
|---|---|---|---|
| 1 | step01 직후 | Python 클래스 / 캡슐화 / 문법 이디엄 / 프레임워크 (13가지) | [notes/exploration_01_python_basics.md](./notes/exploration_01_python_basics.md) |
| 2 | step01 직후 | NumPy 기본 (3권 중심) | [notes/exploration_02_numpy_basics.md](./notes/exploration_02_numpy_basics.md) |
| 3 | step01 직후 | 백엔드 어댑터 (CuPy/MLX, autograd, Define-by-Run) | [notes/exploration_03_backend_adapters.md](./notes/exploration_03_backend_adapters.md) |
| 4 | step01 직후 | sympy vs PyTorch (심볼릭 vs 수치 패러다임) | [notes/exploration_04_symbolic_vs_numeric.md](./notes/exploration_04_symbolic_vs_numeric.md) |
| 5 | step01 직후 | Python 객체 모델 (CPython 내부, 리플렉션, 룩업 체계 5가지 ★공식 참조) | [notes/exploration_05_python_object_model.md](./notes/exploration_05_python_object_model.md) |
| 6 | step01 직후 | Python 기본 자료형 (list/tuple/str, 레퍼런스 모델, 얕은/깊은 복사) | [notes/exploration_06_data_types.md](./notes/exploration_06_data_types.md) |
| 7 | step01 직후 | Python 문법/이디엄 (데코레이터, f-string, lambda, @override/@overload) | [notes/exploration_07_syntax_idioms.md](./notes/exploration_07_syntax_idioms.md) |
| 8 | step01 직후 | 런타임 클래스 조작 (Monkey Patching, 네임스페이스, 역직렬화) | [notes/exploration_08_monkey_patching.md](./notes/exploration_08_monkey_patching.md) |
| 9 | step02 직후 | Python 추상 클래스 (`abc.ABC` vs `NotImplementedError`) | [notes/exploration_09_abc_abstract.md](./notes/exploration_09_abc_abstract.md) |
| 10 | step04 직후 | 도대체 미분이 뭔데? (수치 미분에서 깨달은 본질, 아하 모먼트) | [notes/exploration_10_what_is_derivative.md](./notes/exploration_10_what_is_derivative.md) |
| 11 | step04 직후 | 자동 미분 두 모드 (포워드 vs 리버스, 왜 역전파인가) | [notes/exploration_11_autodiff_modes.md](./notes/exploration_11_autodiff_modes.md) |
| 12 | step04 직후 | 언어 바인딩/타이핑 (early/late binding, 정적/동적 타이핑, 언어 비교) | [notes/exploration_12_language_binding.md](./notes/exploration_12_language_binding.md) |
| 13 | step05 진행 중 | 미분 표기법의 두 얼굴 (`dy/dx` vs `df/dx`, Leibniz/Lagrange, 국소적 미분, 역전파 수학) | [notes/exploration_13_derivative_notation.md](./notes/exploration_13_derivative_notation.md) |
| 14 | step05 진행 중 | "미분" 용어 7중 혼돈과 해독 전략 (미분값/도함수/미분연산, 한영 대조, 밑시딥 실전) | [notes/exploration_14_derivative_terminology.md](./notes/exploration_14_derivative_terminology.md) |
| 15 | step05 진행 중 | 수학 기호의 어원과 역사 (√/∫/d/∂/∇/∞ 모양의 진짜 이유) | [notes/exploration_15_math_symbol_origins.md](./notes/exploration_15_math_symbol_origins.md) |
| 16 | step08 진행 중 | "부작용" 번역 비판 + side effect 재프로그래밍 (번역어 감정색 왜곡, 순수함수, 최적화 충돌) | [notes/exploration_16_side_effect.md](./notes/exploration_16_side_effect.md) |
| 17 | step10 준비 중 | 파이썬 테스팅 패러다임 진화 (unittest→pytest, 책 교육적 선택 vs 실무 국룰, hypothesis) | [notes/exploration_17_python_testing.md](./notes/exploration_17_python_testing.md) |

### 🎨 디자인 패턴 (횡단 관심사, 누적형)

> exploration_XX와 다른 카테고리. 패턴은 여러 step에 걸쳐 재등장하는 횡단 관심사라 단일 파일에 누적 관리.

| 파일 | 시점 | 주제 |
|---|---|---|
| 🎨 | step01~ 누적 | DeZero에 등장하는 디자인 패턴 (래퍼, 템플릿 메서드 등) | [notes/design_patterns.md](./notes/design_patterns.md) |

### 🐛 디버깅 (횡단 관심사, 누적형)

> 디자인 패턴과 같은 구조. 파이썬 런타임 검증/디버깅 메커니즘(assert, 예외, 재귀 한계 등)을 여러 step에 걸쳐 누적 정리.

| 파일 | 시점 | 주제 |
|---|---|---|
| 🐛 | step08~ 누적 | 파이썬 런타임 검증/디버깅 (assert + `-O` 모드, RecursionError, fail-fast 등) | [notes/debugging.md](./notes/debugging.md) |

### 📐 코딩 스타일 (횡단 관심사, 누적형)

> 디자인 패턴/디버깅과 같은 구조. PEP 8 기반 코드 스타일(빈 줄, 주석, 네이밍, 함수 길이 등)을 여러 step에 걸쳐 누적 정리.

| 파일 | 시점 | 주제 |
|---|---|---|
| 📐 | step08~ 누적 | 코드 스타일/가독성 (논리 블록 빈 줄, PEP 8 의무 vs 관행 등) | [notes/coding_style.md](./notes/coding_style.md) |

---

## Step 01 — [1고지] 상자로서의 변수

**Issue**: [#2](https://github.com/ghjang/deep-learning-from-scratch-3/issues/2)
**완료일**: 2026-07-21
**상태**: ✅

### 📖 요약 (한 줄)

Variable 클래스 도입 — numpy ndarray를 감싸는 "데이터 상자"를 만들어, 이후 역전파 메타정보를 붙일 토대 마련.

### 💡 통찰 / 배운 점

**Variable은 "래퍼 패턴"** — Java의 `Integer/int` 박싱(Boxing)과 유사
- 원시값(`ndarray`) → 객체(`Variable`)로 감싸서 **메타정보(`grad`, `creator` 등)를 붙일 공간** 확보
- PyTorch `Tensor`, TF `Tensor`도 같은 철학

**왜 그냥 ndarray 안 쓰고 상자를?**
- ndarray 자체엔 "이 데이터가 어떤 연산에서 왔는지" 추적 기능이 없음
- 역전파(step07+)를 구현하려면 계산 그래프 정보가 필요 → 그걸 담을 그릇이 Variable

### 📐 NumPy 차원 (키워드)

| 표현 | ndim | shape | 비고 |
|---|---|---|---|
| `np.array(1.0)` | 0 | `()` | 스칼라 |
| `np.array([1.0])` | 1 | `(1,)` | 벡터 (길이 1) |
| `np.array([[1.0, 2.0], [3.0, 4.0]])` | 2 | `(2, 2)` | 행렬 |

- `ndim`: 차원 수 (축의 개수)
- `shape`: 각 축의 크기 튜플
- step01은 단일값 미분 다루니 **0차원 스칼라** 사용. 텐서(다차원)는 step41+에서.

### 📝 코드 메모

```python
class Variable:
    def __init__(self, data):
        self.data = data   # 상자 안의 "공"

x = Variable(np.array(1.0))  # 상자에 0차원 스칼라 담기
x.data = np.array(2.0)        # 상자의 내용물 교체 가능 (.data는 일반 속성)
```

- `self.data`는 일반 속성이라 **재할당 가능** → 나중에 `self.grad = ...` 식으로 결과 대입에 활용
- `inspect()` 헬퍼 패턴 도입 (Variable 내부 구조 탐구용, step별 재사용 예정)

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/2
- 구현: `rezero/steps/step01.py`
- 정답지: `steps/step01.py`
- 🎨 디자인 패턴: [notes/design_patterns.md](./notes/design_patterns.md) §1 Wrapper 패턴 (Variable이 ndarray를 감쌈)
- 🧪 보충 탐구 #1: [notes/exploration_01_python_basics.md](./notes/exploration_01_python_basics.md) (Python 기본기 13가지)
- 🧪 보충 탐구 #2: [notes/exploration_02_numpy_basics.md](./notes/exploration_02_numpy_basics.md) (NumPy 3권 중심)
- 🧪 보충 탐구 #3: [notes/exploration_03_backend_adapters.md](./notes/exploration_03_backend_adapters.md) (백엔드 CuPy/MLX)
- 🧪 보충 탐구 #4: [notes/exploration_04_symbolic_vs_numeric.md](./notes/exploration_04_symbolic_vs_numeric.md) (sympy vs 수치)
- 🧪 보충 탐구 #5: [notes/exploration_05_python_object_model.md](./notes/exploration_05_python_object_model.md) (CPython 객체 모델)
- 🧪 보충 탐구 #6: [notes/exploration_06_data_types.md](./notes/exploration_06_data_types.md) (기본 자료형/레퍼런스)
- 🧪 보충 탐구 #7: [notes/exploration_07_syntax_idioms.md](./notes/exploration_07_syntax_idioms.md) (문법/이디엄)
- 🧪 보충 탐구 #8: [notes/exploration_08_monkey_patching.md](./notes/exploration_08_monkey_patching.md) (Monkey Patching/런타임 조작)

**키워드**: `#Variable` `#래퍼패턴` `#박싱` `#ndarray` `#ndim` `#shape` `#스칼라` `#0차원`

## Step 02 — [1고지] 변수를 낳는 함수 (Function 도입)

**Issue**: [#3](https://github.com/ghjang/deep-learning-from-scratch-3/issues/3)
**완료일**: 2026-07-23
**상태**: ✅

### 📖 요약 (한 줄)

`Function` 기반 클래스 도입 — `Variable`(상자)을 받아 → 연산 → 새 `Variable`을 낳는 변환기. Template Method 패턴으로 "상자 까기/포장은 기반이, 실제 계산은 자식이" 분업.

### 💡 통찰 / 배운 점

**"상자는 기반 클래스가, 공은 자식이"** — 관심사 분리(SoC)
- `Function.__call__`: Variable 언팩/패킹 흐름 고정 (프레임워크 관심사)
- `Square.forward`: 순수 수학 연산 (도메인 관심사)
- 자식은 `forward()`만 정의하면 Function처럼 쓸 수 있음 → 확장성의 핵심

**PyTorch와의 연결** — `torch.nn.Module.__call__` → `forward()` 구조가 동일. DeZero가 PyTorch 스타일인 이유가 바로 이 패턴.

**두 패턴의 협력** — step01의 래퍼(Variable)를 step02의 템플릿(Function.__call__)이 다루는 구조. 두 패턴이 DeZero의 기본 골격을 이룸.

### 📝 결정 기록: `__call__` 매개변수 이름

**쟁점**: 책 원본은 `input`. 브로가 수정 제안.

**후보**:
- `input` (원본) — ❌ Python 빌트인 함수 섀도잉 (콘솔 입력용)
- `arg` — Python 관용적(`*args` 등)이나 의미 부족
- `param` — 정의부라 정확하나, PyTorch에선 학습 가중치 뉘앙스
- `input_var` ✅ — 의미 기반, "입력 변수" 역할 명확

**결정**: `input_var`
**이유**: 브로 "읽기 좋은 코드" 선호 + step01 `inspect()` 스타일과 일관

**참고 — Parameter vs Argument 구분**:
- **Parameter(매개변수)**: 함수 정의부의 변수. `def f(input_var):`의 `input_var`
- **Argument(인자/인수)**: 함수 호출부의 값. `f(x)`의 `x`
- 비유: Parameter = "주차 공간", Argument = "거기 들어오는 차"

> 📌 `rezero/core.py`로 프레임워크 코드로 모을 시점엔 네이밍 다시 검토 예정 (backward 등 다른 메서드와의 일관성 고려)

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/3
- 구현: `rezero/steps/step02.py`
- 정답지: `steps/step02.py`
- 🎨 디자인 패턴: [notes/design_patterns.md](./notes/design_patterns.md) §2 Template Method, §1 Wrapper

### 📝 코드 / 수식 메모

```python
class Function:
    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② Template Method 핵심
        output = Variable(y)            # ③ 상자 포장
        return output

    def forward(self, in_data):
        raise NotImplementedError()
```

- `raise NotImplementedError()`: 자식이 안 구현하면 바로 에러. 파이썬 전통적 추상 메서드 관용구. (`abc.ABC`와의 비교는 탐구 후보)
  - 🔬 심화: [exploration_09_abc_abstract.md](./notes/exploration_09_abc_abstract.md) — abc.ABC vs NotImplementedError, 우리 코드 변화 비교
- `f = Square()` 후 `f(x)`로 호출 — `__call__` 덕분에 함수처럼 사용 가능

**키워드**: `#Function` `#TemplateMethod` `#관심사분리` `#SoC` `#NotImplementedError` `#Wrapper패턴협력` `#PyTorch스타일` `#__call__` `#parameter_vs_argument` `#input_var`
---

## Step 03 — [1고지] 함수 연결

**Issue**: [#4](https://github.com/ghjang/deep-learning-from-scratch-3/issues/4)
**완료일**: 2026-07-23
**상태**: ✅

### 📖 요약 (한 줄)

`Exp` 구상 클래스 추가 + `Square → Exp → Square` 함수 연쇄 구현. step02의 Template Method 패턴 확장력 체감, "함수 연쇄 = 계산 그래프" 직감 획득.

### 💡 통찰 / 배운 점

**Template Method의 확장력 체감** — `Exp` 추가는 `forward` 한 줄(`np.exp(x)`)로 끝남. 기반 클래스(`Function`) 설계가 좋으면 새 함수 추가가 거의 공짜. 이게 패턴의 힘.

**"함수 연쇄 = 계산 그래프"** — `x → A(Square) → a → B(Exp) → b → C(Square) → y` 이 선형 연쇄가 곧 **계산 그래프(computational graph)**. step06+ 역전파에서 이 그래프를 거꾸로 타고 미분값이 흐를 거라는 예고만 체감.

**합성 함수** — `y = (e^(x²))²`. 미적분 chain rule이 다음 step들에서 컴퓨터 구현될 예정. 수학적으로 `y = C(B(A(x)))`.

### 📝 결정 기록: abc + @override 도입 실험

**쟁점**: 책 원본(step02/03)은 `raise NotImplementedError()`. 브로가 step03에서 변형 실험으로 `abc.ABC` + `@abstractmethod` + `@override`를 도입해봄.

**후보**:
- `raise NotImplementedError()` (책 원본) — 단순, 학습 명확성
- `abc.ABC` + `@abstractmethod` (Python 공식) — 런타임 강제력 (인스턴스 생성 시 검사)
- 추가로 `@override` (Python 3.12+) — 자식 재정의 명시, 정적 분석 도구(mypy/pyright)로 검증

**결정**: step03에선 **abc + @override 도입** (변형 실험)
**이유**: "강제력 차이"를 직접 체감하기 위함. 특히 `@override`는 런타임 강제력이 없고 정적 분석 도구가 필요하다는 핵심 통찰을 코드로 확인.

**핵심 발견 — 강제력 차이**:
| 데코레이터 | 런타임 강제 | 정적 분석 필요 |
|---|---|---|
| `@abstractmethod` | ✅ 강제 (인스턴스 생성 거부) | ❌ |
| `@override` | ❌ 없음 (조용히 통과) | ✅ mypy/pyright 필수 |

→ 자세한 건 exploration_09 §9에서 심화 정리.

> 📌 step02 노트에선 "학습 스크립트는 NotImplementedError 유지"라 했으나, step03에선 변형 허용. 단, `rezero/core.py`(향후 프레임워크 코드)로 모을 시점엔 정적 분석 도구 설정(pyproject.toml mypy/pyright) 여부에 따라 @override 의미 달라짐.

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/4
- 구현: `rezero/steps/step03.py`
- 정답지: `steps/step03.py`
- 🎨 디자인 패턴: [notes/design_patterns.md](./notes/design_patterns.md) §2 Template Method (Exp가 확장력 예시)
- 🧪 탐구 #9: [notes/exploration_09_abc_abstract.md](./notes/exploration_09_abc_abstract.md) §9 `@override` 심화 (강제력 차이)

### 📝 코드 / 수식 메모

```python
A = Square()
B = Exp()
C = Square()

x = Variable(np.array(0.5))
a = A(x)      # 0.5² = 0.25
b = B(a)      # e^0.25 ≈ 1.2840
y = C(b)      # 1.2840² ≈ 1.6487
```

- `np.exp`: 자연대수 밑 e(≈2.718)의 거듭제곱. sigmoid/softmax 활성화 함수의 핵심. step27에서 `Exp`/`Log` 재등장 예정
- `**` 연산자: 파이썬 내장 거듭제곱. 정수/실수 operand 모두 가능 (`x ** 0.5` = 제곱근). step22에서 `__pow__` 매직 메서드로 다시 만남

**키워드**: `#함수연쇄` `#chain` `#계산그래프` `#Exp` `#np.exp` `#합성함수` `#TemplateMethod확장력` `#abc` `#abstractmethod` `#override` `#강제력차이` `#메서드` `#C++멤버함수`
---

## Step 04 — [1고지] 수치 미분

**Issue**: [#5](https://github.com/ghjang/deep-learning-from-scratch-3/issues/5)
**완료일**: 2026-07-24
**상태**: ✅

### 📖 요약 (한 줄)

`numerical_diff` 함수로 중앙 차분(central difference) 수치 미분 구현. `Function.__call__`에 `self.input`/`self.output` 추가 — step07 역전파의 복선. 수치 미분의 "느림"이 역전파를 필요로 하는 이유 체감.

### 💡 통찰 / 배운 점

**★ 미분의 본질에 대한 아하 모먼트** — 이번 step의 진짜 수확은 코드 자체보다 **개념적 깨달음**.
- "미분 = 공식 외우기"라는 오해에서 벗어남 → "미분 = 순간 변화율(변화를 측정하는 도구)"
- **코드로 짠 함수(신경망)도 미분 가능** → autograd의 철학적 기반 체감
- 3Blue1Brown 영상 시청(수동) vs 코드 구현(능동)의 차이 — Feynman technique
→ 상세: exploration_10 "도대체 미분이 뭔데?"

**중앙 차분 공식**: `f'(x) ≈ [f(x+h) - f(x-h)] / 2h`
- 왜 전진 차분 안 쓰고 2h로 나누나 → 오차 O(h²)로 감소 (step05 심화)

**★ Function.__call__ 복선** — `self.input`/`self.output` 저장은 "왜?" 의문에서 시작.
- 이유: step07+ 역전파에서 "어떤 입력이 들어왔는지" 알아야 backward 계산 가능
- 미리 저장해두는 것 = Define-by-Run 패턴의 핵심 (순전파 시점에 그래프 기록)

**수치 미분의 한계 체감** — N개 파라미터 → 2N회 순전파. 백만 파라미터 신경망이면 백만 배 느림.
→ 역전파(리버스 모드 autodiff)가 왜 필요한지 실감. 상세: exploration_11

### 📝 결정 기록: `f` 변수 재사용 수정

**쟁점**: 책 원본 step04.py에서 `f = Square()` 후 `def f(x):`로 같은 이름 재사용 → IDE 빨간줄.

**후보**:
- 그대로 유지 (책 충실성)
- 이름 분리 (`sq`, `composite_f`) — name shadowing 악취 제거

**결정**: 이름 분리 (`sq`, `composite_f`)
**이유**: name shadowing은 버그는 아니지만 "실행 순서 의존적"이라 순서 바꾸면 깨짐. 학습용 스크립트라도 나쁜 패턴은 피하는 게 교육적. 원본은 steps/에 보존되어 있으니 rezero는 깔끔하게.
**파생 탐구**: 이 문제에서 "왜 파이썬은 후방 참조 OK?" → C/C++과 비교 → early/late binding, 정적/동적 타이핑까지 확장 → exploration_12

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/5
- 구현: `rezero/steps/step04.py`
- 정답지: `steps/step04.py`
- 🧪 탐구 #10: [notes/exploration_10_what_is_derivative.md](./notes/exploration_10_what_is_derivative.md) — 미분 본질 (아하 모먼트 서사)
- 🧪 탐구 #11: [notes/exploration_11_autodiff_modes.md](./notes/exploration_11_autodiff_modes.md) — 포워드/리버스 모드 (수치 미분의 한계)
- 🧪 탐구 #12: [notes/exploration_12_language_binding.md](./notes/exploration_12_language_binding.md) — 언어 바인딩/타이핑 (`f` 재사용에서 출발)

### 📝 코드 / 수식 메모

```python
def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)                          # 블랙박스: f 내부 몰라도 호출만 하면 됨
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)
```

**검증 결과**:
- `Square(x=2)` 미분: 4.000000 (정답 2x=4 ✅)
- 합성 `y=(e^(x²))²`, x=0.5: 3.297443 (해석적 정답 e^0.5·2≈3.2974 ✅, 오차 0.00004)

**eps=1e-4 트레이드오프**: 너무 작으면 부동소수점 오차, 너무 크면 근사 오차. 1e-4가 적절한 타협점 (step05에서 심화).

**수식**: `y = (e^(x²))² = e^(2x²)`, `y' = e^(2x²)·4x`

**키워드**: `#수치미분` `#중앙차분` `#central-difference` `#numerical_diff` `#eps` `#1e-4` `#블랙박스미분` `#autograd철학` `#self.input` `#self.output` `#역전파복선` `#DefineByRun` `#name-shadowing` `#아하모먼트` `#미분본질` `#Feynman-technique`
---

## Step 05 — [1고지] 역전파 이론 [No code]

**Issue**: [#6](https://github.com/ghjang/deep-learning-from-scratch-3/issues/6)
**완료일**: 2026-07-28
**상태**: ✅

### 📖 요약 (한 줄)

역전파 = 연쇄법칙(chain rule)을 계산 그래프에 역방향으로 흘려보내는 시스템. 각 노드는 **자기 국소적 미분 ($df/dx$)만 계산**하고, 전체는 chain rule이 조립. 역전파 = **right fold ($\prod$ 곱하기 누적)** 패턴.

### ❓ 질문 / 막힌 점

- ✅ 진도표/노트 제목 정정 (수치 미분 이론 → 역전파 이론)
- 🎬 브로 유튜브 영상 발견: [합성함수 미분 규칙 증명 (연쇄법칙)](https://youtu.be/BUCUMmm-GQQ) — 엄밀성 검증은 마님 프로젝트 별도 세션
- ❓ df/dx vs dy/dx → 탐구 #13에서 해명
- ❓ "미분" 용어 다의성 → 탐구 #14에서 해독 휴리스틱 정리

### 💡 통찰 / 배운 점

**★ 역전파 = right fold (`foldr`)** — 브로가 책 읽으며 자연스럽게 도달한 통찰. 최종 출력 $y$에서 출발해 오른쪽→왼쪽으로 $\prod$(곱) 누적. step07(재귀) → step08(반복문) 구조를 미리 잡은 사고방식.

**★ 국소적 미분 = $df/dx$ 관점** — 각 노드는 자기 함수만 미분 (`Square.backward()`의 `2*x` = Square의 $df/dx$). 전체 $dy/dx$는 chain rule이 조립. 이게 역전파 설계와 완벽히 일치.

**★ `gy`/`gx` 변수명** — `gy` = upstream gradient (fold 누적값), `gx` = downstream gradient (다음 노드로 전달). 책 원서 변수명은 짧지만 의미가 투명하지 않음. step06 구현에서 변수명 변형 실험 후보 (upstream_grad/downstream_grad).

**★ 미분 연산자 $\dfrac{d}{dx}$** = 고차 함수 (lazy evaluation). 브로의 제곱근/lazy 비유($\sqrt{4}$는 "구하라"는 명령)가 수학 기호 일반의 패턴으로 확장.

**★ 그래디언트 정의 조건** — 출력이 스칼라(1개)인 함수만. 출력 다변수 벡터면 야코비안(Jacobian, Jacobi 1841)이 필요.

### 🔗 관련 링크

- 🎬 [합성함수의 미분 규칙 증명 (연쇄법칙/체인룰) — 브로 유튜브](https://youtu.be/BUCUMmm-GQQ)
  - 25초 숏폼 애니메이션 (파이썬 마님 + Suno BGM)
  - 역전파의 수학적 기반인 연쇄법칙 시각화 → step05 본문과 직결
  - > 엄밀한 증명 검증은 마님/VSCode 확장 프로젝트(별도 세션)에서 수행
- 🧪 탐구 #13: [notes/exploration_13_derivative_notation.md](./notes/exploration_13_derivative_notation.md) — `dy/dx` vs `df/dx`, 역전파 수학 (★ step05 핵심 헷갈림, fold 통찰)
- 🧪 탐구 #14: [notes/exploration_14_derivative_terminology.md](./notes/exploration_14_derivative_terminology.md) — "미분" 용어 7중 혼돈 해독 (미분값/도함수 구분)
- 🧪 탐구 #15: [notes/exploration_15_math_symbol_origins.md](./notes/exploration_15_math_symbol_origins.md) — 수학 기호 어원/역사 (√, ∫, d, ∂, ∇ 모양의 진짜 이유)


### 📝 코드 / 수식 메모

**chain rule (연쇄법칙)** — 합성함수 $y = f(g(x))$:

$$
\frac{dy}{dx} \;=\; \underbrace{f'(g(x))}_{\text{노드 } f \text{의 국소적 미분}} \cdot \underbrace{g'(x)}_{\text{노드 } g \text{의 국소적 미분}}
$$

**역전파 = right fold ($\prod$)**:

$$
\frac{dy}{dx} \;=\; \prod_{\text{모든 노드}} (\text{국소적 미분})
$$

**DeZero 의사코드** (step06 예고):
```python
# 수동 right fold (한 스텝씩 손으로 호출)
y.grad = 1.0              # fold 시작 (최종 출력에서)
b.grad = C.backward(y.grad)   # fold step 1
a.grad = B.backward(b.grad)   # fold step 2
x.grad = A.backward(a.grad)   # fold step 3 (입력에 도달)
```

→ `gy` = upstream gradient (fold 누적값), `gx` = downstream gradient (다음 노드로 전달).

**키워드**: `#역전파이론` `#연쇄법칙` `#chain-rule` `#국소적미분` `#df/dx` `#right-fold` `#foldr` `#upstream-gradient` `#downstream-gradient` `#gy/gx` `#미분연산자` `#고차함수` `#lazy` `#그래디언트` `#야코비안` `#아하모먼트`


---

## Step 06 — [1고지] 수동 역전파 (Variable.grad, Function.backward)

**Issue**: [#7](https://github.com/ghjang/deep-learning-from-scratch-3/issues/7)
**완료일**: 2026-07-29
**상태**: ✅

### 📖 요약 (한 줄)

step05의 역전파 이론(chain rule, right fold)을 **코드로 구현**. `Variable.grad` 속성 + `Function.backward()` 메서드 도입. step04에서 깔아둔 `self.input` 복선이 회수되는 순간. 수동으로 한 스텝씩 backward 호출 = right fold를 손으로 unfold.

### ❓ 질문 / 막힌 점

- ✅ `gy`/`gx` 변수명 → `upstream_grad`/`downstream_grad` + `local_deriv` 분리 변형 채택 (step05 통찰 반영)
- ✅ `backward()` 추상화 → step04 스타일 유지, `@abstractmethod` + 자식에 `@override`
- ✅ `Function.__call__`의 `self.output` → step06 정답지에선 미사용, step07+ 자동 역전파 복선
- ✅ `Variable.grad` 정적 분석 경고 → `Optional[np.ndarray]` 타입 힌트로 해결
- ⏭ `Variable.data: np.ndarray` 타입 힌트 → 선반영 시도했다 **취소** (forward 반환 타입 미정의로 Pyright 오류). 다음 step에서 Variable/Function 시그니처 **세트로** 도입 예정 → [REZERO_CHANGES.md](./REZERO_CHANGES.md) #001

### 💡 통찰 / 배운 점

**★ 역전파 = right fold (foldr)의 코드 구현** — step05 통찰이 코드로 펼쳐짐.
- 수동 역전파 `y.grad → C.backward → B.backward → A.backward` = 최종 출력에서 오른쪽→왼쪽으로 ∏ 누적
- 각 `backward()` = fold accumulator step (받은 누적값에 자기 몫을 곱해 다음 타자에게 전달)

**★ step04 복선 회수** — `self.input` 저장 이유가 드디어 밝혀짐.
- 순전파 시점에 입력을 기억해둬야 backward에서 `x = self.input.data`로 회수 가능
- 이게 Define-by-Run의 핵심 (순전파 시점에 그래프 기록)

**★ 역전파가 수치 미분보다 정확하고 빠르다** — 코드로 체감.
- 수치 미분(step04): 3.297443 (오차 0.00004, 입력 개수만큼 순전파 반복)
- 역전파(step06): 3.297442541400256 (오차 0, 해석적 정답, 순전파 1회 분량)

**★ `local_deriv` 분리의 힘** — 책 원본 한 줄(`gx = 2 * x * gy`)을 두 단계로 쪼개니, "자기 도함수 계산"과 "fold step"이 코드 구조로 드러남. 역전파 본질(각 노드는 자기 도함수만 계산)이 가독성으로 연결.

### 📝 결정 기록: 변형 실험 3종 (step04 ABC 스타일 연장)

**1. `gy`/`gx` → `upstream_grad`/`downstream_grad` + `local_deriv` 분리**

정답지 한 줄을 의미 단위로 분해:
```python
# 정답지: gx = 2 * x * gy  (도함수와 fold step이 한 줄에 섞임)
# rezero:
local_deriv = 2 * x                          # ① 자기 도함수 (df/dx) 평가
downstream_grad = local_deriv * upstream_grad # ② fold step (곱해서 누적)
```
→ step05 통찰("국소적 미분 = df/dx", "역전파 = fold")이 코드에 구현.
상세: [notes/exploration_13_derivative_notation.md](./notes/exploration_13_derivative_notation.md) §8 (gy/gx 헷갈림 분석)

**2. `Variable.grad: Optional[np.ndarray]` 타입 힌트**

책 원본 `self.grad = None`은 정적 분석(VSCode Pylance)에서 `y.grad = np.array(1.0)` 시 경고.
→ `Optional[np.ndarray]`로 해결 + **라이프사이클 명시** (역전파 전 None → 후 ndarray). PyTorch `grad: Optional[Tensor]`와 같은 패턴.

**3. `backward()`도 `@abstractmethod` + `@override`**

step04에선 forward만 ABC화. step06에선 backward도 추가 → 일관성. 자식 Square/Exp의 backward에 `@override` 부착.

> 📌 변수명 변형(`x`/`y` 유지 vs `in_data`/`out_data`)은 검토 후 **`x`/`y` 유지** 결정. 이유: 수학 y=f(x)와 일치 + PyTorch 표준 + 행렬/텐서 확장성 (브로 통찰 "나중엔 행렬 올 텐데").

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/7
- 구현: `rezero/steps/step06.py`
- 정답지: `steps/step06.py`
- 이전 step: step05 역전파 이론 (right fold 통찰)
- 🎨 디자인 패턴: [notes/design_patterns.md](./notes/design_patterns.md) §2 Template Method (backward로 패턴 확장)
- 🧪 탐구 #13: [notes/exploration_13_derivative_notation.md](./notes/exploration_13_derivative_notation.md) §8 역전파 연결 (gy/gx + fold 통찰, ★ step06 변형의 이론적 기반)
- 🔧 rezero 개선 회계: [REZERO_CHANGES.md](./REZERO_CHANGES.md) #007~#009 (step06 변형 3종)

### 📝 코드 / 수식 메모

**chain rule 전개** (합성 `y = (e^(x²))²`, `x = 0.5`):

$$
\frac{dy}{dx} = \underbrace{2b}_{C'} \cdot \underbrace{e^a}_{B'} \cdot \underbrace{2x}_{A'} = 2 \cdot 1.6487 \cdot e^{0.25} \cdot 1.0 = 3.2974\ldots
$$

**수동 역전파 (right fold unfold)**:
```python
y.grad = np.array(1.0)                  # fold 시작점 (최종 출력 y에서, upstream = 1)
b.grad = C.backward(y.grad)             # fold step 1: C 노드 (y → b)
a.grad = B.backward(b.grad)             # fold step 2: B 노드 (b → a)
x.grad = A.backward(a.grad)             # fold step 3: A 노드 (a → x, 입력에 도달)
```

**검증 결과**: `x.grad = 3.297442541400256` (step04 수치 미분 3.297443과 일치, 해석적 정답에 오차 0)

**키워드**: `#수동역전파` `#Variable.grad` `#Function.backward` `#right-fold` `#foldr` `#upstream-gradient` `#downstream-gradient` `#local_deriv` `#국소적미분` `#df/dx` `#chain-rule` `#step04복선회수` `#self.input` `#DefineByRun` `#Optional타입힌트` `#abc` `#@override` `#PyTorch스타일` `#변형실험`


---

## Step 07 — [1고지] 역전파 자동화 (재귀적 right fold)

**Issue**: [#8](https://github.com/ghjang/deep-learning-from-scratch-3/issues/8)
**완료일**: 2026-07-29
**상태**: ✅

### 📖 요약 (한 줄)

step06 수동 역전파를 **자동화** — `Variable.creator` 역방향 링크로 그래프 기록, 전역 `backward(start_var)` 한 번에 재귀 연쇄. step05 통찰(역전파 = right fold)의 **재귀적 구현**. Define-by-Run 완성. **★ 이번 step은 코드 자체보다 5개 구조 변형(#010~#014) + Known Gotcha 재발 사태 대응이 압도적.**

### ❓ 질문 / 막힌 점

- ✅ `creator`/`set_creator` 네이밍 — 책 충실 유지. 검증 결과 `dezero/core.py:81-83`에 generation 설정(step16 복선) 추가 로직 확인 → 메서드 존재 이유 납득 (#012)
- ✅ Variable.backward() vs Function.backward(gy) 혼동 — **전역 backward로 분리** (#014) → 혼동 원천 제거
- ✅ `self.output` 저장 — step07에선 저장하지만 미사용, step08(반복문)에서 실사용 (이중 복선 유지)
- ⚠️ Known Gotcha #10 (`#N` 자동 링크) **재발** — 이슈 #7/#8 본문에서 `#9`/`#10`/`#13`이 oreilly-japan으로 연결. 정정 완료 + AGENTS.md #10 "사전 검증" 절 추가 + 랩업 6단계에 검증 하위 단계 추가. 단, oreilly-japan referenced 이벤트는 영구 손상.

### 💡 통찰 / 배운 점

**★ 역전파 자동화 = right fold의 재귀 구현** — step05 통찰 회수.
- step06: 손으로 unfold (C/B/A.backward 직접 호출 5줄)
- step07: creator 링크로 `backward(y)` 한 번에 재귀 (1줄, upstream_grad 기본값)

**★ Define-by-Run 완성** — 순전파 시점에 `output.set_creator(self)`로 그래프 자동 기록. 역전파 시 creator 링크 따라 연쇄.

**★ 5개 구조 변형 연쇄** (브로 "다 똑같네" 통찰에서 시작):
1. backward 중복 발견 → **derivative hook** (#010)
2. forward도 같은 구조 → **apply hook, 대칭 완성** (#011)
3. set_creator 의심 → **generation 복선 발견** (#012)
4. "도함수값이 아니라 도함수" → **derivative callable 반환** (#013, 노트 13번 §4 구현)
5. "backward는 Variable에 왜?" → **전역 함수 분리** (#014, JAX 스타일, rezero 정체성)

**★ 타입 힌트 세트 도입** (#001 회수) — 부분 도입하면 정적 분석 깨진다는 교훈(step06 실패)을 step07에서 세트 도입으로 증명. Pyright가 실제 버그(grad None)까지 잡아줌.

**★ Known Gotcha #10 재발 사태** — AGENTS.md에 랩업 절차에 #N 검증 없던 게 원인. 이번에 "사전/사후 검증" 절 추가. 미래 AI/브로가 같은 실수 안 하게 방어망 강화.

### 📝 결정 기록: 변형 5종 + 회수 1종 (REZERO_CHANGES #001, #010~#014)

**#010 derivative hook** — backward에 Template Method 재적용. 자식 구현량 5줄→1줄. DRY.
**#011 apply hook** — forward에도 동일 구조. `forward`→`apply` 네이밍 (수학 f(x) 함수 적용과 일치). 대칭 완성.
**#012 set_creator 유지** — 책 충실. 검증 결과 generation(step16) 복선 발견 → 메서드 존재 이유 납득.
**#013 derivative callable 반환** — `derivative()`가 도함수(함수 객체) 반환. 노트 13번 §4 "도함수 = 고차 함수" 통찰의 코드 구현.
**#014 ★★★ backward 전역 함수** — Variable 메서드 → 전역 `backward(start_var)`로 분리. JAX 스타일. Variable은 순수 데이터 상자로 회귀. rezero 정체성. (+ upstream_grad 기본값 None→ones_like, start_var 네이밍, 재귀 버그 수정 교훈)
**#001 회수** — 전체 시그니처 타입 힌트 세트 도입. step06 실패("세트로 넣어야")를 step07에서 증명.

> 📌 모든 변형은 **"최종 반영 보류"** 메모 달아둠 — step13(가변 길이)/step34(행렬 미분) 진입 시점에서 재평가. 복잡해지면 apply/derivative hook이나 전역 backward가 안 맞을 수 있어. 그때 열어둔 탈출구(backward 직접 오버라이드) 사용.

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/8
- 구현: `rezero/steps/step07.py`
- 정답지: `steps/step07.py`
- 이전 step: step06 수동 역전파 (변형 3종 + pyright 0 errors)
- 🧪 탐구 노트 13번 §8: 역전파 = right fold 통찰 (step07 재귀 구현의 사고 기반)
- 🔧 REZERO_CHANGES.md: **step07 변형 5종(#010~#014) + #001 회수** ★ 이번 step 하이라이트
- 🔬 RESEARCH_QUEUE.md 후보 6번: DAG 흡수 vs 분리, 3가지 autograd 패러다임 (#014 실증 자료)

### 📝 코드 / 수식 메모

**최종 구조 (rezero 정체성 — Variable 순수 데이터 상자 + 전역 backward)**:
```python
class Variable:                           # 순수 데이터 상자 (backward 없음 ★)
    data; grad; creator
    set_creator(func)

class Function(ABC):                      # 대칭 구조 (apply/derivative hook)
    __call__(input_var) → forward → apply (hook) + set_creator
    forward(x) → apply(x)                 # 기본 구현
    backward(gy) → derivative(x) * gy     # 기본 구현
    apply(x) / derivative()               # 선택적 hook (NotImplementedError)

def backward(start_var, upstream_grad=None):   # ★★★ 전역 함수 (#014)
    # 3단계 우선순위: 명시적 인자 > 기존 grad > ones_like 자동
    ...
    f.backward(start_var.grad)             # Function.backward (단일 노드)
    backward(x)                            # 재귀 연쇄

# 사용
backward(y)                                # 한 줄이면 역전파 완료
```

**검증**: `x.grad = 3.297442541400256` (step06과 동일, 해석적 정답), pyright 0 errors ✅

**키워드**: `#역전파자동화` `#재귀적right-fold` `#DefineByRun완성` `#creator역방향링크` `#apply-hook` `#derivative-hook` `#TemplateMethod대칭` `#callable반환` `#도함수객체` `#전역함수backward` `#JAX스타일` `#start_var` `#upstream_grad기본값` `#ones_like자동초기화` `#관심사분리` `#SoC` `#타입힌트세트` `#pyright0errors` `#KnownGotcha10재발` `#사전검증` `#변형5종` `#REZERO_CHANGES` `#아하모먼트`


---

## Step 08 — [1고지] 재귀에서 반복문으로 역전파 고속화

**Issue**: [#9](https://github.com/ghjang/deep-learning-from-scratch-3/issues/9)
**완료일**: 2026-07-29
**상태**: ✅

### 📖 요약 (한 줄)

step07의 재귀적 `backward()`를 **반복문(명시적 스택)**으로 전환. 깊은 계산 그래프에서의 스택 오버플로 위험 회피가 핵심 동기. 수학적 구조(right fold)는 동일 — 단지 펼치는 방식이 재귀 호출 스택 → 리스트 스택으로 바뀔 뿐.

### ❓ 질문 / 막힌 점

- ✅ 재귀 깊어지면 RecursionError? → **맞음, 파이썬 예외**. 기본 한계 1000. 상세: debugging.md 항목 2.
- ✅ `assert`는 디버그 모드 전용 아닌가? 파이썬엔 그 구분이? → **있다, `-O` 플래그가 스위치**. 상세: debugging.md 항목 1.
- ✅ rezero 변형 항목 14번(전역 backward) 반복문 전환에서 외부 API 유지? → **유지됨** (`backward(y)` 호출 동일).
- ✅ step07 `upstream_grad` 3단계 우선순위, 반복문에선? → **루프 진입 전 한 번으로 단순화** (부수 효과).
- ✅ assert로 제약 체크가 맞냐? 위치도 맞냐? → ★ **둘 다 적중**. (A)는 사용자 오용이라 if/raise로, 위치도 초기화 시점으로. 상세: 항목 16번.
- ✅ 전역 함수명 backward가 맞냐? → ★ **아니다**, `fill_grad`로 개명. "grad 채우기"가 핵심 동작 명시. 상세: 항목 15번.

### 💡 통찰 / 배운 점

**★ "진짜 별거 없다" 자체가 step07 변형의 가치 증명** — 브로가 짚은 대로 step08은 전역 `backward()` 내부만 고치면 끝.
Variable/Function/Square/Exp는 한 줄도 안 바뀜. 관심사 분리(SoC, 항목 14번)가 다음 step으로의 확장 비용까지 낮춘 실증.

**★ 반복문 단순화 부수 효과** — 재귀의 복잡했던 upstream 3단계 우선순위 로직이 반복문에선 자연스럽게 사라짐.
재귀: 매 호출마다 upstream 결정. 반복문: 루프 진입 전 한 번 (직전 반복이 다음 y.grad를 미리 채워둠).
→ "자료구조가 알고리즘을 지배한다" — 명시적 스택이 로직까지 단순화시킨 사례.

**★ step07 복선 회수** — `Function.__call__`의 `self.output` 저장이 드디어 실사용.
재귀에선 y를 호출 컨텍스트로 넘겼지만, 반복문에선 `y = f.output; f.backward(y.grad)`로 저장해둔 출력에서 grad를 읽어와야 함.

**★ assert + RecursionError → 디버깅 탐구로 확장** — 브로의 두 질문에서 파생. 파이썬에도 디버그/릴리스 구분이 있다는
발견 (`-O` 플래그) + RecursionError 실증. 누적형 디버깅 노트(`notes/debugging.md`) 신설 계기.

**★ 브로 2연타 질문 → 변형 2종 추가 (#015, #016)** — step08 코드를 본 브로가 "assert가 디버깅 도구면 지금 하는 게 맞냐?
위치도 맞냐?" + "함수 이름이 backward가 맞냐?" 두 질문. 둘 다 정곡 → fill_grad 개명 + assert→RuntimeError 전환.
**방금 만든 debugging.md "교훈 2"를 우리 코드가 위반하고 있었다**는 자기반영적 통찰 (메타적 가치).

**★ funcs 리스트 복선 발견 — "점진적 설계" 패턴** — 브로 3연타 질문: *"funcs가 리스트인 이유? 현재는 최대 1개만 있는 구조 아닌가?"*
정확한 관찰. step08에선 선형 체인이라 스택 길이 1. 리스트인 이유는 **step14(같은 변수 반복)/step16(DAG)에서 분기 그래프 등장 시 복수 노드 push 때문**.
→ 책이 미래 step 확장을 대비해 미리 리스트로 깔아둔 "복선". set_creator(step07→step16 generation 복선)과 같은 패턴.
상세: design_patterns.md 패턴 3 "점진적 설계 / 미래 복선" (브로 질문에서 파생된 새 패턴 등록).

**★ 논리 블록 사이 빈 줄 — "코딩 스타일" 횡단 노트 신설** — 브로 4연타 질문: *"의미구분 위해 빈 줄 넣는 걸 금지하는 컨벤션인 거 아니냐?"*
→ 아님. PEP 8은 최상위 2줄/메서드 1줄은 **의무**, 함수 내부 논리 블록은 **"가끔 1줄" 권장**. 금지 아님.
fill_grad 본문을 논리 섹션(검증 / upstream 설정 / 메인 루프)마다 빈 줄 + 섹션 헤더 주석으로 분리.
누적형 코딩 스타일 노트(`notes/coding_style.md`) 신설 — 앞으로 주석 밀도, 네이밍, 함수 길이 등 계속 누적 예정.

**★ funcs → worklist 리네임 — CS 학술 패턴 "Worklist Algorithm" 인식** — 브로 5연타 질문:
*"funcs 변수명을 의미에 맞게 리팩터링 가능할까? 좀 느낌있게?"*
→ 단순 리네임인 줄 알았더니, 이 구조(`while worklist: pop → 처리 → push`)가 **CS 학술 정식 패턴 "Worklist Algorithm"**의 인스턴스.
Dragon Book(컴파일러 데이터플로우), GC handbook(mark phase), CLRS(그래프 순회) 등 CS 전반 골격.
변수명을 `worklist`로 바꾸면 **코드의 학술적 뿌리 인식** (#017, design_patterns 패턴 4 등록).
★ 브로의 "왜 리스트?"(패턴 3 복선) + "funcs 말고 worklist로?"(패턴 4 학술 패턴) 두 질문이 같은 코드의 두 층위를 파냄.

**★★ Worklist 타입 힌트 — 변형 3종의 emergent design 시너지** — 브로 7연타 질문:
*"work item이 Function 인스턴스 → 타입 힌트로 명확히할 수 있지 않나?"*
→ `type Worklist = list[Function]` (Python 3.12+). work item = Function 인스턴스가 타입 수준에서 명시.
★ **시너지 발견**: `start_var.creator: Optional[Function]`인데 `list[Function]`에 넣으면 에러 →
근데 도입부 guard(#016)가 **타입 좁히기** 수행 → 그 아래부턴 `Function` (Optional 풀림) → 안전.
→ **#015(fill_grad) + #016(guard) + #017(worklist)가 독립이 아니라 서로 강화하는 세트**.
guard가 "빠른 실패"뿐 아니라 "타입 안전성"까지 보너스로. 좋은 설계 결정들은 emergent하게 강화됨.
실증: guard 없음 pyright 에러 / guard 있음 ★ 에러 없음.

### 📝 결정 기록: 변형 3종 추가 (#015, #016, #017) — 브로 코드 리뷰에서 파생

**#015 전역 함수명 backward → fill_grad** (브로 작명 통찰):
- 브로: *"전역 backward 함수는 계산 그래프 순회하며 각 노드 변수에 누적미분값 저장하는 건데,
  함수 이름이 좀 거시기하지 않냐? fill_grad 따위가 더 나은 작명 아닌지?"*
- → `backward`는 방향(역방향)만, `fill_grad`는 "grad 채우기" 핵심 동작 명시.
- 역방향은 grad 연산의 유일한 방식이라 이름에 안 넣어도 암시 (JAX `jax.grad`와 정신적 유사).
- 부수 이점: step07의 "전역 backward vs Function.backward 이름 같고 역할 다름" 혼란 자동 해소.

**#016 assert → RuntimeError 전환 (검증 A)** — debugging.md 교훈 2 적용:
- 브로: *"assert가 디버깅 언어 도구라면 저런 제약 체크를 지금 assert로 하는 게 맞냐? 점검 위치도 맞아?"*
- 분석 결과 — 3개 검증 중 (A)만 assert 부적절:
  - (A) start_var.creator None → **사용자 오용** (런타임 케이스) → if/raise RuntimeError ★
  - (B)(C) f.input/output, y.grad None → **불변조건** (프로그래먘 논리 버그) → assert 유지
- ★★ **브로 2차 지적 — 위치를 함수 도입부 맨 앞으로** (fail-fast / guard clause):
  - 처음엔 upstream 설정 **뒤에** 검증 → 에러 내기 전에 `start_var.grad`를 변경하는 부작용
  - 도입부로 옮기니 **fail-fast**(wasted work 없이 즉시 실패) + **부작용 회피**(transactional) 동시 달성
  - 실증: 잘못된 `fill_grad(x)` 호출이 `x.grad`를 None→None 유지 (이전 위치였으면 ones_like로 채워졌을 것)
  - 상세: debugging.md 항목 3 (fail-fast + guard clause)
- ★ **-O 모드 실증**: assert였으면 사라질 검증이 RuntimeError로 살아있음. debugging.md 교훈 2의 코드 증명.
- 친절한 에러 메시지: "왜 잘못됐는지" + "어떻게 고치는지" 둘 다.

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/9
- 구현: `rezero/steps/step08.py`
- 정답지: `steps/step08.py`
- 이전 step: step07 역전파 자동화 (재귀) — Issue 8
- 🔧 REZERO_CHANGES.md: **step08 변형 3종(#015 fill_grad 개명, #016 assert→RuntimeError + 도입부, #017 funcs→worklist 리네임 + Worklist 타입 별칭)** + #014 검증 완료. ★ 변형 3종의 emergent design 시너지(guard가 타입 좁히기 제공)
- 🐛 디버깅 노트: [notes/debugging.md](./notes/debugging.md) 항목 1 (assert + `-O` 모드), 항목 2 (RecursionError), 항목 3 (fail-fast + 부작용 회피)
- 🧪 탐구 노트 16번: [notes/exploration_16_side_effect.md](./notes/exploration_16_side_effect.md) — "부작용" 번역 비판 (assert 부작용 논의에서 파생)
- 🎨 디자인 패턴: [notes/design_patterns.md](./notes/design_patterns.md) 패턴 3 "점진적 설계 / 미래 복선", 패턴 4 "Worklist Algorithm"
- 📐 코딩 스타일: [notes/coding_style.md](./notes/coding_style.md) 항목 1 "빈 줄 — 논리 블록 시각적 분리"


### 📝 코드 / 수식 메모

**반복문 fill_grad 구조** (책 step08 + rezero 전역 함수 + 개명 변형):
```python
def fill_grad(start_var, upstream_grad=None):
    if upstream_grad is not None:           # 루프 진입 전 한 번만
        start_var.grad = upstream_grad
    elif start_var.grad is None:
        start_var.grad = np.ones_like(start_var.data)

    if start_var.creator is None:           # ★ #016: 사용자 오용 → RuntimeError (-O에서도 살아남음)
        raise RuntimeError("역전파할 계산 그래프가 없습니다...")

    funcs = [start_var.creator]             # 명시적 스택 (힙)
    while funcs:
        f = funcs.pop()
        x, y = f.input, f.output            # ★ y = f.output 회수 (step07 복선)
        assert x is not None and y is not None   # 불변조건 (B) — 프로그래먘 논리 가정
        assert y.grad is not None                # 불변조건 (C)
        x.grad = f.backward(y.grad)         # 단일 노드 fold step
        if x.creator is not None:
            funcs.append(x.creator)         # 다음 노드 push
```

**검증 (3케이스)**:
- 정상: `fill_grad(y)` → `x.grad = 3.297442541400256` (step07 재귀와 동일, 해석적 정답) ✅
- 오용: `fill_grad(x)` [입력 변수] → RuntimeError 정상 발생 ✅
- ★ `-O` 모드: `fill_grad(x)` → RuntimeError **여전히 발생** (assert였으면 사라졌을 것!) ✅

**키워드**: `#재귀에서반복문` `#명시적스택` `#while루프` `#funcs.pop` `#스택오버플로회피` `#RecursionError` `#fill_grad` `#개명` `#의미투명성` `#항목14번검증` `#upstream단순화` `#부수효과` `#자료구조가알고리즘을지배` `#step07복선회수` `#self.output실사용` `#assert` `#-O모드` `#__debug__` `#RuntimeError` `#사용자오용vs불변조건` `#debugging.md교훈2적용` `#SoC가치증명` `#디버깅노트신설` `#JAX스타일` `#자기반영적통찰` `#funcs리스트복선` `#점진적설계` `#미래복선` `#DAG복선` `#step14/16대비`


---

## Step 09 — [1고지] 함수를 더 편리하게 (Function 클래스 사용성 개선)

**Issue**: [#10](https://github.com/ghjang/deep-learning-from-scratch-3/issues/10)
**완료일**: 2026-07-29
**상태**: ✅

### 📖 요약 (한 줄)

`Function` 클래스를 더 허들 없이 쓰기 위한 사용성 개선. `Square()(x)` 2단계 → `square(x)` 1단계 wrapper 함수 도입으로 합성 표현을 수학적 표기에 가깝게 (`square(exp(square(x)))`). 부가로 `as_array` 헬퍼(스칼라→ndarray 정규화) + `Variable.__init__` isinstance 런타임 체크 + ★ pipe 헬퍼(브로 제안, FP 합성).

★ 브로 통찰: "여기서 함수는 `Function` 클래스 — 더 편하게 = Function을 허들 없이 쓰자는 취지."
번역 "함수를 더 편하게"는 애매 — "Function 클래스 사용성 개선"이 원 의미에 가까움.

### ❓ 질문 / 막힌 점

- ✅ 브로 직감 "이미 처리한 것 같기도, 구식 같기도" → 검증: 정적(힌트)은 있었으나 동적(isinstance)은 없었음 / 역순 — 책 원본이 구식, 우리 step08이 더 진보됨.
- ✅ Pylance 127줄 `forward(x)` 빨간줄 → Optional 가드 부재. None 가드 3곳 + `# type: ignore` 의도 표시로 해결.
- ✅ "방어막 두 겹" → 실제론 3겹 (정적/동적타입/동적None). as_array와 isinstance가 협력.
- ✅ Pythonic 스캔 4곳 → 전부 "이미 Pythonic" (짧게 하면 오히려 안 좋음 — 항목 4 통찰).
- ✅ abstractmethod 죽은 import → 제거 (브로 제보).

### 💡 통찰 / 배운 점

**★ "코드 양 ≠ 학습 가치"** — step09 코드는 가벼웠지만 브로 코드 리뷰 12연타가 산출물 폭발:
- Pythonic 5종 (삼항, and, 튜플 언패킹, pipe, Pythonic≠짧게)
- coding_style.md 6항목 (레이아웃/제어흐름/철학/모듈시스템)
- 방어막 3겹 (layered defense) + as_array와의 협력
- AGENTS.md "AI 코드 작성 시 빈 줄 자동 적용" 원칙 신설

**★ Define-by-Run 본질 심화** (RESEARCH_QUEUE 6번 거의 완벽 가이드로 자람):
- 브로 혼란 "만들어진 그래프에 신규 입력?" = Define-and-Run 상상 (TF 1.x 직관)
- Define-by-Run = 매 입력마다 새 그래프 = FP 철학 (불변성, pipe와 같은 결)
- 가중치 매핑: W도 Variable (그래프 원점), 역전파가 원점에 grad 채움
- 그래프 구축 비용: 작은 모델에선 병목, 큰 모델+GPU에선 "껌" (조건부)
- 유연성 > 비용 트레이드오프. torch.compile/jax.jit이 "둘 다 잡기" 시도.
- ★ 브로 자가 도달 통찰 3종 (가중치 재사용/Optimizer 순회/그래디언트 순간성)

**★ 책 vs rezero+AI 학습 철학** — 일방향 매체(책)의 본질적 한계 (대화불가/순서고정/메타질문불가/사전지식가정/개인화불가). rezero+AI의 쌍방향 질문-응답이 극복. AGENTS.md에 프로젝트 존재 이유로 천명.

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/10
- 구현: `rezero/steps/step09.py`
- 정답지: `steps/step09.py`
- 이전 step: step08 역전파 반복문 — Issue 9
- 🔧 REZERO_CHANGES.md 항목 1번 정정 (isinstance step37→step09 도입)
- 📐 코딩 스타일: [notes/coding_style.md](./notes/coding_style.md) 항목 2~6 (Pythonic 시리즈 + import 위치)
- 🔬 RESEARCH_QUEUE 6번: Define-by-Run 본질 심화 (가중치 매핑, 그래프 비용, torch.compile 등)


### 📝 코드 / 수식 메모

**step09 새 기능 4종**:
```python
# 1. as_array 헬퍼 (삼항 1줄화 — 항목 2)
def as_array(x: object) -> np.ndarray:
    return np.array(x) if np.isscalar(x) else x  # type: ignore[return-value]

# 2. square/exp wrapper — Function 1단계 사용 (★ 사용성 핵심)
def square(x: Variable) -> Variable: return Square()(x)
def exp(x: Variable) -> Variable: return Exp()(x)

# 3. Variable.__init__ isinstance (방어막 2번, and 결합 — 항목 3)
if data is not None and not isinstance(data, np.ndarray):
    raise TypeError(...)

# 4. ★ pipe 헬퍼 (브로 제안, Haskell/Elixir 스타일)
def pipe(value, *funcs):
    return reduce(lambda val, f: f(val), funcs, value)
# pipe(x, square, exp, square) = square(exp(square(x)))
```

**방어막 3겹 (layered defense)**: 정적(타입힌트) + 동적타입(isinstance) + 동적None(가드).
as_array가 스칼라→ndarray 정규화로 isinstance 통과 보조 → 3겹이 협력.

**검증**: `square(exp(square(0.5)))` → `x.grad = 3.297442541400256` (step08과 동일, 해석적 정답).
`Variable(1.0)` → TypeError 정상. pipe 비교 → 두 스타일 결과 동일 (True).

**키워드**: `#함수사용성개선` `#as_array` `#square-wrapper` `#isinstance` `#방어막3겹` `#layered-defense` `#pipe` `#FP합성` `#Pythonic` `#삼항` `#and결합` `#튜플언패킹` `#Pythonic≠짧게` `#import위치` `#순환참조` `#죽은import` `#Define-by-Run` `#가중치매핑` `#그래디언트순간성` `#그래프구축비용` `#torch.compile` `#책vs-rezero+AI` `#코드양≠학습가치`


---

## Step 10 — [1고지] 테스트 (unittest로 동작 검증) ★ 1고지 마지막 — 완료!

**Issue**: [#11](https://github.com/ghjang/deep-learning-from-scratch-3/issues/11)
**완료일**: 2026-07-29
**상태**: ✅ ★ 1고지 전체 완료 (step01~10)

### 📖 요약 (한 줄)

새 기능이 아니라 **"검증 도구"** 도입 — pytest(국룰, 책의 unittest 대신) + gradient check로 step01~09 구축을 신뢰할 수 있게 만드는 1고지의 "완결성 인증". `numerical_diff`(step04 재등장, 복선 회수)와 역전파(해석적 미분) 결과를 비교해 구현이 맞는지 독립적으로 검증.

### ❓ 질문 / 막힌 점

- ✅ "밑시딥 3권이 좀 됐는데 unittest가 여전히 유효?" → 유효하나 실무 국룰은 pytest. 책의 교육적 선택 vs 실무 국룰 (탐구 17번).
- ✅ "책의 unittest 대신 pytest로?" → 브로 결정: 국룰 pytest로 가자. 책 코드는 역호환 실행 가능.
- ✅ Pylance `x.grad` Optional 빨간줄 (3곳 테스트 + 1곳 데모) → `assert x.grad is not None` (타입 좁히기). `# type: ignore` 아님.
- ✅ "assert에 런타임 처리(if raise)도 필요?" → 아니. y0/y1은 불변조건(assert), x.data는 사용자 오용(if/raise) — 용도에 따른 도구 선택.
- ✅ 빈 줄 누락 (numerical_diff) → 3개 논리 블록 분리 (AGENTS.md 원칙 위반 스스로 잡음).

### 💡 통찰 / 배운 점

**★ gradient check = 1고지 "품질 보증"** — 역전파(해석적)와 수치 미분(독립적 방법)이 일치 → step01~09 모든 구현 신뢰. 이게 없으면 "내가 짠 게 맞나?" 의문 남음.

**★ pytest 도입 = "책 시대 한계" 극복** — 책(2020년)은 교육용 unittest, 실무(2026년)는 pytest 국룰. 역호환 덕분에 둘 다 잡는 하이브리드 전략 (탐구 17번).

**★ assert = 정적 분석과 "협력"** — `# type: ignore`(억압) 대신 `assert x.grad is not None`(협력) 로 타입 좁히기. 일석삼조: 정적 분석 만족 + 불변조건 명시 + 런타임 검증. debugging.md 항목 1 보강.

**★ 방어막 None 가드 일관 적용** — 5곳(`__call__`/`backward`/`fill_grad`/`numerical_diff` + 테스트 4곳 assert). 같은 패턴이 코드 전체로 전파되는 구조.

**★ "과거 step 보존, 현재 step 반영" 원칙** — step04 numerical_diff는 그 시점 기록으로 보존, step10에서 as_array 보강 (step09 isinstance 도입으로 암묵적 깨짐 해결). 코드 진화가 step 단위로.

### 🔗 관련 링크

- Issue: https://github.com/ghjang/deep-learning-from-scratch-3/issues/11
- 구현: `rezero/steps/step10.py`
- 정답지: `steps/step10.py`
- 이전 step: step09 Function 사용성 개선 — Issue 10
- step04 numerical_diff 재등장 (gradient check용 복선 회수)
- 🔧 rezero 변형 항목 14번 (fill_grad 전역 함수) — 테스트에서 검증
- 🧪 탐구 17번: [notes/exploration_17_python_testing.md](./notes/exploration_17_python_testing.md) (unittest vs pytest 패러다임)
- 🐛 debugging.md 항목 1 보강 (정적 분석과 협력하는 assert — 타입 좁히기)


### 📝 코드 / 수식 메모

**pytest 스타일 테스트 (책의 unittest 대신 국룰)**:
```python
def test_square_gradient_check():
    x = Variable(np.random.rand(1))
    y = square(x)
    fill_grad(y)
    assert x.grad is not None              # ★ 불변조건 (Pylance 타입 좁히기)
    num_grad = numerical_diff(square, x)
    assert np.allclose(x.grad, num_grad)   # 역전파 == 수치 미분 → 신뢰
```

**검증**: pytest 5 passed (forward/backward/gradient check + 합성 + pipe).
역전파(1.0) vs 수치 미분(0.9999...) 일치 (x=0.5, square 미분 2x=1.0).

**키워드**: `#테스트` `#pytest` `#unittest대신국룰` `#gradient-check` `#역전파신뢰` `#수치미분비교` `#numerical_diff` `#step04복선회수` `#방어막None가드` `#assert타입좁히기` `#정적분석협력` `#type-ignore아님` `#과거step보존` `#1고지완결성인증` `#책시대한계`


---

## Step 11 — [2고지] 가변 길이 인수 (인수/반환값 여러 개)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 12 — [2고지] 가변 길이 인수 개선

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 13 — [2고지] 가변 길이 인수 역전파

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 14 — [2고지] 같은 변수 반복 사용 (누적 gradient)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 15 — [2고지] 복잡한 계산 그래프 이론 [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 16 — [2고지] 복잡한 계산 그래프 구현 (generation)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 17 — [2고지] 메모리 관리와 순환 참조 (weakref)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 18 — [2고지] 메모리 절약 모드 (Config, no_grad)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 19 — [2고지] Variable 사용성 개선 (이름, len, repr)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 20 — [2고지] 연산자 오버로딩(1) (__add__, __mul__)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 21 — [2고지] Variable 사용성 추가 (인덱스, shape 등)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 22 — [2고지] 연산자 오버로딩(2) (neg, sub, div, pow)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 23 — [2고지] packages로 묶기 (dezero 패키지화)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 24 — [2고지] 복잡한 함수 표현 (Sphere, Rosenbrock)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 25 — [3고지] '정답지 같은' 코드 [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 26 — [3고지] DeZero의 핵심 (core_simple.py 직접 구현)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 27 — [3고지] 지수/로그 함수 (Exp, Log)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 28 — [3고지] 함수 최적화 (경사하강법)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 29 — [3고지] 뉴턴 방법 (2차 최적화)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 30 — [3고지] 최적화 자동화 (2차 미분 자동)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 31 — [3고지] 다른 최적화 기법 (직접 구현) [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 32 — [3고지] 다른 함수 최적화 (뉴턴 적용)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 33 — [3고지] 행렬의 미분 이론

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 34 — [3고지] 벡터의 내적 / 행렬의 곱

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 35 — [3고지] 행렬의 미분 구현 (MatMul)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 36 — [3고지] 고차 미분 이론

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 37 — [4고지] 고차 미분 구현 (1) (Variable.data를 ndarray로)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 38 — [4고지] 고차 미분 구현 (2) (연산자 오버로딩/형상)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 39 — [4고지] 뉴런 한 개 역전파 검증 (gradient check)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 40 — [4고지] 신경망 구축 (은닉층, 활성화)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 41 — [4고지] 텐서 (다차원 배열) 다루기

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 42 — [4고지] 토이 데이터셋 (계단 함수 데이터)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 43 — [4고지] 신경망의 전체 그림 (개요)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 44 — [4고지] Dataset 클래스 구현

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 45 — [4고지] DataLoader 구현 (미니배치)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 46 — [4고지] 신경망 추론 (predict)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 47 — [4고지] 학습 루프 (loss, backward, update)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 48 — [4고지] 다층 신경망 (MLP)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 49 — [4고지] Layer 클래스 도입

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 50 — [4고지] Parameter 클래스 도입

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 51 — [4고지] Model 클래스 도입

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 52 — [5고지] MLP 클래스 정리

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 53 — [5고지] VGG16 구현

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 54 — [5고지] ResNet (skip connection)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 55 — [5고지] 합성곱 연산 효율화 이론 [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 56 — [5고지] im2col 이론 [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 57 — [5고지] im2col 구현 (Conv2d)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 58 — [5고지] CNN 구현 (SimpleConvNet)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 59 — [5고지] ResNet 구현

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 60 — [5고지] 마무리 (정리, 다음 단계)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

