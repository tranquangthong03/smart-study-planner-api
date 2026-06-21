from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from typing import List, Optional
from datetime import datetime

from app.models.topic import Topic
from app.models.study_goal import StudyGoal
from app.models.study_task import StudyTask
from app.schemas.study_task import StudyTaskCreate, StudyTaskUpdate, TaskStatus
def create_task(
    db: Session,
    user_id: int,
    task_in: StudyTaskCreate
) -> StudyTask:
    """
    Tạo Task mới. Yêu cầu topic_id phải hợp lệ và thuộc về user_id (Deep Ownership).
    """
    # 1. Validate Deep Ownership (Task -> Topic -> Goal -> User)
    # Dùng JOIN để nối bảng Topic với StudyGoal, từ đó mới có user_id để check
    topic = db.query(Topic).join(StudyGoal).filter(
        Topic.id == task_in.topic_id,
        StudyGoal.user_id == user_id
    ).first()

    if not topic:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Topic not found" # Trả 404 để không tiết lộ Topic của người khác
      )
    
    # Tạo task
    new_task = StudyTask(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_task_or_404(db: Session, task_id: int, user_id: int) -> StudyTask:
    """
    Helper function: Tìm Task và kiểm tra quyền sở hữu lồng nhau 2 tầng (Deep Ownership).
    """
    # JOIN 2 vòng: StudyTask -> Topic -> StudyGoal
    task = db.query(StudyTask).join(Topic).join(StudyGoal).filter(
        StudyTask.id == task_id,
        StudyGoal.user_id == user_id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

def get_tasks(
    db: Session,
    user_id: int,
    topic_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[StudyTask]:
    """
    Lấy danh sách Task của user. Có thể lọc theo topic_id.
    """
    tasks = db.query(StudyTask).join(Topic).join(StudyGoal).filter(
        StudyGoal.user_id == user_id
    )
    # Nếu muốn tìm theo task thì
    if topic_id:
        tasks = tasks.filter(topic_id == Topic.id)
    return tasks.offset(skip).limit(limit).all()

def update_task(
    db: Session,
    user_id: int,
    task_id: int,
    task_in: StudyTaskUpdate
) -> StudyTask:
    # Kiểm tra task có tồn tại hay không
    task = get_task_or_404(
        db=db,
        user_id= user_id,
        task_id = task_id
    )

    update_task = StudyTask(**task_in.model_dump(exclude_unset=True))
     # Xử lý Business Logic: Tự động cập nhật completed_at dựa vào status
    if "status" in update_task:
        # Nếu status là đã hoàn thành thì tự động cập nhật completed_at của task cần chỉnh sửa
        if update_task["status"] == TaskStatus.DONE:
            task.completed_at = datetime.now()
    # Cập nhật các trường dữ liệu còn lại
    for field, value in update_task.item():
        setattr(task, field, value)
    
    # Lưu thay đổi vào cơ sở dữ liệu
    db.commit()
    db.refresh(task)

    return task

# Delete task
def delete_task(
    db: Session,
    user_id: int,
    task_id: int
) -> None:
    task = get_task_or_404(db=db, user_id=user_id, task_id=task_id)
    # Nếu pass được thì thực hiện xóa task
    db.delete(task)
    db.commit()
    