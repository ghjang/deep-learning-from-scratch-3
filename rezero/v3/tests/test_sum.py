"""rezero.v3 Sum 함수 테스트 — step37 "텐서를 다루다".

텐서(다차원 ndarray)의 sum 축소 검증:
  - 순전파: 전체 원소 합 → 0-dim
  - 역전파: 도함수 ones + 곱셈 브로드캐스팅으로 shape 복원
  - gradient check: numerical_diff 총합 대조 (모든 원소 ±eps 동시 이동이므로
    결과는 원소별 미분계수의 총합 — x.grad.data.sum()과 비교)
  - 2계 미분: 값 참조 갈래(ones)의 2계 소멸 특성 — d²sum(x²)/dx² = 2
  - 텐서 통과: 기존 element-wise 연산이 다차원에서 무수정 동작 (step37 본질)
"""

import numpy as np

from rezero.v3 import Variable, fill_grad, numerical_diff, sin, sum


class TestSumForward:
    """sum 순전파 값 검증 — 전체 원소 합, 0-dim 출력."""

    def test_sum_scalar(self):
        """0-dim 입력: sum(x) = x 그 자체 (0-dim 유지)."""
        x = Variable(np.array(3.0))
        y = sum(x)
        assert y.data is not None
        assert np.isclose(y.data, 3.0)
        assert y.data.ndim == 0

    def test_sum_vector(self):
        """1차원: [1, 2, 3] → 6."""
        x = Variable(np.array([1.0, 2.0, 3.0]))
        y = sum(x)
        assert y.data is not None
        assert np.isclose(y.data, 6.0)

    def test_sum_matrix(self):
        """2차원 (책 step37 배열): [[1,2,3],[4,5,6]] → 21."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = sum(x)
        assert y.data is not None
        assert np.isclose(y.data, 21.0)

    def test_sum_matches_numpy(self):
        """ndarray.sum()과 값 일치."""
        data = np.random.rand(3, 4)
        y = sum(Variable(data))
        assert y.data is not None
        assert np.isclose(y.data, data.sum())


class TestSumBackward:
    """sum 역전파 검증 — ∂(Σx_i)/∂x_i = 1, 브로드캐스팅 shape 복원."""

    def test_grad_ones_matrix(self):
        """2x3 텐서의 grad = ones(2,3) — 0-dim upstream이 shape 복원."""
        x = Variable(np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]))
        y = sum(x)
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None
        assert x.grad.data.shape == (2, 3)
        np.testing.assert_array_equal(x.grad.data, np.ones((2, 3)))

    def test_grad_ones_vector(self):
        """1차원 (4,)의 grad = ones(4)."""
        x = Variable(np.array([1.0, -2.0, 3.0, -4.0]))
        y = sum(x)
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None
        assert x.grad.data.shape == (4,)
        np.testing.assert_array_equal(x.grad.data, np.ones(4))

    def test_grad_type_is_variable_not_object_array(self):
        """grad.data가 ndarray(float) — NumPy 우선 object 배열 오염 방지 회귀.

        step37 발견 버그: 다차원 ndarray 도함수(ones)를 정규화 없이 곱하면
        NumPy가 element-wise를 이겨 object 배열이 됨 (as_variable 정규화로 해결).
        """
        x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
        y = sum(x)
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None
        assert x.grad.data.dtype != np.dtype(object)

    def test_grad_is_variable(self):
        """x.grad는 Variable (v2/v3 계약) — .data 접근으로 ndarray."""
        x = Variable(np.array([1.0, 2.0]))
        y = sum(x)
        fill_grad(y)

        assert x.grad is not None
        assert isinstance(x.grad, Variable)


class TestSumGradientCheck:
    """gradient check — 해석 역전파 vs 수치 미분 (총합 대조).

    numerical_diff는 모든 원소를 동시에 ±eps 흔들므로 결과는 원소별
    미분계수의 총합. backward의 x.grad.data.sum()과 비교해 교차 검증.
    """

    def test_sum_of_squares_matrix(self):
        """f = sum(x²) → x.grad = 2x → 총합 sum(2x)."""

        def f(t: Variable) -> Variable:
            return sum(t * t)

        x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
        y = f(x)
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None

        analytic_total = x.grad.data.sum()
        numeric_total = numerical_diff(f, x)
        assert np.isclose(analytic_total, numeric_total, rtol=1e-5)

    def test_sum_of_sin_matrix(self):
        """f = sum(sin(x)) → x.grad = cos(x) → 총합 sum(cos(x))."""

        def f(t: Variable) -> Variable:
            return sum(sin(t))

        x = Variable(np.array([[0.1, 0.2], [0.3, 0.4]]))
        y = f(x)
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None

        analytic_total = x.grad.data.sum()
        numeric_total = numerical_diff(f, x)
        assert np.isclose(analytic_total, numeric_total, rtol=1e-5)


class TestSumDoubleBackprop:
    """sum의 2계 미분 — 값 참조 갈래(ones)의 2계 소멸 특성."""

    def test_second_derivative_of_sum_of_squares(self):
        """d²sum(x²)/dx² = 2 (각 원소) — Mul(x·x) 갈래만 살아남음.

        Sum의 도함수 ones는 리프(그래프 무연결)라 2계에서 이 갈래는 소멸.
        2를 주는 건 오직 x²의 이계도함수 — Abs와 동일 특성의 텐서판.
        """
        x = Variable(np.array([[1.0, 2.0], [3.0, 4.0]]))
        y = sum(x * x)

        fill_grad(y, create_graph=True)
        gx = x.grad
        assert gx is not None

        x.clear_grad()
        fill_grad(gx)

        assert x.grad is not None
        assert x.grad.data is not None
        np.testing.assert_allclose(x.grad.data, np.full((2, 2), 2.0))


class TestTensorPassThrough:
    """step37 본질 회귀 — 기존 element-wise 연산이 텐서에서 무수정 동작."""

    def test_square_on_matrix(self):
        """x²의 텐서 grad = 2x (shape 유지)."""
        data = np.array([[1.0, 2.0], [3.0, 4.0]])
        x = Variable(data)
        y = x ** 2
        fill_grad(y)

        assert x.grad is not None
        assert x.grad.data is not None
        assert x.grad.data.shape == (2, 2)
        np.testing.assert_allclose(x.grad.data, 2 * data)

    def test_mul_on_matrix(self):
        """x * c (텐서×텐서)의 grad = c / x — 양쪽 다 shape 유지."""
        x_data = np.array([[1.0, 2.0], [3.0, 4.0]])
        c_data = np.array([[10.0, 20.0], [30.0, 40.0]])
        x = Variable(x_data)
        c = Variable(c_data)
        y = x * c
        fill_grad(y)

        assert x.grad is not None and x.grad.data is not None
        assert c.grad is not None and c.grad.data is not None
        np.testing.assert_allclose(x.grad.data, c_data)
        np.testing.assert_allclose(c.grad.data, x_data)

    def test_add_on_matrix_retain_grad(self):
        """정답지 step37.py 재현 — t = x + c → sum → retain_grad 관찰."""
        x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
        c = Variable(np.array([[10, 20, 30], [40, 50, 60]]))
        t = x + c
        y = sum(t)
        fill_grad(y, retain_grad=True)

        ones = np.ones((2, 3))
        assert y.grad is not None and y.grad.data is not None
        assert t.grad is not None and t.grad.data is not None
        assert x.grad is not None and x.grad.data is not None
        assert c.grad is not None and c.grad.data is not None

        np.testing.assert_array_equal(y.grad.data, np.array(1.0))
        np.testing.assert_array_equal(t.grad.data, ones)
        np.testing.assert_array_equal(x.grad.data, ones)
        np.testing.assert_array_equal(c.grad.data, ones)
