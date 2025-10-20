# models.py
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from database import Base


# ==========================
# 👤 User Table
# ==========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    teams_created = relationship("Team", back_populates="creator", cascade="all, delete")
    schedules_created = relationship("Schedule", back_populates="creator", cascade="all, delete")
    team_memberships = relationship("TeamMember", back_populates="user", cascade="all, delete")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


# ==========================
# 👥 Team Table
# ==========================
class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    creator = relationship("User", back_populates="teams_created")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete")
    schedules = relationship("Schedule", back_populates="team", cascade="all, delete")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"


# ==========================
# 🤝 TeamMember Table
# ==========================
class TeamMember(Base):
    __tablename__ = "team_members"

    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_in_team = Column(String, default="member")
    status = Column(String, default="active")
    joined_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

    def __repr__(self):
        return f"<TeamMember(team_id={self.team_id}, user_id={self.user_id}, role='{self.role_in_team}')>"


# ==========================
# 📅 Schedule Table
# ==========================
class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), nullable=False)
    creator_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="schedules")
    creator = relationship("User", back_populates="schedules_created")

    def __repr__(self):
        return f"<Schedule(id={self.id}, title='{self.title}', team_id={self.team_id})>"
