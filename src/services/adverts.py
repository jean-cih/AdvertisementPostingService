from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Advert

async def check_advert_exists(db: AsyncSession, advert_id: int) -> Advert:
    advert = await db.get(Advert, advert_id)
    if not advert:
        raise HTTPException(status_code=404, detail="Advert not found")
    return advert

async def check_advert_ownership(
    db: AsyncSession, 
    advert_id: int, 
    user_id: int
) -> bool:
    advert = await check_advert_exists(db, advert_id)
    if advert.owner_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You don't own this advert"
        )
    return True