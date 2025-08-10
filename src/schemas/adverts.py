from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AdvertType(str, Enum):
    SALE = "sale"
    PURCHASE = "purchase"
    SERVICE = "service"

class AdvertBase(BaseModel):
    title: str
    content: str
    type: AdvertType

class AdvertCreate(AdvertBase):
    pass

class AdvertUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[AdvertType] = None

class AdvertOut(AdvertBase):
    id: int
    owner_id: int
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True