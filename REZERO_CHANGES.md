# rezero 개선 회계 (Changelog of Improvements)

> 책 원본(`dezero/`, `steps/`) 대비 **rezero에서 적용/고려하는 개선사항**을 추적하는 통.
>
> - **목적**: 학습하면서 떠오르는 "더 안전한 최신 파이썬 피처", "더 읽기 좋은 네이밍" 등의
>   개선 아이디어가 흩어지지 않게 한곳에 모으는 것.
> - **사용법**: 생각나는 대로 `### #NNN` 항목으로 **append**. 번호/위치/상태/한 줄 설명만으로 충분.
> - **★ 회수 분류**: step23(패키지화)에서 돌볼 때 **어디로 가나**가 항목마다 다름:
>
>   | 종류 | 예 | 회수처 |
>   |---|---|---|
>   | 🔵 **라이브러리성** | Variable/Function/Square/Exp 등 프레임워크 핵심 변경 | `rezero/core.py`, `functions.py`로 **승격** |
>   | 🟢 **step 한정** | 특정 step 검증/데모 코드의 네이밍, name shadowing 등 | **그 step에 머무름**, 안 옮김 (예: step04 `f` 재사용 수정) |
>   | 🟡 **유틸성** | `numerical_diff` 같은 독립 함수 | `utils.py` 후보 (책도 그렇게 함) |
>
> - **회수 시점**: 주로 **step23 (패키지화)**. 단, 당장 해당 step에서 적용 가능하면 그때그때 반영해도 OK.
> - **이슈와의 관계**: 이 파일은 **"생각 통"**. 아이디어가 구체화되어 작업 단위가 되면
>   그때 GitHub Issue로 분할. 즉 이슈 = 구체화된 것, 이 파일 = 막연한 것까지 포함.

---

## 📋 상태 범례

| 표시 | 의미 |
|---|---|
| 💡 | 아이디어만 (아직 미결정) |
| 🔄 | 고려 중 / 논의 중 |
| ✅ | 반영 완료 |
| ⏭ | 건너뜀 (포기, 또는 책과 크게 달라져 안 함) |

---

## 🗂 분류 (항목이 쌓이면 패턴 보고 채움)

> 지금은 분류 안 함. 어느 정도 쌓이면 주제별로 그룹화(예: 타입 힌트 / 네이밍 / 추상화 강제력 / ...).

---

## 📝 항목

### #001 — Variable.data 타입 힌트 `np.ndarray`
- **위치**: step01~
- **상태**: 💡 아이디어 (선반영 취소 — 다음 step 적절한 시점으로 이월)
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본은 `self.data = data`로 타입 힌트 없음. `data: np.ndarray` / `self.data: np.ndarray`
  로 명시 → 정적 분석 + 의도 명시.
- **★ 확정 정보**: 책 step37 부터 Variable의 data는 **ndarray로 고정**이 확인됨.
  책 원본(`dezero/core.py:46-48`)은 **런타임 `isinstance` 체크**로 보장:
  ```python
  if data is not None:
      if not isinstance(data, array_types):
          raise TypeError(...)
  ```
  즉 책은 "if문 방어"로 보장. 우리는 **타입 힌트로 정적 보장**을 도입할 예정.
- **⚠️ 선반영 취소 사유 (2026-07-29)**: step06에 일단 `data: np.ndarray`를 넣어봤으나 **취소**.
  이유: `data`에만 타입 힌트 넣고 `forward` 반환 타입 힌트는 안 넣으면,
  Pyright가 `forward` 반환값을 None으로 추론해서 `__call__` 안의 `Variable(y)`에서
  정적 오류 발생 ("None is not assignable to ndarray").
  → #001을 제대로 반영하려면 Variable/Function 시그니처 **전체**를 같이 손봐야 함 (forward 반환 타입 등).
  그건 step06 범위를 넘으므로, **다음 step 적절한 시점**에 Variable/Function 타입 힌트를
  **세트로** 도입하는 것으로 이월.
- **★ 교훈**: 타입 힌트는 부분 도입하면 정적 분석 정합성이 깨질 수 있음. **관련 시그니처를 세트로** 넣을 것.
- **회수**: 다음 step 적절한 시점 (또는 step23 → core.py Variable/Function 승격 시)

### #002 — `input` 매개변수명 → `input_var` (빌트인 섀도잉 회피)
- **위치**: step02~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `Function.__call__(self, input)`에서 `input`은 Python 빌트인(콘솔 입력)을 섀도잉.
  `input_var`로 변경 — "입력 변수" 역할 명확 + 빌트인 충돌 회피.
- **결정 기록**: LEARNING_NOTES.md step02 "결정 기록: __call__ 매개변수 이름" 참고.
- **회수**: step23 → `rezero/core.py` Function.__call__ 승격 시 (이름 최종 결정: `input_var` 유지? `downstream`?)

### #003 — `raise NotImplementedError` → `abc.ABC` + `@abstractmethod`
- **위치**: step03~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본은 `raise NotImplementedError()`로 "자식이 안 구현하면 런타임 에러".
  `abc.ABC` + `@abstractmethod`로 변경 → **인스턴스 생성 시점**에 강제 (더 빠른 실패).
