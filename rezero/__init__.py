"""
rezero — 『밑바닥부터 시작하는 딥러닝 3』 직접 구현 학습 프로젝트
====================================================================

이 패키지는 원본 dezero/를 '정답지'로 두고, 책을 읽으며 직접 다시 구현해보는
나만의 DeZero 변종입니다.

이름 유래:
  - zero : 밑바닥부터 다시 시작하는 zero
  - Re:  : Re:Zero (다시 시작하는 이세계로의 진입편) 오마주 + '다시'의 의미

원칙:
  1. dezero/ 소스를 그대로 복사하지 말 것. 막힐 때만 참고할 것.
  2. 이해한 뒤 내 손으로 다시 짤 것. 이해가 안 가면 dezero/를 펴서 분석.
  3. 파이썬 기법/이디엄도 적극 학습. 모르면 그때그때 찾아보기.
  4. 변종 실험 환영. 더 좋은 이름, 더 좋은 구조를 상상해볼 것.

★ 버전 폴더 구조 (step23 도입 — step32 v2 브랜칭, 2026-09-04 v0 신설, 2026-09-09 v3 브랜칭):
  - rezero/v0/ — 순수 Python 학습 실험실 (NumPy 배제, 이슈 43 작업 3). data=float
  - rezero/v1/ — 제 1~2고지 스코프 (step01~22). grad가 ndarray — 1차 미분까지만
  - rezero/v2/ — 제 3고지 "고차 미분 계산" (step32~36). grad가 Variable,
    fill_grad(y, create_graph=True)로 double backprop 지원
  - rezero/v3/ — 제 4고지 "신경망 만들기" (step37~51). v2 계승 + 텐서 1급 시민
    + Sum. 모듈 3분류 A안 (functions / activations·layers는 등장 step에 생성)
  - rezero/common/ — 버전 공통 순수 함수 (numerical_diff).
    판별 기준: "grad 타입/그래프 구조에 의존하는가?" — 무관하면 common
  사용: `from rezero.v1 import ...` / `from rezero.v2 import ...` / `from rezero.v3 import ...`

  ★ vX는 "박제가 아니라 살아있는 코드" — 신중하게 수정 가능
    (rezero/steps/ 과거 학습 흔적 수정 금지와는 별개 규칙).

  rezero/steps/ — 학습 흔적 전부 (step01~60). 과거 step은 수정 금지.

진행 상황:
  - 현재 단계: step38 (제 4고지 진행 중 — 정답지는 reshape/transpose 계열, 제목은 책 확인 필요)
  - 완료한 step: step01 ~ step37 ✅ ★ 제 4고지 개막 (텐서를 다루다 — v3 창설,
    Sum 도함수 ones + 브로드캐스팅 shape 복원, NumPy 우선 버그 수정)
  - 이전 고지: 1고지 미분 자동 계산 ✅ / 2고지 자연스러운 코드로 ✅ /
    3고지 고차 미분 계산 (step25~36) ✅
"""

__version__ = "0.3.1"  # step37 완료 (텐서를 다루다 — v3 창설, 4고지 개막)
