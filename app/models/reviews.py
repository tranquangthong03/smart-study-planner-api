from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.review_schedule import ReviewScheduleCreate, ReviewScheduleUpdate, ReviewScheduleResponse
from app.services import review_service

router = APIRouter()

@router.post("/", response_model=ReviewScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_review_schedule(
    schedule_in: ReviewScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Tạo lịch ôn tập mới (Bắt buộc truyền task_id và review_date)"""
    return review_service.create_review_schedule(db=db, schedule_in=schedule_in, user_id=current_user.id)

@router.get("/", response_model=List[ReviewScheduleResponse])
def get_review_schedules(
    task_id: Optional[int] = Query(None, description="Lọc theo Task ID"),
    review_date: Optional[date] = Query(None, description="Lọc theo ngày ôn tập (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0, description="Bỏ qua N bản ghi đầu tiên"),
    limit: int = Query(100, ge=1, le=100, description="Số lượng bản ghi tối đa"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy danh sách lịch ôn tập của current user"""
    return review_service.get_review_schedules(
        db=db, user_id=current_user.id, task_id=task_id, review_date=review_date, skip=skip, limit=limit
    )

@router.get("/{schedule_id}", response_model=ReviewScheduleResponse)
def get_review_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lấy chi tiết 1 lịch ôn tập"""
    return review_service.get_schedule_or_404(db=db, schedule_id=schedule_id, user_id=current_user.id)

@router.patch("/{schedule_id}", response_model=ReviewScheduleResponse)
def update_review_schedule(
    schedule_id: int,
    schedule_in: ReviewScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cập nhật lịch ôn tập (Tự động cập nhật completed_at khi status=completed)"""
    return review_service.update_review_schedule(db=db, schedule_id=schedule_id, schedule_in=schedule_in, user_id=current_user.id)

@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Xóa lịch ôn tập"""
    review_service.delete_review_schedule(db=db, schedule_id=schedule_id, user_id=current_user.id)