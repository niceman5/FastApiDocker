# app/database.py
# 데이터베이스 연결 세션을 생성하고 관리하는 파일입니다.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- 데이터베이스 연결 설정 ---

# Docker 컨테이너 내의 SQLite 데이터베이스 파일 경로입니다.
# docker run 명령어의 볼륨 마운트 설정(-v C:\docker\FastApi\data:/data)에 따라
# 로컬의 'C:\docker\FastApi\data' 폴더가 컨테이너의 '/data' 폴더와 연결됩니다.
# 따라서 컨테이너 내부에서는 '/data/myapp.db' 경로를 사용합니다.
SQLALCHEMY_DATABASE_URL = "sqlite:////data/myapp.db"

# SQLAlchemy '엔진'을 생성합니다. 엔진은 데이터베이스와의 실제 연결을 관리합니다.
# connect_args={"check_same_thread": False}는 SQLite를 사용할 때만 필요하며,
# FastAPI가 여러 스레드에서 데이터베이스와 상호작용할 수 있도록 허용하는 설정입니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 세션(Session)을 생성하는 클래스입니다.
# 세션은 ORM을 통해 데이터베이스와 대화하는 통로 역할을 합니다.
# autocommit=False, autoflush=False 설정은 트랜잭션을 명시적으로 관리(db.commit())하도록 합니다.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy 모델(models.py의 클래스들)이 상속받을 기본 클래스입니다.
Base = declarative_base()

# --- 의존성 주입(Dependency Injection) ---

# API 라우터에서 데이터베이스 세션을 사용하기 위한 의존성 함수입니다.
# FastAPI가 API 요청을 처리할 때 이 함수를 호출하여 DB 세션을 얻고, 처리가 끝나면 자동으로 세션을 닫습니다.
def get_db():
    db = SessionLocal()  # DB 세션 인스턴스 생성
    try:
        yield db  # API 함수에 DB 세션을 전달(주입)하고, API 함수의 실행이 끝날 때까지 대기
    finally:
        db.close()  # API 함수 실행이 끝나면(성공/실패 무관) 항상 DB 세션을 닫아 연결을 반환
