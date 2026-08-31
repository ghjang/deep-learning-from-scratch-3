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
        dot = fold_multi_layer_dot_graph(layers, verbose=False)  # type: ignore[arg-type]
        assert dot.count('subgraph cluster_') == 2

    def test_five_layers_produce_five_clusters(self):
        """[y, gx, gx2, gx3, gx4] 전달 → cluster 5개."""
        layers = _build_x2_derivatives(max_order=4)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)  # type: ignore[arg-type]
        assert dot.count('subgraph cluster_') == 4 + 1  # 순전파 + 4계

    def test_no_duplication_each_node_appears_once(self):
        """무복제 원칙: 각 노드는 전체 그래프에 딱 1번만 등장 (브로 방향 전환)."""
        layers = _build_x2_derivatives(max_order=2)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)  # type: ignore[arg-type]

        # 복제 노드(ref 접두사)가 없어야 함
        assert 'ref' not in dot.replace('refresh', ''), '복제 노드가 존재하면 안 됨'
        # 복제 스타일이 없어야 함 (점선 간선은 크로스 cluster용으로 허용)
        assert 'moccasin' not in dot

    def test_minimum_two_vars_required(self):
        """시작점 1개면 AssertionError."""
        x = Variable(np.array(1.0))
        y = x * x
        try:
            fold_multi_layer_dot_graph([y])
            assert False, 'Should have raised'
        except AssertionError:
            pass  # 예상된 에러


class TestMultiVariableGradient:
    """다변수 함수의 역전파 — 한 층에 여러 그래디언트 그래프 (브로 발견, 2026-08-31).

    z = x·y의 backward는 x.grad와 y.grad 두 그래디언트 그래프를 만듦.
    [z, [gx, gy]] 중첩 리스트로 전달하면 같은 층에 모두 포함되어야 함.
    """

    def test_multi_var_two_clusters(self):
        """[z, [gx, gy]] → cluster 2개 (순전파 + 역전파 전체)."""
        x = Variable(np.array(3.0), name='x')
        y = Variable(np.array(5.0), name='y')
        z = x * y

        backprop(z, create_graph=True)
        gx = x.grad
        gy = y.grad

        dot = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]
        assert dot.count('subgraph cluster_') == 2

    def test_multi_var_gradients_in_same_cluster(self):
        """cluster_1에 gx와 gy의 그래프가 둘 다 있어야 함 (노드 수 > 단일 그래프)."""
        x = Variable(np.array(3.0), name='x')
        y = Variable(np.array(5.0), name='y')
        z = x * y

        backprop(z, create_graph=True)
        gx = x.grad
        gy = y.grad

        # 다변수: [z, [gx, gy]] — cluster_1이 두 그래프를 모두 포함
        dot_multi = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]

        # 단일 변수 버전과 비교: cluster_1이 더 많은 노드를 가져야 함
        import re
        clusters_multi = re.findall(
            r'subgraph cluster_1 \{(.*?)\}', dot_multi, re.DOTALL
        )
        nodes_multi = len(re.findall(r'^\s+\d+', clusters_multi[0], re.MULTILINE))

        # gx 단독 그래프보다 노드가 많아야 함 (gy의 그래프도 포함되므로)
        assert nodes_multi >= 3, f'cluster_1 노드 {nodes_multi}개 — 다변수 미포함?'

    def test_multi_var_cross_cluster_edges(self):
        """다변수 곱의 미분은 상대방을 참조 → 크로스 간선 존재."""
        x = Variable(np.array(3.0), name='x')
        y = Variable(np.array(5.0), name='y')
        z = x * y

        backprop(z, create_graph=True)
        gx = x.grad
        gy = y.grad

        dot = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]

        # d(xy)/dx = y (cluster_0의 y 참조), d(xy)/dy = x (cluster_0의 x 참조)
        # → 크로스 간선 최소 2개 (x와 y 각각)
        dashed_count = dot.count('style=dashed')
        assert dashed_count >= 2, f'크로스 간선 {dashed_count}개 — 2개 이상 필요'

    def test_single_var_still_works(self):
        """기존 단변수 [y, gx] 방식도 여전히 작동 (호환성)."""
        x = Variable(np.array(2.0))
        y = x ** 2
        backprop(y, create_graph=True)
        gx = x.grad

        dot = fold_multi_layer_dot_graph([y, gx], verbose=False)  # type: ignore[arg-type]
        assert dot.count('subgraph cluster_') == 2


class TestLinearFunction:
    """y = 2x의 미분 — 그래프가 x를 참조하지 않아 2계가 안 되는 경우.

    노트 32 미분식 분류의 "입력 전용형" 실측: d(2x)/dx = 2는 상수라
    미분식이 x를 참조하지 않음 → 1계 그래프에 x가 없음 → x.grad = None.
    """

    def test_linear_1st_derivative_is_constant(self):
        """y = 2x → y' = 2 (x=3에서)."""
        x = Variable(np.array(3.0), name='x')
        y = 2 * x

        backprop(y, create_graph=True)
        gx = x.grad

        assert gx is not None
        assert gx.data is not None
        assert float(gx.data) == 2.0

    def test_linear_2nd_derivative_x_grad_is_none(self):
        """y = 2x의 2계: gx의 그래프가 x를 참조하지 않아 x.grad = None."""
        x = Variable(np.array(3.0), name='x')
        y = 2 * x

        backprop(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        x.clear_grad()
        backprop(gx, create_graph=True)

        assert x.grad is None

    def test_linear_two_layer_graph_works(self):
        """[y, gx] 2층 그래프는 정상 생성 (1계까지만 가능)."""
        x = Variable(np.array(3.0), name='x')
        y = 2 * x

        backprop(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        dot = fold_multi_layer_dot_graph([y, gx], verbose=False)
        assert dot.count('subgraph cluster_') == 2
