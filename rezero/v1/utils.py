"""rezero.v1.utils — 유틸리티 함수.

gradient check 등 검증용 헬퍼 + 계산 그래프 시각화 (Graphviz DOT).
"""

import os
import subprocess
from collections.abc import Callable

import numpy as np

from rezero.v1.core import Function, Variable, as_array, iter_reverse_topo


def numerical_diff(
    f: Callable[[Variable], Variable],
    x: Variable,
    eps: float = 1e-4,
) -> np.ndarray:
    """수치 미분 (중앙 차분). f의 내부를 몰라도 미분 가능 — 블랙박스 관점.

    gradient check용 — 역전파(해석적)와 비교해 구현이 맞는지 독립 검증.
    공식: f'(x) ≈ [f(x+h) - f(x-h)] / 2h  (중앙 차분, 오차 O(h²))

    Args:
        f: 미분할 함수 (square, 또는 합성 함수).
        x: 미분 기준점 Variable.
        eps: h (미세 차분 간격, 기본 1e-4).
    """
    if x.data is None:
        raise RuntimeError(f"{x!r}의 data가 None입니다 — 수치 미분에 사용할 수 없습니다.")

    # 차분점 생성 (x ± eps) — as_array로 스칼라 정규화
    x0 = Variable(as_array(x.data - eps))
    x1 = Variable(as_array(x.data + eps))

    # f 평가 + 결과 회수
    y0 = f(x0)
    y1 = f(x1)

    assert y0.data is not None and y1.data is not None
    return (y1.data - y0.data) / (2 * eps)


# ===== 계산 그래프 시각화 (Graphviz DOT) ========================================
# step25 — Variable/Function으로 구성된 계산 그래프를 DOT 언어로 인코딩하여
# Graphviz dot 바이너리로 PNG/PDF 등에 렌더링.
#
# 파이프라인:
#   Variable/Function 인스턴스
#       ↓ _dot_var / _dot_func    (각 객체 → DOT 노드 문자열)
#   fold_dot_graph(output)        (역방향 순회하며 DOT 텍스트 합성 = fold)
#       ↓
#   "digraph g { ... }"           (완성된 DOT 텍스트)
#       ↓ plot_dot_graph          (파일 쓰기 + dot 명령 → PNG 렌더링)
#   goldstein.png
#
# ★ fold_dot_graph의 순회 패턴(worklist + visited)은 fill_grad와 거의 동일.
#   공통화 리팩터 후보 → 이슈 32번 (step25 이후 회수).
def _dot_var(v: Variable, verbose: bool = False, show_value: bool = False) -> str:
    """Variable을 DOT 노드 문자열로 인코딩 (주황색 원).

    변수명은 볼드로 강조 (DOT HTML-like label 사용) → 그래프에서 변수 위치를
    한눈에 파악하기 쉽게. 값/shape/dtype은 보통 텍스트.

    Args:
        v: 시각화할 Variable.
        verbose: True면 라벨에 shape/dtype 추가 (정적 정보, v2 텐서에서 빛을 발).
        show_value: True면 라벨에 값 추가 (동적 정보, 디버깅용).
            verbose와 독립 — 정적 구조 정보와 동적 상태 정보는 관심사 분리.
    """
    parts: list[str] = []

    # 변수명 — 볼드 강조 (그래프에서 변수 위치를 시각적 앵커로)
    if v.name:
        parts.append(f'<B>{v.name}</B>')

    # shape/dtype (정적 정보) — 변수명 뒤면 ": "로 연결
    if verbose and v.data is not None:
        info = f'{v.shape} {v.dtype}'
        parts.append(f': {info}' if v.name else info)

    # 값 (동적 정보) — 변수명(또는 info) 뒤면 " = "로 연결
    if show_value and v.data is not None:
        value = f'{float(v.data):.4g}'
        parts.append(f' = {value}' if len(parts) > 0 else value)

    # HTML-like label: '<...>' 로 감싸면 Graphviz가 HTML 해석.
    # parts가 비어있으면 빈 라벨. 변수명/info/값은 구분자 포함해 바로 이어붙이기.
    label = ''.join(parts)
    return f'{id(v)} [label=<{label}>, color=orange, style=filled]\n'


def _dot_func(f: Function) -> str:
    """Function을 DOT 노드 문자열로 인코딩 (파란 박스) + 입력/출력 간선.

    v1은 단출력(스칼라) 가정이므로 f.output은 weakref.ref 단수.
    """
    assert f.inputs is not None, "f.inputs must be set"
    assert f.output is not None, "f.output must be set"

    ret = f'{id(f)} [label="{f.__class__.__name__}", color=lightblue, style=filled, shape=box]\n'

    # 입력 간선: 각 input Variable → 이 Function
    dot_edge = '{} -> {}\n'
    for x in f.inputs:
        ret += dot_edge.format(id(x), id(f))

    # 출력 간선: 이 Function → output Variable (weakref 역참조)
    output = f.output()
    if output is not None:
        ret += dot_edge.format(id(f), id(output))

    return ret


