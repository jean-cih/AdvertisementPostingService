from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
from enum import Enum
import uvicorn

app = FastAPI()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class Advert(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    type_advert: Mapped[Advert] = mapped_column(index=True) # 'sale', 'purchase', 'service'
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Advert(str, Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    SERVICE = "service"


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id"))


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    reason: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    complainant_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id"))
    is_resolved: Mapped[bool] = mapped_column(default=False)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)