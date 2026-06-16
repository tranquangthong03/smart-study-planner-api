from datetime import date, datetime

from pydantic import BaseModel


class ReviewScheduleBase(BaseModel):
    task_id: int
    review_date: date


class ReviewScheduleCreate(ReviewScheduleBase):
    pass


class ReviewScheduleUpdate(BaseModel):
    review_date: date | None = None
    status: str | None = None
    completed_at: datetime | None = None


class ReviewScheduleResponse(ReviewScheduleBase):
    id: int
    status: str
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True