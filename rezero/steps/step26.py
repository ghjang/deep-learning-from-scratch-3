"""
rezero.steps.step26 — [3고지] 계산 그래프 시각화(2)
=====================================================

★ 본 step의 코드는 step25에서 이미 커버됨 (2026-08-11).

정답지 steps/step26.py의 내용 — goldstein 함수 정의 + 순전파/역전파 +
name 부여 + plot_dot_graph로 PNG 출력 — 을 step25 작업 시 전부 구현했음.
심지어 정답지보다 풍성하게: show_value 옵션, 변수명 볼드(HTML-like label),
포맷 화이트리스트(png/svg/pdf), DOT 소스 보존, SVG 벡터 출력까지.

→ 실행은 rezero/steps/step25.py 참고:
  uv run python rezero/steps/step25.py
  (output/goldstein.png / goldstein_value.png / goldstein.svg 생성)

★ 경위 (step25/26 코드 배분 착각 — 2026-08-11 기록):
  step25 작업 당시 정답지 steps/step25.py(# No code)와 steps/step26.py(코드 있음)를
  나란히 비교하지 않고 진행 → step25가 step26 영역까지 커버.
  브로가 책 26단계를 다시 보고 발견. 코드는 전부 정상 동작하므로 그대로 승격.
  방지책: AGENTS.md "정답지 인접 step 비교" 원칙 신설.
  상세: 이슈 31번 코멘트 / LEARNING_NOTES step25.

이 파일은 위 경위를 기록하는 리다이렉트 역할만 하며, 별도 코드는 없음.
"""
