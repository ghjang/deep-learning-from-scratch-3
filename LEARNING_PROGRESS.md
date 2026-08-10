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

- **완료**: 20 / 60 (step01~20 ✅)
- **진행 중**: 0
- **막힘**: 0
- **마지막 업데이트**: 2026-08-10 — step20 완료 (연산자 오버로드(1) — __add__/__mul__ 클래스 안 정의 + Mul derivative hook)

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
| step21 | 연산자 오버로드(2) | ⏳ | - | - | - |
| step22 | 연산자 오버로드(3) | ⏳ | - | - | - |
| step23 | packages로 묶기 (dezero 패키지화) | ⏳ | - | - | - |
| step24 | 복잡한 함수 표현 (Sphere, Rosenbrock) | ⏳ | - | - | - |

## 🏔 제 3 고지 — 고차 미분 계산 (step25 ~ 36)

| Step | 주제 | 상태 | Issue | 완료일 | 메모 |
|---|---|---|---|---|---|
| step25 | '정답지 같은' 코드 [No code] | ⏳ | - | - | - |
| step26 | DeZero의 핵심 (core_simple.py 직접 구현) | ⏳ | - | - | - |
| step27 | 지수/로그 함수 (Exp, Log) | ⏳ | - | - | - |
| step28 | 함수 최적화 (경사하강법) | ⏳ | - | - | - |
| step29 | 뉴턴 방법 (2차 최적화) | ⏳ | - | - | - |
| step30 | 최적화 자동화 (2차 미분 자동) | ⏳ | - | - | - |
| step31 | 다른 최적화 기법 (직접 구현) [No code] | ⏳ | - | - | - |
| step32 | 다른 함수 최적화 (뉴턴 적용) | ⏳ | - | - | - |
| step33 | 행렬의 미분 이론 | ⏳ | - | - | - |
| step34 | 벡터의 내적 / 행렬의 곱 | ⏳ | - | - | - |
| step35 | 행렬의 미분 구현 (MatMul) | ⏳ | - | - | - |
| step36 | 고차 미분 이론 | ⏳ | - | - | - |

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
