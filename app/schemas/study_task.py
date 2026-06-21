from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field

# Định nghĩa Enum cho Status
class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
class StudyTaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    estimated_minutes: int | None = Field(default=None, ge=1)
    # 2. Đưa status vào Base và set mặc định là TODO
    status: TaskStatus = Field(default=TaskStatus.TODO)

class StudyTaskCreate(StudyTaskBase):
    topic_id: int


class StudyTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: date | None = None
    estimated_minutes: int | None = Field(default=None, ge=1)
    status: str | None = None


class StudyTaskResponse(StudyTaskBase):
    id: int
    topic_id: int
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True