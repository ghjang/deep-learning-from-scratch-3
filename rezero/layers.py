"""
rezero.layers — Layer 클래스들
==============================

직접 구현할 것들 (dezero/layers.py 대응):
  - Layer       : 매개변수(Parameter)를 모아두는 컨테이너 기반 클래스
  - Linear      : 완전연결층

핵심 개념: Layer는 내부에 Parameter를 자동으로 추적. 메타프로그래밍
(__dict__ 순회 등)으로 하위 Layer/Parameter를 재귀 수집.

참고 단계: step40대 (Parameter, Layer 도입부)
참고 자료: dezero/layers.py
"""
