# 🧪 보충 탐구 #3 — Symbolic vs Numeric: sympy, PyTorch, 그리고 DeZero의 그래프

> **step01 직후 보충 학습 #3** (2026-07-21)
> 브로가 2권 학습 중 sympy + manim으로 수식/애니메이션을 만들어본 경험에서 출발.
> "MLX에서 sympy처럼 심볼릭 조작, LaTeX, eval 호출이 가능할까?"라는 오바망상(?)을 검증.
> → 결론: **오바망상 아님!** 핵심 질문이며, sympy vs PyTorch는 근본적으로 다른 패러다임.

---

## 목차

- [A. 브로의 질문 검증 — 3가지 레벨](#a-브로의-질문-검증--3가지-레벨)
- [B. sympy vs PyTorch/MLX/DeZero — 패러다임 비교](#b-sympy-vs-pytorchmlxdezero--패러다임-비교)
- [C. DeZero의 그래프 시각화 (Graphviz)](#c-dezero의-그래프-시각화-graphviz)
- [D. sympy ↔ MLX 연결하기 (가능하다!)](#d-sympy--mlx-연결하기-가능하다)
- [E. manim과 DeZero 시각화의 관계](#e-manim과-dezero-시각화의-관계)
- [F. 요약 — 왜 이 질문이 중요한가](#f-요약--왜-이-질문이-중요한가)

---

## A. 브로의 질문 검증 — 3가지 레벨

브로가 던진 질문들을 3가지 레벨로 정리:

| 레벨 | 질문 | 정답 |
|---|---|---|
| **1** | MLX/PyTorch가 계산 그래프 시각화? | ✅ 가능. DeZero도 지원 (step09+) |
| **2** | LaTeX로 수식 출력? | ⚠️ 기본 지원 X, 우회 가능 |
| **3** | sympy처럼 심볼릭 조작/eval? | ❌ **완전 다른 패러다임** |

→ 브로의 직관이 핵심을 찌름. 3번이 제일 깊은 질문이야.

---

## B. sympy vs PyTorch/MLX/DeZero — 패러다임 비교

### B.1 sympy: **심볼릭 계산** (Symbolic Computation)

```python
import sympy as sp

x = sp.Symbol('x')                # ← 숫자 아님, "기호"!
expr = x ** 2 + 3 * x + 1         # ← 표현식 자체를 다룸
print(expr)                        # x**2 + 3*x + 1

# 심볼릭 조작
print(sp.diff(expr, x))           # 2*x + 3  ← 수학적으로 미분
print(sp.integrate(expr, x))      # x**3/3 + 3*x**2/2 + x
print(sp.latex(expr))             # x^{2} + 3 x + 1  ← LaTeX!

# x에 숫자 대입 (eval)
print(expr.subs(x, 2))            # 11  ← 그제서야 숫자 계산
```

→ sympy는 **"수학식 자체를 다룸"**. 미분/적분/인수분해/LaTeX 전부 **수학적으로 정확**.

### B.2 PyTorch/MLX: **수치 계산 + autograd** (Numeric + AutoDiff)

```python
import mlx.core as mx

x = mx.array(2.0)                 # ← 실제 숫자!
y = x ** 2 + 3 * x + 1            # ← 바로 11.0 계산됨
print(y)                           # array(11, dtype=float32)

y.backward()                      # ← autograd로 미분
print(x.grad)                     # array(7, ...)  ← dy/dx = 2x+3 = 7 (x=2일 때)

# 근데 "수식"을 모름
# print(sp.latex(y))              # ❌ 안 됨 — y는 이미 숫자 11
# print(y.factor())               # ❌ 안 됨 — 수학 조작 불가
```

→ PyTorch/MLX는 **"숫자를 직접 계산하면서 미분 규칙만 기록"**. 수식 자체를 다루지 않음.

### B.3 비교표

| | sympy | PyTorch/MLX/DeZero |
|---|---|---|
| **x는?** | 기호 (Symbol) | 실제 숫자 (number) |
| **연산 결과** | 수식 (expr) | 계산된 값 (number) |
| **미분** | 수학적 분석 미분 | 수치적 autograd |
| **LaTeX** | ✅ 지원 | ❌ 불가 |
| **인수분해/적분** | ✅ 가능 | ❌ 불가 |
| **속도** | 느림 (수학적 조작) | 빠름 (그냥 계산) |
| **용도** | 수학 연구, 교육 | 머신러닝, 대규모 수치 |

### B.4 핵심 차이: **"언제 숫자가 되느냐"**

```
sympy:      x (기호) → x**2 (기호) → x**2+3*x+1 (기호) → subs(x,2) → 11 (그제야 숫자)
                                                        ↑
                                                     사용자가 원할 때

PyTorch:    x=2 (숫자) → x**2=4 (숫자) → x**2+3*x+1=11 (숫자)
            ↑
         처음부터 다 숫자, 수식은 기록만 됨
```

### B.5 왜 딥러닝은 수치(numeric) 방식을 쓸까?

1. **속도**: 수백만 개 파라미터를 수학식으로 다루면 느려. 숫자로 계산하는 게 빠름
2. **유연성**: 수식으로 표현 못 하는 연산(조건문, 룩업테이블 등)도 autograd는 처리 가능
3. **GPU 최적화**: GPU는 숫자 계산에 특화. 수학 기호 조작엔 부적합

**키워드**: `#심볼릭` `#수치계산` `#sympy` `#autograd` `#패러다임` `#NumericVsSymbolic`

---

## C. DeZero의 그래프 시각화 (Graphviz)

> 브로가 원했던 "그래프 시각화"는 DeZero가 이미 지원! step09부터 등장.

### C.1 DeZero의 시각화 함수

`dezero/utils.py`에 Graphviz DOT 언어로 그래프 생성하는 함수들이 있음:

```python
def _dot_var(v, verbose=False):
    """Variable 노드를 DOT 언어로 표현."""
    # 예: '1234 [label="x", color=orange, style=filled]'

def _dot_func(f):
    """Function 노드와 엣지를 DOT 언어로 표현."""
    # 예: '5678 [label="Square", color=lightblue, style=filled, shape=box]'

def get_dot_graph(output, verbose=True):
    """output Variable에서 거슬러 올라가며 전체 계산 그래프를 DOT 텍스트로 생성."""
    # walks the graph via creator pointers

def plot_dot_graph(output, verbose=True, to_file="graph.png"):
    """계산 그래프를 이미지 파일로 저장."""
    # 1. DOT 텍스트 생성
    # 2. graphviz dot 명령어로 렌더링
    # 3. PNG/PDF 저장
```

### C.2 사용 예시 (step09 이후로 계속 등장)

```python
from dezero import Variable
from dezero.utils import plot_dot_graph

def f(x):
    y = x ** 4 - 2 * x ** 2
    return y

x = Variable(np.array(2.0))
y = f(x)
y.backward()

# 계산 그래프를 이미지로 저장
plot_dot_graph(y, verbose=False, to_file="graph.png")
```

→ 출력은 Graphviz가 렌더링한 PNG 이미지. Variable은 주황색 노드, Function은 파란색 박스.

### C.3 시각화 결과 (개념적)

```
   ┌───┐         ┌──────┐         ┌───┐
   │ x │ ──┬───→ │ **4  │ ──┐    │   │
   └───┘   │    └──────┘   │    │ + │ ──→ y
           │              ├───→│   │
           │    ┌──────┐   │    └───┘
           ├───→ │ **2  │ ──┤
                └──────┘   │
                          │
                     ┌──────┐
                ┌───→│ *(-2)│───┘
                │    └──────┘
           (역전파 추적용 그래프)
```

### C.4 DeZero 시각화의 특징

- ✅ **연산 흐름** 시각화 (어떤 함수가 어떤 변수를 만들었나)
- ✅ **Graphviz** 기반 (DOT 언어 → 이미지)
- ❌ **LaTeX 수식** 아님 (숫자 흐름이지 수식이 아님)
- ❌ **인수분해/적분** 불가

→ 브로가 manim으로 만든 "수식 애니메이션"과는 다른 영역. DeZero는 "연산 흐름 시각화", manim/sympy는 "수식 시각화".

**키워드**: `#Graphviz` `#DOT언어` `#plot_dot_graph` `#계산그래프` `#시각화`

---

## D. sympy ↔ MLX 연결하기 (가능하다!)

> 브로가 상상한 "표현 변환"은 실제로 가능한 워크플로!

### D.1 핵심 도구: `sympy.lambdify`

sympy 수식을 파이썬 함수로 "컴파일"하는 도구:

```python
import sympy as sp

x = sp.Symbol('x')
expr = x ** 2 + 3 * x + 1

# 수식 → 파이썬 함수
f = sp.lambdify(x, expr, 'numpy')    # 'numpy' 백엔드 사용

import numpy as np
print(f(2))                          # 11  ← 이제 숫자 계산
print(f(np.array([1, 2, 3])))        # [5 11 19]
```

### D.2 sympy → MLX 워크플로

```python
import sympy as sp
import mlx.core as mx

# 1. sympy로 수식 정의 + 분석
x_sym = sp.Symbol('x')
expr = x_sym ** 2 + 3 * x_sym + 1

# LaTeX 얻기 (브로가 manim에서 쓰던 방식)
print("LaTeX:", sp.latex(expr))    # x^{2} + 3 x + 1

# 수학적 미분 (autograd와 다름!)
print("수식 미분:", sp.diff(expr, x_sym))   # 2*x + 3

# 2. 수식을 numpy 함수로 컴파일
f_np = sp.lambdify(x_sym, expr, 'numpy')

# 3. MLX로 가져와서 실제 계산
# (lambdify는 mlx 백엔드를 직접 지원하진 않지만, mlx.array는 numpy 호환이라 가능)
x = mx.array(2.0)
# x_sym 자리에 mlx array를 직접 넣기 어려움 → 수동 전환 or numpy 경유
import numpy as np
result_np = f_np(np.array(2.0))     # numpy로 계산
print(result_np)                    # 11

# 4. MLX에 수동으로 옮겨서 autograd 사용
x = mx.array(2.0)
y = x ** 2 + 3 * x + 1              # 수동으로 MLX에 다시 표현
y.backward()
print(x.grad)                       # array(7, ...)  ← 2x+3 = 7 at x=2
```

### D.3 한계

- **자동 변환 아님**: sympy → MLX 수동 옮겨야 함 (함수 본문 다시 짜야)
- **`lambdify` 백엔드**: `'numpy'`/`'scipy'`는 잘 지원, `'torch'`는 부분적, `'mlx'`는 직접 지원 X
- **복잡한 수식**: 조건문, 룩업이 섞이면 sympy 표현 불가

### D.4 실제 활용 사례

연구/교육에서 실제 쓰는 패턴:
1. **sympy**로 수식을 기호적으로 다룸 (LaTeX, 인수분해, 검증)
2. **lambdify**로 파이썬 함수로 변환
3. **numpy/PyTorch/MLX**로 대규모 수치 계산 + autograd

→ "sympy로 설계하고, PyTorch로 실행한다"는 국룰 워크플로.

**키워드**: `#lambdify` `#sympy2numpy` `#수식컴파일` `#워크플로` `#연구패턴`

---

## E. manim과 DeZero 시각화의 관계

> 브로가 manim + sympy로 수식 애니메이션을 만들어본 경험과 DeZero의 관계.

### E.1 manim이 뭘 하는가?

```python
# 브로가 해봤을 manim + sympy 워크플로 (개념)
from manim import *
import sympy as sp

class FormulaScene(Scene):
    def construct(self):
        x = sp.Symbol('x')
        expr = x ** 2 + 3 * x + 1
        latex_str = sp.latex(expr)              # "$x^2 + 3x + 1$"
        formula = MathTex(latex_str)            # manim 수식 객체
        self.play(Write(formula))               # 애니메이션으로 쓰기
```

→ manim은 **"수식의 시각적 표현"**을 다룸. LaTeX 렌더링 + 애니메이션.

### E.2 DeZero 시각화와의 차이

| | manim + sympy | DeZero (plot_dot_graph) |
|---|---|---|
| **대상** | 수식 (수학적 표현) | 계산 그래프 (연산 흐름) |
| **포맷** | LaTeX → 이미지/애니메이션 | Graphviz DOT → 이미지 |
| **정확성** | 수학적 (x² + 3x + 1) | 절차적 (x → square → add → ...) |
| **목적** | 교육/발표 | 디버깅/이해 |

### E.3 두 개를 합치면?

가상 시나리오:
1. DeZero로 모델 구성 + 학습
2. `plot_dot_graph`로 계산 그래프 시각화 (연산 흐름)
3. **핵심 수식**은 sympy로 분석 + LaTeX 획득
4. manim으로 학습 자료/발표 영상 제작

→ 브로가 manim 해봤으면 DeZero 학습하면서 **"이 step의 핵심 수식을 manim으로 시각화해보자"** 같은 실험도 가능. 학습 효과 극대화!

**키워드**: `#manim` `#수식애니메이션` `#LaTeX` `#교육자료` `#시각화비교`

---

## F. 요약 — 왜 이 질문이 중요한가

### F.1 핵심 통찰

1. **브로의 "오바망상"은 핵심 질문** — sympy vs PyTorch는 컴퓨터 수학의 두 큰 패러다임
2. **DeZero는 수치(numeric) + autograd 패러다임** — sympy와 다름
3. **DeZero도 시각화 지원** — 하지만 수식이 아니라 연산 흐름 (Graphviz)
4. **sympy ↔ MLX 수동 연결 가능** — lambdify로 수식 → 함수 컴파일
5. **manim 경험 자산화 가능** — DeZero 학습하면서 수식 시각화 실험

### F.2 DeZero 학습과의 연결

```
step01 (지금):     Variable 도입 — 숫자를 담는 상자
                  ↓
step04:           수치 미분 (numeric) — dy/dx ≈ (f(x+h) - f(x)) / h
                  ↓
step07~18:        autograd (numeric) — 역전파로 정확한 미분
                  ↓
                  ← 비교 → sympy의 수학적 미분: 2*x + 3 (기호적)
                  ↓
step09+:          plot_dot_graph — 계산 그래프 시각화 (Graphviz)
                  ↓
                  ← 비교 → manim/sympy: 수식 자체 시각화 (LaTeX)
```

→ DeZero 학습하면서 "이건 수치(numeric) 방식이구나, sympy는 다르구나" 비교하면 이해 깊어짐.

### F.3 브로를 위한 후속 탐구 제안 (선택)

- **sympy + MLX 실험**: 같은 수식을 두 방식으로 미분해보고 결과 비교
- **DeZero plot_dot_graph 실사용**: step09 이후 직접 그래프 이미지 생성해보기
- **manim + DeZero**: DeZero 모델을 manim으로 시각화 (오버스펙이지만 재미있음)
- **LaTeX 생성기 만들기**: DeZero 계산 그래프 → LaTeX 수식 변환 (고난도 변형 실험)

**키워드**: `#오바망상아님` `#패러다임이해` `#NumericVsSymbolic` `#DeZero위치` `#후속탐구`

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- DeZero 시각화 함수: `dezero/utils.py`의 `plot_dot_graph`
- sympy 공식: https://docs.sympy.org/
- manim 공식: https://www.manim.community/
- 탐구 #2 (백엔드): [exploration_02_backend_adapters.md](./exploration_02_backend_adapters.md)
