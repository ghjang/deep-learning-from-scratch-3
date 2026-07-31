# 탐구 23 — 컨텍스트 매니저와 contextlib: yield가 with를 만드는 마법

> **시점**: step18 진행 중 (2026-07-31)
> **상태**: 📚 학습용 심화 노트 (Config/no_grad 도입에서 파생)
> **트리거**: step18에서 `@contextlib.contextmanager` + `yield`로 `with no_grad():` 구현.
>   "yield가 어떻게 with를 지원하지?" → 탐구 21번(yield/코루틴)의 자연스러운 후속.
> **관련**: step18 (rezero/steps/step18.py — using_config/no_grad), 탐구 21번 (yield/제너레이터)

## 📌 왜 이 탐구를 했나

step18에서 메모리 절약을 위해 `with no_grad():` 컨텍스트 매니저를 도입.
구현부를 보면:

```python
@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield                       # ★ 여기서 멈추고 with 블록 실행?
    finally:
        setattr(Config, name, old_value)
```

★ 의문 3종:
1. `yield`가 값 안 내보내는데 뭘 하는 건가? (제너레이터 아닌가?)
2. `@contextlib.contextmanager`가 어떻게 이걸 `with` 지원 객체로 바꾸나?
3. `try/finally`는 어떻게 with 블록 종료(또는 예외) 시 실행되나?

본 노트에서 깊이 파자. 핵심은 **"yield는 값을 내보내는 용도만이 아니다"** — 실행 일시정지 지점으로서의 역할.

---

## 1. 컨텍스트 매니저란 — `with`의 본질

### 정의

**"들어갈 때(__enter__)와 나갈 때(__exit__) 특정 동작을 수행하는 객체"**.

```python
with expression as var:
    body
# 내부적으로:
mgr = expression
var = mgr.__enter__()
try:
    body
finally:
    mgr.__exit__(...)
```

### 전형적 사례 — 파일

```python
with open('file.txt') as f:
    data = f.read()
# f.__exit__에서 자동으로 파일 닫힘 (예외 나도 닫힘)
```

★ 핵심 가치:
- **자원 획득/해제 쌍** 보장 (open/close, lock/unlock, set/reset)
- **예외 안전** — body에서 예외 나도 `__exit__`은 무조건 실행
- **가독성** — "이 블록 동안만 이 상태"가 코드 구조로 드러남

---

## 2. ★ 전통적 구현 — `__enter__`/`__exit__` 클래스

### 패턴

```python
class MyContextManager:
    def __enter__(self):
        print("진입 — 자원 획득/설정")
        return self    # as var에 들어갈 값

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("탈출 — 자원 해제/복구 (예외 나도 무조건 실행)")
        return False   # True면 예외 삼킴, False면 예외 전파

# 사용
with MyContextManager() as mgr:
    print("블록 본문")
```

출력:
```
진입 — 자원 획득/설정
블록 본문
탈출 — 자원 해제/복구 (예외 나도 무조건 실행)
```

### 단점 — 클래스가 무거움

단순 "set/reset" 같은 패턴도 클래스 2개 메서드 정의해야 함. Pythonic하지 않다는 평가.
→ 그래서 등장한 게 `@contextlib.contextmanager`.

---

## 3. ★★ `@contextlib.contextmanager` + `yield` 마법

### 핵심 아이디어

제너레이터의 `yield`가 **"진입/탈출 경계"** 역할을 하도록 재해석:

```python
@contextlib.contextmanager
def my_cm():
    print("진입 — 자원 획득/설정")     # __enter__ 역할
    try:
        yield "value"                   # ★ yield 지점 = with 블록 본문 실행 지점
    finally:
        print("탈출 — 자원 해제/복구")   # __exit__ 역할
```

- **yield 이전 코드** = `__enter__`
- **yield 값** = `as var`에 들어갈 값
- **yield 이후 코드** = `__exit__` (finally로 예외 안전)
- **yield 지점** = with 블록 본문 실행 중

### 사용

