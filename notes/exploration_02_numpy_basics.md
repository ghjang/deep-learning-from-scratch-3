# 🧪 보충 탐구 #2 — NumPy 기본 (3권 중심)

> **step01 직후 보충 학습 #2** (2026-07-21)
> 탐구 #1(Python 기본)에서 다루던 NumPy 섹션을 분리.
> 3권(DeZero)에서 자주 쓰는 NumPy 사용법 위주로 정리.

---

## 목차

- [A. ndarray의 본질 — 내부 구조](#a-ndarray의-본질--내부-구조)
- [B. shape, size, ndim — 형태 정보](#b-shape-size-ndim--형태-정보)
- [C. 차원과 축 — 0차원 스칼라부터 고차원 텐서까지](#c-차원과-축--0차원-스칼라부터-고차원-텐서까지)
- [D. 배열 생성 — 3권에서 자주 쓰는 패턴](#d-배열-생성--3권에서-자주-쓰는-패턴)
- [E. 인덱싱과 슬라이싱](#e-인덱싱과-슬라이싱)
- [F. 브로드캐스팅](#f-브로드캐스팅)
- [G. 수학 함수 — 3권에서 자주 등장](#g-수학-함수--3권에서-자주-등장)
- [H. 난수 (np.random)](#h-난수-nprandom)
- [I. 형태 변환 — reshape, transpose, np.newaxis](#i-형태-변환--reshape-transpose-npnewaxis)
- [J. 3권에서 특별히 자주 쓰는 유틸](#j-3권에서-특별히-자주-쓰는-유틸)

---

## A. ndarray의 본질 — 내부 구조

**요약**: `ndarray`는 **C 구조체 + 연속 메모리 블록** 기반. 파이썬 객체는 얇은 헤더(메타정보)만 가지고, 실제 데이터는 C 배열에. 이래서 빠름.

```python
arr = np.array([[1.0, 2.0], [3.0, 4.0]])
# 내부 구조 (단순화):
# ┌────────────────────┐
# │ ndarray 헤더        │  ← shape, dtype, strides 등 메타 (파이썬 객체)
# ├────────────────────┤
# │ 1.0 │ 2.0 │ 3.0 │ 4.0 │  ← 연속 C 메모리 (진짜 데이터)
# └────────────────────┘
print(arr.shape)     # (2, 2)  ← 헤더 정보
print(arr.dtype)     # float64
print(arr.strides)   # (16, 8)  ← 각 축 이동 시 바이트 수
```

- `strides`: 다음 요소로 가는 바이트 오프셋. (16, 8) = 행 이동 16바이트, 열 이동 8바이트
- 이 구조 덕분에 `reshape`, `transpose`가 **데이터 복사 없이** 메타만 바꿔서 O(1)로 동작
- 고차원 배열도 메모리는 **1차원 평탄화**되어 저장. shape/strides로 다차원 해석

**키워드**: `#ndarray` `#C기반` `#strides` `#연속메모리` `#dtype` `#헤더`

---

## B. shape, size, ndim — 형태 정보

**요약**: 셋 다 배열의 "형태"를 묘사하지만 다른 정보. 외워두면 NumPy 생활이 편해짐.

```python
arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

print(arr.ndim)     # 2          ← 차원 수 (축 개수)
print(arr.shape)    # (2, 3)     ← 각 축의 크기 튜플
print(arr.size)     # 6          ← 전체 원소 수 = prod(shape)

# 관계: size == shape 원소들의 곱
# (2, 3) → 2 * 3 = 6
# (2, 3, 4) → 24

# 다른 예
np.array(5).shape          # ()      0차원
np.array([1,2,3]).shape    # (3,)    1차원 (길이 3)
np.array([[1],[2]]).shape  # (2, 1)  2차원
```

- `ndim` = `len(shape)` (항상)
- `size` = `prod(shape)` (항상)
- DeZero에선 보통 `shape`을 많이 씀 (레이어 출력 형태 맞출 때)

**키워드**: `#shape` `#size` `#ndim` `#형태정보` `#prod`

---

## C. 차원과 축 — 0차원 스칼라부터 고차원 텐서까지

**요약**: 수학에서 **스칼라**는 0차원. "축"이 없는 단일 값. NumPy는 이 수학적 정의를 그대로 따름. 괄호를 하나 감쌀 때마다 차원이 1씩 증가.

### C.1 괄호 수 = 차원 수

```python
# 괄호 수 = 차원 수
np.array(5)             # 0차원, shape ()
np.array([5])           # 1차원, shape (1,)
np.array([[5]])         # 2차원, shape (1, 1)
np.array([[[5]]])       # 3차원, shape (1, 1, 1)
# 전부 "원소는 5 하나"지만 차원이 다름

# 수학 대응:
#   스칼라   → 0차원   5
#   벡터    → 1차원   [1, 2, 3]
#   행렬    → 2차원   [[1,2],[3,4]]
#   텐서    → 3차원+  이미지, 시계열 등
```

### C.2 DeZero 단계별 차원

- step01~step40: 스칼라/벡터(0~1차원) 위주
- step41+: 텐서(2차원+) 다루기 시작
- VGG16 같은 CNN은 4차원(N, C, H, W) — 배치 N, 채널 C, 높이 H, 너비 W

### C.3 축(axis) 개념

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
#         axis 0 (행) ↓
#                  [1, 2, 3]
#                  [4, 5, 6]
#         axis 1 (열) →

print(arr.sum(axis=0))   # [5, 7, 9]  ← axis 0 따라 합 (열별 합)
print(arr.sum(axis=1))   # [6, 15]    ← axis 1 따라 합 (행별 합)
```

→ axis는 "그 방향으로 스쿼시(축소)"한다고 생각하면 쉬워.

**키워드**: `#스칼라` `#0차원` `#괄호수` `#수학대응` `#axis` `#축` `#스쿼시`

---

## D. 배열 생성 — 3권에서 자주 쓰는 패턴

3권 코드에서 가장 자주 등장하는 배열 생성 패턴들.

### D.1 `np.array` (90회 사용, 1위)

```python
# 0차원 스칼라
x = np.array(1.0)

# 1차원 벡터
x = np.array([1.0, 2.0, 3.0])

# 다차원
x = np.array([[1, 2], [3, 4]])

# dtype 명시 (3권에선 float64가 기본)
x = np.array([1, 2, 3], dtype=np.float64)
```

### D.2 `np.zeros`, `np.ones`, `np.empty` — 초기화

```python
np.zeros((2, 3))        # 0으로 채운 2x3 배열 (grad 초기화 등)
np.ones((3,))           # 1로 채운 길이 3 벡터
np.empty((2, 2))        # 쓰레기값 (초기화 안 함, 속도 우선)
```

→ DeZero에선 `grad` 초기화(`Variable.grad = None` 후 `np.zeros_like`)에 자주 씀.

### D.3 `np.zeros_like`, `np.ones_like` — 기존 배열 형태 복사 (14회)

```python
x = np.array([[1.0, 2.0], [3.0, 4.0]])
grad = np.zeros_like(x)         # x와 같은 shape/dtype의 0 배열
# shape (2, 2), dtype float64
```

→ DeZero 역전파에서 gradient 초기화 용도로 엄청 자주 씀.

### D.4 `np.arange`, `np.linspace` — 범위 생성

```python
np.arange(0, 10, 2)     # [0, 2, 4, 6, 8]   시작, 끝, step
np.linspace(0, 1, 5)    # [0, 0.25, 0.5, 0.75, 1.0]   시작, 끝, 개수
```

### D.5 `np.asarray` — 이미 배열이면 복사 X

```python
x = np.array([1, 2, 3])
y = np.asarray(x)       # x가 이미 ndarray면 같은 객체 반환 (복사 X)
z = np.array(x)         # 항상 복사
```

→ DeZero에선 "입력이 이미 ndarray인지 확인" 용도로 자주 씀.

**키워드**: `#np.array` `#np.zeros` `#np.zeros_like` `#np.arange` `#np.asarray` `#초기화` `#dtype`

---

## E. 인덱싱과 슬라이싱

### E.1 기본 인덱싱

```python
arr = np.array([1, 2, 3, 4, 5])
print(arr[0])           # 1   첫 원소
print(arr[-1])          # 5   마지막
print(arr[1:3])         # [2, 3]   슬라이스

# 다차원
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(arr2d[0, 1])      # 2   (행 0, 열 1)
print(arr2d[:, 1])      # [2, 5]   모든 행의 열 1
print(arr2d[0, :])      # [1, 2, 3]   행 0 전체
```

### E.2 팬시 인덱싱 (리스트로 인덱싱)

```python
arr = np.array([10, 20, 30, 40, 50])
print(arr[[0, 2, 4]])   # [10, 30, 50]   여러 인덱스 한번에

# 불리언 마스크
mask = arr > 20
print(mask)             # [False, True, True, True, True]
print(arr[mask])        # [30, 40, 50]
```

### E.3 DeZero에서의 활용 (step21 `get_item`)

```python
# 3권에선 Variable에도 인덱싱 적용 (step21)
x = Variable(np.array([[1,2,3],[4,5,6]]))
y = F.get_item(x, 0)        # 행 0 가져오기
```

**키워드**: `#인덱싱` `#슬라이싱` `#팬시인덱싱` `#불리언마스크`

---

## F. 브로드캐스팅

**요약**: 다른 shape의 배열 간 연산을 위해 NumPy가 자동으로 shape을 맞추는 기능. 3권 step13~14에서 중요.

### F.1 기본 예시

```python
# 스칼라 + 벡터
x = np.array([1, 2, 3])
print(x + 10)           # [11, 12, 13]   10이 [10,10,10]으로 브로드캐스트

# 벡터 + 행렬
A = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3)
b = np.array([10, 20, 30])               # shape (3,)
print(A + b)
# [[11, 22, 33],
#  [14, 25, 36]]
# b가 (2, 3)으로 브로드캐스트
```

### F.2 브로드캐스팅 규칙

오른쪽 축부터 비교, 다음 조건 중 하나 만족하면 가능:
1. 둘 중 하나가 1
2. 둘이 같음

```python
# 가능: (2, 3) + (3,)        ← (3,)이 (2, 3)으로 확장
# 가능: (2, 3) + (2, 1)      ← (2, 1)이 (2, 3)으로 확장
# 가능: (2, 3) + (1, 3)      ← (1, 3)이 (2, 3)으로 확장
# 불가: (2, 3) + (2,)        ← 축 안 맞음
```

### F.3 역전파에서의 함정 (3권 step13)

브로드캐스트 된 연산은 역전파에서 shape을 원래대로 되돌리는 작업 필요:
```python
# 순전파: x (3,) + b (2,3) → y (2,3)  (b가 (2,3)으로 확장)
# 역전파: dy (2,3) → dx은 다시 (3,)이어야 함
#         → axis=0 따라 sum으로 축소
```

→ DeZero의 `sum_to`, `reshape_sum_backward` 함수가 이 작업 담당.

**키워드**: `#브로드캐스팅` `#shape자동확장` `#역전파함정` `#sum_to`

---

## G. 수학 함수 — 3권에서 자주 등장

### G.1 기본 수학 (빈도순)

```python
np.exp(x)               # e^x (활성화, softmax)
np.log(x)               # 자연로그
np.sqrt(x)              # 제곱근
np.sin(x), np.cos(x)    # 삼각함수 (step28 등)
np.pi                   # 3.141592... (상수)
```

### G.2 합/평균/최대

```python
x = np.array([[1, 2, 3], [4, 5, 6]])

np.sum(x)               # 21   전체 합
np.sum(x, axis=0)       # [5, 7, 9]   열별 합
np.sum(x, axis=1)       # [6, 15]     행별 합
np.sum(x, axis=1, keepdims=True)  # [[6], [15]]   차원 유지

np.mean(x)              # 3.5
np.max(x)               # 6
np.argmax(x)            # 가장 큰 원소의 인덱스
```

### G.3 행렬 연산

```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

A @ B                   # 행렬곱 (Python 3.5+)
np.dot(A, B)            # 같은 의미
A * B                   # 원소별 곱 (Hadamard, 행렬곱 아님!)
A.T                     # 전치
np.linalg.inv(A)        # 역행렬
```

→ `@` vs `*` 차이 주의. 3권 step35 (MatMul)에서 핵심.

**키워드**: `#np.exp` `#np.sum` `#axis` `#keepdims` `#행렬곱` `#Ad연산자` `#MatMul`

---

## H. 난수 (np.random)

3권에선 테스트 데이터, 가중치 초기화에 자주 사용 (37회).

### H.1 주요 함수

```python
np.random.rand(2, 3)        # 0~1 균일분포, shape (2, 3)
np.random.randn(2, 3)       # 표준정규분포 (평균 0, 표준편차 1)
np.random.randint(0, 10, 5) # 0~9 정수 5개
np.random.seed(42)          # 시드 고정 (재현성)
```

### H.2 가중치 초기화 (DeZero에서 자주 쓰는 패턴)

```python
W = np.random.randn(in_size, out_size) * np.sqrt(2.0 / in_size)  # He 초기화
# 또는
W = np.random.randn(in_size, out_size) * 0.01                     # 단순 버전
```

### H.3 재현성 — 시드 고정

```python
np.random.seed(0)            # 같은 시드 → 같은 난수
np.random.rand(3)            # 항상 같은 결과
```

→ 테스트/디버깅 시 필수. 3권에선 종종 등장.

**키워드**: `#np.random` `#rand` `#randn` `#seed` `#가중치초기화` `#재현성`

---

## I. 형태 변환 — reshape, transpose, np.newaxis

### I.1 reshape

```python
x = np.arange(6)             # [0, 1, 2, 3, 4, 5]
y = x.reshape(2, 3)          # [[0,1,2],[3,4,5]]
y = x.reshape(-1, 2)         # -1은 자동 계산 → (3, 2)
```

→ 데이터 복사 없이 메타만 바꿈 (strides 활용). O(1).

### I.2 transpose

```python
x = np.array([[1, 2, 3], [4, 5, 6]])   # shape (2, 3)
y = x.T                                  # shape (3, 2)
y = x.transpose(1, 0)                    # 같은 의미
```

### I.3 np.newaxis — 차원 추가 (4회)

```python
x = np.array([1, 2, 3])          # shape (3,)
y = x[:, np.newaxis]             # shape (3, 1)   열 벡터화
z = x[np.newaxis, :]             # shape (1, 3)   행 벡터화
```

→ `None`을 써도 동일: `x[:, None]`.

**키워드**: `#reshape` `#transpose` `#np.newaxis` `#차원추가` `#strides`

---

## J. 3권에서 특별히 자주 쓰는 유틸

### J.1 `np.isscalar` (19회) — 스칼라 판별

```python
np.isscalar(5)           # True
np.isscalar(5.0)         # True
np.isscalar(np.array(5)) # False! 0차원 배열은 스칼라 아님
```

→ DeZero에선 "입력이 ndarray인지 확인"하는 곳에 자주 등장.

### J.2 `np.allclose` (2회+) — 부동소수점 비교

```python
a = np.array([0.1 + 0.2])
b = np.array([0.3])
print(a == b)            # [False]   부동소수점 오차!
print(np.allclose(a, b)) # True      허용 오차 내 비교
```

→ DeZero 테스트(`tests/`)에서 검증 용도로 자주 사용.

### J.3 `np.ndarray` 타입 체크

```python
isinstance(x, np.ndarray)    # x가 ndarray인지 확인
# DeZero의 as_array, as_variable 등에서 자주 쓰임
```

### J.4 데이터 영속화 (데이터셋 캐싱)

```python
np.savez_compressed('data.npz', x=x, y=y)   # 압축 저장
data = np.load('data.npz')                    # 로드
x = data['x']
```

→ DeZero의 MNIST, PTB 데이터셋 캐싱에 사용.

**키워드**: `#np.isscalar` `#np.allclose` `#부동소수점비교` `#데이터캐싱` `#타입체크`

---

## 요약 — 3권 학습을 위한 NumPy 최소 요건

| 기능 | 중요도 | 언제 쓰임 |
|---|---|---|
| `np.array`, shape/ndim/size | ⭐⭐⭐⭐⭐ | 모든 step |
| `np.zeros_like` (초기화) | ⭐⭐⭐⭐ | 역전파 (step07+) |
| 브로드캐스팅 | ⭐⭐⭐⭐ | step13+, 역전파 shape 복원 |
| axis, keepdims | ⭐⭐⭐⭐ | sum, mean 등 (step26+) |
| 행렬곱 `@` | ⭐⭐⭐⭐ | step35 (MatMul) |
| `np.random` | ⭐⭐⭐ | 가중치 초기화, 테스트 |
| `np.exp`, `np.sin` 등 | ⭐⭐⭐ | 활성화 함수, 미분 예제 |
| `reshape`, `transpose` | ⭐⭐⭐ | 텐서 연산 (step41+) |
| `np.newaxis` | ⭐⭐ | shape 맞추기 |
| `np.isscalar`, `np.allclose` | ⭐⭐ | 입력 검증, 테스트 |

→ 모르는 게 나오면 이 문서로 돌아와서 찾아보기.

---

**학습 완료일**: 2026-07-21
**관련 링크**:
- 탐구 #1 (Python 기본): [exploration_01_python_basics.md](./exploration_01_python_basics.md)
- NumPy 공식 문서: https://numpy.org/doc/
