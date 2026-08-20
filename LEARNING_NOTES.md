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
| 18 | step15 진행 중 | 그래프/DAG/DFS/BFS/위상정렬 (DeZero 계산 그래프 = DAG, 역전파 = 역방향 위상 정렬, generation = 표현식 중첩 깊이) | [notes/exploration_18_graph_traversal.md](./notes/exploration_18_graph_traversal.md) |
| 19 | step16 진행 중 | 네이밍과 헝가리안 표기법 (Systems vs Apps Hungarian, 현대 Pythonic "이름은 역할, 타입은 힌트에", 크로스 참조 네이밍 시도/철회 교훈) | [notes/exploration_19_naming_hungarian.md](./notes/exploration_19_naming_hungarian.md) |
| 20 | step16 완료 후 | Node 상위 클래스 도입 아이디어 (계산 그래프 추상화 경계, Pythonic vs OOP, 간선 비대칭 문제, manim 시각화 시너지, Node vs 이터레이터 옵션 매트릭스) 💡보류 | [notes/exploration_20_node_class_idea.md](./notes/exploration_20_node_class_idea.md) |
| 21 | step16 완료 후 | yield, 제너레이터, 코루틴 (이터레이터 프로토콜, yield 문법, lazy evaluation, 코루틴 3세대 진화 yield→yield from→async/await, 벤다이어그램 관계) | [notes/exploration_21_yield_generator_coroutine.md](./notes/exploration_21_yield_generator_coroutine.md) |
| 22 | step17 진행 중 | weakref와 GC (약한 참조의 마법, CPython Py_INCREF 스킵 + ob_weakreflist 구독자 모델, 참조 카운팅 vs 순환 감지 세대별 GC, 딥러닝 큰 ndarray 특수성, C++/Rust 비교) | [notes/exploration_22_weakref_gc.md](./notes/exploration_22_weakref_gc.md) |
| 23 | step18 진행 중 | 컨텍스트 매니저와 contextlib (yield가 with를 만드는 마법, __enter__/__exit__ vs @contextmanager+yield, 제어 양보 지점으로서 yield, _GeneratorContextManager 내부, async with, PyTorch no_grad 패턴) | [notes/exploration_23_contextmanager.md](./notes/exploration_23_contextmanager.md) |
| 24 | step18 진행 중 | 전략/이터레이터 패턴 + "결정 시점" 딜레마 (Config if문=인라인 전략 선택, 이터레이터 vs 전략 경계 모호성, 결정 시점 4층위 if문/생성시점/wrapper/전역, with no_grad가 런타임 if문 요구하는 이유, DI/PyTorch 합리적 타협, 브로 머리 꼬임=패턴 인식) | [notes/exploration_24_strategy_iterator_config.md](./notes/exploration_24_strategy_iterator_config.md) |
| 25 | step21 진행 중 | `__array_priority__`의 정체 (책 매직 넘버 200은 왜 불필요해졌나, ufunc/rmul 3세대 역사, NEP 13, "책 코드도 검증하라" 교훈) | [notes/exploration_25_array_priority.md](./notes/exploration_25_array_priority.md) |
| 26 | step22 진행 중 | 파이썬 숫자 계보 + 오일러 공식 + ★★★ "무한 번 미분 가능성 ↔ 기울기 소실" (부드러움의 역설, sigmoid vs ReLU) | [notes/exploration_26_numbers_complex.md](./notes/exploration_26_numbers_complex.md) |

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
  - (B)(C) f.input/output, y.grad None → **불변조건** (프로그래머 논리 버그) → assert 유지
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
        assert x is not None and y is not None   # 불변조건 (B) — 프로그래머 논리 가정
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

## Step 11 — [2고지] 가변 길이 인수(순전파 편) ✅

