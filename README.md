# Nikuman Dict (肉まん辞書) 🥟

일본어-한국어 및 한자 검색을 지원하는 빠르고 가벼운 모바일 최적화 웹 사전입니다. FastAPI와 SQLite를 활용하여 오프라인 데이터베이스를 효율적으로 검색합니다.

## ✨ 주요 기능

*   **빠른 검색**: SQLite 데이터베이스를 통한 즉각적인 검색 결과 제공.
*   **두 가지 사전 모드**: 일한사전(기본) 및 한자사전 탭 지원.
*   **다크 모드 지원**: 사용자 기기 설정 및 수동 전환 버튼을 통한 완벽한 다크 모드(Dark Mode) 지원.
*   **모바일 최적화**: 스마트폰 환경에 맞춘 깔끔한 UI와 터치 친화적 디자인.
*   **URL 공유**: 검색어와 사전 설정 상태를 URL(`/?q=단어&dict=jako`)로 복사하여 다른 사람과 쉽게 공유 가능.

## 🛠 기술 스택

*   **Frontend**: HTML5, Vanilla CSS, Vanilla JavaScript
*   **Backend**: Python, FastAPI, Uvicorn (서버)
*   **Database**: SQLite (`.sqlite` 파일 활용)
*   **Deployment**: Koyeb 지원 가능 (`Procfile` 포함)

## 📦 설치 및 로컬 실행 방법

1. **저장소 클론 및 폴더 이동**
   ```bash
   git clone https://github.com/사용자아이디/nikuman-dictionary.git
   cd nikuman-dictionary
   ```

2. **의존성 설치**
   Python 환경(3.8 이상 권장)에서 필요한 패키지를 설치합니다.
   ```bash
   pip install -r requirements.txt
   ```

3. **(필수) 데이터베이스 / 폰트 추가**
   저작권 문제 등으로 데이터베이스 파일은 저장소에 없을 수 있습니다.
   다음 위치에 DB와 폰트 파일을 알맞게 배치해야 합니다.
   *   `resources/sqlite/Ja-Ko_DIC_2018.sqlite`
   *   `resources/sqlite/Hanja-Ko_DIC_2018.sqlite`
   *   `resources/fonts/` 폴더 내 폰트 파일들 (Pretendard 등)

4. **서버 실행**
   ```bash
   python main.py
   # 또는 uvicorn으로 직접 실행:
   # uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **브라우저 접속**
   `http://localhost:8000` 에 접속하여 사전을 사용합니다.

## 🚀 배포 가이드 (Koyeb 무료 배포)

이 프로젝트는 Koyeb(또는 Render)과 같은 호스팅 서비스에 연동하여 쉽게 무료 배포가 가능합니다.

1. GitHub에 이 저장소를 Push합니다.
2. [Koyeb](https://www.koyeb.com/)에서 `Create Web Service`를 선택하고 이 GitHub 저장소를 연동합니다.
3. 배포 타입에 **Buildpack**을 선택합니다.
4. 요금제에서 **Eco Free** 인스턴스를 선택한 후 Deploy를 누릅니다. (`Procfile`에 의해 자동으로 앱이 실행됩니다.)
