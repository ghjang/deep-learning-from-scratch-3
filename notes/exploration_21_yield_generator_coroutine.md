# 탐구 21 — yield, 제너레이터, 코루틴: 파이썬의 "일시정지 가능한 함수" 계보

> **시점**: step16 완료 후 (2026-07-31)
> **상태**: 📚 학습용 심화 노트 (이터레이터 패턴에서 파생)
> **트리거**: 브로 — "이게 그 뭔가 그 '코루틴'인지 뭔지 그거 관련 이야기 아니야? 좀 더 깊게 알아둬서 나쁠 게 없을 듯"
> **관련**: 탐구 노트 20번 §4.5 (옵션 I — 순회 이터레이터 추출)

## 📌 왜 이 탐구를 했나

탐구 노트 20번에서 `fill_grad`의 순회 알고리즘을 제너레이터(`yield`)로 추출하는 옵션을 다뤘음.
그때 브로가 핵심 질문: **"이게 코루틴 그건가?"**

이 질문이 정확한 이유: 파이썬에선 `yield`가 **세 가지 개념의 교차점**이기 때문:
1. **이터레이터 (Iterator)** — 순회 패턴
2. **제너레이터 (Generator)** — `yield`로 만드는 이터레이터
3. **코루틴 (Coroutine)** — 진입/탈출 점이 여러 개인 함수

이 노트는 이 셋의 관계와 진화를 정리. 우리 rezero 순회 이터레이터(옵션 I)가 이 계보의 어디에 속하는지까지.

---

## 1. 출발점 — 이터레이터 패턴 (GoF 디자인 패턴)

### 정의

**"컨테이너의 내부 구조를 드러내지 않고 원소를 순회하게 해주는 패턴"**

```python
# GoF 의사 코드 (언어 무관)
interface Iterator {
    next(): Element       # 다음 원소
    hasNext(): bool       # 더 있나?
}
class ListIterator implements Iterator { ... }

# 사용
while iterator.hasNext():
    process(iterator.next())
```

### 왜 필요한가

- 리스트, 트리, 그래프 등 **다양한 컨테이너를 동일한 방식으로 순회**
- 컨테이너 내부 구조(배열? 연결리스트? 해시?)를 사용자가 몰라도 됨
- 순회 알고리즘과 컨테이너 데이터 구조의 분리 (SoC)

### 파이썬에서

파이썬은 이터레이터 패턴을 **언어 차원에서 내장**. GoF의 `hasNext`/`next` 대신:
- `__iter__()` — 이터레이터 객체 반환
- `__next__()` — 다음 원소 반환, 끝나면 `StopIteration` 예외
- `for x in container:` — 이 프로토콜을 자동 호출

```python
class Range5:
    def __init__(self): self.i = 0
    def __iter__(self): return self
    def __next__(self):
        if self.i >= 5: raise StopIteration
        v = self.i; self.i += 1
        return v

for x in Range5(): print(x)   # 0 1 2 3 4
```

→ 클래스 5줄 필요. 근데 파이썬엔 더 쉬운 길이... ↓

---

## 2. ★ 제너레이터 — `yield`로 이터레이터를 한 줄로 (Python의 특공)

### 핵심 문법: `yield`

```python
def range5():
    i = 0
    while i < 5:
        yield i          # ★ 여기서 "값을 내보내고 일시정지"
        i += 1           # 다음 next() 호출 시 여기서부터 재개

for x in range5(): print(x)   # 0 1 2 3 4
```

`yield`를 쓴 함수를 **제너레이터 함수(generator function)** 라 부르고,
이 함수를 호출하면 **제너레이터 객체(generator object)** 가 반환됨.

### 제너레이터 객체 = 이터레이터 객체

제너레이터는 자동으로 `__iter__`/`__next__` 구현됨. 직접 클래스 안 짜도 됨:
```python
gen = range5()         # 제너레이터 객체 (아직 실행 안 됨!)
next(gen)              # 0 — yield까지 실행하고 멈춤
next(gen)              # 1 — 멈췄던 곳부터 재개, 다음 yield에서 또 멈춤
next(gen); next(gen); next(gen)  # 2, 3, 4
next(gen)              # StopIteration 예외 (끝)
```

### ★ 핵심 — "실행을 일시정지하는 함수"

일반 함수: 호출 → 끝까지 실행 → 반환 (한 번에 종료)
제너레이터: 호출 → `yield`에서 멈춤 → 값 내보냄 → 다시 호출되면 멈춘 곳부터 재개

이게 핵심이야. 함수가 **여러 번 반환하는 것처럼 동작**. C/Java 함수는 불가능.

### 장점