**Issue**: [#12](https://github.com/ghjang/deep-learning-from-scratch-3/issues/12)
**완료일**: 2026-07-30
**상태**: ✅ 완료

> ★ 제2고지 "자연스러운 코드로" 의 첫 단추. step11~13이 "가변 길이 인수" 3부작
> (step11 순전파 → step12 개선 → step13 역전파). step11은 **순전파만** 집중.
> ★ 브로 정정: 원 제목 "가변 길이 인수 (인수/반환값 여러 개)" → **"가변 길이 인수(순전파 편)"** 이 정확.

### 📖 요약 (한 줄)

`Function.__call__` 입출력을 `Variable` → `list[Variable]`로 일반화. Add(다입력 함수) 도입. apply hook 다변 일반화 성공.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★ **방향 (B) 확정**: apply/derivative hook 구조를 다변 인수로 일반화하는 실험 (Issue #12)
- ★ **책의 "구조 리셋" 인지**: step11~13은 다변 인수 구조로 Function을 다시 쌓아올리는 단계
  - `Variable.backward()` 자동화 ❌ (step13에서 다변 버전으로 재도입)
  - `fill_grad` 전역 함수 ❌ (이번 step 사용 안 함) — forward에 집중
- ★ **pipe 보류 결정**: 다입력 함수엔 단일 흐름 pipe가 안 맞음 → step11~22 제외, step23 재도입 (Issue #13)
  - compose / partial binding / bind FP 화두 step23 시점으로 미룸
- ★★ **Add = "가장 단순한 다변수 함수"** — `+`를 다변수 함수로 보는 시선 전환 (브로 통찰)
  - 보통: `+`는 "두 수 합치는 연산자". 수학/프레임워크: $\text{Add}: \mathbb{R}^2 \to \mathbb{R}$ 다변수 매핑
  - 모든 이항 연산(`+`, `*`, `max`)은 $\mathbb{R}^2 \to \mathbb{R}$ 함수로 승격 가능 ("연산 = 함수" 동치)
  - 이 시선이 있으면 step13(Add 역전파), step20(연산자 오버로드), step54(ResNet skip)까지 이어짐
  - Add 역전파는 "들어온 걸 그대로 흘려보내는" 성질 ($\partial y/\partial x_0 = 1$) → skip connection 기초 (복선)
- ★ **다변 회수 루프 타입 좁히기 함정** (디버깅 노트 후보)
  - `for x: if x.data is None: raise` 가드 + 별도 `[x.data for x in inputs]` 컴프리헨션 회수 →
    Pylance가 가드의 타입 좁히기를 컴프리헨션까지 안 이어줌 → `xs: list[Optional]` 경고
  - 해결: 회수와 가드를 **같은 루프에** (`if...: raise` 후 `xs.append(x.data)`) → 흐름 따라잡음
  - step10 `fill_grad`의 `assert` 패턴과 다른, 다변 회수 루프 특유의 패턴
- ★ **책 구조에 대한 비판적 시선 — step11 "거시기함"** (브로 감상)
  - step12(개선)에서 금방 `Add(x0, x1)` 위치 인수로 흡수될 내용이라 **독립 장으로선 약함**
  - 책 특유의 "작게 쪼개서 진화" 스타일(step01~60 전부 이 패턴) — 교육적으론 이해되나
    rezero 입장에선 "step11+12 합쳐도 되지 않나?" 싶은 인위적 분할
  - 다만 이 가벼움이 **2고지를 빠르게 보고 반복하는 학습 전략**(브로 방침)과 맞물려 오히려 적합
- ★ **FP 유틸 도구함 이슈 파생** (Issue #14)
  - 언패킹 head/tail 논의 → DeZero의 FP적 뿌리 발견 → head/tail/compose/curry/bind 유틸 회수 이슈로
  - step23 패키지화 또는 탐구 모드에서 회수

### 🔗 관련 링크

- 진행 이슈: #12
- pipe 보류 + FP 화두: #13
- 정답지: steps/step11.py
- 이전 step: step10 (gradient check, 1고지 완료)

### 📝 코드 / 수식 메모

(step 진행하며 채울 것 — apply hook 다변 일반화 설계, Add 구현)

**키워드**: `#2고지시작` `#가변길이인수` `#순전파편` `#다입력함수` `#Add` `#방향B` `#apply hook다변일반화` `#pipe보류` `#책구조리셋`

## Step 12 — [2고지] 가변 길이 인수(개선 편) ✅

**Issue**: [#15](https://github.com/ghjang/deep-learning-from-scratch-3/issues/15)
**완료일**: 2026-07-30
**상태**: ✅ 완료

> step11~13 3부작 중 2번째. step11의 "거시기한" API를 자연스럽게 개선.
> ★ 브로 정정: "가변 길이 인수 개선" → **"가변 길이 인수(개선 편)"** 이 정확.

### 📖 요약 (한 줄)

step11의 리스트 기반 API를 `*inputs` 가변 인수로 자연스럽게 개선. apply도 `*xs`로 통일(브로 통찰). 출력 단일화. step11 "거시기함" 해소.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★ **apply 가변 인수 통일 결정** (브로 통찰) — forward가 `*xs` 가변 인수인데 apply가 리스트면 불일치.
  → apply도 `*xs`로 통일. Add.apply는 `def apply(self, x0, x1):` 직접 위치 인수.
- ★ **`*` 이중성** (함수 정의 vs 호출) — 같은 `*` 기호인데 문맥에 따라 반대:
  - 정의 `def f(*args)`: 여러 인수 **수집** → tuple
  - 호출 `f(*xs)`: 리스트/튜플 **풀어서** 전달 → 개별 인수
  - 브로 "파람 쪽 문맥은 가변인수, 파람명은 튜플 타입" — 정확
- ★ **step11 "거시기함" 해소 지점** — step12에서 `Add(x0, x1)` 자연스러운 위치 인수로.
- ★ **이중 언패킹 성능 통찰** (브로 질문에서 파생)
  - `__call__→forward→apply` 거치며 "수집→언패킹" 2회 반복 (브로 "불편한 사실" 정확)
  - 벤치마크: 이중 언패킹 133ns/call vs 직접 38ns/call = 3.5x 느림 (95ns 오버헤드)
  - **병목 아님**: NumPy 연산/Variable 생성이 수십~수백 배 비쌈 (Amdahl's law). 인자도 1~2개
  - **유연성 가치 > 95ns**: 부모 apply `*xs`가 자식 시그니처 호환성 보장. Knuth "premature optimization" 사례
  - 실제 프로덕션(PyTorch)은 Python 자체 우회(C++/CUDA)로 최적화 — 언패킹이 아니라 언어 전환

### 🔗 관련 링크

- 진행 이슈: #15
- 정답지: steps/step12.py
- 이전 step: step11 가변 길이 인수(순전파 편) — #12
- 언패킹 노트: exploration_07 A.7 (`*` 이중성 보강 완료)

### 📝 코드 / 수식 메모

- `__call__(*inputs)` 가변 인수 + 회수/가드 한 루프(step11 패턴 유지)
- `forward(*xs)` / `apply(*xs)` — 방향 (B) 시그니처 통일
- Add.apply `(x0, x1)` 직접 위치 인수, 단일값 반환 (`__call__`에서 튜플 정규화)
- Square.apply `(x)` — 단일 함수도 가변 인수 체계에 맞춤
- wrapper `add`/`square` — `assert isinstance(result, Variable)` 타입 좁히기
- 출력 단일화: `return outputs if len(outputs) > 1 else outputs[0]`

**키워드**: `#2고지` `#가변길이인수` `#개선편` `#가변인수` `#star-inputs` `#위치인수` `#출력단일화` `#apply가변인수통일` `#브로통찰` `#star이중성` `#튜플수집` `#언패킹전달` `#step11거시기함해소`

## Step 13 — [2고지] 가변 길이 인수(역전파 편) ✅

**Issue**: [#16](https://github.com/ghjang/deep-learning-from-scratch-3/issues/16)
**완료일**: 2026-07-30
**상태**: ✅ 완료

> step11~13 "가변 길이 인수" 3부작의 대미. step11~12 순전파에 이어 역전파 다변 버전 완결.
> ★★ step07부터 매달아둔 "derivative hook 운명"이 판가관 나는 결정적 시험대.
> ★ 브로 정정: "가변 길이 인수 역전파" → **"가변 길이 인수(역전파 편)"** 이 정확.

### 📖 요약 (한 줄)

fill_grad 다변 입력 진화 + derivative hook 시험대 통과(Add 상수함수) + self.output 단수화(스칼라 출력 명시). 3부작 대미.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★★ **derivative hook 시험대** — Add는 gy→(gy,gy) (1입력 2출력)이라 derivative 1줄 표현 불가.
  → "선택적 hook" 패턴: 단일(Square)은 derivative, 다변(Add)은 backward 직접.
  REZERO_CHANGES 항목 010~013 "최종 반영 보류"가 여기서 판가관.
- ★ **Add 역전파 우아함** — `return gy, gy` ("들어온 걸 그대로 양쪽에 흘려보내라").
  ∂y/∂x0=1, ∂y/∂x1=1. step11 "skip connection 기초" 복선 회수.
- ★ **zip 동시 언패킹** (A.7.6) — `for x, gx in zip(f.inputs, gxs)` 가 입력-grad 배분 핵심 이디엄.
- ★ **fill_grad 다변 진화** — output_grads 회수 + 언패킹 호출 + zip 배분. step08 구조의 자연스러운 확장.
- ★★★ **"다변 역전파 ≠ 다출력 역전파" 혼동 교훈** (step13 구현 중 발견)
  - "다변" = **입력이 여러 개** (Add: x0, x1). 출력은 여전히 스칼라 1개 → gy도 1개.
  - 내가 초안에서 "다변"을 "upstream도 여러 개"로 해석 → `backward(*gys)` 가변으로 너무 앞서감.
  - 브로가 3연속 지적으로 정정:
    1. "너무 나갔다" → backward(gy) 단일로 회귀 (스칼라 가정)
    2. "upstream_grad 써라" → #007 정체성 회복 (책 gy 그대로 안 씀)
    3. "출력 다변 가정하지 마라" → f.outputs 리스트 언패킹 → f.output 단수 직접 회수 (#019 신설)
  - ★ 학습 가치: 책이 self.outputs 복수형으로 "미리 나간" 구조를 둬서 혼란 발생.
    rezero는 step13 시점(스칼라)에 충실하게 self.output 단수로 가고,
    **step34+ 다출력 함수 등장 시 복수로 진화** (REZERO_CHANGES #019에 진화 체크리스트 명시).
- ★ **output 단수화 결정** (REZERO_CHANGES #019) — 스칼라 출력 명시 + Pylance 만족 + step34 진화 지점 명시
  - 책의 "미래 확장 대비 복수형" vs rezero의 "현재 시점 충실 단수형"
  - 브로 철학: "학습이니 우리 의도대로 가고, 잘못되면 뒷목 잡으며 배운다"

### 🔗 관련 링크

- 진행 이슈: #16
- 정답지: steps/step13.py
- 이전 step: step12 가변 길이 인수(개선 편) — #15
- derivative hook 운명: REZERO_CHANGES 항목 010~013
- 동시 언패킹(zip): exploration_07 A.7.6
- fill_grad 변형: REZERO_CHANGES 항목 014~017

### 📝 코드 / 수식 메모

- `fill_grad` 다변 입력 진화 — output_grads 회수 + f.output.grad 직접 + zip 배분
- `Function.backward(upstream_grad)` 단일 인자 (스칼라 출력 가정, 책 step13 충실)
- `derivative` 단일/튜플 자유 + 부모 정규화 (책 패턴 확장)
- Add.derivative `(lambda _: 1, lambda _: 1)` ★ 브로 상수함수 통찰 실현
- `self.output` 단수 (#019) — 스칼라 출력 명시, step34+에서 outputs 복수로 진화
- `partials` 변수명 — 편도함수(partial derivatives), 수학적 정확
- "가정/전제" 표 docstring에 명시 — 다른 세션 혼동 방지

**키워드**: `#2고지` `#가변길이인수` `#역전파편` `#3부작대미` `#fill_grad다변진화` `#Add역전파` `#gy-gy` `#skip-connection기초` `#derivative-hook시험대` `#선택적hook` `#zip동시언패킹` `#항목010~013판가관`

## Step 14 — [2고지] 같은 변수 반복 사용 ✅

**Issue**: [#17](https://github.com/ghjang/deep-learning-from-scratch-3/issues/17)
**완료일**: 2026-07-30
**상태**: ✅ 완료

> 가변 길이 인수 3부작(step11~13) 완결 후 새 패턴.
> 같은 Variable이 여러 곳에 쓰이면 gradient **누적** 필요.
> ★ 브로 정정: "같은 변수 반복 사용 (누적 gradient)" → **"같은 변수 반복 사용"** 이 정확 (책 제목).

### 📖 요약 (한 줄)

같은 Variable 반복 사용 시 gradient 누적(if None 패턴) + clear_grad() 도입 + Define-by-Run 가정 명시.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★ **gradient 누적** — `x.grad = input_grad` 대입 → 덮어쓰기 버그. `if None: 대입 else: 누적` 패턴.
- ★ **`+=` vs 명시적 `x.grad + gx`** — ndarray in-place 부작용 방지. 새 배열 생성이 안전.
- ★ **cleargrad()의 의미** — Variable 재사용 시 이전 grad 잔류 방지. 명시적 초기화.
- ★★ **clear_grad가 전제하는 Define-by-Run 가정** (브로 통찰)
  - clear_grad 존재 자체가 "계산 그래프는 순전파 시 매번 재생성" 가정을 전제
  - Define-by-Run: 순전파 실행 시점에 그래프 "생성" (cf. Define-and-Run은 미리 정의)
  - 같은 Variable로 2번째 forward → 새 그래프 + 이전 grad 잔류 → 잘못 누적
  - 그래서 clear_grad()로 초기화해야 올바른 역전파 결과
  - step13 가정(스칼라 출력)에 추가: "계산 그래프 매번 재생성" 가정
  - 상세: exploration_03/11/16 (Define-by-Run)

### 🔗 관련 링크

- 진행 이슈: #17
- 정답지: steps/step14.py
- 이전 step: step13 가변 길이 인수(역전파 편) — #16
- fill_grad 변형: REZERO_CHANGES 항목 014~017

### 📝 코드 / 수식 메모

- `Variable.clear_grad()` — grad 초기화 (#021 네이밍 일관성, 책 cleargrad → clear_grad)
- fill_grad 누적 로직 — `if x.grad is None: 대입 else: x.grad + downstream_grad` (명시적 +)
- `downstream_grads`/`downstream_grad` 변수명 — #007 upstream/downstream 대칭 완성
- if None 체크 이유 — `add(x,x)` 시 f.inputs=(x,x), zip이 같은 객체 2회 방문 → 누적 필요
- 가정 표 — Define-by-Run(그래프 매번 재생성) + 같은 Variable 반복 가능

**키워드**: `#2고지` `#같은변수반복사용` `#gradient누적` `#if-else패턴` `#cleargrad` `#ndarray-inplace` `#명시적덧셈` `#fill_grad확장`

## Step 15 — [2고지] 복잡한 계산 그래프(이론 편) ✅ [No code]

**Issue**: [#18](https://github.com/ghjang/deep-learning-from-scratch-3/issues/18)
**완료일**: 2026-07-30
**상태**: ✅ 완료

> ★ 이론 step — 코드 없음 (steps/step15.py = `# No code`).
> step16에서 generation 코드로 구현. step15는 "왜 필요한지" 이해 + 노트 정리.
> ★ 브로 정정: "복잡한 계산 그래프 이론" → **"복잡한 계산 그래프(이론 편)"** 이 정확 (책 제목).

### 📖 요약 (한 줄)

복잡한 계산 그래프(분기/합류)에서 역전파 순서 문제 + generation(위상 정렬)으로 해결하는 이론.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★★ **계산 그래프 = DAG** (Directed Acyclic Graph, 방향성 비순환 그래프)
- ★★ **역전파 순서 = 위상 정렬** (topological sort) — 의존성 순서 강제
  - 브로 "BFS?" → 반은 맞고 반은 다름. BFS와 비슷한 효과지만, 핵심은 generation 정렬
- ★ **현재 fill_grad의 문제** — worklist + LIFO pop = DFS. 선형 그래프는 OK, 분기/합류 그래프에선 순서 꼬임 가능
- ★ **generation(세대) 해법** — 순전파 깊이 기록, 역전파 시 generation 내림차순 정렬 → "출력에 가까운 노드부터" 확실히 처리
- ★★★ **generation = 표현식 중첩 깊이** (브로 통찰 — 책 15.3 그림 해석)
  - 책 15.3 그림(순전파 노드들에 "N세대" 주석) 보고 "왜 스택 프레임이 떠오르지?" 짚음
  - ★ 브로 직관 유효! 두 코드 패턴에 따라 두 관점이 있음:
    - 패턴 A (DeZero 사용법 `square(square(x))`): 순수 합성, 인자 먼저 평가 → "표현식 중첩 깊이"
    - 패턴 B (본문 안 호출 중첩 `a() { b() { c() } }`): ★ 진짜 스택 프레임 중첩 → "런타임 스택 깊이" (브로 직관 그대로 맞음)
  - DeZero는 패턴 A지만 "부모 gen + 1" 기록이 패턴 B의 스택 깊이와 정신적으로 같음
  - Define-by-Run 정수: 실행(Run)할 때마다 그래프 + generation 함께 결정 (런타임 값)
  - 상세: exploration_18 §6 "generation = 표현식 중첩 깊이" (두 패턴 비교 포함)
- ★★ **책 그림의 시각적 함정 — 2개 DAG 겹침** (브로 통찰)
  - 책 step15/16 그림이 "순환처럼" 보이는 건 **2개 DAG를 하나에 겹쳐 그린 것**
  - DAG 1 (순전파): Function.inputs/output에 간선 저장, 방향 ↓
  - DAG 2 (역전파): Variable.creator에 간선 저장, 방향 ↑
  - 순전파 한 번 실행으로 양쪽 DAG 동시 구축 (Define-by-Run 정수)
  - 실제론 사이클 없음 = DAG. 시각적 함정일 뿐
  - 상세: exploration_18 §6 "책 그림의 시각적 함정"

### 🔗 관련 링크

- 진행 이슈: #18
- 정답지: steps/step15.py (`# No code`)
- **★ 배경지식 탐구 노트**: [exploration_18_graph_traversal.md](./notes/exploration_18_graph_traversal.md) — 그래프 기본/DFS/BFS/위상정렬, step16 이해 위한 사전 학습
- 다음 step: step16 복잡한 계산 그래프 구현 (generation 도입)
- 기존 worklist: step08 항목 017 (design_patterns Worklist Algorithm)

### 📝 코드 / 수식 메모

(step15는 코드 없음 — 이해 노트 위주. step16에서 generation 구현)

**키워드**: `#2고지` `#복잡한계산그래프` `#이론편` `#No-code` `#DAG` `#위상정렬` `#topological-sort` `#generation` `#역전파순서` `#브로BFS이해반틀림` `#fill_grad확장필요` `#step16구현`

## Step 16 — [2고지] 복잡한 계산 그래프(구현 편) ✅

**Issue**: [#19](https://github.com/ghjang/deep-learning-from-scratch-3/issues/19)
**완료일**: 2026-07-31
**상태**: ✅ 완료

> ★ step15(이론 편)의 짝. generation + visited로 분기/합류 그래프 역전파 순서 문제를 코드로 해결.
> ★ 브로 정정: "복잡한 계산 그래프 구현" → **"복잡한 계산 그래프(구현 편)"** (step15 "(이론 편)"과 짝).

### 📖 요약 (한 줄)

generation(순전파 깊이)으로 역방향 위상 정렬 + visited(set)로 같은 Function 중복 처리 방지.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★★★ **두 방어막의 차이 — step14 누적 vs step16 visited (둘은 다른 문제!)**
  - **step14 누적**(if None: 대입 else: +): "같은 Variable이 하나의 Function에 여러 입력으로"
    - 예: `add(x, x)` → `f.inputs = (x, x)`. 같은 객체 2번 방문.
  - **step16 visited**(set): "같은 Function이 worklist에 여러 번 push"
    - 예: `add(square(a), square(a))` → `a.creator`가 두 번 push됨.
  - 계산 그래프의 **서로 다른 구조적 상황**을 해결하는 서로 다른 방어막. 둘 다 필요.
- ★★ **복선 회수 2종**:
  1. **REZERO_CHANGES 항목 012** — step07에서 "왜 set_creator를 단순 할당 말고 메서드로?" 의심.
     답: set_creator에 generation 로직이 추가되는 순간이 step16. step14 docstring "step16 generation 확장 포인트" 복선 회수.
  2. **exploration_18 §4.4** — 브로가 step15 탐구 때 "방문 기록(visited)이 왜 필요한가" 파고들었던 주제.
     책 원본 `seen_set`이 바로 그 visited의 실체.
- ★★★ **네이밍 셋트 완성** — `worklist` + `visited` + `schedule` = **그래프 순회 알고리즘 CS 학술 용어 3총사**
  - 책 원본: `funcs` / `seen_set` / `add_func` (제네릭, 의미 투명성 낮음)
  - rezero: `worklist` / `visited` / `schedule` → 코드만 봐도 "역방향 위상 정렬 중"이 드러남
  - 탐구 18번(exploration_18) 노트와 같은 단어 사용 → 코드 ↔ 노트 일관성
- ★ **generation = "출력에 가까운 순서" 보장의 도구**
  - 순전파 깊이를 런타임에 기록 (Define-by-Run 정수)
  - 역전파 시 `worklist.sort(key=generation)` → gen 큰 것(=출력에 가까운 것)부터 pop
  - 분기/합류 그래프에서 "아직 grad가 다 안 모인 Function"을 먼저 처리하는 버그 방어
- ★★★ **크로스 참조 네이밍 — 개명 시도/철회 교훈 (현대 Pythonic)** (브로 통찰 2종):
  - **통찰 1**: "creator가 모호하다" → `creator_func`/`input_vars`/`output_var`로 전면 개명 시도
  - **통찰 2 (핵심 자각)**: "변수명과 타입 힌트가 중복 느낌" → **Systems Hungarian**(변수명에 타입 박기) 냄새 자각
  - **최종 결정**: 책 원본 이름(`creator`/`inputs`/`output`) 유지 + 타입 힌트로 보완
  - ★ **현대 파이썬 철학**: "이름은 역할을 말하고, 타입은 힌트에 맡긴다"
    - `creator: Function` → creator(역할) + Function(타입 힌트) = 독립적 정보 ✅
    - `creator_func: Function` → func(타입 인코딩) + Function(타입 힌트) = 중복 ❌
  - ★ **학습 사이클의 가치**: 시도 → 자각 → 원칙 발견 → 회귀(이유 알고). 책 따라가는 것보다 깊음
  - 상세: [exploration_19_naming_hungarian.md](./notes/exploration_19_naming_hungarian.md)

### 🔗 관련 링크

- 진행 이슈: #19
- 정답지: steps/step16.py (결과 일치: `y.data=32.0, x.grad=64.0`)
- 이전 step: step15 복잡한 계산 그래프(이론 편) — generation 이론 배경
- **★ 배경지식 탐구 노트**: [exploration_18_graph_traversal.md](./notes/exploration_18_graph_traversal.md) — DAG/위상정렬/generation = 표현식 중첩 깊이 (§4.4, §6 회수)
- rezero 변형: REZERO_CHANGES 항목 022~024 (이번 step 신설)

### 📝 코드 / 수식 메모

**역전파 추적** (`y = add(square(a), square(a)), a = square(x), x=2.0`):
```
순전파: a=x²=4, b=c=a²=16, y=b+c=32 ✓
역전파:
  y 시드 = 1
  add:       b.grad=1, c.grad=1               (upstream 1을 양쪽에 그대로)
  square(b): db/da=2a=8 × 1 = 8 → a
  square(c): dc/da=2a=8 × 1 = 8 → a
  a.grad = 8 + 8 = 16                         (★ 두 경로 누적)
  square(a): da/dx=2x=4 × 16 = 64 → x
  x.grad = 64 ✓
```

**generation 값 검증** (순전파 깊이 = 표현식 중첩 깊이):
```
x(입력)           → gen 0
square(x)         → gen 0 (max(x.gen)=0).    a.gen = 0+1 = 1
square(a) #1, #2  → gen 1 (max(a.gen)=1).    출력들 gen = 1+1 = 2
add               → gen 2 (max(입력들)=2).    y.gen = 2+1 = 3
```

**키워드**: `#2고지` `#복잡한계산그래프` `#구현편` `#generation` `#visited` `#schedule` `#위상정렬` `#topological-sort` `#역방향` `#중복push방지` `#두방어막차이` `#복선회수항목012` `#복선회수탐구18` `#네이밍셋트`

## Step 17 — [2고지] 메모리 관리와 순환 참조 ✅

**Issue**: [#22](https://github.com/ghjang/deep-learning-from-scratch-3/issues/22)
**완료일**: 2026-07-31
**상태**: ✅ 완료

> ★ 브로 정정: "메모리 관리와 순환 참조 (weakref)" → **"메모리 관리와 순환 참조"** (weakref는 해법, 제목엔 안).

### 📖 요약 (한 줄)

순환 참조(Variable ↔ Function)로 인한 메모리 누수를 weakref(약한 참조)로 해결.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★★★ **브로 통찰 — weakref 도입은 출력 다변화와 별개** (내가 잘못 연결한 걸 브로가 정정)
  - weakref: 순환 참조 끊기용 (출력 개수 무관)
  - 출력 다변화: step34+ 진짜 다출력 함수(Split 등)와 무관
  - → 항목 019(self.output 단수)는 유지한 채 **단수 + weakref** 조합으로 진행 (항목 026)
- ★★ **파이썬 GC 두 단계** (브로 통찰 — "결국 처리한다")
  1. 참조 카운팅 (즉시, 순환 못 잡음)
  2. 순환 감지 GC (주기적 세대별, 순환 잡음)
  - 즉 순환 참조는 결국 회수됨. 근데 딥러닝 큰 ndarray는 GC 주기까지 기다리면 폭발 → weakref로 즉시 회수
- ★★ **weakref도 객체다** (브로 질문)
  - weakref.ReferenceType 인스턴스. 자기 자체 refcount도 있음.
  - 근데 대상 refcount는 **안 올림** — CPython이 Py_INCREF 호출 스킵
  - 마법: 대상 객체의 ob_weakreflist 슬롯에 "구독자"로 등록만 함. 대상 파괴 시 통지받아 None 반환.
- ★ **책의 비대칭 설계 — output만 weakref, inputs는 강한 참조 유지**
  - inputs: 역전파 시 inputs.data 접근에 반드시 필요 → 강한 참조
  - output: 역전파 시 grad 회수용, 그 후엔 안 씀 → weakref로 회수 허용
  - 이 비대칭이 메모리 효율과 역전파 정합성 동시 확보의 핵심
- ★ **우리 변형 — output 이름 유지, 타입 힌트만 진화** (항목 026)
  - 책: self.outputs = [weakref.ref(o)] (복수 리스트, 원래부터 복수였으니)
  - 초기 시도: self.output_ref (AI 제안) → 브로 "파이써닉하지 않아?" → ★ 헝가리안 자각 → 철회
  - 최종: self.output: Optional[weakref.ref] (이름은 output 그대로, 타입 힌트만 Variable→weakref.ref 진화)
  - step16 #025(creator_func 철회)와 같은 패턴 — 탐구 노트 19번 원칙 일관 적용
  - ★ 교훈: "원칙 수립 ≠ 원칙 준수" — step16에서 세운 원칙을 바로 다음 step에서 AI가 위반, 브로가 캐치
- ★★ **"원칙 준수" 3연속 위반 사태 (step17)** 🔥
  - 1차: output_ref 헝가리안 (위 항목)
  - 2차: pylance 경고 피하려고 `upstream_grad` 변수명 제거 (★ 항목 007 rezero 정체성 위반!)
    - 브로: "의미있는 변수 이름으로 가자는 우리 리제로의 특성 아니었어?"
    - 해결: `upstream_grad = output.grad` 할당 후 **변수에 직접 assert** (`assert upstream_grad is not None`)
    - → 변수명 유지 + pylance 타입 좁히기 인식 동시 만족
  - ★★ 핵심 교훈 (강화): "원칙 수립 ≠ 원칙 준수"는 단순 문서 작성 이상의 문제.
    **이미 합의된 원칙(항목 007)을 pylance 경고 하나 피하려고 버리는 순간**이 가장 위험.
    정적 분석 도구 경고 ≠ 원칙 위반 정당화. 변수명/구조 정체성이 우선.

### 🔗 관련 링크

- 진행 이슈: 22번
- 정답지: steps/step17.py (메모리 누수 없으면 출력 없음 = 성공)
- 이전 step: step16 (generation/visited)
- **★ 심화 탐구 노트**: [exploration_22_weakref_gc.md](./notes/exploration_22_weakref_gc.md) — weakref/GC/CPython 내부 (브로 3질문 답)
- rezero 변형: REZERO_CHANGES 항목 019 (output 단수 유지), 026 (weakref 도입)

### 📝 코드 / 수식 메모

**weakref 도입 (3군데)**:
```python
import weakref
# Function.__call__:
self.output_ref = weakref.ref(output)   # 단수, 약한 참조 (항목 019 + 026)
# fill_grad 회수:
output = f.output_ref()                  # 역참조 (호출로 실제 객체, 또는 None)
```

**순환 참조 구조**:
```
Variable ──creator──→ Function ──inputs──→ Variable (강한 참조, 유지)
       ↑                                        │
       └──── output_ref (weakref, 약한) ────────┘
       ★ output 방향만 weakref → 순환 끊김
```

**키워드**: `#2고지` `#메모리관리` `#순환참조` `#weakref` `#약한참조` `#output_ref` `#항목019유지` `#항목026` `#순환감지GC` `#세대별GC` `#딥러닝특수성` `#즉시회수` `#브로정정weakref별개`

---

## Step 18 — [2고지] 메모리 절약 모드 ✅

**Issue**: [#23](https://github.com/ghjang/deep-learning-from-scratch-3/issues/23)
**완료일**: 2026-07-31
**상태**: ✅ 완료

### 📖 요약 (한 줄)

추론(역전파 안 함) 시 계산 그래프 생성 생략(Config/no_grad) + 중간 grad 버리기(retain_grad)로 메모리 절약.

### ❓ 질문 / 막힌 점

- (step 진행하며 업데이트)

### 💡 통찰 / 배운 점

- ★★ **핵심 문제 — 역전파 안 할 때도 그래프 만들면 메모리 낭비**
  - step17까지는 순전파만 해도 역전파 대비 그래프(creator/inputs/output weakref) 구축
  - 추론(predict)은 y.data만 필요한데 그래프까지 유지 → 큰 ndarray 시 폭발
- ★★ **해법 1 — Config 전역 플래그 + 그래프 구축 조건부** (`if Config.enable_backprop:`)
  - 역전파 안 할 땐 creator/inputs/output 세팅 안 함 → 그래프 안 생김 → 메모리 절약
- ★★ **사용자 인터페이스 — 컨텍스트 매니저 `with no_grad():`**
  - 매번 Config 바꾸면 까먹을 위험 → with 블록으로 안전하게 (finally 자동 복구)
  - cf. PyTorch `torch.no_grad()` 와 정확히 같은 패턴/이름
- ★ **추가 최적화 — retain_grad (중간 grad 버리기)**
  - 보통 역전파는 최종 입력 grad만 필요. 중간 Variable grad는 안 씀
  - retain_grad=False(기본): 중간 grad를 None으로 버림 → 큰 ndarray 메모리 해제
- ★★ **`@contextlib.contextmanager` + `yield` 마법** (탐구 23번으로 심화)
  - yield가 "값 내보내기"가 아니라 **"with 블록 본문에 제어 넘기고, 끝나면 이어서"** (제어 양보 지점)
  - yield 이전 = `__enter__`, yield 이후 = `__exit__` (try/finally로 예외 안전)
  - 탐구 21번(yield/코루틴)과 연결 — "yield 본질 = 실행 일시정지 지점"
- ★ **우리 변형 — fill_grad에 retain_grad 매개변수 확장** (항목 014 유지)
  - 책: `y.backward(retain_grad=False)` (Variable 메서드)
  - 우리: `fill_grad(y, retain_grad=False)` (전역 함수, 정체성 유지하며 자연스럽게 확장)
  - ★ 키워드 전용 인자(`*`)로 retain_grad 받아 위치 인자 헷갈림 방지
- ★ **이번엔 변형 최소** (A/B/C 책 방식 그대로, D만 우리 정체성)
  - step17의 4연속 위반 교훈 살려 정체성 위반 없이 깔끔하게 진행

### 🔗 관련 링크

- 진행 이슈: 23번
- 정답지: steps/step18.py (`None None / 2.0 1.0` — 우리 케이스 1과 일치)
- 이전 step: step17 (weakref 순환 참조 해결)
- **★ 심화 탐구 노트**: [exploration_23_contextmanager.md](./notes/exploration_23_contextmanager.md) — contextlib/yield 마법 (탐구 21번과 연결)
- rezero 변형: REZERO_CHANGES 항목 014 (fill_grad — retain_grad 매개변수 확장), 027 (Config/no_grad 도입)

### 📝 코드 / 수식 메모

**Config + no_grad 패턴**:
```python
class Config:
    enable_backprop: bool = True

@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield                        # with 블록 본문에 제어 넘김
    finally:
        setattr(Config, name, old_value)  # 자동 복구 (예외에도)

def no_grad():
    return using_config('enable_backprop', False)
```

**Function.__call__ 조건부 그래프 구축**:
```python
if Config.enable_backprop:
    output.set_creator(self)
    self.inputs = inputs
    self.output = weakref.ref(output)
return output  # no_grad 블록에선 이것만 (그래프 안 만듦)
```

**키워드**: `#2고지` `#메모리절약` `#Config` `#no_grad` `#enable_backprop` `#컨텍스트매니저` `#contextlib` `#yield` `#제어양보` `#retain_grad` `#중간grad버리기` `#PyTorch패턴` `#항목014확장` `#탐구23` `#탐구21연결`

---

## Step 19 — [2고지] 변수 사용성 개선

**Issue**: [#24](https://github.com/ghjang/deep-learning-from-scratch-3/issues/24)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

Variable에 name/`__len__`/`__repr__`/shape/ndim/size/dtype 추가 — 모두 내부 ndarray(self.data)에 **위임(delegate)** 하는 패턴. 역전파 로직은 건드리지 않음.

### 💡 통찰 / 배운 점

- **위임 패턴(delegate pattern)** — Variable이 ndarray를 품고, 매직메서드/property는 "data한테 물어봐" 하고 떠넘김. 파이썬에선 `@property`와 매직메서드(`__len__`)가 이 위임의 도구. 기억에서 날아갔던 용어 다시 복구 ★
- **"순수 데이터 상자" 정체성 강화** — name/property는 데이터 자체에 대한 정보/표현이라 Variable 정체성(항목 014)에 위배되지 않고 오히려 강화. 그래프 순회가 아님.
- **`Variable(` 대문자 repr (변형 E)** — 책 원본은 소문자 `variable(` 하드코딩(chainer 관례 추정). 브로 결정으로 클래스명 그대로 `Variable(` 사용. 우연히 글자 수(9칸)가 같아 들여쓰기 매직 넘버는 안 바뀜.
- **`_ensure_data` 헬퍼 네이밍 토론** — 브로가 "무난한 거 맞냐?" 재질문 → 후보 6종 검토 → `_ensure_data` 합의. "ensure = 보장하다"가 가드 역할(data 있음을 보장)에 정확. 네이밍은 항상 트레이드오프.
- **키워드 전용 매개변수 패턴 (2번째 사례)** — step18 retain_grad에 이어 step19 name도 `*, name=None` 키워드 전용. 아직 "원칙"은 아니고 관찰 수준 (3~4곳 쌓이면 원칙화 검토).

### 🔗 관련 링크

- [Issue #24](https://github.com/ghjang/deep-learning-from-scratch-3/issues/24) — step19 진행 추적
- `REZERO_CHANGES.md` 항목 #028 (name 키워드 전용), #029 (property None 가드 + `_ensure_data`), #030 (`Variable(` 대문자 repr)
- `rezero/steps/step19.py` — 구현

### 📝 코드 / 수식 메모

```python
# 위임 패턴의 핵심 — 모두 _ensure_data()로 None 가드 후 data에 떠넘김
@property
def shape(self) -> tuple[int, ...]:
    return self._ensure_data().shape

def _ensure_data(self) -> np.ndarray:
    if self.data is None:
        raise RuntimeError(...)   # 방어막 일관성 (step09 방어막 3겹 연장)
    return self.data

# __repr__은 헬퍼 안 쓰고 자체 처리 (None도 표현해야 하므로)
def __repr__(self) -> str:
    if self.data is None:
        return 'Variable(None)'
    p = str(self.data).replace('\n', '\n' + ' ' * 9)   # 들여쓰기 매직 넘버 9 = 'Variable(' 길이
    return 'Variable(' + p + ')'
```

**키워드**: `#2고지` `#변수사용성개선` `#위임패턴` `#delegate` `#property` `#매직메서드` `#__len__` `#__repr__` `#name` `#shape` `#ndim` `#size` `#dtype` `#키워드전용` `#방어막일관성` `#_ensure_data` `#항목028` `#항목029` `#항목030`

---

## Step 20 — [2고지] 연산자 오버로드(1)

**Issue**: [#25](https://github.com/ghjang/deep-learning-from-scratch-3/issues/25)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

Variable에 `__add__`/`__mul__` 매직메서드 추가 → `y = a * b + c` 처럼 수학 식처럼 자연스럽게. Mul 클래스 신규 + 연산자 오버로딩 도입. 2고지 "자연스러운 코드로"의 핵심 달성.

### 💡 통찰 / 배운 점

- **연산자 = 매직메서드의 신택스 슈가** — `a + b` 는 사실 `a.__add__(b)`. 클래스에 매직메서드 정의하면 그 객체에 연산자 사용 가능. 파이썬 데이터 모델의 핵심.
- **★★ "클래스 밖 대입" vs "클래스 안 정의" — pyright 11 에러 실증** — 책 원본이 `Variable.__add__ = add` (클래스 밖 대입) 방식을 써서 따랐더니 pyright 11 에러 폭발. 정적 분석기가 클래스 밖 대입을 인식 못 함. 클래스 안 정의로 0 에러. **"책 원본 방식이 항상 권장은 아니다"** 교훈. coding_style.md 섹션 7 + AGENTS.md 작업 원칙으로 영구화.
- **Mul derivative hook (항목 013 재평가 통과)** — Add(상수 1)에서 Mul(다른 입력값 x1/x0)로 확장되어도 derivative hook이 자연스럽게 커버. `derivative() -> (lambda _: x1, lambda _: x0)` — 호출 시점에 값이 고정되므로 상수함수로 표현. step34 행렬 미분이 다음 재평가 시점.
- **브로 결정 흐름 (초기→실증→확정)** — "책 방식으로 가자" → pyright 11 에러 → "비추라는 소리군" → "본체 클래스 안 + 기록 + 작업 원칙". 코드 짜봐야 가시화되는 트레이드오프.

### 🔗 관련 링크

- [Issue #25](https://github.com/ghjang/deep-learning-from-scratch-3/issues/25) — step20 진행 추적
- `REZERO_CHANGES.md` 항목 #031 (매직메서드 클래스 안 정의), #032 (Mul derivative hook 재평가)
- `notes/coding_style.md` 섹션 7 — "매직메서드는 클래스 안에 정의" 작업 원칙
- `AGENTS.md` — "★ 매직메서드는 클래스 안에 정의 (필수)" 작업 원칙 추가

### 📝 코드 / 수식 메모

```python
# 연산자 = 매직메서드의 신택스 슈가
# a + b  →  a.__add__(b)
# a * b  →  a.__mul__(b)

# 클래스 안 정의 (권장 — pyright 0 에러)
class Variable:
    def __add__(self, other: "Variable") -> "Variable":
        return add(self, other)    # wrapper에 위임

# Mul derivative — 다른 입력값 캡처 (항목 013 재평가 통과)
class Mul(Function):
    def derivative(self) -> tuple[Callable, ...]:
        assert self.inputs is not None    # 정적 분석용 타입 좁히기
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return (lambda _: x1, lambda _: x0)   # ∂y/∂x0=x1, ∂y/∂x1=x0
```

**키워드**: `#2고지` `#연산자오버로드` `#매직메서드` `#__add__` `#__mul__` `#신택스슈가` `#파이썬데이터모델` `#Mul` `#클래스안정의` `#pyright11에러` `#항목031` `#항목032` `#항목013재평가` `#coding_style섹션7`

---

## Step 21 — [2고지] 연산자 오버로드(2)

**Issue**: [#26](https://github.com/ghjang/deep-learning-from-scratch-3/issues/26)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

Variable에 `__radd__`/`__rmul__` 역순 연산자 + `as_variable` 헬퍼 추가 → `x + 3.0`, `3.0 * x + 1.0`처럼 ndarray/scalar와 자유롭게 섞어 쓰는 수학 식. ★ `__array_priority__ = 200`은 탐구 25번으로 불필요 증명되어 버림.

### 💡 통찰 / 배운 점

- **★★★ `__array_priority__ = 200`은 현대에 불필요** — 책이 쓴 매직 넘버는 과거 NumPy(NotImplemented 안 반환하던 시절)용 핵. 현대엔 `__rmul__`만으로 충분. 실험(NaiveVar)으로 증명. 탐구 25번으로 영구 보존. **"책 코드도 검증하라" 교훈의 결정적 사례.**
- **역순 연산자 `__radd__`/`__rmul__`** — `3.0 * x` → float.__mul__ 실패 → `x.__rmul__(3.0)`. 교환법칙 성립 연산(+, *)이라 `add`/`mul` wrapper와 동일.
- **as_variable 헬퍼 2층 구조** — as_variable(ndarray/scalar → Variable) 위에 as_array(스칼라 → ndarray). Function.__call__ 도입부에서 입력 정규화.
- **wrapper as_array 중복 제거** — 브로 "중복은 없애는 게 좋다" + 실험 검증. Function.__call__의 as_variable이 변환 책임을 지면 wrapper에서 또 변환할 필요 없음. ★ 점진적 설계의 잔재 정리 — 책은 step20까지의 as_array를 step21에서도 그대로 둠 (정리 누락), 우리는 제거.
- **step20 작업 원칙 자동 적용 첫 사례** — `__radd__`/`__rmul__`을 클래스 안에 정의. AGENTS.md "매직메서드는 클래스 안에 (필수)"가 시스템으로 작동.

### 🔗 관련 링크

- [Issue #26](https://github.com/ghjang/deep-learning-from-scratch-3/issues/26) — step21 진행 추적
- [exploration_25_array_priority.md](./notes/exploration_25_array_priority.md) — `__array_priority__` 200 불필요 + ufunc/rmul 역사 (★ 이번 step 최대 성과)
- `REZERO_CHANGES.md` 항목 #033 (`__array_priority__` 버림), #034 (`__radd__`/`__rmul__` 클래스 안 + wrapper as_array 중복 제거)

### 📝 코드 / 수식 메모

```python
# as_variable 헬퍼 (2층 변환 구조)
def as_variable(obj):
    if isinstance(obj, Variable): return obj
    return Variable(as_array(obj))      # Variable 생성자 → as_array

# Function.__call__ 도입부에서 입력 정규화
def __call__(self, *inputs):
    inputs_vars = tuple(as_variable(x) for x in inputs)   # ★ 여기서 변환 책임
    xs = [x.data for x in inputs_vars]
    ...

# 역순 연산자 (클래스 안 정의 — step20 항목 031 원칙 자동 적용)
def __radd__(self, other): return add(self, other)   # 교환법칙 → add와 동일
def __rmul__(self, other): return mul(self, other)

# ★ wrapper는 단순하게 (as_array 중복 제거)
def add(x0, x1):
    result = Add()(x0, x1)   # x1 스칼라/ndarray여도 Function.__call__이 처리
    ...
```

**키워드**: `#2고지` `#연산자오버로드` `#역순연산자` `#__radd__` `#__rmul__` `#as_variable` `#2층변환구조` `#__array_priority__버림` `#탐구25` `#중복제거` `#점진적설계잔재` `#책검증교훈` `#항목033` `#항목034`

---

## Step 22 — [2고지] 연산자 오버로드(3)

**Issue**: [#28](https://github.com/ghjang/deep-learning-from-scratch-3/issues/28)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

나머지 산술 연산자 전부 추가 — `-x`, `x - y`, `x / y`, `x ** c`. 4개 함수 클래스(Neg/Sub/Div/Pow) + 7개 매직메서드. 연산자 오버로딩 3부작 대미. ★ step20/21 원칙들(항목 031/033/034)이 대량(7개 매직메서드)으로 자동 적용 — "원칙 수립 → 준수" 사이클 검증.

### 💡 통찰 / 배운 점

- **★★★ 원칙 자동 적용 검증** — step20(항목 031: 매직메서드 클래스 안), step21(항목 033: `__array_priority__` 버림, 항목 034: wrapper as_array 제거)에서 확립한 3 원칙이 step22에서 **대량 7개 매직메서드**로 한 번에 적용. 사전에 세운 원칙이 시스템으로 작동함을 증명.
- **Div derivative hook** — `1/x1, -x0/x1²` (제곱 항). Mul(step20)보다 복잡한데도 hook으로 표현 가능 → 항목 013 재평가 또 통과.
- **Pow 특수 구조** — `__init__(c)`로 상수 c 저장. ★ 브로 리뷰 "커스텀은 c만, 나머지는 베이스가" → `super().__init__()` 호출로 DRY (부모에게 inputs/output/generation 위임).
- **Neg 단순화** — `lambda x: np.float64(-1.0) * x`로 브로드캐스팅에 위임 (브로 리뷰). 복잡한 브랜치 제거.
- **비교환 연산의 역순 처리** — rsub/rdiv는 순서 뒤집기. `rsub(x0, x1) = Sub()(x1, x0)`.
- **`__truediv__`의 "true"** — 파이썬 2 vs 3 나눗셈 역사. 탐구 26번에서 파생 → 오일러 공식 → "무한 미분 ↔ 기울기 소실" 통찰로 확장.
- **★ 부수 발견 — pyright 시그니처 엄격성** — `Callable[[ndarray], ndarray]` 단일 반환형은 엄격(int/float 에러), `tuple[Callable, ...]`는 관대. Square는 `2*x`가 float64 승격돼서 우연히 통과한 거였음. 향후 단일 입력 함수 작성 시 주의.

### 🔗 관련 링크

- [Issue #28](https://github.com/ghjang/deep-learning-from-scratch-3/issues/28) — step22 진행 추적
- [exploration_26_numbers_complex.md](./notes/exploration_26_numbers_complex.md) — 파이썬 숫자 계보 + 오일러 + ★★★ "무한 미분 ↔ 기울기 소실" 통찰
- `REZERO_CHANGES.md` 항목 #035 (Pow `super().__init__` DRY + Neg 단순화 + 3원칙 자동 적용 검증)

### 📝 코드 / 수식 메모

```python
# 비교환 연산의 역순 — 순서 뒤집기
def rsub(x0, x1):
    return Sub()(x1, x0)    # ★ x0 자리에 x1, x1 자리에 x0

# Pow — c는 상수 (Variable 아님)
class Pow(Function):
    def __init__(self, c):
        self.c = c                # 커스텀
        super().__init__()        # ★ DRY (브로 리뷰)
    def derivative(self):
        c = self.c
        return lambda x: c * x ** (c - 1)    # c·x^(c-1)

# derivative hook 4종 (복잡도 순)
Neg: lambda x: np.float64(-1.0) * x         # 단일, 브로드캐스팅
Sub: (lambda _: 1, lambda _: -1)           # Add 변형
Div: (lambda _: 1/x1, lambda _: -x0/x1**2) # 가장 복잡 (제곱)
Pow: lambda x: self.c * x**(self.c-1)      # self.c 참조
```

**키워드**: `#2고지` `#연산자오버로드` `#Neg` `#Sub` `#Div` `#Pow` `#__neg__` `#__sub__` `#__truediv__` `#__pow__` `#비교환` `#rsub_rdiv_순서뒤집기` `#super_init_DRY` `#원칙자동적용` `#항목031_033_034` `#탐구26` `#2고지대미`

---

## Step 23 — [2고지] 패키지로 정리

**Issue**: [#29](https://github.com/ghjang/deep-learning-from-scratch-3/issues/29)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

step01~22 코드를 `rezero/v1/` 패키지로 승격. ★ 브로 통찰 "고지별 버전 폴더(v1/v2/v3)" 구조 도입 — 학습 흔적 박제 + 재사용 가능한 패키지. 빈 템플릿 11개 삭제 + 순환 참조 해결(지연 import).

### 💡 통찰 / 배운 점

- **★★★ 버전 폴더 전략 (브로 제안)** — 각 고지 완료 시점의 프레임워크를 별도 폴더(v1/v2/v3)로 스냅샷. "최종 버전" 개념을 버리고, 고지별 스코프에 맞는 패키지를 유지. 추후 기억 날아가도 폴더만 보면 "아, v1은 2고지구나" 즉시 파악. git tag보다 파일 시스템에서 바로 보이는 게 학습자 관점에서 중요.
- **★★★ 순환 참조 — core.py ↔ functions.py** — core.py의 Variable 매직메서드가 functions.py의 wrapper를 호출하는데, functions.py는 core.py를 import함 → 순환 참조. ★ 해결: **지연 import(lazy import)** — 매직메서드 안에서 `from rezero.v1.functions import add` 호출. core.py 로드 시점엔 functions.py 안 부르고, 실제 연산 시점에 로드. dezero는 `setup_variable()`(클래스 밖 대입)로 해결했지만, 우린 클래스 안 정의 원칙(항목 031) 유지를 위해 지연 import 택함.
- **★ 주석 정리 기준 (API화)** — step 파일은 학습 흔적(상세 주석), v1/ 패키지는 API(간결). step 번호 참조/항목 참조/브로 서사 제거, 핵심 아키텍처 설명은 유지. 모르면 steps/에서 뒤지기.
- **★ 빈 템플릿 11개 삭제** — 기존 rezero/core.py 등 빈 템플릿이 헷갈림 유발. v1/이 진짜 패키지니까 과감히 삭제. 추후 vX 없이 export할 일 생기면 그때 더미 만들면 됨.
- **rezero 정체성 3종 패키지화에서도 유지** — fill_grad 전역 함수(항목 014), 매직메서드 클래스 안(항목 031), __array_priority__ 버림(항목 033). dezero와 다른 구조를 패키지 레벨에서도 관철.
- **★★ AGENTS.md 디렉터리 구조 섹션 전면 개서** — ★ 새 세션이 rezero 구조를 즉시 이해하도록: 버전 폴더 전략 설명 + dezero↔rezero 대응표 + rezero 정체성 5종 표. "왜 rezero/core.py가 없지?" 헤매는 것 방지. 브로 "추후 신규 세션에서 원본 소스가 어디와 대응되는지 알아야" 통찰 반영.

### 🔗 관련 링크

- [Issue #29](https://github.com/ghjang/deep-learning-from-scratch-3/issues/29) — step23 진행 추적
- `REZERO_CHANGES.md` 항목 #036 (버전 폴더 전략 + 순환 참조 해결 + 주석 정리 기준)

### 📝 코드 / 수식 메모

```python
# ★ 순환 참조 해결 — 지연 import
class Variable:
    def __add__(self, other):
        from rezero.v1.functions import add  # ★ 호출 시점에 로드
        return add(self, other)

# ★ 버전 폴더 구조
rezero/
├── v1/              ← 2고지 (step01~22) 패키지
│   ├── core.py      ← Variable, Function, Config, fill_grad
│   ├── functions.py ← Square/Add/Mul/Neg/Sub/Div/Pow + wrapper
│   └── __init__.py  ← re-export
├── v2/              ← (미래) 3고지
├── steps/           ← 학습 흔적 전부 (그대로)
└── tests/

# 사용
from rezero.v1 import Variable, fill_grad
y = (x + 3) ** 2
fill_grad(y)
```

**키워드**: `#2고지` `#패키지로정리` `#버전폴더전략` `#v1` `#순환참조` `#지연import` `#lazy_import` `#주석정리` `#API화` `#빈템플릿삭제` `#정체성유지` `#setup_variable_안씀` `#항목036`

---

## Step 24 — [2고지] 복잡한 함수의 미분

**Issue**: [#30](https://github.com/ghjang/deep-learning-from-scratch-3/issues/30)
**완료일**: 2026-08-10
**상태**: ✅

### 📖 요약 (한 줄)

v1 패키지를 사용해 3개 최적화 벤치마크 함수(Sphere/Matyas/Goldstein-Price) 구현 + 자동 미분. ★ step23 패키지화의 가치 증명 — 복잡한 수식도 연산자 오버로딩으로 자연스럽게 + fill_grad로 자동 미분. 2고지 마지막 step 완료 → 2고지 점령!

### 💡 통찰 / 배운 점

- **★★★ v1 패키지 사용 증명** — `from rezero.v1 import Variable, fill_grad`로 패키지를 사용자 코드로 활용. step23 패키지화가 "실제로 잘 작동한다"를 증명. Goldstein-Price 같은 복잡한 다항식도 `x ** 2 + ...` 식으로 자연스럽게 표현.
- **step 한정 함수** — sphere/matyas/goldstein은 v1 패키지 핵심이 아니므로 steps/에만 작성 (AGENTS.md "코드 위치 결정 가이드" 적용 첫 사례).
- **gradient check로 검증** — Goldstein-Price 역전파 오차 8.66e-05. 수치 미분과 해석 역전파 일치 확인.
- **최적화 벤치마크** — Sphere(볼록, 단순) vs Goldstein-Price(비볼록, 많은 지역 최솟값). step28+ 경사하강법 테스트용.

### 🔗 관련 링크

- [Issue #30](https://github.com/ghjang/deep-learning-from-scratch-3/issues/30) — step24 진행 추적

### 📝 코드 / 수식 메모

```python
from rezero.v1 import Variable, fill_grad

def sphere(x, y):
    return x ** 2 + y ** 2       # ★ 패키지 연산자 사용

x = Variable(np.array(1.0))
y = Variable(np.array(1.0))
z = sphere(x, y)
fill_grad(z)                     # x.grad=2.0, y.grad=2.0

# Goldstein(1,1): z=1876, x.grad=-5376, y.grad=8064 (정답지와 일치)
```

**키워드**: `#2고지` `#복잡한함수의미분` `#Sphere` `#Matyas` `#Goldstein` `#최적화벤치마크` `#v1패키지사용` `#2고지점령` `#MINOR_bump`

---

## Step 25 — [3고지] 계산 그래프 시각화(1)

**Issue**: [#31](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31)
**완료일**: 2026-08-11
**상태**: ✅

### 📖 요약 (한 줄)

v1 패키지에 Graphviz DOT 시각화 도구 4종 추가 (`_dot_var`, `_dot_func`, `fold_dot_graph`, `plot_dot_graph`). 정답지 대비 7가지 변형(fold 네이밍, weakref 단수, subprocess 안전, IPython 제거, f-string, ~/.rezero) + 브로 통찰로 `show_value` 옵션 추가. 3고지 첫 step.

### ❓ 질문 / 막힌 점

- ✅ **"()`가 뭐지?"** — 브로 질문. `v.shape`의 결과로, 스칼라(0차원 ndarray)의 shape이 빈 튜플 `()`라서. v1에선 모든 Variable이 스칼라라 전부 `()`. → verbose 옵션이 v1에선 노이즈, v2 텐서에서 빛을 발. 이 통찰로 show_value와 verbose 분리 결정.
- ✅ **"값만 출력하기로 한 거 아니었어?"** — 브로 데모 버그 지적. show_value=True인데 verbose도 True여서 shape/dtype이 섞여 나옴. verbose=False 명시로 깔끔하게 수정.

### 💡 통찰 / 배운 점

- **★★★ `fold_dot_graph` 네이밍** — 정답지 `get_dot_graph`가 사실 fold(역방향 순회하며 DOT 텍스트 누적 합성). rezero fold 계보(step06/07/08)에 이어 일관성. 헬퍼도 `add_func` → `fold_func` (메인이 fold니까).
- **★★★ 순회 공통화 발견** — `fold_dot_graph`의 worklist + visited 패턴이 `fill_grad`와 거의 동일. 탐구 노트 20번 섹션 6이 예측한 "step25 = 순회 일반화 계기" 회수 시그널 도달. 리팩터는 이슈 32번으로 연기 (step25는 독립 구현, 별도 세션에서 리팩터).
- **★★★ `show_value` 아이디어 (브로)** — Variable은 "상자"인데 정작 시각화에선 값이 안 보임. verbose(shape/dtype, 정적)와 show_value(값, 동적)를 관심사 분리. 디버깅 가치: NaN 추적, gradient check 실패 원인 파악.
- **변수명 볼드 강조 (브로)** — DOT HTML-like label로 `<B>x</B> = 1` 형태. 변수명이 시각적 앵커 → 그래프에서 변수 위치 한눈에. 값은 보통 텍스트.
- **포맷 화이트리스트** — png/svg/pdf만 허용, 그 외는 ValueError. SVG(벡터)는 VSCode에서 텍스트로도 까볼 수 있어 학습에 좋음.
- **★ step25/26 코드 배분 착각 (교훈)** — 정답지 `steps/step25.py`는 `# No code`, `steps/step26.py`가 goldstein+plot_dot_graph 코드. 우리는 step25에서 시각화 도구 구축 + Goldstein 그래프 출력(step26 영역)까지 한 번에 커버함. 원인: 정답지 두 파일을 나란히 비교 안 하고 희미한 책 기억에 의존 (브로+AI 둘 다 같은 착각). **다음부론 정답지 stepN-1/N/N+1 세 파일 나란히 비교로 방지**. 실익상 손해는 없음 (코드는 다 작동) — 다만 step26 진행 시 "이미 했음" 처리.
- **변형 7종** (정답지 대비): fold 네이밍 / weakref 단수 / subprocess `check=True` + 리스트 / 파일 경로 반환 (IPython 제거) / f-string / `output/` 폴더 / `show_value` 추가.
- **"결정 요청은 1개씩" 원칙 신설** — 8개 결정 폭풍 출력에 브로가 "빠뜨릴 수 있다, 1개씩 물어달라". 전체 목록 예고(OK) → 실제 결정은 1개씩. AGENTS.md 학습 스타일 + 메타 원칙에 추가.

### 🔗 관련 링크

- [Issue 31번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31) — step25 진행 추적
- [Issue 32번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/32) — 순회 제너레이터 추출 리팩터 (step25 이후)
- [Issue 33번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/33) — fold 과정 단계별 스냅샷 (브로 아이디어, 32번 완료 후)
- [Issue 21번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/21) — Node + manim (순회 공통화 부분 32번으로 이관)

### 📝 코드 / 수식 메모

```python
from rezero.v1 import Variable, fill_grad, plot_dot_graph, fold_dot_graph

x = Variable(np.array(1.0), name='x')
y = Variable(np.array(1.0), name='y')
z = goldstein(x, y)   # name='z'
fill_grad(z)

# 구조만
fold_dot_graph(z, verbose=False)
# → 'digraph g { ... x [label="x", color=orange, ...] ... }'

# 값까지 (브로 통찰 — 상자 안의 실제 값 표시)
fold_dot_graph(z, verbose=False, show_value=True)
# → 'x = 1', 'z = 1876' 식으로 라벨에 값 추가

# PNG 렌더링 (graphviz dot 바이너리 필요)
plot_dot_graph(z, verbose=False, show_value=True, to_file='output/goldstein_value.png')
# 변수명 볼드 + 값 표시 → 그래프에서 변수 위치와 값 동시 파악

# SVG (벡터, VSCode에서 까보기 좋음)
plot_dot_graph(z, verbose=False, show_value=True, to_file='output/goldstein.svg')

# 미지원 포맷은 ValueError (지원: png/svg/pdf)
# plot_dot_graph(z, to_file='output/bad.jpg')  → ValueError
```

**키워드**: `#3고지` `#계산그래프시각화` `#Graphviz` `#DOT언어` `#fold_dot_graph` `#show_value` `#변수명볼드` `#HTML-likelabel` `#포맷화이트리스트` `#SVG` `#순회공통화후보` `#subprocess_check=True` `#결정요청은1개씩` `#output폴더`

---

## Step 26 — [3고지] 계산 그래프 시각화(2)

**Issue**: [#31](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31) (step25가 커버 — 별도 이슈 없음)
**완료일**: 2026-08-19
**상태**: ✅

### 📖 요약 (한 줄)

★ step25에서 선행 커버 완료. 정답지 step26 코드(goldstein + plot_dot_graph 출력)를 step25 작업 시 전부 구현했고, 브로 책 재확인으로 본문에 코드 외 새 개념 없음 확인 → 별도 구현 없이 공식 ✅ 처리.

### 💡 통찰 / 배운 점

- **선행 커버 경위** — step25/26 코드 배분 착각(정답지 steps/step25.py가 `# No code`, steps/step26.py가 실제 코드)으로 step25가 step26 영역까지 커버. 코드는 전부 정상 동작(테스트 99개 통과)이라 그대로 승격.
- **정답지보다 풍성해진 결과** — show_value 옵션, 변수명 볼드(HTML-like label), 포맷 화이트리스트(png/svg/pdf), DOT 소스 보존, SVG 출력까지 step25에서 구현됨.
- **교훈의 제도화** — 이 사태로 AGENTS.md "정답지 인접 step 비교" 원칙(stepN-1/N/N+1 세 파일 나란히) 신설. 미래 세션 재발 방지.
- **"이미 했음" 처리 패턴** — rezero/steps/step26.py는 리다이렉트 docstring만 (경위 + 실행 안내). 별도 이슈 생성 대신 step25 이슈 #31 참조로 관리 최소화.

### 🔗 관련 링크

- [Issue 31번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31) — step25 진행 (step26 커버 경위 코멘트 포함)
- LEARNING_NOTES step25 섹션 — 시각화 도구 상세
- `rezero/steps/step26.py` — 리다이렉트 docstring

### 📝 코드 / 수식 메모

```python
# 정답지 steps/step26.py의 전부 — step25 데모에서 이미 실행:
x = Variable(np.array(1.0), name='x')
y = Variable(np.array(1.0), name='y')
z = goldstein(x, y); z.name = 'z'
fill_grad(z)
plot_dot_graph(z, verbose=False, to_file='output/goldstein.png')
# → uv run python rezero/steps/step25.py
```

**키워드**: `#3고지` `#계산그래프시각화` `#선행커버` `#리다이렉트docstring` `#시각화2부작종결`

---

## Step 27 — [3고지] 테일러 급수 미분

**Issue**: [#34](https://github.com/ghjang/deep-learning-from-scratch-3/issues/34)
**완료일**: 2026-08-19
**상태**: ✅

★ 제목 정정 (2026-08-19): 기존 "지수/로그 함수 (Exp, Log)"는 오등록 — 브로가 교재 실제 제목 "테일러 급수 미분" 확인 전달.

### 💡 통찰 / 배운 점 (★ 학습 시작 전 브로-AI 대화로 도출 — 이 step의 심장)

- **★★★ 두 층위 구조 — 이 step의 감동 포인트 (브로 자각)**:
  - **층위 1 (당연함)**: `Sin` 클래스 — `derivative`에 cos를 **직접 가르쳐 줌**. 도함수를 아는 함수의 미분. "시험 문제에 답 적어놓고 시험 본 격".
  - **층위 2 (대서사)**: `my_sin` — **cos라는 단어를 코드 어디에도 모르는** +, **, * 만의 다항식 합성. 그런데 계산 그래프를 역전파하면 **cos 값이 나온다**.
- **★ 수학적 정체 — 테일러 항별 미분 = cos의 테일러 전개**:
  $$\frac{d}{dx}\Big[x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots\Big] = 1 - \frac{3x^2}{3!} + \frac{5x^4}{5!} - \cdots = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots$$
  (3/3! = 1/2!, 5/5! = 1/4!) — sin↔cos의 미분 관계가 chain rule fold로 **저절로 재현**됨.
- **★ 핵심 문장**: "무엇의 도함수인지 가르쳐 준 함수만 미분할 수 있는 게 아니라, **그래프를 만들 수만 있다면 그 그래프의 도함수가 저절로 나온다**." — Define-by-Run의 본질. Sin 클래스(층위 1)는 이 문장의 대조군.
- **v1 연산자 3부작 총동원**: `y = 0; y = y + t` → `__radd__` (step21). `c * x ** n` → `__rmul__` (step21) + `Pow` (step22). step20~22 구축물의 첫 실전 합성.
- **rezero 관점 — derivative hook의 간결함**: 책은 `backward` 직접 오버라이드 (`gy * np.cos(x)`), rezero는 `derivative` 한 줄 (`lambda x: np.cos(x)`) — chain rule 곱셈은 부모 `Function.backward`가 담당하므로.

### 📖 요약 (한 줄)

Sin 승격 (v1 첫 수학 함수, derivative hook 한 줄) + my_sin 테일러 근사 데모. ★ 근사 다항식의 역전파 = cos — "그래프를 만들면 도함수가 저절로"라는 Define-by-Run 본질 실증. 시각화 도구 2건 개선 (value_format, Pow dot_label) + 책 마지막 예제(1e-150, 노드 377개) 재현.

### ❓ 질문 / 막힌 점

- ✅ **"Sin은 그냥 추가하는 건데, 테일러 다항식 전체의 미분이 cos가 된다는 게 대서사?"** — 브로 자각. 맞음. 두 층위 구조 (위 통찰).
- ✅ **"풀버전(1e-150) PNG에서 값 라벨은 의미없지 않나?"** — 브로 지적. 노드 377개에선 숫자가 안 읽힘 → 구조 감상용으로 show_value=False 적용.

### 💡 통찰 / 배운 점 (진행 중 도출 — 구현/리뷰 과정)

- **value_format (적응형)** — 값 라벨 제각각 문제(브로 지적) → `1e-4 ≤ |v| < 1e5`는 고정 소수점 4자리 + trailing 0 제거, 밖은 지수. NaN/inf 명시 표기 (디버깅 추적 단서). 커스텀 스펙(`.2f` 등)도 `value_format` 파라미터로 지원.
- **Pow.dot_label 훈** — Pow 박스들이 전부 "Pow"라서 어떤 항인지 구분 안 됨(브로 지적) → `dot_label(show_param)` 훅 (derivative hook과 같은 패턴). 표시 조건 `verbose or show_value` — 값 추적 시 c는 해석 맥락이므로. 기본(구조만)은 책 방식 유지.
- **threshold=1e-150 그래프** — 노드 377개. ★ 렌더링이 "뒤집힌 직각 삼각형" — 삼각함수 근사 그래프가 삼각형 (브로 관찰, 책 마지막 웃픈 포인트). 항마다 Pow→Mul→Add 체인이 y 재사용하며 계단으로 쌓이는 구조.
- **pyright와 협력 2건** — `y: Variable | int = 0` + 루프 후 assert (my_sin의 `y = 0` 시작, `__radd__` 학습 포인트 유지). 테스트의 Optional 가드 (`assert x.grad is not None`).

### 🔗 관련 링크

- [Issue 34번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/34) — step27 진행 추적
- `output/my_sin.png` (기본 threshold) / `output/my_sin_full.png` (1e-150, 삼각형)

### 📝 코드 / 수식 메모

```python
from rezero.v1 import Variable, fill_grad, sin

# 층위 1: 도함수를 가르쳐 준 함수
x = Variable(np.array(np.pi / 4)); y = sin(x); fill_grad(y)
# y = 0.70711, x.grad = 0.70711 (cos)

# 층위 2: cos를 모르는 테일러 다항식 — 같은 결과!
def my_sin(x, threshold=0.0001):
    y: Variable | int = 0
    for i in range(100000):
        c = (-1) ** i / math.factorial(2 * i + 1)
        t = c * x ** (2 * i + 1)     # __rmul__ + Pow
        y = y + t                    # int 0 + Variable → __radd__
        if abs(t.data) < threshold: break
    assert isinstance(y, Variable)
    return y
# y = 0.70711 (5자리 일치), x.grad = 0.70710 ★ 저절로 cos
```

**키워드**: `#3고지` `#테일러급수미분` `#Sin` `#my_sin` `#두층위구조` `#근사함수도미분된다` `#Define-by-Run본질` `#__radd__총동원` `#value_format` `#dot_label훅` `#Pow(c=N)` `#1e-150삼각형` `#제목정정`


---

## Step 28 — [3고지] 함수 최적화

**Issue**: [#35](https://github.com/ghjang/deep-learning-from-scratch-3/issues/35)
**완료일**: 2026-08-19
**상태**: ✅

### 💡 통찰 / 배운 점 (★ 학습 시작 전 브로-AI 대화로 도출)

- **★ "v1 반영 없음"이 성격을 말한다** — step24(벤치마크)처럼 응용 step. step23 패키지화의 가치 재증명: "인프라 완료 → 응용은 import만".
- **★★★ "미분 기계가 처음으로 '일'을 한다"** — step01~27은 미분 인프라 구축, step28에서 그 인프라로 실제 문제(함수 최소화)를 푼다. 27 step의 목적이 처음 실현되는 순간.
- **★ "학습"의 정체 폭로** — 딥러닝의 학습 = loss 함수에 대한 경사하강법. 4단계 루프(순전파 → clear_grad → 역전파 → 갱신)가 신경망 학습의 원형. PyTorch `zero_grad()`/`backward()`/`step()` 삼단 콤보의 조상.
- **경사하강법 은유** — 안개 낀 산에서 눈앞 경사만 보고 내려가기. gradient = 가장 가파른 오르막 → `-lr * grad` = 내리막 발걸이. lr 트레이드오프 (크면 발산, 작으면 느림).
- **Define-by-Run의 반복 학습** — 매 iteration 그래프 새로 생성/폐기. "그래프는 영구 저장물이 아니라 계산의 부산물".
- **★ 적합성 메모 (경사하강법)** — 빛나는 경우: 볼록 + 조건수 양호 + gradient 저렴 (딥러닝 loss처럼). 최악인 경우: Rosenbrock식 ill-conditioned 골짜기 (바닥에 붙어 기어감), 평탄부 (saddle point 근처 정체), lr 하나로 방향별 스케일 못 맞춤. → step29 뉴턴 방법의 등장 동기. 상세: 탐구 노트 27.

### 📖 요약 (한 줄)

경사하강법 4단계 갱신 루프로 Rosenbrock 최소화 — v1 반영 없는 응용 step으로 "미분 기계가 처음으로 일을 하는" 순간. 데모 4케이스(수렴/lr 발산/clear_grad 누락/sphere 대비) + 골짜기 바닥 편차 추적으로 "낙하→크롤링" 실증. 탐구 노트 2종(Rosenbrock+NFL 선택지도 / 방향미분+갱신식 해부) 파생.

### ❓ 질문 / 막힌 점

- ✅ **"gradient가 왜 가장 가파른 방향?"** — 방향미분 → 내적 → 코사인 3단 유도로 회수 (탐구 노트 28).
- ✅ **"1변수 미분도 방향미분?"** — 맞음. 선택지 2개(+x/-x)짜리 특수 사례. f'의 부호가 상승 방향.
- ✅ **"경사하강법 코드에 내적이 안 보이는 이유?"** — 증명(why)과 실행(how)의 분리. 코드는 증명된 결론(-∇f)만 사용.
- ✅ **"스칼라장/벡터장? gradient 어원?"** — 장 = 공간 각 점마다 값 배정. gradient = 스칼라장→벡터장 연산. 어원 라틴어 gradiens(기울다), 색 그라데이션과 동족어.
- ✅ **"상위호환은 없나?"** — NFL 정리: 만능 알고리즘 불가능. 질문은 "누가 낫냐"가 아니라 "우리 문제 구조에서 누가 빛나냐" (탐구 노트 27).

### 💡 통찰 / 배운 점 (진행 중 도출 — 구현/리뷰/탐구 과정)

- **복붙 버그와 gd_step 헬퍼** — [4]에서 `x1.data -= lr * x0.grad` 복붙 버그를 재실행 검증으로 포착 → 갱신 공식을 헬퍼로 집중 (재발 방지 + Optional 가드). "코드 수정 후 재실행" 원칙이 이번에도 버그를 잡음.
- **골짜기 바닥의 정체** — A항 `100(x1-x0²)²`가 바닥을 포물선 x1=x0²로 형성. 데모 편차(x1-x0²)가 +1.6 → -0.003으로 수렴 후 유지 = "낙하→크롤링" 2단계 실증.
- **갱신 식의 설계** (탐구 노트 28 8절) — 국소 정보만 쓰는 greedy + 크기 기반 자동 보폭 + 1차 테일러 감소 담보(lr|∇f|² ≥ 0) + 최소점 자동 감속. 관성 없음 → 모멘텀 예고.
- **시험 함수 디자인 = 역설계** — 알고리즘의 실패 모드를 지형으로 번역. "이 방법이 실패하는 지형"을 먼저 정하고 조립 (탐구 노트 27).
- **pdoc API 문서 파이프라인** — docstring → HTML. `PYTHONPATH=. uv run pdoc rezero.v1 -o output/api_doc`. 아스키 테이블은 블록화(들여쓰기)로 Markdown 대응.

### 🔗 관련 링크

- [Issue 35번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/35) — step28 진행 추적
- [탐구 노트 27 — Rosenbrock 해부와 최적화 알고리즘 선택의 지도](./notes/exploration_27_rosenbrock.md)
- [탐구 노트 28 — 방향 미분: 왜 gradient가 가장 가파른 방향인가](./notes/exploration_28_directional_derivative.md)
- AGENTS.md "개발 환경" — pdoc API 문서 생성 메모

### 📝 코드 / 수식 메모

```python
from rezero.v1 import Variable, fill_grad

# 4단계 갱신 루프 — 신경망 학습의 원형
for _ in range(1000):
    y = rosenbrock(x0, x1)   # ① 순전파 (그래프 새로 구축)
    x0.clear_grad()           # ② grad 초기화 (PyTorch zero_grad의 원형)
    x1.clear_grad()
    fill_grad(y)              # ③ 역전파
    gd_step(x0, lr)           # ④ 갱신 — x.data -= lr * x.grad
    gd_step(x1, lr)

# 결과: (0, 2) → (0.6837, 0.4660) — 바나나 골짜기를 따라 천천히
# lr=0.01부터 발산 / clear_grad 누락 시 grad 누적 폭증 → nan
```

**키워드**: `#3고지` `#함수최적화` `#경사하강법` `#Rosenbrock` `#바나나골짜기` `#4단계루프` `#학습의원형` `#zero_grad원형` `#gd_step` `#낙하와크롤링` `#골짜기바닥편차` `#복붙버그교훈` `#탐구노트27` `#탐구노트28` `#NFL정리` `#선택지도` `#방향미분` `#pdoc` `#제목정정`


### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 29 — [3고지] 뉴턴 방법으로 푸는 최적화(수동 계산)

**Issue**: [#36](https://github.com/ghjang/deep-learning-from-scratch-3/issues/36)
**완료일**: 2026-08-19
**상태**: ✅

### 💡 통찰 / 배운 점 (★ 학습 시작 전 브로-AI 대화로 도출)

- **★★★ 브로 사전 통찰 — "경사하강법 = 테일러 1차 항만 사용?"** → 정확!
  - 경사하강: f를 **직선(1차 근사)** → 직선엔 최소점이 없어 **방향**만 알 수 있음 → 보폭(lr)은 임의
  - 뉴턴: f를 **포물선(2차 근사)** → 포물선엔 최소점이 있음 → **그 바닥으로 바로 점프**
  - 탐구 노트 28의 lr|∇f|² 감소 담보 증명이 정확히 "1차 테일러 근사"였음과 연결.
- **★ "수동 계산"의 정체** — f''(x)를 사람이 손으로 유도 (gx2 함수). 현재 프레임워크는 1차 미분까지만 자동. 이 한계가 **step30(최적화 자동화) → 고차 미분(3고지의 진짜 주제)으로 이어지는 복선**.
- **뉴턴 방법의 원래 정체** — 방정식 근 찾기(f(x)=0) 기법. 최적화 = "f'(x)=0 찾기"이므로 f'에 적용 → x ← x - f'/f''.
- **★ 적합성 메모 (뉴턴 방법)** — 빛나는 경우: 매끄러운 함수 + 좋은 초기치 + 1차원/저차원 (2차 수렴으로 몇 스텝에 기계 정밀도). 최악인 경우: f'' ≤ 0 지점(최대점으로 점프), 나쁜 초기치(발산/진동), 고차원(Hessian 역행렬 O(n³) — 딥러닝 불가의 이유, 탐구 노트 27 선택 지도 연결).

### 📖 요약 (한 줄)

뉴턴 방법 `x ← x - f'/f''` — f를 접하는 포물선(2차 테일러)의 바닥으로 점프. 7 iters에 기계 정밀도(2차 수렴). "수동 계산" = f''를 손으로 유도 (step30 고차 미분 자동화의 복선). 탐구 노트 29 파생 (접촉 3조건 → 곡률의 정체 → 물리와의 평행 "원동력은 2차에 있다"까지).

### ❓ 질문 / 막힌 점

- ✅ **"경사하강 = 테일러 1차 항?"** — 맞음. 직선엔 최소점 없어 방향만 → 뉴턴은 2차 포물선 바닥으로 점프.
- ✅ **"접한다는 게 정확히?"** — 접촉 3조건: 접점에서 f, f', f'' 동시 일치.
- ✅ **"왜 f''가 곡률?"** — f'' = 기울기의 변화율 = 휨. 엄밀한 κ = f''/(1+f'²)^{3/2}, 완만하면 κ ≈ |f''|.
- ✅ **"물리 가속도와 기하 곡률은 관계가?"** — 수학 대상은 하나, 독립변수(시간/공간)가 해석 결정. ★ "무엇이 움직이는가(1차)가 아니라 무엇이 움직임을 바꾸는가(2차)" — 원동력은 2차에 있다. 모멘텀 옵티마이저가 이 직관의 구현체.
- ✅ **[그림 피드백 3연타]** — 텍스트 겹침 → 위치 → 우측 미세조정 (브로 QA의 밤 ㅋㅋ).

### 💡 통찰 / 배운 점 (진행 중 도출)

- **2차 수렴 실증** — 오차 1.0 → 0.45 → 0.15 → 0.025 → 9e-4 → 1.2e-6 → 2.3e-12 → 0 (7 iters). 유효숫자 매번 배가.
- **오버슈트 오판 사건** — `|x-1|` 측정이 "실패"로 오판 → 실제론 f의 ±1 두 최소점 중 반대편 안착. 측정식도 문제 정의의 일부.
- **국소 최대 함정** — x=0.3(f''<0 지역) 시작 → 최대점 0에 갇힘. f'(x)=0이면 멈추지만 최소 보장 없음.
- **그림 2장** — `newton_quadratic.png`(전체 연쇄) + `newton_dramatic.png`(한 스텝 클로즈업: 어길난 포물선 바닥 + 실제 우물 회색 별). 접촉 3조건 주석 포함.

### 🔗 관련 링크

- [Issue 36번](https://github.com/ghjang/deep-learning-from-scratch-3/issues/36) — step29 진행 추적
- [탐구 노트 29 — 뉴턴 방법: 곡률을 알면 점프할 수 있다](./notes/exploration_29_newton_method.md)
- `output/newton_quadratic.png` / `output/newton_dramatic.png`

### 📝 코드 / 수식 메모

```python
def f(x):  return x ** 4 - 2 * x ** 2
def gx2(x): return 12 * x ** 2 - 4   # f'' 손유도 — "수동 계산"

# 뉴턴: 2.0 → 1.0까지 7 iters (기계 정밀도), lr 없음
x.data -= x.grad / gx2(x.data)   # 크기까지 f''가 결정

# 경사하강 대비: 13 iters (-1 안착, 오버슈트 서사)
# 나쁜 초기치 0.3: 국소 최대 0에 갇힘 (f''<0 함정)
```

**키워드**: `#3고지` `#뉴턴방법` `#수동계산` `#2차테일러` `#접하는포물선` `#접촉3조건` `#곡률` `#2차수렴` `#7iters기계정밀도` `#국소최대함정` `#원동력은2차에` `#물리와의평행` `#탐구노트29` `#step30복선` `#제목정정`


### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 30 — [3고지] 고차 미분(준비 편)

**Issue**: 없음 — 복습 장이라 별도 이슈 없이 브로 책 재독 + AI 대화 세션으로 커버
**완료일**: 2026-08-20
**상태**: ✅

### 📖 요약 (한 줄)

코드 없음 (정답지 `# No code`). DeZero의 Variable/Function/역전파 구조를 그림·다이어그램으로 되짚는 복습 장 — 고차 미분 3부작(30 준비 / 31 이론 / 32 구현)을 앞두고 개념 캐시를 정리하는 호흡 조절 단계.

### ❓ 질문 / 막힌 점

- (없음 — 브로 재독 판단: "딱히 하는 게 없다, 한번 호흡을 가다듬는 장")

### 💡 통찰 / 배운 점

- **step30의 성격 재확인** — 브로 책 재독 결론: 새 코드 0건. 이전 스텝 내용을 "다시 한번" 차분히 설명. 다만 **그림/다이어그램을 다수 첨부**해 이해를 보조하는 것이 특징 (코드 없이 시각 자료로 개념 재정리).
- **왜 여기서 복습인가** — 고차 미분(31 이론 / 32 구현)은 지금까지 만든 역전파 메커니즘(`set_creator` 연결 → worklist 역전파 → `x.grad`에 accumulate) 위에 세우는 2층 구조. 기초가 흔들리면 3부작에서 반드시 막힘 → 책이 의도적으로 넣은 워밍업.
- **step29와의 연결** — step29 뉴턴 방법에서 f''(2차 미분)을 손으로 유도했던 한계(gx2 함수)가 바로 이 3부작에서 자동화됨. step30은 그 전의 "현재 우리가 뭘 갖고 있는지" 점검.
- **3고지 코드 배분 확인 (step25/26 착각 방지 체크리스트 적용)** — 정답지 step30/31/32 전부 `# No code`: 3고지부터는 개별 step 파일이 아니라 `dezero/core_simple.py`(패키지)가 진화함. step32 "구현 편"의 대개편(backward의 Variable화, `create_graph`)이 실체.

### 🔗 관련 링크

- 정답지: `steps/step30.py` (`# No code`), `dezero/core_simple.py` (현재 시점 전체 구조)
- step29 복선: LEARNING_NOTES step29 — "수동 계산"의 정체 (gx2 손유도 한계)
- [탐구 노트 29](./notes/exploration_29_newton_method.md) — 뉴턴 방법 (곡률 = 2차 정보)

### 📝 코드 / 수식 메모

- (코드 없음 — `rezero/steps/step30.py`는 기록용 리다이렉트 docstring만)


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

