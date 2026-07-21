"""
rezero.utils — 유틸리티 함수
============================

직접 구현할 것들 (dezero/utils.py 대응):
  - get_dot_graph(graph) : 계산 그래프를 Graphviz .dot 문자열로 변환
  - plot_dot_graph(output, ...) : 그래프를 이미지로 저장/표시
  - sum_to(x, shape)    : 브로드캐스트 역전환 헬퍼
  - reshape_sum_backward(gy, x_shape, axis, keepdims) : sum 역전파 형상 복원
  - logsumexp(x, axis)  : 수치 안정 softmax용
  - gradient_check(f, x, ...) : 수치 미분 vs 해석 역전파 검증 (테스트용)
  - array_allclose / array_equal (테스트 헬퍼)
  - download(url) : 파일 캐싱 다운로드 (가중치 등)

참고 단계: 단계별로 필요할 때마다 점진 구현
참고 자료: dezero/utils.py
"""
