from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
router = APIRouter(tags=["Health"])


@router.get("/health")
def heal_check():
  return {
    "status": "ok",
    "message": "Smart Study Planner API running"
  }

@router.get("/health/db")
def database_health_check(db: Session = Depends(get_db)):
  return {
    "database": "kết nối thành công"
  }
