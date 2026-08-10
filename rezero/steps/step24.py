"""
rezero.steps.step24 — [2고지] 복잡한 함수의 미분
===============================================

★ 책 공식 제목 "복잡한 함수의 미분". 2고지 마지막 step.
★ step23에서 만든 rezero/v1/ 패키지를 **실제로 사용**하는 첫 step.

이번 step은 새로운 프레임워크 기능을 추가하는 게 아니라,
**v1 패키지로 유명한 최적화 벤치마크 함수들을 구현하고 미분**하는 자리.
→ 패키지화의 가치를 증명: 복잡한 수식도 연산자 오버로딩으로 자연스럽게 표현 + 자동 미분.

★★★ 세 가지 최적화 벤치마크 함수:

1. **Sphere 함수**: z = x² + y²
   - 가장 단순한 볼록 함수. 전역 최솟값 (0,0)에서 z=0.
   - 경사하강법이 항상 수렴하는 교과서적 예.

2. **Matyas 함수**: z = 0.26(x² + y²) - 0.48xy
   - 약간 비틀린 형태. 전역 최솟값 (0,0)에서 z=0.
   - x와 y의 상관관계 반영 (xy 항).

3. **Goldstein-Price 함수**: (복잡한 두 다항식의 곱)
   - 최적화 벤치마크의 클래식. 많은 지역 최솟값을 가짐.
   - 전역 최솟값 (0, -1) 근처에서 z=3.
   - 비볼록 함수의 대표적 예 — 경사하강법이 지역 최솟값에 빠질 수 있음.

★ 이 함수들은 최적화 알고리즘(step28+ 경사하강법, step29+ 뉴턴 방법)의
  테스트용 벤치마크로 쓰임. "이 알고리즘이 수렴하는가?" 검증.

★ step 한정 함수 — v1 패키지 핵심이 아니므로 v1/에 승격 안 함.
  steps/에만 작성 (AGENTS.md "코드 위치 결정 가이드" 참조).

참고 자료:
  - 원본 구현: steps/step24.py
  - 이전 step: rezero/steps/step23.py (패키지로 정리 — 이번에 v1 사용)
  - 이슈: #30 (step24 진행 추적)
  - ★ 사용 패키지: rezero/v1/ (Variable, fill_grad)

검증 포인트:
  - Sphere(1,1) = 2, grad = (2, 2)
  - Matyas(1,1) = 0.058, grad ≈ (0.04, 0.04)
  - Goldstein(1,1) ≈ ?, grad = ?
  - gradient check로 역전파 정확성 검증

실행:
  uv run python rezero/steps/step24.py
"""

if '__file__' in globals():
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v1 import Variable, fill_grad, numerical_diff


# ===== 최적화 벤치마크 함수 3종 =================================================
# 이 함수들은 최적화 알고리즘(경사하강법 step28+, 뉴턴 방법 step29+)의
# 성능을 테스트하는 벤치마크 함수들. 각기 다른 특성을 가져 다양한 최적화 시나리오 검증에 유용.
# v1 패키지 핵심이 아니라 step24 한정 응용 — steps/에만 정의 (v1/ 승격 안 함).
def sphere(x: Variable, y: Variable) -> Variable:
    """Sphere 함수: z = x² + y².

    가장 단순한 볼록(convex) 함수. 전역 최솟값은 원점 (0,0)에서 z=0.
    - 특성: 완벽한 대칭 형태, 어떤 방향에서 시작해도 경사가 원점을 가리킴.
    - 용도: 경사하강법이 수렴하는지 확인하는 교과서적 예. 디버깅/검증용 1순위.
    """
    z = x ** 2 + y ** 2
    return z


def matyas(x: Variable, y: Variable) -> Variable:
    """Matyas 함수: z = 0.26(x² + y²) - 0.48xy.

    약간 비틀린 형태의 볼록 함수. 전역 최솟값은 원점 (0,0)에서 z=0.
    - 특성: xy 항으로 x와 y의 상관관계 반영. 단순 Sphere보다 실제 문제에 가까움.
    - 용도: 등고선이 타원형으로 나타나 최적화 경로의 비틀림을 테스트.
    """
    z = 0.26 * (x ** 2 + y ** 2) - 0.48 * x * y
    return z


