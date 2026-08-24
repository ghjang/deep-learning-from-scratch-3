"""rezero.v1 Variable 기본 테스트 — 생성, name, property, __len__, __repr__.

step01~19에서 검증한 핵심 케이스를 pytest 스타일로 정리.
"""

import numpy as np
import pytest

from rezero.v2 import Variable


# ===== 생성 (step01, step09) ===================================================
class TestVariableCreation:
    def test_create_with_ndarray(self):
        """ndarray로 Variable 생성."""
        x = Variable(np.array(1.0))
        assert x.data == np.array(1.0)

    def test_create_with_name(self):
        """name 키워드 전용 (step19 항목 028)."""
        x = Variable(np.array(1.0), name='x')
        assert x.name == 'x'

    def test_name_must_be_keyword(self):
        """name은 키워드 전용 — 위치 전달 시 TypeError (step19 항목 028)."""
        with pytest.raises(TypeError):
            Variable(np.array(1.0), 'x')  # type: ignore[misc]

    def test_reject_non_ndarray(self):
        """list/int/float 직접 전달 시 TypeError (step09 방어막)."""
        with pytest.raises(TypeError):
            Variable([1, 2, 3])  # type: ignore[arg-type]
        with pytest.raises(TypeError):
            Variable(3.14)  # type: ignore[arg-type]

    def test_none_data_allowed(self):
        """data=None 허용 (step17 no_grad 등에서 사용)."""
        x = Variable(None)
        assert x.data is None

    def test_grad_init_none(self):
        """grad는 초기값 None."""
        x = Variable(np.array(1.0))
        assert x.grad is None

    def test_creator_init_none(self):
        """creator는 초기값 None (입력 변수)."""
        x = Variable(np.array(1.0))
        assert x.creator is None

    def test_generation_init_zero(self):
        """generation은 초기값 0."""
        x = Variable(np.array(1.0))
        assert x.generation == 0


# ===== property 4종 + __len__ (step19) =========================================
class TestVariableProperties:
    def test_shape(self):
        """shape property — data.shape 위임."""
        x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
        assert x.shape == (2, 3)

    def test_ndim(self):
        """ndim property — data.ndim 위임."""
        x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
        assert x.ndim == 2

    def test_size(self):
        """size property — data.size 위임."""
        x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
        assert x.size == 6

    def test_dtype(self):
        """dtype property — data.dtype 위임."""
        x = Variable(np.array([1, 2, 3]))
        assert x.dtype == np.dtype('int64')

    def test_len(self):
        """__len__ — data의 첫 번째 차원 크기."""
        x = Variable(np.array([[1, 2, 3], [4, 5, 6]]))
        assert len(x) == 2

    def test_none_data_property_raises(self):
        """data=None에서 property 접근 시 RuntimeError (step19 _ensure_data 방어막)."""
        x = Variable(None)
        with pytest.raises(RuntimeError):
            _ = x.shape
        with pytest.raises(RuntimeError):
            _ = x.ndim
        with pytest.raises(RuntimeError):
            _ = x.size
        with pytest.raises(RuntimeError):
            _ = x.dtype
        with pytest.raises(RuntimeError):
            _ = len(x)


# ===== __repr__ (step19 항목 030 — Variable( 대문자) ===========================
class TestVariableRepr:
    def test_repr_scalar(self):
        """스칼라 repr — 'Variable(value)'."""
        x = Variable(np.array(2.0))
        assert repr(x) == 'Variable(2.0)'

    def test_repr_none(self):
        """data=None repr — 'Variable(None)'."""
        x = Variable(None)
        assert repr(x) == 'Variable(None)'

    def test_repr_multiline_indent(self):
        """다중 행 ndarray 들여쓰기.
        NumPy가 자체 1칸 들여쓰기 + 우리가 9칸 replace → 총 10칸.
        """
        x = Variable(np.array([[1, 2], [3, 4]]))
        r = repr(x)
        assert r.startswith('Variable([[1 2]')
        lines = r.split('\n')
        assert len(lines) == 2
        # NumPy 기본 1칸 + 우리 9칸 replace = 10칸
        assert lines[1].startswith(' ' * 10 + '[3 4')


# ===== clear_grad (step14 항목 021) ============================================
class TestClearGrad:
    def test_clear_grad(self):
        """clear_grad() — grad None으로 초기화."""
        from rezero.v2 import fill_grad, square
        x = Variable(np.array(2.0))
        y = square(x)
        fill_grad(y)
        assert x.grad is not None
        x.clear_grad()
        assert x.grad is None
