from datetime import date, datetime

from pydantic import BaseModel


class StudyGoalBase(BaseModel):
    title: str
    description: str | None = None
    target_date: date | None = None


class StudyGoalCreate(StudyGoalBase):
    pass


class StudyGoalUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    target_date: date | None = None
    status: str | None = None


class StudyGoalResponse(StudyGoalBase):
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  