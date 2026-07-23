# 📚 notes/ — 학습 탐구 노트 모음

> step 진도 외에 깊이 파고 싶었던 주제들 (Python, NumPy, 프레임워크, 수학 등)을
> **주제별 개별 파일**로 정리. `LEARNING_NOTES.md`(step 요약)에서 링크로 참조.

## 📋 인덱스

| # | 파일 | 시점 | 주제 |
|---|---|---|---|
| 1 | [exploration_01_python_basics.md](./exploration_01_python_basics.md) | step01 직후 | Python 클래스 / 캡슐화 / 프레임워크 디자인 |
| 2 | [exploration_02_numpy_basics.md](./exploration_02_numpy_basics.md) | step01 직후 | NumPy 기본 (3권 중심) — ndarray 내부, shape/axis, 브로드캐스팅, 수학 함수, 난수 |
| 3 | [exploration_03_backend_adapters.md](./exploration_03_backend_adapters.md) | step01 직후 | 백엔드 어댑터: Variable을 CuPy/MLX로 확장한다면 (autograd, Define-by-Run, xp 패턴) |
| 4 | [exploration_04_symbolic_vs_numeric.md](./exploration_04_symbolic_vs_numeric.md) | step01 직후 | sympy vs PyTorch/DeZero: 심볼릭 vs 수치 계산 패러다임 (manim/Graphviz 시각화 비교) |
| 5 | [exploration_05_python_object_model.md](./exploration_05_python_object_model.md) | step01 직후 | Python 객체 모델 — CPython 내부, descriptor, 리플렉션, 룩업 체계 5가지, `__new__`/`__init__`, 메타클래스 (★공식 참조) |
| 6 | [exploration_06_data_types.md](./exploration_06_data_types.md) | step01 직후 | Python 기본 자료형 — list/tuple/str, 레퍼런스 모델, 얕은/깊은 복사 |
| 7 | [exploration_07_syntax_idioms.md](./exploration_07_syntax_idioms.md) | step01 직후 | Python 문법과 이디엄 — 데코레이터, f-string, == vs is, lambda, @override/@overload |
| 8 | [exploration_08_monkey_patching.md](./exploration_08_monkey_patching.md) | step01 직후 | 런타임 클래스 조작 (Monkey Patching), 네임스페이스, 객체→소스 역직렬화 |
| 9 | [exploration_09_abc_abstract.md](./exploration_09_abc_abstract.md) | step02 직후 | Python 추상 클래스: `abc.ABC` vs `raise NotImplementedError()` (에러 시점, 강제력, 메타클래스) |
| 10 | [exploration_10_what_is_derivative.md](./exploration_10_what_is_derivative.md) | step04 직후 | 도대체 미분이 뭔데? — 수치 미분에서 깨달은 본질 (수포자 학습 궤적, 블랙박스 미분, autograd 기반) |
| 11 | [exploration_11_autodiff_modes.md](./exploration_11_autodiff_modes.md) | step04 직후 | 자동 미분의 두 모드: 포워드 vs 리버스 (왜 신경망은 역전파인가, 수치 미분 캐싱 한계, 비용 비교) |

> 파일 번호 = **생성 순서** (탐구 역사 보존)
> 아래 "추천 읽는 순서"는 처음 읽을 때 논리적 흐름 기준

## 🎨 디자인 패턴 노트 (횡단 관심사, 누적형)

> 위 exploration_XX 시리즈와 다른 카테고리. 패턴은 여러 step에 걸쳐 재등장하는 **횡단 관심사**라서
> 단일 파일에 누적하며 관리. step 진행 중 패턴 발견 시 이 파일에 추가.

| 파일 | 시점 | 주제 |
|---|---|---|
| [design_patterns.md](./design_patterns.md) | step01~ 누적 | DeZero에 등장하는 디자인 패턴 (래퍼, 템플릿 메서드 등) |

## 🎯 추천 읽는 순서 (처음 읽을 때)

현재 파일 번호 순서(1→7)가 곧 추천 순서와 일치함. 논리적 의존 관계:

