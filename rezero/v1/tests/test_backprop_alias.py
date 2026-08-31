"""backprop 별칭 테스트 — fill_grad와 동일 동작 (이슈 49, 항목 041)."""

import numpy as np

from rezero.v1 import Variable, backprop, fill_grad


def test_backprop_same_grad_as_fill_grad():
    """두 이름 모두 같은 그래프에서 동일 grad 생산 — d(x*x + x)/dx = 2x+1."""
    for fn in (fill_grad, backprop):
        x = Variable(np.array(2.0))
        y = x * x + x

        fn(y)

        assert x.grad == np.array(5.0)


def test_backprop_upstream_grad_passthrough():
    """upstream_grad 전달도 동일 — 10배 씨앗이면 grad도 10배."""
    for fn in (fill_grad, backprop):
        x = Variable(np.array(3.0))
        y = x * x

        fn(y, upstream_grad=np.array(10.0))

        assert x.grad == np.array(60.0)  # 2x * 10 = 60
