from datetime import datetime

from pydantic import BaseModel, EmailStr, validator, Field

class UserBase(BaseModel):
  email: EmailStr
  full_name:str | None = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator("password")
    def max_password_bytes(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password must be at most 72 bytes when encoded")
        return v

class UserUpdate(BaseModel):
  # Không cần kế thừa UserBase vì có những thuộc tính không cần thiết
  full_name: str | None = None
  is_active: bool | None = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
