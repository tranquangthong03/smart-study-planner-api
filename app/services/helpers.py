from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.study_goal import StudyGoal
from app.models.user import User

def get_goal_or_404(
    db: Session,
    user_id: int,
    goal_id: int
) -> StudyGoal :
  goal = (
    db.query(StudyGoal)
    .filter(
      StudyGoal.user_id == user_id,
      StudyGoal.id == goal_id
    )
    .first()
  )

  if not goal:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Goal not found"
    )

  return goal

