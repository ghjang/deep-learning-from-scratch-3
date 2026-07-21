"""
rezero.datasets — 데이터셋 클래스들
====================================

직접 구현할 것들 (dezero/datasets.py 대응):
  - Dataset         (기반 클래스, transform 파이프라인 지원)
  - BigDataDataset  (메모리 절약형)
  - Spiral          (예제용 스파이럴 데이터)
  - MNIST, FashionMNIST (다운로드+캐싱)
  - Sin (시계열/RNN 예제용)
  - PtB (Penn Treebank, 자연어 예제용)

참고 단계: 중반부 고지 (학습 파이프라인 구축 단계)
참고 자료: dezero/datasets.py
"""
