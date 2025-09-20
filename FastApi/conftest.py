# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# 테스트용 인메모리 SQLite 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테스트 중에는 get_db 의존성을 테스트용 DB 세션으로 오버라이드(대체)합니다.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# FastAPI 앱의 의존성을 오버라이드합니다.
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """
    각 테스트 함수가 실행될 때마다 새로운 DB 테이블을 생성하고,
    테스트가 끝나면 테이블을 삭제합니다.
    이를 통해 각 테스트는 독립적인 환경에서 실행됩니다.
    """
    # 테이블 생성
    Base.metadata.create_all(bind=engine)

    # TestClient를 컨텍스트 매니저와 함께 사용하여 startup/shutdown 이벤트를 처리합니다.
    with TestClient(app) as c:
        yield c

    # 테이블 삭제
    Base.metadata.drop_all(bind=engine)