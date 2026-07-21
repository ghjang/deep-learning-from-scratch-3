"""
rezero.cuda — GPU 백엔드 추상화
===============================

직접 구현할 것들 (dezero/cuda.py 대응):
  - get_array_module(x) : NumPy/CuPy/MLX 자동 선택
  - as_numpy(x)
  - as_cupy(x)

⚠️ macOS에서 CuPy는 미지원. 현재 환경에선 NumPy로 fallback.
→ 향후 MLX 백엔드(이슈 #1 참조)로 확장할 예정.

참고 자료: dezero/cuda.py, AGENTS.md "Known Gotchas #2"
"""