```python
with my_cm() as v:
    print(f"블록 본문, v={v}")
```

출력:
```
진입 — 자원 획득/설정
블록 본문, v=value
탈출 — 자원 해제/복구
```

★ 마법: `yield`가 "값 내보내기"가 아니라 **"여기서 with 블록 본문에 제어 넘기고, 끝나면 돌아와"** 라는 **동기점(synchronization point)** 으로 쓰임.

---

## 4. ★★ 내부 메커니즘 — 어떻게 with를 지원하나

이게 브로 질문의 핵심. `@contextlib.contextmanager` 데코레이터가 제너레이터 함수를 with-지원 객체로 변환.

### 단계별 흐름

```python
@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield
    finally:
        setattr(Config, name, old_value)
```

#### `with using_config(...)` 진입 시:

1. `using_config(name, value)` **호출** → 제너레이터 객체 생성 (아직 본문 실행 X)
2. 데코레이터가 만든 `_GeneratorContextManager` 래퍼가 그 제너레이터 들고 있음
3. `__enter__` 호출 → 제너레이터의 `next()` 호출 → **yield까지 실행**
   - `old_value = getattr(...)` 실행
   - `setattr(Config, name, value)` 실행 (설정 변경)
   - `yield` 도달 → **일시정지**, 제어 `with` 블록으로

#### with 블록 본문 실행:

```python
with using_config('enable_backprop', False):
    x = Variable(...)    # ← 여기가 with 블록 본문
    y = square(x)        #   Config.enable_backprop = False 상태로 실행
```

#### with 블록 종료 (정상 또는 예외):

4. `__exit__` 호출 → 제너레이터의 `next()` (또는 `throw()`) 호출 → **yield 이후부터 재개**
   - `finally` 블록 실행 → `setattr(Config, name, old_value)` (설정 복구)
   - 제너레이터 종료 (StopIteration)
5. 만약 with 블록에서 예외 → `__exit__`가 `throw(exc)`로 제너레이터에 예외 주입 → yield에서 예외 발생 → `finally` 실행

### ★ 핵심 통찰 — "yield는 동기점"

일반적 제너레이터에선 yield가 "값 내보내기". 컨텍스트 매니저에선 **"호출자에게 제어 넘기고, 다시 호출되면 이어서"**.

이게 탐구 21번의 "코루틴 = 진입/탈출 다수" 개념과 연결:
- 일반 함수: 진입 1, 탈출 1 (return)
- 제너레이터/코루틴: 진입/탈출 다수 (yield)
- 컨텍스트 매니저의 yield: 딱 1번의 "진입→본문→탈출" 코루틴 패턴 특수형

→ **"yield = 실행 일시정지 지점"** 이라는 본질이 컨텍스트 매니저 구현에 빛을 발함.

---

## 5. ★ step18 `using_config` 코드 재해석

```python
@contextlib.contextmanager
def using_config(name: str, value: object) -> None:
    old_value = getattr(Config, name)     # ① 진입 전 — 원래값 백업
    setattr(Config, name, value)          # ② 진입 전 — 새값 설정

    try:
        yield                             # ③ with 블록 본문에 제어 넘김 (일시정지)
    finally:
        setattr(Config, name, old_value)  # ④ 탈출 — 원래값 복구 (예외 나도)
```

각 단계 매핑:
| 단계 | 역할 | 언제 실행 |
|---|---|---|
| ① 백업 | 원래값 저장 | with 진입 직전 |
| ② 설정 | 새값 적용 | with 진입 직전 |
| ③ yield | with 본문 실행 (일시정지) | with 블록 |
| ④ 복구 | 원래값 복구 | with 탈출 (예외 포함) |

★ `try/finally` 핵심: with 블록에서 예외 나도 ④가 실행됨. 이게 "Config.enable_backprop = False로 둔 채 예외 터지면 전체 프로그램이 역전파 안 함 사태"를 막음.

---

## 6. ★ 왜 `yield`가 값 안 내보내나? — 제너레이터와의 차이

