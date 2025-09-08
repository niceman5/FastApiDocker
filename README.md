-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-- docker에서 python fastapi설치, build, 실행
-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# docker 생성
docker build -t fastapi-app .

# docker 컨테이너 실행
# -d: 컨테이너를 백그라운드에서 실행합니다.
docker run -d -p 8000:80 --name fastapi-container fastapi-app
docker run -d -p 8000:80 -v C:\docker\FastApi/app:/app --name fastapi-dev fastapi-app


## 4. 확인 ✅
웹 브라우저를 열고 아래 주소로 접속하여 메시지가 잘 표시되는지 확인합니다.

API 접속: http://localhost:8000

API 자동 문서 (Swagger UI): http://localhost:8000/docs

# 컨테이너 중지
docker stop fastapi-container

# 컨테이너 삭제
docker rm fastapi-container

docker run 명령어를 실행할 때, Dockerfile에 정의된 CMD를 무시하고 --reload 옵션이 추가된 새로운 명령어를 직접 전달하면 됩니다.
docker run -d -p 8000:80 -v C:\docker\FastApi/app:/app --name fastapi-dev fastapi-app uvicorn main:app --reload --host 0.0.0.0 --port 80


-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-- docker에서 shell실행
-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# 이제 확인한 컨테이너 이름을 사용하여 셸을 실행합니다. 가장 일반적으로 사용되는 셸은 Bash입니다
docker exec -it fastapi-dev /bin/bash
* docker exec: 실행 중인 컨테이너에서 명령어를 실행합니다.
* -it: -i(interactive)와 -t(tty) 옵션을 합친 것으로, 셸을 대화형 모드로 실행하기 위해 필수적입니다.
* fastapi-dev: 접속하려는 컨테이너의 이름입니다. ID를 사용해도 됩니다.
* /bin/bash: 컨테이너 내부에서 실행할 명령어입니다. (Bash 셸 실행)


## 3단계: 셸 종료
컨테이너 내부에서 작업을 마친 후 원래의 PC 터미널로 돌아오려면 아래 명령어 중 하나를 입력하세요.

exit
또는 키보드에서 Ctrl + D를 눌러도 됩니다.




-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
-- docker에서 sqllite3 설치, build, 실행
-- ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Docker 이미지 빌드 및 컨테이너 실행
이제 작성한 Dockerfile을 사용하여 Docker 이미지를 만들고 컨테이너를 실행합니다.

이미지 빌드: 터미널을 열고 Dockerfile이 있는 디렉토리로 이동한 후, 다음 명령어를 실행하여 이미지를 빌드합니다. sqlite-image는 원하는 이미지 이름으로 변경할 수 있습니다.

docker build -t sqlite-image .

컨테이너 실행: 빌드된 이미지를 사용하여 컨테이너를 실행합니다. my-sqlite-container는 원하는 컨테이너 이름으로 변경 가능합니다
docker run -d --name my-sqlite-container sqlite-image
  * -d 옵션은 컨테이너를 백그라운드에서 실행합니다.

컨테이너 접속 및 SQLite 실행: 실행 중인 컨테이너의 터미널에 접속합니다.
docker exec -it my-sqlite-container /bin/bash

네, Dockerfile을 사용하여 SQLite3를 설치하고, 이를 실행하여 DB Browser for SQLite에 연결하는 방법을 알려드리겠습니다.

Dockerfile 작성
가장 간단한 방법은 경량화된 리눅스 배포판인 Alpine Linux를 기반으로 Dockerfile을 작성하는 것입니다. 아래 내용으로 Dockerfile이라는 이름의 파일을 만드세요.

Dockerfile

# Alpine Linux를 기반 이미지로 사용합니다.
FROM alpine:latest

# sqlite 패키지를 설치합니다.
# --no-cache 옵션은 이미지 용량을 줄이는 데 도움이 됩니다.
RUN apk add --no-cache sqlite

# 컨테이너가 시작될 때 실행할 기본 명령어를 설정합니다.
# 여기서는 컨테이너가 바로 종료되지 않도록 sleep 명령어를 사용합니다.
CMD ["sleep", "infinity"]
Docker 이미지 빌드 및 컨테이너 실행
이제 작성한 Dockerfile을 사용하여 Docker 이미지를 만들고 컨테이너를 실행합니다.

이미지 빌드: 터미널을 열고 Dockerfile이 있는 디렉토리로 이동한 후, 다음 명령어를 실행하여 이미지를 빌드합니다. sqlite-image는 원하는 이미지 이름으로 변경할 수 있습니다.


docker build -t sqlite-image .
컨테이너 실행: 빌드된 이미지를 사용하여 컨테이너를 실행합니다. my-sqlite-container는 원하는 컨테이너 이름으로 변경 가능합니다.


docker run -d --name my-sqlite-container sqlite-image
-d 옵션은 컨테이너를 백그라운드에서 실행합니다.

컨테이너 접속 및 SQLite 실행: 실행 중인 컨테이너의 터미널에 접속합니다.
docker exec -it my-sqlite-container sh



* DB Browser for SQLite에서 접속하는 방법
DB Browser for SQLite와 같은 GUI 도구에서 Docker 컨테이너 안의 데이터베이스 파일에 직접 접속하려면, 데이터베이스 파일이 들어있는 컨테이너의 디렉토리를 로컬 컴퓨터의 디렉토리와 **연결(마운트)**해야 합니다.

기존 컨테이너 중지 및 삭제: 이전에 실행했던 컨테이너가 있다면 중지하고 삭제합니다.

docker stop my-sqlite-container
docker rm my-sqlite-container


로컬 디렉토리와 볼륨을 마운트하여 컨테이너 실행: 로컬 컴퓨터에 데이터베이스 파일을 저장할 폴더를 만듭니다
(예: C:\docker_volumes\sqlite 또는 ~/docker_volumes/sqlite).
그리고 다음 명령어를 사용하여 로컬 폴더와 컨테이너 내부의 /db 폴더를 연결합니다.

Windows 예시:
# Windows (CMD)
docker run -d --name my-sqlite-container -v "%cd%/db:/data" sqlite-image
# Windows (PowerShell)
docker run -d --name my-sqlite-container -v "${PWD}/db:/data" sqlite-image
docker run -d --name my-sqlite-container -v "C:\docker\SQLITE3\db:/data" sqlite-image

Mac/Linux 예시: docker run -d --name my-sqlite-container -v ~/docker_volumes/sqlite:/db sqlite-image



docker exec -it my-sqlite-container /bin/bash
sqlite3 test.db