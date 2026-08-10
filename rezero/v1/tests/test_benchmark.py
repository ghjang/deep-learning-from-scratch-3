"""rezero.v1 응용 레벨 테스트 — 복잡한 합성 함수 역전파 검증.

step24 최적화 벤치마크 함수(Sphere/Matyas/Goldstein-Price)로 v1 역전파 압력 테스트.
★ 함수 정의 자체는 steps/step24.py에 (v1 패키지 핵심 아님).
  이 테스트는 "복잡한 응용에서도 v1 역전파가 정확한지" 검증이 목적.
"""

import os
import sys

import numpy as np

# step24.py에서 벤치마크 함수 import (steps/에 정의됨)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'rezero', 'steps'))
from step24 import sphere, matyas, goldstein  # type: ignore[import-not-found] # noqa: E402

from rezero.v1 import Variable, fill_grad, numerical_diff  # noqa: E402


def _grad_close(x: Variable, nd: np.ndarray, atol: float = 1e-5) -> None:
    """x.grad vs nd 비교 헬퍼 (pyright Optional 가드 포함)."""
    assert x.grad is not None
    assert np.allclose(x.grad, nd, atol=atol)


class TestSphere:
    """Sphere 함수: z = x² + y². 가장 단순한 볼록 함수."""

    def test_value_at_1_1(self):
        """Sphere(1,1) = 2."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = sphere(x, y)
        assert z.data == np.array(2.0)

    def test_gradient_at_1_1(self):
        """Sphere(1,1) grad = (2, 2) = (2x, 2y)."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = sphere(x, y)
        fill_grad(z)
        assert x.grad == np.array(2.0)
        assert y.grad == np.array(2.0)

    def test_minimum_at_origin(self):
        """★ (0,0)이 전역 최솟값 — z=0, grad=(0,0). 경사하강법이 찾아야 할 점."""
        x = Variable(np.array(0.0))
        y = Variable(np.array(0.0))
        z = sphere(x, y)
        fill_grad(z)
        assert z.data == np.array(0.0)
        assert x.grad == np.array(0.0)
        assert y.grad == np.array(0.0)

    def test_gradient_check(self):
        """★ gradient check — 해석 역전파 vs 수치 미분."""
        x = Variable(np.array(1.5))
        y = Variable(np.array(0.5))
        z = sphere(x, y)
        fill_grad(z)
        f_x = lambda t: sphere(t, Variable(np.array(0.5)))
        nd = numerical_diff(f_x, x)
        _grad_close(x, nd)


class TestMatyas:
    """Matyas 함수: z = 0.26(x²+y²) - 0.48xy."""

    def test_value_at_1_1(self):
        """Matyas(1,1) = 0.04 = 0.26*2 - 0.48."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = matyas(x, y)
        assert np.allclose(z.data, np.array(0.04))

    def test_gradient_at_1_1(self):
        """Matyas(1,1) grad = (0.04, 0.04). dz/dx = 0.52x - 0.48y."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = matyas(x, y)
        fill_grad(z)
        assert x.grad is not None and np.allclose(x.grad, np.array(0.04))
        assert y.grad is not None and np.allclose(y.grad, np.array(0.04))   # 대칭

    def test_gradient_symmetric(self):
        """Matyas는 x,y 대칭 — 같은 값이면 grad도 같음."""
        x = Variable(np.array(2.0))
        y = Variable(np.array(2.0))
        z = matyas(x, y)
        fill_grad(z)
        assert x.grad is not None and y.grad is not None
        assert np.allclose(x.grad, y.grad)

    def test_gradient_check(self):
        """★ gradient check."""
        x = Variable(np.array(1.5))
        y = Variable(np.array(0.5))
        z = matyas(x, y)
        fill_grad(z)
        f_x = lambda t: matyas(t, Variable(np.array(0.5)))
        nd = numerical_diff(f_x, x)
        _grad_close(x, nd)


class TestGoldstein:
    """Goldstein-Price 함수: 복잡한 두 다항식 곱. 비볼록, 많은 지역 최솟값."""

    def test_value_at_1_1(self):
        """Goldstein(1,1) = 1876 (정답지에서 확인한 값)."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = goldstein(x, y)
        assert z.data == np.array(1876.0)

    def test_gradient_at_1_1(self):
        """★ Goldstein(1,1) grad = (-5376, 8064). 정답지와 일치 (step24 핵심 검증)."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = goldstein(x, y)
        fill_grad(z)
        assert x.grad == np.array(-5376.0)
        assert y.grad == np.array(8064.0)

    def test_gradient_check(self):
        """★ gradient check — 가장 복잡한 함수로 v1 역전파 압력 테스트."""
        x = Variable(np.array(1.0))
        y = Variable(np.array(1.0))
        z = goldstein(x, y)
        fill_grad(z)
        f_x = lambda t: goldstein(t, Variable(np.array(1.0)))
        nd = numerical_diff(f_x, x)
        _grad_close(x, nd, atol=1e-3)

    def test_gradient_check_multiple_points(self):
        """★ 여러 점에서 gradient check — 비볼록 함수 신뢰성."""
        test_points = [(0.5, 0.5), (-0.5, -0.5), (0.0, -1.0)]
        for x_val, y_val in test_points:
            x = Variable(np.array(x_val))
            y = Variable(np.array(y_val))
            z = goldstein(x, y)
            fill_grad(z)
            f_x = lambda t, yv=y_val: goldstein(t, Variable(np.array(yv)))
            nd = numerical_diff(f_x, x)
            _grad_close(x, nd, atol=1e-3)
