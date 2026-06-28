from datetime import date, datetime
from enum import Enum
from pydantic import BaseModel, Field

# 1. Định nghĩa Enum để chặn Client gửi status lung tung
class ReviewStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"

class ReviewScheduleBase(BaseModel):
    review_date: date
    # 2. Đưa status vào Base, mặc định là pending
    status: ReviewStatus = Field(default=ReviewStatus.PENDING)

class ReviewScheduleCreate(ReviewScheduleBase):
    # task_id bắt buộc khi tạo mới để biết được schedule đó thuộc task nào
    task_id: int 

class ReviewScheduleUpdate(BaseModel):
    review_date: date | None = None
    status: ReviewStatus | None = None
    # 3. ĐÃ XÓA completed_at ở đây. Backend sẽ tự lo!

class ReviewScheduleResponse(ReviewScheduleBase):
    id: int
    task_id: int
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True