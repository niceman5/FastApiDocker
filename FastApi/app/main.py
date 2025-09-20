# FastAPI 애플리케이션을 생성하고, 라우터를 포함하며, 앱 시작 시 데이터베이스 테이블을 생성합니다.

# app/main.py
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, posts

# SQLAlchemy 모델을 기반으로 데이터베이스 테이블 생성
# 만약 테이블이 이미 존재하면 생성하지 않음
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 라우터 포함
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI application!"}
