-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Docker를 이용한 Python FastAPI 프로젝트 설정

## 1. FastAPI 애플리케이션

### Docker 이미지 빌드
```bash
docker build -t fastapi-app .
```

### Docker 컨테이너 실행

#### 기본 실행
```bash
# -d: 컨테이너를 백그라운드에서 실행합니다.
docker run -d -p 8000:80 --name fastapi-container fastapi-app
docker run -d -p 8000:80 -v C:\docker\FastApi/app:/app --name fastapi-dev fastapi-app
```

#### 개발용 실행 (소스코드 변경 시 자동 리로드)
> `ImportError: attempted relative import with no known parent package` 오류를 해결하고,
> 소스코드 변경 시 `uvicorn`이 자동으로 재시작되도록 `--reload` 옵션을 사용합니다.

```bash
# -v C:\docker\FastApi:/app : 프로젝트 루트를 컨테이너의 /app으로 마운트
# -v C:\docker\FastApi\data:/data : 로컬 data 폴더를 컨테이너의 /data 폴더에 마운트하여 DB 파일 영속성 유지
# -w /app : 컨테이너의 작업 디렉토리를 /app으로 설정
docker run -d -p 8000:80 -v C:\docker\FastApi:/app -v C:\docker\FastApi\data:/data -w /app --name fastapi-dev fastapi-app uvicorn app.main:app --reload --host 0.0.0.0 --port 80
```

### 확인 ✅
웹 브라우저를 열고 아래 주소로 접속하여 메시지가 잘 표시되는지 확인합니다.

*   **API 접속:** http://localhost:8000
*   **API 자동 문서 (Swagger UI):** http://localhost:8000/docs

### 테스트 실행 (Pytest)
1.  실행 중인 개발 컨테이너의 셸에 접속합니다.
    ```bash
    docker exec -it fastapi-dev /bin/bash
    ```
2.  컨테이너 내부의 `/app` 디렉토리에서 `pytest`를 실행합니다.
    ```bash
    # pytest 명령어는 자동으로 'tests' 폴더를 찾아 테스트를 실행합니다.
    pytest
    ```

### 컨테이너 관리
```bash
# 컨테이너 중지
docker stop fastapi-dev

# 컨테이너 삭제
docker rm fastapi-dev
```

---

## 2. Docker 컨테이너 셸(Shell) 실행

1.  **컨테이너 셸 접속**
    가장 일반적으로 사용되는 Bash 셸을 실행합니다.
    ```bash
    # docker exec: 실행 중인 컨테이너에서 명령어를 실행합니다.
    # -it: -i(interactive)와 -t(tty) 옵션을 합친 것으로, 셸을 대화형 모드로 실행하기 위해 필수적입니다.
    # fastapi-dev: 접속하려는 컨테이너의 이름입니다. ID를 사용해도 됩니다.
    # /bin/bash: 컨테이너 내부에서 실행할 명령어입니다. (Bash 셸 실행)
    docker exec -it fastapi-dev /bin/bash
    ```

2.  **셸 종료**
    컨테이너 내부에서 작업을 마친 후 원래의 PC 터미널로 돌아오려면 아래 명령어 중 하나를 입력하세요.
    ```bash
    exit
    ```
    또는 키보드에서 `Ctrl + D`를 눌러도 됩니다.

---

## 3. Docker를 이용한 SQLite3 환경 설정

### Dockerfile 작성
경량화된 리눅스 배포판인 Alpine Linux를 기반으로 Dockerfile을 작성합니다.

```dockerfile
# Alpine Linux를 기반 이미지로 사용합니다.
FROM alpine:latest

# sqlite 패키지를 설치합니다.
# --no-cache 옵션은 이미지 용량을 줄이는 데 도움이 됩니다.
RUN apk add --no-cache sqlite

# 컨테이너가 시작될 때 실행할 기본 명령어를 설정합니다.
# 여기서는 컨테이너가 바로 종료되지 않도록 sleep 명령어를 사용합니다.
CMD ["sleep", "infinity"]
```

### Docker 이미지 빌드 및 컨테이너 실행
1.  **이미지 빌드**
    ```bash
    # -t my-sqlite는 이미지의 이름을 my-sqlite로 지정하는 옵션입니다.
    docker build -t my-sqlite .
    ```

2.  **컨테이너 실행 (로컬 볼륨 마운트)**
    > DB Browser for SQLite와 같은 GUI 도구에서 접속하려면, 데이터베이스 파일이 저장될 컨테이너의 디렉토리를 로컬 PC의 디렉토리와 연결(마운트)해야 합니다.

    *   **Windows (CMD)**
        ```bash
        docker run -d --name my-sqlite-container -v "%cd%/db:/data" my-sqlite
        ```
    *   **Windows (PowerShell)**
        ```bash
        docker run -d --name my-sqlite-container -v "${PWD}/db:/data" my-sqlite
        ```
    *   **Mac/Linux**
        ```bash
        docker run -d --name my-sqlite-container -v "$(pwd)/db:/data" my-sqlite
        ```
3.  **컨테이너 접속 및 SQLite 사용**
    ```bash
    docker exec -it my-sqlite-container /bin/bash
    ```
4.  **컨테이너 내부에서 DB 작업**
    ```bash
    # /data 디렉터리로 이동
    cd /data

    # sqlite3로 데이터베이스 파일(예: myapp.db)을 엽니다. 파일이 없으면 새로 생성됩니다.
    sqlite3 myapp.db

    # sqlite> 프롬프트가 나타나면 아래 명령어로 스키마를 읽어옵니다.
    .read schema.sql

    # .tables 명령어로 테이블이 잘 생성되었는지 확인합니다.
    .tables

    # .exit 로 빠져나옵니다.
    .exit
    ```