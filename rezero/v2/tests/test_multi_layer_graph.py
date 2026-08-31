"""다층 계산 그래프 시각화 테스트 — 이슈 45 도구 검증 + 그래프 성장 실험.

실행: uv run pytest rezero/v2/tests/test_multi_layer_graph.py -v
PNG 생성 확인: output/ 폴더 (demo_x2_*.png)

노트 36 §8 "그래프는 항상 자란다"의 실측 근거.
"""

import numpy as np

from rezero.v2 import Variable, backprop
from rezero.v2.core import iter_reverse_topo
from rezero.v2.utils import fold_multi_layer_dot_graph


def _count_funcs(var: Variable) -> int:
    """Variable의 그래프에서 Function 노드 수 세기."""
    return sum(1 for _ in iter_reverse_topo(var))


def _build_x2_derivatives(x_val: float = 2.0, max_order: int = 4):
    """y = x²의 1~max_order계 미분 Variable 목록 생성."""
    x = Variable(np.array(x_val), name='x')
    y = x ** 2

    layers = [y]
    current = y
    for _ in range(max_order):
        x.clear_grad()
        backprop(current, create_graph=True)
        g = x.grad
        assert g is not None
        layers.append(g)
        current = g

    return layers


class TestMultiLayerGraphStructure:
    """DOT 구조 검증 — cluster 수, 공유 노드, 점선 참조."""

    def test_two_layers_produce_two_clusters(self):
        """[y, gx] 전달 → cluster 2개 생성."""
        layers = _build_x2_derivatives(max_order=1)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)
        assert dot.count('subgraph cluster_') == 2

    def test_five_layers_produce_five_clusters(self):
        """[y, gx, gx2, gx3, gx4] 전달 → cluster 5개."""
        layers = _build_x2_derivatives(max_order=4)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)
        assert dot.count('subgraph cluster_') == 4 + 1  # 순전파 + 4계

    def test_shared_variable_has_duplicate_and_dashed_reference(self):
        """공유 변수 x: 원본(cluster 안) + 복제(점선 테두리) + 점선 참조 간선."""
        layers = _build_x2_derivatives(max_order=1)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)

        # 점선 참조 간선 존재 (원본 → 복제)
        assert 'style=dashed' in dot
        # 복제 노드 스타일 (fillcolor=moccasin + 점선 테두리)
        assert 'fillcolor=moccasin' in dot

    def test_minimum_two_vars_required(self):
        """시작점 1개면 AssertionError."""
        x = Variable(np.array(1.0))
        y = x * x
        try:
            fold_multi_layer_dot_graph([y])
            assert False, 'Should have raised'
        except AssertionError:
            pass  # 예상된 에러


class TestGraphGrowthPattern:
    """그래프 성장 패턴 실측 — 노트 36 §8의 근거.

    x²의 값은 소멸 (4 → 4 → 2 → 0 → -0) 하지만
    그래프는 선형 성장 (+2 Function/계).
    """

    def test_values_diminish(self):
        """미분값: y=4, 1계=4, 2계=2, 3계=0."""
        layers = _build_x2_derivatives(max_order=3)
        expected = [4.0, 4.0, 2.0, 0.0]  # y, gx, gx2, gx3
        for var, exp in zip(layers, expected):
            assert var is not None and var.data is not None
            assert float(var.data) == exp

    def test_graph_grows_linearly(self):
        """Function 수: 1 → 3 → 5 → 7 → 9 (각 +2씩 선형 성장)."""
        layers = _build_x2_derivatives(max_order=4)
        counts = [_count_funcs(v) for v in layers]
        expected = [1, 3, 5, 7, 9]
        assert counts == expected

    def test_growth_is_constant_increment(self):
        """각 계층 간 성장량이 일정한지 (+2)."""
        layers = _build_x2_derivatives(max_order=4)
        counts = [_count_funcs(v) for v in layers]
        increments = [counts[i + 1] - counts[i] for i in range(len(counts) - 1)]
        assert all(d == 2 for d in increments), f'성장: {increments}'
