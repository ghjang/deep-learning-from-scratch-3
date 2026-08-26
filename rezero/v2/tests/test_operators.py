"""rezero.v2 산술 연산자 테스트 — +, -, *, /, **, 단항 -, 역순.

step20~22에서 검증한 핵심 케이스를 pytest 스타일로 정리.
"""

from collections.abc import Callable

import numpy as np

from rezero.v2 import Variable, add, div, fill_grad, mul, neg, numerical_diff, pow, rdiv, rsub, sub


# ===== 교환법칙 O: +, * (step20) ===============================================
class TestCommutativeOperators:
    def test_add_variable_variable(self):
        """Variable + Variable."""
        a = Variable(np.array(3.0))
        b = Variable(np.array(2.0))
        assert (a + b).data == np.array(5.0)

    def test_mul_variable_variable(self):
        """Variable * Variable."""
        a = Variable(np.array(3.0))
        b = Variable(np.array(2.0))
        assert (a * b).data == np.array(6.0)

    def test_add_variable_scalar(self):
        """Variable + scalar (step21 as_variable)."""
        x = Variable(np.array(2.0))
        assert (x + 3.0).data == np.array(5.0)

    def test_mul_variable_scalar(self):
        """Variable * scalar."""
        x = Variable(np.array(2.0))
        assert (x * 3.0).data == np.array(6.0)

    def test_radd_scalar_variable(self):
        """scalar + Variable (step21 __radd__)."""
        x = Variable(np.array(2.0))
        assert (3.0 + x).data == np.array(5.0)

    def test_rmul_scalar_variable(self):
        """scalar * Variable (step21 __rmul__)."""
        x = Variable(np.array(2.0))
        assert (3.0 * x).data == np.array(6.0)

    def test_add_ndarray_variable(self):
        """ndarray + Variable (step21 — __array_priority__ 없이도 동작)."""
        x = Variable(np.array(2.0))
        y = np.array(3.0) + x
        assert isinstance(y, Variable)
        assert y.data == np.array(5.0)

    def test_mul_ndarray_variable(self):
        """ndarray * Variable."""
        x = Variable(np.array(2.0))
        y = np.array(3.0) * x
        assert isinstance(y, Variable)
        assert y.data == np.array(6.0)

    def test_operator_vs_wrapper(self):
        """연산자와 wrapper가 동일 동작 (step20)."""
        a = Variable(np.array(3.0))
        b = Variable(np.array(2.0))
        assert (a + b).data == add(a, b).data
        assert (a * b).data == mul(a, b).data


# ===== 단항 - (step22) =========================================================
class TestNegOperator:
    def test_neg(self):
        """단항 부호: -x."""
        x = Variable(np.array(2.0))
        assert (-x).data == np.array(-2.0)

    def test_neg_zero(self):
        """-0 = 0."""
        x = Variable(np.array(0.0))
        assert (-x).data == np.array(0.0)

    def test_neg_backward(self):
        """★ y = -x → dy/dx = -1 (상수) — step34 버그 회귀 테스트 (v1~v2 공통 버그).

        derivative가 -1 상수가 아니라 -1.0 * x (원 함수)를 반환해 x.grad = -x가
        되었음. sin 고차 미분 3차(Neg.backward 첫 호출 시점)에서 발견 (2026-08-24).
        """
        x = Variable(np.array(2.0))
        y = -x
        fill_grad(y)
        assert x.grad is not None
        assert x.grad.data == np.array(-1.0)   # -2.0이면 버그 재발

    def test_neg_backward_higher(self):
        """★ 상수 도함수의 재미분 — gx 그래프에 x가 없어 x.grad는 None.

        y = -x의 도함수는 상수 -1 → gx = -1·1 그래프의 리프는 ones뿐,
        원본 x로 가는 간선이 없다 → 재미분이 x에 도달 못 함.
        수학적으론 d²y/dx² = 0이지만 autodiff는 "연결 없음"으로 표현.
        dezero 정답지와 동일 동작 (실증 확인 2026-08-24).
        """
        x = Variable(np.array(3.0))
        y = -x
        fill_grad(y, create_graph=True)

        gx = x.grad
        assert gx is not None and gx.data is not None
        assert gx.data == np.array(-1.0)

        x.clear_grad()
        fill_grad(gx)
        assert x.grad is None   # 그래프 연결 없음 — 0이 아니라 None


