from datetime import datetime

from pydantic import BaseModel, Field


class StudySessionBase(BaseModel):
    task_id: int
    started_at: datetime
    ended_at: datetime | None = None
    duration_minutes: int | None = Field(default=None, ge=1)
    note: str | None = None


class StudySessionCreate(StudySessionBase):
    pass


class StudySessionUpdate(BaseModel):
    ended_at: datetime | None = None
    duration_minutes: int | None = Field(default=None, ge=1)
    note: str | None = None


class StudySessionResponse(StudySessionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True