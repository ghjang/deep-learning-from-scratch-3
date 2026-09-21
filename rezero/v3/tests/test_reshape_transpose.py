"""rezero.v3 reshape/transpose 테스트 — step38 "형상 변환 함수".

형상 변환 (값 불변, shape만 이동) 검증:
  - 순전파: 값 보존 + shape 변경 (reshape) / 축 교환 (transpose)
  - 역전파: grad = ones(입력 shape) — "미분은 형상을 기억한다" (shape 왕복)
  - no-op 최적화: 같은 shape이면 노드 없이 x 자체 반환 (dezero 관례)
  - 메서드 스타일: x.reshape(6) / x.T — NumPy 관습 API (VariableShapeMixin)
  - gradient check: reshape은 함수값을 안 바꾸므로 합성 미분값도 불변
  - 2계 미분: backward가 모듈 함수를 호출 → 2층 그래프 연결 유지 (⑤형 계약)
  - view 공유: np.reshape이 view를 반환하는 문서화 canary (NumPy 동작 기록)
"""

import numpy as np

from rezero.v3 import Variable, fill_grad, numerical_diff, reshape, square, sum, transpose


class TestReshapeForward:
    """reshape 순전파 — 값 보존, shape 변경."""

    def test_reshape_values_preserved(self):
        """책 38단계 배열: (2,3) → (6,). 값은 순서대로, 하나도 안 바뀜."""
        x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
        y = reshape(x, (6,))

        assert y.data is not None
        assert y.data.shape == (6,)
        np.testing.assert_array_equal(y.data, np.arange(6.0))

    def test_reshape_roundtrip(self):
        """(2,3) → (6,) → (2,3): shape 왕복 — 최종 shape/값 모두 원본과 동일."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = reshape(reshape(x, (6,)), (2, 3))

        assert y.data is not None
        assert y.data.shape == (2, 3)
        np.testing.assert_array_equal(y.data, x.data)

    def test_reshape_order_preserved(self):
        """(2,3) → (6,) → (3,2): 최종 shape이 달라도 평탄화 순서(C-order) 보존."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = reshape(reshape(x, (6,)), (3, 2))

        assert y.data is not None
        assert y.data.shape == (3, 2)
        np.testing.assert_array_equal(y.data, np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]))


class TestReshapeBackward:
    """reshape 역전파 — grad = ones(입력 shape). "미분은 형상을 기억한다"."""

    def test_grad_ones_input_shape(self):
        """(2,3) → (6,)의 grad = ones(2,3) — 출력이 아니라 **입력** shape."""
        x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
        y = reshape(x, (6,))
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None
        assert x.grad.data.shape == (2, 3)
        np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))

    def test_grad_through_chain(self):
        """합성: sum(square(reshape(x))) — reshape은 함수값을 안 바꾸므로
        f = Σx²와 동일 → grad = 2x (reshape이 미분값에 영향 없음을 실증)."""
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())
        y = sum(square(reshape(x, (6,))))
        fill_grad(y)

        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_allclose(x.grad.data, 2.0 * data)

    def test_gradient_check(self):
        """수치 미분 대조 — 전 원소 동시 ±eps이므로 총합 비교 (test_sum 관례)."""
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())

        def f(t: Variable) -> Variable:
            return sum(square(reshape(t, (6,))))

        y = f(x)
        fill_grad(y)
        assert x.grad is not None and x.grad.data is not None

        numerical = numerical_diff(f, x)
        assert np.isclose(x.grad.data.sum(), numerical)

    def test_second_derivative(self):
        """2계 미분 — ⑤형 backward가 모듈 reshape()을 호출하는 계약 검증.

        f = Σ(reshape(x))²의 2계 도함수는 2 (reshape 투명성). raw np.reshape을
        썼다면 2층 그래프가 끊겨 재미분이 실패하거나 None이어야 함.
        """
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())
        y = sum(square(reshape(x, (6,))))

        fill_grad(y, create_graph=True)
        gx = x.grad
        assert gx is not None and gx.creator is not None

        # gx 캡처 후 clear_grad — 안 하면 누적(step14)으로 2x + 2가 됨 (이슈 43 D1)
        x.clear_grad()
        fill_grad(gx)  # 2차 미분
        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_allclose(x.grad.data, 2.0 * np.ones((2, 3)))


