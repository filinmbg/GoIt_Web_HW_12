import enum

from sqlalchemy import Column, Integer, String, DateTime, func, Enum, Date
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    first_name = Column(String(25), nullable=False, index=True)
    last_name = Column(String(30), nullable=False, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column("roles", Enum(Role), default=Role.user)
    phone_number = Column(String(25), nullable=False)
    born_date = Column(Date, nullable=False)
    description = Column(String(250))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
