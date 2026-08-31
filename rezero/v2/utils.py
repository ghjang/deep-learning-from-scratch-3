"""rezero.v2.utils — 유틸리티 함수.

계산 그래프 시각화 (Graphviz DOT) — 그래프 순회 구조와 결합되어 v2 소유.
numerical_diff는 버전 공통 순수 수학이라 rezero.common에 상주 (step32).
"""

import math
import os
import subprocess

import numpy as np

from rezero.common.utils import numerical_diff  # noqa: F401 — 공통 모듈 re-export
from rezero.v2.core import Function, Variable, iter_reverse_topo

__all__ = [
    "fold_dot_graph",
    "fold_multi_layer_dot_graph",
    "numerical_diff",
    "plot_dot_graph",
    "plot_multi_layer_graph",
]


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
def _format_value(v: float, fmt: "str | None" = None) -> str:
    """show_value용 값 포맷팅 — 디버깅 관점 설계.

    기본(fmt=None): 적응형 — 사람이 읽기 좋은 범위(1e-4 ≤ |v| < 1e5)는
    고정 소수점 4자리 (trailing 0 제거), 밖은 지수 표기 2자리.
    작은 값을 강제 고정 소수점하면 0.0000으로 죽어버려 정보 손실 → 지수로 보존.

    NaN/inf는 명시적 표기 — 디버깅 시 역전파 어디서 터졌는지 추적하는 단서.

    Args:
        v: 포맷팅할 값.
        fmt: 커스텀 포맷 스펙 (f-string format spec. 예: '.2f', '.6e', '.3g').
            None이면 적응형 기본.
    """
    if fmt is not None:
        return f'{v:{fmt}}'

    if math.isnan(v):
        return 'nan'
    if math.isinf(v):
        return 'inf'
    if v == 0:
        return '0'

    # 적응형: 읽기 좋은 범위는 고정 소수점, 밖은 지수
    if 1e-4 <= abs(v) < 1e5:
        return f'{v:.4f}'.rstrip('0').rstrip('.')
    return f'{v:.2e}'


