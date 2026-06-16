from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base

# Có tác dụng ôn tập lại theo thời gian (1 ngày, 3 ngày, 7 ngày để chống quên)
class ReviewSchedule(Base):
    __tablename__ = "review_schedules"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("study_tasks.id"), nullable=False, index=True)

    review_date = Column(Date, nullable=False, index=True)

    status = Column(String, default="pending", nullable=False, index=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    study_task = relationship(
        "StudyTask",
        back_populates="review_schedules"
    )