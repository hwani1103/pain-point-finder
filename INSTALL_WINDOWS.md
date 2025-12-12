# 🪟 Windows 설치 문제 해결 가이드

## ❌ 에러 발생: pandas 설치 실패

pandas 설치 중 컴파일러 오류가 발생하는 경우 (특히 Python 3.14 사용 시)

```
ERROR: Failed to build 'pandas' when installing build dependencies
```

---

## ✅ 해결 방법 (3가지)

### 🔥 방법 1: 최신 pandas 바이너리 설치 (추천!)

미리 컴파일된 버전을 설치합니다.

```bash
# 기존 설치 시도 중단
Ctrl+C

# pip 업그레이드
python -m pip install --upgrade pip

# pandas만 먼저 최신 버전 설치
python -m pip install pandas --upgrade

# 나머지 설치
python -m pip install requests beautifulsoup4 lxml openpyxl
```

---

### 🟢 방법 2: 하나씩 설치하기

```bash
python -m pip install --upgrade pip
python -m pip install requests
python -m pip install beautifulsoup4
python -m pip install lxml
python -m pip install openpyxl
python -m pip install pandas
```

각 단계마다 오류가 나는지 확인하세요!

---

### 🟡 방법 3: pandas 없이 실행 (최후의 수단)

pandas 설치가 계속 안 되면, pandas 없이도 작동하는 버전을 사용하세요!

```bash
# pandas 제외하고 설치
python -m pip install requests beautifulsoup4 lxml openpyxl

# CSV 전용 버전 실행 (pandas 불필요)
python pain_point_crawler_no_pandas.py
```

---

## 🔧 추가 해결 방법

### A. Microsoft Visual C++ 재배포 패키지 설치

pandas가 필요로 하는 C++ 라이브러리가 없을 수 있습니다.

1. [Microsoft Visual C++ 재배포 패키지](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170) 다운로드
2. **x64** 버전 설치 (vc_redist.x64.exe)
3. 설치 후 재부팅
4. 다시 pandas 설치 시도

---

### B. conda 사용 (Anaconda/Miniconda)

conda는 미리 컴파일된 패키지를 제공합니다.

```bash
# Anaconda나 Miniconda가 설치되어 있다면
conda install pandas requests beautifulsoup4 lxml openpyxl
```

---

### C. Python 버전 낮추기

Python 3.14는 매우 최신 버전이라 일부 패키지가 지원하지 않을 수 있습니다.

**권장 버전: Python 3.10 또는 3.11**

1. [Python 3.11](https://www.python.org/downloads/) 다운로드
2. 설치 (기존 Python 유지 가능)
3. 새 Python으로 재시도:
   ```bash
   py -3.11 -m pip install -r requirements.txt
   py -3.11 pain_point_crawler_interactive.py
   ```

---

## 🎯 빠른 해결 순서

### 1단계: 이것부터 시도

```bash
python -m pip install --upgrade pip
python -m pip install pandas --upgrade --only-binary :all:
```

`--only-binary :all:` 옵션은 소스 컴파일을 건너뛰고 미리 빌드된 버전만 설치합니다.

### 2단계: 안 되면 하나씩

```bash
python -m pip install requests
python -m pip install beautifulsoup4
python -m pip install lxml
python -m pip install openpyxl
python -m pip install pandas
```

### 3단계: 그래도 안 되면

**pandas 없는 버전 사용** (아래 참조)

---

## 📝 pandas 없는 버전 만들기

pandas가 정말 설치 안 되면, CSV를 직접 쓰는 버전을 사용하세요.

`pain_point_crawler_no_pandas.py` 파일 생성 후 아래에서 제공하는 코드 사용!

---

## 💡 확인 방법

### 설치 확인

```bash
python -m pip list | findstr pandas
python -m pip list | findstr requests
python -m pip list | findstr beautifulsoup4
```

### Python 버전 확인

```bash
python --version
```

---

## 🆘 그래도 안 될 때

1. **가상환경 사용해보기**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   python -m pip install --upgrade pip
   python -m pip install pandas requests beautifulsoup4 lxml openpyxl
   ```

2. **인터넷 연결 확인**
   - 프록시나 방화벽 때문일 수 있음
   - 회사망이라면 IT 부서에 문의

3. **관리자 권한으로 실행**
   - 명령 프롬프트를 **관리자 권한**으로 실행
   - 다시 설치 시도

---

## ✅ 성공하면

```bash
# 정상 실행
python pain_point_crawler_interactive.py
```

화면에 이렇게 뜨면 성공:
```
🔍 Pain Point Finder - 대화형 버전
```

---

**문제가 계속되면 에러 메시지를 캡처해서 물어보세요!** 🙋‍♂️