def _dot_var(
    v: Variable,
    verbose: bool = False,
    show_value: bool = False,
    value_format: "str | None" = None,
) -> str:
    """Variable을 DOT 노드 문자열로 인코딩 (주황색 원).

    변수명은 볼드로 강조 (DOT HTML-like label 사용) → 그래프에서 변수 위치를
    한눈에 파악하기 쉽게. 값/shape/dtype은 보통 텍스트.

    Args:
        v: 시각화할 Variable.
        verbose: True면 라벨에 shape/dtype 추가 (정적 정보, v2 텐서에서 빛을 발).
        show_value: True면 라벨에 값 추가 (동적 정보, 디버깅용).
            verbose와 독립 — 정적 구조 정보와 동적 상태 정보는 관심사 분리.
        value_format: 값 포맷 스펙 (None이면 적응형 기본). 상세는 _format_value.
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
        value = _format_value(float(v.data), value_format)
        parts.append(f' = {value}' if len(parts) > 0 else value)

    # HTML-like label: '<...>' 로 감싸면 Graphviz가 HTML 해석.
    # parts가 비어있으면 빈 라벨. 변수명/info/값은 구분자 포함해 바로 이어붙이기.
    label = ''.join(parts)
    return f'{id(v)} [label=<{label}>, color=orange, style=filled]\n'


def _dot_func(f: Function, verbose: bool = False, show_value: bool = False) -> str:
    """Function을 DOT 노드 문자열로 인코딩 (파란 박스) + 입력/출력 간선.

    라벨은 f.dot_label(show_param) 훅 — 기본은 클래스명(구조만, 책 방식).
    파라미터 표시 조건: verbose(정적 상세) **또는** show_value(값의 해석 맥락 —
    값 추적 시 Pow의 c가 있어야 어떤 항의 값인지 해석 가능).
    v1은 단출력(스칼라) 가정이므로 f.output은 weakref.ref 단수.
    """
    assert f.inputs is not None, "f.inputs must be set"
    assert f.output is not None, "f.output must be set"

    show_param = verbose or show_value
    ret = f'{id(f)} [label="{f.dot_label(show_param)}", color=lightblue, style=filled, shape=box]\n'

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
    value_format: "str | None" = None,
) -> str:
    """output에서 역방향으로 그래프를 순회하며 DOT 텍스트를 합성(fold).

    순회 알고리즘은 fill_grad와 공유 (iter_reverse_topo 제너레이터).
    이 함수는 순회하며 DOT 텍스트를 누적하는 시각화 로직만 담당 (관심사 분리).

    Args:
        output: 그래프의 최종 출력 Variable (순회 시작점).
        verbose: True면 Variable 노드에 shape/dtype 추가 (정적 정보).
        show_value: True면 Variable 노드에 값 추가 (동적 정보, 디버깅용).
        value_format: 값 포맷 스펙 (None이면 적응형 기본). 상세는 _format_value.

    Returns:
        완성된 DOT 텍스트 ("digraph g { ... }").
    """
    # output 노드는 순회 시작 전 먼저 찍기 (iter_reverse_topo가 yield하는 건 Function뿐)
    txt = _dot_var(output, verbose, show_value, value_format)

    # 역방향 순회하며 각 Function + inputs를 DOT 텍스트로 누적
    for func in iter_reverse_topo(output):
        assert func.inputs is not None, "func.inputs must be set"
        assert func.output is not None, "func.output must be set"
        txt += _dot_func(func, verbose, show_value)
        for x in func.inputs:
            txt += _dot_var(x, verbose, show_value, value_format)

    return f'digraph g {{\n{txt}}}'


# ===== 다층 계산 그래프 시각화 (이슈 45) =========================================
# 여러 시작 Variable의 그래프를 한 장에 병합 — 층별 cluster + 공유 노드 복제+점선.
#
# 핵심 착안: fold_dot_graph의 노드 id가 Python 객체 id이므로,
# 여러 그래프에서 같은 객체가 나타나면 자동으로 같은 id → "공유"가 즉시 가시화됨.
#
# ★ 브로 원안 (2026-08-31): 공유 변수는 **원본을 원층 cluster 안에 두고**,
# 다른 층에는 **복제 노드**를 배치한 뒤 원본을 **점선 화살표**로 가리키게 함.
# 각 층이 그래프의 완결성을 유지하면서 변수 재사용이 명시적으로 보임.
#
# 파이프라인:
#   [Variable, Variable, ...]     (예: [y, x.grad] — 1계 미분 + 2계 미분)
#       ↓ 각 층별 역순회
#   노드별 소속 층 기록           (id → {0, 1, ...})
#       ↓ 분류
#   소속 1개 → 해당 층 cluster 안
#   소속 2개+ → 원본은 첫 층 cluster 안 / 복제는 이후 층 cluster 안 + 점선 → 원본
#       ↓ DOT 조립


def _dot_var_node(
    v: Variable,
    verbose: bool = False,
    show_value: bool = False,
    value_format: "str | None" = None,
) -> str:
    """Variable을 DOT 노드 정의만으로 인코딩 (간선 제외, _dot_var의 노드 부분)."""
    return _dot_var(v, verbose, show_value, value_format)


def _dot_var_dup(
    v: Variable,
    dup_id: str,
    verbose: bool = False,
    show_value: bool = False,
    value_format: "str | None" = None,
) -> str:
    """공유 Variable의 복제 노드 — 원본과 같은 라벨, 점선 테두리로 구분."""
    base = _dot_var_node(v, verbose, show_value, value_format)
    # 노드 id 치환 (문자열 첫 등장 = 노드 정의의 id)
    result = base.replace(str(id(v)), dup_id, 1)
    # 복제 노드 시각: 흐린 배경(moccasin) + 점선 테두리 — "같은 변수의 참조"임을 표현
    result = result.replace(
        'color=orange, style=filled]',
        'color=orange, fillcolor=moccasin, style="filled,dashed"]',
    )
    return result


def _dot_func_node(f: Function, verbose: bool = False, show_value: bool = False) -> str:
    """Function을 DOT 노드 정의만으로 인코딩 (간선 제외, _dot_func의 첫 줄)."""
    show_param = verbose or show_value
    return f'{id(f)} [label="{f.dot_label(show_param)}", color=lightblue, style=filled, shape=box]\n'


def fold_multi_layer_dot_graph(
    start_vars: "list[Variable]",
    verbose: bool = True,
    show_value: bool = False,
    value_format: "str | None" = None,
    layer_names: "list[str] | None" = None,
) -> str:
    """여러 시작 Variable의 계산 그래프를 층별 cluster로 병합한 DOT 생성.

    공유 변수는 원본이 첫 소속 층 cluster 안에, 이후 층에는 복제 노드가
    배치되고 원본을 점선 화살표로 가리킴 — 층별 완결성 + 재사용 명시.

    Args:
        start_vars: 각 층의 시작 Variable 목록 (예: [y, x.grad] — 1계/2계).
        verbose: True면 Variable 노드에 shape/dtype 추가.
        show_value: True면 Variable 노드에 값 추가.
        value_format: 값 포맷 스펙 (None이면 적응형 기본).
        layer_names: 각 층의 표시 이름 (None이면 "1층", "2층"...).

    Returns:
        완성된 DOT 텍스트 (cluster + 복제 + 점선 포함).
    """
    assert len(start_vars) >= 2, "다층 시각화는 시작점 2개 이상 필요"

    # ① 각 층별 역순회 → 노드별 소속 층 + 객체 참조 + 간선(층 정보 포함)
    var_layers: dict[int, set[int]] = {}
    func_layers: dict[int, set[int]] = {}
    vars_by_id: dict[int, Variable] = {}
    funcs_by_id: dict[int, Function] = {}
    edge_layers: dict[tuple[int, int], int] = {}  # (from, to) → first layer_idx

    for layer_idx, start_var in enumerate(start_vars):
        vid = id(start_var)
        var_layers.setdefault(vid, set()).add(layer_idx)
        vars_by_id[vid] = start_var

        for func in iter_reverse_topo(start_var):
            fid = id(func)
            func_layers.setdefault(fid, set()).add(layer_idx)
            funcs_by_id[fid] = func

            output = func.output() if func.output else None
            if output is not None:
                oid = id(output)
                var_layers.setdefault(oid, set()).add(layer_idx)
                vars_by_id[oid] = output
                edge_layers.setdefault((fid, oid), layer_idx)

            if func.inputs:
                for x in func.inputs:
                    xid = id(x)
                    var_layers.setdefault(xid, set()).add(layer_idx)
                    vars_by_id[xid] = x
                    edge_layers.setdefault((xid, fid), layer_idx)

    # ② 공유(복제) 대상 = 순전파(층 0)에 소속 + 다른 층에도 등장하는 Variable
    # 순전파의 변수(사용자 입력 x, 출력 y)만 복제 — 역전파에서 생성된
    # 상수(1, 2, 0.5 등)나 씨앗은 자기 층에만 존재 (브로 지정, 2026-08-31)
    primary_of: dict[int, int] = {vid: min(ls) for vid, ls in var_layers.items()}
    shared_vars = {
        vid for vid, ls in var_layers.items()
        if len(ls) > 1 and primary_of[vid] == 0
    }

    def effective_id(real_id: int, layer_idx: int) -> "int | str":
        """해당 층에서 이 노드를 지칭할 id — 원본 층이면 실제 id, 아니면 복제 id."""
        if real_id not in shared_vars or layer_idx == primary_of[real_id]:
            return real_id
        return f'ref{layer_idx}_{real_id}'

    # ③ DOT 조립
    lines: list[str] = []

    # 각 층 cluster
    for layer_idx in range(len(start_vars)):
        lines.append(f'subgraph cluster_{layer_idx} {{\n')
        if layer_names:
            lines.append(f'  label = "{layer_names[layer_idx]}";\n')
        lines.append('  style = rounded;\n')
        lines.append('  color = lightgray;\n')

        for vid, ls in var_layers.items():
            if layer_idx not in ls:
                continue
            if vid in shared_vars and layer_idx != primary_of[vid]:
                # 순전파 변수의 복제 (점선 테두리 — x/y 등이 하위 층에서 재사용됨)
                dup_id = f'ref{layer_idx}_{vid}'
                lines.append('  ' + _dot_var_dup(vars_by_id[vid], dup_id, verbose, show_value, value_format))
            elif layer_idx == primary_of[vid]:
                # 원본 — 리프 공유든 중간값이든, 처음 등장한 층에만 배치
                lines.append('  ' + _dot_var_node(vars_by_id[vid], verbose, show_value, value_format))
            # else: 중간값이 후속 층에도 등장하지만 primary 층에만 두고 간선으로 연결

        for fid, ls in func_layers.items():
            if layer_idx in ls:
                lines.append('  ' + _dot_func_node(funcs_by_id[fid], verbose, show_value))

        lines.append('}\n')

    # 간선 — 고유 (from, to) 조합을 실제 객체 id로 1회씩만 생성.
    # 중간값은 primary cluster에만 있으므로 자연히 그 cluster 안/경계 간선이 됨.
    # 공유 x의 간선은 원본(층 0)으로 직결 — 점선 참조 화살표가 재사용을 표현.
    for (from_id, to_id) in sorted(edge_layers):
        lines.append(f'{from_id} -> {to_id}\n')

    # 점선 참조 간선 — 복제 → 원본 ("공유" 라벨)
    for vid in shared_vars:
        for layer_idx in sorted(var_layers[vid]):
            if layer_idx != primary_of[vid]:
                dup_id = f'ref{layer_idx}_{vid}'
                lines.append(f'{vid} -> {dup_id} [style=dashed, color=gray]\n')

    return f'digraph g {{\n{"".join(lines)}}}'


def plot_multi_layer_graph(
    start_vars: "list[Variable]",
    verbose: bool = True,
    show_value: bool = False,
    value_format: "str | None" = None,
    layer_names: "list[str] | None" = None,
    to_file: str = 'output/multi_layer.png',
) -> str:
    """다층 계산 그래프를 DOT로 인코딩하여 Graphviz로 렌더링, 파일로 저장.

    Args:
        start_vars: 각 층의 시작 Variable 목록.
        verbose: True면 Variable 노드에 shape/dtype 추가.
        show_value: True면 Variable 노드에 값 추가.
        value_format: 값 포맷 스펙 (None이면 적응형 기본).
        layer_names: 각 층의 표시 이름.
        to_file: 출력 파일 경로 (확장자가 렌더링 포맷 결정).

    Returns:
        저장된 파일 경로.
    """
    extension = os.path.splitext(to_file)[1][1:]
    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"지원하지 않는 포맷: '.{extension}'. "
            f"지원 포맷: {sorted(SUPPORTED_FORMATS)}"
        )

    dot_graph = fold_multi_layer_dot_graph(
        start_vars, verbose, show_value, value_format, layer_names
    )

    out_dir = os.path.dirname(to_file) or '.'
    os.makedirs(out_dir, exist_ok=True)

    dot_path = os.path.splitext(to_file)[0] + '.dot'
    with open(dot_path, 'w') as f:
        f.write(dot_graph)

    subprocess.run(['dot', dot_path, '-T', extension, '-o', to_file], check=True)
    return to_file


# Graphviz dot이 지원하는 렌더링 포맷 (학습/디버깅 용도로 자주 쓰는 3종).
# 이 외에도 jpg, gif, ps 등 수십 개 있지만, rezero 범위에선 이 3개면 충분.
# 용도: png(범용/문서), svg(벡터/VSCode에서 까보기 좋음), pdf(인쇄/발표).
SUPPORTED_FORMATS: frozenset[str] = frozenset({'png', 'svg', 'pdf'})


def plot_dot_graph(
    output: Variable,
    verbose: bool = True,
    show_value: bool = False,
    value_format: "str | None" = None,
    to_file: str = 'output/graph.png',
) -> str:
    """계산 그래프를 DOT로 인코딩하여 Graphviz로 렌더링, 파일로 저장.

    관심사 분리: 렌더링(이 함수)과 표시(호출자)를 분리.
    항상 파일 경로(to_file)를 반환 → 터미널 환경에서 파일 위치 명확.
    Jupyter에서 인라인 표시가 필요하면 호출자가
    ``IPython.display.Image(plot_dot_graph(...))`` 로 감쌀 것.

    산출물은 output/ 폴더에 통합:
      - ``{to_file}`` (PNG/PDF/SVG 등 렌더링 결과)
      - ``{같은 이름}.dot`` (DOT 소스 — 브로가 까볼 수 있도록 산출물로 보존)

    Args:
        output: 그래프의 최종 출력 Variable.
        verbose: True면 Variable 노드에 shape/dtype 추가 (정적 정보).
        show_value: True면 Variable 노드에 값 추가 (동적 정보, 디버깅용).
        value_format: 값 포맷 스펙 (None이면 적응형 기본). 상세는 _format_value.
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

    dot_graph = fold_dot_graph(output, verbose, show_value, value_format)

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
