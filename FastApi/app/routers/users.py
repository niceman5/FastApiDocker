# app/routers/users.py
# Users API 라우터
# 회원 가입 및 사용자 정보 관리를 위한 api 엔드포인트

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 회원 가입
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_id = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user_by_id:
        raise HTTPException(status_code=400, detail="ID already registered")

    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 전체 사용자 조회
@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# 특정 사용자 조회
@router.get("/{user_no}", response_model=schemas.User)
def read_user(user_no: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 사용자 정보 수정
@router.put("/{user_no}", response_model=schemas.User)
def update_user(user_no: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 삭제
@router.delete("/{user_no}", response_model=schemas.User)
def delete_user(user_no: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user
