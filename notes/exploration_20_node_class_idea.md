# 탐구 20 — 계산 그래프 추상화 경계: Node 클래스와 순회 이터레이터

> **시점**: step16 완료 후 (2026-07-31)
> **상태**: 💡 아이디어 단계 (미실행, 설계 탐색용)
> **트리거**: 브로 통찰 2종 —
>   1. "그래프 노드 정보를 좀 더 잘 코드상에 분리표현하면 어떨까" (Node 상위 클래스)
>   2. "'순회' 용어를 떠올리니 이터레이터 패턴이 떠올라" (순회 제너레이터 추출)
> **추적**: GitHub enhancement 이슈 (Node 도입 + manim 시각화)

## 📌 왜 이 탐구를 했나

step16에서 `generation`이 Variable/Function 양쪽에 **동일한 이름, 타입, 의미**로 존재함을 확인.
exploration_18 §6에서 "간선 정보가 객체 속성에 흡수되어 있다"는 통찰도 이미 파악.
여기에 브로가 두 가지 연관 통찰을 추가하며, **"계산 그래프를 코드로 어떻게 표현할지"** 라는 설계 질문이 열림.

이 노트는 두 통찰(Node 클래스, 순회 이터레이터)을 **"추상화의 두 차원"** 으로 정리하고,
어디까지 갈지(장점), 어디가 거시기한지(단점), 언제 할지(시점)를 균형 있게 탐구.
실행은 나중에. 지금은 아이디어 영구 보존이 목적.

---

## 1. 배경 — 현재 구조에서 무엇이 보이나

### Variable/Function의 속성 분류

| 속성 | Variable | Function | 분류 |
|---|---|---|---|
| `generation` | ✅ (int) | ✅ (int) | **노드 메타데이터** (공통) |
| `name` | (step19에서 추가 예정) | (암묵적: `f.__class__.__name__`) | **노드 메타데이터** (공통 가능) |
| `data`, `grad` | ✅ | ❌ | Variable 고유 |
| `creator` | ✅ (Function) | ❌ | Variable의 역전파 간선 |
| `inputs`, `output` | ❌ | ✅ (Variable) | Function의 순전파 간선 |
| `forward`, `backward`, `derivative` | ❌ | ✅ | Function 고유 (연산) |

★ 관찰: `generation` (그리고 잠재적으로 `name`)은 **"노드로서의 공통 속성"**.
반면 간선(`creator` vs `inputs`/`output`)은 **타입/방향이 비대칭**.

### exploration_18 §6 통찰 회수

> DeZero에선 "간선"이라는 별도 객체가 없음.
> 간선 정보가 **객체의 속성(attribute)** 으로 녹아들어감.
> `y.creator = Add`는 코드에선 속성, 그래프론 간선 — 이중적 의미.

→ "속성으로 녹인 건 좋은데, 노드 공통 부분은 빼내자"는 게 본 탐구의 출발점.

---

## 2. ★ 추상화의 두 차원 — Node(구조) vs 이터레이터(알고리즘) ★

브로의 두 통찰은 사실 **직교하는 두 차원**을 가리키고 있었음:

| 차원 | 질문 | 통찰 |
|---|---|---|
| **Node (객체 구조)** | "타입 계층을 어떻게?" | Variable/Function의 공통 조상을 둘 것인가? |
| **이터레이터 (순회 알고리즘)** | "순회를 어떻게?" | `while worklist` 명시적 루프 vs `yield` 제너레이터? |

→ 둘은 독립적 결정이라 **4가지 조합**이 가능:

| 조합 | Node? | 이터레이터? | 특징 | 복잡도 |
|---|---|---|---|---|
| **현재 (step16)** | ❌ | ❌ | 명시적 `while worklist` + 객체에 분산 | 최소 |
| **옵션 I** (이터레이터만) | ❌ | ✅ | 순회 알고리즘을 별도 제너레이터로 추출 ★ 간단 | 약간 ↑ |
| **옵션 N** (Node만) | ✅ | ❌ | Node 타입 추가, 순회는 여전히 명시적 | 약간 ↑ |
| **옵션 N+I** (둘 다) | ✅ | ✅ | Node + 순회 인터페이스. 가장 추상화됨 | ↑ |

