"""
rezero.steps.step23 — [2고지] 패키지로 정리
===============================================

★ 책 공식 제목 "패키지로 정리". step01~22 코드를 rezero/v1/ 패키지로 승격.

이 스텝 자체는 코드를 짜는 게 아니라 **패키화 결과를 검증**하는 자리.
- rezero/v1/core.py — Variable, Function, Config, fill_grad 등 핵심
- rezero/v1/functions.py — Square, Add, Mul, Neg, Sub, Div, Pow + wrapper
- rezero/v1/__init__.py — re-export

★ rezero 정체성 (dezero와 다른 점):
  - 역전파: Variable.backward() 메서드 → fill_grad() 전역 함수 (관심사 분리)
  - 매직메서드: setup_variable() 클래스 밖 대입 → 클래스 안 정의 (정적 분석 호환)
  - __array_priority__ = 200 → 버림 (현대 NumPy에선 __rmul__로 충분)
  - is_simple_core 스위치 → 없음 (core 하나로)
  - setup_variable() → 없음 (클래스 안 정의라 불필요)

★ 빈 템플릿 삭제 — 기존 rezero/core.py 등 11개 빈 파일은 헷갈려서 삭제.
  v1/이 진짜 패키지. 추후 vX 없이 export할 일 생기면 그때 더미 만들면 됨.

참고:
  - 학습 흔적(주석, step 번호 참조)은 rezero/steps/stepNN.py에 남아있음.
  - v1 코드는 API화되어 주석이 간결함. 모르면 steps/에서 뒤지기.

실행:
  uv run python rezero/steps/step23.py
"""

# step23.py를 직접 실행할 때 rezero 패키지를 찾을 수 있도록 프로젝트 루트를 path에 추가.
# (정답지 step23.py와 동일한 패턴)
if '__file__' in globals():
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from rezero.v1 import Variable, fill_grad, numerical_diff
from rezero.v1 import square, add, mul, neg, sub, div, pow
import numpy as np


# --- 패키지화 검증 데모 ---------------------------------------------------------
if __name__ == "__main__":
    print("=== step23 패키지로 정리 — rezero.v1 검증 ===")
    print()

    # --- 케이스 1: 정답지 step23.py 동일 시나리오 ---
    print("[1] 정답지 동일 시나리오 — y = (x + 3) ** 2")
    x = Variable(np.array(1.0))
    y = (x + 3) ** 2
    fill_grad(y)
    print(f"    y      = {y}  (기대: Variable(16.0))")
    print(f"    x.grad = {x.grad}  (기대: 8.0 = 2(x+3))")
    print()

    # --- 케이스 2: 전 연산자 패키지에서 동작 확인 ---
    print("[2] 전 연산자 패키지 동작 — +, -, *, /, **, 단항 -")
    a = Variable(np.array(2.0))
    b = Variable(np.array(3.0))
    y = a * b + a ** 2 - b / a + (-a)
    fill_grad(y)
    # y = 6 + 4 - 1.5 + (-2) = 6.5
    print(f"    y = a*b + a**2 - b/a + (-a) = {y.data}  (기대: 6.5)")
    print()

    # --- 케이스 3: no_grad 컨텍스트 매니저 ---
    print("[3] no_grad — 추론 모드 (그래프 구축 안 함)")
    from rezero.v1 import no_grad
    with no_grad():
        x = Variable(np.array(2.0))
        y = square(x)
    print(f"    y      = {y.data}  (기대: 4.0 — 순전파 값은 나옴)")
    print(f"    y.creator = {y.creator}  (기대: None — no_grad라 그래프 안 만듦)")
    print()

    # --- 케이스 4: scalar/ndarray 혼합 연산 ---
    print("[4] 혼합 연산 — 3.0 * x + np.array(2.0)")
    x = Variable(np.array(2.0))
    y = 3.0 * x + np.array(2.0)
    fill_grad(y)
    print(f"    y      = {y.data}  (기대: 8.0 = 3*2+2)")
    print(f"    x.grad = {x.grad}  (기대: 3.0)")
    print()

    # --- 케이스 5: numerical_diff (utils 승격 검증) ---
    print("[5] numerical_diff — utils.py 승격 검증 (gradient check)")
    x = Variable(np.array(2.0))
    f = lambda t: square(t) + t     # f(x) = x² + x, f'(2) = 2*2+1 = 5
    # 해석 역전파
    y = square(x) + x
    fill_grad(y)
    # 수치 미분
    nd = numerical_diff(f, x)
    print(f"    f(x) = x² + x")
    print(f"    해석 역전파 x.grad = {x.grad}  (기대: 5.0 = 2x+1)")
    print(f"    수치 미분          = {nd}  (기대: 5.0에 근사)")
    print(f"    ★ gradient check 통과 (오차 {abs(x.grad - nd):.2e})")
    print()

    print("=== step23 완료 — rezero.v1 패키지 정상 동작 ===")
    print("    from rezero.v1 import Variable, fill_grad")
    print("    2고지(스칼라 Variable) 프레임워크 완성.")
