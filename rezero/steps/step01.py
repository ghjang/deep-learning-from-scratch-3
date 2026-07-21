"""
rezero.steps.step01 — [1고지] 테니스 공 같은 '상자' (Variable 도입)
===============================================

이 step에서 배운 것:
  - Variable 클래스 도입: numpy ndarray를 감싸는 "데이터 상자"
  - 0차원(스칼라) vs 1차원(벡터) 구분
  - 상자 안의 데이터(.data)는 교체 가능

실행: uv run python rezero/steps/step01.py
"""

import numpy as np


class Variable:
    """DeZero의 변수. 데이터를 담는 '상자'.

    현재(step01)는 data 속성 하나만 있지만, 이후 step들에서
    grad, creator 등 역전파에 필요한 메타정보가 추가된다.

    비유: Java의 Integer/int 박싱(Boxing)과 유사한 래퍼 패턴.
    PyTorch Tensor, TF Tensor도 같은 철학.
    """

    def __init__(self, data):
        self.data = data


def inspect(label, x):
    """Variable 상자의 내부 구조를 살펴보는 헬퍼 (step별 탐구용)."""
    print(f"[{label:>10}] data={x.data!s:>10}  type={type(x.data).__name__}  "
          f"ndim={x.data.ndim}  shape={x.data.shape}")


# --- 0차원 스칼라 ---------------------------------------------------
x = Variable(np.array(1.0))
inspect("스칼라", x)

# 상자 안의 데이터 교체 (같은 상자에 다른 공 넣기)
x.data = np.array(2.0)
inspect("스칼라 교체", x)

# --- 1차원 벡터 -----------------------------------------------------
x.data = np.array([1.0])
inspect("벡터", x)
