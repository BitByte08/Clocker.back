from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    password: str  # 평문 입력

class UserRead(BaseModel):
    id: int
    name: str
    created_at: datetime  # DB에서 읽어올 때 문자열 혹은 datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
