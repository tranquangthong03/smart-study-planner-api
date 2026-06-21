from datetime import datetime
from pydantic import BaseModel, Field

# Base chỉ chứa những trường chung nhất
class StudySessionBase(BaseModel):
    note: str | None = None

# Khi tạo mới (Bắt đầu phiên học)
class StudySessionCreate(StudySessionBase):
    task_id: int = Field(..., description="ID của Task đang học")
    started_at: datetime = Field(default_factory=datetime.now, description="Thời gian bắt đầu")
    # KHÔNG CÓ ended_at và duration_minutes ở đây

# Khi cập nhật (Kết thúc phiên học hoặc thêm ghi chú)
class StudySessionUpdate(BaseModel):
    ended_at: datetime | None = Field(None, description="Thời gian kết thúc")
    note: str | None = None
    # KHÔNG CÓ duration_minutes ở đây vì Backend sẽ tự tính

# Khi trả về cho Client
class StudySessionResponse(StudySessionBase):
    id: int
    task_id: int
    started_at: datetime
    ended_at: datetime | None = None
    duration_minutes: int | None = None  # Backend trả về sau khi tính toán
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True