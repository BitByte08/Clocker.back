from pydantic import BaseModel
from datetime import datetime

class UserRead(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        orm_mode = True