# ===== 비교환: - (step22) =====================================================
class TestSubOperator:
    def test_sub_variable_variable(self):
        """Variable - Variable."""
        a = Variable(np.array(4.0))
        b = Variable(np.array(2.0))
        assert (a - b).data == np.array(2.0)

    def test_sub_variable_scalar(self):
        """Variable - scalar."""
        x = Variable(np.array(2.0))
        assert (x - 1.0).data == np.array(1.0)

    def test_rsub_scalar_variable(self):
        """scalar - Variable → rsub 순서 뒤집기."""
        x = Variable(np.array(2.0))
        assert (3.0 - x).data == np.array(1.0)

    def test_rsub_not_commutative(self):
        """Sub는 비교환 — x - y ≠ y - x."""
        x = Variable(np.array(5.0))
        y = Variable(np.array(2.0))
        assert (x - y).data != (y - x).data


# ===== 비교환: / (step22) =====================================================
class TestDivOperator:
    def test_div_variable_variable(self):
        """Variable / Variable."""
        a = Variable(np.array(6.0))
        b = Variable(np.array(2.0))
        assert (a / b).data == np.array(3.0)

    def test_div_variable_scalar(self):
        """Variable / scalar."""
        x = Variable(np.array(6.0))
        assert (x / 2.0).data == np.array(3.0)

    def test_rdiv_scalar_variable(self):
        """scalar / Variable → rdiv 순서 뒤집기."""
        x = Variable(np.array(2.0))
        assert (6.0 / x).data == np.array(3.0)

    def test_rdiv_not_commutative(self):
        """Div는 비교환."""
        x = Variable(np.array(6.0))
        y = Variable(np.array(2.0))
        assert (x / y).data != (y / x).data


# ===== 거듭제곱 ** (step22) ===================================================
class TestPowOperator:
    def test_pow_positive(self):
        """x ** 3 (양수 지수)."""
        x = Variable(np.array(2.0))
        assert (x ** 3).data == np.array(8.0)

    def test_pow_zero(self):
        """x ** 0 = 1."""
        x = Variable(np.array(2.0))
        assert (x ** 0).data == np.array(1.0)

    def test_pow_negative(self):
        """x ** -1 (음수 지수)."""
        x = Variable(np.array(2.0))
        assert (x ** -1).data == np.array(0.5)

    def test_pow_fraction(self):
        """x ** 0.5 (분수 지수)."""
        x = Variable(np.array(9.0))
        assert (x ** 0.5).data == np.array(3.0)

    def test_pow_backward(self):
        """★ x ** 3 역전파: dy/dx = 3·x² (step22 핵심 기대값)."""
        from rezero.v2 import fill_grad
        x = Variable(np.array(2.0))
        y = x ** 3
        fill_grad(y)
        assert x.grad is not None
        assert x.grad.data == np.array(12.0)   # 3 * 2² = 12


class TestNonCommutativeBackward:
    """★ 비교환 연산자 역전파 수치 검증 (step22 핵심 — 부호/크기)."""

    def test_sub_backward_signs(self):
        """z = x - y → ∂z/∂x=1, ∂z/∂y=-1 (Sub는 두 번째가 -1)."""
        from rezero.v2 import fill_grad
        x = Variable(np.array(4.0))
        y = Variable(np.array(2.0))
        z = x - y
        fill_grad(z)
        assert x.grad is not None
        assert x.grad.data == np.array(1.0)
        assert y.grad is not None
        assert y.grad.data == np.array(-1.0)   # ★ 음수

    def test_div_backward_values(self):
        """z = x / y → ∂z/∂x=1/y, ∂z/∂y=-x/y² (제곱 항)."""
        from rezero.v2 import fill_grad
        x = Variable(np.array(6.0))
        y = Variable(np.array(2.0))
        z = x / y
        fill_grad(z)
        assert x.grad is not None
        assert x.grad.data == np.array(0.5)     # 1/y = 1/2
        assert y.grad is not None
        assert y.grad.data == np.array(-1.5)    # -x/y² = -6/4 = -1.5


# ===== 복합 식 (step20~22) =====================================================
class TestCompoundExpressions:
    def test_a_mul_b_plus_c(self):
        """y = a * b + c (step20 핵심 데모)."""
        from rezero.v2 import fill_grad
        a = Variable(np.array(3.0))
        b = Variable(np.array(2.0))
        c = Variable(np.array(1.0))
        y = a * b + c
        fill_grad(y)
        assert y.data == np.array(7.0)
        assert a.grad is not None
        assert a.grad.data == np.array(2.0)   # ∂y/∂a = b
        assert b.grad is not None
        assert b.grad.data == np.array(3.0)   # ∂y/∂b = a
        assert c.grad is not None
        assert c.grad.data == np.array(1.0)   # ∂y/∂c

    def test_scalar_mul_add(self):
        """3.0 * x + 1.0 (step21 핵심 데모)."""
        from rezero.v2 import fill_grad
        x = Variable(np.array(2.0))
        y = 3.0 * x + 1.0
        fill_grad(y)
        assert y.data == np.array(7.0)

    def test_operator_precedence(self):
        """-x ** 2 = -(x²) (**가 단항 -보다 우선)."""
        x = Variable(np.array(3.0))
        assert (-x ** 2).data == np.array(-9.0)

    def test_complex_mixed(self):
        """y = a*b + a**2 - b/a + (-a) (step23 케이스 2)."""
        a = Variable(np.array(2.0))
        b = Variable(np.array(3.0))
        y = a * b + a ** 2 - b / a + (-a)
        # 6 + 4 - 1.5 - 2 = 6.5
        assert y.data == np.array(6.5)

    def test_wrapper_rsub_rdiv(self):
        """rsub/rdiv wrapper 직접 호출도 정상 동작."""
        x = Variable(np.array(2.0))
        assert rsub(x, 3.0).data == np.array(1.0)   # 3.0 - 2.0
        assert rdiv(x, 6.0).data == np.array(3.0)   # 6.0 / 2.0


