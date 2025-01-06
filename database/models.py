from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, DeclarativeMeta
from sqlalchemy.sql import func
from pydantic import BaseModel


Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__: str = 'test_table'

    id: Column = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email: Column = Column(String, unique=True, index=True)
    password: Column = Column(String)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class UserSchema(BaseModel):
    id: int
    email: str
    password: str | None
    updated_at: datetime

    class Config:
        from_attributes: bool = True
