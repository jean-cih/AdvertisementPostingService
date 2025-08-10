from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from enum import Enum


class Base(DeclarativeBase):
    pass


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)

    adverts: Mapped[list["Advert"]] = relationship(back_populates="owner")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")
    complaints: Mapped[list["Complaint"]] = relationship(back_populates="complainant")


class AdvertType(str, Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    SERVICE = "service"


class Advert(Base):
    __tablename__ = "adverts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    type_advert: Mapped[AdvertType] = mapped_column(index=True) # 'sale', 'purchase', 'service'
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="adverts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="advert")
    complaints: Mapped[list["Complaint"]] = relationship(back_populates="advert")


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    advert: Mapped["Advert"] = relationship(back_populates="comments")


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True)
    reason: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    complainant_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    advert_id: Mapped[int] = mapped_column(ForeignKey("adverts.id"))
    is_resolved: Mapped[bool] = mapped_column(default=False)

    complainant: Mapped["User"] = relationship(back_populates="complainants")
    advert: Mapped["Advert"] = relationship(back_populates="complainants")