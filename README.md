# 🔍 Pain Point Finder

네이버 블로그에서 사람들의 불편함과 문제점을 자동으로 발굴하는 크롤링 도구

## 📌 주요 기능

1. **네이버 블로그 검색 크롤링**
   - 여러 검색어로 자동 검색
   - 다중 페이지 크롤링 지원

2. **Pain Point 자동 감지**
   - 20개 이상의 키워드 패턴 자동 탐지
   - "불편해", "어려워", "없나요", "개선됐으면" 등

3. **엑셀 결과 저장**
   - 날짜, 제목, 본문 일부, 링크, 매칭 키워드 포함
   - 자동 타임스탬프 파일명

4. **통계 분석**
   - 키워드별 빈도수 통계
   - 검색어별 발견 개수
   - 자동 통계 시트 생성

## 🚀 빠른 시작

### 1. Python 설치 확인

Windows PowerShell 또는 명령 프롬프트에서:

```bash
python --version
```

Python 3.8 이상이 필요합니다. 설치되어 있지 않다면 [python.org](https://www.python.org/downloads/)에서 다운로드하세요.

### 2. 의존성 설치

프로젝트 폴더에서 다음 명령어 실행:

```bash
pip install -r requirements.txt
```

### 3. 실행

```bash
python pain_point_crawler.py
```

## 📖 사용 방법

### 기본 실행

프로그램을 실행하면 기본 검색어로 자동 크롤링이 시작됩니다:

```bash
python pain_point_crawler.py
```

### 검색어 커스터마이징

`pain_point_crawler.py` 파일을 열고 `main()` 함수의 `search_queries` 리스트를 수정하세요:

```python
search_queries = [
    '일상 불편함',
    '생활 불편',
    '앱 사용 불편',
    # 원하는 검색어 추가
    '스마트폰 불편',
    '집안일 힘들어'
]
```

### 페이지 수 조절

더 많은 결과를 원하면 `max_pages` 값을 조정하세요:

```python
crawler.search_naver_blog(query, max_pages=5)  # 기본값은 2
```

## 📊 출력 파일 구조

### 저장되는 파일들

프로그램 실행 후 다음 파일들이 생성됩니다:

1. **pain_points_YYYYMMDD_HHMMSS.csv** - 메인 결과 (CSV)
2. **pain_points_YYYYMMDD_통계.csv** - 키워드 통계 (CSV)
3. **pain_points_YYYYMMDD_검색어_통계.csv** - 검색어별 통계 (CSV)
4. **pain_points_YYYYMMDD_HHMMSS.xlsx** - 엑셀 버전 (모든 데이터 포함)

### CSV 파일 열기

- **Windows**: 메모장, Excel(설치된 경우), Google Sheets
- **온라인**: [Google Sheets](https://sheets.google.com)에 업로드
- **무료 프로그램**: LibreOffice Calc

### Pain Points 데이터
| 날짜 | 제목 | 본문_일부 | 링크 | 매칭_키워드 | 키워드_개수 | 검색어 |
|------|------|-----------|------|-------------|-------------|--------|
| 2024.12.12 | ... | ... | ... | 불편해, 개선 | 2 | 일상 불편함 |

### 키워드_통계
| 키워드 | 빈도수 |
|--------|--------|
| 불편해 | 15 |
| 어려워 | 12 |
| ... | ... |

### 검색어_통계
| 검색어 | 발견_개수 |
|--------|-----------|
| 일상 불편함 | 25 |
| ... | ... |

## 🎯 Pain Point 키워드 목록

현재 감지하는 키워드들:

```
불편해, 불편하다, 불편한
어려워, 어렵다, 어려운
없나요, 없을까, 없네
왜 이런 게 없지, 왜 없
개선됐으면, 개선되면, 개선이 필요
힘들어, 힘들다, 힘든
짜증, 화나
답답해, 답답하다, 답답한
불만, 문제가, 문제점
고치면, 고쳐, 바꿔
왜 이래, 왜 이렇게
불편, 개선, 해결
```

### 키워드 추가하기

`pain_point_crawler.py` 파일의 `PAIN_POINT_KEYWORDS` 리스트에 원하는 키워드를 추가하세요:

```python
PAIN_POINT_KEYWORDS = [
    '불편해', '불편하다', '불편한',
    # ... 기존 키워드들 ...
    '이것도 추가',  # 새로운 키워드
    '저것도 추가'
]
```

## ⚙️ 고급 사용법

### 프로그래밍 방식으로 사용

```python
from pain_point_crawler import PainPointCrawler

# 크롤러 생성
crawler = PainPointCrawler()

# 특정 키워드로 검색
crawler.search_naver_blog('내가 원하는 검색어', max_pages=3)

# 통계 확인
crawler.show_statistics()

# 결과 저장
crawler.save_to_excel('my_results.xlsx')
```

### 결과 데이터 직접 활용

```python
# 결과 데이터 접근
for result in crawler.results:
    print(result['제목'])
    print(result['매칭_키워드'])
```

## 🛠️ 문제 해결

### 크롤링이 너무 느려요
- `max_pages` 값을 줄이세요 (기본값: 2)
- `time.sleep(1)` 값을 줄이세요 (단, 너무 빠르면 차단될 수 있음)

### 결과가 없어요
- 검색어를 더 일반적인 것으로 변경해보세요
- Pain Point 키워드를 더 추가해보세요

### 연결 오류가 발생해요
- 인터넷 연결을 확인하세요
- 방화벽 설정을 확인하세요
- VPN을 사용 중이라면 비활성화해보세요

## 📝 주의사항

1. **윤리적 크롤링**
   - 네이버 서버에 과도한 부하를 주지 않도록 적절한 딜레이를 유지합니다
   - 개인정보가 포함된 데이터는 수집하지 않습니다

2. **법적 고지**
   - 이 도구는 교육 및 개인 연구 목적으로만 사용하세요
   - 상업적 이용 시 네이버의 이용약관을 확인하세요

3. **데이터 정확성**
   - 크롤링된 데이터는 참고용이며, 항상 원본을 확인하세요
   - 네이버 페이지 구조 변경 시 크롤링이 작동하지 않을 수 있습니다

## 🔧 향후 개선 계획

- [ ] 네이버 카페 크롤링 추가
- [ ] 감정 분석 기능 추가
- [ ] GUI 인터페이스 개발
- [ ] 실시간 모니터링 기능
- [ ] 더 다양한 출력 형식 지원 (CSV, JSON)

## 📄 라이선스

MIT License

## 👨‍💻 기여

이슈와 풀 리퀘스트는 언제나 환영합니다!

---

**Happy Pain Point Hunting! 🎯**
