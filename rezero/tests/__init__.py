"""
rezero.tests — 학습용 프레임워크 rezero의 단위 테스트 모음
============================================================

이 패키지는 원본 tests/(dezero 검증용)와 대응되는 rezero 검증용 자리입니다.

구조 원칙:
  - 각 테스트 파일명은 원본 tests/test_*.py 와 1:1 대응
    (단, chainer 비교 테스트는 macOS 환경에서 의미 없으므로 제외)
  - 템플릿 상태에선 모든 테스트가 @unittest.skip 처리되어 있음
  - 브로가 rezero 모듈 구현을 진행하면서 해당 테스트의 skip을 풀고 구현

실행:
  # rezero 테스트만
  uv run python -m unittest discover rezero/tests

  # 특정 테스트만
  uv run python -m unittest rezero.tests.test_sum

  # 원본 + rezero 전부
  uv run python -m unittest discover tests
  uv run python -m unittest discover rezero/tests
"""
