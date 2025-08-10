from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from typing import List, Optional
from src.models.models import Advert, User, AdvertType
from src.schemas.adverts import AdvertCreate, AdvertOut, AdvertUpdate
from src.database import get_db
from src.core.security import get_current_user


router = APIRouter(prefix="/adverts", tags=["adverts"])


@router.post("/", response_model=AdvertOut, status_code=status.HTTP_201_CREATED)
async def create_advert(
    advert: AdvertCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_advert = Advert(
        title=advert.title,
        content=advert.content,
        type_advert=advert.type,
        owner_id=current_user.id,
        created_at=datetime.utcnow()
    )
    db.add(db_advert)
    await db.commit()
    await db.refresh(db_advert)
    return db_advert


@router.get("/", response_model=List[AdvertOut])
async def read_adverts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    advert_type: Optional[AdvertType] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Advert).offset(skip).limit(limit)
    
    if advert_type:
        query = query.where(Advert.type_advert == advert_type)
    
    if search:
        query = query.where(Advert.title.ilike(f"%{search}%"))
    
    result = await db.execute(query.order_by(Advert.created_at.desc()))
    return result.scalars().all()


@router.get("/{advert_id}", response_model=AdvertOut)
async def read_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db)
):
    advert = await db.get(Advert, advert_id)
    if advert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Advert not found"
        )
    return advert


@router.put("/{advert_id}", response_model=AdvertOut)
async def update_advert(
    advert_id: int,
    advert: AdvertUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_advert = await db.get(Advert, advert_id)
    if not db_advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    
    if db_advert.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own adverts"
        )
    
    update_data = advert.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_advert, key, value)
    
    await db.commit()
    await db.refresh(db_advert)
    return db_advert


@router.delete("/{advert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(
    advert_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_advert = await db.get(Advert, advert_id)
    if not db_advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    
    # Проверка прав (владелец или админ)
    if db_advert.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this advert"
        )
    
    await db.delete(db_advert)
    await db.commit()
    return None