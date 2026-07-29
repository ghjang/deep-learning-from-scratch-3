# 탐구 17 — 파이썬 테스팅 패러다임 진화: unittest에서 pytest로

> **시점**: step10 학습 준비 중 (2026-07-29)
> **출처**: 브로 질문 — *"밑시딥 3권이 나온 지 좀 됐고 파이썬도 발전했는데, step10의 unittest가 여전히 유효한가? 더 나은 국룰이 나왔나?"*
> **짝**: [AGENTS.md "책 vs rezero+AI" 학습 철학](../AGENTS.md) — "매체(책)의 시대 한계" 시리즈
> **동기**: 책이 가르치는 unittest가 여전히 동작은 하지만, 파이썬 실무의 사실상 국룰은 pytest로 전환됨. "왜 책은 unittest를 가르치나?" → 교육적 선택 vs 실무 국룰.

---

## 📋 목차

1. [결론부터 — unittest 유효하지만 국룰은 pytest](#1-결론부터--unittest-유효하지만-국룰은-pytest)
2. [unittest — Java JUnit 유산 (2001)](#2-unittest--java-junit-유산-2001)
3. [pytest — 혁신적 단순화 (2005/2010대 폭발)](#3-pytest--혁신적-단순화-20052010대-폭발)
4. [★ 왜 책은 unittest를 가르치나 — 교육적 합리적 선택](#4-왜-책은-unittest를-가르치나--교육적-합리적-선택)
5. [pytest 역호환 — unittest 코드를 그대로 실행](#5-pytest-역호환--unittest-코드를-그대로-실행)
6. [최신 트렌드 (2024-2026) — pytest 생태계 확장](#6-최신-트렌드-2024-2026--pytest-생태계-확장)
7. [DeZero/rezero에서의 선택](#7-dezerorezero에서의-선택)
8. [핵심 요약](#8-핵심-요약)

---

## 1. 결론부터 — unittest 유효하지만 국룰은 pytest

| 도구 | 위치 | 현재 위상 |
|---|---|---|
| `unittest` | 표준 라이브러리 (batteries included) | 레거시 호환, 교육용. 여전히 동작 |
| **`pytest`** | 서드파티 | ★★★ 사실상 국룰 (2010년대부터 현재까지) |

- `unittest`는 **Python 2.1 (2001)** 부터 표준. deprecated 될 일 없음 → 영구 동작
- `pytest`는 **2005년 출시, 2010년대 폭발적 채택** → 현재 파이썬 실무의 사실상 표준

→ 밑시딥 3권이 가르치는 `unittest` 코드는 **여전히 유효** (동작함). 하지만 파이썬 커뮤니티의 **국룰은 pytest**로 전환됨.

---

## 2. unittest — Java JUnit 유산 (2001)

`unittest`는 **Java의 JUnit을 모방**해서 만들어졌어 (2001년, PEP 없이 조금씩 발전). JUnit 유산의 특징:

```python
import unittest

class SquareTest(unittest.TestCase):              # ★ 클래스 기반 (JUnit 스타일)

    def setUp(self):                                # 보일러플레이트
        self.x = Variable(np.array(2.0))

    def test_forward(self):
        y = square(self.x)
        self.assertEqual(y.data, np.array(4.0))     # ★ self.assertEqual (어서션 메서드)

    def test_backward(self):
        y = square(self.x)
        fill_grad(y)
        self.assertTrue(np.allclose(self.x.grad, np.array(4.0)))
```

**JUnit 유산으로 인한 특징**:
- **클래스 기반** — `class XTest(unittest.TestCase)` 상속 필수
- **어서션 메서드** — `self.assertEqual`, `self.assertTrue`, `self.assertIn` 등 (약 30종)
- **setUp/tearDown** — 픽스처 보일러플레이트 (메서드 오버라이드)
- **발견 규칙** — `test_` 접두어 + 클래스는 `Test` 접미어

→ 단점: **보일러플레이트 많음**. 간단한 테스트도 클래스 + self.assertEqual 필요.

---

## 3. pytest — 혁신적 단순화 (2005/2010대 폭발)

`pytest` (Holger Krekel 등, 2005년 출시)는 unittest의 JUnit 유산을 **혁신적으로 단순화**:

```python
# pytest 스타일 — 클래스 불필요, assert 문 직접
def test_forward():
    x = Variable(np.array(2.0))
    y = square(x)
    assert y.data == np.array(4.0)                  # ★ 그냥 assert! self.assertEqual 불필요

def test_backward():
    x = Variable(np.array(2.0))
    y = square(x)
    fill_grad(y)
    assert np.allclose(x.grad, np.array(4.0))
```

★ **핵심 차이 4가지**:

| 관점 | unittest | pytest |
|---|---|---|
| 구조 | 클래스 상속 필수 | ★ 함수만으로 OK (클래스도 가능) |
| 어서션 | `self.assertEqual(a, b)` | ★ `assert a == b` (일반 assert 문) |
| 픽스처 | setUp/tearDown 메서드 오버라이드 | ★ `@pytest.fixture` 의존성 주입 |
| 파라미터화 | 서브클래스/루프로 어색하게 | ★ `@pytest.mark.parametrize` 한 번에 |

### 픽스처 (fixture) 예시 — pytest의 강력함

```python
import pytest

@pytest.fixture
def sample_var():
    """테스트마다 새 Variable 생성 — setUp보다 유연"""
    return Variable(np.array(2.0))

def test_forward(sample_var):           # ★ fixture를 인자로 주입
    y = square(sample_var)
    assert y.data == np.array(4.0)
```

### 파라미터화 (parametrize) — 한 테스트 여러 케이스

```python
@pytest.mark.parametrize("input, expected", [
    (2.0, 4.0),
    (3.0, 9.0),
    (0.0, 0.0),
    (-1.5, 2.25),
])
def test_square_forward(input, expected):
    x = Variable(np.array(input))
    y = square(x)
    assert np.allclose(y.data, expected)
```

→ unittest로 이걸 하려면 서브클래스 4개 or 루프. pytest는 데코레이터 한 줄.

---

## 4. ★ 왜 책은 unittest를 가르치나 — 교육적 합리적 선택

브로 질문의 핵심: "책이 좀 됐으니 더 나은 게 나왔을 텐데?" → 맞음 (pytest). 근데 책이 unittest 택한 건 **합리적 선택**:

| 이유 | 설명 |
|---|---|
| **표준 라이브러리** | `uv add pytest` 없이 `python -m unittest`로 바로 실행. 책에선 의존성 설치 부담 덜기 |
| **JUnit 유산** | Java/C# 사용자에게 익숙. 국제적 교재라는 점에서 접근성 |
| **안정성** | 표준이라 deprecated 될 일 없음. 책이 10년 지나도 동작 |
| **교육적 단순함** | pytest 기능 전부를 가르치면 본질(autograd)에서 벗어남 |
| **발행 시점** | 일본 원서 2020년 — pytest가 이미 국룰이었지만, 교육용으론 unittest 관례 |

→ ★ 책의 선택은 **교육적 합리적**. 본질(autograd 학습)에 집중하게 하려고. 하지만 실무에서는 pytest가 압도적 국룰.

cf. 밑시딥 1권, 2권도 unittest 사용 — 시리즈 전체의 일관된 교육적 선택.

---

## 5. pytest 역호환 — unittest 코드를 그대로 실행

★★★ 핵심 통찰: **pytest는 unittest 코드를 그대로 실행**할 수 있어! 역호환.

```bash
# 우리 레포의 기존 unittest 코드를 pytest로 실행 가능
uv run pytest tests/                    # ★ unittest.TestCase 코드도 실행됨
uv run pytest rezero/tests/             # rezero 테스트도
```

→ 그래서 실무 전략:
- **학습 단계**: 책 따라 unittest 코드 작성 (step10)
- **실행/확장 단계**: pytest로 실행 + 점진적 pytest 스타일 전환

이게 **하이브리드 전략** — 책 호환성 + 실무 국룰 둘 다 잡기.

---

## 6. 최신 트렌드 (2024-2026) — pytest 생태계 확장

브로가 "더 나은 게 나왔다" 한 것, 실제로 pytest 생태계가 확장됨:

### 6.1 pytest 플러그인 생태계

| 플러그인 | 역할 |
|---|---|
| `pytest-xdist` | 병렬 실행 (대규모 테스트 속도 향상) |
| `pytest-cov` | 커버리지 측정 (어떤 코드가 테스트 안 됐나) |
| `pytest-randomly` | 테스트 순서 무작위화 (숨겨진 의존성 발견) |
| `pytest-mock` | `mock` 통합 |
| `pytest-asyncio` | async/await 테스트 |

### 6.2 Property-based testing — `hypothesis`

★ 가장 혁신적인 패러다임 — "내가 입력을 고르는 게 아니라, **라이브러리가 임의의 입력을 자동 생성**":

```python
from hypothesis import given, strategies as st

@given(st.floats(allow_nan=False, allow_infinity=False))   # ★ 임의의 float 자동 생성
def test_square_gradient_matches_numerical(x_val):
    """임의의 x에 대해 역전파 == 수치 미분 (gradient check 자동화)"""
    x = Variable(np.array(x_val))
    y = square(x)
    fill_grad(y)
    num_grad = numerical_diff(square, x)
    assert np.allclose(x.grad, num_grad, atol=1e-4)
```

→ unittest/pytest의 "내가 고른 입력" 테스트에서 → hypothesis의 **"수천 개 임의 입력에 대해 자동 검증"** 으로 확장. QuickCheck (Haskell)에서 유래한 패러다임.

### 6.3 AI 시대 — 테스트 자동 생성

GitHub Copilot/Claude가 **pytest 스타일 테스트 자동 생성**에 강함:
- 함수 시그니처 보고 테스트 케이스 제안
- pytest의 간결함이 AI 생성에 유리 (unittest의 self.assertEqual보다 assert가 자연스러움)

### 6.4 CI/CD 통합

GitHub Actions에서 pytest가 **사실상 표준**:
```yaml
# .github/workflows/test.yml
- run: uv run pytest --cov=dezero tests/
```

→ pytest가 CI 시대의 국룰로 굳어짐.

---

## 7. DeZero/rezero에서의 선택

이 탐구의 실천적 결론 — 우리 프로젝트에서 어떻게 할까:

### 옵션 비교

| 옵션 | 장점 | 단점 |
|---|---|---|
| **unittest만** (책 추종) | 책 호환, 표준, 의존성 없음 | 보일러플레이트, 구식 |
| **pytest만** (국룰 전환) | 간결, 현재 실무 표준, fixture 강력 | 책과 어긋남, 의존성 추가 |
| **★ 하이브리드** (unittest 코드 + pytest 실행) | 책 호환 + 실무 국룰 둘 다 | 학습 곡선 (두 패러다임) |

★ **추천: 하이브리드**. 이유:
1. step10은 책 따라 unittest 코드 작성 (학습 충실도)
2. 실행은 `uv run pytest`로 (실무 관례)
3. 점진적 pytest 스타일 도입 — step이 진행되며 복잡해지면 fixture/parametrize 활용
4. ★ hypothesis는 gradient check 자동화에 진가 — 추후 RESEARCH_QUEUE 후보

### 우리 레포 현황 점검

```bash
# 원본 dezero 테스트
uv run python -m unittest discover tests            # 현행 방식 (unittest)

# pytest가 있다면
uv run pytest tests/                                # 같은 코드를 pytest로 실행 가능 ★
```

→ 이미 unittest 코드가 있으니, `uv add pytest --dev` 한 번이면 pytest 실행 가능. 역호환의 힘.

---

## 8. 핵심 요약

1. **unittest는 여전히 유효** — 표준 라이브러리, 영구 동작. 책 코드 그대로 실행됨
2. **★ 파이썬 실무 국룰은 pytest** — 2010년대부터 현재까지. 클래스 불필요, assert 직접, fixture 강력
3. **책이 unittest 택한 건 교육적 합리적 선택** — 표준/안정성/JUnit 유산/본질 집중
4. **★ pytest는 unittest 역호환** — 기존 unittest 코드를 그대로 pytest로 실행 가능
5. **최신 트렌드** — pytest 생태계 확장 (xdist/cov/randomly), hypothesis (property-based), AI 생성, CI/CD 표준
6. **rezero 추천** — 하이브리드: unittest 코드(책 충실) + pytest 실행(실무 관례) + 점진적 pytest 스타일

★ 핵심 통찰: **책(2020년)과 파이썬 생태계(2026년)의 시대 차이**. 책은 교육용으로 unittest 선택했지만, 실무에선 pytest.
이게 [AGENTS.md "책 vs rezero+AI" 학습 철학](../AGENTS.md)의 구체적 사례 — 책의 시대 한계를 rezero+AI가 보완.

---

## 🔑 핵심 키워드

`#unittest` `#pytest` `#테스팅패러다임` `#JUnit유산` `#보일러플레이트` `#assert` `#fixture` `#parametrize` `#역호환` `#property-based-testing` `#hypothesis` `#QuickCheck` `#CI/CD` `#책시대한계` `#교육적선택` `#실무국룰` `#하이브리드전략`

---

## 🔗 관련 링크

- **출처 step**: [LEARNING_NOTES.md step10](../LEARNING_NOTES.md) — 책이 unittest 가르치는 step
- [AGENTS.md "책 vs rezero+AI" 학습 철학](../AGENTS.md) — "매체(책)의 시대 한계" 시리즈 짝
- [pytest 공식](https://docs.pytest.org/) — 현재 파이썬 테스팅 국룰
- [hypothesis 공식](https://hypothesis.readthedocs.io/) — property-based testing
- 밑시딥 1권, 2권 — 시리즈 전체 unittest 사용 (일관된 교육적 선택)
