"""rezero.common.utils — 버전 공통 유틸리티 함수.

v1/v2 어느 쪽의 Variable과도 동작하는 순수 함수.
특정 버전(rezero.v1.core 등)을 import하지 않는다 — 인자의 타입에서
필요한 클래스를 얻는 duck typing으로 진짜 공통을 유지.
"""

from collections.abc import Callable
from typing import Optional, Protocol, TypeVar

import numpy as np


class VariableLike(Protocol):
    """numerical_diff가 요구하는 최소 인터페이스 (v1/v2 Variable 공통).

    구조적 타이핑(Protocol) — v1.Variable도 v2.Variable도 이 모양이면 통과.
    common이 특정 버전을 import하지 않기 위한 장치.

    __init__ 선언 이유: type(x)(...) 생성자 호출의 시그니처를 정적 분석에
    알려주기 위함 (없으면 "Expected 0 positional arguments" 오탐).
    """

    data: Optional[np.ndarray]

    def __init__(self, data: Optional[np.ndarray]) -> None: ...


VariableT = TypeVar("VariableT", bound=VariableLike)


def numerical_diff(
    f: Callable[[VariableT], VariableT],
    x: VariableT,
    eps: float = 1e-4,
) -> np.ndarray:
    """수치 미분 (중앙 차분). f의 내부를 몰라도 미분 가능 — 블랙박스 관점.

    gradient check용 — 역전파(해석적)와 비교해 구현이 맞는지 독립 검증.
    공식: f'(x) ≈ [f(x+h) - f(x-h)] / 2h  (중앙 차분, 오차 O(h²))

    ★ v1/utils.py에서 이관 (step32) — grad 타입/그래프 구조와 무관한 순수 수학이라
    어느 버전에서도 동일. 차분점 생성은 type(x)(...)로 인자의 클래스를 재사용
    (common이 v1/v2 어느 쪽도 import하지 않기 위함).

    ★ 제네릭 (TypeVar bound VariableLike): f를 Callable[[Variable], Variable]로
    넘겨도 반공변 위반이 안 나게 — f와 x의 원소 타입이 같으면 호환 (invariant).

    Args:
        f: 미분할 함수 (square, 또는 합성 함수).
        x: 미분 기준점 Variable (v1/v2 어느 쪽이든).
        eps: h (미세 차분 간격, 기본 1e-4).
    """
    if x.data is None:
        raise RuntimeError(f"{x!r}의 data가 None입니다 — 수치 미분에 사용할 수 없습니다.")

    # 차분점 생성 (x ± eps) — type(x)로 같은 버전의 Variable 생성.
    # np.asarray 정규화: data - eps 결과가 numpy scalar일 수 있어 ndarray로.
    x0 = type(x)(np.asarray(x.data - eps))
    x1 = type(x)(np.asarray(x.data + eps))

    # f 평가 + 결과 회수
    y0 = f(x0)
    y1 = f(x1)

    assert y0.data is not None and y1.data is not None
    return (y1.data - y0.data) / (2 * eps)
