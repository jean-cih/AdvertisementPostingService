from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from src.models.models import User, Comment, Complaint

async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment:
    comment = await db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

async def get_complaint_by_id(db: AsyncSession, complaint_id: int) -> Complaint:
    complaint = await db.get(Complaint, complaint_id)
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint