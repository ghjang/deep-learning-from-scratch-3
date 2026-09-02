"""rezero.v1 수학 함수 테스트 — sin (step27~).

수학 함수 클래스(Sin 등)의 순전파 값 + 역전파 gradient check 검증.
산술 연산자(test_operators.py)와 분리 — 향후 exp/log 등도 이 파일에 추가.
"""

import numpy as np

from rezero.v2 import Variable, fill_grad, numerical_diff, sin, tanh
from rezero.v2.functions import abs as rz_abs  # 내장 abs() 덮어쓰기 방지 — 별칭


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
        assert x.grad.data is not None
        assert np.isclose(x.grad.data, 1.0)

    def test_grad_at_pi_quarter(self):
        """sin'(π/4) = cos(π/4) ≈ 0.7071."""
        x = Variable(np.array(np.pi / 4))
        y = sin(x)
        fill_grad(y)
        assert x.grad is not None
        assert x.grad.data is not None
        assert np.isclose(x.grad.data, np.cos(np.pi / 4))

    def test_gradient_check(self):
        """gradient check — 해석 역전파 vs 수치 미분 (v1 검증 국룰)."""
        x = Variable(np.array(np.pi / 4))
        y = sin(x)
        fill_grad(y)

        assert x.grad is not None
        nd = numerical_diff(sin, x)
        assert abs(x.grad.data - nd) < 1e-6


# ===== Tanh (step35 — 자기 참조 도함수) ========================================
class TestTanh:
    def test_forward(self):
        """순전파: tanh(1.0)."""
        x = Variable(np.array(1.0))
        y = tanh(x)
        assert y.data is not None
        assert np.isclose(y.data, np.tanh(1.0))

    def test_gradient_check(self):
        """1차 미분 gradient check — 해석(1-tanh²) vs 수치."""
        for x_val in [0.5, 1.0, -0.8]:
            x = Variable(np.array(x_val))
            y = tanh(x)
            fill_grad(y)
            nd = numerical_diff(tanh, Variable(np.array(x_val)))
            assert x.grad is not None and x.grad.data is not None
            assert np.allclose(x.grad.data, nd)

    def test_second_deriv(self):
        """2차 미분: y'' = -2·tanh(x)·(1-tanh(x)²) — Tanh 재귀 노드 경유."""
        x = Variable(np.array(0.5))
        y = tanh(x)
        fill_grad(y, create_graph=True)

        gx = x.grad
        assert gx is not None and gx.data is not None
        assert np.isclose(gx.data, 1 - np.tanh(0.5) ** 2)   # y'

        x.clear_grad()
        fill_grad(gx)
        t = np.tanh(0.5)
        expected = -2 * t * (1 - t ** 2)                      # y''
        assert x.grad is not None and x.grad.data is not None
        assert np.isclose(x.grad.data, expected)


    def test_reuse_output_strategy(self):
        """★ 두 derivative 전략의 수치 동일성 (Config.reuse_output 스위치).

        ★ derivative는 역전파(fill_grad) 중 호출 — using_config 블록이
          fill_grad를 감싸야 효과가 있다 (순전파 시점 아님).
        """
        from rezero.v2 import using_config

        for x_val in [0.5, 1.0, -0.8]:
            for reuse in [False, True]:
                x = Variable(np.array(x_val))
                y = tanh(x)

                with using_config('reuse_output', reuse):
                    fill_grad(y, create_graph=True)

                    gx = x.grad
                    assert gx is not None and gx.data is not None
                    assert np.isclose(gx.data, 1 - np.tanh(x_val) ** 2)

                    x.clear_grad()
                    fill_grad(gx)

                t = np.tanh(x_val)
                expected = -2 * t * (1 - t ** 2)
                assert x.grad is not None and x.grad.data is not None
                assert np.isclose(x.grad.data, expected)

    def test_reuse_output_graph_compact(self):
        """★ 재사용형은 Tanh 노드 1개 유지 — 폭증 완화 실증 (탐구 노트 32)."""
        from rezero.v2 import using_config
        from rezero.v2.utils import fold_dot_graph

        x = Variable(np.array(1.0))
        y = tanh(x)

        with using_config('reuse_output', True):
            fill_grad(y, create_graph=True)

            for _ in range(3):   # 3번 재미분 — 블록 안의 역전파 전부 재사용형
                g = x.grad
                assert g is not None
                x.clear_grad()
                fill_grad(g, create_graph=True)

        final = x.grad
        assert final is not None
        d = fold_dot_graph(final, verbose=False)
        # show_param=False면 라벨은 'Tanh' — 재사용형은 3번 재미분해도 단 1개
        assert d.count('label="Tanh"') == 1


class TestAbs:
    """절댓값 — 부호 참조형 (이슈 45 투어 준비, 2026-09-02).

    미분 = sign(x), 값 참조 방식 (dezero ReLU 관례) — sign이 ndarray 값으로
    반환되어 x의 그래프와 무연결. 고차 미분에서의 운명이 관찰 포인트.
    """

    def test_forward(self):
        """|2| = 2, |-3| = 3."""
        y = rz_abs(Variable(np.array(2.0)))
        assert y.data is not None
        assert float(y.data) == 2.0

        y2 = rz_abs(Variable(np.array(-3.0)))
        assert y2.data is not None
        assert float(y2.data) == 3.0

    def test_dunder_abs(self):
        """Python 내장 abs()와 1:1 — __abs__ 던더 경유."""
        y = abs(Variable(np.array(-1.5)))  # 내장 abs → Variable.__abs__
        assert y.data is not None
        assert float(y.data) == 1.5

    def test_gradient_sign(self):
        """부호 참조: x>0이면 +1, x<0이면 -1 (출력이 아니라 입력의 부호를 봄)."""
        x = Variable(np.array(2.0))
        fill_grad(rz_abs(x))
        gx = x.grad
        assert gx is not None and gx.data is not None
        assert float(gx.data) == 1.0

        x2 = Variable(np.array(-2.0))
        fill_grad(rz_abs(x2))
        gx2 = x2.grad
        assert gx2 is not None and gx2.data is not None
        assert float(gx2.data) == -1.0

    def test_gradient_check(self):
        """numerical_diff와 일치 (x=1.5 — 특이점 0에서 충분히 먼 지점)."""
        x = Variable(np.array(1.5))
        fill_grad(rz_abs(x))
        gx = x.grad
        assert gx is not None and gx.data is not None
        approx = numerical_diff(rz_abs, x)
        assert abs(float(gx.data) - approx) < 1e-6

    def test_second_derivative_disconnected(self):
        """2계: 값 참조라 x가 gx 그래프에 없음 → x.grad = None (그래프 단절).

        노트 32 §3 'x 참조 여부가 고차 미분 가능성을 결정'의 부호 참조형 실증 —
        sign이 상수 복사(±1)라 2계 백프롭이 x에 도달하지 못한다.
        """
        x = Variable(np.array(2.0))
        fill_grad(rz_abs(x), create_graph=True)
        gx = x.grad
        assert gx is not None

        x.clear_grad()
        fill_grad(gx, create_graph=True)

        assert x.grad is None
