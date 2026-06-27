from fastapi import APIRouter, status, Depends, Query

from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.user import User
from app.schemas.study_task import StudyTaskResponse, StudyTaskCreate, StudyTaskUpdate
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.services.task_service import create_task as create_task_service, get_tasks as get_tasks_service, get_task_or_404, update_task as update_task_service, delete_task as delete_task_service
router = APIRouter()

@router.post("/", response_model=StudyTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
  task_in: StudyTaskCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return create_task_service(task_in=task_in, db=db, user_id=current_user.id)

@router.get("/", response_model=List[StudyTaskResponse])
def get_tasks(
  topic_id: Optional[int] = Query(None, description="Lọc Task theo Topic ID"),
  skip: int = Query(0, ge=0, description="Bỏ qua N bản ghi đầu tiên"),
  limit: int = Query(100, ge=1, le=100, description="Số lượng bản ghi tối đa"),
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return get_tasks_service(topic_id=topic_id, skip=skip, limit=limit, db=db, user_id=current_user.id)

@router.get("/{task_id}", response_model=StudyTaskResponse)
def get_task(
  task_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return get_task_or_404(db=db, task_id=task_id, user_id=current_user.id)

@router.patch("/{task_id}", response_model=StudyTaskResponse)
def update_task(
  task_id: int,
  task_in: StudyTaskUpdate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return update_task_service(db=db, task_id=task_id, task_in=task_in, user_id=current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
  return delete_task_service(task_id=task_id, db=db, user_id=current_user.id)