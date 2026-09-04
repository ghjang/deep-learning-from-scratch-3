"""v0 회귀 테스트 — NumPy 없는 스칼라 DeZero (이슈 43 작업 3).

실행: uv run pytest rezero/v0/tests/ -v

목적 테스트 3종:
  1. 스칼라 기본 — 값/grad/gradient check (v1과 동일 결과)
  2. 두 축 분리 시연 — "배치"가 루프로 드러남 (v0의 존재 이유)
  3. 순수성 — v0 모듈에 numpy가 없음 검증
"""

import math

import pytest

from rezero.v0 import Variable, fill_grad, numerical_diff, sin, square
from rezero.v0.functions import cos


class TestScalarBasic:
    """스칼라 기본 — v1과 같은 수학, 다른 데이터 표현."""

    def test_forward_value(self):
        x = Variable(2.0)
        y = square(x)

        assert y.data == 4.0
        assert isinstance(y.data, float)  # ndarray가 아님 — v0의 요점

    def test_grad_and_gradient_check(self):
        x = Variable(3.0)
        y = square(x)

        fill_grad(y)

        assert x.grad == 6.0  # 2x = 6

        assert x.data is not None and x.grad is not None
        approx = numerical_diff(square, x)
        assert abs(x.grad - approx) < 1e-6

    def test_sin_gradient_check(self):
        x = Variable(math.pi / 4)

        fill_grad(sin(x))

        assert x.data is not None
        approx = numerical_diff(sin, x)
        assert x.grad is not None
        assert abs(x.grad - approx) < 1e-6


class TestTwoAxesSeparation:
    """두 축 분리 시연 — v0의 존재 이유 (노트 34 "배치 = 독립 스칼라 실험의 묶음").

    v1에서는:
        x = Variable(np.array([1.0, 2.0, 3.0]))
        fill_grad(sin(x))  # 1번 호출 — 데이터축이 배열에 숨음

    v0에서는 같은 일을 하려면:
        xs = [Variable(1.0), Variable(2.0), Variable(3.0)]
        for x in xs:
            fill_grad(sin(x))  # ← 데이터축이 코드에 보임 = 독립 실험 3개!
    """

    def test_batch_is_independent_scalar_experiments(self):
        """"배치" = 독립 스칼라 실험의 묶음 — 루프가 그 사실을 드러냄."""
        xs = [1.0, 2.0, 3.0]

        results = []
        for v in xs:
            x = Variable(v)
            y = sin(x)
            fill_grad(y)

            assert x.grad is not None and x.data is not None
            results.append((float(x.data), float(x.grad)))

        # 각 점의 grad = cos(x) — 노트 34의 "대각 압축 VJP"를 루프로 체감
        assert all(g is not None for _, g in results)
        for x_val, grad_val in results:
            assert grad_val == pytest.approx(math.cos(x_val), abs=1e-9)

    def test_no_cross_contamination_between_experiments(self):
        """독립 실험들은 서로 오염되지 않음 — 각각의 그래프가 완전히 분리."""
        x1 = Variable(1.0)
        x2 = Variable(5.0)

        y1 = square(x1)
        fill_grad(y1)
        assert x1.grad == 2.0  # 2·1

        # x2의 그래프는 x1과 무관 — x1 결과에 영향받지 않음
        y2 = square(x2)
        fill_grad(y2)
        assert x2.grad == 10.0  # 2·5


class TestPurityNoNumpy:
    """순수성 — v0 모듈에 numpy가 없음 검증."""

    def test_core_does_not_import_numpy(self):
        """core.py 모듈 네임스페이스에 numpy 없음."""
        import rezero.v0.core as v0_core

        assert not hasattr(v0_core, 'np')
        assert not hasattr(v0_core, 'numpy')

    def test_functions_does_not_import_numpy(self):
        """functions.py 모듈 네임스페이스에 numpy 없음."""
        import rezero.v0.functions as v0_functions

        assert not hasattr(v0_functions, 'np')
        assert not hasattr(v0_functions, 'numpy')

    def test_variable_data_is_float(self):
        """Variable.data는 float — shape/dtype 속성 없음 (NumPy 흔적 제거)."""
        x = Variable(3.0)

        assert isinstance(x.data, float)
        assert not hasattr(type(x), 'shape')
        assert not hasattr(type(x), 'dtype')


class TestRemovedNumpyHelpers:
    """v1에서 NumPy가 하던 일이 v0에선 어떻게 됐나 — 걷어내기 관찰."""

    def test_as_float_replaces_as_array(self):
        """v1의 as_array(스칼라→ndarray) → v0의 as_float(int→float)."""
        from rezero.v0.core import as_float

        assert as_float(42) == 42.0
        assert isinstance(as_float(42), float)

    def test_seed_is_scalar_one(self):
        """씨앗이 np.ones_like가 아니라 그냥 1.0 — dy/dy=1이 코드 그대로."""
        from rezero.v0.core import Function

        x = Variable(3.0)
        y = square(x)
        fill_grad(y)

        # grad 전체가 float — 씨앗 1.0이 곱해져도 float
        assert isinstance(x.grad, float)
        assert not isinstance(x.grad, Function)

    def test_no_broadcasting(self):
        """브로드캐스팅 없음 — 1 * upstream는 오직 스칼라×스칼라."""
        x = Variable(2.0)
        y = x + 3  # 상수와의 연산

        fill_grad(y)

        assert x.grad == 1.0
        assert y.data == 5.0
