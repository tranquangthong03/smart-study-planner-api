from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class StudyTask(Base):
    __tablename__ = "study_tasks"

    id = Column(Integer, primary_key=True, index=True)

    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    due_date = Column(Date, nullable=True, index=True)
    estimated_minutes = Column(Integer, nullable=True)

    status = Column(String, default="pending", nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    topic = relationship(
        "Topic",
        back_populates="study_tasks"
    )

    study_sessions = relationship(
        "StudySession",
        back_populates="study_task",
        cascade="all, delete-orphan"
    )

    review_schedules = relationship(
        "ReviewSchedule",
        back_populates="study_task",
        cascade="all, delete-orphan"
    )