from sqlalchemy.orm import Session
from models import Team

def create_team(db: Session, name: str, description: str | None, creator_user_id: int):
    team = Team(name=name, description=description, creator_user_id=creator_user_id)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()
