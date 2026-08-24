"""rezero.common — 버전 공통 유틸리티.

v1/v2 양쪽에서 재사용하는, **버전 차이에 영향받지 않는 순수 함수들**의 집합.

★ 공통/버전별 판별 기준 (step32 — 브로 합의):
    "grad 타입이나 계산 그래프 구조에 의존하는가?"
    - 의존 X → common   (예: numerical_diff — f(x±h)만 평가하는 순수 수학)
    - 의존 O → 각 vX 소유 (예: plot_dot_graph — 그래프 순회 구조와 결합)

★ vX는 "박제가 아니라 살아있는 코드" (AGENTS.md 원칙):
    v1도 이후 수정 가능성이 있으므로, 공통 코드를 한 곳(common)에서
    유지보수하면 양쪽 수정 시 불일치가 발생하지 않음.
"""

from rezero.common.utils import numerical_diff

__all__ = ["numerical_diff"]
