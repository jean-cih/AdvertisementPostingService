from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional
from src.models.models import User, Advert, Comment, Complaint
from src.schemas.admin import (
    UserUpdateRole,
    UserOut,
    ComplaintOut,
    ComplaintUpdate
)
from src.database import get_db
from src.core.security import get_admin_user
from src.services.admin import (
    get_user_by_id,
    get_comment_by_id,
    get_complaint_by_id
)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserOut])
async def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    query = select(User).offset(skip).limit(limit)
    
    if search:
        query = query.where(User.username.ilike(f"%{search}%"))
    
    result = await db.execute(query.order_by(User.id))
    return result.scalars().all()

@router.patch("/users/{user_id}/role", response_model=UserOut)
async def change_user_role(
    user_id: int,
    role_data: UserUpdateRole,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot change your own role"
        )
    
    user = await get_user_by_id(db, user_id)
    
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(role=role_data.role)
    )
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/users/{user_id}/ban", response_model=UserOut)
async def ban_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    if admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot ban yourself"
        )
    
    user = await get_user_by_id(db, user_id)
    
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(is_active=False)
    )
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/users/{user_id}/unban", response_model=UserOut)
async def unban_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    user = await get_user_by_id(db, user_id)
    
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(is_active=True)
    )
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    comment = await get_comment_by_id(db, comment_id)
    
    await db.delete(comment)
    await db.commit()
    return None

@router.get("/complaints", response_model=List[ComplaintOut])
async def get_all_complaints(
    resolved: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    query = select(Complaint).offset(skip).limit(limit)
    
    if resolved is not None:
        query = query.where(Complaint.is_resolved == resolved)
    
    result = await db.execute(query.order_by(Complaint.created_at.desc()))
    return result.scalars().all()

@router.patch("/complaints/{complaint_id}", response_model=ComplaintOut)
async def resolve_complaint(
    complaint_id: int,
    complaint_data: ComplaintUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    complaint = await get_complaint_by_id(db, complaint_id)
    
    await db.execute(
        update(Complaint)
        .where(Complaint.id == complaint_id)
        .values(is_resolved=complaint_data.is_resolved)
    )
    await db.commit()
    await db.refresh(complaint)
    return complaint

@router.delete("/adverts/{advert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert_admin(
    advert_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    advert = await db.get(Advert, advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    
    await db.delete(advert)
    await db.commit()
    return None