# app/routers/posts.py
# Post API 라우터
# 게시물 생성 및 관리를 위한 API 엔드포인트입니다.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

# 게시물 생성
@router.post("/", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # 게시물 작성 전 사용자가 존재하는지 확인
    db_user = db.query(models.User).filter(models.User.user_no == post.user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Owner User not found")

    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 전체 게시물 조회
@router.get("/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

# 특정 게시물 조회
@router.get("/{post_no}", response_model=schemas.Post)
def read_post(post_no: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# 게시물 수정
@router.put("/{post_no}", response_model=schemas.Post)
def update_post(post_no: int, post: schemas.PostBase, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    for key, value in post.dict().items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)
    return db_post

# 게시물 삭제
@router.delete("/{post_no}", response_model=schemas.Post)
def delete_post(post_no: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.post_no == post_no).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(db_post)
    db.commit()
    return db_post
