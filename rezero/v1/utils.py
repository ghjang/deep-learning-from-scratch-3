"""rezero.v1.utils — 유틸리티 함수.

gradient check 등 검증용 헬퍼.
"""

from collections.abc import Callable

import numpy as np

from rezero.v1.core import Variable, as_array


def numerical_diff(
    f: Callable[[Variable], Variable],
    x: Variable,
    eps: float = 1e-4,
) -> np.ndarray:
    """수치 미분 (중앙 차분). f의 내부를 몰라도 미분 가능 — 블랙박스 관점.

    gradient check용 — 역전파(해석적)와 비교해 구현이 맞는지 독립 검증.
    공식: f'(x) ≈ [f(x+h) - f(x-h)] / 2h  (중앙 차분, 오차 O(h²))

    Args:
        f: 미분할 함수 (square, 또는 합성 함수).
        x: 미분 기준점 Variable.
        eps: h (미세 차분 간격, 기본 1e-4).
    """
    if x.data is None:
        raise RuntimeError(f"{x!r}의 data가 None입니다 — 수치 미분에 사용할 수 없습니다.")

    # 차분점 생성 (x ± eps) — as_array로 스칼라 정규화
    x0 = Variable(as_array(x.data - eps))
    x1 = Variable(as_array(x.data + eps))

    # f 평가 + 결과 회수
    y0 = f(x0)
    y1 = f(x1)

    assert y0.data is not None and y1.data is not None
    return (y1.data - y0.data) / (2 * eps)
