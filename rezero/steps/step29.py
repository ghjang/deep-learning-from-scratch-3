"""
rezero.steps.step29 — [3고지] 뉴턴 방법으로 푸는 최적화(수동 계산)
=====================================================================

★ 책 공식 제목 "뉴턴 방법으로 푸는 최적화(수동 계산)". 괄호는 책 공식 부제.

★★★ 이 step의 심장 — 근사 차수의 차이:

  경사하강법 (step28): f를 직선(1차)으로 봄
    → 직선엔 최소점이 없음 → 방향만 알 수 있음 → 보폭(lr)은 임의
  뉴턴 방법 (이번):   f를 포물선(2차)으로 봄
    → 포물선엔 최소점이 있음 → 그 바닥으로 바로 점프
    → "곡률을 알면 점프할 지점까지 수학이 정해준다"

  뉴턴 갱신식 유도 (2차 테일러의 바닥):
    f(x) ≈ f(x₀) + f'(x₀)(x-x₀) + ½f''(x₀)(x-x₀)²
    이 포물선을 미분해 0으로 두면 → x = x₀ - f'(x₀)/f''(x₀)

★ "수동 계산": f''(x)를 프레임워크가 못 뽑음 (자동 미분 1차까지만) →
  사람이 손으로 유도 (gx2). step30 "최적화 자동화"의 복선.

★ 시각화 [4]: 책 그림 재현 — 울퉁불퉁한 f 곡선에 각 스텝에서
  "접하는" 2차 테일러 포물선을 겹쳐 그리고 점프 과정 표시.

★ v1 패키지 변경 없음 (응용 step).

참고 자료:
  - 원본 구현: steps/step29.py
  - 이전 step: rezero/steps/step28.py (경사하강법 — 1차 근사의 대조군)
  - 이슈: 36번

실행:
  uv run python rezero/steps/step29.py
"""

import os
import sys

if '__file__' in globals():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np

from rezero.v1 import Variable, fill_grad


# ===== 대상 함수 + 손으로 유도한 2차 미분 (★ "수동 계산") =======================
# f(x)  = x⁴ - 2x²
# f'(x) = 4x³ - 4x        ← fill_grad가 자동 계산
# f''(x) = 12x² - 4       ← ★ 사람이 손으로 유도! (자동 미분은 1차까지만)
#
# 임계점: f' = 0 → x = 0, ±1
#   x = ±1: f'' = 8 > 0 (최소점, f = -1) ← 목적지
#   x = 0:  f'' = -4 < 0 (최대점!)       ← [3] 실험의 함정
def f(x: Variable) -> Variable:
    """최적화 대상: f(x) = x⁴ - 2x². 최소점 x = ±1 (f = -1)."""
    return x ** 4 - 2 * x ** 2


def gx2(x: np.ndarray) -> np.ndarray:
    """f''(x) = 12x² - 4 — 손으로 유도한 2차 미분 (수동 계산)."""
    return 12 * x ** 2 - 4


def newton_step(x: Variable) -> None:
    """뉴턴 갱신 한 걸음: x.data -= f'(x)/f''(x).

    곡률(f'')로 보정된 스텝 — 방향뿐 아니라 크기까지 수학이 결정.
    (gd_step의 -lr·grad와 대조: lr이 사라졌다!)
    """
    assert x.grad is not None, "fill_grad 이후에 호출할 것"
    assert x.data is not None
    x.data -= x.grad / gx2(x.data)


def _val(x: Variable) -> float:
    """데모 출력용 — data를 float로 (None 가드, pyright 대응)."""
    assert x.data is not None
    return float(x.data)


