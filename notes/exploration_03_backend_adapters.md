# 🧪 보충 탐구 #3 — 백엔드 어댑터: Variable을 CuPy/MLX로 확장한다면

> **step01 직후 보충 학습 #3** (2026-07-21)
> 2권에서 "CuPy가 NumPy 인터페이스를 따른다"는 이야기를 들었고,
> "MLX도 NumPy 인터페이스?"라는 궁금증에서 출발.
> Variable을 CuPy/MLX 백엔드로 확장하면 어떤 모양일지 초간단 프로토타입으로 살펴봄.

---

## 목차

- [A. NumPy / CuPy / MLX / PyTorch — 인터페이스 비교](#a-numpy--cupy--mlx--pytorch--인터페이스-비교)
- [B. autograd와 Define-by-Run — "표현이 곧 그래프"](#b-autograd와-define-by-run---표현이-곧-그래프)
- [C. Variable을 CuPy/MLX로 확장 — 초간단 프로토타입](#c-variable을-cupymlx로-확장---초간단-프로토타입)
- [D. DeZero의 백엔드 추상화 (cuda.py)](#d-dezero의-백엔드-추상화-cudapy)
- [E. 요약 + MLX 포팅 로드맵 (Issue #1과 연결)](#e-요약--mlx-포팅-로드맵-issue-1과-연결)

---

## A. NumPy / CuPy / MLX / PyTorch — 인터페이스 비교

> 브로가 PyTorch/TF를 안 써봤다고 했으니, 개념부터 차근차근.

### A.1 각 라이브러리의 포지션

| 라이브러리 | 역할 | 인터페이스 | GPU | autograd |
|---|---|---|---|---|
| **NumPy** | 범용 수치 계산 (원조) | — | ❌ | ❌ |
| **CuPy** | NumPy의 GPU 드라이버 | NumPy 거의 복사 | ✅ NVIDIA | ❌ |
| **PyTorch** | 딥러닝 프레임워크 | NumPy 영향 + 자체 | ✅ | ✅ 내장 |
| **MLX** | 딥러닝 프레임워크 (Apple) | PyTorch 영향 | ✅ Apple | ✅ 내장 |
| **DeZero** | 학습용 프레임워크 (이 책) | PyTorch 스타일 | CuPy로 | ✅ 직접 구현 |

### A.2 "NumPy 인터페이스"가 뭔데?

**"NumPy 문법으로 코드를 짜면 그대로 동작한다"**는 뜻. 예를 들어:

```python
# NumPy 코드
import numpy as np
x = np.array([1.0, 2.0, 3.0])
y = np.sum(x ** 2)
print(y)    # 14.0

# CuPy는 import만 바꾸면 그대로 GPU에서 돎
import cupy as cp
x = cp.array([1.0, 2.0, 3.0])
y = cp.sum(x ** 2)
print(y)    # 14.0 (GPU에서 연산)
```

CuPy는 "Drop-in replacement" (그냥 갈아끼우는 대체품)를 목표로 만들어져. 그래서 `numpy.ndarray`와 대응되는 `cupy.ndarray`까지 만들어놨어.

### A.3 CuPy: NumPy 인터페이스 → **맞음**

CuPy 개발팀의 공식 목표:
> "NumPy 코드에서 `import numpy as np`만 `import cupy as cp`로 바꾸면 GPU에서 돈다"

```python
import numpy as np
import cupy as cp

x_np = np.array([1.0, 2.0, 3.0])
x_cp = cp.array([1.0, 2.0, 3.0])

print(type(x_np))    # <class 'numpy.ndarray'>
print(type(x_cp))    # <class 'cupy.ndarray'>  ← 이름까지 똑같음!
```

함수 이름, 메서드, 동작 방식이 90% 이상 일치. CuPy가 "NumPy의 NVIDIA GPU 버전"이라고 불리는 이유.

### A.4 MLX: NumPy 인터페이스? → **절반만 맞음**

MLX는 **PyTorch 영향이 훨씬 큼**. NumPy 비슷한 부분도 있지만, 근본은 PyTorch.

```python
import mlx.core as mx

# NumPy와 비슷한 부분 (생성/연산)
x = mx.array([1.0, 2.0, 3.0])     # ✅ 비슷
print(x.shape)                     # ✅ 비슷
print(mx.sum(x))                   # ✅ 비슷

# PyTorch 냄새가 강한 부분 (autograd)
y = mx.array([1.0, 2.0])
loss = mx.sum((x - y) ** 2)
loss.backward()                    # ← 이게 핵심! (NumPy엔 없는 기능)
grad = x.grad                      # ← 미분 결과
```

→ "NumPy 문법 그대로 MLX로 바꿔서 돈다"는 **아님**. 다만 NumPy 사용자가 배우기엔 쉬운 편.

### A.5 정리 — 브로의 통찰 검증

| 브로 질문 | 정답 |
|---|---|
| "CuPy가 NumPy 인터페이스?" | ✅ 맞음. 거의 완벽히 호환 |
| "MLX도 NumPy 인터페이스?" | ⚠️ 절반만. 실제론 PyTorch에 가까움 |

---

## B. autograd와 Define-by-Run — "표현이 곧 그래프"

> 브로가 핵심을 꿰뚫었어: **"표현 템플릿에서 계산 그래프가 도출된다"**. 이게 Define-by-Run이야!

### B.1 "자동 백프로퍼게이션"이 뭔가요?

일반 NumPy 코드를 보면:

```python
x = np.array(2.0)
y = x ** 2
print(y)    # 4.0

# 이제 dy/dx를 구하고 싶어. NumPy는 모름.
# y가 x로부터 어떻게 만들어졌는지 "기억"을 안 하니까.
```

→ NumPy는 **"어디서 왔는지" 추적 능력이 없음**. 그래서 미분을 사람이 직접 계산해야 해.

PyTorch/MLX는 다름:

```python
import mlx.core as mx

x = mx.array(2.0)
x.grad = None   # 초기화

y = x ** 2       # ← 이 한 줄에서 마법이 일어남!
print(y)         # array(4, dtype=float32)

y.backward()     # 미분해줘!
print(x.grad)    # array(4, dtype=float32)  ← dy/dx = 2x = 4
```

→ **"y를 만드는 과정(x ** 2)을 기억했다가, backward() 호출하면 자동으로 미분"**.

### B.2 어떻게 "기억"하지? — Define-by-Run의 핵심

브로가 "표현 템플릿에서 계산 그래프가 도출"이라고 정확히 짚었어. 그림으로 보면:

```python
x = mx.array(2.0)            # x 노드 생성
#   ┌───┐
#   │ x │  (값: 2.0)
#   └───┘

y = x ** 2                    # 연산을 수행하면서
#   ┌───┐     ┌─────┐     ┌───┐
#   │ x │ ──→ │ **2 │ ──→ │ y │
#   └───┘     └─────┘     └───┘
#   (2.0)                 (4.0)
#
# MLX는 **이 연산을 그래프로 자동 저장**

y.backward()                  # 그래프를 거꾸로 거슬러 올라가며 미분
#   ┌───┐     ┌─────┐     ┌───┐
#   │ x │ ←── │ **2 │ ←── │ y │
#   └───┘     └─────┘     └───┘
#   (grad: 4)  (grad: 1)  (grad: 1)
#
# 체인 룰: dx = dy * d(x**2)/dx = 1 * 2x = 4
```

### B.3 Define-by-Run vs Define-and-Run (비교)

**Define-by-Run** (PyTorch, DeZero, MLX):
- 코드를 **실행하면서** 그래프가 만들어짐
- Python의 if/for문과 자연스럽게 어울림
- 디버깅 쉬움 (한 줄씩 실행되니까)

**Define-and-Run** (구 TensorFlow 1.x, Caffe):
- 그래프를 **미리 정의**하고 나중에 데이터를 흘림
- 성능 최적화엔 유리하지만 코딩이 불편

DeZero 책이 PyTorch 스타일(Define-by-Run)을 따르는 이유: **파이썬 코드로 자연스럽게 그래프를 만들 수 있어서**.

### B.4 DeZero는 autograd를 직접 구현!

여기가 핵심이야. PyTorch/MLX는 C++로 autograd를 구현해놨지만, **DeZero는 Python으로 autograd를 직접 만들어**. 그게 step07~step18의 내용이야.

```python
# DeZero 미래 모습 (step07+)
from dezero import Variable

x = Variable(np.array(2.0))
y = x ** 2              # ← 연산하면서 그래프 저장
y.backward()            # ← 역전파 수행
print(x.grad)           # 4.0  ← 미분 결과
```

→ 브로가 step01에서 만든 Variable이 **이 과정의 시작점**이야. 지금은 `self.data`만 있지만, 앞으로:
- `self.grad` (미분 결과) — step07
- `self.creator` (이 Variable을 만든 함수) — step07
- `self.generation` (역전파 우선순위) — step16

이런 메타정보가 추가되면서 autograd가 완성돼.

**키워드**: `#autograd` `#자동미분` `#DefineByRun` `#계산그래프` `#역전파` `#체인룰` `#PyTorch` `#MLX`

---

## C. Variable을 CuPy/MLX로 확장 — 초간단 프로토타입

> step01 수준의 단순 Variable을 CuPy/MLX 백엔드로 만들면 어떤 모양일지 살펴봄.

### C.1 현재 rezero의 Variable (NumPy 전용)

```python
import numpy as np

class Variable:
    def __init__(self, data):
        self.data = data           # data는 numpy.ndarray라고 가정

x = Variable(np.array(1.0))
print(x.data)   # 1.0
```

문제: `data`가 무조건 `numpy.ndarray`여야 함. GPU(Apple Silicon) 못 씀.

### C.2 접근 방식 3가지

#### 방식 1: 각 백엔드마다 별도 Variable 클래스

```python
# numpy_variable.py
import numpy as np

class Variable:                    # NumPy 전용
    def __init__(self, data):
        self.data = np.asarray(data)

# mlx_variable.py
import mlx.core as mx

class Variable:                    # MLX 전용
    def __init__(self, data):
        self.data = mx.array(data)
```

❌ **단점**: 코드가 중복됨. 한 번 수정하면 두 군데 다 고쳐야 함.

#### 방식 2: 백엔드를 인자로 받기

```python
class Variable:
    def __init__(self, data, backend="numpy"):
        if backend == "numpy":
            import numpy as np
            self.data = np.asarray(data)
        elif backend == "mlx":
            import mlx.core as mx
            self.data = mx.array(data)
        else:
            raise ValueError(f"Unknown backend: {backend}")
```

❌ **단점**: 모든 메서드마다 if/elif 남발. 코드 지저분.

#### 방식 3: `xp` 패턴 (DeZero 방식) — 백엔드 모듈 자체를 교체 ⭐

```python
class Variable:
    def __init__(self, data):
        # data가 뭘로 만들어졌든 그대로 받음
        self.data = data

# 백엔드를 외부에서 결정
import numpy as np        # CPU
# import cupy as cp       # NVIDIA GPU (macOS에선 안 됨)
# import mlx.core as mx   # Apple Silicon GPU

# 사용자가 알아서 백엔드 선택
xp = np                    # 또는 cp, mx
x = Variable(xp.array([1.0, 2.0, 3.0]))
print(x.data)              # [1. 2. 3.]
```

✅ **장점**: Variable 클래스 자체는 백엔드 무관. 백엔드 선택은 사용자 책임.

이게 DeZero가 택한 방식이야. 핵심 헬퍼가 `get_array_module()`.

### C.3 `xp` 패턴이 강력한 이유

```python
# 사용자 코드는 백엔드 바꿔도 그대로 동작
def my_computation(xp):
    x = xp.array([1.0, 2.0, 3.0])
    y = xp.sum(x ** 2)
    return y

import numpy as np
print(my_computation(np))         # NumPy로 실행 (CPU)

import cupy as cp                  # NVIDIA GPU가 있으면
print(my_computation(cp))          # CuPy로 실행 (GPU)

import mlx.core as mx              # Apple Silicon이면
print(my_computation(mx))          # MLX로 실행 (GPU)
```

→ `xp`라는 변수에 모듈을 할당해두면, **나머지 코드는 그대로**. 이래서 CuPy가 NumPy 인터페이스를 따른 게 큰 의미가 있음.

### C.4 초간단 "멀티 백엔드 Variable" 프로토타입

```python
"""
초간단 멀티 백엔드 Variable — step01 수준.
NumPy / CuPy / MLX 중 하나를 선택해 사용.
"""
import numpy as np


def get_array_module(x):
    """데이터 x를 보고 어느 백엔드 모듈을 쓸지 결정."""
    if hasattr(x, '__mlx_array__'):
        import mlx.core as mx
        return mx
    elif 'cupy' in str(type(x)):
        import cupy as cp
        return cp
    else:
        return np


class Variable:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Variable(data={self.data}, type={type(self.data).__module__})"


# --- 사용 예 ---

# 1. NumPy (CPU)
x_np = Variable(np.array([1.0, 2.0, 3.0]))
xp = get_array_module(x_np.data)
y = xp.sum(x_np.data ** 2)
print(f"NumPy: {y}")               # 14.0

# 2. CuPy (NVIDIA GPU) — 설치되어 있으면
# import cupy as cp
# x_cp = Variable(cp.array([1.0, 2.0, 3.0]))
# xp = get_array_module(x_cp.data)
# y = xp.sum(x_cp.data ** 2)

# 3. MLX (Apple Silicon GPU) — 설치되어 있으면
# import mlx.core as mx
# x_mx = Variable(mx.array([1.0, 2.0, 3.0]))
# xp = get_array_module(x_mx.data)
# y = xp.sum(x_mx.data ** 2)
```

→ 핵심 통찰: **Variable 자체는 단순한 상자**. 백엔드 추상화는 `get_array_module()` 헬퍼가 담당.

### C.5 DeZero가 실제로 쓰는 패턴 (cuda.py)

```python
# dezero/cuda.py (단순화)
import numpy as np

gpu_enable = True
try:
    import cupy as cp
    cupy = cp
except ImportError:
    gpu_enable = False


def get_array_module(x):
    """x를 보고 numpy 또는 cupy 반환."""
    if isinstance(x, Variable):
        x = x.data
    if not gpu_enable:
        return np
    return cp.get_array_module(x)


def as_numpy(x):
    """어떤 백엔드든 numpy로 변환."""
    if np.isscalar(x):
        return np.array(x)
    elif isinstance(x, np.ndarray):
        return x
    return cp.asnumpy(x)


def as_cupy(x):
    """numpy를 cupy로 변환."""
    return cp.asarray(x)
```

→ MLX 포팅하려면 `as_cupy` 자리에 `as_mlx` 추가하고, `get_array_module`이 MLX도 인식하게 확장하면 됨. **이게 Issue #1 (MLX 백엔드)의 핵심 작업**.

**키워드**: `#xp패턴` `#get_array_module` `#백엔드추상화` `#드롭인대체` `#MLX포팅` `#Issue1`

---

## D. DeZero의 백엔드 추상화 (cuda.py)

실제 `dezero/cuda.py`를 보면 위에서 설명한 `xp` 패턴이 그대로 쓰임.

### D.1 cuda.py의 구조

```python
import numpy as np
gpu_enable = True
try:
    import cupy as cp
    cupy = cp
except ImportError:
    gpu_enable = False
from dezero import Variable


def get_array_module(x):
    """x가 ndarray인지 cupy.ndarray인지 판별해서 모듈 반환."""
    if isinstance(x, Variable):
        x = x.data
    if not gpu_enable:
        return np
    xp = cp.get_array_module(x)
    return xp


def as_numpy(x):
    """어떤 백엔드든 numpy.ndarray로 변환."""
    if isinstance(x, Variable):
        x = x.data
    if np.isscalar(x):
        return np.array(x)
    elif isinstance(x, np.ndarray):
        return x
    return cp.asnumpy(x)


def as_cupy(x):
    """numpy를 cupy.ndarray로 변환."""
    if isinstance(x, Variable):
        x = x.data
    if not gpu_enable:
        raise Exception('CuPy cannot be loaded. Install CuPy!')
    return cp.asarray(x)
```

### D.2 MLX로 확장하려면?

`cuda.py`의 구조를 MLX용으로 확장하려면 (개념적):

```python
import numpy as np

# 백엔드별 활성화 상태
gpu_enable = True
mlx_enable = True

try:
    import cupy as cp
except ImportError:
    gpu_enable = False

try:
    import mlx.core as mx
except ImportError:
    mlx_enable = False


def get_array_module(x):
    """x가 무슨 타입인지 보고 적절한 백엔드 모듈 반환."""
    if isinstance(x, Variable):
        x = x.data
    if mlx_enable and hasattr(x, '__mlx_array__'):
        return mx                  # ← MLX 배열
    if gpu_enable and 'cupy' in str(type(x)):
        return cp                  # ← CuPy 배열
    return np                      # ← 기본 (NumPy)


def as_numpy(x):
    """어떤 백엔드든 numpy로."""
    if mlx_enable and hasattr(x, '__mlx_array__'):
        return np.array(x)         # MLX → NumPy 변환
    if gpu_enable:
        return cp.asnumpy(x)
    return x


def as_mlx(x):
    """numpy/cupy를 MLX로."""
    if not mlx_enable:
        raise Exception('MLX cannot be loaded. Install MLX!')
    return mx.array(x)
```

→ 핵심은 **`get_array_module` 하나의 함수**가 모든 백엔드를 판별. 이게 잘 동작하면 Variable은 건드릴 필요 없음.

### D.3 DeZero 전체에 미치는 영향

DeZero의 모든 함수(add, mul, sin, ...)는 내부적으로 이런 식으로 동작:

```python
class Add(Function):
    def forward(self, x0, x1):
        xp = get_array_module(x0)      # ← 이 한 줄이 백엔드 추상화 핵심
        return xp.asarray(x0 + x1)     # np/cp/mx 중 알아서 선택

    def backward(self, gy):
        ...
```

→ `xp`를 쓰면 같은 코드가 NumPy/CuPy/MLX에서 다 동작. 이래서 CuPy가 NumPy 인터페이스를 따른 게 중요한 거야.

**키워드**: `#cuda.py` `#get_array_module` `#as_numpy` `#as_cupy` `#as_mlx` `#백엔드확장` `#드롭인`

---

## E. 요약 + MLX 포팅 로드맵 (Issue #1과 연결)

### E.1 핵심 통찰 요약

1. **CuPy ≈ NumPy** 인터페이스 (거의 완벽 호환, NVIDIA GPU)
2. **MLX ≈ PyTorch** 인터페이스 (NumPy와 부분만 호환, Apple GPU, autograd 내장)
3. **autograd** = "코드 실행하면서 그래프 자동 생성 → backward()로 미분"
4. **Define-by-Run** = PyTorch/DeZero/MLX가 채택한 패턴. 표현이 곧 그래프
5. **DeZero는 Python으로 autograd 직접 구현** — step07~step18이 그 과정
6. **백엔드 추상화 핵심** = `get_array_module()` 한 함수. CuPy/MLX 다 이걸로 확장

### E.2 브로가 step01에서 만든 Variable의 위치

```
step01 (지금):     Variable은 단순 상자 (.data만 있음)
                  ↓
step07~18:         Variable에 grad/creator/generation 추가 → autograd 구현
                  ↓
step33+:           Variable이 텐서(다차원) 지원, core.py로 이관
                  ↓
(DeZero 완성):     cuda.py가 백엔드 추상화 담당 (NumPy/CuPy)
                  ↓
(Issue #1, 미래):  MLX 백엔드 추가 — cuda.py 확장으로 가능
                  ↓                  get_array_module에 MLX 인식 추가
                                  rezero/cuda.py에서 실험
```

### E.3 MLX 포팅 로드맵 (Issue #1)

Issue #1의 세부 단계 (이 탐구 노트가 그 초안 겸):

| 단계 | 작업 | 난이도 |
|---|---|---|
| 1 | MLX 설치 + 기본 동작 확인 (mx.array 생성/연산) | ⭐ |
| 2 | `rezero/cuda.py`에 `as_mlx`, `get_array_module` MLX 확장 | ⭐⭐ |
| 3 | Variable이 mlx.array도 담을 수 있게 (사실 이미 됨 — data는 any type) | ⭐ |
| 4 | 사칙연산(add/mul) 함수를 xp 패턴으로 재작성 | ⭐⭐ |
| 5 | 기본 역전파가 MLX에서도 동작하는지 검증 | ⭐⭐⭐ |
| 6 | sin/matmul 등 주요 함수 MLX 지원 | ⭐⭐⭐ |
| 7 | VGG16 등 examples를 MLX로 돌려보기 | ⭐⭐⭐⭐ |

→ step01에서 배운 개념(Variable, 래퍼 패턴)이 **MLX 포팅의 토대**가 됨. 브로가 만든 Variable이 사실 이미 백엔드 무관야 (`data`가 any type이니까).

### E.4 핵심 딜레마 (앞으로 풀 과제)

MLX 포팅 시 가장 큰 결정:
- **DeZero 자체 역전파 유지** + MLX는 forward 연산 가속만?
- **아니면 MLX의 autograd 적극 활용** + DeZero는 thin wrapper?

| 접근 | 장점 | 단점 |
|---|---|---|
| DeZero 역전파 유지 | 학습 목적 부합, step01~18 코드 재사용 | MLX 최적화 일부 포기 |
| MLX autograd 활용 | 성능 극대화 | DeZero 학습 의미 상실 |

→ DeZero 책의 목적(역전파 직접 구현으로 학습)을 생각하면 **전자 권장**. 단, 학습 완료 후 실험적으로 후자도 시도해볼 만함.

**키워드**: `#MLX포팅로드맵` `#Issue1` `#역전파딜레마` `#forward가속` `#autograd활용`

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- Issue #1: https://github.com/ghjang/deep-learning-from-scratch-3/issues/1
- DeZero 백엔드 코드: `dezero/cuda.py`
- rezero 백엔드 자리: `rezero/cuda.py`

**다음 step**: step02 (Function 도입) — `__call__`이 Function 인스턴스를 함수처럼 호출하는 역할. 이게 Define-by-Run의 시작.
