from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from typing import List, Optional
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate
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

def get_session_or_404(db: Session, user_id: int, session_id: int) -> StudySession:
   db_session = db.query(StudySession).join(StudyTask).join(Topic).join(StudyGoal).filter(
      session_id == StudySession.id,
      StudyGoal.id == user_id
   ).first()

   if not db_session:
      raise HTTPException(
          status_code=status.HTTP_404_NOT_FOUND,
          detail="Session not found"
      )
   return db_session

def get_sessions(db: Session, user_id: int, skip: int = 0, limit: int = 100, task_id: Optional[int] = None) -> List[StudySession]:
   # Lấy ra danh sách các session của user
   query = db.query(StudySession).join(StudyTask).join(Topic).join(StudyGoal).filter(
    user_id == StudyGoal.user_id
   )
   if task_id:
    query = query.filter(task_id==StudySession.id)

   return query.offset(skip).limit(limit).all()

def update_session(db: Session, user_id: int, session_id: int, session_in: StudySessionUpdate) -> StudySession:
    db_session = get_session_or_404(db, session_id, user_id) # Lấy ra session đó có tồn tại

    update_data = session_in.model_dump(exclude_unset=True)

    # Xử lý bussines logic: Tính toán thời gian học, nếu người dùng gửi lên sự chỉnh sửa thời gian kết thúc
    if "ended_at" in update_data and update_data["ended"]:
        ended_at = update_data["ended_at"]

        # 1. Validate: ended_at không được diễn ra trước started_at
        # Lưu ý: db_session.started_at có thể là timezone-aware hoặc naive, 
        # nên đảm bảo ended_at client gửi lên cùng định dạng.
        if ended_at < db_session.started_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ended_at cannot be earlier than started_at"
            )
    # 2. Tính toán thời gian duration (phút)
    time_diff = ended_at - db_session.started_at
    duration_minutes = int(time_diff.total_seconds()/60) # Chuyển toàn bộ thành số dây để có thể chuyển thành số phút

    # Gán giá trị vào model
    db_session.ended_at = ended_at
    db_session.duration_minutes = duration_minutes

    # Ended_at đã được xử lý riêng, không cần phải gán lại, xóa để tránh bị lỗi
    del update_data["ended_at"]

    for field, value in update_data.item():
        setattr(db_session, field, value)
    
    # Cập nhật vào dữ liệu
    db.commit()
    db.refresh(db_session)

    return db_session

def delete_session(db: Session, session_id: int, user_id: int):
    db_session = get_session_or_404(db=db, session_id=session_id, user_id=user_id)

    db.delete(db_session)
    db.commit()
    