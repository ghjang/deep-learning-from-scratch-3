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
| 7 | [exploration_07_syntax_idioms.md](./exploration_07_syntax_idioms.md) | step01 직후 / step11 | Python 문법과 이디엄 — 데코레이터, f-string, == vs is, lambda, @override/@overload, 언패킹(`*` 스플래트, head/tail) |
| 8 | [exploration_08_monkey_patching.md](./exploration_08_monkey_patching.md) | step01 직후 | 런타임 클래스 조작 (Monkey Patching), 네임스페이스, 객체→소스 역직렬화 |
| 9 | [exploration_09_abc_abstract.md](./exploration_09_abc_abstract.md) | step02 직후 | Python 추상 클래스: `abc.ABC` vs `raise NotImplementedError()` (에러 시점, 강제력, 메타클래스) |
| 10 | [exploration_10_what_is_derivative.md](./exploration_10_what_is_derivative.md) | step04 직후 | 도대체 미분이 뭔데? — 수치 미분에서 깨달은 본질 (수포자 학습 궤적, 블랙박스 미분, autograd 기반) |
| 11 | [exploration_11_autodiff_modes.md](./exploration_11_autodiff_modes.md) | step04 직후 | 자동 미분의 두 모드: 포워드 vs 리버스 (왜 신경망은 역전파인가, 수치 미분 캐싱 한계, 비용 비교) |
| 12 | [exploration_12_language_binding.md](./exploration_12_language_binding.md) | step04 직후 | 언어 바인딩/타이핑: early vs late binding, 정적 vs 동적 타이핑, C/C++/Java/Python/JS 비교 (step04 `f` 재사용에서 출발) |
| 13 | [exploration_13_derivative_notation.md](./exploration_13_derivative_notation.md) | step05 진행 중 | 미분 표기법의 두 얼굴: `dy/dx` vs `df/dx` (Leibniz/Lagrange, 국소적 미분, 역전파 수학) |
| 14 | [exploration_14_derivative_terminology.md](./exploration_14_derivative_terminology.md) | step05 진행 중 | "미분" 용어 7중 혼돈과 해독 전략 (미분값/도함수/미분연산, 한영 대조, 밑시딥 실전 해독) |
| 15 | [exploration_15_math_symbol_origins.md](./exploration_15_math_symbol_origins.md) | step05 진행 중 | 수학 기호의 어원과 역사 (√/∫/d/∂/∇/∞ 왜 이런 모양인가, radix/summa/differentia) |
| 16 | [exploration_16_side_effect.md](./exploration_16_side_effect.md) | step08 진행 중 | "부작용"이라는 번역이 사고를 지배한다: side effect 재프로그래밍 (번역어 감정색 왜곡, 순수 함수, 최적화 충돌) |
| 17 | [exploration_17_python_testing.md](./exploration_17_python_testing.md) | step10 준비 중 | 파이썬 테스팅 패러다임 진화: unittest에서 pytest로 (책의 교육적 선택 vs 실무 국룰, hypothesis property-based testing) |
| 18 | [exploration_18_graph_traversal.md](./exploration_18_graph_traversal.md) | step15 | 그래프 기본과 순회 — DAG, DFS/BFS 파이썬 구현, 위상 정렬(Kahn's). step16 generation 이해 위한 배경지식 (확장 후보 open-ended) |
| 19 | [exploration_19_naming_hungarian.md](./exploration_19_naming_hungarian.md) | step16 | 네이밍과 헝가리안 표기법 — 변수명에 타입을 박을 것인가? (Systems Hungarian vs 현대 Pythonic, creator_func 시도/철회에서 도출) |
| 20 | [exploration_20_node_class_idea.md](./exploration_20_node_class_idea.md) | step16 | 계산 그래프 추상화 경계 — Node 클래스와 순회 이터레이터 (Function/Variable 역할 분담 심화) |
| 21 | [exploration_21_yield_generator_coroutine.md](./exploration_21_yield_generator_coroutine.md) | step16 | yield, 제너레이터, 코루틴 — 파이썬의 "일시정지 가능한 함수" 계보 (step18 contextmanager 배경) |
| 22 | [exploration_22_weakref_gc.md](./exploration_22_weakref_gc.md) | step17 | weakref와 GC — 약한 참조의 마법과 CPython 내부 (참조 카운팅, 순환 감지 GC, ob_weakreflist 구독자 모델) |
| 23 | [exploration_23_contextmanager.md](./exploration_23_contextmanager.md) | step18 | 컨텍스트 매니저와 contextlib — yield가 with를 만드는 마법 (__enter__/__exit__ vs @contextmanager+yield) |
| 24 | [exploration_24_strategy_iterator_config.md](./exploration_24_strategy_iterator_config.md) | step18 | 전략 패턴, 이터레이터 패턴, "결정 시점"의 딜레마 (Config if문=인라인 전략, DI, PyTorch 합리적 타협) |
| 25 | [exploration_25_array_priority.md](./exploration_25_array_priority.md) | step21 | `__array_priority__`의 정체 — 책의 매직 넘버 200은 왜 불필요해졌나 (ufunc/rmul 역사, NEP 13, "책 코드도 검증하라" 교훈) |
| 26 | [exploration_26_numbers_complex.md](./exploration_26_numbers_complex.md) | step22 | 파이썬 숫자 계보 (int 임의 정밀도 / float 64비트 / complex), 오일러 공식, ★★★ "무한 번 미분 가능성 ↔ 기울기 소실" 연결 (부드러움의 역설, sigmoid vs ReLU) |
| 27 | [exploration_27_rosenbrock.md](./exploration_27_rosenbrock.md) | step28 | Rosenbrock 해부 — 골짜기 바닥이 포물선인 이유(A/B항 역할), "낙하→크롤링" 궤적 실증, 조건수/lr딜레마, ★ 시험 함수 디자인 = 알고리즘 실패 모드의 역설계 (벤치마크 계보), ★★ NFL 정리 — 만능 알고리즘 없음, 선택 지도, 뉴턴 vs SGD (이론적 우위 ≠ 실제 선택) |
| 28 | [exploration_28_directional_derivative.md](./exploration_28_directional_derivative.md) | step28 | 방향 미분 — "gradient가 가장 가파른 방향"인 이유를 당연시하지 않고 증명 (방향미분 → 내적 → 코사인 3단 유도), ★ 1변수 미분 = 선택지 2개짜리 방향미분, ★ 경사하강법 코드에 내적이 안 보이는 이유 (증명 why와 실행 how의 분리), 등고선 ⊥ gradient 귀결 |
| 29 | [exploration_29_newton_method.md](./exploration_29_newton_method.md) | step29 | 뉴턴 방법 — "곡률을 알면 점프할 수 있다". 1차/2차 근사 대비 (직선엔 바닥 없음, 포물선엔 있음), 갱신식 유도, 원조=방정식 근 찾기(f'에 적용), 2차 수렴 (오차 제곱, 유효숫자 배가 실증 7 iters), ★ "수동 계산"=f'' 손유도 (step30 고차 미분 복선), 국소 최대 함정(f''≤0) 실험, 선택 지도 두 번째 좌표 |
| 30 | [exploration_30_double_backprop.md](./exploration_30_double_backprop.md) | step31 | double backprop 이론 — "미분도 계산이다" 3단 논법 (미분=계산 → 실행하면 그래프 → 그래프는 재미분 가능). grad ndarray의 기억 상실 문제 (값 vs 식 대비), backward 내부를 Variable 연산으로 (before/after), y=x² 2층 그래프 ASCII 풀코스, ★ 머리 꼬임 3지점 해부 (backward가 forward를 만든다 / gy도 리프 / 2층 구조), Define-by-Run 자기 참조 ("모든 실행은 그래프를 낳는다" 완전 대칭). 후속 질문 3연타로 확장된 3개 좌표 — ★ 수학 좌표: Hessian은 특수한 야코비안 (gradient의 Jacobian + 슈발츠 정리 대칭성), ★ 실무 좌표: 사용 빈도의 진실 (1차 압도적/2차 간혹/3차+ 없음 — 능력 시연 ≠ 실무 빈도), ★ 역사 좌표: double backprop 용어의 Chainer 계보 (죽었지만 이긴 프레임워크) |
| 31 | [exploration_31_python_generics.md](./exploration_31_python_generics.md) | step32 | Python 제네릭 — TypeVar/Protocol/bound를 96 errors 사건으로 실전 습득. type 별칭 (Worklist/DerivativeFn, 3.12 `type`문), ★ 반공변 해부 (함수 매개변수는 반대 방향 — Callable[[Variable]]이 Callable[[VariableLike]]에 못 들어가는 이유), TypeVar가 해결책인 이유 (f와 x를 같은 타입으로 묶으면 방향 비교 자체가 소멸), Protocol에 __init__ 선언 팁 (type(x)(...) 생성자 오탐 해결), ★ 인터페이스 두 진영 (명목적 Java/C# vs 구조적 Go/TS/Python — Java `<T extends>`와 1:1 평행), 런타임 소거 ("힌트를 달았으면 계약을 지켜라") |
| 32 | [exploration_32_derivative_anatomy.md](./exploration_32_derivative_anatomy.md) | step35 | 미분식 해부 — 자기 참조 3총사 (exp/sigmoid/tanh — 흔하다!), ★ 미분식 성분 분류 (출력만·입력만·입출력 동시(SiLU)·상수·다른 입력 — 활성함수가 출력형인 이유: forward 캐시=역전파 완결), 그래프 3형태 실증 (소멸·순환·폭증 — Tanh 2→4→8 지수폭증, Function ≈3배, 8차는 렌더링조차 무거움), ★ rezero vs dezero 미분식 두 길 (출력 재사용 vs tanh·pow 파이프라인 — 계산 이득 vs 수학적 명시성, 브로 자가 도달 분석), exp의 특이성 (자기 참조인데 구현에 따라 크기 유지 — 수학 특성과 구현은 직교) |

> 파일 번호 = **생성 순서** (탐구 역사 보존)
> 아래 "추천 읽는 순서"는 처음 읽을 때 논리적 흐름 기준

## 🔬 탐구 후보 큐 (Research Queue)

> 지금 당장 문서화하지 않지만, **나중에 파고 싶은 주제**를 기록해두는 곳.
> 대화 중 터진 통찰이 "그냥 사라지는" 걸 방지. step 진도 여유 생기면 회수.

| 파일 | 내용 |
|---|---|
| [RESEARCH_QUEUE.md](./RESEARCH_QUEUE.md) | 대기 중인 탐구 후보 주제들 (제미나이 대화 통찰, h vs η, Loss Landscape 등) |

## 🎨 디자인 패턴 노트 (횡단 관심사, 누적형)

> 위 exploration_XX 시리즈와 다른 카테고리. 패턴은 여러 step에 걸쳐 재등장하는 **횡단 관심사**라서
> 단일 파일에 누적하며 관리. step 진행 중 패턴 발견 시 이 파일에 추가.

| 파일 | 시점 | 주제 |
|---|---|---|
| [design_patterns.md](./design_patterns.md) | step01~ 누적 | DeZero에 등장하는 디자인 패턴 (래퍼, 템플릿 메서드 등) |

## 🐛 디버깅 노트 (횡단 관심사, 누적형)

> 디자인 패턴과 같은 구조. 파이썬의 런타임 검증/디버깅 메커니즘(`assert`, 예외 계층, 재귀 한계 등)을
> 여러 step에 걸쳐 누적 정리. step 진행 중 검증/에러 메커니즘 마주치면 이 파일에 추가.

| 파일 | 시점 | 주제 |
|---|---|---|
| [debugging.md](./debugging.md) | step08~ 누적 | 파이썬 런타임 검증/디버깅 (assert + `-O` 모드, RecursionError, fail-fast 등) |

## 📐 코딩 스타일 노트 (횡단 관심사, 누적형)

> 디자인 패턴/디버깅과 같은 구조. PEP 8 기반 코드 스타일(빈 줄, 주석, 네이밍, 함수 길이 등)을
> 여러 step에 걸쳐 누적 정리. rezero 구현 중 스타일 결정이 생기면 이 파일에 추가.

| 파일 | 시점 | 주제 |
|---|---|---|
| [coding_style.md](./coding_style.md) | step08~ 누적 | 코드 스타일/가독성 (논리 블록 빈 줄, PEP 8 의무 vs 관행 등) |

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
- **#8~26 (step 진행 파생)**: step08~22 진행 중 자연스럽게 파생된 주제별 심화. step 진도에 맞춰 읽기. 기본기(#1~7) 먼저 본 뒤 관심 가는 step 탐구로.

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