브로 질문 핵심: "yield가 값을 안 내보내는데 뭘 하는 건가?"

### 두 가지 yield 용도

| 용도 | 형태 | 사례 |
|---|---|---|
| **값 내보내기** (이터레이터) | `x = yield value` | `def gen(): yield 1; yield 2` |
| **제어 양보** (컨텍스트 매니저) | `yield` (값 없음) | `def cm(): ...; yield; ...` |

★ 컨텍스트 매니저의 `yield`는 값을 안 내보냄. 그럼 왜 yield인가?
→ "여기서 일시정지하고 호출자(with 블록)에게 제어 넘기고, 다시 호출되면 이어서" 라는 **코루틴적 의미**.

`as var`에 값 넘기려면: `yield value` (using_config에선 값 안 써서 `as` 안 씀).

### 탐구 21번과의 연결

탐구 21번에선 "yield = 코루틴의 씨앗" 이라고 했음. 컨텍스트 매니저가 그 증거:
- yield의 "일시정지/재개" 능력이 with 블록 진입/탈출을 자연스럽게 구현
- 값 내보내기는 yield의 부가 기능일 뿐, 본질은 **"실행 지점 저장"**
- 컨텍스트 매니저는 이 본질을 활용한 가장 우아한 사례 중 하나

---

## 7. ★ `no_grad()` — 컨텍스트 매니저 합성

```python
def no_grad() -> contextlib._GeneratorContextManager[None]:
    return using_config('enable_backprop', False)
```

★ 핵심: `no_grad()`는 using_config를 **호출만** 함. 데코레이터 아님.
`using_config(...)`가 `_GeneratorContextManager` 객체를 반환하니까, 그걸 그대로 반환.
→ `with no_grad():` 가 `with using_config('enable_backprop', False):` 와 동일.

이게 "사용자 친화적 이름" 제공하는 일반적 패턴:
- 일반형: `using_config(name, value)` — 어떤 Config 속성이든
- 특수형: `no_grad()` — 가장 흔한 케이스(enable_backprop=False)의 짧은 이름

PyTorch도 동일: `torch.no_grad()`, `torch.enable_grad()`, `torch.set_grad_enabled()` 전부 같은 패턴.

---

## 8. ★ 다른 컨텍스트 매니저 사례들 — 패턴 인식

컨텍스트 매니저는 파이썬 전반에 스며들어 있어:

### 표준 라이브러리

```python
# 파일 (자동 close)
with open('f.txt') as f: ...

# 락 (자동 unlock)
import threading
with threading.Lock() as lock: ...

# decimal 정밀도 (자동 복구)
import decimal
with decimal.localcontext() as ctx:
    ctx.prec = 20

# 리디렉션 (자동 복구)
import contextlib
with contextlib.redirect_stdout(io.StringIO()): ...
```

### 사용자 정의 흔한 패턴

```python
# 타이머 (진입 시 시작, 탈출 시 출력)
@contextlib.contextmanager
def timer(name):
    import time
    start = time.time()
    try:
        yield
    finally:
        print(f"{name}: {time.time() - start:.2f}s")

with timer("sort"):
    data.sort()
```

### PyTorch 생태계

```python
# 역전파 끄기 (우리 no_grad와 정확히 같은 패턴/이름)
with torch.no_grad():
    y = model(x)    # 추론 — 그래프 안 만듦

# 역전파 켜기 (no_grad 안에서 일부만 다시 켤 때)
with torch.enable_grad():
    ...

# 분산 — 장치 컨텍스트
with torch.device('cuda'):
    ...
```

★ DeZero가 PyTorch 패턴을 충실히 따르는 게 step18에서 가장 잘 드러남.

---

## 9. ★ `async with` — 비동기 컨텍스트 매니저 (확장)

Python 3.5+ 에선 `async with` 로 비동기 컨텍스트 매니저 지원:

```python
class AsyncCM:
    async def __aenter__(self): ...
    async def __aexit__(self, *args): ...

async def main():
    async with AsyncCM() as cm:
        await something()
```