각 차원을 따로 살펴보자.

---

## 3. 차원 1 — Node 상위 클래스 도입 (객체 구조)

### 제안 구조

```python
class Node(ABC):
    """계산 그래프의 노드. Variable/Function의 공통 메타데이터."""
    generation: int = 0
    name: str = ""

class Variable(Node):
    # Node에서 generation, name 상속
    data: np.ndarray
    grad: np.ndarray
    creator: Function        # 역전파 간선 (자식 고유)

class Function(Node):
    # Node에서 generation, name 상속
    inputs: tuple[Variable, ...]   # 순전파 간선 (자식 고유)
    output: Variable               # 순전파 간선 (자식 고유)
```

### 설계 원칙 (브로가 그은 선)

> "무리하게 '노드, 간선' 구조를 '완전히 일반화'하자는 것은 아니고,
> 그럼에도 불구하고, 좀 더 그래프의 노드 정보를 좀 더 잘 코드상에 분리표현하면 어떨까"

→ **"노드 메타데이터는 공통, 간선은 자식에서만"** 이라는 절충점.
Edge 클래스는 명시적 배제. Node까지만.

### 장점

1. **`generation` 공통 속성 OOP적 명확화** — 양쪽에 "우연히" 같은 게 아니라 "노드의 본질적 속성"으로 타입 계층 명시
2. **책 step19 `name` 속성 대비** — 미리 Node에 올려두면 상속으로 자연스럽게 확장
3. **"계산 그래프" 개념의 코드화** — 말이 아니라 타입 계층으로 "이 둘은 그래프 노드다" 선언

★ 핵심: 장점 1은 헝가리안 논쟁(탐구 19번)과 **반대 결**.
- 탐구 19번: "불필요한 이름 중복 제거" (Pythonic)
- 여기: "불필요한 속성 중복 제거" (OOP로 공통화)
둘 다 "중복 제거"라는 결이지만, 적용 대상이 이름 vs 속성.

### 단점 / 어려운 점

