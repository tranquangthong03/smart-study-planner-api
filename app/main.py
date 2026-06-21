from fastapi import FastAPI
from app.api.v1 import auth, health, goals, topics, tasks
app = FastAPI(
  title="Smart Study Planner API",
  version="1.0.0"
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(goals.router, prefix="/api/v1")
app.include_router(topics.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Task"])