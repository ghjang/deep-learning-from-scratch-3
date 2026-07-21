# 📚 notes/ — 학습 탐구 노트 모음

> step 진도 외에 깊이 파고 싶었던 주제들 (Python, NumPy, 프레임워크, 수학 등)을
> **주제별 개별 파일**로 정리. `LEARNING_NOTES.md`(step 요약)에서 링크로 참조.

## 📋 인덱스

| # | 파일 | 시점 | 주제 |
|---|---|---|---|
| 1 | [exploration_01_python_basics.md](./exploration_01_python_basics.md) | step01 직후 | Python 클래스 / 캡슐화 / 문법 이디엄 / 프레임워크 디자인 (13가지) |
| 2 | [exploration_02_numpy_basics.md](./exploration_02_numpy_basics.md) | step01 직후 | NumPy 기본 (3권 중심) — ndarray 내부, shape/axis, 브로드캐스팅, 수학 함수, 난수 |
| 3 | [exploration_03_backend_adapters.md](./exploration_03_backend_adapters.md) | step01 직후 | 백엔드 어댑터: Variable을 CuPy/MLX로 확장한다면 (autograd, Define-by-Run, xp 패턴) |
| 4 | [exploration_04_symbolic_vs_numeric.md](./exploration_04_symbolic_vs_numeric.md) | step01 직후 | sympy vs PyTorch/DeZero: 심볼릭 vs 수치 계산 패러다임 (manim/Graphviz 시각화 비교) |

## 📝 새 탐구 노트 작성 규칙

- **파일명**: `exploration_NN_주제.md` (NN은 순번, 예: `exploration_02_decorators.md`)
- **시점**: 어떤 step 이후에 진행했는지 헤더에 명시
- **형식**: 하이브리드 (핵심 요약 + 짧은 코드 예시)
- **키워드**: 각 항목마다 `#태그` 달아두기 (나중에 검색 용이)
- **목차**: 파일 상단에 목차 두기 (길어질 경우)

## 🔗 연결 고리

- `LEARNING_NOTES.md` 각 step 섹션에서 relevant 탐구 노트로 링크
- `AGENTS.md`의 "학습 관리 워크플로"에서 이 디렉터리 언급
