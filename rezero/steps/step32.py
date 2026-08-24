"""
rezero.steps.step32 — [3고지] 고차 미분(구현 편)
=====================================================

★ v2 브랜칭 + double backprop 구현 (2026-08-20).

정답지 steps/step32.py는 `# No code` — 구현의 실체는 dezero/core.py의
backward(create_graph) 였고, rezero에서는 **v2 패키지 탄생**으로 답했다:

  rezero/v2/ — v1 (제 1~2고지)을 브랜칭한 고차 미분 지원 패키지
    - Variable.grad: ndarray → Variable (미분 결과가 "값"에서 "식"으로)
    - fill_grad(y, create_graph=True): 역전파가 그래프를 남기며 수행
    - derivative hook: Callable[[ndarray], ndarray] → Callable[[Variable], ...]
    - Cos 신규 추가 (sin의 2차 미분 = -sin 경로용)
    - rezero/common/ 신설 — numerical_diff 이관 (버전 공통 순수 수학)

★ 구조 생존 원칙 (브로-AI 합의):
    apply/derivative hook + fill_grad 전역 함수 + iter_reverse_topo 순회는
    100% 생존. 바뀐 건 "흐르는 데이터의 타입"(ndarray → Variable)과
    using_config('enable_backprop', create_graph) 컨텍스트뿐 —
    기존 설계를 backward 자신에게도 일관되게 적용한 결과 (탐구 노트 30).

실행: uv run python rezero/steps/step32.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v2 import Variable, fill_grad, sin


# ===== 데모 1 — 책의 검증 코드: y = x²의 2차 미분 =============================
# 기대: f'(2) = 4, f''(2) = 2 (d/dx(2x) = 2 — 상수)
print("=== 데모 1: y = x² — 2차 미분 (double backprop) ===")

x = Variable(np.array(2.0))
y = x ** 2
fill_grad(y, create_graph=True)   # 역전파가 그래프를 남기며 수행 (2층 구축)

gx = x.grad                        # gx는 Variable — "2x라는 식" (값 4)
assert gx is not None              # Pylance Optional 가드 (grad는 None 가능 타입)
print(f"1차 미분  gx = x.grad      = {gx.data}")   # 4.0
assert gx.data == np.array(4.0)

x.clear_grad()
fill_grad(gx)                      # gx에 다시 역전파 = 미분의 미분!
assert x.grad is not None
print(f"2차 미분  fill_grad(gx) 후  = {x.grad.data}")   # 2.0
assert x.grad.data == np.array(2.0)

print("→ f''(2) = 2 — step29에서 손으로 유도했던 f''가 자동으로! (gx2 함수 대체)")


# ===== 데모 2 — 3층 그래프: y = x⁴의 3차 미분 ==================================
# 기대: f'(2)=32, f''(2)=48, f'''(2)=48 (24x — 우연의 일치로 같은 48)
print()
print("=== 데모 2: y = x⁴ — 3차 미분 (그래프 3층 누적) ===")

x = Variable(np.array(2.0))
y = x ** 4
fill_grad(y, create_graph=True)

gx = x.grad                        # 4x³ = 32 — 2층 그래프 유
assert gx is not None
print(f"f'  (2) = {gx.data}")
x.clear_grad()

fill_grad(gx, create_graph=True)   # gx의 역전파도 그래프 남김 — 3층!
gxx = x.grad                       # 12x² = 48
assert gxx is not None
print(f"f'' (2) = {gxx.data}")
x.clear_grad()

fill_grad(gxx)                     # f''' = 24x
assert x.grad is not None
print(f"f'''(2) = {x.grad.data}")
assert gx.data == np.array(32.0)
assert gxx.data == np.array(48.0)
assert x.grad.data == np.array(48.0)

print("→ 필요한 만큼 위로 계속 쌓인다 — n차 미분이 '공짜'로 따라옴 (step34 예고)")


# ===== 데모 3 — sin의 2차 미분 (Cos 신규 함수 경유) ============================
# 기대: y'=cos(1), y''=-sin(1) — Sin.derivative가 cos "함수"를 호출해야
# 그래프가 연결됨 (np.cos이면 ndarray 세계로 추락 — v1 방식)
print()
print("=== 데모 3: y = sin(x) — 2차 미분 (Cos 경유) ===")

x = Variable(np.array(1.0))
y = sin(x)
fill_grad(y, create_graph=True)

gx = x.grad                        # cos(1)
assert gx is not None
print(f"y'(1)  = {gx.data:.8f}   (cos(1) = {np.cos(1.0):.8f})")
x.clear_grad()

fill_grad(gx)
assert x.grad is not None
print(f"y''(1) = {x.grad.data:.8f}   (-sin(1) = {-np.sin(1.0):.8f})")
assert gx.data is not None and x.grad.data is not None
assert np.isclose(gx.data, np.cos(1.0))
assert np.isclose(x.grad.data, -np.sin(1.0))

print("→ sin → cos → -sin — 미분 순환이 고차 미분으로 실증됨 (step34 본령)")


# ===== 데모 4 — 기본 모드는 lean: 그래프 안 남김 ================================
print()
print("=== 데모 4: create_graph=False (기본) — lean 확인 ===")

x = Variable(np.array(2.0))
y = x ** 2
fill_grad(y)                       # 기본 — 그래프 안 남김

gx = x.grad
assert gx is not None
print(f"1차 미분 값 = {gx.data}, gx.creator = {gx.creator}")
assert gx.creator is None          # 기억 상실 = 메모리 절약 (step18 철학 연장)

print("→ 일반 SGD 학습에 2차 미분 그래프는 메모리만 2배 — 기본은 버린다")


# ===== 데모 5 — 정답지(dezero/core.py)와 대조 ==================================
print()
print("=== 데모 5: dezero 정답지 대조 ===")

from dezero import Variable as DeZeroVariable   # noqa: E402

dx = DeZeroVariable(np.array(2.0))
dy = dx ** 2  # type: ignore[operator]  # dezero __pow__는 클래스 밖 대입(setup_variable)이라 Pylance가 못 봄 — 항목 031 실증
dy.backward(create_graph=True)     # dezero: backward 메서드 + create_graph

dgx = dx.grad
assert dgx is not None            # dezero grad도 Optional
dx.cleargrad()
dgx.backward()
print(f"dezero  f''(2) = {dx.grad}")            # variable(2.0)

# rezero 측도 동일 계산을 새로 수행해 나란히 비교
rx = Variable(np.array(2.0))
ry = rx ** 2
fill_grad(ry, create_graph=True)
rgx = rx.grad
assert rgx is not None
rx.clear_grad()
fill_grad(rgx)
assert rx.grad is not None
print(f"rezero  f''(2) = Variable({rx.grad.data})")   # Variable(2.0)

print()
print("★ step32 완료 — v2 탄생: Define-by-Run이 backward에도 적용되었다.")
print("  다음: step33 (뉴턴 방법 자동 계산) — gx2 손유도가 완전히 사라지는 수확")
