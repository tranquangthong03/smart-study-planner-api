from datetime import date, datetime

from pydantic import BaseModel, Field


class StudyTaskBase(BaseModel):
    title: str
    description: str | None = None
    due_date: date | None = None
    estimated_minutes: int | None = Field(default=None, ge=1)


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
    status: str
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True