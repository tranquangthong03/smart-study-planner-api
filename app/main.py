from fastapi import FastAPI
from app.api.v1.health import router as health_router

app = FastAPI(
  title="Smart Study Planner API",
  description="Backend API for planner",
  version="1.0.0"
)
app.include_router(health_router, prefix="/api/v1")