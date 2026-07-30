# 🧪 보충 탐구 #18 — 그래프 기본과 순회 (DFS/BFS/위상 정렬)

> **step15 학습을 위한 배경 지식** (2026-07-30)
> step16 "복잡한 계산 그래프 구현(generation)"을 이해하기 위해 필요한 CS 기본기.
> ★ **가벼운 마음으로** — 핵심만 짚고 step16으로 넘어감. 더 파고 싶은 주제는 말단 "확장 후보"에 열어둠.

---

## 목차

- [1. 그래프란? — 노드와 엣지](#1-그래프란--노드와-엣지)
- [2. 그래프의 종류 — 방향/무방향, 순환/비순환(DAG)](#2-그래프의-종류--방향무방향-순환비순환dag)
- [3. 그래프 표현 — 파이썬 딕셔너리로 인접 리스트](#3-그래프-표현--파이썬-딕셔너리로-인접-리스트)
- [4. 순회(Traversal) — 모든 노드 방문하기](#4-순회traversal--모든-노드-방문하기)
  - [4.1 DFS (깊이 우선 탐색)](#41-dfs-깊이-우선-탐색)
  - [4.2 BFS (너비 우선 탐색)](#42-bfs-너비-우선-탐색)
  - [4.3 핵심 차이 — 스택(LIFO) vs 큐(FIFO)](#43-핵심-차이--스택lifo-vs-큐fifo)
- [5. 위상 정렬 (Topological Sort) — 의존성 순서](#5-위상-정렬-topological-sort--의존성-순서)
- [6. DeZero와 연결 — 계산 그래프는 DAG, 역전파는 위상 정렬](#6-dezero와-연결--계산-그래프는-dag-역전파는-위상-정렬)
- [7. 요약표](#7-요약표)
- [8. 🔓 더 파고 싶으면 (확장 후보, open-ended)](#8--더-파고-싶으면-확장-후보-open-ended)

---

## 1. 그래프란? — 노드와 엣지

**그래프(graph)**: 사물을 **점(노드/node)** 으로, 관계를 **선(엣지/edge)** 으로 나타낸 구조.

```python
# 가장 단순한 그래프 표현 — 노드 4개, 엣지 3개
#   A ── B
#   │
#   C ── D
nodes = ["A", "B", "C", "D"]
edges = [("A", "B"), ("A", "C"), ("C", "D")]
```

**실생활 예시**:
- **지하철 노선도** — 역(노드), 선로(엣지)
- **소셜 네트워크** — 사람(노드), 친구 관계(엣지)
- **도로망** — 교차로(노드), 도로(엣지)
- **계산 그래프** ★ — Variable(노드), Function 연결(엣지) ← DeZero

→ ★ DeZero의 Variable/Function 그래프도 결국 그래프 이론의 한 사례.

---

## 2. 그래프의 종류 — 방향/무방향, 순환/비순환(DAG)

### 방향 vs 무방향

| 종류 | 엣지 방향 | 예시 |
|---|---|---|
| **무방향(undirected)** | 양방향 (A─B) | 페이스북 친구, 지하철 |
| **방향(directed)** ★ | 한 방향 (A→B) | 트위터 팔로우, 계산 그래프 |

```python
# 무방향: A─B (A에서 B도, B에서 A도 가능)
# 방향: A→B (A에서 B만, B에서 A는 불가)
```

### 순환 vs 비순환

| 종류 | 정의 | 예시 |
|---|---|---|
| **순환(cyclic)** | 시작점으로 돌아오는 경로 있음 | 일방통행 순환로로, A→B→C→A |
| **비순환(acyclic)** ★ | 사이클 없음 | 계산 그래프 (되돌아오는 경로 없음) |

### ★★★ DAG — DeZero의 그래프 형태

**DAG (Directed Acyclic Graph, 방향성 비순환 그래프)**: 방향 + 사이클 없음.

```
   x₀   x₁       ← 입력 노드 (시작점)
    │   │
    ▼   ▼
    Add         ← 함수 노드 (중간)
      │
      ▼
    Square      ← 함수 노드 (중간)
      │
      ▼
      y         ← 출력 노드 (끝점)
```

★ 핵심: DAG는 **되돌아가는 길이 없음**. 그래서 "어디서부터 처리해야 하는지"(순서)가 명확해야 함.
이게 바로 역전파에서 **순서 문제**가 중요한 이유.

---

## 3. 그래프 표현 — 파이썬 딕셔너리로 인접 리스트

그래프를 코드로 표현하는 가장 흔한 방법 — **인접 리스트(adjacency list)**.

### 3.1 가장 단순한 예시부터 (선형: A → B → C → D)

```
그래프 그림:
   A ──→ B ──→ C ──→ D
```

이걸 파이썬 딕셔너리로 표현하면:

```python
graph = {
    "A": ["B"],     # A에서 출발하는 엣지: A → B 하나뿐
    "B": ["C"],     # B에서 출발하는 엣지: B → C 하나뿐
    "C": ["D"],     # C에서 출발하는 엣지: C → D 하나뿐
    "D": [],        # D에서 출발하는 엣지: 없음 (끝 노드)
}
```

★ 핵심 매핑:
- **키(key)** = "출발 노드" (엣지의 시작점)
- **값(value)** = "그 노드에서 뻗어나가는 엣지들의 도착점 목록"

즉 `graph["A"]`는 **"A에서 뻗어나가는 엣지들이 도착하는 노드들"** 이야.

### 3.2 각 키가 뭘 반환하는지 한눈에 보기

```python
graph["A"]   → ["B"]    # A에서 B로 가는 엣지 1개
graph["B"]   → ["C"]    # B에서 C로 가는 엣지 1개
graph["C"]   → ["D"]    # C에서 D로 가는 엣지 1개
graph["D"]   → []       # D에서 나가는 엣지 없음 (끝)
```

★ 중요: `graph["A"]`는 **"A와 같은 레벨의 노드들"이 아니라 "A에서 갈 수 있는 노드들"** 이야.
- `graph["A"]` = "A의 이웃/자식" = ["B"] ← A 다음에 갈 수 있는 곳
- "A와 같은 레벨"은 그래프에 없어 (A가 유일한 시작점이니까)

### 3.3 엣지가 여러 개인 노드 (분기)

노드에서 뻗어나가는 엣지가 여러 개면, value 리스트에 여러 개 담김:

```python
# 그래프:
#   A ──→ B
#    └──→ C      (A에서 B, C로 분기 — 엣지 2개)

graph = {
    "A": ["B", "C"],   # ★ A에서 출발하는 엣지 2개: A→B, A→C
    "B": ["D"],         # B에서 D로
    "C": ["D"],         # C에서 D로
    "D": [],            # D는 끝
}

# 각 키 확인:
graph["A"]   → ["B", "C"]   # A에서 갈 수 있는 곳: B, C (엣지 2개)
graph["B"]   → ["D"]        # B에서 갈 수 있는 곳: D
graph["C"]   → ["D"]        # C에서 갈 수 있는 곳: D
graph["D"]   → []           # D에서 갈 수 있는 곳: 없음
```

★ `graph["A"] = ["B", "C"]`의 의미:
- "A에서 B로 가는 엣지" + "A에서 C로 가는 엣지" → 2개 엣지 존재
- 리스트에 원소가 2개 = 엣지가 2개

### 3.4 핵심 공식 — `graph[node]`가 뭘 반환하는가

```
graph[node] = "그 노드에서 뻗어나가는 엣지들이 도착하는 노드들"의 리스트
            = "node의 이웃(자식)들"
            = "node에서 다음으로 갈 수 있는 곳들"
```

→ ★ **node 자체가 아니라, node에서 갈 수 있는 곳들의 목록**을 반환.
이게 "인접 리스트"라는 이름의 유래 — 인접한(이웃한) 노드들의 리스트.

★ **용어 통일**: 이 노트에선 **이웃 = 자식 = 다음 노드**를 같은 의미로 씀.
(엄밀히: 무방향 그래프에선 "이웃(neighbor)", 방향 트리/DAG에선 "자식(child)"이 더 정확.
여기선 DAG를 다루지만 직관성 위해 섞어 씀 — 모두 "node에서 갈 수 있는 다음 노드"를 가리킴.)

### 3.5 왜 "같은 레벨"이 아닌가 (헷갈림 방지)

| 질문 | 답 |
|---|---|
| `graph["A"]`는 "A와 같은 레벨의 노드들"? | ❌ 아님 |
| `graph["A"]`의 정확한 의미? | ✅ "A에서 갈 수 있는 노드들" = A의 이웃/자식 |
| 왜 헷갈림? | 우연히 `graph["A"] = ["B","C"]`가 B,C(레벨 1)를 반환해서 "같은 레벨"처럼 보임 |

★ 딕셔너리 자체엔 "레벨" 정보가 없어. 레벨(깊이)은 그래프 구조(A에서 몇 단계 떨어졌나)로 결정되는 거지, 딕셔너리에 저장된 게 아니야.

### 3.6 다른 표현 — 인접 행렬 (참고만)

```python
# 인접 행렬 (2차원 배열). 노드가 많을 땐 메모리 낭비 but 조회 O(1)
import numpy as np
matrix = np.array([
    [0, 1, 1, 0],   # A행: A→B, A→C
    [0, 0, 0, 1],   # B행: B→D
    [0, 0, 0, 1],   # C행: C→D
    [0, 0, 0, 0],   # D행: 없음
])
```

★ DeZero는 인접 리스트 방식 — Variable의 `creator`가 "이 노드로 들어오는 엣지" 역할.

---

## 4. 순회(Traversal) — 모든 노드 방문하기

그래프의 모든(또는 일부) 노드를 방문하는 것. **두 가지 방식**이 있어.
§3의 **분기/합류 그래프**로 설명 (step15의 복잡한 그래프 형태):

```python
# 그래프:
#   A ──→ B ──┐
#    └──→ C ──┴──→ D    (B, C가 D로 합류)

graph = {
    "A": ["B", "C"],   # A의 이웃: B, C (분기)
    "B": ["D"],         # B의 이웃: D
    "C": ["D"],         # C의 이웃: D (합류)
    "D": [],            # D의 이웃: 없음
}
```

### 4.1 DFS (깊이 우선 탐색)

**한 길을 끝까지 파고든 뒤, 막히면 되돌아와서 다른 길**.

```python
def dfs(graph, start, visited=None):
    """DFS — 재귀 버전 (가장 직관적)."""
    if visited is None:
        visited = []
    visited.append(start)
    print(f"방문: {start}  (지금까지: {visited})")

    for neighbor in graph[start]:       # ★ graph[start] = 이 노드의 이웃들
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

dfs_result = dfs(graph, "A")
```

#### ★ DFS 단계별 추적 (이해 핵심)

`graph["A"] = ["B", "C"]`니까 A의 이웃은 B, C. for 루프가 이 순서대로 처리:

```
dfs(graph, "A") 시작
  visited = ["A"]
  graph["A"] = ["B", "C"]  → for 루프: 먼저 B, 다음 C

  ① neighbor = "B" (아직 방문 안 함) → dfs(graph, "B") 재귀 호출
     visited = ["A", "B"]
     graph["B"] = ["D"]  → for 루프: D

     ② neighbor = "D" → dfs(graph, "D") 재귀 호출
        visited = ["A", "B", "D"]
        graph["D"] = []  → for 루프 돌 게 없음 → return (막다른 길, 되돌아감)

     B의 for 루프 끝 → return

  ③ neighbor = "C" (아직 방문 안 함) → dfs(graph, "C") 재귀 호출
     visited = ["A", "B", "D", "C"]
     graph["C"] = ["D"]  → for 루프: D
        ★ D는 이미 방문됨 → skip (if neighbor not in visited)

     C의 for 루프 끝 → return

  A의 for 루프 끝 → return

최종 방문 순서: A → B → D → C
```

★ 핵심: **B를 끝까지 파고든 뒤(D까지), 돌아와서 C로 감**. "깊이" 우선.

### 4.2 BFS (너비 우선 탐색)

**같은 깊이(레벨)의 노드들을 먼저 다 방문한 뒤, 다음 깊이로**.

```python
from collections import deque

def bfs(graph, start):
    """BFS — 큐(deque) 사용."""
    visited = []
    queue = deque([start])            # ★ 큐(FIFO) — deque는 양끝 추가/제거가 빠른 큐

    while queue:
        node = queue.popleft()        # ★ 맨 앞에서 꺼냄 (FIFO — 들어온 순서대로)
        if node not in visited:
            visited.append(node)
            print(f"방문: {node}  (지금까지: {visited})")
            # ★ extend(iterable) — 리스트/튜플 등의 "모든 원소"를 한 번에 큐 끝에 추가.
            #   cf. append(x)는 x를 "1개의 원소"로 추가.
            #   예: queue.append(["B","C"]) → [["B","C"]] (리스트 1개가 원소로)
            #       queue.extend(["B","C"]) → ["B","C"] (각각 별도 원소로) ★
            #   즉 extend는 "리스트를 풀어서 각 원소를 추가" (A.7.5 언패킹과 같은 결)
            queue.extend(graph[node]) # ★ graph[node] = 그 노드의 이웃들 → 큐에 추가
    return visited

bfs_result = bfs(graph, "A")
```

#### ★ BFS 단계별 추적 (이해 핵심)

`queue`의 상태 변화를 따라가면 "너비 우선"이 보여:

```
초기: queue = ["A"], visited = []

① queue.popleft() → "A"
   visited = ["A"]
   graph["A"] = ["B", "C"]  → queue.extend → queue = ["B", "C"]

② queue.popleft() → "B"            ★ FIFO라 "A 다음에 들어온 B"부터
   visited = ["A", "B"]
   graph["B"] = ["D"]       → queue.extend → queue = ["C", "D"]

③ queue.popleft() → "C"            ★ B 다음에 들어온 C (D보다 먼저!)
   visited = ["A", "B", "C"]
   graph["C"] = ["D"]       → queue.extend → queue = ["D", "D"]  (D 2번 들어감)

④ queue.popleft() → "D"
   visited = ["A", "B", "C", "D"]
   graph["D"] = []          → queue.extend → queue = ["D"]  (남은 D 하나)

⑤ queue.popleft() → "D"            ★ 이미 방문됨 → skip (if node not in visited)
   queue = [] → 루프 종료

최종 방문 순서: A → B → C → D
```

★ 핵심: **B, C (같은 레벨)를 먼저 처리한 뒤 D로 감**. "너비" 우선.
★ D가 2번 큐에 들어가지만, 2번째엔 "이미 방문됨"으로 skip → 중복 방문 방지.

##### ★ 직접 확인 — `append` vs `extend` (파이썬 알몹 배려)

`append`와 `extend`의 차이를 실험으로 확인:

```python
from collections import deque

# append — 1개의 객체를 통째로 추가
q1 = deque([1, 2])
q1.append([3, 4])
print(list(q1))   # [1, 2, [3, 4]]  ← [3,4] 리스트가 "1개의 원소"로 통째로 ★

# extend — iterable의 각 원소를 풀어서 추가
q2 = deque([1, 2])
q2.extend([3, 4])
print(list(q2))   # [1, 2, 3, 4]    ← 3, 4가 각각 별도 원소로 풀어짐 ★
```

★ 왜 BFS에선 `extend`인가? `graph["A"] = ["B", "C"]`인데:
- `extend(graph["A"])` → 큐에 `"B"`, `"C"` 각각 들어감 (올바름 ✅)
- `append(graph["A"])` → 큐에 `["B", "C"]` 리스트가 통째로 들어감 → 다음 pop에서 **버그** ❌

→ `extend`는 "리스트를 풀어서 각 원소를 추가" — A.7.5 `*` 언패킹과 같은 결.
   `append`는 "리스트를 1개의 객체로 취급" — 풀지 않고 통째로.

### 4.3 핵심 차이 — 스택(LIFO) vs 큐(FIFO)

| | DFS | BFS |
|---|---|---|
| 자료구조 | **스택**(LIFO) | **큐**(FIFO) |
| 방향 | 깊이 우선 (한 길 끝까지) | 너비 우선 (같은 레벨부터) |
| 구현 | 재귀 또는 스택 | 큐 (deque) |
| 방문 순서 (위 그래프) | A → B → D → C | A → B → C → D |

```python
# 같은 worklist 구조지만 pop 방식이 다름:
worklist = [start]
while worklist:
    node = worklist.pop()        # ★ pop() = 맨 뒤 = LIFO = DFS
    # node = worklist.pop(0)     # pop(0) = 맨 앞 = FIFO = BFS (느림)
    # node = queue.popleft()     # deque.popleft = FIFO = BFS (빠름)
```

★ ★ DeZero의 `fill_grad`는 `worklist.pop()` = **LIFO = DFS 방식**.
step15는 "이 DFS 방식이 복잡한 그래프에서 순서 문제를 일으킬 수 있다"는 걸 다루고,
step16에서 generation 정렬로 해결.

---

## 5. 위상 정렬 (Topological Sort) — 의존성 순서

### 문제 — "어떤 순서로 처리해야 할까?"

DAG에서 노드들에 **의존성**이 있을 때, "먼저 처리해야 할 것부터" 나열하는 것.

예: 요리 순서
```
재료 손질 → (굽기, 소스 만들기) → 플레이팅
```
- "굽기"와 "소스 만들기"는 "재료 손질"이 끝난 뒤에 가능 (의존)
- "플레이팅"은 "굽기"와 "소스 만들기"가 끝난 뒤 (두 개에 의존)

→ 위상 정렬 = 이런 의존성 순서를 나열하는 것.

### 파이썬 구현 (Kahn's 알고리즘 — 간략 버전)

```python
from collections import deque

def topological_sort(graph):
    """DAG의 위상 정렬 — '들어오는 엣지'가 0인 노드부터."""
    # 진입 차수(in-degree) 계산 — 각 노드로 들어오는 엣지 수
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    # 진입 차수 0인 노드부터 큐에 (의존성 없는 시작점)
    queue = deque([n for n in graph if in_degree[n] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1    # 이 노드 처리했으니 의존성 하나 감소
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return result

# 위 graph 예시: A → (B, C) → D
print(topological_sort(graph))   # ['A', 'B', 'C', 'D'] 또는 ['A', 'C', 'B', 'D']
```

★ 핵심: **"들어오는 엣지가 0인 노드부터"** 처리 → 의존성이 해소된 노드만 다음으로.

### 위상 정렬의 두 구현 방식

| 방식 | 설명 |
|---|---|
| **Kahn's 알고리즘** ↑ | 진입 차수(in-degree) 0부터. BFS 스타일 |
| **DFS 기반** | DFS 끝나는 역순. 더 깊이 파면 나옴 (여기선 생략) |

---

## 6. DeZero와 연결 — 계산 그래프는 DAG, 역전파는 위상 정렬

이제 step15/16이 왜 이 개념들을 필요로 하는지 보여:

### ★★ 책 그림의 시각적 함정 — 2개 DAG가 하나에 겹쳐 보임 (브로 통찰)

> 책 step15/16 그림을 보면 화살표가 "순환처럼" 보여서 헷갈림.
> 브로가 정확히 감지: **이건 2개의 DAG를 하나의 다이어그램에 겹쳐 그린 것**.

DeZero는 순전파 한 번 실행할 때 **양쪽 방향의 그래프 정보를 동시에 구축**해:

#### DAG 1: 순전파 그래프 (Function이 간선 저장)

```
   x₀   x₁        ← 입력 Variable들
    │   │
    ▼   ▼         ← 순전파 방향 (데이터 흐름, ↓)
    Add          ← Function
      │
      ▼
      y          ← 출력 Variable
```

- **간선 정보 저장**: Function의 `inputs` / `output` 속성
  - `Add.inputs = (x₀, x₁)`, `Add.output = y`
- ★ "내가 누구를 받아 누구에게 주는지" — 단방향 순서는 함수 자체가 가정

#### DAG 2: 역전파 그래프 (Variable이 간선 저장, creator 링크)

```
      y          ← 출력 Variable
      ▲
      │          ← 역전파 방향 (grad 흐름, ↑ — 순전파와 반대)
    Add
    ▲   ▲
    │   │
   x₀   x₁      ← 입력 Variable들
```

- **간선 정보 저장**: Variable의 `creator` 속성
  - `y.creator = Add` → 역전파 시 `Add.inputs` 통해 x₀, x₁ 역추적
- ★ "나를 만든 Function이 누구인지" — 역방향 링크

#### 책이 이 둘을 겹쳐 그림 → "순환처럼" 보임

```
   x₀   x₁
    │   │
    ▼   ▼         ← 순전파 화살표 (Function.inputs/output, ↓)
    Add
      │
      ▼
      y
      ▲           ← ★ 역전파 화살표 (Variable.creator, ↑) — 같은 선에 겹쳐!
      │
    (Add 역추적)
```

→ 순전파 ↓ + 역전파 ↑ 가 **같은 선에 겹쳐서** 시각적으로만 순환처럼 보임.
실제론 **간선 정보가 다른 속성에 저장된 2개의 독립적인 DAG**.

#### 왜 "순환(사이클)"이 아닌가 — DAG인 이유

- 데이터(x→y): 한 방향(↓)으로만 흐름 — 절대 y에서 x로 데이터 안 돌아감
- grad(y→x): 한 방향(↑)으로만 흐름 — 절대 x에서 y로 grad 안 돌아감
- 두 흐름이 "같은 선"에 겹쳐 그려져서 **시각적으로만 순환** ★
- 실제론 사이클 없음 = **DAG** (방향성 비순환 그래프)

#### ★ Define-by-Run 설계의 정수

순전파 한 번 실행으로 **두 방향 그래프 정보가 모두 채워짐**:
- Function은 inputs/output 기록 (순전파 DAG)
- Variable은 creator 기록 (역전파 DAG)

그래서 역전파는 creator 링크만 따라가면 됨 (이미 구축된 역전파 DAG 탐색).
이게 "Define-by-Run" 이름의 유래 — **실행(Run)하면서 그래프를 정의(Define)** 하는 패러다임.

### ★★ DeZero에서 노드/간선 읽는 법 — 코드 어디에 숨어있나 (브로 지적)

> 브로: *"간선 정보를 개인적으로 캐치하기가 살짝 어렵다"*
> → 맞음. DeZero엔 Graph 클래스 같은 **명시적 자료구조가 없음**.
> 노드/간선이 Variable/Function 객체에 **흩어져 녹아있어**. 어디서 읽어야 하는지 매핑 필요.

#### 노드와 간선의 정체 — 코드 어디에?

| 그래프 개념 | DeZero 코드에서의 정체 | 어디 저장? |
|---|---|---|
| **노드 (node)** | `Variable` 객체 | — (객체 자체가 노드) |
| **간선 (edge)** 순전파 | Function의 `inputs`/`output` 속성 | Function 인스턴스 |
| **간선 (edge)** 역전파 | Variable의 `creator` 속성 | Variable 인스턴스 |

★ 핵심: DeZero에선 **"간선"이라는 별도 객체가 없음**. 간선 정보가 **객체의 속성(attribute)** 으로 녹아들어감.

#### ★ 방향성 읽는 법 — 화살표가 어디서 어디로?

브로가 "방향성과 관련해서 어떻게 읽어나가면 좋을지" 질문 — 코드에서 화살표를 추적하는 법:

##### 순전파 화살표 (↓ 방향) — Function 입장

```python
class Function:
    def __call__(self, *inputs):
        ...
        self.inputs = inputs    # ★ "내가 받은 입력들" ← 화살표의 시작점들
        self.output = output    # ★ "내가 만든 출력"   ← 화살표의 도착점
```

읽는 법: `f.inputs`에 있는 Variable들이 **→(화살표)→** `f.output`으로 모임.
```
inputs[0] ──┐
inputs[1] ──┴──→ f ──→ output    (f가 inputs를 받아 output 생성)
```

##### 역전파 화살표 (↑ 방향) — Variable 입장

```python
class Variable:
    def set_creator(self, func):
        self.creator = func      # ★ "나를 만든 Function" ← 역전파 화살표
```

읽는 법: `y.creator`에 있는 Function이 **y를 만든 놈**. 역전파는 이 링크를 **역방향(↑)** 으로 따라감.
```
y ──creator──→ Add    (y의 creator는 Add — "Add가 y를 만들었다")
                                    ↑ 역전파는 이 링크를 거꾸로 탐색
```

#### ★ 역전파 탐색 흐름 — 코드로 따라가기

`fill_grad`가 역전파 DAG를 어떻게 탐색하는지 (방향성 읽기):

```python
def fill_grad(start_var):
    # ① 시작점: 출력 Variable에서 creator 링크로 역방향 진입
    worklist = [start_var.creator]       # y.creator → Add (역전파 화살표 ↑)

    while worklist:
        f = worklist.pop()
        # ② Function의 output에서 grad 회수 (역전파 화살표 ↑)
        upstream_grad = f.output.grad   # f.output = y → y.grad 회수

        # ③ backward로 downstream 계산 (chain rule)
        downstream_grads = f.backward(upstream_grad)

        # ④ Function의 inputs로 역방향 확장 (역전파 화살표 ↑)
        for x, dg in zip(f.inputs, downstream_grads):
            x.grad = dg                  # x (입력 Variable)에 grad 할당
            if x.creator is not None:    # ★ x도 creator 있으면 더 역추적
                worklist.append(x.creator)   # 다음 Function으로 ↑
```

★ 방향성 핵심:
- **탐색은 항상 ↑ (역방향)**: output → creator → inputs → (그 inputs의 creator) → ...
- **화살표를 읽는 키**: `creator`(Variable에서 Function으로 ↑), `inputs`/`output`(Function에서 Variable로, 역전파에선 거꾸로 ↑)

#### ★ 일반 그래프와의 차이 — 왜 캐치 어려운가

| | 일반 그래프 자료구조 | DeZero 계산 그래프 |
|---|---|---|
| 노드/간선 | 명시적 (Node/Edge 객체) | **암묵적** (Variable/Function 속성 — 위 매핑 표 참조) |
| 그래프 저장 | 별도 Graph 클래스 | **흩어져 있음** (객체들에 분산) |
| 탐색 | Graph.traverse() 명시적 | fill_grad가 속성 체인으로 암묵적 탐색 |

→ ★ DeZero의 "간선"은 **객체 참조(reference)** 라는 점이 핵심. `y.creator = Add`는
파이썬 관점에선 그냥 "Add 객체를 참조하는 속성"이지만, 그래프 관점에선 **"y에서 Add로 가는 간선"**.
이중적 의미를 동시에 가짐 — 코드에선 속성, 그래프론 간선.

★ 이게 브로가 "캐치하기 어렵다"고 느낀 이유. 명시적 Graph 객체가 없으니까.

### DeZero의 그래프 = DAG

> ★ 참고: 여기부턴 노드명을 `A/B/C/D` 대신 **DeZero 기호**(`x/f/g/h`)로 전환.
> §4/§5의 일반 그래프 예시와 다르게 보일 수 있지만, 구조는 같은 분기+합류 DAG.
> DeZero 실제 코드(Variable/Function)와 직접 매핑하기 위해 기호를 바꿈.

```
   x
   │
   ├──→ f ──┐
   │        ├──→ h    ← f, g가 h로 합류
   └──→ g ──┘
```

- 방향성: 순전파 방향 (위에서 아래)
- 비순환: 역전파로 다시 위로 안 올라감 (데이터만 아래로 흐름)
- → DAG ★

### 역전파 = "역방향 위상 정렬"

역전파는 출력(y)에서부터 입력(x) 방향으로 처리. 이건 **"출력에 가까운 노드부터"** 처리하는 위상 정렬의 한 형태.

### step08의 fill_grad는? — worklist + LIFO (DFS 스타일)

```python
worklist = [start_var.creator]
while worklist:
    f = worklist.pop()              # ★ LIFO (DFS 스타일)
    ...
    worklist.append(x.creator)
```

★ 선형 그래프(square(square(x)))에선 문제 없음 — 갈래가 하나라 순서가 정해짐.

### ★ 문제 — 분기/합류 그래프에서 DFS 순서 꼬임

```
   x ─┬─→ f ──┐
      │       ├─→ h
      └─→ g ──┘
```

- h 역전파 → f, g worklist에 push → LIFO라 **f만 끝까지 파고들어감**
- f 경로: f → x (x.grad += f의 기여)
- 그런데 g가 아직 처리 안 됨 → x의 grad가 "완전하지 않은 상태"
- 그 후 g가 처리되어 x.grad에 또 더해짐 → ★ 순서가 보장 안 됨

★ 정확한 순서: **출력(h)에 가장 가까운 generation부터** 처리해야 함.

### step16의 해법 — generation으로 위상 정렬

각 Function에 **generation**(순전파 시 깊이) 부여:
```
   x (gen 0)
   │
   ├─→ f (gen 1) ──┐
   │               ├─→ h (gen 2)
   └─→ g (gen 1) ──┘
```

역전파 시 worklist를 **generation 내림차순으로 정렬**:
- gen 2 (h) 먼저 → gen 1 (f, g) → gen 0 (x)
- ★ "출력에 가까운(=gen 큰) 노드부터" → 합류 노드(x)는 f, g 모두 처리된 뒤에 방문

```python
# step16에서 추가될 코드 (예상)
worklist.sort(key=lambda f: f.generation, reverse=True)  # ★ gen 큰 순
```

→ 이게 사실상 **위상 정렬의 한 구현**. Kahn's 알고리즘과 정신적으로 같음 (의존성 순서 강제).

### ★★★ generation = 표현식 중첩 깊이 (브로 통찰 — 책 15.3 그림 해석)

> 브로가 책 15.3 그림(순전파 노드들에 "N세대" 주석)을 보고 **"왜 여기서 스택 프레임이 떠오르지?"** 라고 짚음.
> → ★★★ 직관이 정확! 핵심은 "순전파 실행 순서가 깊이로 기록된다"는 것.
> 다만 코드 구조에 따라 두 가지 관점이 있어 둘 다 이해 필요.

#### ★ 두 가지 코드 패턴 — 브로 직관의 적용 대상

##### 패턴 A: 순수 함수 합성 (DeZero 실제 사용 패턴)

```python
y = square(square(x))    # square의 인자로 square(x)의 "결과" 전달
```

파이썬은 **인자를 먼저 평가**하므로 실행 순서는 안→바깥:
1. 안쪽 `square(x)` 먼저 실행 → 완료 → 결과 (스택에서 사라짐)
2. 바깥 `square(그 결과)` 실행 → 완료

★ 두 square가 **동시에 스택에 공존하지 않음**. 둘 다 런타임 스택 깊이는 같음.
이 패턴에선 "런타임 스택 깊이 = generation"은 엄밀히 틀림. 정확한 건 **"표현식 중첩 깊이(nesting depth)"**:
- 안쪽 `square(x)` = 중첩 1 → generation 1
- 바깥 `square(...)` = 중첩 2 → generation 2

##### 패턴 B: 함수 본문 안에서 호출 중첩 (브로가 상상한 패턴) ★

```python
def composite_a(x):
    return composite_b(x) + 1       # ★ 본문 안에서 b 호출

def composite_b(x):
    return composite_c(x) * 2       # ★ 본문 안에서 c 호출

def composite_c(x):
    return x ** 2
```

★ 이 패턴에선 **진짜 스택 프레임 중첩**이 일어남!
- a 실행 중 b 호출 → b 실행 중 c 호출 → a, b, c가 **동시에 스택에 공존**
- 런타임 스택 깊이: 1 → 2 → 3으로 증가 (a=깊이 1, a가 b 호출=깊이 2, b가 c 호출=깊이 3)
- ★ 이땐 "런타임 스택 깊이 = 호출 깊이"가 정확히 맞음 — 브로 직관 그대로!

##### ★ 두 패턴 비교 — 왜 헷갈렸나

| | 패턴 A (DeZero 사용) | 패턴 B (브로 상상) |
|---|---|---|
| 코드 | `square(square(x))` | `a() { b() { c() } }` |
| 인자 평가 | 인자 먼저 → 안쪽 먼저 실행+완료 | 본문 순차 → a 실행 중 b 호출 |
| 동시 스택 공존 | ❌ 없음 | ★ **있음** (a,b,c 동시) |
| "런타임 스택 깊이" | 틀림 (동시 공존 X) | ★★ **맞음** (브로 직관 정확) |
| 정확한 용어 | 표현식 중첩 깊이 | 런타임 스택 깊이 |

★ 브로가 "스택 프레임"이라고 했을 때, 본문 안 호출 중첩(패턴 B)을 상상한 거라면
그 직관은 **완전히 맞음**. DeZero 사용법이 패턴 A라 "엄밀히는 중첩 깊이"로 정정한 것이지,
브로 직관 자체가 틀린 게 아님. 두 패턴 모두에서 "깊이 = generation"이라는 핵심은 동일.

#### ★ DeZero는 어느 패턴? — 패턴 A, 하지만 결과는 같아

DeZero 사용법 `y = square(square(x))`은 **패턴 A** (순수 합성).
근데 결과적으로 generation은 "부모 gen + 1"로 누적되므로, **패턴 B의 스택 깊이와 같은 값**이 나와.
- 패턴 A: 표현식 중첩 깊이로 generation 누적
- 패턴 B: 런타임 스택 깊이로 호출 깊이 누적
- ★ 두 패턴 모두에서 generation/깊이는 같은 순서로 증가

→ 브로가 패턴 B를 상상했든 패턴 A를 봤든, **"깊이가 누적된다"는 직관은 유효**.
DeZero는 패턴 A지만 "부모 gen + 1" 기록이 패턴 B의 스택 깊이와 정신적으로 같음.

#### ★ 함수 호출 그래프(call graph)와 계산 그래프의 관계

브로가 "함수 호출 그래프"를 떠올린 것도 핵심:

```
함수 호출 그래프 (call graph):
   square() ──호출──→ square() ──호출──→ Variable()
   (이것 자체가 DAG — 재귀/순환 없으면)

계산 그래프 (computation graph):
   Variable ──creator──→ Function ──inputs──→ Variable
   (이것도 DAG)

★ 두 그래프의 "깊이"는 동일!
  순전파 시 중첩 깊이 = 계산 그래프 깊이 = generation
```

→ 파이썬 함수 호출 구조가 **자연스럽게 generation을 "계산"** 해줌.
DeZero가 별도 깊이 추적 안 해도, "부모 generation + 1"만 기록하면 순전파 실행 순서가 보존됨.

#### ★ Define-by-Run과 generation의 관계

generation은 **런타임에 결정되는 값** (컴파일 타임 고정이 아님).
- 같은 코드 `y = square(square(x))`라도, x 값이 바뀌면 매번 새 순전파 실행 → 새 generation 부여
- 이게 "Define-by-Run"의 정수 — **실행(Run)할 때마다 그래프 구조 + generation이 함께 결정**
- cf. Define-and-Run: 그래프를 미리 정의하므로 "깊이"도 고정. generation 개념이 불필요.

→ 브로가 "런타임에서 생성되는"이라고 한 게 ★ 정확 — generation은 런타임(순전파 실행)에 비로소 값이 정해지는 정보.

### ★ 브로 "BFS?" 이해의 정확한 정정

| 브로 이해 | 정확한 답 |
|---|---|
| "DAG 그래프" | ✅ 정확 — DeZero 계산 그래프는 DAG |
| "BFS" | ★ **반틀림** — BFS와 비슷한 효과(같은 깊이 우선)를 내지만, 진짜 BFS는 아님 |

- BFS는 "같은 레벨(깊이)부터 퍼져나가는 순회 알고리즘"
- step16의 generation 정렬은 **"출력에 가까운 순서로 정렬"** — 이게 위상 정렬
- 핵심 차이: BFS는 순회 **방식**(큐 사용), generation 정렬은 **정렬 기준**. worklist가 스택이든 큐든 정렬되어 있으면 올바른 순서 보장

→ 브로 직관 "순회 순서가 중요하다"는 정확했어. 정확한 용어는 **위상 정렬**.

---

## 7. 요약표

| 개념 | 핵심 | DeZero 연결 |
|---|---|---|
| **그래프** | 노드+엣지로 관계 표현 | Variable/Function 그래프 |
| **DAG** | 방향 + 비순환 | DeZero 계산 그래프의 형태 ★ |
| **DFS** | 깊이 우선 (스택/LIFO) | 현재 fill_grad의 방식 |
| **BFS** | 너비 우선 (큐/FIFO) | (참고용, DeZero 직접 사용 X) |
| **위상 정렬** | 의존성 순서 나열 | 역전파 순서 = 역방향 위상 정렬 ★ |
| **generation** | 순전파 깊이 기록 | step16에서 도입, 위상 정렬 구현 수단 |

---

## 8. 🔓 더 파고 싶으면 (확장 후보, open-ended)

> ★ 브로 철학: "가벼운 마음으로 넘어가되, 나중에 더 파고 싶으면 이 주제들로."
> step16 진행하다 막히거나 호기심 생기면 회수할 후보들.

### 후보 주제들 (필요 시 별도 탐구)

| 주제 | 언제 필요? | 키워드 |
|---|---|---|
| **DFS 기반 위상 정렬** | Kahn's 외에 다른 구현 궁금할 때 | DFS, finish time 역순 |
| **사이클 검출** | "왜 DAG여야 하는지" 깊이 파고 싶을 때 | 순환 그래프면 역전파 무한 루프 |
| **인접 행렬 vs 인접 리스트** | 그래프 표현 trade-off 궁금할 때 | 메모리 vs 조회 속도 |
| **강연결 컴포넌트(SCC)** | 그래프 이론 깊이 파고 싶을 때 | Tarjan, Kosaraju 알고리즘 |
| **최단 경로 (Dijkstra/Bellman-Ford)** | 그래프 알고리즘 전반 탐구 | 가중치 그래프 |
| **A* 알고리즘** | 길 찾기 문제 관심 있을 때 | 휴리스틱 탐색 |
| **DeZero generation 정렬 복잡도** | step16 성능 분석 | O(n log n) sort 비용 |

### 회수 시그널

- step16 구현 중 "왜 generation으로 정렬하는 거지?" → 본 노트 §5, §6 복습
- "위상 정렬이 Kahn's 말고도 있나?" → 후보 "DFS 기반 위상 정렬"
- "DAG가 아닌 그래프(순환)면 어떻게 될까?" → 후보 "사이클 검출"

→ 이 노트는 **step16의 사전 학습 자료**이자 **확장을 위한 점검판**. 필요할 때 돌아오면 됨.

---

## 🔑 핵심 키워드

`#그래프` `#graph` `#노드` `#node` `#엣지` `#edge` `#DAG` `#방향성비순환그래프` `#인접리스트` `#adjacency-list` `#DFS` `#깊이우선탐색` `#BFS` `#너비우선탐색` `#스택` `#LIFO` `#큐` `#FIFO` `#위상정렬` `#topological-sort` `#Kahns-algorithm` `#의존성순서` `#진입차수` `#in-degree` `#generation` `#step15배경지식` `#step16연결` `#브로BFS이해반틀림` `#DeZero역전파순서` `#fill_grad` `#worklist` `#확장후보` `#open-ended` `#가벼운탐구`

## 📝 학습 완료일 / 관련 링크

**학습 완료일**: 2026-07-30 (step15 진행 중)
**관련 링크**:
- step15 진행 이슈: #18
- step16 (generation 구현) — 다음 step
- step08 design_patterns Worklist Algorithm — 기존 fill_grad의 그래프 순회 패턴
- exploration_11 autodiff_modes §7 (Define-by-Run) — 그래프가 매번 생성되는 이유
