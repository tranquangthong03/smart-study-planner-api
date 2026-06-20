from fastapi import FastAPI
from app.api.v1 import auth, health, goals
app = FastAPI(
  title="Smart Study Planner API",
  version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(goals.router, prefix="/api/v1")