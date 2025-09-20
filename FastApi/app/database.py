# app/database.py
# 데이터베이스 연결 세션을 생성하고 관리하는 파일입니다.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Docker 컨테이너 내에서 SQLite DB 파일 경로
# README.md에서 볼륨 마운트 설정을 (-v ...:/data) 기준으로 경로를 /data/myapp.db로 지정합니다.
SQLALCHEMY_DATABASE_URL = "sqlite:////data/myapp.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 의존성 주입 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
