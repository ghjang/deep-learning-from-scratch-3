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
| 33 | [exploration_33_evaluation_timing.md](./exploration_33_evaluation_timing.md) | step36 | Define-by-Run의 평가 시점 — "이미 계산된 세계에서의 미분". ★ 브로 서술 4항목 검증 (그대로 맞음 — 그래프 구성+평가 동시 / 입력값 불변 / 고정된 값 기반 미분 / 리프에 합성 미분값), 모든 미분은 "x=2라는 한 점에서의 평가" (f''(2)라는 숫자, 함수가 아님), Variable 이중성 (data=평가값/grad=마지막 역전파의 미분값/creator=식 구조), grad의 생애 (쌓이는 게 아니라 그때그때 충전), step36 흐름 지도 표, ★ 헷갈림 원인 (z'는 y''가 아니다 — 새 함수의 1차 미분), 재사용형 이해의 열쇠와 연결 |
| 34 | [exploration_34_jacobian_vjp.md](./exploration_34_jacobian_vjp.md) | 3고지 완료 후 (4고지 전) | 야코비안은 흐르지 않는다 — VJP와 autograd의 실체. ★ 흐르는 건 언제나 gradient (야코비안은 교차로의 변환기로만 존재), JVP/VJP 쌍둥이 (어순=곱셈 순서, 동치 아님 — 구체 예시), ★ 명세와 실행의 분리 ("만들지 않는데 곱한다" — 탐구 28과 동형, JVP tangent 포함), 3고지 성분곱 = 대각 압축 VJP (조건부 필연 — 함수가 성분을 안 섞는 조건), ★★ step34 재해석 (본질은 독립 스칼라 실험 200개의 병렬 계산 — 야코비안은 해석의 렌즈, 두 관점 + 세 개의 축, 대각/비대각을 갈라놓는 건 함수의 섞음이지 데이터 관련성 아님), 4고지 전치곱 VJP 예고 + derivative hook 붕괴, shape 지도 (m×n 직사각이 일반형), autograd 용어 (오토그라드 국룰, HIPS/Autograd→JAX 계보) + 구현/수학 이중 구조, 분모 표기 (∂L/∂W는 묶음 축약), 수치 실증 (`v @ J` = `df(x) * v`, 0이 아닌 성분 0.5%, 200배 절약). ★ 초심자 보강: §0 기호/용어 치트시트 (`@`/`*`/⊙/전치/≡) + 각 절 머리에 "이 절이 답하는 질문" |
| 35 | [exploration_35_function_taxonomy.md](./exploration_35_function_taxonomy.md) | 이슈 43 작업 4 중 | 함수의 형태 분류학 — 브로 질문 5개를 뼈대로: 입출력 유무(Variable 리프=0입력 함수 + 리프 기억법 3종), 간섭의 두 층위(출력 조합은 필연 / 도함수의 형제 의존이 진짜 구분축) + 직교성 용어 코너(직교⊂독립, 내적 공간, 푸리에 "간섭 없는 분해" 연결) + 오해 포인트 메모, 섞음의 패턴=야코비안 희소 패턴(conv 밴드 포함), 구조 연산(sum↔broadcast 대칭, 치환) + 책 타임라인 1:1(step38~41), 도함수 참조 스펙트럼(①~⑤ + 조합 2종 — hook의 국경선, MatMul 예고). ★ 유형 표기 체계 통일 (D1 ⑤ 입출력형→②+④ 조합 흡수, ⑤=upstream형 이양) + 약어 사전 |
| 36 | [exploration_36_backprop_memory_ecology.md](./exploration_36_backprop_memory_ecology.md) | v2 UML 리뷰 중 | 역전파의 메모리 생태계 (v2 심화편 1탄) — 책이 다루지 않는 층위. ★ fill_grad 하나가 차수를 결정 (대상 그래프가 1계/2계를 가름), 원본 그래프와 미분의 관계(1차 역전파=2층 순전파+eval까지 완료 — 브로 최종 정리), gx의 이중 정체, grad 슬롯 생애(중간 자동 처분 vs 리프 면책 — clear_grad는 사용자 몫), 신생 vs 재참조(미분식 성분이 명단 결정 — 중간 출력 재등장 예고), gy 생존 조건, data·grad·output 3색 구분, 순·역방향 대칭(씨앗 1=곱셈 항등원). 다이어그램 04/05/06과 상호 참조 |
| 37 | [exploration_37_transpose_ndarray_addressing.md](./exploration_37_transpose_ndarray_addressing.md) | 이슈 43 4고지 전 (노트 35 §4에서 분리) | 전치와 다차원 어드레싱 — 두뇌 개조 (NumPy 메모리 구조론). ★ 배열은 메모리에 존재하지 않는다 — 존재하는 건 1D 버퍼 + 해석 규칙(shape+strides). 전치=strides 재배치(버퍼 무동 O(1) view), (길이,보폭) 묶음 이동, 보정 없음·한 줄 공식(곱셈 교환법칙), 관찰자 비유(종이는 그대로 내가 움직인다), shape 이중 역할(총량→버퍼/구조→strides), row/column-major 두 파벨, C++ 배열=신택틱 슈거, 수학-구현 이중성(세 번째 발현), 실전 지도(CHW↔HWC·어텐션), 역전파=뷰 규칙 왕복. ★★ concept image vs concept definition (2D 접기는 2D 안에서 완전 성공하는 알고리즘 — 정의로 위장, 3D부터 들통), 3D 축0↔축2 맞바꾸기(가운데 축 구경꾼 + 주소 대응 a[i,j,k]==b[k,j,i]), strides 정체=혼합 진법(시계 (24,60,60) — 1일=86400초가 stride), view 3요소+자기 검증 코드, 수학자의 전치 정의=내적 보존(쌍대 사상 — 그림 아닌 구조), 개념 생존표(shape/원소수/좌표 생존, strides 소멸 — 선형화는 선택), (Ax)·y=x·(Aᵀy) 성분 전개 유도, 미분=선형 사상·야코비안=행렬 표현(4고지 예고, 접선 기울기=1×1 특수 케이스). ★ 뇌구조 수술 점검표 38문항 (2026-08-28 정독 중 대화로 대폭 보강 + 저녁 수다: std::vector=1축 ndarray·이름의 역설(strides 미소유로 전치 불가), &v[0]+캐스팅↔view/reshape 대응(C는 모든 것이 as_strided), 어드레싱=인덱스×strides 내적(전치 불변=순열 직교 — 교환법칙의 좌표 없는 버전), strides 자유도(음수·0=broadcast step40 복선·as_strided), 래그드/재그드 용어 2형제 / 2026-08-30 정독 보강: axis 국어 사전(항해 방향≠생존자, 행/열은 2D 유산), 3D 성적표 contraction, 축 해석 프로토콜 3단계(국어 극복), sum=1-벡터와의 contraction·뷰 불가, reshape 해부(총량 불변의 율법, 선형 순서 보존 vs 전치 재해석 — 뷰 전치 불가·ascontiguousarray, PyTorch .view() 연속성 예고), 트리(재귀) 뷰 — 격자 이미지 대체재(균일 트리=ndarray 정의 조건, contraction=형제 서브트리 합병, DFS=row-major, 당기기 트리 통일 규약 + swap 함정 + 전치⊃교환·당기기 포함 관계, reduction 가족 일반화), 두 클럽 정리(뷰=안경 갈아끼우기 vs reduction=요약 계산), NCHW 재조직화·큐브 배치도((n-3)차원 배치도+잎 큐브)) |
| 39 | [exploration_39_highdim_transpose_gym.md](./exploration_39_highdim_transpose_gym.md) | 이슈 43 4고지 전 (노트 37 §8 정독 중 브로 요청, 2026-08-30) | 고차원 전치 연습장 — 4D·5D·6D에서 "묶음" 읽기. ★ 푸는 노트 (연습장): 전치=서류 재철(첫 축=묶음 기준, NCHW=이미지별 폴더 / CNHW=채널별 폴더), 창고 비유, 4D 기본기 ((2,3,2,2) 손실습 — a[0] vs transpose(1,0,2,3)[0], 인덱스 대응 검증), 연습 문제 Level 1~4 (축 읽기→전치 후 묶음 예측→역방향 설계(NHWC→NCHW, 어텐션 (B,S,H,D)→(B,H,S,D), 채널 당기기)→5D 비디오), 5D+ 큐브 배치도 재귀 + 잎 선택 자유(7D=6D 하이퍼큐브 나열도 정당 — 브로 관찰), 회수 지도(step38~41·CNN·어텐션). 최적 타이밍: 4고지 step38 직전 |
| 40 | [exploration_40_permutation_matrices.md](./exploration_40_permutation_matrices.md) | 이슈 43 4고지 전 (노트 37 §4 순열 행렬 캠프에서 분리, 2026-08-31) | 순열 행렬 실험실 — Sₙ을 행렬로 놀기 (브로 흥미로 신설). ★ 순열의 합성=행렬의 곱 (P_σP_τ=P_{σ∘τ}), S₃ 6개 행렬 전수 조사, 생성법 4종 (np.eye(n)[perm] 조립 / 행 교환 반복 / 거듭제곱=순환 부분군·노트 38 모드와 동일 구조 / 재귀 삽입), 생성원 — 인접 교환 s₀·s₁ 두 행렬의 단어로 군 전체 생성 + 땋음 관계(s₀s₁s₀=s₁s₀s₁), 케일리 표(라틴 방진), det=±1 짝홀순열·교대군 A₃, 연습 5문제 (거품정렬=순열의 단어 분해 포함), 행렬→순열 해독 P@np.arange(n) |
| 41 | [exploration_41_inner_product.md](./exploration_41_inner_product.md) | 이슈 43 4고지 전 (노트 37 §4 내적 보존에서 분리, 2026-08-31) | 내적: 곱들의 합이 세상을 재는 방법 (입문+지도 노트). ★ 두 얼굴 — 곱들의 합(대수) = 정렬도 측정기(기하, |v||w|cosθ), 표기 3형제(⟨v,w⟩ 앵글브래킷·v·w 점곱·vᵀw 행렬곱), 그림자(사영) 해석, 우리 문맥 3종(어드레싱 오프셋=가중합 / 순열과 내적 — 같이 이사·항 집합 불변 / 수반 항등식 ⟨Aᵀy,x⟩=⟨y,Ax⟩), 행렬 판(행렬곱=내적의 격자 — A@v=행별 내적, QKᵀ=정렬도 표), 실전 얼굴(코사인 유사도·공분산·거리-내적 번역·직교=내적 0의 대수적 정의), 내적 공리 3종 + 함수 공간 ∫fg 확장(푸리에 직교기저 연결), 연습 5문제 |
| 42 | [exploration_42_derivative_tensor_hierarchy.md](./exploration_42_derivative_tensor_hierarchy.md) | 이슈 45 실험 준비 중 브로 질문 (2026-09-02) | 고차 미분의 위계: n^k 성분과 이름 없는 3계 — ★ k계 성분 수 = n^k (미분마다 n배, 브로 추측 확인), 기하는 k차 하이퍼큐브 꼭짓점 (벡터→정사각형→정육면체→테서랙트, 브로 직관), gradient·Hessian까지만 이름 있고 3계부터 고유명 없음 (수요 부재 — 4차 큐브엔 테서랙트란 이름이 있는데 ㅋㅋ), ★ 성분(지수 2^k) ≠ 정보량(중복조합 C(n+k-1,k), 2변수는 k+1로 선형) — Schwarz가 접는데 autodiff는 모르고 중복 계산 (sin·cos hyx=hxy 실증), 그래프 관점: k계 층 덩어리 n^(k-1)개 (서브그룹핑 관찰과 연결), 단변수 n=1은 성분 1개 특수 케이스 (x² 실험의 비밀), HVP 우회의 3차 확장은 수요 없어 미진화 |
| 43 | [exploration_43_graph_inheritance_tour.md](./exploration_43_graph_inheritance_tour.md) | 이슈 45 투어 총정리 (2026-09-04) | 다층 그래프 투어와 상속의 구조 — ★ 함수 5종 관찰 (abs 부호참조·값복사→2계 단결, identity 동형이나 값의 역사 다름, sin 재료 2주기·선형 성장, tanh 곱셈 분기 공범·재사용에도 지수, x²+y² 대각만), ★ 3패턴 법칙 (k행의 열 = 미분식의 참조, 참조는 곱에서만 태어난다 — 곱=강한/덧셈=약한 연결, 브로 직관), ★★ 흡수 법칙 (k계는 참조된 변수→태생 함수 사슬만 흡수 — g1∩g3=0/g2∩g3=2 id 동일, 복제 아닌 재참조), seed 법칙 (씨앗 수 = backprop 호출 횟수), all층수(새것만) vs last전체수 미스터리 해답, 지방 노드(1곱셈·torch.compile 영역), 0지점 함정(gradient check 사각지대), 브로 혼동 포인트 4종 |
| 44 | [exploration_44_geometry_linear_algebra_dictionary.md](./exploration_44_geometry_linear_algebra_dictionary.md) | 이슈 45 투어 후 대각선 질문에서 (2026-09-04) | 기하 ↔ 선형대수 대응 사전 — ★ 수 모음이 기하가 되는 오묘함의 해소 (데카르트의 번역, 표현vs의미 — 노트 37 이중성과 같은 층), 측정 3종 (길이=노름·각=내적·면적/부피=det 부피배율), 변환 4종 (평행이동=벡터덧셈·닮음=스칼라곱·회전행렬·반사 det=-1), 심화 (그림자=사영→최소제곱, 뾰족함=고유값→PCA + sharpness≠convexity 구분, 무게중심=평균), ★ §3 행렬 무늬 도감 (대각 백슬래시 vs 반대각 슬래시·삼각=한방향 의존·밴드=이웃 결합·토블리츠=이동 불변·조밀=완전연결층 — 무늬=계산 난이도 지도, 무늬의 대칭=도형의 대칭: 대칭행렬=선대칭 종이접기·Schwarz, 토블리츠=벽지 평행이동, 순환=회전), 연결 지도 (헤시안=곡률·3패턴, 그래디언트=기울기, 대각선=비대각의 비인접 연결 재해석) |
| 38 | [exploration_38_mixed_radix_fft_music.md](./exploration_38_mixed_radix_fft_music.md) | 이슈 43 곁가지 (노트 37 저녁 수다 → 2026-08-30 아침 브로 망상) | 혼합 진법에서 FFT와 화성학까지 — ★ 지도 노트 (준비 단계, 나중에 파볼 뼈대). ★ 어드레싱 두 노브: 전치는 strides 항(선형 부분), 음악 모드는 base 상수항(아핀 평행이동). 혼합 진법의 선형대수 클러스터(선형 범함수/쌍대·기저 변환=진법 변환·CRT와 RNS·텐서곱 ℝ^mn≅ℝ^m⊗ℝ^n=reshape의 본체), FFT=reshape의 스포츠(Cooley-Tukey 혼합 기수, 반데르몬드), 음악의 산수=로그+모듈러(피치 클래스=ℤ/12), 다장조={0,2,4,5,7,9,11}·음정 패턴 [2,2,1,2,2,2,1], 7모드(버금)=같은 버퍼의 회전 뷰(concatenate 트릭), 조옮김(ℤ/12 평행이동, 음 변함) vs 모드(음급 회전, 음 불변), MIDI=(옥타브,반음) 혼합 진법, 다섯번째 원=생성원 7, Lewin GIS·Tymoczko·새 리만 PLR 항해 지도, 파볼 후보 5건(FFT 구현·화성학 군론·CRT 실험·모드 뷰 실험·braiding) |

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
