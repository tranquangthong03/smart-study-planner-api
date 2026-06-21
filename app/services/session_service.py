from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.study_session import StudySessionCreate
from app.models.study_task import StudyTask
from app.models.topic import Topic
from app.models.study_goal import StudyGoal
from app.models.study_session import StudySession
def create_session(db: Session, session_in: StudySessionCreate, user_id: int) -> StudySession:
    """
    Tạo phiên học mới (Bắt đầu học).
    Yêu cầu task_id phải hợp lệ và thuộc về user_id (Deep Ownership).
    """
    # 1. Validate Deep Ownership (Task -> Topic -> Goal -> User)
    # Dùng JOIN để nối bảng Task -> Topic -> StudyGoal để lấy user_id
    task = db.query(StudyTask).join(Topic).join(StudyGoal).filter(
        user_id == StudyGoal.user_id, # Kiểm tra xem user_id có tồn tại hay không
        StudyTask.id == session_in.task_id # Kiểm tra session có nằm trong task đó hay không 
    ).first()

    if not task:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Task not found" # Trả 404 để bảo mật
      )
    # 2. Tạo Session
    # Nhờ default_factory=datetime.now ở Schema, nếu client không gửi started_at, 
    # Pydantic sẽ tự động lấy giờ server.
    db_session = StudySession(**session_in.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session