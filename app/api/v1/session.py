from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.services import session_service
from app.schemas.study_session import StudySessionCreate, StudySessionResponse, StudySessionUpdate
from app.models.user import User
router = APIRouter()

@router.post("/", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
  session_in: StudySessionCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return session_service.create_session(db=db, session_in=session_in, user_id=current_user.id)

@router.get("/", response_model=List[StudySessionResponse])
def get_sessions(
  task_id: Optional[int] = Query(None, description="Lọc Session theo Task ID"),
  skip: int = Query(0, ge=0, description="Bỏ qua N bản ghi đầu tiên"),
  limit: int = Query(100, ge=1, le=100, description="Số lượng bản ghi tối đa"),
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  # Lấy danh sách các phiên học của user
  return session_service.get_sessions(
    task_id=task_id,
    skip=skip,
    limit=limit,
    db=db,
    user_id=current_user.id
  )

# Lấy ra session, truyền vào session_id
@router.get("/{session_id}", response_model=StudySessionResponse)
def get_session(
  session_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return session_service.get_session_or_404(
    db=db,
    session_id=session_id,
    user_id=current_user.id
  )

# Update session

@router.patch("/{session_id}", response_model=StudySessionResponse)
def update_session(
  session_id: int,
  session_ind: StudySessionUpdate,
  current_user = Depends(get_current_user),
  db: Session = Depends(get_db)
):
   return session_service.update_session(db=db, session_id=session_id, session_in=session_in, user_id=current_user.id)
@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa phiên học"""
    session_service.delete_session(db=db, session_id=session_id, user_id=current_user.id)