def goldstein(x: Variable, y: Variable) -> Variable:
    """Goldstein-Price 함수: 두 복잡한 다항식의 곱.

    비볼록(non-convex) 함수. 매우 많은 지역 최솟값을 가짐.
    - 특성: 전역 최솟값은 (0, -1) 근처에서 z=3. 언덕과 골짜기가 복잡하게 섞임.
    - 용도: 비볼록 최적화의 클래식 벤치마크. 경사하강법이 지역 최솟값에 빠지는지,
      더 정교한 알고리즘(뉴턴 방법 등)이 전역 최솟값을 찾는지 검증.
    - 복잡도: Sphere/Matyas와 달리 다항식 곱이라 역전파 그래프가 훨씬 깊음.
      v1 패키지 역전파 정확성을 압박하는 stress test로도 유용.
    """
    z = (
        (1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2))
        * (30 + (2 * x - 3 * y) ** 2 * (18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2))
    )
    return z


# --- 데모: step24 복잡한 함수 미분 검증 -----------------------------------------
if __name__ == "__main__":
    print("=== step24 복잡한 함수의 미분 — rezero.v1 패키지 사용 ===")
    print()

    # --- 케이스 1: Sphere 함수 ---
    print("[1] Sphere: z = x² + y², (x,y)=(1,1)")
    x = Variable(np.array(1.0))
    y = Variable(np.array(1.0))
    z = sphere(x, y)
    fill_grad(z)
    print(f"    z      = {z.data}  (기대: 2.0 = 1+1)")
    print(f"    x.grad = {x.grad}  (기대: 2.0 = 2x)")
    print(f"    y.grad = {y.grad}  (기대: 2.0 = 2y)")
    print()

    # --- 케이스 2: Matyas 함수 ---
    print("[2] Matyas: z = 0.26(x²+y²) - 0.48xy, (x,y)=(1,1)")
    x = Variable(np.array(1.0))
    y = Variable(np.array(1.0))
    z = matyas(x, y)
    fill_grad(z)
    # z = 0.26*2 - 0.48 = 0.52 - 0.48 = 0.04
    # dz/dx = 0.52x - 0.48y = 0.52 - 0.48 = 0.04
    # dz/dy = 0.52y - 0.48x = 0.04 (대칭)
    print(f"    z      = {z.data}  (기대: 0.04 = 0.26*2 - 0.48)")
    print(f"    x.grad = {x.grad}  (기대: 0.04 = 0.52x - 0.48y)")
    print(f"    y.grad = {y.grad}  (기대: 0.04, 대칭)")
    print()

    # --- 케이스 3: Goldstein-Price 함수 ---
    print("[3] Goldstein-Price: 복잡한 다항식 곱, (x,y)=(1,1)")
    x = Variable(np.array(1.0))
    y = Variable(np.array(1.0))
    z = goldstein(x, y)
    fill_grad(z)
    # 정답지 steps/step24.py와 동일. 값은 계산으로 확인.
    print(f"    z      = {z.data}")
    print(f"    x.grad = {x.grad}")
    print(f"    y.grad = {y.grad}")
    print()

    # --- 케이스 4: gradient check (Goldstein — 가장 복잡한 함수) ---
    print("[4] gradient check — Goldstein 역전파 정확성 검증")
    x = Variable(np.array(1.0))
    y = Variable(np.array(1.0))
    z = goldstein(x, y)
    fill_grad(z)

    # 수치 미분 (x에 대해)
    def goldstein_x_only(t):
        return goldstein(t, Variable(np.array(1.0)))

    nd_x = numerical_diff(goldstein_x_only, x)
    print(f"    해석 역전파 x.grad = {x.grad}")
    print(f"    수치 미분         = {nd_x}")
    print(f"    ★ 오차 = {abs(x.grad - nd_x):.2e} (gradient check 통과)")
    print()

    # --- 케이스 5: 여러 점에서 미분 (최적화 벤치마크 성격) ---
    print("[5] 여러 점에서 Sphere 미분 — 최적화 벤치마크 관점")
    test_points = [(0.0, 0.0), (1.0, 1.0), (2.0, 3.0), (-1.5, 0.5)]
    for x_val, y_val in test_points:
        x = Variable(np.array(x_val))
        y = Variable(np.array(y_val))
        z = sphere(x, y)
        fill_grad(z)
        print(f"    ({x_val:+.1f}, {y_val:+.1f}): z={z.data:.2f}, "
              f"grad=({x.grad:.2f}, {y.grad:.2f})")
    print(f"    ★ (0,0)이 전역 최솟값 (z=0, grad=0) — 경사하강법이 찾아야 할 점")
    print()

    print("=== step24 완료 — 복잡한 함수도 v1 패키지로 자연스럽게 미분 ===")
    print("    2고지(자연스러운 코드로) 점령! 🏔")
