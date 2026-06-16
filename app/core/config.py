from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str # Tên biến phải trùng với tên biến củ file .env
  ALGORITHM: str = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

  class Config:
    env_file = ".env"

settings = Settings()
