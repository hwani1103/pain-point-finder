# 🚀 빠른 시작 가이드

## 📥 코드 받기

### 방법 1: 작업한 브랜치로 이동
```bash
# 현재 브랜치 확인
git branch

# 작업한 브랜치로 전환
git checkout claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs

# 최신 코드 받기
git pull origin claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
```

### 방법 2: 새로 Clone
```bash
git clone <repository-url>
cd pain-point-finder
git checkout claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
```

## 🔧 설치

```bash
pip install -r requirements.txt
```

## ▶️ 실행 방법

### 1️⃣ 자동 실행 (추천 - 처음 사용자용)
미리 설정된 검색어로 바로 실행됩니다.

```bash
python pain_point_crawler.py
```

**특징:**
- 검색어: 일상 불편함, 생활 불편, 앱 사용 불편
- 페이지: 각 2페이지
- 결과: CSV + Excel 자동 저장

---

### 2️⃣ 대화형 실행 (추천 - 직접 입력하고 싶은 경우)
단계별로 입력하면서 실행합니다.

```bash
python pain_point_crawler_interactive.py
```

**입력 내용:**
1. **키워드 설정**: 기본 키워드 사용 or 직접 입력
2. **검색어 입력**: 원하는 검색어 입력 (쉼표로 구분)
3. **페이지 수**: 검색할 페이지 수
4. **저장 여부**: 결과를 파일로 저장할지

**예시:**
```
기본 키워드 사용? (y/n): y
검색어 입력: 스마트폰 불편, 인터넷 뱅킹 어려움, 배달앱 문제
페이지 수: 3
결과를 저장하시겠습니까? (y/n): y
```

---

### 3️⃣ 코드로 직접 사용 (고급 사용자용)

새 파일 `my_crawler.py` 생성:

```python
from pain_point_crawler import PainPointCrawler

# 크롤러 생성
crawler = PainPointCrawler()

# 내가 원하는 키워드로 검색
crawler.search_naver_blog('택배 불편', max_pages=3)
crawler.search_naver_blog('온라인 쇼핑 어려움', max_pages=5)

# 통계 확인
crawler.show_statistics()

# 저장
crawler.save_to_csv('my_results.csv')
```

실행:
```bash
python my_crawler.py
```

## 📊 결과 확인

### CSV 파일 열기
- **메모장**: 우클릭 → 연결 프로그램 → 메모장
- **엑셀**: 더블클릭 (설치된 경우)
- **Google Sheets**: [sheets.google.com](https://sheets.google.com) → 파일 업로드
- **무료 프로그램**: LibreOffice Calc

### 생성되는 파일
```
pain_points_20241212_143052.csv          # 메인 데이터
pain_points_20241212_143052_통계.csv      # 키워드 빈도수
pain_points_20241212_143052_검색어_통계.csv # 검색어별 통계
pain_points_20241212_143052.xlsx          # 엑셀 (위 3개 모두 포함)
```

## ⚙️ 설정 변경

### 검색어 변경 (자동 실행 버전)

`pain_point_crawler.py` 열기 → 295줄 근처:

```python
search_queries = [
    '일상 불편함',
    '생활 불편',
    # 원하는 검색어 추가
    '스마트폰 배터리',
    '교통 불편'
]
```

### 페이지 수 변경

307줄 근처:
```python
crawler.search_naver_blog(query, max_pages=5)  # 2 → 5로 변경
```

### Pain Point 키워드 추가

23줄 근처:
```python
PAIN_POINT_KEYWORDS = [
    '불편해', '불편하다', '불편한',
    # ... 기존 키워드들 ...
    '짜증나',  # 새로운 키워드 추가
    '귀찮아'
]
```

## 🆘 문제 해결

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### 결과가 없어요
- 더 일반적인 검색어 사용
- 페이지 수 늘리기
- Pain Point 키워드 추가

### 한글이 깨져요 (CSV)
- UTF-8 인코딩 지원하는 프로그램 사용
- Google Sheets 추천
- 또는 Excel로 열기

## 💡 활용 팁

### 1. 특정 분야 집중 조사
```python
# 예: 육아 관련 pain point
search_queries = [
    '육아 힘들어',
    '아이 키우기 불편',
    '유아용품 불편함'
]
```

### 2. 제품별 조사
```python
search_queries = [
    '스마트워치 불편',
    '무선이어폰 문제',
    '전기차 충전 어려움'
]
```

### 3. 서비스별 조사
```python
search_queries = [
    '배달앱 사용 어려움',
    '은행앱 불편',
    '공공 서비스 개선'
]
```

---

**Happy Pain Point Hunting! 🎯**

문제가 있으면 issue를 남겨주세요!
