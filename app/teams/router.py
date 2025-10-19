from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud, schemas
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.TeamRead)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db, team.name, team.description, team.creator_user_id)

@router.get("/", response_model=list[schemas.TeamRead])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_teams(db, skip, limit)