class TestReshapeNoop:
    """no-op 최적화 — 같은 shape이면 노드 없이 x 자체 반환."""

    def test_noop_returns_same_object(self):
        """reshape(x, x.shape) → y is x (동일 객체, creator도 없음)."""
        x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
        y = reshape(x, (2, 2))

        assert y is x
        assert y.creator is None

    def test_noop_midchain_backprop(self):
        """그래프 중간 no-op — 노드 없이도 역전파 정상, grad 동일.

        z = square(x); y = reshape(z, z.shape) → y is z. fill_grad(y)는
        z의 creator(체인)를 그대로 타고 내려간다.
        """
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())
        z = square(x)
        y = reshape(z, (2, 3))

        assert y is z
        assert y.creator is not None and type(y.creator).__name__ == "Square"

        fill_grad(y)
        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_allclose(x.grad.data, 2.0 * data)


class TestTransposeForward:
    """transpose 순전파 — 축 역순 (2차원: 행/열 교환)."""

    def test_transpose_2d(self):
        """(2,3) → (3,2). 행렬 전치 — 책 38단계 배열."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = transpose(x)

        assert y.data is not None
        assert y.data.shape == (3, 2)
        np.testing.assert_array_equal(y.data, np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]))

    def test_transpose_1d_identity(self):
        """1차원 전치는 identity — 역순으로 뒤집을 축이 없음."""
        x = Variable(np.array([1.0, 2.0, 3.0]))
        y = transpose(x)

        assert y.data is not None
        assert y.data.shape == (3,)
        np.testing.assert_array_equal(y.data, np.array([1.0, 2.0, 3.0]))


class TestTransposeBackward:
    """transpose 역전파 — grad = ones(입력 shape). 미분이 자기 자신 (involution)."""

    def test_grad_ones_input_shape(self):
        """(2,3) 전치의 grad = ones(2,3) — shape 왕복."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = transpose(x)
        fill_grad(y)

        assert x.grad is not None and x.grad.data is not None
        assert x.grad.data.shape == (2, 3)
        np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))

    def test_double_transpose_roundtrip(self):
        """전치의 전치 = 항등 (involution) — shape/값 원복, grad도 ones."""
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())
        y = transpose(transpose(x))

        assert y.data is not None
        assert y.data.shape == (2, 3)
        np.testing.assert_array_equal(y.data, data)

        fill_grad(y)
        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))

    def test_transpose_chain_grad(self):
        """합성: sum(square(transpose(x))) — 전치도 미분값 불변 (grad = 2x).

        square/sum이 element-wise·전체 합이라 transpose와 교환 — 형상 변환
        2종(reshape/transpose) 모두 "값 불변 → 미분값 불변"임을 함께 실증.
        """
        data = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        x = Variable(data.copy())
        y = sum(square(transpose(x)))
        fill_grad(y)

        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_allclose(x.grad.data, 2.0 * data)


class TestMethodStyle:
    """메서드/프로퍼티 스타일 — NumPy 관습 API (VariableShapeMixin)."""

    def test_reshape_method_flat_args(self):
        """x.reshape(6) — 가변 int 인자."""
        x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
        y = x.reshape(6)

        assert y.data is not None
        assert y.data.shape == (6,)

    def test_reshape_method_tuple_args(self):
        """x.reshape((6,)) — 단일 튜플 인자 (둘 다 같은 결과)."""
        x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
        y = x.reshape((6,))

        assert y.data is not None
        assert y.data.shape == (6,)
        np.testing.assert_array_equal(y.data, np.arange(6.0))

    def test_T_property(self):
        """x.T — 전치 프로퍼티 (정답지 데모 관례)."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = x.T

        assert y.data is not None
        assert y.data.shape == (3, 2)
        np.testing.assert_array_equal(y.data, np.array([[1.0, 4.0], [2.0, 5.0], [3.0, 6.0]]))

    def test_T_backward(self):
        """x.T의 grad = ones(입력 shape) — F.transpose와 동일 경로."""
        x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
        y = x.T
        fill_grad(y)

        assert x.grad is not None and x.grad.data is not None
        np.testing.assert_array_equal(x.grad.data, np.ones((2, 2)))


class TestViewSharing:
    """NumPy view 동작 기록 — 문서화 canary (rezero 동작이 아니라 NumPy 관찰).

    np.reshape은 가능하면 view를 반환 — y.data와 x.data가 같은 메모리 버퍼를
    공유할 수 있다 (Reshape 클래스 docstring 경고의 실증). rezero 전제
    (data 불변 사용)에서는 안전. 미래에 in-place가 등장하면 이 특성이 함경.
    """

    def test_contiguous_reshape_returns_view(self):
        """연속 배열의 reshape은 view — shares_memory True (관찰 기록)."""
        x = Variable(np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0]]))
        y = reshape(x, (6,))

        assert x.data is not None and y.data is not None
        assert np.shares_memory(x.data, y.data)
