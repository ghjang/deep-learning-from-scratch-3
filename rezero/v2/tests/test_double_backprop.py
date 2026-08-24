"""double backprop (고차 미분) 테스트 — step32의 본체 검증.

grad가 Variable이 된 것의 의미:
  - create_graph=True → 역전파가 그래프를 남김 → gx에 재역전파 가능
  - 기본 (False) → 그래프 안 남김 (lean) → gx는 creator 없는 순수 값
"""

import numpy as np
import pytest

from rezero.v2 import Variable, fill_grad, sin


class TestSecondDerivative:
    """2차 미분 (double backprop) — d/dx(dy/dx)."""

    def test_second_deriv_square(self):
        """y = x² → f' = 2x, f'' = 2. x=2에서 f''=2 — 책 검증 코드와 동일."""
        x = Variable(np.array(2.0))
        y = x ** 2
        fill_grad(y, create_graph=True)

        gx = x.grad
        assert gx is not None
        assert gx.data == np.array(4.0)   # f'(2) = 4 — 그래프 소유한 채

        x.clear_grad()
        fill_grad(gx)
        assert x.grad is not None
        assert x.grad.data == np.array(2.0)   # f''(2) = 2 ★ double backprop

    def test_second_deriv_pow4(self):
        """y = x⁴ → f' = 4x³, f'' = 12x². x=2에서 f''=48 — Pow 합성 경로."""
        x = Variable(np.array(2.0))
        y = x ** 4
        fill_grad(y, create_graph=True)

        gx = x.grad
        assert gx is not None
        assert gx.data == np.array(32.0)  # f'(2) = 32

        x.clear_grad()
        fill_grad(gx)
        assert x.grad is not None
        assert x.grad.data == np.array(48.0)   # f''(2) = 12·4 = 48

    def test_second_deriv_sin(self):
        """y = sin(x) → y' = cos(x), y'' = -sin(x). x=1에서 -sin(1) — Cos 경유."""
        x = Variable(np.array(1.0))
        y = sin(x)
        fill_grad(y, create_graph=True)

        gx = x.grad   # cos(1) — Sin.derivative가 cos 함수를 호출 (np.cos 아님)
        assert gx is not None
        assert gx.data is not None
        assert np.isclose(gx.data, np.cos(1.0))

        x.clear_grad()
        fill_grad(gx)
        assert x.grad is not None
        assert x.grad.data is not None
        assert np.isclose(x.grad.data, -np.sin(1.0))   # y'' = -sin(1)

    def test_third_deriv_pow4(self):
        """y = x⁴ → f''' = 24x. x=2에서 48 — 3층 그래프 (2차까지 create_graph)."""
        x = Variable(np.array(2.0))
        y = x ** 4
        fill_grad(y, create_graph=True)

        gx = x.grad                # 4x³ — 그래프 유
        assert gx is not None
        x.clear_grad()
        fill_grad(gx, create_graph=True)   # gx의 역전파도 그래프 남김!
        gxx = x.grad               # 12x² — 그래프 유
        assert gxx is not None
        assert gxx.data == np.array(48.0)

        x.clear_grad()
        fill_grad(gxx)             # f'''(2) = 24·2 = 48 (우연의 일치로 48)
        assert x.grad is not None
        assert x.grad.data == np.array(48.0)

    def test_second_deriv_composite(self):
        """y = (x²)² = x⁴ 합성 — Square 2층 경유의 2차 미분. f''(2) = 48."""
        from rezero.v2 import square

        x = Variable(np.array(2.0))
        y = square(square(x))
        fill_grad(y, create_graph=True)

        gx = x.grad
        assert gx is not None
        x.clear_grad()
        fill_grad(gx)
        assert x.grad is not None
        assert x.grad.data == np.array(48.0)


class TestCreateGraphDefault:
    """create_graph 기본값 (False) — lean 동작 확인."""

    def test_default_no_graph(self):
        """기본 fill_grad: gx는 그래프 없음 — 기억 상실 (lean)."""
        x = Variable(np.array(2.0))
        y = x ** 2
        fill_grad(y)   # create_graph 기본 False

        gx = x.grad
        assert gx is not None
        assert gx.data == np.array(4.0)
        assert gx.creator is None   # 그래프 없음 = 재미분 불가

    def test_gx_backward_without_graph_raises(self):
        """그래프 없는 gx에 fill_grad 호출 → RuntimeError (도입부 guard)."""
        x = Variable(np.array(2.0))
        y = x ** 2
        fill_grad(y)

        gx = x.grad
        assert gx is not None
        with pytest.raises(RuntimeError):
            fill_grad(gx)   # creator 없음 — "역전파할 계산 그래프가 없습니다"

    def test_grad_is_variable_type(self):
        """grad의 타입이 Variable (v1과의 결정적 차이)."""
        x = Variable(np.array(3.0))
        y = x ** 2
        fill_grad(y)
        assert isinstance(x.grad, Variable)


class TestGradientCheckStillWorks:
    """고차 미분 도입 후에도 1차 gradient check 유효 — 회귀 방어."""

    def test_gradient_check_square(self):
        """y = x² 해석(역전파) vs 수치 미분 — common numerical_diff 사용."""
        from rezero.v2 import numerical_diff, square

        for x_val in [0.5, 1.0, 2.0, -1.5]:
            x = Variable(np.array(x_val))
            y = square(x)
            fill_grad(y)
            nd = numerical_diff(square, Variable(np.array(x_val)))
            assert x.grad is not None
            assert x.grad.data is not None
            assert np.allclose(x.grad.data, nd)
