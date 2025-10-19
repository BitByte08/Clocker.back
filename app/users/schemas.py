# users/schemas.py
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    password_hash: str

class UserRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True
