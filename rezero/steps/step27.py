"""
rezero.steps.step27 — [3고지] 테일러 급수 미분
=================================================

★ 책 공식 제목 "테일러 급수 미분". 3고지 3번째 step.
★ Sin 클래스는 v1/functions.py로 승격됨 (이 파일은 사용자 코드 관점).

★★★ 이 step의 심장 — 두 층위 구조:

  층위 1 (당연함): sin(x) — derivative에 cos를 직접 가르쳐 준 함수.
    도함수를 아는 함수의 미분. "시험 문제에 답 적어놓고 시험 본 격".

  층위 2 (대서사): my_sin(x) — cos라는 단어를 코드 어디에도 모르는
    +, **, * 만의 다항식 합성. 그런데 계산 그래프를 역전파하면
    cos 값이 나온다!

    수학적 정체 — 테일러 항별 미분 = cos의 테일러 전개:
      d/dx[x - x³/3! + x⁵/5! - ...] = 1 - x²/2! + x⁴/4! - ...
      (3/3! = 1/2!, 5/5! = 1/4!)

  ★ 핵심 문장: "무엇의 도함수인지 가르쳐 준 함수만 미분할 수 있는 게 아니라,
  그래프를 만들 수만 있다면 그 그래프의 도함수가 저절로 나온다."
  → Define-by-Run의 본질. sin(층위 1)은 이 문장의 대조군.

★ v1 연산자 3부작 총동원:
  - y = 0; y = y + t   → int + Variable → __radd__ (step21)
  - c * x ** (2i+1)    → float * Variable → __rmul__ (step21), Pow (step22)

참고 자료:
  - 원본 구현: steps/step27.py (정답지 — 인접 step26/28 비교 완료)
  - 이전 step: rezero/steps/step25.py (plot_dot_graph 재사용)
  - 이슈: 34번 (step27 진행 추적)

실행:
  uv run python rezero/steps/step27.py
"""

if '__file__' in globals():
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import math

import numpy as np

from rezero.v1 import Variable, fill_grad, fold_dot_graph, plot_dot_graph, sin
from rezero.v1.utils import _format_value


# ===== my_sin — 테일러 급수 근사 (step 한정 학습 함수) ===========================
# sin(x) = Σ (-1)^i / (2i+1)! · x^(2i+1)  (i = 0, 1, 2, ...)
#
# 마지막 항의 크기가 threshold보다 작아지면 break — 수렴 판정.
# cos를 전혀 모르는 +, **, * 연산의 합성 → 역전파하면 cos 근사값이 나옴 (대서사).
def my_sin(x: Variable, threshold: float = 0.0001) -> Variable:
    """테일러 급수로 sin을 근사. threshold는 수렴 판정 임계값."""
    y: Variable | int = 0  # int 0에서 시작 — 첫 y = y + t에서 int + Variable → __radd__ 호출!
    for i in range(100000):
        c = (-1) ** i / math.factorial(2 * i + 1)   # 계수 (파이썬 float 상수)
        t = c * x ** (2 * i + 1)                    # float * Variable → __rmul__, x**n → Pow
        y = y + t

        # 수렴 판정 — 마지막 항이 충분히 작으면 중단
        if abs(t.data) < threshold:
            break

    # 루프는 최소 1회 실행되므로 y는 항상 Variable (int 0은 첫 덧셈에서 Variable 됨)
    assert isinstance(y, Variable)
    return y


