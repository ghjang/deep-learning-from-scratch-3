"""rezero.v0.utils — 유틸리티 (numerical_diff 스칼라판).

v0은 시각화 스코프 아님 (순수 학습 실험실 — 그래프 관찰은 v1/v2 도구 사용).
numerical_diff만 v0 자체 소유 — common의 것은 ndarray 가정이라 여기선 스칼라판.
"""

from rezero.v0.core import Variable

__all__ = ["numerical_diff"]


def numerical_diff(f: "callable", x: "Variable", eps: float = 1e-4) -> float:  # type: ignore[type-arg]
    """중앙차분 수치 미분 (스칼라판) — gradient check용.

    v1의 numerical_diff와 동일 공식이지만 data가 float 하나 —
    "한 점에서의 미분"이라는 본질이 배열 없이 그대로 보임.

    Args:
        f: Variable을 받아 Variable을 반환하는 함수.
        x: 미분 위치의 Variable.
        eps: h (미세 차분). 너무 작으면 반올림 오차 지배 (이슈 53 참고).

    Returns:
        수치 미분 근사값 (float).
    """
    assert x.data is not None, "x.data must be set"

    x0 = Variable(x.data - eps)
    x1 = Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)

    assert y0.data is not None and y1.data is not None
    return (float(y1.data) - float(y0.data)) / (2 * eps)
