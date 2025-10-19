from sqlalchemy.orm import Session
from models import Schedule

def create_schedule(db: Session, team_id: int, creator_user_id: int, title: str,
                    description: str | None, start_time, end_time):
    schedule = Schedule(
        team_id=team_id,
        creator_user_id=creator_user_id,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule

def get_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Schedule).offset(skip).limit(limit).all()
