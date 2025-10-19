# schedules/router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from database import get_db

router = APIRouter()

# -------------------- Create Schedule --------------------
@router.post("/", response_model=schemas.ScheduleRead)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    return crud.create_schedule(
        db=db,
        team_id=schedule.team_id,
        creator_user_id=schedule.creator_user_id,
        title=schedule.title,
        description=schedule.description,
        start_time=schedule.start_time,
        end_time=schedule.end_time
    )

# -------------------- Read Schedules --------------------
@router.get("/", response_model=list[schemas.ScheduleRead])
def read_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_schedules(db, skip=skip, limit=limit)
