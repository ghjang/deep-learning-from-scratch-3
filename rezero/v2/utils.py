"""rezero.v2.utils — 유틸리티 함수.

계산 그래프 시각화 (Graphviz DOT) — 그래프 순회 구조와 결합되어 v2 소유.
numerical_diff는 버전 공통 순수 수학이라 rezero.common에 상주 (step32).
"""

import math
import os
import subprocess
from typing import cast

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


def _format_data(
    data: np.ndarray,
    fmt: "str | None" = None,
    max_items: int = 4,
    show_array: bool = True,
) -> str:
    """노드 라벨용 데이터 포맷팅 — 스칼라는 값 그대로, 배열은 show_array에 따라.

    책 관례(dezero)는 배열 값을 표시하지 않고 shape/dtype만(verbose) 보이지만,
    rezero의 show_value 옵션은 "값을 보여준다"는 계약이므로 배열도 성실히 이행 —
    show_array=True(기본): 앞 max_items개 원소 (적응형 포맷 재사용) + shape.
    show_array=False: 배열은 값 없이 shape만 (책 관례에 가까운 절제 모드).
    """
    if data.ndim == 0:
        return _format_value(float(data), fmt)

    if not show_array:
        return f'{data.shape}'

    flat = data.ravel()
    shown = [_format_value(float(u), fmt) for u in flat[:max_items]]
    suffix = ', ...' if flat.size > max_items else ''
    return f'[{", ".join(shown)}{suffix}] {data.shape}'


