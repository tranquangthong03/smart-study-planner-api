from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Optional
from app.schemas.topic import TopicResponse, TopicCreate, TopicUpdate

from sqlalchemy.orm import Session
from app.services import topic_service
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
router = APIRouter()

@router.post("/", response_model=TopicResponse, status_code = status.HTTP_201_CREATED)
def create_topic(
  topic_in: TopicCreate,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
):
  return topic_service.create_topic(
    db=db,
    topic_in=topic_in,
    user_id=current_user.id
  )

@router.get("/", response_model=List[TopicResponse])
def get_topics(
  goal_id: Optional[int] = Query(None, description="Lọc Topic theo Goal ID"),
  skip: int = Query(0, ge=0, description="Bỏ qua N bản ghi đầu tiên (Pagination)"),
  limit: int = Query(100, ge=1, le=100, description="Số lượng bản ghi tối đa trả về"),
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  return topic_service.get_topics(
    goal_id=goal_id,
    skip=skip,
    limit=limit,
    user_id=current_user.id,
    db=db
  )

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(
  topic_id: int,
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return topic_service.get_topic_or_404(
    db=db,
    user_id=current_user.id,
    topic_id=topic_id
  )

@router.patch("/{topic_id}", response_model=TopicResponse)
def update_topic(
  topic_in: TopicUpdate,
  topic_id: int,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  return topic_service.update_topic(
    db=db,
    user_id=current_user.id,
    topic_id=topic_id,
    topic_in=topic_in
  )

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
  topic_id: int,
  current_user: User = Depends(get_current_user),
  db: Session = Depends(get_db)
):
  return topic_service.delete_topic(db=db, user_id=current_user.id, topic_id=topic_id)