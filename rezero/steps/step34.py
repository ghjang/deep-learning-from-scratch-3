"""
rezero.steps.step34 — [3고지] sin 함수 고차 미분
=====================================================================

★ 책 공식 제목 "sin 함수 고차 미분". sin을 3번 미분해 y/y'/y''/y''' 곡선으로
**미분 순환**(sin→cos→-sin→-cos)을 실증하는 능력 시연 스텝.

★★★ 이 step의 실험 — 두 버전 대조 (브로 제안):

  [A] 벡터 버전 (정답지 방식)     [B] 루프 버전 (무식하게 포인트별)
  ─────────────────────────────    ─────────────────────────────────
  x = linspace(200) 하나의          각 점 x_i마다 스칼라 Variable을
  Variable — NumPy가 element-wise   만들어 3계 미분, 결과를 모아서
  로 통째로 계산                    배열에 저장 (200회 반복)

  데이터축 처리: NumPy에 위임       데이터축 처리: 사람이 직접 순회
  v2 전제 4 (스칼라): 위반 ✗        v2 전제 4 (스칼라): 완전 준수 ✅

  → 둘의 결과가 일치하면? "벡터화는 편리함이지 수학적 필연이 아니다" 실증.
    element-wise 함수는 각 원소가 수학적으로 독립이라 루프로 쪼개도 같은 답.

★ 벡터 버전이 (전제 위반인데) 동작하는 이유 — 조건부 필연:
    벡터 y의 미분은 원래 야코비안(VJP)이 흐르지만, element-wise 함수의
    야코비안은 **대각행렬** → 대각행렬 × 벡터 = 대각원소 ⊙ 벡터 = element-wise 곱
    → 우리 derivative hook 공식 df(x) * upstream과 정확히 일치.
    "스칼라 전제"는 보수적 문서화였지 코드 강제가 아니었다는 것의 실증.

★ 두 축의 구분 (브로 통찰 — RESEARCH_QUEUE 후보 8/9번):
    함수 인자축 (f(x0,x1) 다변수 — step11~13 명시 구현) vs
    데이터축 (data가 스칼라냐 벡터냐 — NumPy에 위임).
    버전 A는 두 축이 겹쳐 보이고, 버전 B는 물리적으로 분리된다.

실행: uv run python rezero/steps/step34.py  → output/sin_higher_deriv.png
"""

import os
import sys
import time

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import matplotlib

matplotlib.use('Agg')  # 터미널 환경 — 화면 표시 없이 파일로 저장
import matplotlib.pyplot as plt
import numpy as np

from rezero.v2 import Variable, fill_grad, sin


# ===== [A] 벡터 버전 — 정답지 방식 (NumPy element-wise 위임) ==================
def run_vector_version(n: int = 200) -> list[np.ndarray]:
    """x를 (n,) 벡터 하나로 — v2 전제 4 위반이지만 대각 야코비안으로 동작 예측."""
    x = Variable(np.linspace(-7, 7, n))
    y = sin(x)
    fill_grad(y, create_graph=True)

    assert y.data is not None and x.grad is not None and x.grad.data is not None
    logs = [y.data.copy()]           # y = sin(x)
    for _ in range(3):
        logs.append(x.grad.data.copy())   # y', y'', y'''
        gx = x.grad
        x.clear_grad()
        fill_grad(gx, create_graph=True)

    return logs


# ===== [B] 루프 버전 — 포인트별 스칼라 계산 (전제 완전 준수) ====================
def run_loop_version(n: int = 200) -> list[np.ndarray]:
    """각 점마다 스칼라 Variable로 3계 미분 — 데이터축을 사람이 직접 순회.

    element-wise 함수는 각 원소가 수학적으로 독립이라, 포인트별로 쪼개도
    벡터 버전과 같은 답이 나와야 한다 (이것이 이 실험의 검증 대상).
    """
    xs = np.linspace(-7, 7, n)
    logs = [np.zeros(n) for _ in range(4)]   # y, y', y'', y'''

    for i, xv in enumerate(xs):
        x = Variable(np.array(float(xv)))    # 스칼라 Variable — 전제 준수
        y = sin(x)
        fill_grad(y, create_graph=True)

        assert y.data is not None and x.grad is not None and x.grad.data is not None
        logs[0][i] = float(y.data)
        for k in range(3):
            logs[k + 1][i] = float(x.grad.data)
            gx = x.grad
            x.clear_grad()
            fill_grad(gx, create_graph=True)

    return logs


# ===== 실험 실행 + 3자 대조 =====================================================
print("=== [A] 벡터 버전 — NumPy element-wise (전제 4 위반, 동작 예측) ===")
t0 = time.perf_counter()
logs_a = run_vector_version()
ta = time.perf_counter() - t0
print(f"실행: {ta:.3f}s — x 하나(벡터 200)로 3계 미분 완료")

print()
print("=== [B] 루프 버전 — 포인트별 스칼라 계산 (전제 4 완전 준수) ===")
t0 = time.perf_counter()
logs_b = run_loop_version()
tb = time.perf_counter() - t0
print(f"실행: {tb:.3f}s — 스칼라 Variable 200개 각각 3계 미분")

# 수학적 기대값 (y=sin, y'=cos, y''=-sin, y'''=-cos)
xs = np.linspace(-7, 7, 200)
expected = [np.sin(xs), np.cos(xs), -np.sin(xs), -np.cos(xs)]
labels = ["y=sin(x)", "y'", "y''", "y'''"]

print()
print("=== 3자 대조 (A 벡터 / B 루프 / 수학 기대값) ===")
for k in range(4):
    a_ok = np.allclose(logs_a[k], expected[k])
    b_ok = np.allclose(logs_b[k], expected[k])
    ab_ok = np.allclose(logs_a[k], logs_b[k])
    print(f"{labels[k]:12s}  A=수학 {a_ok}  B=수학 {b_ok}  A=B {ab_ok}")
    assert a_ok and b_ok and ab_ok, f"{labels[k]} 불일치!"

print()
print("→ 세 상자 전부 일치 — 벡터화는 편리함이지 수학적 필연이 아니다.")
print("  element-wise 함수의 각 원소는 수학적으로 독립 (대각 야코비안의 의미).")
print(f"→ 속도: 벡터 {ta:.3f}s vs 루프 {tb:.3f}s — NumPy의 C 루프가 Python 루프를 대신")


# ===== 그래프 저장 — 미분 순환 시각화 ==========================================
fig, ax = plt.subplots(figsize=(10, 6))
for k in range(4):
    ax.plot(xs, logs_a[k], label=labels[k])

ax.set_title('Higher-order derivatives of sin(x) — sin → cos → -sin → -cos (cycle)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)

out_path = 'output/sin_higher_deriv.png'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
fig.savefig(out_path, dpi=120, bbox_inches='tight')
print()
print(f"그래프 저장: {out_path}")
print("→ 곡선 4개가 각각 90도씩 phase shift — 미분할 때마다 cos 쪽으로 회전하는 순환.")

print()
print("★ step34 완료 — v2가 벡터도(억지로) 삼킨다: 대각 야코비안의 조건부 필연.")
print("  다음: step35 (tanh 고차 미분 + 계산 그래프 시각화 — 후보 8번 회수 예정)")
