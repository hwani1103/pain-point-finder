# 💻 설치 및 실행 가이드 (python -m pip 버전)

## ⚠️ pip 명령어가 안 되는 경우

`pip` 명령어가 안 되고 `python -m pip`만 되는 경우 이 가이드를 따라하세요!

---

## 📥 1단계: 코드 받기

### 방법 1: 브랜치 전환 (이미 clone한 경우)

```bash
git checkout claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
git pull origin claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
```

### 방법 2: 새로 Clone

```bash
git clone <your-repository-url>
cd pain-point-finder
git checkout claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
```

---

## 🔧 2단계: 라이브러리 설치

Windows 명령 프롬프트 또는 PowerShell에서 실행:

```bash
python -m pip install -r requirements.txt
```

### 설치 확인

```bash
python -m pip list
```

다음 패키지들이 보이면 성공:
- requests
- beautifulsoup4
- lxml
- openpyxl
- pandas

---

## 🚀 3단계: 실행

### 방법 1: 대화형 실행 (추천!)

**직접 검색어 입력 가능**

```bash
python pain_point_crawler_interactive.py
```

실행하면 물어봐요:
```
기본 키워드 사용? (y/n): y
검색어 입력: 스마트폰 불편, 배달앱 문제
페이지 수 (Enter=2): 3
```

---

### 방법 2: 자동 실행

**미리 설정된 검색어로 바로 실행**

```bash
python pain_point_crawler.py
```

---

## 📊 4단계: 결과 확인

실행이 끝나면 다음 파일들이 생성됩니다:

```
📁 pain-point-finder/
  ├── pain_points_20241212_143052.csv          # 메인 데이터
  ├── pain_points_20241212_통계.csv             # 키워드 통계
  ├── pain_points_20241212_검색어_통계.csv       # 검색어별 통계
  └── pain_points_20241212_143052.xlsx          # 엑셀 버전
```

### CSV 파일 여는 방법

1. **메모장으로 열기**
   - 파일 우클릭 → 연결 프로그램 → 메모장

2. **Google Sheets로 열기**
   - [sheets.google.com](https://sheets.google.com) 접속
   - 파일 → 가져오기 → CSV 파일 업로드

3. **무료 프로그램**
   - LibreOffice Calc 다운로드 (무료)

---

## 🔥 전체 명령어 한눈에 보기

### 처음 설치할 때

```bash
# 1. 코드 받기
git checkout claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs
git pull origin claude/pain-point-crawler-01XFb7yECAyqsaWccUdn2Xqs

# 2. 설치
python -m pip install -r requirements.txt

# 3. 실행 (대화형)
python pain_point_crawler_interactive.py
```

### 다시 실행할 때

```bash
# 그냥 실행만 하면 됨!
python pain_point_crawler_interactive.py
```

---

## 🆘 문제 해결

### 1. ModuleNotFoundError 발생

```bash
python -m pip install -r requirements.txt
```

다시 설치해보세요.

### 2. python 명령어도 안 됨

Python이 설치되지 않았을 수 있습니다.

**Python 설치 확인:**
```bash
python --version
```

**Python 설치:**
- [python.org](https://www.python.org/downloads/) 접속
- Python 3.8 이상 다운로드
- 설치 시 **"Add Python to PATH"** 체크!

### 3. pip 버전 업그레이드 필요

```bash
python -m pip install --upgrade pip
```

### 4. 특정 패키지만 설치 안 될 때

하나씩 설치해보기:

```bash
python -m pip install requests
python -m pip install beautifulsoup4
python -m pip install lxml
python -m pip install openpyxl
python -m pip install pandas
```

### 5. SSL 인증서 오류

```bash
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### 6. 권한 오류 (Permission denied)

**Windows:**
명령 프롬프트를 **관리자 권한**으로 실행

**또는 사용자 폴더에만 설치:**
```bash
python -m pip install --user -r requirements.txt
```

---

## 💡 추가 팁

### 가상환경 사용하기 (선택사항)

프로젝트별로 독립된 환경을 만들고 싶다면:

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source venv/bin/activate

# 이후 설치
python -m pip install -r requirements.txt
```

### 설치된 패키지 확인

```bash
python -m pip list
```

### 특정 패키지 제거

```bash
python -m pip uninstall pandas
```

---

## ✅ 체크리스트

설치 전:
- [ ] Python 3.8 이상 설치됨
- [ ] Git으로 코드 받음
- [ ] 올바른 브랜치에 있음

설치 후:
- [ ] `python -m pip install -r requirements.txt` 실행 완료
- [ ] `python -m pip list`에서 패키지 확인됨
- [ ] `python pain_point_crawler_interactive.py` 실행됨

결과 확인:
- [ ] CSV 파일 생성됨
- [ ] 파일이 정상적으로 열림

---

**문제가 계속되면?**

1. Python 재설치 (PATH 설정 확인)
2. 명령 프롬프트 재시작
3. 컴퓨터 재부팅

그래도 안 되면 에러 메시지를 복사해서 물어보세요! 🙋‍♂️
