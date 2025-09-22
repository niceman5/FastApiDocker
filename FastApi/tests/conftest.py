# tests/conftest.py

# 이 파일은 pytest가 테스트를 실행하기 전에 필요한 환경을 설정하는 '설정 파일'입니다.
# 여기서는 실제 데이터베이스가 아닌, 테스트 전용 인메모리(in-memory) 데이터베이스를 사용하도록 설정하여
# 테스트가 실제 데이터에 영향을 주지 않고 독립적으로 실행되도록 합니다.

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 테스트할 FastAPI 애플리케이션과 데이터베이스 관련 모듈을 가져옵니다.
from app.main import app
from app.database import Base, get_db

# 테스트용 인메모리 SQLite 데이터베이스 설정
# 실제 DB 파일('myapp.db') 대신 메모리에서 실행되는 SQLite를 사용합니다.
# 이렇게 하면 각 테스트가 독립적으로 실행되고, 실제 데이터베이스에 영향을 주지 않습니다.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# 테스트용 데이터베이스 엔진 생성
# connect_args={"check_same_thread": False}는 SQLite를 사용할 때만 필요하며,
# FastAPI가 여러 스레드에서 데이터베이스와 상호작용할 수 있도록 허용합니다.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# 테스트용 데이터베이스 세션 생성기
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FastAPI의 의존성(Dependency)을 오버라이드(Override)하는 함수
# API 라우터 함수들에서 Depends(get_db)로 주입받는 DB 세션을
# 실제 DB 세션(SessionLocal) 대신 테스트용 DB 세션(TestingSessionLocal)으로 교체합니다.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# FastAPI 앱의 의존성을 위에서 정의한 override_get_db 함수로 교체합니다.
# 이제부터 앱의 모든 API 요청은 테스트용 데이터베이스를 사용하게 됩니다.
app.dependency_overrides[get_db] = override_get_db

# pytest의 fixture를 사용하여 테스트용 클라이언트를 설정합니다.
# scope="function"은 이 fixture가 각 테스트 함수마다 실행됨을 의미합니다.
# 즉, 모든 테스트는 깨끗한 상태에서 시작됩니다.
@pytest.fixture(scope="function")
def client():
    """
    각 테스트 함수가 실행될 때마다 새로운 DB 테이블을 생성하고,
    테스트가 끝나면 테이블을 삭제합니다.
    이를 통해 각 테스트는 독립적인 환경에서 실행됩니다.
    """
    # 테스트 시작 전: SQLAlchemy 모델에 정의된 모든 테이블을 테스트용 DB에 생성합니다.
    Base.metadata.create_all(bind=engine)

    # TestClient를 생성하여 API에 요청을 보낼 수 있게 합니다.
    # with 문을 사용하면 테스트가 끝난 후 자동으로 정리(shutdown)됩니다.
    with TestClient(app) as c:
        yield c  # 테스트 함수에 TestClient 인스턴스(c)를 전달합니다.

    # 테스트 종료 후: 생성했던 모든 테이블을 DB에서 삭제하여 다음 테스트에 영향을 주지 않도록 합니다.
    Base.metadata.drop_all(bind=engine)
