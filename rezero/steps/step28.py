"""
rezero.steps.step28 — [3고지] 함수 최적화
=============================================

★ 책 공식 제목 "함수 최적화". 3고지 4번째 step.
★ v1 패키지 반영 없음 — 기존 기능(clear_grad, fill_grad, 연산자)만으로
  구현하는 응용 step (step24 벤치마크와 같은 성격).

★★★ 이 step의 심장 — "미분 기계가 처음으로 '일'을 한다":

  step01~27: 미분을 위한 인프라 구축 (상자 → 역전파 자동화 → 연산자 → Sin)
  step28:    그 인프라로 실제 문제를 푼다 — "함수를 최소화하는 점을 찾아라"

  4단계 갱신 루프가 신경망 학습의 원형:
    ① y = rosenbrock(x0, x1)     순전파 — 이 시점에 그래프 새로 구축 (Define-by-Run)
    ② x.clear_grad()             grad 초기화 — 누적 방지 (step14 설계의 역할)
    ③ fill_grad(y)               역전파 — gradient 획득
    ④ x.data -= lr * x.grad      파라미터 갱신 — 그래프 밖 in-place 업데이트

  → PyTorch의 zero_grad() → backward() → step() 삼단 콤보의 조상.

★ 경사하강법 은유 — 안개 낀 산에서 눈앞 경사만 보고 내려가기.
  gradient = 가장 가파른 오르막 → -lr * grad = 내리막으로 발걸이.
  lr 트레이드오프: 크면 골짜기 건너편으로 튕겨 발산, 작으면 영영 느림.

★ Rosenbrock ("바나나 함수"):
  y = 100(x1 - x0²)² + (x0 - 1)²
  전역 최소 (1, 1)에서 y=0. 등고선이 바나나 모양 골짜기 —
  골짜기가 굽어있어 경사하강법이 느리게 수렴 (비볼록 벤치마크 클래식).

★ rezero 변형 포인트 (정답지 대비):
  - cleargrad() → clear_grad() (항목 021 snake_case 일관성)
  - y.backward() → fill_grad(y) (rezero 정체성)
  - is_simple_core 분기 없음 (rezero는 core 하나)

참고 자료:
  - 원본 구현: steps/step28.py (정답지 — 인접 step27/29 비교 완료)
  - 이슈: 35번 (step28 진행 추적)

실행:
  uv run python rezero/steps/step28.py
"""

if '__file__' in globals():
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v1 import Variable, fill_grad


# ===== Rosenbrock 함수 (step 한정 벤치마크 — v1 승격 안 함) =====================
# "바나나 함수". 전역 최소 (1, 1)에서 y = 0.
# 골짜기가 x0=1을 축으로 굽어있어, 경사하강법이 골짜기를 따라 미끄러지듯
# 천천히 내려감 — 볼록하지만 조건수가 나쁜 최적화 벤치마크의 클래식.
def rosenbrock(x0: Variable, x1: Variable) -> Variable:
    """Rosenbrock: y = 100(x1 - x0²)² + (x0 - 1)². 최소 (1, 1) → y=0."""
    y = 100 * (x1 - x0 ** 2) ** 2 + (x0 - 1) ** 2
    return y


def gd_step(x: Variable, lr: float) -> None:
    """경사하강 갱신 한 걸음 (4단계 루프의 ④): x.data -= lr * x.grad.

    헬퍼로 뺀 이유: (a) grad/data Optional 가드 집중 (pyright) (b) 갱신 공식
    복붙 버그 방지 — [4]에서 x1을 x0.grad로 갱신하는 복붙 버그를 재실행 검증으로
    발견한 뒤 도입.
    """
    assert x.grad is not None, "fill_grad 이후에 호출할 것"
    assert x.data is not None, "data는 항상 존재해야 함"
    x.data -= lr * x.grad


def _val(x: Variable) -> float:
    """데모 출력용 — data를 float로 회수 (None 가드 포함, pyright 대응)."""
    assert x.data is not None
    return float(x.data)


