"""
rezero.core_simple — 단순화된 코어 (step23~32 학습용)
=====================================================

dezero/core.py보다 단순한 버전. 책의 step23~step32에서는 이쪽을 사용한다.
(원본 dezero/__init__.py의 is_simple_core 플래그와 동일한 개념.)

직접 구현할 것들 (dezero/core_simple.py 대응):
  - Variable, Function (기본형)
  - setup_variable (편의 함수들 등록)
  - as_array, as_variable
  - Config, using_config, no_grad

참고 단계: step23 ~ step32
참고 자료: dezero/core_simple.py
"""
