from pydantic import BaseModel
from datetime import datetime
from src.models.models import UserRole

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: str
    
    class Config:
        from_attributes = True

class UserUpdateRole(BaseModel):
    role: UserRole

class ComplaintOut(BaseModel):
    id: int
    reason: str
    created_at: datetime
    is_resolved: bool
    complainant_id: int
    advert_id: int
    
    class Config:
        from_attributes = True

class ComplaintUpdate(BaseModel):
    is_resolved: bool