- **상세**: notes/exploration_09_abc_abstract.md (abc vs NotImplementedError 심화 비교)
- **회수**: step23 → `rezero/core.py` Function 승격 시 유지

### #004 — `@override` 데코레이터로 자식 재정의 명시 (Python 3.12+)
- **위치**: step03~
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 자식의 `forward`/`backward`에 `@override` 부착 → 부모 메서드 재정의임을 명시.
  정적 분석 도구(mypy/pyright)가 "부모에 없는 메서드를 @override 했는지" 검증 가능.
  단, **런타임 강제력은 없음** (정적 분석 도구 필요).
- **주의**: `@override` 효과를 보려면 mypy/pyright 설정 필요. 현재 rezero엔 설정 없음 —
  step23 패키지화 시점에 `pyproject.toml`에 정적 분석 도구 설정 추가 검토.
- **상세**: notes/exploration_09_abc_abstract.md §9
- **회수**: step23 → `rezero/core.py` Function + `functions.py` 자식들 승격 시

### #005 — name shadowing 제거 (step04 `f` 변수 재사용)
- **위치**: step04
- **상태**: ✅ 반영
- **종류**: 🟢 step 한정 ★ (라이브러리성 아님)
- **내용**: 책 원본 step04.py에서 `f = Square()` 후 `def f(x):`로 같은 이름 재사용 → IDE 워닝.
  `sq`, `composite_f`로 이름 분리. name shadowing은 실행 순서 의존적이라 순서 바뀌면 깨짐.
- **파생 탐구**: notes/exploration_12_language_binding.md (언어 바인딩/타이핑까지 확장)
- **회수**: ❌ **옮기지 않음** — step04 검증 스크립트 한정 변경이라 step23 패키지화와 무관.
  step04 파일에 머무름. (이런 "step 한정" 변경이 브로가 짚은 핵심 케이스)

### #006 — `numerical_diff` docstring + 블랙박스 관점 주석
- **위치**: step04
- **상태**: ✅ 반영
- **종류**: 🟡 유틸성
- **내용**: 책 원본은 주석 거의 없음. docstring으로 공식/eps 트레이드오프/블랙박스 관점 명시.
  "f의 내부를 몰라도 f(x+h)/f(x-h) 호출로 미분 가능 → autograd 철학" 서술.
- **회수**: step23 → `rezero/utils.py` 승격 후보 (책도 dezero/utils.py에 넣음)

### #007 — 역전파 변수명 `gy`/`gx` → `upstream_grad`/`downstream_grad` + `local_deriv` 분리
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `gx = 2 * x * gy` 한 줄을 두 단계로 분해:
  ```python
  local_deriv = 2 * x                          # ① 자기 도함수 (df/dx) 평가
  downstream_grad = local_deriv * upstream_grad # ② fold step (곱해서 누적)
  ```
  → step05 통찰("역전파 = right fold", "국소적 미분 = df/dx")이 **코드 구조로 드러남**.
- **상세**: notes/exploration_13_derivative_notation.md §8 (gy/gx 헷갈림 분석 + fold 통찰)
- **회수**: step23 → `rezero/core.py` Function.backward 승격 시

### #008 — `Variable.grad` 타입 힌트 `Optional[np.ndarray]`
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: 책 원본 `self.grad = None`은 정적 분석(VSCode Pylance)에서
  `y.grad = np.array(1.0)` 시 "None에 ndarray 대입" 경고.
  `self.grad: Optional[np.ndarray] = None`로 타입 힌트 → 경고 제거 + **라이프사이클 명시**
  (역전파 전 None → 역전파 후 ndarray). PyTorch의 `grad: Optional[Tensor]`와 같은 패턴.
- **검증**: `mypy rezero/steps/step06.py` → `Success: no issues found` ✅
- **회수**: step23 → `rezero/core.py` Variable 승격 시

### #009 — `Function.backward` docstring에 fold 흐름 명시
- **위치**: step06
- **상태**: ✅ 반영
- **종류**: 🔵 라이브러리성
- **내용**: `backward(upstream_grad)`의 의미를 docstring으로 풀어 서술.
  - `upstream_grad`: 상류에서 접어 내려온 누적 미분값 (최종 출력에서부터의 fold)
  - 반환값: 자기 도함수 곱해 한 번 더 접은 새 누적값 (하류로 전달)
  cf. PyTorch `grad_output`/`grad_input`, 학술 용어 upstream/downstream gradient.
- **회수**: step23 → `rezero/core.py` Function.backward 승격 시

---

## 💡 대기 중 아이디어 (구체화 안 됨)

> 생각나는 대로 한 줄씩. 구체화되면 위 항목으로 승격.

- (아직 없음 — 떠오르는 대로 추가)

---

## 🔗 관련 링크

- `AGENTS.md` — rezero 학습 원칙 (dezero 복붙 금지, 변형 실험 환영)
- `LEARNING_NOTES.md` — step별 핵심 통찰 (변형 결정 기록도 여기)
- `notes/exploration_09_abc_abstract.md` — abc vs NotImplementedError 심화 (#003, #004 관련)
- `notes/exploration_13_derivative_notation.md` §8 — gy/gx + fold 통찰 (#007 관련)
- 책 step23 — `dezero/` 패키지화 (회수 시점의 원본 참고)
