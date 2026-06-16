from datetime import datetime

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
  email: EmailStr
  full_name:str | None = None

class UserCreate(UserBase):
  password: str

class UserUpdate(BaseModel):
  # Không cần kế thừa UserBase vì có những thuộc tính không cần thiết
  full_name: str | None = None
  is_active: bool | None = None

class UserResponse(UserBase):
  id: int
  is_active: bool
  created_at: datetime
  update_at: datetime

  class config:
    from_attributes = True
  