# --- 데모: 뉴턴 방법 vs 경사하강법 ----------------------------------------------
if __name__ == "__main__":
    print("=== step29 뉴턴 방법으로 푸는 최적화(수동 계산) ===")
    print()

    # --- [1] 뉴턴 기본 — 2차 수렴 관찰 ---
    print("[1] 뉴턴 방법 — x=2.0 시작, 10 iters")
    x = Variable(np.array(2.0))
    for i in range(10):
        y = f(x)
        x.clear_grad()
        fill_grad(y)

        err = abs(_val(x) - 1.0)  # 최소점 x=1까지의 거리
        grad_val = float(x.grad) if x.grad is not None else float('nan')
        print(f"    iter {i}: x = {_val(x):.15f} | f'(x) = {grad_val:+.3e} | 오차 = {err:.3e}")

        if err < 1e-14:
            print(f"    → 기계 정밀도 도달! ({i} iters)")
            break

        newton_step(x)

    print(f"    ★ 오차 감축: ~제곱으로 줄어듦 (2차 수렴) — 유효숫자가 매번 배가")
    print(f"    ★ lr이 없다! 크기까지 f''(곡률)이 결정")
    print()

    # --- [2] 경사하강법 대비 — 같은 함수, 같은 시작점 ---
    print("[2] 경사하강법 대비 — 같은 f, x=2.0, lr=0.1")
    print("    (f는 대칭 — 최소점이 ±1 두 개. 어느 쪽이든 도달하면 성공으로 측정)")
    x = Variable(np.array(2.0))
    reached = -1
    for i in range(100000):
        # 두 최소점 ±1 중 가까운 쪽까지의 거리
        err = min(abs(_val(x) - 1.0), abs(_val(x) + 1.0))
        if err < 1e-6:
            reached = i
            break

        y = f(x)
        x.clear_grad()
        fill_grad(y)
        assert x.grad is not None and x.data is not None
        x.data -= 0.1 * x.grad

    if reached >= 0:
        which = '+1' if _val(x) > 0 else '-1'
        print(f"    오차 < 1e-6 도달: 경사하강 {reached} iters (최소점 {which}에 안착) vs 뉴턴 7 iters")
    else:
        print(f"    ★ 100,000 iters(루프 상한)에도 도달 못함")
    print(f"    ★ lr=0.1은 첫 스텝을 크게 오버슈트(2 → -0.4) — 이 문제에선")
    print(f"      우연히 반대편 골짜기로 넘어가 -1에 안착. lr 민감성의 실증")
    print(f"    ★ 근처에서 뉴턴의 압도적 속도 — 단, 근처에 '도달한 뒤'의 이야기")
    print()

    # --- [3] 나쁜 초기치 — f'' ≤ 0 지역의 함정 (적합성 메모 실증) ---
    print("[3] 나쁜 초기치 — x=0.3 시작 (f''(0.3) = -2.92 < 0 지역)")
    x = Variable(np.array(0.3))
    for i in range(10):
        y = f(x)
        x.clear_grad()
        fill_grad(y)

        second = gx2(np.array(_val(x)))
        print(f"    iter {i}: x = {_val(x):+.6f} | f'' = {float(second):+.3f} "
              f"| f(x) = {_val(y):+.6f}")

        # f'가 사실상 0이면 정지 (임계점 — 최소가 아닐 수도!)
        assert x.grad is not None
        if abs(float(x.grad)) < 1e-12:
            print(f"    → 정지: f'(x) ≈ 0. f(0) = 0 > f(±1) = -1 — 최소점이 아닌 최대점에 갇힘!")
            break

        newton_step(x)

    print(f"    ★ 뉴턴은 f'(x)=0이면 멈춘다 — 그게 최소점이란 보장 없음 (f'' ≤ 0 지역)")
    print(f"    ★ 적합성 메모 실증: '나쁜 초기치 → 최악' — 국소 최대/안장에 갇힘")
    print()

    # --- [4] 시각화 — 책 그림 재현: f에 "접하는" 포물선과 점프 ---
    print("[4] 시각화 — 2차 테일러 포물선이 f에 접하고, 그 바닥으로 점프")
    import matplotlib
    matplotlib.use('Agg')  # 헤드리스 환경 대응
    import matplotlib.pyplot as plt

    # 한글 폰트 — DejaVu Sans엔 한글 글리프가 없어 macOS 기본 한글 폰트 사용.
    # 유니코드 마이너스(U+2212)는 AppleGothic에 없음 → ASCII 하이픈으로 대체
    matplotlib.rcParams['font.family'] = 'AppleGothic'
    matplotlib.rcParams['axes.unicode_minus'] = False

    xs = np.linspace(-0.6, 2.3, 400)
    fig, ax = plt.subplots(figsize=(10, 7))

    # 울퉁불퉁한 원본 곡선 f (수식 라벨은 mathtext — 위첨자 글리프 문제 회피)
    ax.plot(xs, xs ** 4 - 2 * xs ** 2, 'k-', linewidth=2, label=r'$f(x) = x^4 - 2x^2$')

    # 각 스텝: 접하는 2차 테일러 포물선 + 현재 점 + 점프 화살표
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    x_cur = 2.0
    for i in range(4):
        fv = x_cur ** 4 - 2 * x_cur ** 2       # f(x₀)
        d1 = 4 * x_cur ** 3 - 4 * x_cur        # f'(x₀)
        d2 = 12 * x_cur ** 2 - 4               # f''(x₀)

        # 2차 테일러 근사 포물선: T(x) = f + f'·(x-x₀) + ½f''·(x-x₀)²
        taylor = fv + d1 * (xs - x_cur) + 0.5 * d2 * (xs - x_cur) ** 2
        ax.plot(xs, taylor, '--', color=colors[i], linewidth=1.5, alpha=0.8,
                label=f'{i}차 스텝의 접 포물선 ($x_0$={x_cur:.3f})')
        ax.plot(x_cur, fv, 'o', color=colors[i], markersize=8)

        # 점프: 포물선의 바닥으로
        x_next = x_cur - d1 / d2
        ax.annotate('', xy=(x_next, fv + d1 * (x_next - x_cur) + 0.5 * d2 * (x_next - x_cur) ** 2),
                    xytext=(x_cur, fv),
                    arrowprops=dict(arrowstyle='->', color=colors[i], lw=2))
        x_cur = x_next

    ax.axhline(y=0, color='gray', linewidth=0.5)
    ax.axvline(x=1.0, color='gray', linewidth=0.5, linestyle=':')
    ax.plot(1.0, -1.0, 'r*', markersize=20, label='최소점 (1, -1)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title("뉴턴 방법: f에 '접하는' 2차 테일러 포물선의 바닥으로 점프")
    ax.legend(loc='upper center')
    ax.grid(True, alpha=0.3)

    out = 'output/newton_quadratic.png'
    os.makedirs('output', exist_ok=True)
    fig.savefig(out, dpi=120, bbox_inches='tight')
    print(f"    저장: {out}")
    print(f"    ★ 파란 점에서 시작 → 각 색의 접 포물선 바닥으로 점프 → 빨은 별(최소점)으로")
    print()

    # --- [5] 책 그림 클로즈업 — "아직 근사가 덜 된" 한 순간의 드라마 ---
    # [4]가 전체 과정 연쇄라면, 이쪽은 1스텝의 클로즈업:
    # 포물선 바닥(점프 목적지)이 실제 우물과 어긋나 있는 상태 —
    # "근사라서 틀릴 수 있다 → 그래서 반복한다"가 그림으로 보이는 장면.
    print("[5] 책 그림 클로즈업 — 어긋난 포물선 바닥 (아직 근사 중인 한 스텝)")
    fig2, ax2 = plt.subplots(figsize=(11, 7))

    # 극값 3개 (우물 ±√10 ≈ ±3.16, 언덕 0) — f(x) = x⁴/20 - x²
    g = lambda t: t ** 4 / 20 - t ** 2
    gp = lambda t: t ** 3 / 5 - 2 * t       # f'
    gpp = lambda t: 3 * t ** 2 / 5 - 2      # f''

    # x범위: 접점(+2.4)이 그림 중앙에 오도록 — 왼쪽 언덕(0), 오른쪽 우물(+3.16)까지
    ts = np.linspace(-1.5, 5.5, 600)
    ax2.plot(ts, g(ts), 'k-', linewidth=2.0, label=r'$f(x) = x^4/20 - x^2$')
    ax2.set_ylim(-6.9, 3.5)

    # 접점: x₀ = +2.4 — 내리막(f' < 0)이라 포물선 "좌측 가지"가 f에 접하고 바닥은 오른쪽
    x0 = 2.4
    fv, d1, d2 = g(x0), gp(x0), gpp(x0)
    taylor = fv + d1 * (ts - x0) + 0.5 * d2 * (ts - x0) ** 2
    ax2.plot(ts, taylor, 'b--', linewidth=1.8, alpha=0.9,
             label='2차 테일러 포물선 (완전한 U자)')

    # 점프 목적지 — 포물선의 극점
    x_jump = x0 - d1 / d2
    y_jump = fv + d1 * (x_jump - x0) + 0.5 * d2 * (x_jump - x0) ** 2
    ax2.plot(x_jump, y_jump, 'r*', markersize=18, zorder=5)
    ax2.annotate('포물선의 바닥 = 점프 목적지\n(실제 우물과 어긋남!)',
                 xy=(x_jump, y_jump), xytext=(x_jump - 4.3, y_jump - 1.1),
                 fontsize=11, color='red', bbox=dict(facecolor='white', alpha=0.85, edgecolor='none'),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.5))

    # 실제 우물 바닥 — 회색 별 (어긋남의 기준점). 주석은 별 왼쪽 위 허공으로
    x_well = np.sqrt(10)
    ax2.plot(x_well, g(x_well), '*', color='dimgray', markersize=14, zorder=4)
    ax2.annotate('실제 우물 바닥', xy=(x_well, g(x_well)),
                 xytext=(x_well - 0.5, g(x_well) + 1.6), fontsize=10, color='dimgray',
                 bbox=dict(facecolor='white', alpha=0.85, edgecolor='none'),
                 arrowprops=dict(arrowstyle='->', color='dimgray', lw=1.2))

    # 접점 표시 — 포물선과 f가 만나는 곳 (f, f', f'' 동시 일치)
    ax2.plot(x0, fv, 'o', color='blue', markersize=9, zorder=5)
    ax2.annotate('여기서 접함 (f, f\', f\'\' 일치)', xy=(x0, fv),
                 xytext=(x0 - 2.3, fv + 2.4), fontsize=10, color='blue',
                 bbox=dict(facecolor='white', alpha=0.85, edgecolor='none'),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=1.2))

    # 점프 화살표 — 곡선 궤적
    ax2.annotate('', xy=(x_jump - 0.1, y_jump + 0.12), xytext=(x0 + 0.1, fv - 0.12),
                 arrowprops=dict(arrowstyle='-|>', color='red', lw=2.0,
                                 connectionstyle='arc3,rad=0.3'))

    ax2.axhline(y=0, color='gray', linewidth=0.5)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title("뉴턴의 한 스텝: 포물선을 믿고 점프 — 근사라 아직 어긋난다 (그래서 반복)")
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)

    out2 = 'output/newton_dramatic.png'
    fig2.savefig(out2, dpi=120, bbox_inches='tight')
    print(f"    저장: {out2}")
    print(f"    접점 x₀ = {x0:.2f} (그림 중앙) → 포물선 바닥 x = {x_jump:.3f} vs 실제 우물 x = {x_well:.3f}")
    print(f"    ★ 빨간 별(점프 목적지)이 실제 우물을 지나쳐 처짐 — 2차 근사의 오차")
    print(f"    ★ 근처에선 이 어긋남이 제곱으로 줄어 2차 수렴 (다음 스텝이 곧 우물)")
    print()

    print("=== step29 완료 — 곡률을 알면 점프할 수 있다 ===")
    print("    경사하강: 직선 근사 → 방향만 → 조금씩 걷기")
    print("    뉴턴:     포물선 근사 → 바닥까지 → 점프 (2차 수렴) 🎉")
