from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, datetime

from app.models.review_schedule import ReviewSchedule
from app.models.study_task import StudyTask
from app.models.topic import Topic
from app.models.study_goal import StudyGoal
from app.schemas.review_schedule import ReviewScheduleCreate, ReviewScheduleUpdate, ReviewStatus

def create_review_schedule(
    db: Session,
    user_id: int,
    schedule_in : ReviewScheduleCreate,
) -> ReviewSchedule:
  # Kiểm tra task_id, user có hợp lệ hay không 
  task = db.query(StudyTask).join(Topic).join(StudyGoal).filter(
    StudyTask.id == schedule_in.task_id,
    user_id == StudyGoal.user_id
  )

  if not task:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Task not found"
    )
  
  db_schedule = ReviewSchedule(**schedule_in.model_dump())
  db.add(db_schedule)
  db.commit()
  db.refresh(db_schedule)

  return db_schedule

def get_schedule_or_404(db: Session, user_id: int, schedule_id: int):
  schedule = db.query(ReviewSchedule).join(StudyTask).join(Topic).join(StudyGoal).filter(
    user_id == StudyGoal.user_id,
    schedule_id == ReviewSchedule.id
  ).first()

  if not schedule:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Review schedule not found"
    )
  
  return schedule

def get_review_schedules(db: Session, task_id: Optional[int], user_id: int, skip: int = 0, limit: int = 100, review_date: Optional[date] = None) -> List[ReviewSchedule]:
  """
  Lấy danh sách Lịch ôn tập. Hỗ trợ lọc theo task_id hoặc review_date.
  """

  # Xác định user có hợp lệ hay không
  query = db.query(ReviewSchedule).join(StudyTask).join(Topic).join(StudyGoal).filter(
    user_id == StudyGoal.user_id
  )

  if task_id:
    query = query.filter(
      StudyTask.id == task_id
    )
  # Logic lọc theo ngày (Ví dụ: Lấy tất cả bài cần ôn trong ngày hôm nay)
  if review_date:
    query = query.filter(review_date == ReviewSchedule.review_date)

  return query.offset(skip).limit(limit).all()

def update_review_schedule(db: Session, schedule_id: int, schedule_in: ReviewScheduleUpdate, user_id: int) -> ReviewSchedule:
  """
  Cập nhật Lịch ôn tập. Tự động xử lý completed_at dựa vào status.
  """
  db_schedule  = get_schedule_or_404(
    db=db,
    user_id = user_id,
    schedule_id=schedule_id
  )
  update_data = schedule_in.model_dump(exclude_unset=True)

# Xử lý Business Logic: Tự động cập nhật completed_at
  if "status" in update_data:
    if update_data["status"] == ReviewStatus.COMPLETED:
      # Cập nhật db_schedule hiện tại bằng thời gian hiện tại
      db_schedule.completed_at = datetime.now()
    else: # Nếu chuyển về pending hoặc missed thì xóa thời gian hoàn thành
      db_schedule.completed_at = None

  # Cập nhật các trường còn lại
  for field, value in update_data.items():
    setattr(db_schedule, field, value)

  db.commit()
  db.refresh()

  return db_schedule

def delete_review_schedule(db: Session, schedule_id: int, user_id: int) -> None:
    """Xóa Lịch ôn tập"""
    db_schedule = get_schedule_or_404(db, schedule_id, user_id)
    db.delete(db_schedule)
    db.commit()