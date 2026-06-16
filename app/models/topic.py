from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)

    goal_id = Column(Integer, ForeignKey("study_goals.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    priority = Column(Integer, default=3, nullable=False, index=True)
    status = Column(String, default="not_started", nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    study_goal = relationship(
        "StudyGoal",
        back_populates="topics"
    )

    study_tasks = relationship(
        "StudyTask",
        back_populates="topic",
        cascade="all, delete-orphan"
    )