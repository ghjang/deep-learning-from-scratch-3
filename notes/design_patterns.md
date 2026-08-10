# 🎨 디자인 패턴 노트 — DeZero에 등장하는 패턴들

> DeZero(및 `rezero`) 구현에 등장하는 **소프트웨어 디자인 패턴**을 정리하는 누적형 레퍼런스.
> step 진행 중 패턴이 발견될 때마다 이 파일에 추가/업데이트.
>
> 다루는 범위:
> - GoF 23패턴 등 표준 정의 (일반적 패턴 설명)
> - DeZero/rezero **메타 패턴** (점진적 설계, 복선/회수, 학습 서사 등 책/학습 고유 패턴)
> - 알고리즘 패턴 (Worklist, 위상 정렬 등)
> - 코드 스니펫은 최소, 핵심 구조만
> - 각 패턴이 **어느 step**에 등장하는지 위치 명시

---

## 📋 인덱스

| # | 패턴 | 최초 등장 | 분류 |
|---|---|---|---|
| 1 | Wrapper (래퍼 / 박싱) | step01 | 구조 (GoF: Decorator/Adapter 근원) |
| 2 | Template Method | step02 | 행동 (GoF) |
| 3 | 점진적 설계 / 미래 복선 (Progressive Design / Forward-Laying) | step07~ | 메타 (책의 설계 철학) |
| 4 | Worklist Algorithm (처리 대기열 알고리즘) | step08 | 알고리즘 (CS 학술, GoF 외) |