# --- 데모: 경사하강법으로 Rosenbrock 최소화 -------------------------------------
if __name__ == "__main__":
    print("=== step28 함수 최적화 — 경사하강법 (Rosenbrock) ===")
    print()

    # --- [1] 기본 갱신 루프 — (0, 2)에서 (1, 1)을 향해 ---
    print("[1] 경사하강법 기본 — lr=0.001, 1000 iters")
    x0 = Variable(np.array(0.0))
    x1 = Variable(np.array(2.0))
    lr = 0.001
    iters = 1000

    for i in range(iters):
        y = rosenbrock(x0, x1)        # ① 순전파 — 그래프 새로 구축

        x0.clear_grad()               # ② grad 초기화 (누적 방지)
        x1.clear_grad()

        fill_grad(y)                  # ③ 역전파

        gd_step(x0, lr)               # ④ 갱신 — x.data -= lr * x.grad
        gd_step(x1, lr)

        # 궤적은 100 iter마다만 (정답지는 매번 print — 압축)
        # 골짜기 바닥 편차 x1 - x0²: 0에 가까우면 골짜기 바닥(포물선 x1 = x0²)에 붙어 있는 것
        if i % 100 == 0 or i == iters - 1:
            valley_gap = _val(x1) - _val(x0) ** 2
            print(f"    iter {i:4d}: x0 = {_val(x0):.6f}, x1 = {_val(x1):.6f}, y = {_val(y):.6f}"
                  f" | 골짜기 편차 x1-x0² = {valley_gap:+.6f}")

    print(f"    ★ (0, 2) → ({_val(x0):.4f}, {_val(x1):.4f}) — 최소점 (1, 1)을 향해")
    print(f"    ★ 궤적 해설: 초반 x1 급강하 = 골짜기 바닥으로 낙하,")
    print(f"      이후 편차 ≈ 0 유지 = 바닥(포물선 x1 = x0²)을 따라 기어가는 단계")
    print(f"    ★ Rosenbrock은 골짜기가 굽어서 천천히 수렴 (바나나 계곡)")
    print()

    # --- [2] 학습률 트레이드오프 — lr 크면 발산 ---
    # 발산 시 overflow RuntimeWarning이 뜨는데, "발산 관찰"이 목적이라 억제하고 결과만.
    print("[2] 학습률 트레이드오프 — lr이 크면?")
    with np.errstate(over='ignore', invalid='ignore'):
        for lr_test in [0.001, 0.01, 0.1]:
            x0 = Variable(np.array(0.0))
            x1 = Variable(np.array(2.0))

            for _ in range(100):          # 100 iters만 (경향 관찰용)
                y = rosenbrock(x0, x1)
                x0.clear_grad()
                x1.clear_grad()
                fill_grad(y)
                gd_step(x0, lr_test)
                gd_step(x1, lr_test)

            y_check = _val(rosenbrock(x0, x1))
            status = "발산!" if (np.isnan(y_check) or np.isinf(y_check) or y_check > 1e10) else "진행"
            print(f"    lr = {lr_test:<6}: x0 = {_val(x0):>+12.4f}, x1 = {_val(x1):>+12.4f}, y = {y_check:>+.4e}  [{status}]")
    print(f"    ★ lr=0.01부터 발산 — 발걸이가 커서 골짜기 건너편으로 튕기는 오버슈트 반복")
    print(f"      (Rosenbrock은 100 계수 탓에 gradient가 커서 발산 문턱이 낮음)")
    print()

    # --- [3] clear_grad 누락 실험 — grad 누적의 오염 ---
    print("[3] clear_grad 누락 실험 — 100 iters 후 비교")
    with np.errstate(over='ignore', invalid='ignore'):
        for use_clear in [True, False]:
            x0 = Variable(np.array(0.0))
            x1 = Variable(np.array(2.0))

            for _ in range(100):
                y = rosenbrock(x0, x1)

                if use_clear:            # ★ 누락 실험 — 이 초기화를 빼면?
                    x0.clear_grad()
                    x1.clear_grad()

                fill_grad(y)
                gd_step(x0, 0.001)
                gd_step(x1, 0.001)

            label = "clear_grad O" if use_clear else "clear_grad X"
            print(f"    {label}: x0 = {_val(x0):+.6f}, x1 = {_val(x1):+.6f}")

    print(f"    ★ 누락 시 nan — grad가 iteration마다 누적돼 갱신량 폭증 → 발산")
    print(f"    ★ grad 누적 설계(step14)는 '같은 그래프 안 합산'용 —")
    print(f"      갱신 루프처럼 '매번 새 그래프'에선 초기화 필수 (PyTorch zero_grad의 원형)")
    print()

    # --- [4] 볼록 vs 비볼록 — 최소점까지 거리로 수렴 속도 비교 ---
    print("[4] sphere 대비 — 볼록하면 빠르다 (양쪽 다 1000 iters, lr=0.001)")

    def sphere2(x0, x1):
        return x0 ** 2 + x1 ** 2

    for name, func, start, target in [
        ("sphere    ", sphere2, (5.0, 5.0), (0.0, 0.0)),
        ("rosenbrock", rosenbrock, (0.0, 2.0), (1.0, 1.0)),
    ]:
        x0 = Variable(np.array(start[0]))
        x1 = Variable(np.array(start[1]))

        for _ in range(1000):
            y = func(x0, x1)
            x0.clear_grad()
            x1.clear_grad()
            fill_grad(y)
            gd_step(x0, 0.001)
            gd_step(x1, 0.001)

        dist_init = np.hypot(start[0] - target[0], start[1] - target[1])
        dist_now = np.hypot(_val(x0) - target[0], _val(x1) - target[1])
        print(f"    {name}: ({start[0]:+.1f}, {start[1]:+.1f}) → ({_val(x0):+.4f}, {_val(x1):+.4f})"
              f" | 최소점까지 거리 {dist_init:.3f} → {dist_now:.3f} ({dist_now/dist_init:.1%} 남음)")

    print(f"    ★ sphere는 남은 거리 13% — 그릇이라 지수적으로 수렴")
    print(f"    ★ rosenbrock은 44% — 굽은 골짜기라 미끄러지듯 느리게 (최적화 난이도의 차이)")
    print()

    print("=== step28 완료 — 미분 기계가 처음으로 '일'을 했다 ===")
    print("    4단계 루프 = 신경망 학습의 원형 (zero_grad → backward → step) 🎉")
