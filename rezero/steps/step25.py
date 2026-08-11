"""
rezero.steps.step25 — [3고지] 계산 그래프 시각화(1)
=====================================================

★ 책 공식 제목 "계산 그래프 시각화(1)". 3고지 첫 step.
★ step24의 goldstein 함수로 만들어지는 계산 그래프를 Graphviz로 시각화.

이번 step은 새 프레임워크 기능(역전파/연산자 등)을 추가하는 게 아니라,
**지금까지 만든 계산 그래프를 눈으로 보는** 시각화 도구를 붙이는 자리.
→ rezero/v1/utils.py에 fold_dot_graph / plot_dot_graph 구현 (이 step에서 승격).

★ 시각화 파이프라인 (4개 함수):
  1. _dot_var(v)        — Variable → DOT 노드 문자열 (주황색 원)
  2. _dot_func(f)       — Function → DOT 노드 (파란 박스) + 간선
  3. fold_dot_graph(z)  — output에서 역방향 순회하며 DOT 텍스트 합성 (fold)
  4. plot_dot_graph(z)  — DOT 텍스트 → 파일 → dot 명령 → PNG 렌더링

★ rezero 변형 포인트 (정답지 대비):
  - 메인 함수명: get_dot_graph → fold_dot_graph (이 작업이 fold라서)
  - 헬퍼명: add_func → fold_func (메인 함수가 fold니까)
  - weakref 처리: f.outputs 복수 → f.output() 단수 (v1은 단출력 가정)
  - subprocess: shell=True 문자열 → 리스트 인자 + check=True (안전/에러 명시)
  - 반환값: IPython Image 시도 → 파일 경로 (IPython 의존 제거, 관심사 분리)
  - 임시 폴더: ~/.dezero → ~/.rezero (브랜드 일관성)
  - 포맷팅: .format() → f-string (Python 3.12 시대 표준)

★ 순회 공통화 후보:
  fold_dot_graph의 순회 패턴(worklist + visited)이 fill_grad와 거의 동일.
  리팩터(iter_reverse_topo 제너레이터 추출)는 이슈 32번에서 step25/26 완료 후 회수.

참고 자료:
  - 원본 구현: steps/step25.py
  - 이전 step: rezero/steps/step24.py (복잡한 함수의 미분 — goldstein 재사용)
  - 이슈: 31번 (step25 진행), 32번 (순회 공통화 리팩터 — step25 이후)
  - ★ 사용 패키지: rezero/v1/ (Variable, fill_grad, plot_dot_graph, fold_dot_graph)

사전 요구:
  - Graphviz dot 바이너리 설치 (macOS: brew install graphviz)

실행:
  uv run python rezero/steps/step25.py
"""

if '__file__' in globals():
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v1 import Variable, fill_grad, fold_dot_graph, plot_dot_graph


# ===== Goldstein-Price 함수 (step24 재사용) =====================================
# step24에서 구현한 벤치마크 함수. 복잡한 다항식 곱이라 계산 그래프가 깊음.
# → 시각화용으로 적격 (그래프 구조가 풍성하게 나옴).
def goldstein(x: Variable, y: Variable) -> Variable:
    """Goldstein-Price 함수: 두 복잡한 다항식의 곱. (step24와 동일)"""
    z = (
        (1 + (x + y + 1) ** 2 * (19 - 14 * x + 3 * x ** 2 - 14 * y + 6 * x * y + 3 * y ** 2))
        * (30 + (2 * x - 3 * y) ** 2 * (18 - 32 * x + 12 * x ** 2 + 48 * y - 36 * x * y + 27 * y ** 2))
    )
    return z


