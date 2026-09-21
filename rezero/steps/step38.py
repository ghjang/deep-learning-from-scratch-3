"""
rezero.steps.step38 — [4고지] 형상 변환 함수
=====================================================================

★ 책 공식 제목 "형상 변환 함수" (브로 확인, 2026-09-21). 제 4고지 "신경망
만들기" (step37~51) 두 번째 스텝.

★★★ 이 step의 성격 — 신경망 시대의 shape 인프라:

    step37이 "텐서를 1급 시민으로 선언"했다면, step38은 그 텐서의 **shape을
    다루는 도구** 확보. 신경망의 실체는 행렬 곱(MatMul, step41 예고)인데
    행렬 곱은 shape 계약이 까다롭다 — (은닉 수, 배치) 맞추기.
    37(텐서) → 38(형상 변환) → 39(sum 확장) → ... → 41(MatMul) 순서로
    shape 관리 연산을 쌓아올리는 구성.

    reshape/transpose의 공통 성질: **값은 하나도 안 바꾸고 shape만 이동**.
    순전파가 shape을 바꾸면 역전파는 shape을 되돌린다 — 미분의 본체가
    "곱"이 아니라 "이동".

★★ 감동 포인트 (가이드에서 후보 제시 → 브로 세 결정과 함께 확정):

    1. "미분은 형상을 기억한다" — Reshape은 forward 시점의 입력 shape을
       스냅샷(self.x_shape)으로 기억하고, backward에서 upstream을 그 shape으로
       되돌린다. step37 "브로드캐스팅 = 미분의 shape 복원 장치"(Sum의 ones)에
       이은 shape 이야기 2막.

    2. ★★ 도함수 성분 유형 지도 ⑤ upstream형의 첫 등장 — rezero의 backward
       뼈대는 df(x) * upstream **곱셈 fold**. 그런데 reshape/transpose는 곱셈으로
       표현 불가: 도함수는 입력 shape, upstream은 출력 shape → 브로드캐스팅도
       성립 안 함 ((6,) * (2,3) → 브로드캐스팅 실패. Sum의 "ones * 0-dim" 트릭이
       안 통하는 이유). 따라서 v3 **첫 backward 직접 오버라이드 함수**.
       지도 ⑤가 예언해둔 관례의 첫 사례 (본격 사례는 MatMul — 이슈 47).

    3. transpose의 미분은 transpose — 자기 역함수(involution). 전치의 전치는
       항등. Neg과 같은 "자기 역" 부류. backward가 forward와 같은 호출.

★ 변형 포인트 3개 — 브로 결정 (2026-09-21):
    1. 구현 방식: backward 직접 오버라이드 — "전통적 미분이라 부르기 애매한"
       연산을 곱셈 fold에 우겨넣지 않는다 (브로 동감).
    2. no-op 최적화: 채택 — 같은 shape이면 노드 생성 없이 x 자체 반환.
       나쁠 게 없음 (계산/메모리 이득, 수학적 손실 0).
    3. x_shape 기억: dezero 방식 (forward 스냅샷) — backward 시점 상태에
       의존 안 하는 쪽이 견고 + PyTorch 관례 + "기억"이라는 개념과 코드 일치
       (AI 위임 결정, 브로 승인).

★★★ NumPy 경고 — view 메모리 공유 (브로 요청 문서화, 2026-09-21):

    np.reshape은 가능하면 **view**를 반환 — y.data와 x.data가 같은 버퍼를
    공유할 수 있다 (데모 7에서 np.shares_memory로 실증). transpose도 항상 view.
    rezero 전제(data를 불변처럼 사용)에서는 안전하지만, in-place 연산이
    미래에 등장하면 한쪽 수정이 다른 쪽을 오염시키는 함경 지점.
    → Reshape/Transpose 클래스 docstring + 테스트 canary로 기록.

★ 스코프 방침 (브로 — "현재 스텝 집중 + 확장 포인트 기록"):
    - Transpose는 axes=None 최소분 (전체 축 역순만). axes 지정 전치와 역치환
      계산(np.argsort)은 정답지 최종형(dezero/functions.py)에만 기록 참조 —
      합성곱(5고지) 언저리에서 필요해지면 그때 확장.
    - Variable.transpose() 메서드도 미추가 — 데모는 x.T(프로퍼티)로 충분.
      VariableShapeMixin에 같은 패턴으로 추가하면 되는 자리.

실행: uv run python rezero/steps/step38.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v3 import Variable, fill_grad, numerical_diff, reshape, square, sum, transpose


# ===== 데모 1 — 정답지 steps/step38.py 재현 (reshape) ==========================
print("=== 데모 1: 정답지 재현 — reshape + 역전파 ===")

x = Variable(np.array([[0, 1, 2], [3, 4, 5]]))
y = reshape(x, (6,))   # y = x.reshape(6) 와 동일 (메서드판은 데모 4)

fill_grad(y, retain_grad=True)

assert y.grad is not None and y.grad.data is not None
assert x.grad is not None and x.grad.data is not None
print(f"y.data = {y.data}")          # [0 1 2 3 4 5] — 값 보존, (6,)으로 평탄화
print(f"y.grad = {y.grad.data}")     # 1.0 — 0-dim
print(f"x.grad =\n{x.grad.data}")    # ones(2,3) — ★ 입력 shape으로 왕복

np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))
print("→ (2,3) → (6,)의 grad가 ones(2,3): 미분은 '입력'의 shape을 기억한다")


# ===== 데모 2 — 정답지 steps/step38.py 재현 (transpose) ========================
print()
print("=== 데모 2: 정답지 재현 — transpose + 역전파 ===")

x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
y = transpose(x)   # y = x.T 와 동일

fill_grad(y)

assert x.grad is not None and x.grad.data is not None
print(f"y.data =\n{y.data}")         # (3,2) — 행/열 교환
print(f"x.grad =\n{x.grad.data}")    # ones(2,3)

np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))
print("→ 전치의 역전파 = 전치 (involution): backward가 forward와 같은 호출")


# ===== 데모 3 — no-op 최적화 관찰 =============================================
print()
print("=== 데모 3: no-op 최적화 — 같은 shape이면 노드를 안 만든다 ===")

x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
y = reshape(x, (2, 2))   # 이미 (2,2) — 항등 reshape

print(f"y is x → {y is x}")           # True — 동일 객체 (노드 0개)
print(f"y.creator → {y.creator}")     # None

assert y is x and y.creator is None

# 그래프 중간 no-op — 역전파는 creator 체인을 그대로 탄다
z = square(x)
w = reshape(z, (2, 2))
assert w is z and w.creator is not None and type(w.creator).__name__ == "Square"

fill_grad(w)
assert x.grad is not None and x.grad.data is not None
np.testing.assert_allclose(x.grad.data, 2.0 * np.array([[1.0, 2.0], [3.0, 4.0]]))
print(f"중간 no-op 후 grad = 2x 정상 (w.creator = {type(w.creator).__name__})")
print("→ 그래프에 항등 노드가 쌓이지 않는다 (dezero 관례 — 변형 포인트 2)")


# ===== 데모 4 — 메서드 스타일 (NumPy 관습 — VariableShapeMixin) ================
print()
print("=== 데모 4: x.reshape(6) / x.T — NumPy 관습 메서드 ===")

x = Variable(np.array([[0, 1, 2], [3, 4, 5]]))

y1 = x.reshape(6)      # 가변 int 인자
y2 = x.reshape((6,))   # 단일 튜플 인자 — 둘 다 허용
y3 = x.T               # 전치 프로퍼티

assert y1.data is not None and y2.data is not None and y3.data is not None
print(f"x.reshape(6).shape  = {y1.data.shape}")   # (6,)
print(f"x.reshape((6,)).shape = {y2.data.shape}") # (6,)
print(f"x.T.shape = {y3.data.shape}")             # (3,2)

assert y1.data.shape == (6,) and y2.data.shape == (6,) and y3.data.shape == (3, 2)
print("→ F.reshape/F.transpose와 x.reshape/x.T — 두 스타일이 같은 그래프를 만든다")


# ===== 데모 5 — 값 불변 → 미분 불변 (gradient check) ===========================
print()
print("=== 데모 5: reshape은 함수값/미분값을 안 바꾼다 — gradient check ===")

data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
x = Variable(data.copy())


def f(t: Variable) -> Variable:
    """reshape을 낀 Σx² — 수학적으로는 sum(square(t))과 동일한 함수."""
    return sum(square(reshape(t, (6,))))


y = f(x)
fill_grad(y)

assert x.grad is not None and x.grad.data is not None
np.testing.assert_allclose(x.grad.data, 2.0 * data)   # grad = 2x (reshape 무영향)

# 수치 미분 대조 — 전 원소 동시 ±eps → 원소별 미분계수의 총합과 비교 (test_sum 관례)
numerical = numerical_diff(f, x)
print(f"역전파 grad 총합 = {x.grad.data.sum():.6f}")
print(f"수치 미분 총합    = {float(numerical):.6f}")
assert np.isclose(x.grad.data.sum(), numerical)
print("→ gradient check 통과 — reshape은 그래프에 노드를 남겨도 값 세계엔 투명")


# ===== 데모 6 — 2계 미분 (⑤형 backward의 계약: 모듈 함수 호출) =================
print()
print("=== 데모 6: 2계 미분 — backward가 모듈 reshape()을 쓰는 이유 ===")

data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
x = Variable(data.copy())
y = sum(square(reshape(x, (6,))))

fill_grad(y, create_graph=True)   # 역전파가 2층 그래프를 남긴다

gx = x.grad
assert gx is not None and gx.creator is not None and gx.data is not None
print(f"gx = x.grad → {gx.data} (shape {gx.data.shape}) — '2x'라는 식")

# ★ fill_grad 누적 함정 (1차 역전파가 실제로 밟음): x.grad가 이미 2x로 차 있는
# 상태에서 fill_grad(gx)를 돌리면 누적(step14 방식)이 일어나 2x + 2가 된다
# (실제로 4,6,8,... 나와서 캐치). gx를 캡처한 뒤 clear_grad — 이슈 43 D1
# (fill_grad 누적 토론, step45 언저리 회수 예정)의 실사례.
x.clear_grad()
fill_grad(gx)   # 2차 미분: d²(Σx²)/dx² = 2

assert x.grad is not None and x.grad.data is not None
np.testing.assert_allclose(x.grad.data, 2.0 * np.ones((2, 3)))
print(f"d²y/dx² = {x.grad.data} — 2로 정착")
print("→ Reshape.backward가 raw np.reshape 대신 모듈 reshape()을 호출하므로")
print("  2층 그래프가 끊기지 않고 재미분이 흐른다 (⑤형의 구현 계약)")


# ===== 데모 7 — view 메모리 공유 관찰 (NumPy 경고 문서화) ======================
print()
print("=== 데모 7: view 경고 — reshape은 메모리를 공유할 수 있다 ===")

x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
y = reshape(x, (6,))

assert x.data is not None and y.data is not None
shared = np.shares_memory(x.data, y.data)
print(f"np.shares_memory(x.data, y.data) = {shared}")   # True (연속 배열 → view)

assert shared
print("→ 연속 배열의 reshape은 view: x.data와 y.data가 같은 버퍼를 본다.")
print("  rezero 전제(data 불변 사용)에서는 안전 — in-place 등장 시 함경 지점")
print("  (Reshape 클래스 docstring + test_reshape_transpose.py canary로 기록)")


print()
print("step38 데모 전부 통과 ✅  (reshape/transpose — 형상 변환 함수)")
