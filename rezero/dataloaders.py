"""
rezero.dataloaders — DataLoader
===============================

직접 구현할 것들 (dezero/dataloaders.py 대응):
  - DataLoader      (Dataset을 미니배치 단위로 순회)
  - SeqDataLoader   (시계열용, 시간 순서 유지)

핵심 개념: shuffle + minibatch slicing. 다중 프로세스 옵션도 학습 대상.

참고 단계: 중반부 고지
참고 자료: dezero/dataloaders.py
"""
