from datetime import datetime

from pydantic import BaseModel, Field


class TopicBase(BaseModel):
    title: str
    description: str | None = None
    priority: int = Field(default=3, ge=1, le=3)


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    priority: int | None = Field(default=None, ge=1, le=3)
    status: str | None = None


class TopicResponse(TopicBase):
    id: int
    goal_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True