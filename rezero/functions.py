"""
rezero.functions — DeZero 함수 모음
====================================

직접 구현할 것들 (dezero/functions.py 대응):
  - 사칙연산     : add, sub, mul, div, neg, pow
  - 기본 수학    : sin, cos, tanh, exp, log
  - 형상 변환    : reshape, transpose, broadcast_to, sum, matmul
  - 비교/조건    : max, min, clip
  - 활성화       : sigmoid, relu (or softmax_cross_entropy)
  - loss         : mean_squared_error, softmax_cross_entropy
  - 기타         : get_item, flatten, linear

패턴: 각 함수는 Function 클래스(또는 래퍼)로 구현되고, Variable에 편의 연산자
오버로딩을 추가해 Variable + Variable 같은 자연스러운 표현을 가능케 함.

참고 단계: step26 ~ step60 (단계별로 점진 확장)
참고 자료: dezero/functions.py

MLX 백엔드 (Issue #1):
  - 각 forward()에서 np.* 대신 xp.* (get_array_module 결과)를 쓰면 NumPy/MLX 겸용.
  - cuda.py와 core.py의 백엔드 추상화가 선행되어야 함.
"""
