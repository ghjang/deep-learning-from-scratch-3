"""다층 계산 그래프 시각화 테스트 — 이슈 45 도구 검증 + 그래프 성장 실험.

실행: uv run pytest rezero/v2/tests/test_multi_layer_graph.py -v
PNG 생성 확인: output/ 폴더 (demo_x2_*.png)

노트 36 §8 "그래프는 항상 자란다"의 실측 근거.
"""

import numpy as np

from rezero.v2 import Variable, backprop
from rezero.v2.core import iter_reverse_topo
from rezero.v2.functions import cos, sin
from rezero.v2.utils import _format_data, fold_multi_layer_dot_graph


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
    2026-09-02 서브그룹핑: 각 Variable이 서브그룹 박스(cluster_1_0/1_1)로 구분됨.
    """

    def _build_xy(self):
        x = Variable(np.array(3.0), name='x')
        y = Variable(np.array(5.0), name='y')
        z = x * y
        backprop(z, create_graph=True)
        return x, y, z, x.grad, y.grad

    def test_multi_var_two_clusters(self):
        """[z, [gx, gy]] → 층 cluster 2개 + 서브그룹 박스 2개 = subgraph 4개."""
        _, _, z, gx, gy = self._build_xy()

        dot = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]
        assert dot.count('subgraph cluster_') == 2 + 2  # 층 2 + 서브그룹 2

    def test_multi_var_gradients_in_same_cluster(self):
        """cluster_1 안에 gx박스(cluster_1_0) + gy박스(cluster_1_1)가 둘 다 있어야 함."""
        _, _, z, gx, gy = self._build_xy()

        dot = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]
        assert 'cluster_1_0' in dot, 'gx 서브그룹 박스 없음'
        assert 'cluster_1_1' in dot, 'gy 서브그룹 박스 없음'

        # 각 서브그룹 박스 안에 노드가 최소 1개씩 있어야 함
        import re
        for sub in ('cluster_1_0', 'cluster_1_1'):
            block = re.search(
                rf'subgraph {sub} \{{(.*?)\}}\n', dot, re.DOTALL
            )
            assert block is not None, f'{sub} 블록 파싱 실패'
            nodes = len(re.findall(r'^\s+\d+ \[', block.group(1), re.MULTILINE))
            assert nodes >= 1, f'{sub}에 노드 {nodes}개 — 그래프 미포함?'

    def test_multi_var_cross_cluster_edges(self):
        """다변수 곱의 미분은 상대방을 참조 → 크로스 간선 존재."""
        _, _, z, gx, gy = self._build_xy()

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


def _subgroup_spans(dot: str) -> list[tuple[int, int]]:
    """cluster_{layer}_{group} 서브그룹 블록의 (시작, 끝) 라인 범위 목록.

    층 cluster_{n} (밑줄 1개)와 구분하기 위해 이름 성분 수로 판별.
    """
    spans = []
    lines = dot.splitlines()

    for i, line in enumerate(lines):
        s = line.strip()
        if not s.startswith('subgraph cluster_'):
            continue

        name = s[len('subgraph '):].rstrip(' {').strip()
        if len(name.split('_')) != 3:  # cluster, layer, group
            continue

        depth = 0
        for j in range(i, len(lines)):
            depth += lines[j].count('{') - lines[j].count('}')
            if depth == 0:
                spans.append((i, j))
                break

    return spans


class TestFormatData:
    """show_value의 배열 대응 (책 관례 정렬 + rezero 옵션 계약 이행, 2026-09-02).

    스칼라는 값 그대로, 배열은 앞 4개 요약 + shape — 책은 배열 값을
    표시하지 않지만 show_value 옵션의 "값을 보여준다" 계약은 배열도 이행.
    """

    def test_scalar_unchanged(self):
        """스칼라(ndim=0)는 기존 _format_value 동작 그대로."""
        assert _format_data(np.array(5.0)) == '5'
        assert _format_data(np.array(0.0)) == '0'

    def test_short_vector_all_shown(self):
        """4개 이하 벡터는 전부 표시 + shape, 생략 없음."""
        assert _format_data(np.array([1.0, 2.0])) == '[1, 2] (2,)'

    def test_long_vector_summarized(self):
        """5개 이상 벡터는 앞 4개 + '...' + shape."""
        result = _format_data(np.arange(10.0))
        assert result == '[0, 1, 2, 3, ...] (10,)'

    def test_matrix_flattened_with_shape(self):
        """2D 배열도 ravel 요약 + 원 shape 표시."""
        result = _format_data(np.ones((2, 3)))
        assert result == '[1, 1, 1, 1, ...] (2, 3)'

    def test_shape_only_mode(self):
        """show_array=False — 배열은 값 없이 shape만 (책 관례 절제 모드)."""
        result = _format_data(np.arange(10.0), show_array=False)
        assert result == '(10,)'

    def test_shape_only_keeps_scalar_value(self):
        """show_array=False여도 스칼라 값은 유지 (절제는 배열에만 적용)."""
        assert _format_data(np.array(7.0), show_array=False) == '7'


    def test_auto_layer_labels_default(self):
        """show_labels 기본 True — [forward]/[1st backward] 자동 (verbose와 독립, 중앙 상단)."""
        x = Variable(np.array(2.0), name='x')
        y = x ** 2
        backprop(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        dot = fold_multi_layer_dot_graph([y, gx], verbose=False)
        assert 'labeljust = c' in dot
        assert 'label = "< forward >"' in dot
        assert 'label = "< 1st backward >"' in dot

    def test_auto_layer_labels_ordinal(self):
        """2계까지 — < 2nd backward > 서수 표기."""
        layers = _build_x2_derivatives(max_order=2)
        dot = fold_multi_layer_dot_graph(layers, verbose=False)  # type: ignore[arg-type]
        assert 'label = "< 2nd backward >"' in dot

    def test_show_labels_false(self):
        """show_labels=False → 층 라벨 없음."""
        x = Variable(np.array(2.0), name='x')
        y = x ** 2
        backprop(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        dot = fold_multi_layer_dot_graph([y, gx], verbose=False, show_labels=False)
        assert 'forward' not in dot
        assert 'backward' not in dot


class TestSubgroupLayout:
    """층 내 서브그룹핑 (브로 아이디어, 2026-09-02 — 이슈 45).

    다변수 층의 그래프는 성분별(1계)·Hessian 행별(2계) 덩어리가 섞여 보임 →
    중첩 cluster로 구분. 공유 노드(seed 등)는 서브그룹 밖 층 최상위에 배치.
    """

    def _build_xy(self):
        x = Variable(np.array(3.0), name='x')
        y = Variable(np.array(5.0), name='y')
        z = x * y
        backprop(z, create_graph=True)
        return x, y, z, x.grad, y.grad

    def test_shared_seed_outside_subgroups(self):
        """seed는 gx·gy 양쪽의 공통 재료 → 서브그룹 밖(cluster_1 최상위)에 배치."""
        _, _, z, gx, gy = self._build_xy()

        dot = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]
        lines = dot.splitlines()

        seed_lines = [i for i, line in enumerate(lines) if 'seed' in line]
        assert seed_lines, 'seed 노드가 그래프에 없음'

        for start, end in _subgroup_spans(dot):
            for sl in seed_lines:
                assert not (start <= sl <= end), (
                    f'seed(라인 {sl})가 서브그룹 블록 ({start}~{end}) 안에 있음 — '
                    '공유 재료는 층 최상위여야 함'
                )

    def test_single_group_layer_omits_subgroup_box(self):
        """서브그룹 1개뿐인 층은 하위 박스를 그리지 않음 (불필요한 중첩 방지)."""
        x = Variable(np.array(2.0), name='x')
        y = x ** 2
        backprop(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        dot = fold_multi_layer_dot_graph([y, gx], verbose=False)
        assert 'cluster_0_' not in dot, '서브그룹 1개 층에 하위 박스가 그려짐'
        assert 'cluster_1_' not in dot

    def test_hessian_row_grouping(self):
        """sin(x)·cos(y) 2계 — 중첩 리스트로 Hessian 행별 서브그룹.

        [z, [gx, gy], [[hxx, hyx], [hxy, hyy]]] → cluster_2 안에
        x행 박스(cluster_2_0) + y행 박스(cluster_2_1).
        """
        x = Variable(np.array(1.0), name='x')
        y = Variable(np.array(2.0), name='y')
        z = sin(x) * cos(y)

        backprop(z, create_graph=True)
        gx, gy = x.grad, y.grad
        assert gx is not None and gy is not None

        # x행: backprop(gx) → x.grad = ∂²z/∂x², y.grad = ∂²z/∂y∂x
        x.clear_grad(); y.clear_grad()
        backprop(gx, create_graph=True)
        hxx, hyx = x.grad, y.grad

        # y행: backprop(gy) → x.grad = ∂²z/∂x∂y, y.grad = ∂²z/∂y²
        x.clear_grad(); y.clear_grad()
        backprop(gy, create_graph=True)
        hxy, hyy = x.grad, y.grad

        # 4성분 전부 계산되는지 — sin·cos는 미분식이 x·y 둘 다 참조하므로 기대
        assert hxx is not None and hyx is not None
        assert hxy is not None and hyy is not None

        layers = [z, [[gx], [gy]], [[hxx, hyx], [hxy, hyy]]]
        dot = fold_multi_layer_dot_graph(layers, verbose=False)  # type: ignore[arg-type]

        assert 'cluster_1_0' in dot and 'cluster_1_1' in dot  # 1계: gx박스 + gy박스
        assert 'cluster_2_0' in dot and 'cluster_2_1' in dot  # 2계: x행 + y행
        assert dot.count('subgraph cluster_') == 3 + 4  # 층 3 + 서브그룹 2+2

    def test_flat_list_equals_auto_subgroups(self):
        """[z, [gx, gy]] (자동)와 [z, [[gx], [gy]]] (명시)는 같은 구조 생성."""
        _, _, z, gx, gy = self._build_xy()

        dot_auto = fold_multi_layer_dot_graph([z, [gx, gy]], verbose=False)  # type: ignore[arg-type]
        dot_explicit = fold_multi_layer_dot_graph([z, [[gx], [gy]]], verbose=False)  # type: ignore[arg-type]

        assert dot_auto == dot_explicit
