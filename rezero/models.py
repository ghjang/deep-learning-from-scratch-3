"""
rezero.models — Model 클래스와 신경망 모델들
=============================================

직접 구현할 것들 (dezero/models.py 대응):
  - Model           : Layer를 상속, predict/loss 등 학습 흐름의 기반
  - MLP             : 다층 퍼셉트론
  - VGG16           : VGG16 (및 가중치 다운로드 지원)
  - SimpleConvNet   : 소형 CNN
  - ResNet          : ResNet (잔차 연결)
  - SeqDataseq / RNN/LSTM 계열 (필요 시)

참고 단계: 후반부 고지 (신경망 조립 단계)
참고 자료: dezero/models.py

MLX 백엔드 (Issue #1):
  - VGG16/ResNet 같은 모델은 MLX 백엔드 도입 시 가장 성능 이득이 큰 영역.
    (M5 Max에서 GPU 활용하면 학습 속도 비약적 향상 기대)
"""