1. **코드 간결** — `__iter__`/`__next__` 클래스 대신 `yield` 한 줄
2. **메모리 효율** — 무한 시퀀스도 가능 (필요할 때만 계산 = lazy evaluation)
   ```python
   def fibonacci():
       a, b = 0, 1
       while True:          # ★ 무한 루프지만 메모리 안 터짐
           yield a
           a, b = b, a + b
   ```
3. **파이프라인** — 여러 제너레이터 연결 가능
   ```python
   def double(x): yield from (n*2 for n in x)
   for v in double(range5()): print(v)   # 0 2 4 6 8
   ```

### 우리 rezero에 적용 — 순회 제너레이터 (탐구 노트 20번 옵션 I)

```python
def iter_reverse_topo(start_var):
    """역방향 위상 정렬 순회 제너레이터."""
    worklist, visited = [start_var.creator], set()
    while worklist:
        worklist.sort(key=lambda f: f.generation)
        f = worklist.pop()
        if f not in visited:
            visited.add(f)
            yield f                    # ★ Function을 하나씩 내보냄
            for x in f.inputs:
                if x.creator:
                    worklist.append(x.creator)
```

→ `fill_grad`가 `for f in iter_reverse_topo(...)` 로 깔끔해짐.
이게 제너레이터의 가장 일반적 용도 — **순회 알고리즘의 우아한 추출**.

---

## 3. ★ 코루틴 — "여러 진입/탈출 점을 가진 함수"

### 정의 (Donald Knuth, 1959)

**"실행을 일시정지했다가 재개할 수 있는 함수. 진입/탈출 점이 여러 개"**

대조:
- **서브루틴(일반 함수)**: 진입 1개(시작), 탈출 1개(return). 엄격한 호출-반환 계층.
- **코루틴**: 진입/탈출 다수. 호출자와 피호출자가 "대화"하듯 번갈아 실행.

### 파이썬에서의 진화 (3단계)

#### 1세대: `yield`로 값 "받기" (코루틴의 시작)

`yield`는 값 내보낼 때만 쓰는 게 아님. **값을 받을 수도 있음**:

```python
def accumulator():
    total = 0
    while True:
        x = yield total        # ★ yield가 값을 받을 수도!
        total += x

acc = accumulator()
next(acc)                      # 0 — 첫 yield까지 실행 (priming)
acc.send(10)                   # 10 — yield에 10 보내고 다음 yield까지 실행
acc.send(20)                   # 30
acc.send(5)                    # 35
```

→ `yield`가 양방향: 값을 내보내기도, 받기도. 이게 **코루틴의 기본 형태**.

#### 2세대: `yield from` (Python 3.3) — 위임

```python
def sub_gen():
    yield 1; yield 2

def main_gen():
    yield from sub_gen()       # ★ sub_gen에 위임
    yield 3

for x in main_gen(): print(x)  # 1 2 3
```

`yield from`은 단순 순회뿐 아니라 **send/throw도 위임**. 코루틴 합성의 기초.

#### 3세대: `async`/`await` (Python 3.5) — 현대 코루틴 ★

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)     # ★ 비동기 대기 (코루틴 안에서만)
    return "data"

async def main():
    result = await fetch_data()  # ★ 코루틴 호출
    print(result)

asyncio.run(main())
```

→ **`await`는 사실 `yield from`의 문법 설탕**. 비동기 I/O에 특화된 코루틴.
이게 현대 파이썬 비동기 프로그래밍(async/await, asyncio)의 기초.

### 제너레이터 vs 코루틴 — 용어 정리

파이썬에선 용어가 혼재되어 있어. 핵심 구분:

| 개념 | 주 용도 | 핵심 |
|---|---|---|
| **이터레이터** | 순회 | `__iter__`/`__next__` 프로토콜 |
| **제너레이터** | 순회 (이터레이터의 한 종류) | `yield`로 만듦 |
| **코루틴(전통적)** | 상태 머신, 데이터 흐름 | `yield`로 값 받기 (`send`) |
| **코루틴(현대, async)** | 비동기 I/O | `async`/`await` |

★ 중요: **모든 제너레이터는 이터레이터다. 하지만 모든 이터레이터가 제너레이터인 건 아님** (클래스로 만든 이터레이터는 제너레이터가 아님).
그리고 **제너레이터는 코루틴의 특수한 형태로 볼 수 있음** (PEP 342 이후).

---

## 4. ★ 세 개념의 관계 — 벤다이어그램 식 정리

```
┌─────────────────────────────────────────────────┐
│  코루틴 (Coroutine) — 가장 넓은 개념             │
│  "일시정지/재개 가능한 함수"                      │
│  ┌───────────────────────────────────────────┐  │
│  │  제너레이터 (Generator)                    │  │
│  │  "yield로 만드는 코루틴/이터레이터"         │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │  이터레이터 (Iterator)               │  │  │
│  │  │  "순회 패턴 (next/StopIteration)"   │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘

