# 📊 LEARNING_PROGRESS.md

『밑바닥부터 시작하는 딥러닝 ❸』 학습 진척도 추적
================================================

> 이 파일은 **목차** 역할. 각 step의 세부 진행/질문/토론은 GitHub Issue로.
> 새 AI 세션에서 이 파일을 먼저 읽으면 "어디까지 했는지" 즉시 파악 가능.

## 🎯 워크플로

1. **새 step 시작** → 💬 학습 질문 템플릿으로 이슈 생성, 아래 표에 이슈 링크 등록
2. **step 진행 중** → 이슈 안에서 질문/토론 + `LEARNING_NOTES.md`에 자유 노트
3. **step 완료** → 이슈 close, 상태 ✅로 변경, 노트에 한 줄 요약 추가

## 📍 상태 범례

| 이모지 | 의미 |
|---|---|
| ⏳ | 아직 시작 전 |
| 🔄 | 진행 중 |
| ✅ | 완료 |
| ⚠️ | 막힘 (도움 필요) |
| ⏭ | 건너뜀 |

## 📈 전체 요약

- **완료**: 36 / 60 (step01~36 ✅)
- **진행 중**: 0
- **막힘**: 0
- **마지막 업데이트**: 2026-08-24 — ★★★ step36 완료 = 제 3고지 (step25~36, 고차 미분 계산) 점령! 하루에 step33/34/35/36 4개 완료. / 같은 날 밤: 이슈 43 작업 1+2 완료 — 탐구 노트 34 "야코비안은 흐르지 않는다" 승격 (후보 10번+8번 잔여 회수, 수치 실증 포함)
- ★ **다음 작업** (2026-08-28 저녁 갱신 — 새 세션용 인수인계): **① 노트 37(전치·다차원 어드레싱) 브로 정독 + 점검표 38문항 도전** — 작성 완료 + 대화 보강 완료(2026-08-28: concept image, 혼합 진법, 수학자의 전치 정의, 내적 보존 유도, 미분=선형 근사, std::vector·캐스팅=view/reshape, 어드레싱=내적·strides 자유도 / 2026-08-30 정독 중: axis 국어 사전·3D contraction·축 해석 프로토콜·reshape 해부·트리 뷰(브로 아이디어 — 당기기 규약·포함 관계·S₂/S₃ 원소 나열 포함)·두 클럽 정리·NCHW 재조직화·큐브 배치도, 문항 30→38), 브로가 읽고 답하는 단계. ② [이슈 49 — fill_grad 이름 확정](https://github.com/ghjang/deep-learning-from-scratch-3/issues/49) (4고지 전 타이밍 중요). ③ [이슈 45](https://github.com/ghjang/deep-learning-from-scratch-3/issues/45) 다층 그래프 도구 → [이슈 48](https://github.com/ghjang/deep-learning-from-scratch-3/issues/48) Hessian 실험 → 후보 12(미분 그래프 4종) — 이 3건 세트로 하면 시너지. ④ [이슈 46](https://github.com/ghjang/deep-learning-from-scratch-3/issues/46) 던더 믹스인. ⑤ [이슈 47](https://github.com/ghjang/deep-learning-from-scratch-3/issues/47) MatMul 이중 구현 (step41 시점). ⑥ 작업 3(v0) or 5(연습문제) — 브로 선택. ⑦ [노트 39 — 고차원 전치 연습장](https://github.com/ghjang/deep-learning-from-scratch-3/blob/master/notes/exploration_39_highdim_transpose_gym.md) (2026-08-30 신설, 브로 요청 — 4D·5D 묶음 읽기 훈련, step38 직전이 최적 타이밍). ⑧ [노트 40 — 순열 행렬 실험실](https://github.com/ghjang/deep-learning-from-scratch-3/blob/master/notes/exploration_40_permutation_matrices.md) (2026-08-31 신설, 브로 흥미 — 생성법·생성원·케일리 표, 언제든 놀이터). ⑨ [노트 41 — 내적](https://github.com/ghjang/deep-learning-from-scratch-3/blob/master/notes/exploration_41_inner_product.md) (2026-08-31 신설, 브로 요청 — 두 얼굴·수반·행렬 판·코사인 유사도, 4고지 전 기초 화력). ★ 완료: 이슈 43 작업 1~4 전부 종결 (노트 34/35/36/37, UML 7종, gradient check, 유형 지도). [Issue 43](https://github.com/ghjang/deep-learning-from-scratch-3/issues/43) / [Issue 44](https://github.com/ghjang/deep-learning-from-scratch-3/issues/44)
- ★ **step25/26 특이사항 (해결됨)**: step25 작업 시 step26 영역(Goldstein 그래프 출력)까지 선행 커버했었음 (정답지 배분 착각). 2026-08-19 브로 책 재확인으로 step26 본문에 코드 외 새 개념 없음 확인 → step26 공식 ✅ 처리 완료. 시각화 2부작 종결.

---

> **고지 구성** (총 60 step + 부록 A/B/C)
> - **제 1 고지 미분 자동 계산**: step01 ~ 10
> - **제 2 고지 자연스러운 코드로**: step11 ~ 24
> - **제 3 고지 고차 미분 계산**: step25 ~ 36
> - **제 4 고지 신경망 만들기**: step37 ~ 51
> - **제 5 고지 DeZero의 도전**: step52 ~ 60
> - **부록**: A / B / C

## 🏔 제 1 고지 — 미분 자동 계산 (step01 ~ 10)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step01 | 상자로서의 변수 | ✅ | [#2](https://github.com/ghjang/deep-learning-from-scratch-3/issues/2) | 2026-07-21 | Variable 래퍼 패턴, ndarray 차원 |
| step02 | 변수를 낳는 함수 (Function 도입) | ✅ | [#3](https://github.com/ghjang/deep-learning-from-scratch-3/issues/3) | 2026-07-23 | Function/Template Method, 패턴 노트 신설, abc 탐구 |
| step03 | 함수 연결 | ✅ | [#4](https://github.com/ghjang/deep-learning-from-scratch-3/issues/4) | 2026-07-23 | Exp 추가, 함수 연쇄=계산그래프, abc+@override 실험 |
| step04 | 수치 미분 | ✅ | [#5](https://github.com/ghjang/deep-learning-from-scratch-3/issues/5) | 2026-07-24 | numerical_diff 중앙차분, self.input/output 복선, 탐구 3종 (#10/#11/#12) |
| step05 | 역전파 이론 [No code] | ✅ | [#6](https://github.com/ghjang/deep-learning-from-scratch-3/issues/6) | 2026-07-28 | 역전파=chain rule, 계산그래프, 국소적 미분; 탐구 3종 (#13 표기법+fold 통찰 / #14 용어 / #15 기호 어원) |
| step06 | 수동 역전파 (Variable.grad, Function.backward) | ✅ | [#7](https://github.com/ghjang/deep-learning-from-scratch-3/issues/7) | 2026-07-29 | 수동 역전파=right fold unfold; step04 복선 회수; 변형 3종(gy/gx→upstream/downstream+local_deriv, grad Optional 힌트, backward @abstractmethod); REZERO_CHANGES.md 신설 |
| step07 | 역전파 자동화 (재귀적 right fold) | ✅ | [#8](https://github.com/ghjang/deep-learning-from-scratch-3/issues/8) | 2026-07-29 | 역전파 자동화=재귀 right fold; Define-by-Run 완성; 변형 5종(#010~#014: apply/derivative hook 대칭, derivative callable, backward 전역 함수 JAX 스타일); #001 회수(타입 힌트 세트); Known Gotcha 10 재발+방어망 강화; RESEARCH_QUEUE 6 등록 |
| step08 | 재귀에서 반복문으로 역전파 고속화 | ✅ | [#9](https://github.com/ghjang/deep-learning-from-scratch-3/issues/9) | 2026-07-29 | 반복문(worklist) 전환; 변형 3종(#015 fill_grad 개명, #016 assert→RuntimeError+도입부, #017 worklist 리네임+타입); 패턴 2종(점진적 설계 복선, Worklist Algorithm); debugging/coding_style 노트 신설; 탐구 16번(side effect 번역 비판); 브로 코드 리뷰 7연타 |
| step09 | 함수를 더 편리하게 (Function 클래스 사용성 개선) | ✅ | [#10](https://github.com/ghjang/deep-learning-from-scratch-3/issues/10) | 2026-07-29 | as_array+wrapper(square/exp)+isinstance 방어막3겹 도입; pipe 헬퍼(FP 합성); coding_style.md 6항목(Pythonic 시리즈); RESEARCH_QUEUE #6 거의 완벽 가이드로 자람(Define-by-Run 본질, 가중치 매핑, 그래프 비용, torch.compile); AGENTS.md "책 vs rezero+AI" 학습 철학 추가; 브로 코드 리뷰 12연타 |
| step10 | 테스트 (unittest로 동작 검증) | ✅ | [#11](https://github.com/ghjang/deep-learning-from-scratch-3/issues/11) | 2026-07-29 | pytest 도입(국룰, 탐구 17번); numerical_diff + gradient check (step04 복선 회수); 방어막 None 가드 일관 적용(5곳 assert); debugging.md "정적 분석과 협력하는 assert" 보강; 1고지 "완결성 인증" ★ |

## 🏔 제 2 고지 — 자연스러운 코드로 (step11 ~ 24)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step11 | 가변 길이 인수(순전파 편) | ✅ | [#12](https://github.com/ghjang/deep-learning-from-scratch-3/issues/12) | 2026-07-30 | 다입력 Add; 방향 (B) apply hook 다변 일반화 성공; pipe 보류(#13); FP 유틸 이슈(#14) 파생; 언패킹 탐구(exploration_07 A.7) |
| step12 | 가변 길이 인수(개선 편) | ✅ | [#15](https://github.com/ghjang/deep-learning-from-scratch-3/issues/15) | 2026-07-30 | *inputs 가변 인수; apply도 *xs 통일(브로 통찰); 출력 단일화; assert isinstance(wrapper); 탐구 3건(A.7.5 이중성, C.1.4 오버라이드 시그니처 자유, debugging Type Narrowing 변형) |
| step13 | 가변 길이 인수(역전파 편) | ✅ | [#16](https://github.com/ghjang/deep-learning-from-scratch-3/issues/16) | 2026-07-30 | 3부작 대미; fill_grad 다변 입력 진화; Add derivative 상수함수(브로 통찰); self.output 단수(#019); "다변≠다출력" 혼동 교훈; 역전파 주석 정비(#020, step23 회수) |
| step14 | 같은 변수 반복 사용 | ✅ | [#17](https://github.com/ghjang/deep-learning-from-scratch-3/issues/17) | 2026-07-30 | gradient 누적(if None 패턴); clear_grad() 도입(#021 네이밍 일관성); downstream_grads 네이밍(#007); Define-by-Run 가정 명시; ndarray in-place 방지(명시적 +) |
| step15 | 복잡한 계산 그래프(이론 편) | ✅ | [#18](https://github.com/ghjang/deep-learning-from-scratch-3/issues/18) | 2026-07-30 | [No code]; exploration_18 풍성한 탐구(그래프/DAG/DFS/BFS/위상정렬); 브로 통찰 3개(DAG 2개 겹침, 노드/간선 매핑, generation=표현식중첩깊이); step16 구현 준비 완료 |
| step16 | 복잡한 계산 그래프(구현 편) | ✅ | [#19](https://github.com/ghjang/deep-learning-from-scratch-3/issues/19) | 2026-07-31 | generation + visited + schedule; 복선 회수(항목 012, 탐구 18 §4.4); 네이밍 셋트(worklist/visited/schedule); 크로스참조 네이밍 시도/철회 교훈(항목 025, 탐구 19); 탐구 20/21(Node/이터레이터/코루틴 파생) |
| step17 | 메모리 관리와 순환 참조 | ✅ | [#22](https://github.com/ghjang/deep-learning-from-scratch-3/issues/22) | 2026-07-31 | weakref(약한 참조)로 순환 참조 끊기; output 이름 유지+타입힌트 진화(항목 026); 브로 4연속 원칙 위반 캐치(output_ref 헝가리안, upstream_grad 변수명, Gotcha #10, 주석 gy); 탐구 22(weakref/GC/CPython 내부) |
| step18 | 메모리 절약 모드 | ✅ | [#23](https://github.com/ghjang/deep-learning-from-scratch-3/issues/23) | 2026-07-31 | Config 전역 플래그 + contextlib 컨텍스트 매니저(no_grad); retain_grad 중간 grad 버리기(항목 014 확장); 탐구 23(contextmanager/yield)+24(전략/팩토리/결정시점 5층위); AGENTS.md 보강(제목 확인 절차/원칙); pyproject.toml pyright 설정 |
| step19 | 변수 사용성 개선 | ✅ | [#24](https://github.com/ghjang/deep-learning-from-scratch-3/issues/24) | 2026-08-10 | name + __len__/__repr__ + shape/ndim/size/dtype (위임 패턴); _ensure_data None 가드(항목 029); name 키워드 전용(항목 028); Variable( 대문자 repr(항목 030) |
| step20 | 연산자 오버로드(1) | ✅ | [#25](https://github.com/ghjang/deep-learning-from-scratch-3/issues/25) | 2026-08-10 | __add__/__mul__ 클래스 안 정의(항목 031, pyright 11→0 에러); Mul derivative hook 확장(항목 032, 항목 013 재평가 통과); coding_style 섹션 7 + AGENTS.md 작업 원칙 추가 |
| step21 | 연산자 오버로드(2) | ✅ | [#26](https://github.com/ghjang/deep-learning-from-scratch-3/issues/26) | 2026-08-10 | __radd__/__rmul__ 클래스 안 정의(항목 034); __array_priority__=200 버림(항목 033, 탐구 25); wrapper as_array 중복 제거; 탐구 25번 작성(__array_priority__/ufunc 역사); 문서 대공사 11건 + 이슈 27 등록 |
| step22 | 연산자 오버로드(3) | ✅ | [#28](https://github.com/ghjang/deep-learning-from-scratch-3/issues/28) | 2026-08-10 | Neg/Sub/Div/Pow 4종 + 매직메서드 7종 (항목 031/033/034 자동 적용 검증); Pow super().__init__ DRY(항목 035); Neg 단순화(브로드캐스팅); Div derivative hook(항목 013 재평가 통과); 탐구 26번(숫자 계보/오일러/무한미분↔기울기소실) |
| step23 | 패키지로 정리 | ✅ | [#29](https://github.com/ghjang/deep-learning-from-scratch-3/issues/29) | 2026-08-10 | rezero/v1/ 패키지 생성(브로 버전 폴더 전략); 순환 참조 해결(지연 import); 빈 템플릿 11개 삭제; 주석 정리(API화); 항목 #036 회수; 부분 — 이슈 [#27](https://github.com/ghjang/deep-learning-from-scratch-3/issues/27)(AGENTS.md 구조 개선) 일부 처리(디렉터리 구조/대응표/정체성/작업흐름 개서), 섹션 분할은 step25+로 연기 |
| step24 | 복잡한 함수의 미분 | ✅ | [#30](https://github.com/ghjang/deep-learning-from-scratch-3/issues/30) | 2026-08-10 | Sphere/Matyas/Goldstein 벤치마크; v1 패키지 사용 증명 (step 한정 함수, vX 승격 안 함); gradient check 통과; ★ 2고지 점령! |

## 🏔 제 3 고지 — 고차 미분 계산 (step25 ~ 36)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step25 | 계산 그래프 시각화(1) | ✅ | [#31](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31) | 2026-08-11 | Graphviz DOT 시각화 4종 (fold_dot_graph + plot_dot_graph); 변형 7종 (fold 네이밍, weakref 단수, subprocess 안전, IPython 제거, f-string, output/ 폴더, show_value); 변수명 볼드 (HTML-like label); 포맷 화이트리스트 (png/svg/pdf); 순회 공통화 발견 → 이슈 32번/33번. ★ step25/26 코드 배분 착각으로 step26 영역(Goldstein 출력)까지 선행 커버 — 2026-08-19 step26 공식 ✅ 처리로 해결. 상세는 LEARNING_NOTES step25 / 이슈 31번 코멘트. |
| step26 | 계산 그래프 시각화(2) | ✅ | [#31](https://github.com/ghjang/deep-learning-from-scratch-3/issues/31) (step25가 커버) | 2026-08-19 | ★ step25에서 선행 커버 완료 (Goldstein 그래프 출력 = 정답지 step26 코드 전부). 별도 이슈 없음 — step26.py는 리다이렉트 docstring만. 브로 책 재확인: step26 본문에 코드 외 새 개념 없음 |
| step27 | 테일러 급수 미분 | ✅ | [#34](https://github.com/ghjang/deep-learning-from-scratch-3/issues/34) | 2026-08-19 | Sin 승격 (v1 첫 수학 함수) + my_sin 테일러 근사; ★ 근사 다항식 역전파 = cos (Define-by-Run 본질 실증); 시각화 개선 2건 (value_format 적응형 + Pow dot_label 훅); 1e-150 풀버전 (노드 377, 삼각형); 테스트 105개 |
| step28 | 함수 최적화 | ✅ | [#35](https://github.com/ghjang/deep-learning-from-scratch-3/issues/35) | 2026-08-19 | 경사하강법 4단계 갱신 루프 (신경망 학습의 원형); Rosenbrock "낙하→크롤링" 실증 (골짜기 편차); 데모 4케이스 (수렴/lr 발산/clear_grad 누락/sphere 대비); ★ 탐구 노트 2종 (27: Rosenbrock+NFL 선택지도 / 28: 방향미분+갱신식 해부); pdoc API 문서 파이프라인; AGENTS.md 제도화 2건 (감동 포인트 사전 도출 + 적합성 메모) |
| step29 | 뉴턴 방법으로 푸는 최적화(수동 계산) | ✅ | [#36](https://github.com/ghjang/deep-learning-from-scratch-3/issues/36) | 2026-08-19 | 뉴턴 갱신 x ← x - f'/f'' (접하는 포물선의 바닥으로 점프); 2차 수렴 실증 (7 iters 기계 정밀도); 국소 최대 함정 실험; 그림 2장 (연쇄 + 어긋난 바닥 클로즈업); ★ 탐구 노트 29 (접촉 3조건 → 곡률 정체 → 물리 평행 "원동력은 2차에 있다"); step30 고차 미분 복선 |
| step30 | 고차 미분(준비 편) | ✅ | - (복습 장 — 별도 이슈 없음) | 2026-08-20 | [No code] 복습/조망 장 — Variable/Function/역전파 구조를 그림·다이어그램으로 재정리 (코드 0건, 브로 책 재독으로 완료). 고차 미분 3부작(31 이론/32 구현) 전 호흡 조절 |
| step31 | 고차 미분(이론 편) [No code] | ✅ | [#37](https://github.com/ghjang/deep-learning-from-scratch-3/issues/37) | 2026-08-20 | double backprop 이론 — grad를 Variable로, 역전파가 미분 계산 그래프 구성 → 재역전파. ★ 탐구 노트 30 (3단 논법 + 머리 꼬임 3지점 해부 + Define-by-Run 자기 참조). 구현은 step32, 수확(뉴턴 자동화)은 step33 |
| step32 | 고차 미분(구현 편) | ✅ | [#38](https://github.com/ghjang/deep-learning-from-scratch-3/issues/38) | 2026-08-20 | ★ rezero v2 탄생 (v1 브랜칭) — grad의 Variable화 + fill_grad(create_graph) + derivative hook Variable 취급. 구조 생존 원칙 (apply/derivative/fill_grad 100% 유지, 타입만 진화). common 모듈 신설 (numerical_diff). Cos 신규. 테스트 219 (v1 105 + v2 114). dezero 대조 일치. 고차 미분 3부작 완결! |
| step33 | 뉴턴 방법으로 푸는 최적화(자동 계산) | ✅ | [#39](https://github.com/ghjang/deep-learning-from-scratch-3/issues/39) | 2026-08-24 | step29의 gx2 손유도 함수가 완전히 사라짐 — `fill_grad(y, create_graph=True)` + `fill_grad(gx)`로 f'' 자동 (v2 첫 수확). 7 iters 기계 정밀도 2차 수렴 + dezero 완전 일치. ★ 후보 8번 등록 (2층 그래프 실제 모양 — step35 회수 예정) |
| step34 | sin 함수 고차 미분 | ✅ | [#40](https://github.com/ghjang/deep-learning-from-scratch-3/issues/40) | 2026-08-24 | 미분 순환 (sin→cos→-sin→-cos) 4곡선 시각화. ★ 벡터/루프 두 버전 대조 (브로 실험 설계) → 3자 대조 전부 True. ★★ 브로 실험이 v1 시절 Neg 버그 발견 (도함수가 아니라 원 함수 반환 — step22부터 은닉, dezero는 멀쩡 = rezero 고유) — v1/v2 수정 + 회귀 테스트 3개 + None 특성 전제 문서화. 큐 후보 8/9번 확장 (그래프 3형태, 용어 이중 구조, v0 아이디어) |
| step35 | 고차 미분 계산 그래프 | ✅ | [#41](https://github.com/ghjang/deep-learning-from-scratch-3/issues/41) | 2026-08-24 | tanh 자기 참조 도함수(1-tanh²)의 고차 미분 그래프 시각화 — 폭증 실증 (Tanh 2^n). ★ 후보 8번 회수 (큐 첫 완주: 같은 x 공유 id 검증 + gy 리프 + 그래프 10장). ★★ 브로 "self.output 왜 안 써?" → 재사용형 발견 → **Config.reuse_output** 2전략 옵션화 (설계 변천: 인스턴스→Config). 탐구 노트 32 (미분식 해부). U+2212 금지 원칙 신설 |
| step36 | 고차 미분 이외의 용도 | ✅ | [#42](https://github.com/ghjang/deep-learning-from-scratch-3/issues/42) | 2026-08-24 | z = gx³+y — 살아있는 그래프 재사용 (미분 식을 새 함수의 부품으로). z'(2)=100 (두 갈래 96+4 합산). ★ 탐구 노트 33 (평가 시점 — 브로 혼란 4연타 정리 + 그래프의 생애). ★★★ 제 3고지 (step25~36) 완료! |

## 🏔 제 4 고지 — 신경망 만들기 (step37 ~ 51)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step37 | 고차 미분 구현 (1) (Variable.data를 ndarray로) | ⏳ | - | - | - |
| step38 | 고차 미분 구현 (2) (연산자 오버로딩/형상) | ⏳ | - | - | - |
| step39 | 뉴런 한 개 역전파 검증 (gradient check) | ⏳ | - | - | - |
| step40 | 신경망 구축 (은닉층, 활성화) | ⏳ | - | - | - |
| step41 | 텐서 (다차원 배열) 다루기 | ⏳ | - | - | - |
| step42 | 토이 데이터셋 (계단 함수 데이터) | ⏳ | - | - | - |
| step43 | 신경망의 전체 그림 (개요) | ⏳ | - | - | - |
| step44 | Dataset 클래스 구현 | ⏳ | - | - | - |
| step45 | DataLoader 구현 (미니배치) | ⏳ | - | - | - |
| step46 | 신경망 추론 (predict) | ⏳ | - | - | - |
| step47 | 학습 루프 (loss, backward, update) | ⏳ | - | - | - |
| step48 | 다층 신경망 (MLP) | ⏳ | - | - | - |
| step49 | Layer 클래스 도입 | ⏳ | - | - | - |
| step50 | Parameter 클래스 도입 | ⏳ | - | - | - |
| step51 | Model 클래스 도입 | ⏳ | - | - | - |

## 🏔 제 5 고지 — DeZero의 도전 (step52 ~ 60)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step52 | MLP 클래스 정리 | ⏳ | - | - | - |
| step53 | VGG16 구현 | ⏳ | - | - | - |
| step54 | ResNet (skip connection) | ⏳ | - | - | - |
| step55 | 합성곱 연산 효율화 이론 [No code] | ⏳ | - | - | - |
| step56 | im2col 이론 [No code] | ⏳ | - | - | - |
| step57 | im2col 구현 (Conv2d) | ⏳ | - | - | - |
| step58 | CNN 구현 (SimpleConvNet) | ⏳ | - | - | - |
| step59 | ResNet 구현 | ⏳ | - | - | - |
| step60 | 마무리 (정리, 다음 단계) | ⏳ | - | - | - |

## 📎 부록 (A / B / C)

> 책 본문 60 step 외의 부록. 주제/상태는 브로가 진도 나갈 때 채우기.

| 부록 | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| A | (주제 미정) | ⏳ | - | - | - |
| B | (주제 미정) | ⏳ | - | - | - |
| C | (주제 미정) | ⏳ | - | - | - |

---

## 🔗 관련 링크

- [Issue #1: MLX 백엔드 지원](https://github.com/ghjang/deep-learning-from-scratch-3/issues/1) — 장기적 방향성
- `LEARNING_NOTES.md` — 자유 형식 학습 노트
- `AGENTS.md` — AI 에이전트용 컨텍스트
- `rezero/` — 직접 구현하는 학습 프레임워크

## 📝 업데이트 가이드

이 파일은 **직접 편집**. step 완료 시:
1. 해당 행의 상태를 ✅로 변경
2. Issue 컬럼에 이슈 번호/링크 입력
3. 완료일 입력
4. 메모에 한 줄 요약 (예: "Variable 클래스 기본 구조 이해")
5. 전체 요약의 완료 카운트 +1