```
[#1 Python 클래스/캡슐화]
   ↓ Variable 클래스가 파이썬에서 어떻게 구현되는지 (래퍼 패턴, attribute 등)
[#2 NumPy 기본]
   ↓ Variable이 담는 'data'가 실제로 뭔지 (ndarray, shape, axis)
[#3 백엔드 어댑터]
   ↓ 그 ndarray를 다른 백엔드(CuPy/MLX)로 교체하면? (Define-by-Run, autograd 개념 등장)
[#4 sympy vs 수치]
   ↓ autograd vs 심볼릭 계산의 철학적 차이 (심화)
[#5 Python 객체 모델]
   ↓ 파이썬 객체의 내부 구조/리플렉션/룩업 체계 (★공식 참조, 필요시 독자적 참조도 가능)
[#6 Python 기본 자료형]
   ↓ list/tuple/str/레퍼런스 모델 (#5의 전제 지식)
[#7 Python 문법과 이디엄]
   ↓ 데코레이터, f-string, lambda, == vs is, @override/@overload (#1과 병행 읽기도 좋음)
```

- **처음부터 끝까지 읽기**: 1 → 2 → 3 → 4 → 5 → 6 → 7 (기본)
- **특정 주제만**: 각 탐구는 독립적으로도 읽을 수 있음 (필요시 다른 탐구 링크로 연결)
- **키워드 검색**: 각 항목의 `#키워드` 태그로 검색해서 찾기

## 📖 공통 용어 안내 (모든 탐구에서 인용)

이 탐구 노트들에서 반복적으로 등장하는 용어/표준을 미리 정리. 각 탐구 첫 페이지엔 중복 안 함 (여기로 링크).

### PEP (Python Enhancement Proposal)

파이썬의 **"향상 제안서"**. 법률 발의안이나 RFC 같은 역할 — 파이썬을 어떻게 발전시킬지 공식 제안/토론/채택하는 문서. 누구나 쓸 수 있고, 번호가 붙어. 각 PEP는 보통 https://peps.python.org/pep-NNNN/ 형식으로 접근.

| PEP | 제목 | 자주 인용되는 곳 |
|---|---|---|
| **PEP 8** | Style Guide for Python Code | self 관례, 전반적 코딩 스타일 |
| **PEP 20** | The Zen of Python (`import this`) | 파이썬 철학 |
| **PEP 227** | Nested Scopes — LEGB 규칙, 클래스 스코프 | 스코프와 룩업 |
| **PEP 253** | C3 선형화 도입 (아래 참조) | MRO |
| **PEP 318** | Decorators (`@staticmethod` 등) | 데코레이터 |
| **PEP 498** | f-string (Python 3.6+) | f-string |

→ "PEP N에 따르면..." 은 **"공식 표준이야"** 라는 뜻 (내 생각이 아니라).

> 💡 **특히 PEP 8, PEP 20** 은 진짜 많이 인용되니 한 번 읽어보길 권장.

### C3 선형화 (C3 Linearization)

다중 상속에서 **MRO(메서드 결정 순서)를 계산하는 공식 알고리즘**. Dylan 언어에서 유래(1996), PEP 253으로 파이썬에 도입(Python 2.3+).

**3가지 핵심 규칙**:
1. 자식은 부모보다 먼저
2. 상속 선언 순서 유지 (`class D(B, C)`면 B가 C보다 먼저)
3. 부모의 MRO 보존

세 규칙을 동시에 만족하는 순서가 하나일 때만 MRO 결정. 충돌하면 `TypeError`:
```python
class X(A, B): pass
class Y(B, A): pass
class Z(X, Y): pass   # ❌ TypeError — X는 A>B, Y는 B>A로 모순
```

→ **DeZero는 단일 상속만 쓰므로 C3 실질적으로 무관**. 다만 "`__mro__`가 어떻게 정해지나?" 호기심에 대한 답.

**키워드**: `#PEP` `#PEP8` `#PEP20` `#PEP227` `#PEP253` `#PEP318` `#PEP498` `#C3선형화` `#MRO` `#다중상속` `#Python표준`

## 📝 새 탐구 노트 작성 규칙

- **파일명**: `exploration_NN_주제.md` (NN은 순번, 예: `exploration_02_decorators.md`)
- **시점**: 어떤 step 이후에 진행했는지 헤더에 명시
- **형식**: 하이브리드 (핵심 요약 + 짧은 코드 예시)
- **키워드**: 각 항목마다 `#태그` 달아두기 (나중에 검색 용이)
- **목차**: 파일 상단에 목차 두기 (길어질 경우)

## 🔗 연결 고리

- `LEARNING_NOTES.md` 각 step 섹션에서 relevant 탐구 노트로 링크
- `AGENTS.md`의 "학습 관리 워크플로"에서 이 디렉터리 언급