def fold_dot_graph(
    output: Variable,
    verbose: bool = True,
    show_value: bool = False,
) -> str:
    """output에서 역방향으로 그래프를 순회하며 DOT 텍스트를 합성(fold).

    순회 알고리즘은 fill_grad와 공유 (iter_reverse_topo 제너레이터).
    이 함수는 순회하며 DOT 텍스트를 누적하는 시각화 로직만 담당 (관심사 분리).

    Args:
        output: 그래프의 최종 출력 Variable (순회 시작점).
        verbose: True면 Variable 노드에 shape/dtype 추가 (정적 정보).
        show_value: True면 Variable 노드에 값 추가 (동적 정보, 디버깅용).

    Returns:
        완성된 DOT 텍스트 ("digraph g { ... }").
    """
    # output 노드는 순회 시작 전 먼저 찍기 (iter_reverse_topo가 yield하는 건 Function뿐)
    txt = _dot_var(output, verbose, show_value)

    # 역방향 순회하며 각 Function + inputs를 DOT 텍스트로 누적
    for func in iter_reverse_topo(output):
        assert func.inputs is not None, "func.inputs must be set"
        assert func.output is not None, "func.output must be set"
        txt += _dot_func(func)
        for x in func.inputs:
            txt += _dot_var(x, verbose, show_value)

    return f'digraph g {{\n{txt}}}'


# Graphviz dot이 지원하는 렌더링 포맷 (학습/디버깅 용도로 자주 쓰는 3종).
# 이 외에도 jpg, gif, ps 등 수십 개 있지만, rezero 범위에선 이 3개면 충분.
# 용도: png(범용/문서), svg(벡터/VSCode에서 까보기 좋음), pdf(인쇄/발표).
SUPPORTED_FORMATS: frozenset[str] = frozenset({'png', 'svg', 'pdf'})


def plot_dot_graph(
    output: Variable,
    verbose: bool = True,
    show_value: bool = False,
    to_file: str = 'output/graph.png',
) -> str:
    """계산 그래프를 DOT로 인코딩하여 Graphviz로 렌더링, 파일로 저장.

    관심사 분리: 렌더링(이 함수)과 표시(호출자)를 분리.
    항상 파일 경로(to_file)를 반환 → 터미널 환경에서 파일 위치 명확.
    Jupyter에서 인라인 표시가 필요하면 호출자가
    ``IPython.display.Image(plot_dot_graph(...))`` 로 감쌀 것.

    산출물은 output/ 폴더에 통합:
      - ``{to_file}`` (PNG/PDF/SVG 등 렌더링 결과)
      - ``{同名}.dot`` (DOT 소스 — 브로가 까볼 수 있도록 산출물로 보존)

    Args:
        output: 그래프의 최종 출력 Variable.
        verbose: True면 Variable 노드에 shape/dtype 추가 (정적 정보).
        show_value: True면 Variable 노드에 값 추가 (동적 정보, 디버깅용).
        to_file: 출력 파일 경로. **확장자가 렌더링 포맷 결정**.
            지원 포맷: png (범용/문서), svg (벡터/VSCode에서 텍스트로도 까볼 수 있음),
            pdf (인쇄/발표). 그 외 확장자는 ValueError.

    Returns:
        저장된 파일 경로 (to_file 그대로).

    Raises:
        ValueError: to_file의 확장자가 지원 포맷이 아닐 때.
        FileNotFoundError: graphviz dot 바이너리가 시스템에 없을 때.
        subprocess.CalledProcessError: dot 바이너리는 있지만 렌더링 실패
            (exit code nonzero). subprocess.run(check=True)가 발생.
    """
    # 포맷 검증 — 지원 포맷만 허용 (확장자 → 포맷)
    extension = os.path.splitext(to_file)[1][1:]  # e.g. 'png', 'svg'
    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"지원하지 않는 포맷: '.{extension}'. "
            f"지원 포맷: {sorted(SUPPORTED_FORMATS)} (png/svg/pdf)"
        )

    dot_graph = fold_dot_graph(output, verbose, show_value)

    # 산출물 디렉터리 보장 — to_file이 'output/foo.png'면 같은 폴더에 DOT도 저장
    out_dir = os.path.dirname(to_file) or '.'
    os.makedirs(out_dir, exist_ok=True)

    # DOT 소스 저장 (to_file에서 확장자만 .dot으로 교체)
    dot_path = os.path.splitext(to_file)[0] + '.dot'
    with open(dot_path, 'w') as f:
        f.write(dot_graph)

    # dot 바이너리로 렌더링 (확장자 → 포맷). shell=False + check=True로 안전하게.
    subprocess.run(
        ['dot', dot_path, '-T', extension, '-o', to_file],
        check=True,
    )

    return to_file
