# ssinema

**국내외 영화 평점 차이로 인해 영화 선택에 망설이는 사용자에게 객관적인 비교 정보와 풍부한 영화 데이터를 제공하여, 더 나은 영화 선택 경험을 제공하고 정보 접근의 장벽을 낮추는 것을 목표로 하는 서비스입니다.**

---
---

# 프로젝트 문서

https://www.notion.so/1fdb0d8f7a7f81e2bac0f85982cadadd

## 목차

* [프로젝트 소개](#프로젝트-소개)
    * [핵심 가치](#핵심-가치)
    * [주요 기능 상세](#주요-기능-상세)
* [기술 스택](#기술-스택)
* [프로젝트 구조](#프로젝트-구조)
    * [프론트엔드 (Vue.js)](#프론트엔드-vuejs)
    * [백엔드 (Django - DDD)](#백엔드-django---ddd)
* [설치](#설치)
    * [사전 준비 사항](#사전-준비-사항)
    * [소스 코드 가져오기](#소스-코드-가져오기)
    * [의존성 설치 및 환경 설정](#의존성-설치-및-환경-설정)
* [실행](#실행)
* [시작하기](#시작하기)
* [리소스](#리소스)
* [소통 창구](#소통-창구)
* [라이선스](#라이선스)
* [팀](#팀-선택-사항)

---

## 프로젝트 소개

**[프로젝트 이름]** 은 영화 선택의 어려움을 겪는 이용자를 위한 서비스입니다. 국내외 다양한 출처의 영화 평점을 한눈에 비교하고, 심도 있는 영화 정보와 사용자 커뮤니티 기능을 제공합니다.

### 특징

* **객관적인 정보 제공**: 국내 평점과 해외 평점(예: IMDb, watcha 등)을 비교하여 제공합니다.

* **풍부한 콘텐츠**: 영화의 기본 정보 외에도 심층 리뷰, 트레일러, OTT 시청 가능 정보 등 다양한 콘텐츠를 통합 제공합니다.
* **커뮤니티 활성화**: 사용자들이 영화에 대한 생각과 평가를 자유롭게 공유하고 소통할 수 있는 댓글 기능을 제공합니다.

### 주요 기능 상세

본 프로젝트는 다음과 같은 주요 기능을 제공합니다:

1.  **통합 영화 정보 제공**
    * 다양한 영화(최신작, 인기작, 고전 등)에 대한 기본 정보(줄거리, 감독, 출연진, 장르, 개봉일, 상영 시간 등)를 제공합니다.
    * 고화질 포스터, 스틸컷, 트레일러 등 시각적 자료를 통해 영화에 대한 이해를 돕습니다.
    * 국내 주요 평점 사이트와 해외 유명 평점 사이트(예: IMDb, watcha 등)의 평점을 수집하여 비교 표시함으로써, 사용자가 보다 객관적으로 영화를 판단할 수 있도록 지원합니다.
    * 어떤 OTT 플랫폼에서 해당 영화를 시청할 수 있는지 최신 정보를 제공합니다.

2.  **강력한 검색 및 필터링**
    * 사용자는 영화 제목, 장르 등 다양한 키워드를 조합하여 원하는 영화를 빠르고 정확하게 검색할 수 있습니다.
    * 평점순, 인기순, 최신순 등 다양한 기준으로 결과를 정렬할 수 있습니다.

3.  **사용자 맞춤 기능 및 커뮤니티**
    * Google 계정을 이용한 간편 로그인/회원가입 기능을 제공하여 서비스 접근성을 높입니다.
    * 각 영화 상세 페이지에서 사용자는 자신의 댓글을 남길 수 있으며, 다른 사용자의 의견을 확인하고 공감하며 소통할 수 있습니다.

4.  **다양한 추천 및 인기 목록**
    * 현재 가장 인기 있는 영화, 높은 평점을 받은 영화, 최근 개봉작 등 다양한 기준으로 정렬된 영화 목록을 제공하여 사용자의 영화 탐색을 돕습니다.
    * (향후 확장 기능) 사용자 활동 패턴 및 선호도를 분석하여 개인화된 영화를 추천하는 기능을 제공할 수 있습니다.

---

## 기술 스택

### Backend
* **Language**: Python
* **Framework**: Django
* **Architecture**: Domain-Driven Design (DDD)
* **Authentication**: Google Social Login 
* **Database**: sqlite
* **APIs**: Django REST framework

### Frontend
* **Framework**: Vue.js (v3.5.13)
* **Language**: JavaScript
* **Build Tool**: Vite
* **Routing**: Vue Router (v4.5.1)
* **State Management**: Pinia (v3.0.2)
* **HTTP Client**: Axios (v1.9.0)
* **UI/Icons**: Font Awesome (v6.7.2)
* **Social Login**: vue3-google-login (v2.0.33)
* **Dev Tools**: vite-plugin-vue-devtools (v7.7.2)

### Common
* **Version Control**: Git, GitHub

---

## 프로젝트 구조

### 프론트엔드 (Vue.js)

프론트엔드는 Vue.js를 기반으로 하며, 주요 디렉토리 구성은 다음과 같습니다.

* `src/assets/`: 정적 에셋(이미지, 폰트 등)을 포함합니다.
* `src/components/`: 애플리케이션 전반에서 사용되는 공통 컴포넌트 및 특정 도메인(예: `movie`, `user`)별 UI 컴포넌트, 페이지 레이아웃 컴포넌트(`layout`)를 관리합니다.
    * `common/`: `AppHeader`, `AppFooter`, `LoadingSpinner`, `SearchBar` 등 범용 컴포넌트
    * `movie/`: `MovieCard`, `MovieList`, `RatingComparison` 등 영화 관련 컴포넌트
    * `user/`: `WishlistButton`, `UserProfile` 등 사용자 관련 컴포넌트
    * `layout/`: `MainLayout`, `AuthLayout` 등 페이지 구조를 정의하는 레이아웃
* `src/views/`: Vue Router에 의해 관리되는 페이지 레벨의 컴포넌트들입니다. (예: `HomeView`, `MovieDetailView`)
* `src/stores/`: Pinia를 사용한 상태 관리 모듈입니다. (예: `auth.js`, `movies.js`)
* `src/router/`: Vue Router 설정 파일(`index.js`)을 포함하여 라우팅 로직을 관리합니다.
* `src/services/`: 외부 API 연동과 같은 비즈니스 로직 또는 서비스 모듈을 관리합니다.
* `src/styles/`: 전역 CSS 또는 스타일 관련 파일을 관리합니다.
* `src/App.vue`: 애플리케이션의 최상위 루트 컴포넌트입니다.
* `src/main.js`: Vue 인스턴스를 생성하고, 플러그인 및 전역 설정을 초기화하는 엔트리 파일입니다.

### 백엔드 (Django - DDD)

백엔드는 Django 프레임워크를 기반으로 하며, 도메인 주도 설계(DDD) 원칙을 적용하여 각 Django 앱이 특정 비즈니스 도메인 또는 컨텍스트를 담당하도록 구성됩니다. `apps` 디렉토리 내에 각 도메인별 앱(예: `account`, `movie`, `review_community` 등)이 위치합니다.

각 DDD 앱 내의 주요 패키지 역할은 다음과 같습니다.

* **`apps/`**:
    * Django 애플리케이션들의 루트 디렉토리입니다. 각 하위 디렉토리(예: `account`, `movie`)는 하나의 독립적인 Django 앱이자, DDD에서의 바운디드 컨텍스트(Bounded Context) 또는 주요 기능 영역을 나타냅니다.

* **`apps/[도메인_앱_이름]/application/`**:
    * **역할**: 애플리케이션 서비스 계층입니다. 사용자의 요청(Use Case)을 입력받아 해당 유스케이스의 실행 흐름을 조정하고, 도메인 객체들 간의 상호작용을 오케스트레이션합니다. 외부(Interface 계층)와 도메인 계층 사이의 중재자 역할을 수행합니다.
    * **주요 구성**: `services.py`(유스케이스 로직), `dtos.py`(Data Transfer Objects, 계층 간 데이터 전달용 객체).

* **`apps/[도메인_앱_이름]/domain/`**:
    * **역할**: 도메인 계층으로, 프로젝트의 핵심 비즈니스 로직과 규칙, 상태를 포함하는 도메인 모델이 위치합니다.
    * **주요 구성**: `aggregates/entity` 또는 `aggregates/aggregate root` (애그리거트 루트, 엔티티), `value_objects` (값 객체), `repositories.py` (리포지토리 인터페이스), (필요시) `services.py` (도메인 서비스).

* **`apps/[도메인_앱_이름]/infrastructure/`**:
    * **역할**: 인프라스트럭처 계층입니다. 도메인 계층에서 정의한 인터페이스(주로 리포지토리)에 대한 실제 구현을 담당하며, 데이터베이스 연동, 외부 API 호출 등 기술적인 세부 사항을 처리합니다.
    * **주요 구성**: `repositories.py` (리포지토리 구현체)

* **`apps/[도메인_앱_이름]/interface/`**:
    * **역할**: 인터페이스 계층 (프레젠테이션 계층 또는 어댑터 계층)입니다. 외부 시스템(주로 웹 클라이언트)과의 상호작용을 담당합니다. HTTP 요청을 수신하고, 이를 내부 시스템이 이해할 수 있는 형태로 변환하여 애플리케이션 서비스로 전달하며, 애플리케이션 서비스의 처리 결과를 HTTP 응답으로 변환하여 반환합니다.
    * **주요 구성**: `views.py` (API 엔드포인트 로직, DRF의 ViewSet 등), `serializers.py` (데이터 직렬화/역직렬화), `urls.py` (URL 라우팅).

* **`apps/[도메인_앱_이름]/models.py`**:
    * **역할**: Django의 ORM 모델을 정의합니다 model은 데이터베이스와의 영속성을 담당합니다. 

* **`apps/[도메인_앱_이름]/tests/`**:
    * **역할**: 해당 Django 앱의 단위 테스트, 통합 테스트, 기능 테스트 등 다양한 유형의 테스트 코드를 포함합니다. 각 계층의 역할과 책임에 맞게 테스트를 작성하여 코드의 안정성과 품질을 확보합니다.

---

## 설치

### 사전 준비 사항

* Python (버전 명시, 예: 3.10 이상)
* pip (Python 패키지 관리자)
* Git
* Node.js (버전 명시, 예: 18.x 이상) 및 npm 또는 yarn
* [데이터베이스 종류 및 버전] (예: PostgreSQL 14 이상)
* (선택 사항) Docker, Docker Compose

### 소스 코드 가져오기

```bash
git clone [프로젝트_저장소_URL]
cd [프로젝트_디렉토리명]
```

## 설치

### 사전 준비 사항

* Python (버전 명시, 예: 3.10 이상)
* pip (Python 패키지 관리자)
* Git
* Node.js (버전 명시, 예: 18.x 이상) 및 npm 또는 yarn
* [데이터베이스 종류 및 버전] (예: PostgreSQL 14 이상)
* (선택 사항) Docker, Docker Compose

### 소스 코드 가져오기

```bash
git clone [프로젝트_저장소_URL]
cd [프로젝트_디렉토리명]
```



# 의존성 설치 및 환경 설정

# backend(django)

```bash
python -m venv venv
```
## Linux/macOS
```bash
source venv/bin/activate
```
## Windows
```bash
venv\Scripts\activate
```

## 의존성 패키지 설치

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

# frontend(vue.js)

프론트엔드 디렉토리로 이동: cd [프론트엔드_경로]

## 의존성 패키지 설치

```bash
npm install
또는 yarn 사용 시:
yarn install
```

# 실행

## backend(django)

```bash
python manage.py runserver
```

## frontend(vue.js)

```bash
npm run dev
또는 yarn 사용 시:
yarn dev
```

# 시작하기
애플리케이션 실행 후, 웹 브라우저에서 프론트엔드 개발 서버 주소로 접속하여 서비스를 이용할 수 있습니다.

회원가입/로그인: Google 계정을 이용하여 간편하게 시작하세요.
영화 탐색: 메인 페이지의 추천 목록, 검색창, 필터 기능을 활용하여 원하는 영화를 찾아보세요.
상세 정보 확인: 영화 카드를 클릭하여 상세 페이지로 이동하면 국내외 평점, OTT 정보, 사용자 댓글 등 다양한 정보를 확인할 수 있습니다.

# 팀

성경준(backend): skil1489@naver.com

고재혁(frontend): 



