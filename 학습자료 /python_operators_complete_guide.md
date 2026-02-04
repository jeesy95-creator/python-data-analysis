# Python 특수 연산자 완벽 가이드

## 📚 목차
1. [산술 연산자](#1-산술-연산자)
2. [비교 연산자](#2-비교-연산자)
3. [논리 연산자](#3-논리-연산자)
4. [비트 연산자](#4-비트-연산자)
5. [할당 연산자](#5-할당-연산자)
6. [멤버십 연산자](#6-멤버십-연산자)
7. [신원 연산자](#7-신원-연산자)
8. [Walrus 연산자 (Python 3.8+)](#8-walrus-연산자-python-38)
9. [기타 특수 연산자](#9-기타-특수-연산자)

---

## 1. 산술 연산자

### 기본 산술
```python
# 덧셈
result = 5 + 3        # 8

# 뺄셈
result = 5 - 3        # 2

# 곱셈
result = 5 * 3        # 15

# 나눗셈 (float)
result = 5 / 3        # 1.6666...

# 몫 (정수 나눗셈) ⭐
result = 5 // 3       # 1
result = 7 // 2       # 3

# 나머지 (modulo) ⭐
result = 5 % 3        # 2
result = 10 % 3       # 1

# 거듭제곱 ⭐
result = 2 ** 3       # 8 (2의 3승)
result = 5 ** 2       # 25
```

**실전 활용:**
```python
# 짝수/홀수 판별
if number % 2 == 0:  # ⭐
    print("짝수")

# 페이지네이션
page_count = total_items // items_per_page  # ⭐
if total_items % items_per_page > 0:
    page_count += 1

# 거듭제곱 (로그 역연산)
original = 10 ** np.log10(value)  # ⭐
```

---

## 2. 비교 연산자

```python
# 같음
5 == 5        # True
'a' == 'a'    # True

# 같지 않음 ⭐
5 != 3        # True
df[df['age'] != 30]  # MCLP에서 자주 사용

# 크다
5 > 3         # True

# 작다
5 < 3         # False

# 크거나 같다 ⭐
age >= 18     # 성인 여부
df[df['score'] >= 80]  # 점수 80 이상

# 작거나 같다 ⭐
threshold <= 200  # 임계값 체크
df[df['distance'] <= threshold]  # MCLP 커버리지
```

**실전 활용:**
```python
# MCLP: 거리 기준 필터링
covered = od[
    (od['i_state'] == hub) & 
    (od['dist'] <= threshold)  # ⭐
]['j_state']

# 복원력 점수 필터링
high_resilience = rank_df[
    rank_df['resilience_score'] >= 0.5  # ⭐
]
```

---

## 3. 논리 연산자 (Boolean)

### Python 기본
```python
# and (그리고)
True and True    # True
True and False   # False

# or (또는)
True or False    # True
False or False   # False

# not (부정)
not True         # False
not False        # True
```

### Pandas/NumPy 용 ⭐⭐⭐⭐⭐
```python
# & (AND) - 반드시 괄호 필요!
df[(df['age'] > 30) & (df['city'] == 'Seoul')]  # ⭐

# | (OR)
df[(df['age'] > 30) | (df['verified'] == True)]  # ⭐

# ~ (NOT)
df[~(df['status'] == 'deleted')]  # ⭐
df[~df['city'].isin(['Seoul', 'Busan'])]  # ⭐⭐

# ^ (XOR - 배타적 OR)
df[(df['a'] == True) ^ (df['b'] == True)]  # 둘 중 하나만
```

**중요: Python vs Pandas 차이**
```python
# ❌ Pandas에서 이렇게 하면 에러!
df[df['age'] > 30 and df['city'] == 'Seoul']  # 에러!

# ✅ Pandas에서는 & 사용
df[(df['age'] > 30) & (df['city'] == 'Seoul')]  # ⭐

# ❌ Pandas에서 not 사용 불가
df[not df['deleted']]  # 에러!

# ✅ Pandas에서는 ~ 사용
df[~df['deleted']]  # ⭐
```

**실전 활용:**
```python
# MCLP: 복합 조건
selected = df[
    (df['resilience_score'] > 0.5) &  # ⭐
    (df['demand'] > 1000) &
    ~df['state_id'].isin(excluded)    # ⭐
]

# 두 기간 모두 데이터 있는 경우
valid = df[
    df['pre_value'].notna() &   # ⭐
    df['post_value'].notna()
]
```

---

## 4. 비트 연산자 (덜 자주 사용)

```python
# & (AND)
5 & 3         # 1 (0b101 & 0b011 = 0b001)

# | (OR)
5 | 3         # 7 (0b101 | 0b011 = 0b111)

# ^ (XOR)
5 ^ 3         # 6 (0b101 ^ 0b011 = 0b110)

# ~ (NOT) - 2의 보수
~5            # -6

# << (왼쪽 시프트)
5 << 1        # 10 (5 * 2)

# >> (오른쪽 시프트)
5 >> 1        # 2 (5 // 2)
```

**실전 활용 (드묾):**
```python
# 플래그 관리
PERMISSION_READ = 1 << 0    # 0b001 = 1
PERMISSION_WRITE = 1 << 1   # 0b010 = 2
PERMISSION_EXEC = 1 << 2    # 0b100 = 4

user_permissions = PERMISSION_READ | PERMISSION_WRITE  # 3

# 권한 확인
can_read = user_permissions & PERMISSION_READ  # True
```

---

## 5. 할당 연산자 ⭐⭐⭐⭐⭐

### 기본 할당
```python
x = 5         # 할당
```

### 복합 할당 (매우 자주 사용!)
```python
# 더하기 후 할당 ⭐⭐⭐⭐⭐
count += 1           # count = count + 1
total += value       # 누적 합계

# 빼기 후 할당
remaining -= used    # remaining = remaining - used

# 곱하기 후 할당
score *= 2           # score = score * 2

# 나누기 후 할당
average /= count     # average = average / count

# 몫 할당
page //= 2

# 나머지 할당
value %= 10

# 거듭제곱 할당
base **= 2

# 비트 연산 할당
flags &= mask
flags |= new_flag
```

**실전 활용:**
```python
# MCLP: 커버리지 업데이트
covered_count = 0
for hub in selected_hubs:
    covered_count += len(coverage_sets[hub])  # ⭐

# 값 누적
total_value = 0
for state in covered:
    total_value += demand_map[state]  # ⭐

# 카운터
iteration = 0
for _ in range(max_iter):
    iteration += 1  # ⭐
    if converged:
        break
```

---

## 6. 멤버십 연산자 ⭐⭐⭐⭐⭐

### in / not in
```python
# in (포함되어 있는지) ⭐⭐⭐⭐⭐
'a' in 'apple'           # True
5 in [1, 2, 3, 4, 5]     # True
'Seoul' in cities        # True

# not in (포함되지 않았는지) ⭐⭐⭐⭐
6 not in [1, 2, 3, 4, 5]  # True
'key' not in dictionary   # False
```

**실전 활용 (MCLP):**
```python
# 이미 선택된 허브인지 확인
if candidate in selected_hubs:  # ⭐⭐⭐⭐⭐
    continue

# 이미 커버된 지역인지 확인
if state in covered_states:  # ⭐⭐⭐⭐⭐
    continue

# 딕셔너리 키 존재 확인
if key in distance_dict:  # ⭐⭐⭐⭐⭐
    distance = distance_dict[key]

# 리스트에서 찾기
if hub_id not in excluded_hubs:  # ⭐⭐⭐⭐
    candidates.append(hub_id)
```

**Pandas에서:**
```python
# isin() 메서드 ⭐⭐⭐⭐⭐
df[df['city'].isin(['Seoul', 'Busan'])]

# ~isin() 제외 ⭐⭐⭐⭐⭐
df[~df['city'].isin(['Seoul', 'Busan'])]

# Series.isin()
selected_mask = states.isin(selected_hubs)
```

---

## 7. 신원 연산자 (Identity)

### is / is not
```python
# is (같은 객체인지) ⭐⭐⭐
x = None
x is None        # True ⭐⭐⭐
x is not None    # False

# 객체 동일성 vs 값 동일성
a = [1, 2, 3]
b = [1, 2, 3]
c = a

a == b           # True (값이 같음)
a is b           # False (다른 객체)
a is c           # True (같은 객체)

# id() 확인
id(a)            # 메모리 주소
id(b)            # 다른 주소
id(c)            # a와 같은 주소
```

**중요한 차이:**
```python
# ❌ None 체크 잘못된 방법
if x == None:    # 동작하지만 권장 안 함

# ✅ None 체크 올바른 방법
if x is None:    # ⭐⭐⭐ 권장!

# ❌ Boolean 체크 잘못된 방법
if flag is True:  # 비추천

# ✅ Boolean 체크 올바른 방법
if flag:         # ⭐ 권장!
```

**실전 활용:**
```python
# None 체크 (가장 흔한 사용)
if result is None:  # ⭐⭐⭐⭐⭐
    print("결과 없음")

if best_hub is not None:  # ⭐⭐⭐⭐⭐
    selected_hubs.append(best_hub)

# 함수 기본값
def function(param=None):
    if param is None:  # ⭐⭐⭐⭐⭐
        param = []
```

---

## 8. Walrus 연산자 (Python 3.8+) ⭐⭐⭐

### := (할당 표현식)
```python
# 기존 방식
value = expensive_function()
if value > 10:
    print(value)

# Walrus 연산자 ⭐
if (value := expensive_function()) > 10:
    print(value)

# 리스트 컴프리헨션에서
data = [1, 2, 3, 4, 5]
[y for x in data if (y := x * 2) > 5]  # ⭐
# [6, 8, 10]
```

**실전 활용:**
```python
# while 루프에서 파일 읽기
while (line := file.readline()):  # ⭐
    process(line)

# 정규표현식 매칭
if (match := re.search(pattern, text)):  # ⭐
    print(match.group(1))

# 리스트 필터링
[item for item in data 
 if (processed := process(item)) is not None  # ⭐
 and len(processed) > 10]
```

---

## 9. 기타 특수 연산자

### 9.1 삼항 연산자 (Ternary) ⭐⭐⭐⭐⭐
```python
# 형식: value_if_true if condition else value_if_false
result = "성인" if age >= 18 else "미성년자"  # ⭐

# 여러 줄
status = (
    "높음" if score > 80 
    else "중간" if score > 50 
    else "낮음"
)
```

**실전 활용:**
```python
# MCLP: 기본값 설정
threshold = user_input if user_input else 200  # ⭐

# 안전한 나눗셈
ratio = a / b if b != 0 else 0  # ⭐

# 문자열 포매팅
message = f"선택됨: {count}개" if count > 0 else "선택 없음"  # ⭐

# Pandas apply
df['category'] = df['score'].apply(
    lambda x: '상' if x >= 80 else '중' if x >= 50 else '하'  # ⭐
)
```

### 9.2 ** (언패킹 연산자) ⭐⭐⭐⭐

#### 리스트/튜플 언패킹 (*)
```python
# 함수 인자 언패킹
numbers = [1, 2, 3]
print(*numbers)      # print(1, 2, 3)과 동일

# 리스트 합치기
list1 = [1, 2, 3]
list2 = [4, 5, 6]
combined = [*list1, *list2]  # [1, 2, 3, 4, 5, 6] ⭐

# 함수 가변 인자
def sum_all(*args):  # ⭐
    return sum(args)

sum_all(1, 2, 3, 4, 5)  # 15
```

#### 딕셔너리 언패킹 (**)
```python
# 딕셔너리 합치기
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
combined = {**dict1, **dict2}  # ⭐
# {'a': 1, 'b': 2, 'c': 3, 'd': 4}

# 함수 키워드 인자
def function(**kwargs):  # ⭐
    for key, value in kwargs.items():
        print(f"{key}: {value}")

function(name="Alice", age=30)

# 기본값 + 업데이트
default_config = {'threshold': 200, 'p': 8}
user_config = {'threshold': 150}
config = {**default_config, **user_config}  # ⭐
# {'threshold': 150, 'p': 8}
```

**실전 활용:**
```python
# MCLP: 여러 시나리오 실행
thresholds = [50, 100, 200, 300, 400]
ps = [5, 8, 10]

# 모든 조합 실행
for threshold in thresholds:
    for p in ps:
        run_mclp(threshold=threshold, p=p, **common_params)  # ⭐

# 설정 병합
default_settings = {
    'alpha': 0.8,
    'post_years': [2022, 2023, 2024]
}
user_settings = {'alpha': 0.6}
final_settings = {**default_settings, **user_settings}  # ⭐
```

### 9.3 @ (행렬 곱셈 연산자) - NumPy ⭐⭐
```python
import numpy as np

# 행렬 곱셈
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# @ 연산자 (Python 3.5+)
C = A @ B  # ⭐
# [[19 22]
#  [43 50]]

# 이전 방식
C = np.matmul(A, B)
C = np.dot(A, B)
```

### 9.4 // (경로 연산자) - pathlib ⭐⭐⭐
```python
from pathlib import Path

# 경로 연결
base = Path('/home')
user = 'claude'
data = 'data.csv'

full_path = base / user / data  # ⭐
# /home/claude/data.csv

# 실전
data_dir = Path(__file__).parent / 'data'  # ⭐
csv_file = data_dir / 'logistics.csv'
```

---

## 🎯 연산자 우선순위 (중요!)

```python
# 우선순위 (높음 → 낮음)
1. **                    # 거듭제곱
2. ~ + -                 # 비트 NOT, 단항 +/-
3. * / // %              # 곱셈, 나눗셈
4. + -                   # 덧셈, 뺄셈
5. << >>                 # 비트 시프트
6. &                     # 비트 AND
7. ^                     # 비트 XOR
8. |                     # 비트 OR
9. == != > < >= <=       # 비교
10. is, is not           # 신원
11. in, not in           # 멤버십
12. not                  # 논리 NOT
13. and                  # 논리 AND
14. or                   # 논리 OR
15. = += -= etc.         # 할당
```

**실전 예제:**
```python
# ❌ 잘못된 예 (우선순위 문제)
result = 2 + 3 * 4       # 14 (3*4가 먼저)

# ✅ 명확하게
result = 2 + (3 * 4)     # 14
result = (2 + 3) * 4     # 20

# Pandas에서 매우 중요!
# ❌ 에러!
df[~df['age'] > 30]      # ~ 우선순위가 > 보다 높음!

# ✅ 괄호 필수!
df[~(df['age'] > 30)]    # ⭐⭐⭐⭐⭐
```

---

## 📊 MCLP 분석에서 가장 많이 쓰인 연산자 Top 10

| 순위 | 연산자 | 용도 | 빈도 |
|------|--------|------|------|
| 1 | `==` | 조건 비교 | ⭐⭐⭐⭐⭐ |
| 2 | `&` | AND 조건 | ⭐⭐⭐⭐⭐ |
| 3 | `~` | NOT / 제외 | ⭐⭐⭐⭐⭐ |
| 4 | `in` | 멤버십 체크 | ⭐⭐⭐⭐⭐ |
| 5 | `+=` | 누적 합계 | ⭐⭐⭐⭐⭐ |
| 6 | `<=` `>=` | 임계값 비교 | ⭐⭐⭐⭐⭐ |
| 7 | `|` | OR 조건 | ⭐⭐⭐⭐ |
| 8 | `is None` | None 체크 | ⭐⭐⭐⭐ |
| 9 | `//` | 정수 나눗셈 | ⭐⭐⭐ |
| 10 | `**` | 거듭제곱/언패킹 | ⭐⭐⭐ |

---

## 💡 핵심 팁

### Tip 1: Pandas 논리 연산 ⭐⭐⭐⭐⭐
```python
# ✅ DO (Pandas)
df[(df['a'] > 5) & (df['b'] < 10)]  # &
df[(df['a'] > 5) | (df['b'] < 10)]  # |
df[~(df['a'] > 5)]                  # ~

# ❌ DON'T (에러!)
df[df['a'] > 5 and df['b'] < 10]   # and (X)
df[not df['deleted']]               # not (X)
```

### Tip 2: None 체크 ⭐⭐⭐⭐⭐
```python
# ✅ 권장
if x is None:        # is
if x is not None:    # is not

# ❌ 비권장
if x == None:        # ==
if x != None:        # !=
```

### Tip 3: 괄호 사용 ⭐⭐⭐⭐⭐
```python
# 복잡한 조건은 항상 괄호!
df[
    ((df['score'] > 80) & (df['verified'] == True)) |  # ⭐
    ((df['vip'] == True) & ~df['banned'])
]
```

### Tip 4: 가독성 우선
```python
# 명확하지 않으면 풀어쓰기
# ❌ 복잡함
x = a if b else c if d else e

# ✅ 명확함
if b:
    x = a
elif d:
    x = c
else:
    x = e
```

---

## 🎓 연습 문제

### 문제 1: 연산자 선택
```python
df = pd.DataFrame({
    'age': [25, 30, 35, 40],
    'city': ['Seoul', 'Busan', 'Seoul', 'Incheon'],
    'verified': [True, False, True, False]
})

# TODO: 30세 이상이고 검증된 사람 (어떤 연산자?)
# TODO: 서울이 아닌 사람 (어떤 연산자?)
# TODO: None이 아닌 값 (어떤 연산자?)
```

<details>
<summary>정답</summary>

```python
# 1. AND 조건
result1 = df[(df['age'] >= 30) & (df['verified'] == True)]  # &

# 2. NOT 조건
result2 = df[~(df['city'] == 'Seoul')]  # ~
# 또는
result2 = df[df['city'] != 'Seoul']     # !=

# 3. None 체크
result3 = df[df['age'].notnull()]       # notnull()
# 또는
result3 = df[~df['age'].isnull()]       # ~
```
</details>

---

## 📚 요약표

| 카테고리 | 연산자 | 설명 | 빈도 |
|---------|--------|------|------|
| **산술** | `+` `-` `*` `/` | 기본 연산 | ⭐⭐⭐⭐⭐ |
| | `//` `%` `**` | 몫, 나머지, 제곱 | ⭐⭐⭐⭐ |
| **비교** | `==` `!=` | 같음/다름 | ⭐⭐⭐⭐⭐ |
| | `>` `<` `>=` `<=` | 대소 비교 | ⭐⭐⭐⭐⭐ |
| **논리** | `&` `|` `~` | AND/OR/NOT (Pandas) | ⭐⭐⭐⭐⭐ |
| | `and` `or` `not` | AND/OR/NOT (Python) | ⭐⭐⭐⭐ |
| **할당** | `=` `+=` `-=` | 할당/누적 | ⭐⭐⭐⭐⭐ |
| **멤버십** | `in` `not in` | 포함 여부 | ⭐⭐⭐⭐⭐ |
| **신원** | `is` `is not` | 동일 객체 | ⭐⭐⭐⭐ |
| **언패킹** | `*` `**` | 리스트/딕셔너리 | ⭐⭐⭐ |
| **Walrus** | `:=` | 할당 표현식 | ⭐⭐ |

---

**핵심 기억사항:**
1. ⭐ Pandas는 `&` `|` `~` 사용 (괄호 필수!)
2. ⭐ None 체크는 `is None`
3. ⭐ `in`과 `~isin()`은 최고의 조합
4. ⭐ 복잡하면 괄호로 명확하게!

🚀 **연산자 마스터 = Python 마스터!**
