"""
rezero.steps.step31 — [3고지] 고차 미분(이론 편)
=====================================================

★ 본 step은 코드가 없는 이론 편 (2026-08-20 완료).

정답지 steps/step31.py가 `# No code`인 그대로, 새로 짤 코드는 0건.
구현은 다음 step32(구현 편)에서. 이 step의 산출물은 "이론"이다:

핵심 논리 (3단 논법):
  1. 미분 계산도 결국 계산이다 — 곱셈과 덧셈의 나열
  2. DeZero에서 계산은 실행만 하면 그래프로 남는다 (Define-by-Run)
  3. 남은 그래프는 또 미분할 수 있다
  → 2차, 3차, ... n차 미분이 무한히 가능해진다

구현 변경의 방향 (step32에서 실제 반영):
  - Variable.grad를 ndarray → Variable로 (그래프 소유 = 기억 상실 해소)
  - backward 내부를 Variable 연산으로 (`2 * x * gy`가 Mul 노드를 만든다)
  - gy 시작점도 Variable(np.ones_like) — 상수도 그래프의 리프
  - create_graph 옵션 (기본 False) — step18의 lean 철학 연장

머리가 꼬이는 3지점 (해소됨 — 상세는 탐구 노트 30):
  A. backward가 forward를 만든다?  → backward도 "그냥 실행"이다
  B. gy(시작 기울기)의 정체?        → 상수 1도 리프 노드
  C. 그래프가 2층으로 쌓인다?       → 아래층 원래 함수 / 위층 미분 계산

★ 상세 기록: notes/exploration_30_double_backprop.md
  (2층 그래프 ASCII 풀코스, Define-by-Run 자기 참조, step32 미리보기 표)

→ 다음: rezero/steps/step32.py (고차 미분(구현 편) — 실제 구현)
  이 파일은 위 기록을 남기는 역할만 하며, 별도 코드는 없음.
"""