# --- 데모: 원본 sin vs 테일러 근사 my_sin ---------------------------------------
if __name__ == "__main__":
    print("=== step27 테일러 급수 미분 — sin vs my_sin ===")
    print()

    # --- [1] 층위 1: 원본 sin (derivative에 cos를 가르쳐 준 함수) ---
    print("[1] 원본 sin(x) — derivative hook이 cos를 알고 있음")
    x = Variable(np.array(np.pi / 4))
    y = sin(x)
    fill_grad(y)
    print(f"    y      = {y.data:.10f}   (기대: sin(π/4) = {np.sin(np.pi/4):.10f})")
    print(f"    x.grad = {x.grad:.10f}   (기대: cos(π/4) = {np.cos(np.pi/4):.10f})")
    print()

    # --- [2] 층위 2: my_sin (cos를 모르는 다항식 합성) — 대서사 ---
    print("[2] my_sin(x) — cos를 전혀 모르는 테일러 다항식")
    x = Variable(np.array(np.pi / 4))
    y = my_sin(x)
    fill_grad(y)
    print(f"    y      = {y.data:.10f}   (원본 sin과 일치?)")
    print(f"    x.grad = {x.grad:.10f}   (원본 cos와 일치? ★ 대서사!)")
    print(f"    → +, **, * 만의 그래프를 역전파했을 뿐인데 cos가 나옴")
    print()

    # --- [3] threshold에 따른 항 개수와 정확도 비교 ---
    print("[3] threshold별 비교 — 항 개수 vs 정확도")
    for threshold in [1e-2, 1e-4, 1e-6, 1e-8]:
        x = Variable(np.array(np.pi / 4))
        y = my_sin(x, threshold=threshold)
        fill_grad(y)

        # 실제 사용된 항 개수 계산 (threshold 도달 시점)
        n_terms = 0
        t_val = 1.0
        i = 0
        while abs(t_val) >= threshold:
            c = (-1) ** i / math.factorial(2 * i + 1)
            t_val = abs(c * (np.pi / 4) ** (2 * i + 1))
            n_terms += 1
            i += 1

        err_y = abs(y.data - np.sin(np.pi / 4))
        err_g = abs(x.grad - np.cos(np.pi / 4))
        print(f"    threshold={threshold:.0e}: 항 {n_terms}개 | "
              f"y 오차 {err_y:.2e} | grad 오차 {err_g:.2e}")
    print(f"    ★ 항이 늘수록 오차 급감 — 테일러 급수의 수렴")
    print(f"    ★ grad 오차도 같이 줄어듦 — 근사 다항식의 미분 = cos의 근사")
    print()

    # --- [4] my_sin 계산 그래프 시각화 ---
    print("[4] my_sin 계산 그래프 시각화")
    x = Variable(np.array(np.pi / 4))
    y = my_sin(x)
    fill_grad(y)
    x.name = 'x'
    y.name = 'y'
    saved = plot_dot_graph(y, verbose=False, show_value=True, to_file='output/my_sin.png')
    print(f"    저장: {saved}")
    print(f"    ★ 반복문으로 조립한 테일러 다항식의 그래프 — Pow/Add/Mul 체인")
    print()

    # show_value=True → Pow 라벨에 지수 포함 (값의 해석 맥락 — 어떤 항의 값인지 구분)
    print("    show_value=True의 Pow 라벨 (값 해석 맥락으로 c 표시):")
    dot_value = fold_dot_graph(y, verbose=False, show_value=True)
    pow_labels = sorted(set(l.strip() for l in dot_value.split('\n') if 'Pow(c=' in l))
    for line in pow_labels:
        print(f"      {line}")
    print(f"    ★ 테일러 급수의 홀수 차수 구조 (c=1, 3, 5, 7)가 라벨로 보임")

    # 구조만 보고 싶을 때 — 둘 다 False면 책 방식 (클래스명만)
    print("    참고: verbose=False + show_value=False (구조만) → Pow (클래스명만)")
    print()

    # --- [5] 값 포맷팅 — 적응형 기본 vs 커스텀 스펙 (디버깅 관점) ---
    print("[5] show_value 포맷팅 — 테일러 계수 스케일 다양성으로 비교")
    test_values = [0.7853981634, -0.0807455122, 0.0021486871, -2.48446e-05, 1876.0]
    print(f"    {'원래 값':>16} | {'기본 (적응형)':>14} | {'.2f':>8} | {'.8e':>12}")
    for v in test_values:
        print(f"    {v:>16.10g} | {_format_value(v):>14} | {_format_value(v, '.2f'):>8} | {_format_value(v, '.8e'):>12}")
    print(f"    ★ 기본: 읽기 좋은 범위는 고정 소수점 4자리, 작은 값은 지수로 정보 보존")
    print(f"    ★ value_format 스펙으로 원하는 형태 지정 가능 (f-string format spec)")
    print()

    # 실제 fold_dot_graph에 적용한 모습 (커스텀 스펙 .2f)
    dot_custom = fold_dot_graph(y, verbose=False, show_value=True, value_format='.2f')
    shown = [l.strip() for l in dot_custom.split('\n') if 'orange' in l][:5]
    print(f"    value_format='.2f' 적용 라벨 예시:")
    for line in shown:
        print(f"      {line}")
    print()

    # --- [6] threshold=1e-150 — 책의 마지막 예제 (그래프 폭발 관찰) ---
    # threshold가 극도로 작으면 테일러 항이 약 48개(x^97 부근)까지 늘어남.
    # 각 항마다 Pow/Mul/Add 노드가 쌓이며 노드 수백 개짜리 그래프가 됨.
    # 노드가 수밭 개면 값 라벨이 깨알처럼 붙어 안 읽힘 → 구조 감상용으로 show_value=False.
    print("[6] threshold=1e-150 — 책의 마지막 예제")
    x = Variable(np.array(np.pi / 4))
    y = my_sin(x, threshold=1e-150)
    fill_grad(y)
    x.name = 'x'
    y.name = 'y'
    saved = plot_dot_graph(y, verbose=False, show_value=False, to_file='output/my_sin_full.png')
    print(f"    저장: {saved}")

    # 그래프 규모 체감 — 노드/간선 수
    dot_text = fold_dot_graph(y, verbose=False, show_value=False)
    n_nodes = sum(1 for l in dot_text.split('\n') if '[label=' in l)
    n_edges = sum(1 for l in dot_text.split('\n') if '->' in l)
    print(f"    노드 {n_nodes}개 / 간선 {n_edges}개 (기본 threshold=1e-4일 때는 ~30개)")
    print(f"    ★ 렌더링된 그림이 '뒤집힌 직각 삼각형' 모양 — 삼각함수 근사 그래프가")
    print(f"      삼각형이라는 우연 (브로 관찰, 책의 마지막 웃픈 포인트) ㅍㅋㅋ")
    print()

    print("=== step27 완료 — 근사 함수도 Define-by-Run으로 미분된다 ===")
    print("    sin:  도함수를 가르쳐 준 함수 (당연)")
    print("    my_sin: 그래프를 만들기만 한 함수 (★ 저절로 cos!) 🎉")