# ===== gradient check — 전 연산자 도함수의 수치 검증 (작업 4) ====================
class TestOperatorGradientCheck:
    """★ 산술 연산자 도함수 gradient check — 해석(derivative hook) vs 수치 미분.

    step34 Neg 버그(2026-08-24 발견, v1 step22부터 은닉)의 교훈: 순전파만 검사하면
    도함수 버그가 은닉된다. 자명해 보이는 상수 도함수(1, -1)도 포함해 전 연산자를
    numerical_diff로 검증 — Div(제곱 항 포함, 가장 복잡)이 최우선 대상이었다.

    이변수 함수는 한쪽 입력을 고정한 클로저로 각 입력별 검증
    (test_autodiff.TestMultivariableBackward 패턴 재사용).
    """

    def test_add_both_inputs(self):
        """∂(x0+x1)/∂x0 = ∂(x0+x1)/∂x1 = 1 — 상수 도함수도 검증 대상."""
        x1 = Variable(np.array(1.3))
        x0_fixed = Variable(np.array(0.6))
        for a in (0.7, 2.0, -1.5):
            _assert_gradclose(lambda t: add(t, x1), a, f"add x0편 (a={a})")
            _assert_gradclose(lambda t: add(x0_fixed, t), a, f"add x1편 (a={a})")

    def test_mul_both_inputs(self):
        """∂(x0·x1)/∂x0 = x1, ∂(x0·x1)/∂x1 = x0 — 다른 입력 의존 도함수."""
        x1 = Variable(np.array(1.7))
        x0 = Variable(np.array(0.5))
        for a in (0.6, 2.0, -1.2):
            _assert_gradclose(lambda t: mul(t, x1), a, f"mul x0편 (a={a})")
            _assert_gradclose(lambda t: mul(x0, t), a, f"mul x1편 (a={a})")

    def test_sub_both_inputs(self):
        """∂(x0-x1)/∂x0 = 1, ∂(x0-x1)/∂x1 = -1 — 비교환, 부호까지 검증."""
        x1 = Variable(np.array(2.0))
        x0 = Variable(np.array(0.8))
        for a in (0.5, 3.0, -1.0):
            _assert_gradclose(lambda t: sub(t, x1), a, f"sub x0편 (a={a})")
            _assert_gradclose(lambda t: sub(x0, t), a, f"sub x1편 (a={a})")

    def test_div_both_inputs(self):
        """∂(x0/x1)/∂x0 = 1/x1, ∂(x0/x1)/∂x1 = -x0/x1² — 제곱 항, ★ 최우선."""
        x1 = Variable(np.array(1.7))
        x0 = Variable(np.array(2.5))
        for a in (0.6, 3.0, -1.2):
            _assert_gradclose(lambda t: div(t, x1), a, f"div x0편 (a={a})")
            _assert_gradclose(lambda t: div(x0, t), a, f"div x1편 (a={a})")

    def test_pow_exponents(self):
        """d(x^c)/dx = c·x^(c-1) — c=2, 3, 0.5 (0.5은 양수 점에서)."""
        _assert_gradclose(lambda t: pow(t, 2), 1.5, "pow c=2")
        _assert_gradclose(lambda t: pow(t, 3), -0.7, "pow c=3")
        _assert_gradclose(lambda t: pow(t, 0.5), 2.0, "pow c=0.5")


def _assert_gradclose(f: Callable[[Variable], Variable], x_val: float, label: str) -> None:
    """f의 해석 grad(x_val) ≈ 수치 미분 대조 (gradient check 1점, v2판)."""
    x = Variable(np.array(x_val))
    fill_grad(f(x))
    assert x.grad is not None
    assert x.grad.data is not None
    nd = numerical_diff(f, Variable(np.array(x_val)))
    assert np.isclose(x.grad.data, nd), f"{label}: analytic={x.grad.data} vs numeric={nd}"
