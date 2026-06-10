from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def heal_check():
  return {
    "status": "ok",
    "message": "Smart Study Planner API running"
  }