1. **간선 정보 비대칭** — Variable은 `creator` (1개), Function은 `inputs`/`output` (여러 개). Node에 올리기 어려움 ★ 핵심 어려움
2. **step16 시점엔 시기상조** — 본 목적은 generation 도입이지 구조 개편 아님
3. **책 원본 구조에서 벗어남** — 학습 서사 영향 (다만 이미 #010~#014 변형에서 감수한 결)
4. **추상화 비용 vs 실제 이득 트레이드오프** — 순회 소비자가 fill_grad 하나뿐이면 이득 미미
5. **간선을 인터페이스로 추상화하면 Define-by-Run 직관성 훼손 우려** — `y.creator` 직관이 `y.prev_nodes()`로 감싸짐
6. **"완전 일반화" 유혹** — Node + Edge 객체까지 가면 본질 상실. 브로가 그은 선(Node까지) 지키기

---

## 4. 차원 2 — 순회 이터레이터 추출 (알고리즘) ★ 브로 추가 통찰

### 브로 자각

> "거 그래프 노드의 '순회'란 용어를 떠올리니, 뭔가 '이터레이터 패턴' 따위도 떠오르는데"

→ 핵심: **`fill_grad`의 `while worklist: pop()`은 사실상 수동 이터레이터**.
파이썬은 이걸 언어 차원에서 더 우아하게 지원 (`yield`/제너레이터).

### 옵션 I (이터레이터만) — 가장 가벼운 개선

Node 도입 없이도 순회 알고리즘을 제너레이터로 추출 가능:

```python
def iter_reverse_topo(start_var: Variable):
    """역방향 위상 정렬 순회 제너레이터. generation 정렬 + visited 포함."""
    worklist, visited = [start_var.creator], set()
    while worklist:
        worklist.sort(key=lambda func: func.generation)
        f = worklist.pop()
        if f not in visited:
            visited.add(f)
            yield f                          # ★ 하나씩 내보내기
            for x in f.inputs:
                if x.creator is not None:
                    worklist.append(x.creator)
```

이러면:
```python
def fill_grad(start_var):
    ...
    for f in iter_reverse_topo(start_var):   # ★ for 루프로 깔끔!
        upstream = f.output.grad
        downstreams = f.backward(upstream)
        ...

def get_dot_graph(output):                   # ★ 시각화도 같은 제너레이터!
    txt = ""
    for f in iter_reverse_topo(output):
        txt += _dot_func(f)
    return "digraph g {...}"
```

### 옵션 I의 장점

1. **관심사 분리 (SoC)** — 순회 알고리즘(`iter_reverse_topo`)과 계산(`fill_grad`) 분리
2. **재사용성** — fill_grad, get_dot_graph, (미래) manim 순회가 **같은 제너레이터** 사용 ★
3. **파이썬닉** — `for f in iter_reverse_topo(...)` 가 가장 파이썬스러운 패턴
4. **테스트 용이** — 순회 알고리즘을 독립 테스트 가능 (역전파 계산과 분리)
5. **가벼움** — Node 도입(타입 계층 변경) 없이 함수 하나 추가만으로 끝

### 옵션 I의 단점 / 고려점

1. **제너레이터 지연 평가(lazy) 특성** — `yield`가 순회 소비자가 `next()` 부를 때만 실행.
   역전파처럼 "반드시 끝까지 순회해야 결과가 온전한" 경우엔 지연이 오히려 헷갈림 가능
2. **visited 처리 위치** — 제너레이터 안에서 방문 표시 vs 바깥에서? 일관성 필요
3. **schedule 클로저(항목 023)와 충돌** — 현재 schedule은 fill_grad 내부 클로저인데,
   제너레이터로 빼면 schedule 로직이 어디로 가는지 설계 결정 필요

### yield와 코루틴 — 더 깊은 주제

브로가 추가 연결: "이게 그 뭔가 그 '코루틴'인지 뭔지 그거 관련 이야기 아니야?"
→ ★ 정확함. `yield`는 **제너레이터**의 씨앗이자, 더 나아가 **코루틴(coroutine)** 의 기초.
이 주제는 별도 탐구 노트로 분리: [exploration_21_yield_generator_coroutine.md](./exploration_21_yield_generator_coroutine.md)

---

## 5. 시너지 — 두 차원이 만날 때 (시각화) ★★

### 관찰: fill_grad와 get_dot_graph 순회가 거의 동일

`dezero/utils.py:get_dot_graph()` 코드를 보면 **순회 알고리즘이 fill_grad와 거의 동일**:

```python
# fill_grad (step16 역전파 순회)
worklist, visited = [], set()
def schedule(f):                          # ★ get_dot_graph의 add_func과 거의 동일!
    if f not in visited:
        worklist.append(f); visited.add(f)
schedule(start_var.creator)
while worklist:
    f = worklist.pop()
    ...
    for x in f.inputs:
        if x.creator: schedule(x.creator)

# get_dot_graph (책 step25 시각화 순회)
funcs, seen_set = [], set()
def add_func(f):
    if f not in seen_set:
        funcs.append(f); seen_set.add(f)
add_func(output.creator)
while funcs:
    func = funcs.pop()
    ...
    for x in func.inputs:
        if x.creator: add_func(x.creator)
```

★ 핵심: **순회 알고리즘 자체가 Variable/Function 차이를 거의 안 씀**.
공통 패턴: `node.creator` (Variable) / `func.inputs` (Function)로 다음 노드 찾기.

### 시각화(graphviz/manim)와의 시너지

옵션 I(이터레이터 추출) + 옵션 N(Node)이 만나면:
- 순회를 Node 인터페이스로 일반화 (`prev_nodes()`)
- `fill_grad`, `get_dot_graph`, manim 애니메이션 순회가 **동일한 추상화** 사용
- 세 가지 순회 소비자가 하나의 인터페이스 공유 = DRY + 확장성

→ **옵션 N+I가 가장 추상화됨**. 시각화(manim 포함)를 본격 다룰 때 가치가 빛남.

### manim(Math Animation) 시각화 아이디어 — 브로 제안

[manim](https://www.manim.community/) — 3Blue1Brown의 수학 애니메이션 엔진.
graphviz DOT 정적 텍스트 대신 계산 그래프를 **애니메이션**으로:
- 순전파 흐름: 노드가 차례로 나타나고 간선이 그려짐, 값이 전파되는 과정 시각화
- 역전파 흐름: 역방향으로 grad 값이 전파/누적되는 과정 시각화
- generation별 층 배치 → 위상 정렬 구조 시각적 체감

장점: ★ 학습 가치 최고 (움직임 = 직관), 스타일 자유도, 외부 시스템 패키지 불필요
단점: 의존성 무거움(manimgl/manimce + FFmpeg), 러닝 커브, 렌더링 시간

→ Node 추상화가 있으면 manim 렌더링 코드가 **"Node를 순회하며 그린다"** 로 깔끔해짐.
Node 도입과 manim은 시너지 관계.

---

## 6. 시점 후보 — 언제 도입하면 좋을까

### 후보 A: step19 (name 추가 시점) ★ 자연스러움

- 책 step19에서 `Variable.name` 도입
- 그때 "name은 노드 공통 속성 아닌가?" 자각 → Node 도입 계기
- 과거 step은 보존(우리 원칙), step19부터 Node 상속
- **가장 자연스러운 학습 서사**

### 후보 B: step25 (graphviz 시각화 시점) — 순회 일반화 계기

- 책 step25에서 `get_dot_graph` 순회 코드 등장
- "fill_grad와 순회가 같다!" 자각 → 옵션 I(이터레이터 추출) 계기
- 시각화 시점이라 manim 실험도 자연스러움
- **시각화 + 순회 일반화 동시 진행**

### 후보 C: step23 (패키지화) — 구조 정리 시점

- `rezero/core.py`로 승격하면서 전체 구조 재편
- Node/이터레이터 도입이 core.py 설계의 일부
- **가장 "엔지니어링" 시점**

### 후보 D: 별도 "구조 개선 주간" — step 사이

- 진도 멈추고 구조 실험에 몰입
- 브로 스타일(탐구 좋아)에 맞음
- **가장 "탐구적" 시점**

### ★ 옵션 I는 Node 결정과 독립적

옵션 N(Node)은 step19/23 시점에 결정하되, **옵션 I(이터레이터 추출)는 그 전에도 가능**.
예: step16 랩업 직후 "구조 개선 주간"에 옵션 I만 실험해보는 것도 좋음.

---

## 7. ★ Pythonic vs OOP 트레이드오프 — 정리

| 관점 | 현재 (Pythonic) | Node 도입 (OOP) | 이터레이터 추출 (Pythonic++) |
|---|---|---|---|
| generation | 양쪽에 각자 선언 (중복) | Node에서 상속 (공통화) | 영향 없음 |
| name | (step19에서 Variable에 추가) | Node에서 상속 (Function도 자동) | 영향 없음 |
| 간선 | 각자 다른 이름/타입 (비대칭 반영) | 그대로 자식에 (추상화 안 함) | 영향 없음 |
| 순회 | fill_grad 내부에 하드코딩 | 영향 없음 | 별도 제너레이터로 추출 |
| 학습 서사 | 책과 동일 | 책과 다름 (rezero 실험) | 책과 다름 (더 파이썬답게) |

★ 결론: **"어디까지 추상화로 갈 것인가"** 가 핵심 질문.
- 극단 Pythonic: 지금 (책 방식)
- 절충: 옵션 I만 / 옵션 N만 (브로 제안의 두 차원 각각)
- 최대 추상화: 옵션 N+I (시각화 시점에 가치 빛남)
- 과잉: Node + Edge 객체 (배제)

브로 제안은 **절충점**으로 합리적. 시점(step19/23/25)과 범위(I만/N만/둘 다)만 조율하면 됨.

---

## 8. 🔓 더 파고 싶으면 (확장 후보)

| 주제 | 키워드 | 방향 |
|---|---|---|
| **PyTorch의 autograd 구조** | `Node`, `Function`, `grad_fn` | PyTorch는 내부적으 Node 클래스 있음! 우리 제안과 비교 |
| **JAX의 그래프 표현** | jaxpr, traced values | Define-by-Run 아닌 패러다임에서 그래프 추상화 |
| **manim 학습 곡선** | Scene, Mobject, Animation | manim 입문 난이도, 계산 그래프에 적합한지 |
| **graphviz vs manim** | 정적 vs 동적 시각화 | 학습용 시각화의 두 접근법 비교 |
| **객체 참조 = 간선 (Python 의미론)** | reference, id(), weakref | Python 객체 모델과 그래프 이론의 교차점 |
| **Mixin 다중 상속 대안** | `class Variable(Node, DataHolder)` | 단일 상속 vs Mixin (설계 옵션) |
| **yield/제너레이터/코루틴 심화** | send, async/await, asyncio | 별도 노트 exploration_21에서 다룸 |

### 회수 시그널

- step19에서 Variable.name 추가 → "이거 Node에 올리는 거 아닌가" → 본 노트 §3 장점 2
- step25 graphviz 순회 → "fill_grad랑 같네" → 본 노트 §5 시너지
- 옵션 I 실험 → 본 노트 §4 + exploration_21
- manim 실험 시작 → 본 노트 §5 manim 시너지
- "왜 이 속성 양쪽에 있지?" → 본 노트 §1 매핑 표

---

## 9. 🎯 결론 — 현 시점의 판단

### 도입 여부: **보류 (이슈로 추적, 시점/범위 후보 명시)**

이유:
1. step16 본 목적(generation)과 Node/이터레이터 도입은 별개 결정
2. 시각화 시점(step25+)에 추상화 가치가 본격 체감
3. 지금 도입하면 추상화 이득 미미 (순회 소비자가 fill_grad 하나뿐)
4. 과거 step 보존 원칙상, 자연스러운 도입 시점(step19/23) 기다림이 학습 서사에 좋음

### 추적: GitHub enhancement 이슈 21번

- Node 도입 + manim 시각화를 함께 묶어서 추적
- 옵션 I(이터레이터만)는 Node 결정과 독립적이라 언제든 가능
- 시점 후보: step19 / step23 / step25 / 별도 주간
- 결정은 그때 브로가

### 브로 멘션

> "대충 패키지화 시점이 될지 언제가 될지, 좀 야무지게(?) 찰지게 좀 고쳐보고 싶네,
> 어짜피 이건 학습용 코드이니"

→ ★ 맞음. 학습용 코드라 "실용성"보다 "이해/가독성/파이썬 철학" 우선.
step23 패키지화 시점이나 그 전 "구조 개선 주간"에 실험해보면 좋겠음.

### 이 노트의 가치

- 아이디어 영구 보존 (미루면 까먹음 방지)
- 두 차원(Node/이터레이터)을 직교로 정리 → 결정 시 혼란 방지
- 장/단/어려운 점 균형 정리 (나중에 결정 시 참고)
- 시점 + 범위 후보 명시 (자연스러운 도입 타이밍/범위 놓치지 않게)
- 브로의 OOP 직관 + 시각화 아이디어(manim) 영구 기록

---

## 🔑 핵심 키워드

`#노드클래스` `#Node` `#상위클래스` `#추상화` `#OOP` `#Pythonic` `#이터레이터` `#제너레이터` `#yield` `#순회추출` `#옵션I` `#옵션N` `#직교하는두차원` `#트레이드오프` `#generation공통` `#간선흡수` `#간선비대칭` `#시각화` `#graphviz` `#dot` `#manim` `#수학애니메이션` `#순회일반화` `#Define-by-Run` `#step16파생` `#아이디어보류` `#이슈추적` `#시점후보` `#학습서사`

## 📝 작성일 / 관련 링크

- **작성일**: 2026-07-31 (step16 완료 후). §4.5 재편(전체 재구성) 동일일.
- **트리거**: 브로 통찰 — "노드 정보를 좀 더 잘 코드상에 분리표현하면 어떨까" + "마님(manim)으로 시각화" + "순회 → 이터레이터 패턴"
- **GitHub 이슈**: Node 도입 + manim 시각화 enhancement 이슈 21번
- **관련 노트**:
  - exploration_18 §6 (간선 = 객체 속성 흡수 통찰) — 본 노트 출발점
  - exploration_19 (Pythonic vs 헝가리안) — 장점 1과 반대 결
  - exploration_21 (yield/제너레이터/코루틴) — 차원 2 심화
- **관련 코드**: rezero/steps/step16.py (generation 양쪽), dezero/utils.py (graphviz 순회 — fill_grad와 동일 패턴)
- **관련 책 단계**: step19 (name 추가), step25 (graphviz 시각화)
- **미래 결정 시점**: step19 / step23 / step25 / 별도 주간 중 브로 선택
