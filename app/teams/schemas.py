# auth 또는 team/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TeamCreate(BaseModel):
    name: str
    description: Optional[str] = None

class TeamRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    creator_user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2
