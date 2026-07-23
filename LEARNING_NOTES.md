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

### 🎨 디자인 패턴 (횡단 관심사, 누적형)

> exploration_XX와 다른 카테고리. 패턴은 여러 step에 걸쳐 재등장하는 횡단 관심사라 단일 파일에 누적 관리.

| 파일 | 시점 | 주제 |
|---|---|---|
| 🎨 | step01~ 누적 | DeZero에 등장하는 디자인 패턴 (래퍼, 템플릿 메서드 등) | [notes/design_patterns.md](./notes/design_patterns.md) |

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
- 책의 "테니스 공 상자" 비유 = 이 래핑 구조를 직관적으로 설명

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

## Step 04 — [1고지] 수치 미분 (수치 미분 구현)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 05 — [1고지] 수치 미분 이론 [No code]

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 06 — [1고지] 역전파 이론 (계산 그래프, 국소적 미분)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 07 — [1고지] 역전파 구현 - Variable.backward()

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 08 — [1고지] Function.backward() 구현

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 09 — [1고지] 함수를 더 편하게 (Function 기반 클래스화)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


---

## Step 10 — [1고지] 테스트 (unittest로 동작 검증)

**Issue**: (링크)
**완료일**: -
**상태**: ⏳

### 📖 요약 (한 줄)


### ❓ 질문 / 막힌 점


### 💡 통찰 / 배운 점


### 🔗 관련 링크


### 📝 코드 / 수식 메모


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

