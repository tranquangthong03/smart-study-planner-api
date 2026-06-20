from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.services import goal_service
from app.core.dependencies import get_current_user
from app.schemas.study_goal import StudyGoalCreate, StudyGoalResponse, StudyGoalUpdate
router = APIRouter(
  prefix="/goals",
  tags=["Goals"]
)

@router.post(
  "",
  response_model=StudyGoalResponse,
  status_code=status.HTTP_201_CREATED,
)
def create_goal(
  goal_data: StudyGoalCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return goal_service.create_goal(
    db=db,
    user=current_user,
    goal_data=goal_data
  )

@router.get("", response_model=list[StudyGoalResponse])
def get_goals(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return goal_service.get_goals(
    db=db,
    user=current_user
  )

@router.get("/{goal_id}", response_model=StudyGoalResponse)
def goal_detail(
  goal_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return goal_service.goal_detail(
    db=db,
    goal_id=goal_id,
    user=current_user
  )
# Update goal

@router.patch("/{goal_id}", response_model=StudyGoalResponse)
def update_goal(
    goal_id: int,
    goal_data: StudyGoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
  return goal_service.update_goal(
    db=db,
    user=current_user,
    goal_id=goal_id,
    goal_data=goal_data
  )

@router.delete("/{goal_id}")
def delete_goal(
  goal_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
):
  return goal_service.delete_goal(
    db=db,
    goal_id=goal_id,
    user=current_user
  )