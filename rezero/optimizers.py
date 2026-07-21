"""
rezero.optimizers — 최적화 기법들
=================================

직접 구현할 것들 (dezero/optimizers.py 대응):
  - Optimizer   (기반 클래스)
  - SGD
  - MomentumSGD
  - AdaGrad
  - Adam

핵심 흐름: model(=Layer)의 params()를 순회하며 각 Parameter.data를 갱신.

참고 단계: step40대 후반 (Optimizer 도입)
참고 자료: dezero/optimizers.py
"""
