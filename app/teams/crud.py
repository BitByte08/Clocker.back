from sqlalchemy.orm import Session
from models import Team, TeamMember

def create_team(db: Session, name: str, creator_user_id: int, description: str = None):
    # 팀 생성
    team = Team(name=name, creator_user_id=creator_user_id, description=description)
    db.add(team)
    db.commit()
    db.refresh(team)

    # 생성자 팀멤버(admin) 추가
    member = TeamMember(team_id=team.id, user_id=creator_user_id, role_in_team="admin")
    db.add(member)
    db.commit()
    db.refresh(member)

    return team