- 이터레이터 ⊂ 제너레이터 ⊂ 코루틴 (포함 관계, 개념적으로)
- 단, 파이썬에선 용어 혼재. PEP 342 이후 제너레이터=코루틴으로 봄.
- async/await 코루틴은 별도 타입(네이티브 코루틴)이라 엄격히는 다름.
```

### 우리 rezero 순회 제너레이터는 어디?

```python
def iter_reverse_topo(start_var):
    ...
    yield f
```

이건 **이터레이터(순회) 용도의 제너레이터**. 가장 일반적이고 단순한 형태.
코루틴 기능(`send`, 상태 유지하며 대화)은 안 씀.

→ 브로 질문 "이게 코루틴 그건가?"에 대한 답: **"엄밀히는 제너레이터이고, 제너레이터는 코루틴의 한 형태지만, 우리 용도(순회)에선 그냥 이터레이터라 불러도 됨"**.

---

## 5. ★ "일시정지"가 가능한 진짜 이유 — 실행 프레임 보존

### 일반 함수의 실행

```python
def add(a, b):
    c = a + b        # 지역 변수 c
    return c

result = add(1, 2)   # 함수 실행 → c 생성 → return → c 소멸
# 함수 반환 후엔 c, a, b 모두 사라짐 (스택 프레임 제거)
```

### 제너레이터의 실행

```python
def gen():
    a = 1
    yield a          # ① 여기서 멈춤. a=1 보존됨
    b = 2
    yield a + b      # ② 재개. a=1 그대로, b=2 생성

g = gen()
next(g)             # 1 (①에서 멈춘 상태로 프레임 보존)
next(g)             # 3 (②로 재개, a=1 유지된 채 b=2 생성)
```

→ 핵심: 제너레이터는 `yield`에서 멈출 때 **실행 프레임(지역 변수, 실행 위치)을 보존**.
이게 일반 함수와의 본질적 차이. CPython에선 제너레이터 객체가 프레임을 들고 있음.

### 왜 중요한가 — 메모리와 계산의 분리

```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()    # 한 줄씩만 메모리에

for line in read_large_file("10GB.csv"):
    process(line)                 # 전부 메모리에 안 올림
```

→ 일반 함수였으면 전부 리스트로 반환해야 하니 메모리 폭발.
제너레이터는 **한 번에 하나씩** (lazy evaluation). 이게 파이썬에서 제너레이터가 널리 쓰이는 이유.

---

## 6. 실전 예시 — 파이썬 표준 라이브러리에서

### `range` vs `xrange` (Python 2 역사)

Python 2에선 `range(1000000)`이 리스트를 만들어 메모리 폭발.
`xrange`가 제너레이터 버전이었음. Python 3에선 `range`가 제너레이터 기반으로 통일.

### `map`, `filter`, `zip` (Python 3)

Python 3의 `map`/`filter`/`zip`은 전부 **이터레이터 반환** (리스트 아님):
```python
m = map(lambda x: x*2, [1,2,3])   # 이터레이터
next(m)   # 2
next(m)   # 4
# 한 번 순회하면 끝 (재사용 안 됨) — 리스트가 아님
```

### `dict.items()`, `file` 객체

```python
for k, v in d.items(): ...      # 이터레이터
for line in open("file.txt"): ... # 파일 객체 자체가 이터레이터
```

→ **파이썬 전반에 이터레이터 프로토콜이 스며들어 있음**. 이해하면 파이썬 전체가 보인다.

---

## 7. ★ 비동기 코루틴 (async/await) — 왜 등장했나

### 문제: I/O 대기 시 CPU 놀림

```python
# 동기 버전 — 요청 보내고 1초 기다리는 동안 CPU가 아무것도 안 함
def fetch_sync(url):
    response = requests.get(url)    # 1초 대기 (블로킹)
    return response.text

# 10개 URL 가져오는 데 10초 걸림
```

### 해결: 대기 중 다른 일 하기 (비동기)

```python
import asyncio, aiohttp

async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()   # ★ 대기하는 동안 다른 코루틴 실행

# 10개 URL을 동시에 → 1초 걸림 (병렬 대기)
async def main():
    results = await asyncio.gather(*[fetch_async(u) for u in urls])
