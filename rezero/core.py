"""
rezero.core — 핵심 클래스들
===========================

직접 구현할 것들 (dezero/core.py 대응):
  - Variable    : 데이터를 담는 클래스 (역전파 추적 대상)
  - Function    : 변수 간 연산의 기반 클래스
  - Config      : 전역 설정 (역전파 활성화 플래그 등)
  - using_config, no_grad : Config 컨텍스트 매니저
  - as_array, as_variable : 타입 변환 헬퍼

참고 단계: step07 ~ step32 (core_simple에서 시작 → step33부터 이 파일로 이관)

참고 자료:
  - 정답지: dezero/core.py
  - 핵심 개념: Define-by-Run (동적 계산 그래프)
"""
