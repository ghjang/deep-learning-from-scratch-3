"""rezero.v1 산술 연산자 테스트 — +, -, *, /, **, 단항 -, 역순.

step20~22에서 검증한 핵심 케이스를 pytest 스타일로 정리.
"""

import numpy as np

from rezero.v1 import Variable, add, div, fill_grad, mul, neg, pow, rdiv, rsub, sub


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
        """★ y = -x → dy/dx = -1 (상수) — step34 버그 회귀 테스트.

        버그 이력: derivative가 -1 상수가 아니라 -1.0 * x (원 함수)를
        반환해 x.grad = -x가 되었음. sin 고차 미분 3차에서 발견 (2026-08-24).
        (2차 미분 검증은 v2 tests — v1은 create_graph 미지원)
        """
        x = Variable(np.array(2.0))
        y = -x
        fill_grad(y)
        assert x.grad is not None
        assert x.grad == np.array(-1.0)   # -2.0이면 버그 재발


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
        from rezero.v1 import fill_grad
        x = Variable(np.array(2.0))
        y = x ** 3
        fill_grad(y)
        assert x.grad == np.array(12.0)   # 3 * 2² = 12


class TestNonCommutativeBackward:
    """★ 비교환 연산자 역전파 수치 검증 (step22 핵심 — 부호/크기)."""

    def test_sub_backward_signs(self):
        """z = x - y → ∂z/∂x=1, ∂z/∂y=-1 (Sub는 두 번째가 -1)."""
        from rezero.v1 import fill_grad
        x = Variable(np.array(4.0))
        y = Variable(np.array(2.0))
        z = x - y
        fill_grad(z)
        assert x.grad == np.array(1.0)
        assert y.grad == np.array(-1.0)   # ★ 음수

    def test_div_backward_values(self):
        """z = x / y → ∂z/∂x=1/y, ∂z/∂y=-x/y² (제곱 항)."""
        from rezero.v1 import fill_grad
        x = Variable(np.array(6.0))
        y = Variable(np.array(2.0))
        z = x / y
        fill_grad(z)
        assert x.grad == np.array(0.5)     # 1/y = 1/2
        assert y.grad == np.array(-1.5)    # -x/y² = -6/4 = -1.5


# ===== 복합 식 (step20~22) =====================================================
class TestCompoundExpressions:
    def test_a_mul_b_plus_c(self):
        """y = a * b + c (step20 핵심 데모)."""
        from rezero.v1 import fill_grad
        a = Variable(np.array(3.0))
        b = Variable(np.array(2.0))
        c = Variable(np.array(1.0))
        y = a * b + c
        fill_grad(y)
        assert y.data == np.array(7.0)
        assert a.grad == np.array(2.0)   # ∂y/∂a = b
        assert b.grad == np.array(3.0)   # ∂y/∂b = a
        assert c.grad == np.array(1.0)   # ∂y/∂c

    def test_scalar_mul_add(self):
        """3.0 * x + 1.0 (step21 핵심 데모)."""
        from rezero.v1 import fill_grad
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
