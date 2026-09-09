"""
rezero.steps.step37 — [4고지] 텐서를 다루다
=====================================================================

★ 책 공식 제목 "텐서를 다루다". 제 4고지 "신경망 만들기" (step37~51) 개막 스텝.

★★★ 이 step의 성격 — "선언"의 스텝 (새 코드가 거의 없음):

    1~3고지: NumPy 배열을 쓰긴 했지만 '병렬 계산' 용도가 일부일 뿐,
    배열 자체를 배열로서 인식하고 설명한 부분은 없었다 (브로 책 리딩 노트).
    37단계부터 "이제부터 텐서(다차원 배열)를 본격적으로 다룬다"는 선언.

    기존 구현(Add/Mul/Pow/Sin/...)은 전부 element-wise → 다차원 ndarray가
    **수정 0으로** 순전파·역전파 모두 통과. 프레임워크가 이미 텐서를 품고
    있었음을 확인하는 자리 — v2 → v3 브랜칭도 구조 변경 없이 계승.

★ 책 '보충' 절 (수학 — 브로 리딩 노트):
    - 역전파 시 실제로 야코비안 행렬 계산 없이 역전파가 가능한 상황 설명
    - element-wise 연산의 역전파가 단순하다는 이야기
    → "야코비안은 결코 만들어지지 않는다 — 흐르는 건 언제나 gradient(VJP)"
      (RESEARCH_QUEUE 후보 10번, 이슈 43 작업 1에서 회수 완료)와 직결.

★ 정답지 페이스 참고 (브로 지적 — "DeZero 스텝바이스텝 추가가 슬슬 대충"):
    정답지 steps/step37.py는 F.sum을 쓰지만 책 본문은 sum의 구현을 설명하지
    않음 — dezero 패키지에 미리 들어있는 것을 꺼내 쓰기만 한다.
    sum_to / broadcast_to, axis/keepdims는 뒷 스텝에서 상세화.
    rezero 페이스: 데모 동작에 필요한 최소 Sum(전체 합만)을 v3에 포함.

★★ Sum의 역전파 — 이번 스텝의 유일한 신규 코드가 보여주는 것:

    순전파:  y = x.sum()            (2,3) 텐서 → 0-dim (축소)
    역전파:  ∂y/∂x_i = 1 (모든 원소) → grad = ones — 문제는 "0-dim upstream을
    어떻게 (2,3) shape로 복원하나"

    rezero는 derivative hook 유지: 도함수 np.ones_like(x.data) 반환 (Abs가
    확립한 '값 참조 ndarray' 관례의 shape판) → backward 뼈대의
    local_deriv * upstream이 **곱셈 브로드캐스팅으로 자동 shape 복원**.
    ★ "브로드캐스팅 = 미분의 shape 복원 장치".
    (dezero는 backward 직접 오버라이드 + np.broadcast_to — rezero는 hook 유지)

★★★ 개발 중 발견한 버그 (v3 창설 직후, 스모크 테스트에서 포착):

    도함수가 **다차원 ndarray**를 반환하면 NumPy가 element-wise를 이겨버려
    object 배열(원소가 Variable)이 만들어져 grad가 오염됨.
    탐구 25의 "__array_priority__ 없이도 __rmul__로 충분"은 **스칼라(0-dim)
    기준**이었다 — (2,3) 배열 * Variable은 NumPy 승리.
    해결: backward 뼈대가 local_deriv를 as_variable로 정규화 (리프 Variable화).
    "값 참조 → 곱해지면 리프 Variable이 된다"는 기존 계약(이슈 45)을 뼈대가
    이행. 3고지의 Abs(np.sign)는 0-dim만 반환해서 이 지뢰를 안 밟았음.

실행: uv run python rezero/steps/step37.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v3 import Variable, fill_grad, numerical_diff, sin, sum


# ===== 데모 1 — 정답지 steps/step37.py 재현 ===================================
print("=== 데모 1: 정답지 재현 — t = x + c → y = sum(t) → retain_grad ===")

x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
c = Variable(np.array([[10, 20, 30], [40, 50, 60]]))
t = x + c
y = sum(t)

fill_grad(y, retain_grad=True)   # 중간 grad도 유지 — 텐서 grad를 눈으로 본다

assert y.grad is not None and y.grad.data is not None
assert t.grad is not None and t.grad.data is not None
assert x.grad is not None and x.grad.data is not None
assert c.grad is not None and c.grad.data is not None

print(f"y.grad = {y.grad.data}          (0-dim — sum 출력)")
print(f"t.grad =\n{t.grad.data}")
print(f"x.grad =\n{x.grad.data}")
print(f"c.grad =\n{c.grad.data}")

np.testing.assert_array_equal(y.grad.data, np.array(1.0))
np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))
np.testing.assert_array_equal(c.grad.data, np.ones((2, 3)))
print("→ Add(텐서+텐서)의 grad = ones: element-wise라 3고지 구조 그대로 통과.")


# ===== 데모 2 — 수정 0 확인: 기존 element-wise 연산의 텐서 통과 ================
print()
print("=== 데모 2: v2 유산 연산이 텐서에서 무수정 동작 (이 step의 본질) ===")

xt_data = np.array([[1.0, 2.0], [3.0, 4.0]])
xt = Variable(xt_data)

# x² — Pow의 derivative hook (c·x^(c-1))이 텐서에서 그대로
yt = xt ** 2
fill_grad(yt)
grad_sq = xt.grad
assert grad_sq is not None and grad_sq.data is not None
print(f"x²     grad =\n{grad_sq.data}   (기대: 2x)")
np.testing.assert_allclose(grad_sq.data, 2 * xt_data)

# sin — 수학 함수도 element-wise라 무수정 통과
xt.clear_grad()
yst = sin(xt)
fill_grad(yst)
grad_sin = xt.grad
assert grad_sin is not None and grad_sin.data is not None
print(f"sin(x) grad =\n{np.round(grad_sin.data, 4)}   (기대: cos(x))")
np.testing.assert_allclose(grad_sin.data, np.cos(xt_data), atol=1e-7)

print("→ 3고지에서 짜둔 구조가 텐서를 이미 품고 있었다 — '선언'의 스텝.")


# ===== 데모 3 — sum의 역전파: 브로드캐스팅 shape 복원 ==========================
print()
print("=== 데모 3: sum(x·x) — 0-dim upstream이 브로드캐스팅으로 shape 복원 ===")

xs_data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
xs = Variable(xs_data)
ys = sum(xs * xs)
fill_grad(ys, retain_grad=True)

grad_sum = xs.grad
assert grad_sum is not None and grad_sum.data is not None
print(f"y = sum(x·x) = {ys.data}   (1+4+9+16+25+36)")
print(f"x.grad =\n{grad_sum.data}")
print("   (기대: 2x — Sum의 ones(2,3) * upstream이 곱셈 브로드캐스팅으로 복원)")
np.testing.assert_allclose(grad_sum.data, 2 * xs_data)

# gradient check — 수치 미분과 교차 검증
# numerical_diff는 모든 원소를 동시에 ±eps 흔든다 → 결과는 원소별
# 미분계수의 총합. 역전파 grad의 총합(sum(2x))과 비교.


def f_sum_sq(v: Variable) -> Variable:
    return sum(v * v)


numeric_total = numerical_diff(f_sum_sq, xs)
analytic_total = float(grad_sum.data.sum())
print(f"gradient check: 역전파 총합 = {analytic_total:.6f} / 수치 미분 = {float(numeric_total):.6f}")
assert np.isclose(analytic_total, numeric_total, rtol=1e-5)
print("→ 일치 — Sum의 hook 방식 역전파가 수치 미분과 교차 검증됨.")


# ===== 데모 4 — dezero 정답지 대조 =============================================
print()
print("=== 데모 4: dezero 정답지 대조 ===")

import dezero.functions as DF   # noqa: E402
from dezero import Variable as DeZeroVariable   # noqa: E402

dx = DeZeroVariable(np.array([[1, 2, 3], [4, 5, 6]]))
dc = DeZeroVariable(np.array([[10, 20, 30], [40, 50, 60]]))
dt = dx + dc  # type: ignore[operator]  # dezero 클래스 밖 대입 한계 (항목 031)
dy = DF.sum(dt)  # type: ignore[union-attr]  # dezero __call__ 반환 추론 한계 (원본)
dy.backward(retain_grad=True)  # type: ignore[union-attr]

assert dx.grad is not None and dx.grad.data is not None
np.testing.assert_array_equal(dx.grad.data, x.grad.data)
print(f"dezero x.grad =\n{dx.grad.data}")
print("→ rezero와 완전 일치 — hook 유지 구현이 정답지와 같은 grad를 낳는다.")


# ===== 마무리 — 4고지 개막 =====================================================
print()
print("★★★ 제 4고지 (step37~51, 신경망 만들기) 개막! ★★★")
print("  이번 스텝: 텐서 1급 시민 선언 + Sum (도함수 ones — 값 참조 shape판)")
print("  v3 창설: v2 계승 + backward 뼈대 as_variable 정규화 (NumPy 우선 버그 수정)")
print("  다음: step38 — 정답지는 reshape/transpose (형상 변환 계열)")