> 📖 하단에 [용어집(Glossary)](#📖-용어집-glossary--번역이-어색한-oop패턴-용어-모음) 섹션 있음 — 한국어 OOP/패턴 용어 중 원어 모르면 이해 어려운 것들.

---

## 1. Wrapper 패턴 (래퍼 / 박싱)

### 📖 일반 설명

**한 객체를 다른 객체로 감싸서(Wrap)** 새로운 인터페이스를 제공하거나 기능을 확장하는 패턴.
원본 객체의 동작은 그대로 보존하면서, 겉에 "상자"를 씌워 메타정보/추가 동작을 덧붙임.

- **Java의 예**: `int`(원시) → `Integer`(객체) 박싱. `BufferedReader`가 `Reader`를 감쌈.
- **Python의 예**: `functools.wraps`가 함수를 감쌈, `collections.deque`가 리스트를 감쌈.
- **표준 분류**: GoF의 **Decorator**(기능 추가)와 **Adapter**(인터페이스 변환)의 근원이 되는 더 원초적 개념. "래퍼"는 패턴 언어에서 구조적 관용구로 널리 쓰임.

### 🎯 DeZero 등장 지점

#### step01 — `Variable`이 `ndarray`를 감쌈

```python
class Variable:
    def __init__(self, data):
        self.data = data   # ndarray를 상자 안에 넣음
```

- **왜 감싸는가?**: `ndarray` 자체엔 "이 데이터가 어떤 연산에서 왔는지" 추적 기능이 없음.
- **감싸서 얻는 것**: `grad`(미분값), `creator`(어떤 Function이 만들었는지) 등 역전파 메타정보를 붙일 공간 확보.
- **PyTorch/TensorFlow 동일 철학**: `Tensor` 클래스가 ndarray 대신 감싸는 구조.

#### (예정) 이후 step에서 래퍼 재등장
- step50: `Parameter`가 `Variable`을 다시 감쌈 (가중치 표현용)
- step51: `Model`이 여러 `Layer`/`Parameter`를 감쌈

### 🔑 핵심 키워드

`#래퍼` `#박싱` `#박스(Box)` `#메타정보추가` `#관심사분리`

---

## 2. Template Method 패턴

### 📖 일반 설명

**기반 클래스(base class)가 알고리즘의 뼈대(골격)를 정의**하고,
**구상 클래스(concrete subclass)가 살(특정 단계의 구현)을 붙이는** 행동 패턴.

- "무엇을 할지는 고정, 어떻게 할지는 자식에게 위임"
- GoF 23패턴 중 **행동(Behavioral)** 분류
- **전형적 예**: 프레임워크에서 흔히 보는 "여기는 우리가 정해둠, 너희는 이 메서드만 구현해"

### 🎯 DeZero 등장 지점

#### step02 — `Function.__call__`이 뼈대, `forward()`가 살

```python
class Function:
    def __call__(self, input_var):
        x = input_var.data              # ① 상자 까기
        y = self.forward(x)             # ② 핵심: 자식이 구현한 forward 호출 ← 패턴의 정수
        return Variable(y)              # ③ 상자 포장

    def forward(self, x):
        raise NotImplementedError()     # 자식이 반드시 구현해야 함


class Square(Function):                 # 자식은 forward()만 정의하면 OK
    def forward(self, x):
        return x ** 2
```

- **뼈대(`__call__`)**: "상자 까기 → 계산 → 상자 포장" 흐름. 이 알고리즘은 모든 Function에 동일.
- **살(`forward`)**: `x ** 2`냐 `np.exp(x)`냐 `x + y`냐 — 함수마다 다름. 자식이 채움.
- **`raise NotImplementedError()`**: "자식이 안 구현하면 바로 에러"라는 강제. 파이썬 전통적 추상 메서드 관용구.

### 💡 통찰

- **"상자는 기반 클래스가, 공은 자식이"** — 관심사 분리(SoC, Separation of Concerns).
  - `Function.__call__`: Variable 상자 언팩/패킹 (프레임워크 관심사)
  - `Square.forward`: 순수 수학 연산 (도메인 관심사)
- **PyTorch와의 연결**: `torch.nn.Module.__call__` → `forward()` 구조가 동일. DeZero가 PyTorch 스타일인 이유가 여기에.
- **`abc.ABC`와 비교** (탐구 후보): `raise NotImplementedError()` 대신 `@abstractmethod` 데코레이터를 쓰면 인스턴스화 자체를 막을 수 있음. DeZero는 전통적 방식 택함 (나중에 깊이 파볼 주제).

> 🔬 **심화 탐구**: [exploration_09_abc_abstract.md](./exploration_09_abc_abstract.md) — `abc.ABC` vs `NotImplementedError` 비교, 우리 step02 코드를 abc로 바꿨을 때의 변화, 왜 책은 전통 방식을 택했는지 분석

### 🔑 핵심 키워드

`#TemplateMethod` `#GoF` `#행동패턴` `#기반클래스` `#추상메서드` `#NotImplementedError` `#관심사분리` `#SoC` `#PyTorch스타일`

---

## 3. 점진적 설계 / 미래 복선 (Progressive Design / Forward-Laying)

### 📖 일반 설명

**지금 단계에선 과잉이거나 의미 없어 보이는 구조를, 미래 단계의 확장을 대비해 미리 깔아두는 설계 패턴.**
"복선(forshadowing)"이라는 문학 용어를 빌려옴 — 소설에서 뒤에 일어날 사건을 앞서 암시하듯,
코드에서도 뒤에 추가될 기능을 현재 구조에 미리 염두에 두는 것.

**GoF 23패턴에 없는 "메타 패턴"** — 특정 코드 구조가 아니라 **"책/프레임워크가 단계를 밟는 방식"** 자체를 가리킴.
밑바닥부터 시작하는 딥러닝 시리즈처럼 **점진적 구축(progressive building)** 을 전제로 한 학습용 코드에서 두드러짐.

**특징**:
- 현재 시점엔 "왜 이렇게?" 의문이 드는 구조
- 미래 step에서 그 구조가 자연스럽게 활용되며 의미가 드러남
- 미리 깔아두지 않았으면 미래 step에서 **리팩터링(구조 변경)** 이 필요했을 자리

**트레이드오프**:
- ✅ 확장 비용 낮춤 (미래 step에서 구조 안 바꿈 → 버그 위험 감소)
- ✅ 학습자에게 "이건 단순하지 않을 수 있다" 신호 (의심을 유도하는 교육적 가치)
- ⚠️ 현재 시점 가독성 약간 떨어짐 ("왜 리스트지?" 같은 의문)
- ⚠️ 과잉 엔지니어링 경계 — 정말 확장될지 모르면 YAGNI 위반

### 🎯 DeZero 등장 지점

#### step07 → step16 — `set_creator` 메서드 (generation 복선)

```python
# step07: 한 줄짜리 메서드 — 단순 속성 할당과 다를 바 없음
def set_creator(self, func):
    self.creator = func

# step16에서 추가될 로직 (dezero/core.py:81-83)
def set_creator(self, func):
    self.creator = func
    self.generation = func.generation + 1   # ★ 복선 회수 — 복잡한 계산 그래프 정렬용
```

- step07 시점엔 `output.creator = self` 직접 할당과 동일 → "왜 메서드?" 의문 (브로가 실제로 제기)
- 답: step16 "복잡한 계산 그래프(generation)"에서 `generation` 설정이 추가될 **확장 포인트** 예약
- 메서드가 아니었으면 step16에서 메서드로 리팩터링 필요 → 이중 작업
- 상세: REZERO_CHANGES.md 항목 12번 (브로 의심 → 검증 → "미래 확장 때문" 납득)

#### ★ step08 → step14/16 — `funcs` 리스트 (DAG 복선) — 브로 질문에서 발견

```python
# step08 fill_grad 내부
funcs = [start_var.creator]   # ★ 왜 리스트? 현재는 길이 1뿐인데?
while funcs:
    f = funcs.pop()
    ...
    if x.creator is not None:
        funcs.append(x.creator)
```

**step08 시점엔 리스트일 이유가 없음** — 선형 체인 `x → A → a → B → b → C → y`라
스택에 동시에 **최대 1개**만 존재. `f = start_var.creator; while f: ...` 단일 변수 루프와 결과 동일.

**왜 리스트인가?** — step14/16에서 **분기 그래프(DAG)** 가 등장하면 리스트가 필수가 되기 때문:

```python
# step14 "같은 변수 반복 사용" — x가 두 갈래로 쓰임
y = x + x
#     x ──→ add ←── x
#     └────────┘
# 역전파 시 add 노드 하나 pop → x로 grad 전달, 그런데 x.creator는 동일 → 중복 처리 이슈
# → step16에서 seen_set 등으로 관리하며 funcs에 복수 노드 push 발생

# step16 "복잡한 계산 그래프" — 다중 분기 정식화
a = A(x); b = B(x); c = C(a, b)
#     x ─→ A ─→ a ─┐
#     └→ B ─→ b ─→ C → c
# 역전파: C pop → A, B push → funcs에 2개 동시 존재 ★ 리스트 필수
```

**책 최종 코드(dezero/core.py)의 funcs** — 복수 노드를 담는 진짜 스택:
```python
funcs = []
seen_set = set()
self.add_func(self.creator, funcs, seen_set)   # 헬퍼로 추가 (중복 방지 포함)
while funcs:
    f = funcs.pop()
    gys = [output.grad for output in f.outputs]   # 다중 출력의 grad
    gxs = f.backward(*gys)                        # 다중 입력 역전파
    for x, gx in zip(f.inputs, gxs):              # 각 입력에 grad 분배
        if x.creator is not None:
            x.add_func(x.creator, funcs, seen_set)  # ★ 복수 노드 push
```

step08의 `funcs = [start_var.creator]`는 이 구조의 **단순화된 버전(선형 특수 케이스)**.
리스트 타입 자체가 "복수 노드 가능"을 **타입으로 선언** — 미래 DAG 확장을 대비한 복선.

**브로 통찰의 가치**: *"코드만 봐도 현재 시점에서는 그냥 리스트에 1개만 최대 있을 수 있는 구조 아니야?"*
→ 정확한 관찰. "현재 과잉"을 감지한 것 자체가 이 패턴을 인식한 것. 의심이 패턴 발견으로 이어짐.

#### (예정) 이후 step에서 재등장 가능한 복선들
- `Function.outputs` (복수) — 현재는 단일 출력이지만 step13(가변 길이)에서 복수 출력 대비
- `Config` 클래스 — step18에서 본격 등장하지만 그 전부터 흔적 있을 수 있음
- `as_variable` / `as_array` 헬퍼 — step11+ 가변 길이 대비

### 🔑 핵심 키워드

`#점진적설계` `#ProgressiveDesign` `#복선` `#foreshadowing` `#미래확장` `#Forward-Laying` `#메타패턴` `#set_creator` `#generation` `#funcs리스트` `#DAG복선` `#선형vs분기그래프` `#확장포인트예약` `#리팩터링회피` `#YAGNI경계` `#단계적구축` `#책설계철학`

### 💡 식별 힌트 (이 패턴 의심해볼 신호)

현재 step 코드를 보고 이런 의문이 들면 → 복선일 가능성 점검:
1. **"왜 컬렉션(리스트/딕셔너리)인데 요소 1개뿐이지?"** → 미래 다중 대응 복선 의심 (funcs 리스트)
2. **"왜 메서드/속성인데 한 줄이지? 직접 할당과 다를 바 없는데?"** → 미래 로직 추가 복선 의심 (set_creator)
3. **"왜 타입 힌트/클래스 계층이 현재 필요 이상으로 정교하지?"** → 미래 확장 대비 의심
4. **"이 속성 저장해두는데 지금 안 쓰이네?"** → 미래 step에서 사용 복선 (self.output)

→ 해결법: **"최종 코드(dezero/)에서 이 부분이 어떻게 쓰이나?"** 확인. 추가 로직/복수 처리 있으면 복선 확정.

### ⚠️ 주의 — 과잉 엔지니어링과의 구분

복선 ≠ 무조건 좋음. **정말 확장될지 확실하지 않으면 YAGNI(You Aren't Gonna Need It)** 위반.
- DeZero는 **책이라 미래 step이 정해져 있음** → 복선이 정당화됨 (작성자가 확장 계획을 앎)
- 일반 프로젝트에선 "확장될 것 같은데..."로 과잉 구조를 미리 깔면 오히려 복잡도만 늘림
- → "복선"은 **확장 경로가 명확히 예정된 경우**에만 정당.

### 🔗 관련

- 밑바닥부터 시작하는 딥러닝 시리즈 전체의 설계 철학 (점진적 구축)
- YAGNI (eXtreme Programming 원칙) — 복선의 안티테제스
- REZERO_CHANGES.md 항목 12번 (set_creator 복선 — 브로 의심 → 검증 사례)
- step08 학습 — worklist(옛 funcs) 리스트 복선 발견 (브로 질문에서 파생)

---

## 4. Worklist Algorithm (처리 대기열 알고리즘)

### 📖 일반 설명

**"처리할 노드를 대기열(worklist)에 넣고, 빌 때까지 하나씩 꺼내 처리 + 새 대상 추가"** 구조.
CS 학술에서 정식으로 정의된 **알고리즘 패턴**. GoF 23패턴(객체지향 설계 패턴)엔 없지만,
**알고리즘/컴파일러/정적 분석 분야**에서는 거의 모든 그래프 기반 계산의 기본 골격.

**골격 (모든 worklist algorithm의 공통 형태)**:
```
worklist = [초기 work item(들)]
while worklist:
    item = worklist.pop()     # 처리 대상 work item 하나 꺼내기
    결과 = 처리(item)         # work item 처리 (계산/마킹/전파 등)
    for next in 후속(item):   # 이 item이 가리키는 다음 대상들
        if 조건(next):        # (방문 안 함 / 변경됨 등)
            worklist.append(next)
```

**핵심 용어**:
- **worklist** = 처리 대기열 (리스트/큐/스택)
- **work item** = worklist의 원소 하나하나, 즉 처리 단위 ★
  - work item이 **무엇인가**는 알고리즘마다 다르고, 그 구체화가 알고리즘의 정체를 결정 (아래 표 참고)

**특징**:
- `pop()` 순서에 따라 **DFS**(스택, LIFO) 또는 **BFS**(큐, FIFO)가 됨
- "방문 집합(visited set)"으로 중복 처리 방지 (필요 시)
- 종료 조건: worklist가 빌 때 (더 이상 처리할 게 없음)

### 🎯 등장 분야 (CS 전반)

이 패턴은 의외로 널리 쓰임. 같은 골격, 다른 용도:

| 분야 | 용도 | work item |
|---|---|---|
| **역전파 (autograd)** | 미분값 전파 | **Function 인스턴스** ★ (우리 케이스) |
| **컴파일러 데이터플로우 분석** | 도달 정의, 라이브 변수 | CFG 노드/엣지 |
| **가비지 컬렉션** | mark-and-sweep | 객체 참조 |
| **그래프 순회** | DFS/BFS, 위상 정렬 | 정점 (vertex) |
| **모델 체킹** | 상태 공간 탐색 | 상태 (state) |
| **구문 분석 (파싱)** | CKY 파서 등 | 규칙/span |
| **타입 추론** | Hindley-Milner | 미해결 타입 제약 |

### 🎯 핵심 참고 자료 (학술 어디에 기록되나 — 브로 질문)

- **Dragon Book** (Aho-Lam-Sethi-Ullman, *Compilers: Principles, Techniques, and Tools*) —
  데이터플로우 분석의 worklist 알고리즘 (reaching definitions 등)
- **Nielson-Nielson-Hankin**, *Principles of Program Analysis* — 추상 해석/정적 분석의 worklist
- **Jones-Hosking-Moss**, *The Garbage Collection Handbook* — GC mark phase의 worklist
- **CLRS** (Cormen et al., *Introduction to Algorithms*) — DFS/BFS가 넓은 의미의 worklist
- **Cooper-Torczon**, *Engineering a Compiler* — worklist 기반 데이터플로우 최적화

→ "worklist algorithm"이라는 용어 자체는 **컴파일러/정적 분석 교과서**에서 가장 정식으로 다룸.

### 🎯 DeZero/rezero 등장 지점

#### step08 — `fill_grad()` 역전파 순회 (★ 이 패턴의 인스턴스)

```python
def fill_grad(start_var, upstream_grad=None):
    ...
    worklist = [start_var.creator]       # ★ worklist 초기화
    while worklist:                       # ★ "빌 때까지"
        f = worklist.pop()                # 처리 대상 Function 꺼내기 (LIFO → DFS)
        x, y = f.input, f.output
        x.grad = f.backward(y.grad)       # 노드 처리 (grad 전파 = fold step)

        if x.creator is not None:         # 후속 노드(입력 쪽)가 있으면
            worklist.append(x.creator)    # worklist에 push
```

★ 매핑:
| 일반 골격 | DeZero 역전파 |
|---|---|
| 초기 노드 | `start_var.creator` (최종 출력을 만든 함수) |
| 처리(n) | `f.backward(y.grad)` — 단일 노드의 국소적 미분 fold step |
| 후속(n) | `x.creator` (입력 변수를 만든 함수) |
| 종료 | `worklist` 빈 경우 (입력 원점 도달) |
| 순회 방향 | 역방향 + LIFO(pop) = **DFS** (깊이 우선) |

→ DeZero의 역전파는 **"그래프 역방향 DFS with worklist"**의 정확한 인스턴스.
브로가 "funcs를 worklist로 바꾸자" 한 것은, **이름만 바꾼 게 아니라 코드가 속한 학술 전통을 인식한 것**.

### 🎯 ★ 타입 힌트로 "work item이 무엇인가" 명시 (항목 17번 연장)

브로 통찰: *"work item이 Function 인스턴스 → 타입 힌트로 명확히 할 수 있지 않나?"*
→ 맞음. worklist를 단순 `list`가 아니라 **`list[Function]`** 으로 선언하면, "work item = Function 인스턴스"가 타입 수준에서 명시됨.

```python
# Python 3.12+ type 문 — "Worklist" 개념에 타입 별칭 부여
type Worklist = list[Function]

def fill_grad(start_var, upstream_grad=None):
    if start_var.creator is None: raise ...    # ★ guard clause (항목 16번)
    worklist: Worklist = [start_var.creator]    # ★ Optional[Function]이 아닌 list[Function] — 안전
```

★ **시너지 — guard clause(#016)와 타입 힌트가 협력**:
- `start_var.creator: Optional[Function]` 이라 그냥 `list[Function]`에 넣으면 pyright 에러
  (`list[Function | None]`를 `list[Function]`에 할당 불가)
- 근데 도입부 guard(`if creator is None: raise`)가 **타입 좁히기(type narrowing)** 수행
  → 그 아래부턴 `start_var.creator: Function` (Optional 풀림) → `list[Function]` 안전

→ 실증 (step08 학습 중):
```
case1 (guard 없음): error "list[Function | None]" is not assignable to "list[Function]"
case2 (guard 있음): ★ 에러 없음 — guard가 Optional → Function으로 좁힘
```

**★ 교훈 — 변형들이 독립이 아니라 세트**:
step08의 변형 3종(#015 fill_grad, #016 guard clause, #017 worklist)이 개별 결정인 줄 알았더니,
타입 힌트를 넣는 순간 **#016이 #017에 타입 안전성을 제공**한다는 게 드러남.
guard clause가 단순 "빠른 실패"가 아니라 **타입 좁히기**까지 보너스로 가져오는 구조.
→ 좋은 설계 결정들은 서로 강화한다 (emergent design).

### 🎯 ★ 패턴 3 (점진적 설계)과의 시너지

step08의 worklist는 **패턴 3(복선)** + **패턴 4(worklist)** 가 겹친 사례:
- **패턴 3**: 현재(step08 선형)는 worklist 길이 1이지만, step14/16 DAG 대비해 리스트(=worklist)로 미리 깔아둠
- **패턴 4**: 그 리스트가 worklist algorithm의 정확한 골격을 따름

→ 브로의 두 질문("왜 리스트?", "funcs 말고 worklist로?")이 **같은 코드의 두 층위**를 각각 파낸 것.

### 🔑 핵심 키워드

`#WorklistAlgorithm` `#처리대기열` `#그래프순회` `#역방향DFS` `#데이터플로우분석` `#가비지컬렉션` `#mark-sweep` `#고정점계산` `#fixpoint` `#컴파일러` `#정적분석` `#Dragon-Book` `#CLRS` `#LIFO스택` `#FIFO큐` `#DFS` `#BFS` `#방문집합` `#visited-set`

### 🔗 관련

- step08 `rezero/steps/step08.py` — worklist 기반 역전파 구현
- Dragon Book (Aho et al.) — 컴파일러 데이터플로우 분석의 worklist
- CLRS Introduction to Algorithms — 그래프 순회의 "처리 대기 큐/스택"
- REZERO_CHANGES.md 항목 17번 (funcs → worklist 리네임)
- 패턴 3 (점진적 설계) — worklist가 리스트형인 이유 (DAG 복선)

---

## 📌 참고: 패턴 간 구분 (자주 헷갈리는 포인트)

### Wrapper vs Template Method

두 패턴은 **다른 레벨**의 관심사:

| | Wrapper | Template Method |
|---|---|---|
| **무엇을?** | 객체를 객체로 감쌈 | 알고리즘 뼈대를 고정 |
| **DeZero 사례** | `Variable`이 `ndarray`를 감쌈 | `Function.__call__`이 호출 흐름 고정 |
| **등장 step** | step01 | step02 |
| **GoF 분류** | 구조 (Decorator/Adapter 근원) | 행동 |

→ `Variable`(래퍼)을 `Function.__call__`(템플릿)이 다루는 구조. 두 패턴이 **협력**해서 DeZero의 기본 골격을 이룸.

---

## 📖 용어집 (Glossary) — 번역이 어색한 OOP/패턴 용어 모음

> 한국어 OOP/패턴 용어 중 **원어를 모르면 이해하기 어려운** 것들 정리.
> 일상어와 의미가 충돌하거나, 번역이 어색해 헷갈리는 경우 위주.

| 한국어 | 원어 | 실제 의미 | 비고 |
|---|---|---|---|
| **구상 클래스** | Concrete class | "구체화된 클래스" — 실제 구현을 가진 자식 클래스 | ⚠️ 일상어 "구상(구상하다=생각하다)"과 충돌. OOP에선 "abstract(추상) ↔ concrete(구체)" 대척 개념 |
| **추상 클래스** | Abstract class | "추상적인 클래스" — 구현 없이 개념만 정의한 부모 클래스 | 비교적 직관적이라 헷갈림 적음 |
| **래퍼** | Wrapper | "감싸는 것" — 객체를 다른 객체로 감싸는 구조 | 일상어와 일치, 헷갈림 없음 |
| **데코레이터** | Decorator | (1) **패턴**: 기능 추가를 위해 객체를 감쌈. (2) **파이썬 기능**: `@` 구문으로 함수/클래스 장식 | ⚠️ 두 의미 혼동 주의. GoF 패턴 vs 파이썬 `@decorator` |
| **디스크립터** | Descriptor | 속성 접근을 커스터마이징하는 객체 (`__get__`, `__set__`) | 번역 없이 음차. `property`가 대표적 디스크립터 |
| **메타클래스** | Metaclass | "클래스의 클래스" — 클래스 생성을 커스터마이징 | `type`이 최상위 메타클래스. abc.ABCMeta 등 |
| **인스턴스** | Instance | 클래스로부터 생성된 구체적 객체 | 번역 없이 음차. 일상어 혼동 적음 |
| **인스턴스화** | Instantiation | 클래스 → 인스턴스를 만드는 행위 | "instantiation"의 번역. "객체 생성"과 거의 동의어 |
| **상속** | Inheritance | 부모 클래스의 속성/메서드를 자식이 물려받음 | 직관적 |
| **오버로딩** | Overloading | 같은 이름의 함수/연산자를 여러 정의로 쓰는 것 | ⚠️ 파이썬에선 진짜 오버로딩 없음. 연산자 오버로딩은 `__add__` 등 매직 메서드 정의 |
| **오버라이딩** | Overriding | 부모의 메서드를 자식이 **재정의**하는 것 | Square.forward가 Function.forward를 오버라이딩 |
| **매직 메서드** | Magic method (dunder) | `__init__`, `__call__` 등 밑줄 2개로 둘러싼 특수 메서드 | "dunder" = double underscore. "스페셜 메서드"라고도 |
| **메서드** | Method | 클래스 내부에 정의된 함수 | ⚠️ C++에서는 "멤버 함수(member function)"라 부름. Python/Java/C#/Ruby 등은 "메서드". 사실상 동일 개념, 언어 전통만 다름 (C++: 함수 중심 / Smalltalk: 메시지 전달 패러다임) |
| **@override** | Override 데코레이터 (Python 3.12+) | 부모 메서드를 재정의함을 명시 | ⚠️ 런타임 강제력 ❌ (정적 분석 도구 mypy/pyright 필수). C++ `override`/Java `@Override`와 비슷하지만 강제력 약함. 상세: exploration_09 §9 |

### 💡 자주 헷갈리는 쌍

- **추상(abstract) ↔ 구상(concrete)**: 개념 ↔ 구현. GoF 책의 기본 대척.
- **오버로딩(overloading) ↔ 오버라이딩(overriding)**: 이름 같은 여러 함수 ↔ 부모 메서드 재정의. **파이썬에선 오버라이딩만 진짜 기능**.
- **인스턴스(instance) ↔ 객체(object)**: 거의 동의어. 엄밀히는 "클래스로부터 만든 객체"가 인스턴스.
- **매개변수(parameter) ↔ 인자(argument)**: 정의부 변수 ↔ 호출부 값 (step02 결정 기록에서 정리)
- **메서드(method) ↔ 함수(function)**: 클래스 내부 정의 ↔ 독립 함수. C++ "멤버 함수" = "메서드". 파이썬에선 실제로 "첫 인자 self 자동 바인딩" 설명자로 함수를 감싼 것뿐
- **@override ↔ @abstractmethod**: 재정의 명시 (정적 분석) ↔ 구현 강제 (런타임). 강제력과 검사 시점이 다름. 상세: exploration_09 §9

---