def _dot_var(
    v: Variable,
    verbose: bool = False,
    show_value: bool = False,
    value_format: "str | None" = None,
    array_show_value: bool = True,
) -> str:
    """Variable을 DOT 노드 문자열로 인코딩 (주황색 원).

    변수명은 볼드로 강조 (DOT HTML-like label 사용) → 그래프에서 변수 위치를
    한눈에 파악하기 쉽게. 값/shape/dtype은 보통 텍스트.

    Args:
        v: 시각화할 Variable.
        verbose: True면 라벨에 shape/dtype 추가 (정적 정보, v2 텐서에서 빛을 발).
        show_value: True면 라벨에 값 추가 (동적 정보, 디버깅용).
            스칼라는 값 그대로, 배열은 array_show_value에 따라 요약/shape.
            verbose와 독립 — 정적 구조 정보와 동적 상태 정보는 관심사 분리.
        array_show_value: show_value=True일 때 배열 값을 표시할지.
            True(기본) — 앞 4개 요약 + shape / False — shape만 (책 관례 절제 모드).
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
        value = _format_data(v.data, value_format, show_array=array_show_value)
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
    array_show_value: bool = True,
) -> str:
    """output에서 역방향으로 그래프를 순회하며 DOT 텍스트를 합성(fold).

    순회 알고리즘은 fill_grad와 공유 (iter_reverse_topo 제너레이터).
    이 함수는 순회하며 DOT 텍스트를 누적하는 시각화 로직만 담당 (관심사 분리).

    Args:
        output: 그래프의 최종 출력 Variable (순회 시작점).
        verbose: True면 Variable 노드에 shape/dtype 추가 (정적 정보).
        show_value: True면 Variable 노드에 값 추가 (동적 정보, 디버깅용).
        value_format: 값 포맷 스펙 (None이면 적응형 기본). 상세는 _format_value.
        array_show_value: show_value=True일 때 배열 값 표시 (True=요약 / False=shape만).

    Returns:
        완성된 DOT 텍스트 ("digraph g { ... }").
    """
    # output 노드는 순회 시작 전 먼저 찍기 (iter_reverse_topo가 yield하는 건 Function뿐)
    txt = _dot_var(output, verbose, show_value, value_format, array_show_value)

    # 역방향 순회하며 각 Function + inputs를 DOT 텍스트로 누적
    for func in iter_reverse_topo(output):
        assert func.inputs is not None, "func.inputs must be set"
        assert func.output is not None, "func.output must be set"
        txt += _dot_func(func, verbose, show_value)
        for x in func.inputs:
            txt += _dot_var(x, verbose, show_value, value_format, array_show_value)

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


def _is_seed(v: Variable) -> bool:
    """역전파 씨앗 판별 — fill_grad가 name='seed'로 이름을 부여함.

    값이 1이라고 전부 씨앗이 아님 (chain rule 상수 1과 구분).
    """
    return v.name == "seed"


def _dot_var_node(
    v: Variable,
    verbose: bool = False,
    show_value: bool = False,
    value_format: "str | None" = None,
    is_seed: bool = False,
    array_show_value: bool = True,
) -> str:
    """Variable을 DOT 노드 정의만으로 인코딩 (간선 제외).
    is_seed=True면 금색으로 구분 (역전파 시작 씨앗)."""
    base = _dot_var(v, verbose, show_value, value_format, array_show_value)
    if is_seed:
        # 씨앗: gold 배경 + 별도 표시 — "이 1이 역전파를 시작했다"
        base = base.replace(
            'color=orange, style=filled',
            'color=gold, style=filled, penwidth=2'
        )
    return base


def _dot_func_node(f: Function, verbose: bool = False, show_value: bool = False) -> str:
    """Function을 DOT 노드 정의만으로 인코딩 (간선 제외, _dot_func의 첫 줄)."""
    show_param = verbose or show_value
    return f'{id(f)} [label="{f.dot_label(show_param)}", color=lightblue, style=filled, shape=box]\n'


def _normalize_layers(
    start_vars: "list[Variable | list[Variable] | list[list[Variable]]]",
) -> list[list[list[Variable]]]:
    """각 층을 서브그룹 목록 list[list[Variable]]로 정규화.

    층 표현 3종 (서브그룹핑 — 브로 아이디어, 이슈 45):
      Variable             → 서브그룹 1개 (하위 박스는 생략 — 1개뿐이니 그릴 필요 없음)
      list[Variable]       → 각 Variable이 서브그룹 1개씩 (자동 서브그룹핑 —
                             "층에 넘긴 리스트의 각 Variable = 서브그룹 1개" 규칙)
      list[list[Variable]] → 각 내부 리스트가 서브그룹 (2계 Hessian 행별 묶음 —
                             [[hxx, hyx], [hxy, hyy]] → x행 박스 + y행 박스)
    """
    assert len(start_vars) >= 2, "다층 시각화는 시작점 2개 이상 필요"

    layers: list[list[list[Variable]]] = []
    for item in start_vars:
        if isinstance(item, Variable):
            layers.append([[item]])
        elif all(isinstance(v, Variable) for v in item):
            assert item, "빈 층(list)은 전달할 수 없음"
            # all(isinstance)는 타입 가드가 아니므로 cast로 정적 분석과 화해
            flat = cast("list[Variable]", item)
            layers.append([[v] for v in flat])
        else:
            groups = [list(cast("list[Variable]", g)) for g in item]
            assert groups and all(
                g and all(isinstance(v, Variable) for v in g) for g in groups
            ), "list[list[Variable]] 형태여야 함 (각 내부 리스트는 비지 않은 Variable 목록)"
            layers.append(groups)

    return layers


def _ordinal(n: int) -> str:
    """서수 접미사 — 1st/2nd/3rd/4th... (11~13은 th). 층 라벨용."""
    if 11 <= n % 100 <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f'{n}{suffix}'


def fold_multi_layer_dot_graph(
    start_vars: "list[Variable | list[Variable] | list[list[Variable]]]",
    verbose: bool = True,
    show_value: bool = False,
    value_format: "str | None" = None,
    layer_names: "list[str] | None" = None,
    array_show_value: bool = True,
    show_labels: bool = True,
) -> str:
    """여러 시작 Variable의 계산 그래프를 층별 cluster + 층 내 서브그룹으로 병합.

    ★ 무복제 원칙: 각 노드는 전체 그래프에 딱 1번만 등장.
    ★ 다변수 지원 (브로 발견, 2026-08-31): 한 층에 여러 Variable을 리스트로
      전달 가능 — 다변수 함수의 역전파는 입력 변수 수만큼 그래디언트 그래프를
      만들므로, 같은 층에 전부 포함해야 정확한 시각화.
    ★ 층 내 서브그룹핑 (브로 아이디어, 2026-09-02): 다변수 층의 그래프는
      그래디언트 성분별(1계)·Hessian 행별(2계)로 여러 덩어리가 섞여 보임 →
      Graphviz 중첩 cluster로 구분. 서브그룹 2개 이상에 소속된 노드
      (seed 등 공통 재료)는 서브그룹 밖 층 최상위에 배치해 '공유'임을 시각화.

    Args:
        start_vars: 각 층의 시작점. 3종 (상세는 _normalize_layers).
            단변수: [y, gx, gx2] (기존 방식 그대로 — 하위 박스 없음)
            다변수 자동: [z, [gx, gy]] — cluster_1 안에 gx박스 + gy박스
            Hessian 행별: [z, [gx, gy], [[hxx, hyx], [hxy, hyy]]]
        verbose: True면 Variable 노드에 shape/dtype 추가 (노드 정적 정보 — 책 관례).
        show_value: True면 Variable 노드에 값 추가.
        value_format: 값 포맷 스펙 (None이면 적응형 기본).
        layer_names: 각 층의 표시 이름 (주면 자동 라벨 대신 사용).
        array_show_value: show_value=True일 때 배열 값 표시 (True=요약 / False=shape만).
        show_labels: True(기본)면 층 라벨 표시 — verbose와 독립인 별도 축.
            layer_names 우선, 없으면 자동: <forward> / <1st backward> / <2nd backward> ...

    Returns:
        완성된 DOT 텍스트.
    """
    layers = _normalize_layers(start_vars)

    # ① 층별·서브그룹별 역순회 → 노드별 소속 (층 × 서브그룹) + 객체 + 간선 수집
    var_groups: dict[int, dict[int, set[int]]] = {}   # vid → {층 idx: {서브그룹 idx}}
    func_groups: dict[int, dict[int, set[int]]] = {}  # fid → {층 idx: {서브그룹 idx}}
    vars_by_id: dict[int, Variable] = {}
    funcs_by_id: dict[int, Function] = {}
    edges: set[tuple[int, int]] = set()

    def register_var(v: Variable, layer_idx: int, group_idx: int) -> None:
        vid = id(v)
        var_groups.setdefault(vid, {}).setdefault(layer_idx, set()).add(group_idx)
        vars_by_id[vid] = v

    for layer_idx, groups in enumerate(layers):
        for group_idx, group in enumerate(groups):
            for start_var in group:
                register_var(start_var, layer_idx, group_idx)

                for func in iter_reverse_topo(start_var):
                    fid = id(func)
                    func_groups.setdefault(fid, {}).setdefault(layer_idx, set()).add(group_idx)
                    funcs_by_id[fid] = func

                    output = func.output() if func.output else None
                    if output is not None:
                        register_var(output, layer_idx, group_idx)
                        edges.add((fid, id(output)))

                    if func.inputs:
                        for x in func.inputs:
                            register_var(x, layer_idx, group_idx)
                            edges.add((id(x), fid))

    # ② 배치 결정 — primary = 처음 등장한 층. 그 층에서의 소속 서브그룹이
    #    정확히 1개면 그 서브그룹 박스로, 2개 이상이면(공유 재료) 층 최상위로.
    var_cell: dict[int, tuple[int, int | None]] = {}   # vid → (층, 서브그룹 or None)
    func_cell: dict[int, tuple[int, int | None]] = {}

    for vid, groups_by_layer in var_groups.items():
        primary = min(groups_by_layer)
        members = groups_by_layer[primary]
        var_cell[vid] = (primary, next(iter(members)) if len(members) == 1 else None)

    for fid, groups_by_layer in func_groups.items():
        primary = min(groups_by_layer)
        members = groups_by_layer[primary]
        func_cell[fid] = (primary, next(iter(members)) if len(members) == 1 else None)

    # ③ DOT 조립 — 각 노드는 자기 배치에 딱 1번 (무복제)
    lines: list[str] = []

    for layer_idx in range(len(layers)):
        draw_subgroups = len(layers[layer_idx]) > 1

        lines.append(f'subgraph cluster_{layer_idx} {{\n')
        lines.append('  style = rounded;\n')
        lines.append('  color = lightgray;\n')

        # 층 라벨 — 내부 중앙 상단 (labeljust="c" + labelloc 기본 "t").
        # show_labels 독립 옵션 (verbose=shape/dtype와 분리 — 브로 결정):
        # layer_names 우선, 없으면 <forward> / <1st backward> ... 자동 (서수+앵글 브래킷).
        if show_labels:
            label = (
                layer_names[layer_idx] if layer_names
                else ('forward' if layer_idx == 0 else f'{_ordinal(layer_idx)} backward')
            )
            lines.append('  labeljust = c;\n')
            lines.append(f'  label = "< {label} >";\n')

        # (a) 층 최상위 — 공유 재료(서브그룹 2개 이상 소속) + 서브그룹 없는 층 전체
        for vid, (l, g) in var_cell.items():
            if l == layer_idx and (g is None or not draw_subgroups):
                seed = layer_idx > 0 and _is_seed(vars_by_id[vid])
                lines.append('  ' + _dot_var_node(vars_by_id[vid], verbose, show_value, value_format, is_seed=seed, array_show_value=array_show_value))

        for fid, (l, g) in func_cell.items():
            if l == layer_idx and (g is None or not draw_subgroups):
                lines.append('  ' + _dot_func_node(funcs_by_id[fid], verbose, show_value))

        # (b) 서브그룹 박스 — 각 그래디언트 성분/Hessian 행을 중첩 cluster로 구분.
        #     라벨은 없음 — 박스 안 노드들이 이미 무엇인지 보여주므로 (브로 취향).
        if draw_subgroups:
            for group_idx in range(len(layers[layer_idx])):
                lines.append(f'  subgraph cluster_{layer_idx}_{group_idx} {{\n')
                lines.append('    style = rounded;\n')
                lines.append('    color = gray62;\n')

                for vid, (l, g) in var_cell.items():
                    if l == layer_idx and g == group_idx:
                        seed = layer_idx > 0 and _is_seed(vars_by_id[vid])
                        lines.append('    ' + _dot_var_node(vars_by_id[vid], verbose, show_value, value_format, is_seed=seed, array_show_value=array_show_value))

                for fid, (l, g) in func_cell.items():
                    if l == layer_idx and g == group_idx:
                        lines.append('    ' + _dot_func_node(funcs_by_id[fid], verbose, show_value))

                lines.append('  }\n')

        lines.append('}\n')

    # 간선 — 실제 객체 id로 직결. 배치가 다른 박스(층 or 서브그룹)에 걸치면 점선.
    # (공유 노드 ↔ 서브그룹 연결은 같은 층 안이면 실선 — "공유 재료에서 흐름" 표현)
    cell = {**var_cell, **func_cell}
    for from_id, to_id in sorted(edges):
        l_from, g_from = cell[from_id]
        l_to, g_to = cell[to_id]
        crosses_boundary = (l_from != l_to) or (
            g_from is not None and g_to is not None and g_from != g_to
        )

        if crosses_boundary:
            lines.append(f'{from_id} -> {to_id} [style=dashed, color=dimgray]\n')
        else:
            lines.append(f'{from_id} -> {to_id}\n')

    return f'digraph g {{\n{"".join(lines)}}}'


def plot_multi_layer_graph(
    start_vars: "list[Variable | list[Variable] | list[list[Variable]]]",
    verbose: bool = True,
    show_value: bool = False,
    value_format: "str | None" = None,
    layer_names: "list[str] | None" = None,
    to_file: str = 'output/multi_layer.png',
    array_show_value: bool = True,
    show_labels: bool = True,
) -> str:
    """다층 계산 그래프를 DOT로 인코딩하여 Graphviz로 렌더링, 파일로 저장.

    Args:
        start_vars: 각 층의 시작점. 3종 (상세는 fold_multi_layer_dot_graph).
            단변수: [y, gx, gx2] / 다변수 자동: [z, [gx, gy]] /
            Hessian 행별: [z, [gx, gy], [[hxx, hyx], [hxy, hyy]]]
        verbose: True면 Variable 노드에 shape/dtype 추가 (노드 정적 정보).
        show_value: True면 Variable 노드에 값 추가.
        value_format: 값 포맷 스펙 (None이면 적응형 기본).
        layer_names: 각 층의 표시 이름 (주면 자동 라벨 대신 사용).
        to_file: 출력 파일 경로 (확장자가 렌더링 포맷 결정).
        array_show_value: show_value=True일 때 배열 값 표시 (True=요약 / False=shape만).
        show_labels: True(기본)면 층 라벨 — <forward> / <1st backward> ... 자동.

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
        start_vars, verbose, show_value, value_format, layer_names,
        array_show_value, show_labels
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
    array_show_value: bool = True,
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
        array_show_value: show_value=True일 때 배열 값 표시 (True=요약 / False=shape만).

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

    dot_graph = fold_dot_graph(output, verbose, show_value, value_format, array_show_value)

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
