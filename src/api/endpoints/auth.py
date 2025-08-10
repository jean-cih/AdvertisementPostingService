from fastapi import APIRouter, HTTPException, status, Depends
from ..database import get_db
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


async def create_user(db: AsyncSession, user_data):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.regresh(db_user)

    access_token = create_access_token(data={"sub": user_data.username})
    return {"success": True, "message": "User was added"}


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):
    return await authenticate_user(db, form_data.username, form_data.password)