```

### 왜 코루틴이 해법인가

- 스레드/프로세스 없이 **단일 스레드에서 여러 작업 번갈아 실행**
- I/O 대기(`await`) 때 이벤트 루프가 다른 코루틴으로 전환
- `yield`의 "일시정지" 능력이 I/O 대기에 딱 맞음 → 발전시킨 게 `await`

### 우리 rezero와 관계?

현재로선 **직접 관계 없음**. 역전파는 동기 계산이라 비동기 필요 없음.
→ 다만, 나중에 **대규모 신경망 학습**(step50+)에서 GPU/분산 처리 논의 나오면
"비동기 학습" 개념이 등장 가능. 그때 이 노트가 배경지식으로 도움.

---

## 8. 우리 상황으로 회귀 — 순회 제너레이터의 의미

### 옵션 I(탐구 노트 20번) 재방문

```python
def iter_reverse_topo(start_var):
    worklist, visited = [start_var.creator], set()
    while worklist:
        worklist.sort(key=lambda f: f.generation)
        f = worklist.pop()
        if f not in visited:
            visited.add(f)
            yield f
            for x in f.inputs:
                if x.creator:
                    worklist.append(x.creator)
```

→ 이 제너레이터는:
- **이터레이터**: 역방향 위상 정렬 순회
- **제너레이터**: `yield`로 만듦
- **코루틴?**: 엄밀히 코루틴의 한 형태지만, 우리 용도(순회)에선 `send()` 안 씀
  → "코루틴 기능까지 쓰는 건 아님"

### 언제 코루틴 기능까지 쓸까? (우리에겐 해당 안 함)

예: 데이터 파이프라인에서 역압(backpressure) 제어
```python
def consumer():
    buffer = []
    while True:
        x = yield buffer       # 데이터 받고 버퍼 상태 반환
        if len(buffer) < 10:
            buffer.append(x)
```

→ 이런 식의 "양방향 대화"가 필요하면 코루틴. 우리 역전파 순회는 단방향이라 필요 없음.

### 결론 — 브로 질문에 대한 최종 답

> "이게 그 뭔가 그 '코루틴'인지 뭔지 그거 관련 이야기 아니야?"

**맞음. `yield`는 코루틴의 기초 문법.** 다만:
- 우리가 쓸 용도(순회)는 **이터레이터 패턴**에 가까움 (코루틴 기능의 일부만 사용)
- 코루틴의 전체 기능(`send`, 비동기)은 우리에겐 오버스펙
- 그래도 개념을 알아두면 파이썬 전반(for, map, async/await)이 보임 ★

---

## 9. 🔓 더 파고 싶으면 (확장 후보)

| 주제 | 키워드 | 방향 |
|---|---|---|
| **CPython 제너레이터 내부** | gi_frame, gi_code, 스택 프레임 | 제너레이터가 프레임을 어떻게 보존하는가 (C 구현) |
| **이터레이터 알고리즘 패턴** | 제너레이터 합성, 파이프라인 | `yield from`, `itertools.chain` 등 순회 합성 |
| **asyncio 깊이** | event loop, task, future | 비동기 코루틴의 엔진. 단일 스레드 동시성 원리 |
| **코루틴 vs 스레드** | 동시성 vs 병렬성 | GIL, 선점형 vs 협력형, 언제 뭘 쓰나 |
| **Go의 goroutine** | CSP 모델, channel | 다른 언어의 코루틴 접근 (파이썬과 비교) |
| **functools.reduce와 제너레이터** | fold 패턴 | 역전파 = right fold (탐구 13번)와 이터레이터 결합 |

### 회수 시그널

- 옵션 I(순회 제너레이터) 실제 도입 시도 → 본 노트 §2, §8
- async/await 코드 마주칠 때 → 본 노트 §3 (3세대), §7
- "yield가 뭐지?" 헷갈릴 때 → 본 노트 §2, §5
- 파이썬 `for` 내부 이해 → 본 노트 §1, §6

---

## 🔑 핵심 키워드

`#이터레이터` `#iterator` `#이터레이터패턴` `#iterator-pattern` `#GoF` `#제너레이터` `#generator` `#yield` `#일시정지` `#지연평가` `#lazy-evaluation` `#코루틴` `#coroutine` `#send` `#yield-from` `#async` `#await` `#asyncio` `#비동기` `#이벤트루프` `#프레임보존` `#순회추출` `#파이썬철학` `#step16파생` `#탐구20연결`

## 📝 작성일 / 관련 링크

- **작성일**: 2026-07-31 (step16 완료 후)
- **트리거**: 브로 — "이게 그 '코루틴' 관련 이야기 아니야? 좀 더 깊게 알아둬서 나쁠 게 없을 듯"
- **관련 노트**: exploration_20 (Node 도입 §4.5 옵션 I — 순회 이터레이터)
- **관련 코드**: rezero/steps/step16.py (fill_grad 순회 — 옵션 I 적용 대상)
- **파생**: 브로가 옵션 I 실험할 때 직접 제너레이터로 순회 추출해보는 것도 좋음
