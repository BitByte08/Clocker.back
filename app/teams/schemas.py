from pydantic import BaseModel
from datetime import datetime

class TeamCreate(BaseModel):
    name: str
    description: str | None = None
    creator_user_id: int

class TeamRead(BaseModel):
    id: int
    name: str
    description: str | None
    creator_user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
