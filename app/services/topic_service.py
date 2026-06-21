from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.topic import Topic
from app.schemas.topic import TopicCreate, TopicUpdate
from app.services.helpers import get_goal_or_404
from typing import List, Optional
from app.models.study_goal import StudyGoal

def create_topic(
    db: Session,
    topic_in: TopicCreate,
    user_id: int
) -> Topic:
  # Kiểm tra goal và user_id phải tồn tại
  goal = get_goal_or_404(
    db=db,
    user_id=user_id,
    goal_id=topic_in.goal_id
  )

  # Nếu pass qua được thì tiến hành tạo topic mới
  new_topic = Topic(**topic_in.model_dump())

  db.add(new_topic)
  db.commit()
  db.refresh(new_topic)

  return new_topic

def get_topic_or_404(
    db: Session,
    topic_id: int,
    user_id: int
) -> Topic:
  """
  Helper function: Tìm Topic và kiểm tra quyền sở hữu lồng nhau (Nested Ownership).
  """
  # Dùng JOIN để nối bảng Topic và StudyGoal
  topic = db.query(Topic).join(StudyGoal).filter(
    topic_id == Topic.id,
    user_id == StudyGoal.user_id
  ).first()

  if not topic:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Topic not found"
    )
  
  return topic

# Lấy tất cả các topic của studygoal
def get_topics(
  db: Session,
  user_id: int,
  goal_id: Optional[int] = None,
  skip: int = 0,
  limit: int = 100
) -> List[Topic]:
    """
    Lấy danh sách Topic của user. Có thể lọc theo goal_id.
    """
    # Luôn luôn phải JOIN và filter theo user_id để bảo mật
    # Lấy toàn bộ topic của tất cả các goal
    topics = db.query(Topic).join(StudyGoal).filter(
       user_id == StudyGoal.user_id,
    )
    # Nếu client muốn lọc theo một goal id nhất định
    if goal_id:
       topics = topics.filter(Topic.goal_id == goal_id)
    
    # Bỏ qua skip và lấy limit số lượng bảng ghi
    return topics.offset(skip).limit(limit).all()

def update_topic(
  db: Session,
  user_id: int,
  topic_id: int,
  topic_in: TopicUpdate
):
   # lấy ra topic cần update
    topic = get_topic_or_404(
        db=db,
        user_id=user_id,
        topic_id=topic_id
    )
    # 2. Cập nhật các trường được gửi lên
    # exclude_unset=True rất quan trọng trong PATCH: chỉ lấy những trường client thực sự gửi
    update_data = topic_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
       setattr(topic, field, value)

    db.commit()
    db.refresh(topic)

    return topic

def delete_topic(
      db: Session,
      user_id: int,
      topic_id: int
):
   # lấy ra topic cần xóa nếu không có thì báo lỗi
   delete_topic = get_topic_or_404(
      db=db,
      user_id=user_id,
      topic_id=topic_id
   )

   # Thực hiện xóa trong cơ sở dữ liệu
   db.delete(delete_topic)
   db.commit() # Lưu sự thay đổi