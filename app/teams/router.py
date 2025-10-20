from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth.dependencies import get_current_user
from . import crud, schemas
from auth.crud import User

router = APIRouter()

@router.post("", response_model=schemas.TeamRead)
def create_team(
    team_data: schemas.TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    팀 생성 API
    - 팀 생성 시 로그인한 유저를 admin으로 자동 추가
    """
    return crud.create_team(
        db,
        name=team_data.name,
        description=team_data.description,
        creator_user_id=current_user.id
    )
