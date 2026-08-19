"""rezero.v1 수학 함수 테스트 — sin (step27~).

수학 함수 클래스(Sin 등)의 순전파 값 + 역전파 gradient check 검증.
산술 연산자(test_operators.py)와 분리 — 향후 exp/log 등도 이 파일에 추가.
"""

import numpy as np

from rezero.v1 import Variable, fill_grad, numerical_diff, sin


class TestSinForward:
    """sin 순전파 값 검증."""

    def test_sin_zero(self):
        """sin(0) = 0."""
        x = Variable(np.array(0.0))
        y = sin(x)
        assert y.data is not None
        assert y.data == np.array(0.0)

    def test_sin_pi_half(self):
        """sin(π/2) = 1."""
        x = Variable(np.array(np.pi / 2))
        y = sin(x)
        assert y.data is not None
        assert np.isclose(y.data, 1.0)

    def test_sin_pi_quarter(self):
        """sin(π/4) ≈ 0.7071."""
        x = Variable(np.array(np.pi / 4))
        y = sin(x)
        assert y.data is not None
        assert np.isclose(y.data, np.sin(np.pi / 4))


class TestSinBackward:
    """sin 역전파 검증 — derivative hook (cos)."""

    def test_grad_at_zero(self):
        """sin'(0) = cos(0) = 1."""
        x = Variable(np.array(0.0))
        y = sin(x)
        fill_grad(y)
        assert x.grad is not None
        assert np.isclose(x.grad, 1.0)

    def test_grad_at_pi_quarter(self):
        """sin'(π/4) = cos(π/4) ≈ 0.7071."""
        x = Variable(np.array(np.pi / 4))
        y = sin(x)
        fill_grad(y)
        assert x.grad is not None
        assert np.isclose(x.grad, np.cos(np.pi / 4))

    def test_gradient_check(self):
        """gradient check — 해석 역전파 vs 수치 미분 (v1 검증 국룰)."""
        x = Variable(np.array(np.pi / 4))
        y = sin(x)
        fill_grad(y)

        assert x.grad is not None
        nd = numerical_diff(sin, x)
        assert abs(x.grad - nd) < 1e-6
