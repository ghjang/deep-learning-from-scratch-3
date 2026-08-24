"""
rezero.steps.step36 — [3고지] 고차 미분 이외의 용도
=====================================================================

★ 책 공식 제목 "고차 미분 이외의 용도". 3고지(고차 미분 계산)의 마무리 스텝.

★★★ 이 step의 심장 — 살아있는 그래프의 재사용:

    고차 미분 (step33~35): gx를 **다시 미분**        → f'', f''' ...
    이외의 용도 (이번):    gx를 **다른 식에 조립**    → z = gx³ + y

    gx는 "2x라는 식" (그래프 소유 Variable) — 이를 세제곱하고 원래 출력 y에 더해
    **완전히 새로운 함수 z**를 만들 수 있다. chain rule이 d(gx³)/dx = 3·gx²·(dgx/dx)를
    자동으로 타고 내려감 — 미분 '결과'가 아니라 미분 '과정'을 재료로 쓰는 것.
    "미분 결과도 계산의 일등 시민" (Define-by-Run의 완성형).

검산:
    x = 2, y = x², gx = 2x
    z = (2x)³ + x² = 8x³ + x²
    z' = 24x² + 2x  →  z'(2) = 96 + 4 = 100

실무 연결 (탐구 노트 30 실무 좌표의 2차 사용례):
    - gradient penalty (WGAN-GP): gradient의 norm을 loss에 추가
    - 메타러닝 ("learning to learn by gradient descent"): gradient를 입력으로
      받는 옵티마이저 학습 — 모두 "gx를 새 계산에 조립"하는 이 패턴.

실행: uv run python rezero/steps/step36.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v2 import Variable, fill_grad


# ===== 데모 1 — 살아있는 그래프 재사용: z = gx³ + y ============================
print("=== 데모 1: z = gx³ + y — 미분 식과 원래 출력을 새 계산의 재료로 ===")

x = Variable(np.array(2.0))
y = x ** 2
fill_grad(y, create_graph=True)   # 역전파가 그래프를 남기며 (gx가 "식"이 된다)

gx = x.grad                        # gx = 2x — 그래프 소유한 채
assert gx is not None and gx.data is not None
print(f"y  = x²     → y(2)  = {y.data}")
print(f"gx = 2x     → gx(2) = {gx.data}   (살아있는 식)")

x.clear_grad()

z = gx ** 3 + y                    # ★ 재사용 — 미분 식 + 원래 출력을 조립
print(f"z  = gx³+y  → z(2)  = {z.data}   (= 4³ + 4)")

fill_grad(z)                       # z' = 3·(2x)²·2 + 2x = 24x² + 2x
assert x.grad is not None and x.grad.data is not None
print(f"z' = 24x²+2x → z'(2) = {x.grad.data}")
assert x.grad.data == np.array(100.0)

print("→ 100! chain rule이 gx³의 내부(dgx/dx=2)까지 자동으로 타고 내려갔다.")
print("  미분 '결과'가 아니라 미분 '과정'을 재료로 쓴 것 — 살아있는 그래프.")


# ===== 데모 2 — dezero 정답지 대조 =============================================
print()
print("=== 데모 2: dezero 정답지 대조 ===")

from dezero import Variable as DeZeroVariable   # noqa: E402

dx = DeZeroVariable(np.array(2.0))
dy = dx ** 2  # type: ignore[operator]  # dezero __pow__ 밖 대입 한계 (항목 031)
dy.backward(create_graph=True)
dgx = dx.grad
assert dgx is not None

dx.cleargrad()
dz = dgx ** 3 + dy  # type: ignore[operator]
dz.backward()
assert dx.grad is not None and dx.grad.data is not None
print(f"dezero z'(2) = {dx.grad}   rezero z'(2) = {x.grad.data}")
assert float(dx.grad.data) == float(x.grad.data) == 100.0
print("→ 완전 일치 — rezero의 살아있는 그래프가 정답지와 같은 길.")


# ===== 마무리 — 3고지 완료 =====================================================
print()
print("★★★ 3고지 (step25~36, 고차 미분 계산) 완료! ★★★")
print("  시각화(25/26) → 최적화(27~29) → 3부작(30 준비/31 이론/32 구현)")
print("  → 수확(33 뉴턴 자동) → 시연(34 sin 순환/35 tanh 폭증) → 용도 확장(36)")
print("  다음: 제 4고지 (step37~51, 신경망 만들기) — 진입 전 후보 10번(야코비안) 회수 예정!")
