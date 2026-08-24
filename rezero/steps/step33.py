"""
rezero.steps.step33 — [3고지] 뉴턴 방법으로 푸는 최적화(자동 계산)
=====================================================================

★ 책 공식 제목 "뉴턴 방법으로 푸는 최적화(자동 계산)". step29(수동 계산)의 쌍둥이.

★★★ 이 step의 심장 — "3줄 차이의 혁명":

  step29 (수동)                          step33 (자동)
  ------------------------------------   ------------------------------------
  y = f(x); x.cleargrad()                y = f(x); x.clear_grad()
  y.backward()                           fill_grad(y, create_graph=True)  ← ①
                                         gx = x.grad                      ← ② f'가 Variable(식)
                                         x.clear_grad()
                                         fill_grad(gx)                    ← ③ f'' 자동!
  gx2 = gx2(x.data)   # f'' 손유도 함수   gx2 = x.grad.data
  x.data -= gx.data / gx2                x.data -= gx.data / gx2

  사라진 건 단 하나 — 손으로 유도해 들고 다녀야 했던 gx2 함수.
  f(x) = x⁴ − 2x²도 같고, 갱신식도 같고, 루프도 같다.

복선 회수 3부작 완결:
  step29 "수동 한계 발견" (탐구 노트 29)
    → step31 이론 (double backprop — 탐구 노트 30)
    → step32 구현 (v2 탄생 — grad의 Variable화)
    → step33 수확 ← 지금 여기. v2의 첫 배당.

수학:
  f(x)  = x⁴ − 2x²
  f'(x) = 4x³ − 4x          → f' = 0의 근: x = 0 (국소 최대 함정), x = ±1 (최소)
  f''(x) = 12x² − 4
  뉴턴 갱신: x ← x − f'/f'' — x₀ = 2에서 출발하면 1로 2차 수렴 (오차 제곱).

실행: uv run python rezero/steps/step33.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v2 import Variable, fill_grad


def f(x: Variable) -> Variable:
    """테스트 함수 — step29와 동일."""
    return x ** 4 - 2 * x ** 2


# ===== 뉴턴 방법 — 자동 계산 (f''를 프레임워크가 알아서) =======================
print("=== 뉴턴 방법 (자동 계산) — f(x) = x⁴ − 2x², x₀ = 2 ===")
print("기대: 최소점 x = 1 로 2차 수렴 (오차 제곱 — 유효숫자 배가)\n")

x = Variable(np.array(2.0))
iters = 10

for i in range(iters):
    print(i, x)

    y = f(x)
    x.clear_grad()
    fill_grad(y, create_graph=True)   # ★ ① 역전파가 그래프를 남기며 (2층 구축)

    gx = x.grad                        # ★ ② f' — Variable (4x³−4x라는 "식")
    assert gx is not None and gx.data is not None
    x.clear_grad()
    fill_grad(gx)                      # ★ ③ f'' 자동 — gx2 손유도 함수 대체!
    assert x.grad is not None and x.grad.data is not None
    gx2 = x.grad.data                  # f'' = 12x² − 4

    assert x.data is not None          # Pylance Optional 가드 (data는 유지되지만 타입상 Optional)
    x.data -= gx.data / gx2            # 뉴턴 갱신 (step29와 동일 라인)

# 최종 수렴 검증
assert x.data is not None
final = float(x.data)
print(f"\n최종 x = {final!r}")
print(f"기대 최소점 1과의 오차: {abs(final - 1.0):.2e}")
assert abs(final - 1.0) < 1e-10, f"수렴 실패: {final}"

print("→ step29에서 7 iters 기계 정밀도 도달했던 것과 같은 궤적 —")
print("  이번엔 f''를 단 한 줄도 손으로 유도하지 않았다!")


# ===== 정답지(dezero)와 대조 — 같은 루프, 같은 수렴값 ==========================
print()
print("=== dezero 정답지 대조 ===")

from dezero import Variable as DeZeroVariable   # noqa: E402

dx = DeZeroVariable(np.array(2.0))

for _ in range(iters):
    dy = dx ** 4 - 2 * dx ** 2  # type: ignore[operator]  # dezero __pow__ 밖 대입 한계 (항목 031)
    dx.cleargrad()
    dy.backward(create_graph=True)

    dgx = dx.grad
    assert dgx is not None and dgx.data is not None
    dx.cleargrad()
    dgx.backward()
    assert dx.grad is not None
    dgx2 = dx.grad
    assert dgx2.data is not None

    assert dx.data is not None
    dx.data -= dgx.data / dgx2.data

assert dx.data is not None
print(f"dezero 최종 x = {float(dx.data)!r}")
print(f"rezero 최종 x = {final!r}")
assert float(dx.data) == final
print("→ 완전 일치 — rezero v2의 double backprop이 정답지와 같은 길을 걷는다.")

print()
print("★ step33 완료 — v2 첫 수확. 뉴턴 갱신 x ← x − f'/f''의 세 성분")
print("  (f, f', f'') 중 이제 남은 건 f 하나. 미분은 전부 프레임워크의 일.")
