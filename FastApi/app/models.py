# app/models.py
# schema.sql의 테이블 구조를 파이썬 클래스로 정의합니다. 이 모델을 통해 ORM이 데이터베이스와 상호작용합니다.

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base


# 'users' 테이블에 매핑되는 User 클래스
class User(Base):
    # 데이터베이스 내의 테이블 이름
    __tablename__ = "users"

    # 테이블의 컬럼(속성) 정의
    user_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=True)
    user_sex = Column(String, default='M')
    user_name = Column(String, nullable=False)
    # default=func.now()는 SQLAlchemy가 데이터베이스의 현재 시간 함수(예: NOW())를 사용하도록 합니다.
    reg_date = Column(DateTime, nullable=False, default=func.now())

    # 다른 테이블과의 관계(Relationship) 설정
    # 'Post' 모델과의 관계를 정의합니다. 한 명의 사용자는 여러 개의 게시물(posts)을 가질 수 있습니다.
    # back_populates="owner"는 Post 모델의 'owner' 속성과 상호 연결되어 양방향 관계를 형성합니다.
    posts = relationship("Post", back_populates="owner")


# 'posts' 테이블에 매핑되는 Post 클래스
class Post(Base):
    # 데이터베이스 내의 테이블 이름
    __tablename__ = "posts"

    # 테이블의 컬럼(속성) 정의
    post_no = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    reg_date = Column(DateTime, nullable=False, default=func.now())
    # 외래 키(Foreign Key) 설정. 'users' 테이블의 'user_no' 컬럼을 참조합니다.
    # ondelete="CASCADE"는 연결된 User가 삭제될 때, 해당 User가 작성한 Post도 함께 삭제되도록 하는 설정입니다.
    user_no = Column(Integer, ForeignKey("users.user_no", ondelete="CASCADE"), nullable=False)

    # 'User' 모델과의 관계를 정의합니다. 하나의 게시물은 한 명의 소유자(owner)를 가집니다.
    # back_populates="posts"는 User 모델의 'posts' 속성과 상호 연결됩니다.
    owner = relationship("User", back_populates="posts")