# --- 데모: Goldstein 계산 그래프 시각화 -----------------------------------------
if __name__ == "__main__":
    print("=== step25 계산 그래프 시각화(1) — Goldstein 그래프 ===")
    print()

    # --- [1] 순전파 + 역전파 ---
    print("[1] Goldstein 순전파 + 역전파")
    x = Variable(np.array(1.0))
    y = Variable(np.array(1.0))
    z = goldstein(x, y)
    fill_grad(z)
    print(f"    z      = {z.data}")
    print(f"    x.grad = {x.grad}")
    print(f"    y.grad = {y.grad}")
    print()

    # --- [2] DOT 텍스트만 출력 (graphviz 없이도 그래프 구조 확인 가능) ---
    print("[2] fold_dot_graph — DOT 텍스트 (graphviz 없이 구조 확인)")
    x.name = 'x'
    y.name = 'y'
    z.name = 'z'
    dot_text = fold_dot_graph(z, verbose=False)
    print(dot_text)
    print(f"    ★ Variable은 주황색 원, Function은 파란 박스로 인코딩됨")
    print()

    # --- [3] PNG 렌더링 (Graphviz dot 바이너리 필요) ---
    print("[3] plot_dot_graph — PNG 렌더링")
    to_file = 'output/goldstein.png'
    saved_path = plot_dot_graph(z, verbose=False, to_file=to_file)
    print(f"    저장: {saved_path}")
    print(f"    DOT 소스: {saved_path.replace('.png', '.dot')} (브로가 까볼 수 있음)")
    print(f"    ★ 파일을 열어 계산 그래프 구조를 직접 확인해보세요")
    print()

    # --- [4] verbose=True vs False 비교 ---
    print("[4] verbose=True — Variable 노드에 shape/dtype 추가")
    dot_verbose = fold_dot_graph(z, verbose=True)
    # 노드 라벨만 추출해서 비교 (전체 출력은 [2]와 구조 동일)
    for line in dot_verbose.split('\n'):
        if 'label=' in line and 'orange' in line:
            print(f"    {line.strip()}")
    print(f"    ★ verbose=True면 'x: () float64' 식으로 shape/dtype이 라벨에 붙음")
    print(f"    ★ v1은 스칼라라 shape이 ()라 시시해 보이지만, v2 텐서가 되면 빛을 발함")
    print()

    # --- [5] show_value=True (verbose=False) — Variable 노드에 실제 값만 표시 ---
    print("[5] show_value=True — Variable 노드에 값 추가 (디버깅용)")
    dot_value = fold_dot_graph(z, verbose=False, show_value=True)
    for line in dot_value.split('\n'):
        if 'label=' in line and 'orange' in line:
            print(f"    {line.strip()}")
    print(f"    ★ show_value=True면 'x = 1', 'z = 1876' 식으로 값이 라벨에 붙음")
    print(f"    ★ 이름 없는 중간 Variable도 값은 표시 ('= 12' 등)")
    print(f"    ★ verbose(정적 구조)와 독립 — 관심사 분리")
    print(f"    ★ 실용: NaN 추적, 역전파 값 검증, gradient check 실패 시 원인 파악")
    print()

    # --- [6] show_value PNG — 값이 표시된 그래프 파일 ---
    print("[6] show_value=True PNG — 값이 표시된 그래프")
    to_file_value = 'output/goldstein_value.png'
    saved_value = plot_dot_graph(z, verbose=False, show_value=True, to_file=to_file_value)
    print(f"    저장: {saved_value}")
    print(f"    ★ verbose=False라 shape/dtype 노이즈 없이, 값만 깔끔하게")
    print(f"    ★ 변수명이 볼드로 강조되어 그래프에서 변수 위치가 한눈에 (DOT HTML-like label)")
    print()

    # --- [7] 포맷 비교 (PNG vs SVG) — 벡터 포맷의 가치 ---
    print("[7] 포맷 비교 — PNG(비트맵) vs SVG(벡터)")
    print("    지원 포맷: png (범용), svg (벡터), pdf (인쇄)")
    print("    ★ SVG는 확대해도 깨끗함 + VSCode에서 텍스트(XML)로도 까볼 수 있음")

    svg_path = plot_dot_graph(z, verbose=False, show_value=True, to_file='output/goldstein.svg')
    print(f"    SVG 저장: {svg_path}")
    print()

    # --- [8] 미지원 포맷 에러 처리 ---
    print("[8] 미지원 포맷 — ValueError")
    try:
        plot_dot_graph(z, to_file='output/bad.jpg')
    except ValueError as e:
        print(f"    ValueError: {e}")
    print(f"    ★ 지원 포맷이 아닌 확장자는 명시적 에러 (조용한 실패 방지)")
    print()

    print("=== step25 완료 — 계산 그래프 시각화 도구 구축 ===")
    print("    output/goldstein.png:        구조만 (verbose=False, show_value=False)")
    print("    output/goldstein_value.png:  구조 + 값 (verbose=False, show_value=True)")
    print("    output/goldstein.svg:        SVG 벡터 (확대해도 깨끗함)")
    print("    파일을 열어 그래프를 직접 눈으로 확인! 🎨")
