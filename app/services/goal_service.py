# Nơi xử lý logic để đưa vào phần router trong api/v1
# Yêu cầu của mentor: Người dùng đã đăng nhập mới được tạo Goal. -> phải get current user
from fastapi import HTTPException
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.study_goal import StudyGoal
from app.schemas.study_goal import StudyGoalCreate, StudyGoalUpdate
from sqlalchemy.orm import Session
from app.services.helpers import get_goal_or_404

# Tạo goal mới
def create_goal(
    db: Session,
    user: User,
    goal_data: StudyGoalCreate
):
  goal = StudyGoal(
    **goal_data.model_dump(),
    user_id=user.id # gán goal đúng với user đó
  )

  db.add(goal)
  db.commit()
  db.refresh(goal)

  return goal

# Get Goals

def get_goals(
    db: Session,
    user: User
):
  goals = (
    db.query(StudyGoal)
    .filter(user.id == StudyGoal.user_id)
    .order_by(StudyGoal.created_at.desc()) # Tìm trong bảng StudyGoal các id trùng với user id
    .all() # lấy tất cả
  )

  return goals # Trả về danh sách các StudyGoal fastAPI tự convert thành StudyGoalResponse

def goal_detail(
    db: Session,
    user: User,
    goal_id: int
):
  # Tìm trong bảng goals 1 cái goal có id = goal_id và có user_id = user.id
  goal = db.query(StudyGoal).filter(user.id == StudyGoal.user_id, goal_id == StudyGoal.id).first()
  # Nếu không tồn tại goal sẽ trả về None
  if not goal:
    raise HTTPException(
        status_code=404,
        detail="Goal not found"
    )
  return goal

# Update goal
def update_goal(
    db: Session,
    user: User,
    goal_id: int,
    goal_data: StudyGoalUpdate
):
  # Lấy ra đối tượng goal cần update
  goal = get_goal_or_404(
    db=db,
    goal_id=goal_id,
    user_id=user.id
  )

  update_goal = goal_data.model_dump(
    exclude_unset= True
  ) # Chuyển dữ liệu update về dictionary

  for field, value in update_goal.items():
    setattr(goal, field, value) #setattr(đối_tượng, tên_thuộc_tính, giá_trị_mới)

  # Lưu và db
  db.commit()
  db.refresh(goal)

  return goal

# Delete goal
def delete_goal(
    db: Session,
    goal_id: int,
    user: User
):
  # Lấy ra goal cần xóa
  goal = get_goal_or_404(
    db=db,
    user_id=user.id,
    goal_id=goal_id
  )
  db.delete(goal)
  db.commit()

  return {
    "message": "Goal deleted successfully"
  }


