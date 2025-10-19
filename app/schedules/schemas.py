from pydantic import BaseModel
from datetime import datetime

class ScheduleCreate(BaseModel):
    team_id: int
    creator_user_id: int
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime

class ScheduleRead(BaseModel):
    id: int
    team_id: int
    creator_user_id: int
    title: str
    description: str | None
    start_time: datetime
    end_time: datetime
    created_at: datetime

    class Config:
        orm_mode = True
