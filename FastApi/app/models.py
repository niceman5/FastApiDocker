# app/models.py
# schema.sql의 테이블 구조를 파이썬 클래스로 정의합니다. 이 모델을 통해 ORM이 데이터베이스와 상호작용합니다.
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    user_sex = Column(String, default='M')
    user_name = Column(String, nullable=False)
    reg_date = Column(DateTime, nullable=False, default=func.now())

    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"

    post_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    reg_date = Column(DateTime, nullable=False, default=func.now())
    user_no = Column(Integer, ForeignKey("users.user_no", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="posts")
