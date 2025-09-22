# app/routers/users.py
# Users API 라우터
# 회원 가입 및 사용자 정보 관리를 위한 api 엔드포인트

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

# APIRouter 인스턴스를 생성합니다.
# prefix="/users": 이 라우터의 모든 경로는 "/users"로 시작합니다.
# tags=["users"]: FastAPI 자동 문서에서 API들을 "users" 그룹으로 묶어줍니다.
router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# 회원 가입 API 엔드포인트
# POST /users/
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # ID 중복 확인: 요청된 ID가 이미 DB에 존재하는지 확인합니다.
    db_user_by_id = db.query(models.User).filter(models.User.id == user.id).first()
    if db_user_by_id:
        raise HTTPException(status_code=400, detail="ID already registered")

    # 이메일 중복 확인: 요청된 이메일이 이미 DB에 존재하는지 확인합니다.
    db_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # schemas.UserCreate(Pydantic 모델)를 models.User(SQLAlchemy 모델)로 변환하여 DB에 저장할 객체를 만듭니다.
    db_user = models.User(**user.dict())
    db.add(db_user)      # DB 세션에 새 사용자 객체를 추가합니다.
    db.commit()          # 세션의 변경사항을 DB에 최종 반영(저장)합니다.
    db.refresh(db_user)  # DB에 저장된 후의 최신 정보(예: user_no, reg_date)를 객체에 다시 로드합니다.
    return db_user

# 전체 사용자 목록 조회 API 엔드포인트
# GET /users/
@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # offset(skip).limit(limit)를 사용하여 페이지네이션(pagination)을 구현합니다.
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

# 특정 사용자 한 명 조회 API 엔드포인트
# GET /users/{user_no}
@router.get("/{user_no}", response_model=schemas.User)
def read_user(user_no: int, db: Session = Depends(get_db)):
    # user_no를 기준으로 사용자를 조회합니다.
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        # 사용자가 없으면 404 Not Found 에러를 발생시킵니다.
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# 사용자 정보 수정 API 엔드포인트
# PUT /users/{user_no}
@router.put("/{user_no}", response_model=schemas.User)
def update_user(user_no: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 수정할 사용자를 DB에서 조회합니다.
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # ID 중복 체크: 변경하려는 ID가 현재 사용자의 ID가 아니면서, 다른 사용자가 이미 사용 중인지 확인
    if user.id != db_user.id:
        existing_user_id = db.query(models.User).filter(models.User.id == user.id).first()
        if existing_user_id:
            raise HTTPException(status_code=400, detail="ID already registered")

    # 이메일 중복 체크: 변경하려는 이메일이 현재 사용자의 이메일이 아니면서, 다른 사용자가 이미 사용 중인지 확인
    if user.email != db_user.email:
        existing_user_email = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user_email:
            raise HTTPException(status_code=400, detail="Email already registered")

    # 요청으로 받은 데이터(user)의 각 필드를 기존 사용자 객체(db_user)에 업데이트합니다.
    for key, value in user.dict().items():
        setattr(db_user, key, value)

    db.commit()  # 변경사항을 DB에 저장합니다.
    db.refresh(db_user)  # DB의 최신 정보로 객체를 갱신합니다.
    return db_user

# 사용자 삭제 API 엔드포인트
# DELETE /users/{user_no}
@router.delete("/{user_no}", response_model=schemas.User)
def delete_user(user_no: int, db: Session = Depends(get_db)):
    # 삭제할 사용자를 DB에서 조회합니다.
    db_user = db.query(models.User).filter(models.User.user_no == user_no).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)  # 해당 사용자를 삭제 대상으로 지정합니다.
    db.commit()         # 변경사항(삭제)을 DB에 최종 반영합니다.
    return db_user
