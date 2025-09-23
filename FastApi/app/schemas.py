# app/schemas.py
# API의 요청(Request) 및 응답(Response) 데이터 형식을 정의하고 유효성을 검사합니다.

from pydantic import BaseModel
from typing import List, Optional
import datetime


# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    user_no: int


class Post(PostBase):
    post_no: int
    reg_date: datetime.datetime
    user_no: int

    class Config:
        orm_mode = True


# --- User Schemas ---
class UserBase(BaseModel):
    id: str
    email: str
    phone_number: Optional[str] = None
    user_sex: Optional[str] = 'M'
    user_name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    user_no: int
    reg_date: datetime.datetime
    posts: List[Post] = []

    class Config:
        orm_mode = True