★ `__aenter__`/`__aexit__` (async 버전) 사용. `@contextlib.asynccontextmanager` 도 있음.

우리 step18과 직접 관련은 없지만 (동기), 탐구 21번(async/await)과 연결되는 또 하나의 점.
"yield → async yield" 진화가 "with → async with" 진화와 짝.

---

## 10. 요약 — 브로 질문에 대한 답

| 질문 | 답 |
|---|---|
| yield가 값 안 내보내는데 뭘 하는 건가? | ★ **"제어 양보 지점"**. with 블록 본문에 제어 넘기고, 블록 끝나면 이어서. 값 내보내기는 부가 기능일 뿐. |
| `@contextlib.contextmanager`가 어떻게 with를 지원하나? | 제너레이터 함수를 `_GeneratorContextManager`로 감쌈. `__enter__`에서 next()로 yield까지, `__exit__`에서 next()/throw()로 yield 이후 실행. |
| try/finally는 어떻게 예외 시에도 실행되나? | `__exit__`이 with 블록의 예외를 잡아 제너레이터에 `throw()`로 주입. yield에서 예외 발생하므로 finally 실행. |

### 핵심 키워드 세 줄 요약

- **yield의 본질 = "실행 일시정지 지점"** (값 내보내기는 부가)
- **`@contextmanager` = yield를 진입/탈출 경계로 재해석** (제너레이터 → with 지원)
- **`with`의 가치 = 자원 획득/해제 쌍 보장** (예외 안전, 가독성, PyTorch 패턴과 일치)

---

## 11. 🔓 더 파고 싶으면 (확장 후보)

| 주제 | 키워드 | 방향 |
|---|---|---|
| **`_GeneratorContextManager` 내부** | CPython 구현, `__enter__`/`__exit__` | contextlib.py 소스 읽기 |
| **`ExitStack`** | 동적 컨텍스트 매니저 합성 | 여러 CM을 조건부로 묶을 때 |
| **`contextlib.suppress`** | 특정 예외 무시 | `with suppress(FileNotFoundError): ...` |
| **`@contextmanager` vs 클래스 CM** | 성능, 가독성, 디버깅 | 어느 쪽이 언제 나은가 |
| **`async with`/`asynccontextmanager`** | 비동기 자원 | 탐구 21(async/await)과 연결 |
| **PyTorch no_grad 내부** | torch.C._set_grad_enabled | C++ 레벨 구현 비교 |
| **스레드 안전성** | thread-local Config | PyTorch/JAX의 분산 학습에서 no_grad 동기화 |

### 회수 시그널

- 다른 step에서 `with` 마주칠 때 → 본 노트 §1, §2 (기본)
- `@contextmanager` 또는 yield-with 패턴 → 본 노트 §3, §4 (마법)
- async/await 다시 볼 때 → 본 노트 §9 (async with)
- "yield가 값을 안 내보내는데?" → 본 노트 §6 (두 가지 yield 용도)

---

## 🔑 핵심 키워드

`#컨텍스트매니저` `#context-manager` `#with` `#__enter__` `#__exit__` `#contextlib` `#contextmanager` `#yield` `#제어양보` `#실행일시정지` `#_GeneratorContextManager` `#try-finally` `#예외안전` `#자원획득해제` `#no_grad` `#using_config` `#PyTorch패턴` `#async-with` `#탐구21연결` `#step18파생`

## 📝 학습 완료일 / 관련 링크

- **완료일**: 2026-07-31 (step18 진행 중)
- **트리거**: step18 `@contextlib.contextmanager` + `yield`로 `with no_grad():` 구현
- **관련 코드**: rezero/steps/step18.py (Config, using_config, no_grad)
- **관련 노트**: exploration_21 (yield/제너레이터/코루틴 — 본 노트의 전편, yield 본질과 연결)
- **관련 생태계**: PyTorch torch.no_grad()/torch.enable_grad() (동일 패턴)
