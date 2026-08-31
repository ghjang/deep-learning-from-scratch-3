"""backprop 별칭 테스트 — fill_grad와 동일 동작 + create_graph 경로 (이슈 49, 항목 041)."""

import numpy as np

from rezero.v2 import Variable, backprop, fill_grad


def test_backprop_same_grad_as_fill_grad():
    """두 이름 모두 같은 그래프에서 동일 grad 생산 — d(x**2)/dx = 2x."""
    for fn in (fill_grad, backprop):
        x = Variable(np.array(2.0))
        y = x ** 2

        fn(y)

        assert x.grad is not None
        assert x.grad.data == np.array(4.0)


def test_backprop_create_graph_double_backprop():
    """backprop의 create_graph=True → double backprop 경로 (AGENTS 예시 평행).

    gx = 2x라는 식(값 4.0)이므로 2차 미분은 d(2x)/dx = 2.0.
    """
    x = Variable(np.array(2.0))
    y = x ** 2

    backprop(y, create_graph=True)
    gx = x.grad  # Variable ("2x라는 식")
    assert gx is not None
    assert gx.data == np.array(4.0)

    x.clear_grad()
    backprop(gx)

    assert x.grad is not None
    assert x.grad.data == np.array(2.0)
