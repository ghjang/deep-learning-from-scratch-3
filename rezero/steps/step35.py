"""
rezero.steps.step35 — [3고지] 고차 미분 계산 그래프
=====================================================================

★ 책 공식 제목 "고차 미분 계산 그래프". tanh의 고차 미분 그래프를 시각화.

★★★ 이 step의 심장 — 자기 참조 도함수와 그래프 폭증:

    y  = tanh(x)
    y' = 1 - tanh(x)²            ← tanh가 다시 등장 (자기 참조!)
    y'' = -2·tanh(x)·(1-tanh(x)²) ← tanh가 또!

  sin(순환): 다른 함수들 사이를 4주기로 돌음 → 그래프 크기 일정
  tanh(폭증): 자기를 다시 참조 → 미분마다 Tanh 노드가 그래프에 추가
  → 책이 iters=1 (2차까지만)로 제한한 이유.

★★ 후보 8번 회수 (step33에서 등록한 탐구) — 이 데모에서 눈으로 검증:
  1. 1층/2층이 **같은 x 객체를 공유** — DOT 노드 id(id(v))가 같은 번호로 찍힘
     (id(x)가 그래프에 여러 간선으로 등장 = 재미분 가능의 구조적 비밀)
  2. gy(시작 기울기 Variable(1))도 리프로 존재
  3. Tanh 노드가 미분 차수만큼 추가 (폭증의 실체)

실행: uv run python rezero/steps/step35.py → output/tanh_gx2.png 등 생성
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v2 import Variable, fill_grad, tanh
from rezero.v2.utils import fold_dot_graph, plot_dot_graph


# ===== 데모 1 — tanh 고차 미분 수치 검증 =======================================
print("=== 데모 1: tanh 고차 미분 수치 검증 (x = 0.5) ===")

x = Variable(np.array(0.5))
y = tanh(x)
fill_grad(y, create_graph=True)

t = np.tanh(0.5)
gx = x.grad                          # y' = 1 - tanh²
assert gx is not None and gx.data is not None
print(f"y'  실측 {gx.data:.8f}  기대 {1 - t**2:.8f}  (1 - tanh²)")
assert np.isclose(gx.data, 1 - t**2)

x.clear_grad()
fill_grad(gx, create_graph=True)
gxx = x.grad                         # y'' = -2·tanh·(1-tanh²)
assert gxx is not None and gxx.data is not None
expected2 = -2 * t * (1 - t**2)
print(f"y'' 실측 {gxx.data:.8f}  기대 {expected2:.8f}  (-2·tanh·(1-tanh²))")
assert np.isclose(gxx.data, expected2)

print("→ 자기 참조 도함수의 2차 미분까지 정확 — Tanh 노드를 경유해 흐름")


# ===== 데모 2 — gx 그래프 시각화 (책 방식, iters=1) ============================
print()
print("=== 데모 2: 미분 식의 계산 그래프 시각화 (1차 → 2차 순서로) ===")

x = Variable(np.array(1.0))
x.name = 'x'
y = tanh(x)
y.name = 'y'
fill_grad(y, create_graph=True)

gx = x.grad                          # 1차 미분 식 (그래프 유)
assert gx is not None
gx.name = 'gx'
out1 = plot_dot_graph(gx, verbose=False, show_value=True, to_file='output/tanh_gx.png')
print(f"1차 미분 식 gx 그래프: {out1} (Tanh 1개 — derivative의 tanh 재호출분)")

x.clear_grad()
fill_grad(gx, create_graph=True)     # 2차도 그래프 남김
gx2 = x.grad                         # 2차 미분 식
assert gx2 is not None
gx2.name = 'gx2'
out2 = plot_dot_graph(gx2, verbose=False, show_value=True, to_file='output/tanh_gx2.png')
print(f"2차 미분 식 gx2 그래프: {out2} (Tanh 2개 — 재호출이 한 번 더 누적)")
print("→ ★ 시각화 코드(v1 step25 제작)는 무수정 — gx2도 '그래프 소유 Variable'일 뿐이라")
print("  fold_dot_graph가 그냥 재활용됨 (Define-by-Run 일반성의 시각화 버전)")
print("→ ★ show_value=True — 우리 변수명+값 옵션 (step25 제작). 값이 1.0/0.7616 등으로")
print("  찍히며 어느 노드가 어느 값인지 추적 가능")


# ===== 데모 3 — ★ 후보 8번 검증: 같은 x 공유 + gy 리프 ========================
print()
print("=== 데모 3: 후보 8번 — 1층/2층이 같은 x를 공유하는가? ===")

dot = fold_dot_graph(gx2, verbose=False)

x_id = id(x)
# x 노드 정의/간선으로 등장한 총 횟수 — 여러 번이면 하나의 객체에 여러 연결 = 공유
x_refs = dot.count(str(x_id))
print(f"id(x) = {x_id} → 그래프 내 등장 {x_refs}회 (정의 + 간선)")
assert x_refs >= 3, "x가 그래프에 여러 간선으로 이어져야 함 (1층 Tanh + 2층 Tanh)"

# Function 노드 수 확인 — Tanh가 몇 개인가 (폭증의 실체)
tanh_count = dot.count('label="Tanh"')
total_funcs = dot.count('shape=box')
print(f"Function 노드: 총 {total_funcs}개, 그중 Tanh = {tanh_count}개")
assert tanh_count == 2, "1차(원래 함수) + 2차(derivative의 tanh 재호출) = 2개"

print("→ ★ 검증 완료: 같은 x 객체에 1층/2층 Tanh가 모두 연결 —")
print("  이것이 'gx를 x로 미분'이 물리적으로 성립하는 구조 (탐구 노트 30 실증)")


# ===== 데모 4 — 폭증 실증: 미분 차수별 Tanh 노드 수 ===========================
print()
print("=== 데모 4: 폭증 실증 — 미분 반복 시 Tanh 노드 누적 ===")


def count_tanh_nodes(iters: int) -> tuple[int, int]:
    """iters번 재미분한 식의 그래프에서 (Tanh 노드 수, 전체 Function 수) 카운트."""
    xx = Variable(np.array(1.0))
    yy = tanh(xx)
    fill_grad(yy, create_graph=True)

    for _ in range(iters):
        g = xx.grad
        assert g is not None
        xx.clear_grad()
        fill_grad(g, create_graph=True)

    final = xx.grad
    assert final is not None
    d = fold_dot_graph(final, verbose=False)
    return d.count('label="Tanh"'), d.count('shape=box')


for iters in [1, 2, 3, 4, 5]:
    tanh_n, funcs_n = count_tanh_nodes(iters)
    print(f"재미분 {iters}회 → Tanh {tanh_n}개 / 전체 Function {funcs_n}개")

print("→ Tanh가 2→4→8 — 매 미분마다 2배씩 **지수 폭증**!")
print("  y'' = -2·tanh·(1-tanh²)처럼 식 속의 tanh 참조가 미분마다 복제되므로.")
print("  (sin이었다면 순환해 크기 일정 — 그래프 3형태의 '폭증' vs '순환' 대비)")


# ===== 데모 5 — 3~5차 미분 그래프 각각 시각화 (폭증 관찰) =====================
print()
print("=== 데모 5: 3~5차 미분 그래프 각각 시각화 ===")

x = Variable(np.array(1.0))
x.name = 'x'
y = tanh(x)
y.name = 'y'
fill_grad(y, create_graph=True)

for re_iter in range(1, 5):          # 재미분 1~4회 → 2~5차
    g = x.grad
    assert g is not None
    x.clear_grad()
    fill_grad(g, create_graph=True)
    order = re_iter + 1              # 현재 차수

    if order >= 3:                   # 3, 4, 5차만 시각화
        final = x.grad
        assert final is not None
        final.name = f'gx{order}'
        d = fold_dot_graph(final, verbose=False)
        tanh_n = d.count('label="Tanh"')
        funcs_n = d.count('shape=box')
        out = plot_dot_graph(final, verbose=False, to_file=f'output/tanh_gx{order}.png')
        print(f"{order}차: Tanh {tanh_n}개 / Function {funcs_n}개 → {out}")

print("→ 그래프를 열어보면 차수마다 Tanh 박스가 2배씩 늘어나는 폭증이 보임.")
print("  (8차는 노드 수만 개라 dot 렌더링이 수 분 — 폭증의 진짜 의미: 렌더링조차 무거움)")


# ===== 데모 6 — 재사용형(Config.reuse_output=True) 그래프 — 대비 관찰 =========
print()
print("=== 데모 6: 재사용형(Config.reuse_output=True) — 폭증 대비 ===")
print("★ derivative는 역전파 중 호출 — 블록이 fill_grad를 감싸야 효과 있음\n")

from rezero.v2 import using_config   # noqa: E402

x = Variable(np.array(1.0))
x.name = 'x'
y = tanh(x)
y.name = 'y'

with using_config('reuse_output', True):
    fill_grad(y, create_graph=True)

    gx = x.grad                      # 1차 (재사용형 — Tanh 1개)
    assert gx is not None
    gx.name = 'gx'
    plot_dot_graph(gx, verbose=False, show_value=True, to_file='output/tanh_gx_reuse.png')

    for re_iter in range(1, 5):      # 재미분 1~4회 → 2~5차
        g = x.grad
        assert g is not None
        x.clear_grad()
        fill_grad(g, create_graph=True)
        order = re_iter + 1

        final = x.grad
        assert final is not None
        final.name = f'gx{order}'
        d = fold_dot_graph(final, verbose=False)
        print(f"{order}차: Tanh {d.count('label=\"Tanh\"')}개 / "
              f"Function {d.count('shape=box')}개 → output/tanh_gx{order}_reuse.png")
        plot_dot_graph(final, verbose=False, to_file=f'output/tanh_gx{order}_reuse.png')

# 파일 크기 대비 — 폭증이 눈에 보이는 또 하나의 척도
print()
print("=== 파일 크기 대비 (재호출형 vs 재사용형) ===")
for n in [1, 2, 3, 4, 5]:
    suffix = '' if n == 1 else str(n)
    size_a = os.path.getsize(f'output/tanh_gx{suffix}.png') // 1024
    size_b = os.path.getsize(f'output/tanh_gx{suffix}_reuse.png') // 1024
    print(f"{n}차: 재호출 {size_a:5d} KB  vs  재사용 {size_b:4d} KB")

print("→ 재사용형은 차수를 올려도 Tanh 1개 — 그래프가 컴팩트하게 유지된다.")
print("  두 전략의 수치 결과는 완전히 동일 (test_reuse_output_strategy 검증).")

print()
print("★ step35 완료 — 재귀적 도함수(tanh)의 그래프를 눈으로 봤다.")
print("  다음: step36 (살아있는 그래프 재사용 — z = gx³ + y) — 3고지 마지막!")
