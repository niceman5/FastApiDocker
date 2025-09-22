# app/routers/posts.py
# Post API 라우터
# 게시물 생성 및 관리를 위한 API 엔드포인트입니다.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

# APIRouter 인스턴스를 생성합니다.
# prefix="/posts": 이 라우터의 모든 경로는 "/posts"로 시작합니다. (예: /posts/, /posts/1)
# tags=["posts"]: FastAPI 자동 문서(Swagger UI)에서 API들을 "posts" 그룹으로 묶어줍니다.
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# 게시물 생성 API 엔드포인트
# POST /posts/
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # 게시물을 생성하기 전에, 게시물의 소유자(owner)가 될 사용자가 DB에 실제로 존재하는지 확인합니다.
    db_user = db.query(models.User).filter(models.User.user_no == post.user_no).first()
    if db_user is None:
        # 사용자가 존재하지 않으면 404 Not Found 에러를 발생시킵니다.
        raise HTTPException(status_code=404, detail="Owner User not found")

    # schemas.PostCreate(Pydantic 모델)를 models.Post(SQLAlchemy 모델)로 변환하여 DB에 저장할 객체를 만듭니다.
    db_post = models.Post(**post.dict())
    db.add(db_post)  # DB 세션에 새 게시물 객체를 추가합니다. (아직 DB에 저장된 것은 아님)
    db.commit()     # 세션의 변경사항(새 게시물 추가)을 DB에 최종 반영(저장)합니다.
    db.refresh(db_post)  # DB에 저장된 후의 최신 정보(예: 자동 생성된 post_no, reg_date)를 객체에 다시 로드합니다.
    return db_post

# 전체 게시물 목록 조회 API 엔드포인트
# GET /posts/
@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # offset(skip).limit(limit)를 사용하여 페이지네이션(pagination)을 구현합니다.
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

# 특정 게시물 한 개 조회 API 엔드포인트
# GET /posts/{post_no}
@router.get("/{post_no}", response_model=schemas.Post)
def read_post(post_no: int, db: Session = Depends(get_db)):
    # post_no를 기준으로 게시물을 조회합니다.
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        # 게시물이 없으면 404 Not Found 에러를 발생시킵니다.
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# 게시물 수정 API 엔드포인트
# PUT /posts/{post_no}
@router.put("/{post_no}", response_model=schemas.Post)
def update_post(post_no: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    # 수정할 게시물을 DB에서 조회합니다.
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # 요청으로 받은 데이터(post)의 각 필드를 기존 게시물 객체(db_post)에 업데이트합니다.
    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()  # 변경사항을 DB에 저장합니다.
    db.refresh(db_post)  # DB의 최신 정보로 객체를 갱신합니다.
    return db_post

# 게시물 삭제 API 엔드포인트
# DELETE /posts/{post_no}
@router.delete("/{post_no}", response_model=schemas.Post)
def delete_post(post_no: int, db: Session = Depends(get_db)):
    # 삭제할 게시물을 DB에서 조회합니다.
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)  # 해당 게시물을 삭제 대상으로 지정합니다.
    db.commit()         # 변경사항(삭제)을 DB에 최종 반영합니다.
    return db_post
