from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.study_goal import StudyGoal
from app.models.study_session import StudySession
from app.models.study_task import StudyTask
from app.models.topic import Topic
from app.schemas.study_session import StudySessionCreate, StudySessionUpdate


def create_session(db: Session, session_in: StudySessionCreate, user_id: int) -> StudySession:
    """
    Tạo phiên học mới (Bắt đầu học).
    Yêu cầu task_id phải hợp lệ và thuộc về user_id (Deep Ownership).
    """
    task = db.query(StudyTask).join(Topic).join(StudyGoal).filter(
        StudyTask.id == session_in.task_id,
        StudyGoal.user_id == user_id,
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    db_session = StudySession(**session_in.model_dump())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return db_session


def get_session_or_404(db: Session, user_id: int, session_id: int) -> StudySession:
    db_session = db.query(StudySession).join(StudyTask).join(Topic).join(StudyGoal).filter(
        StudySession.id == session_id,
        StudyGoal.user_id == user_id,
    ).first()

    if not db_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return db_session


def get_sessions(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    task_id: Optional[int] = None,
) -> List[StudySession]:
    query = db.query(StudySession).join(StudyTask).join(Topic).join(StudyGoal).filter(
        StudyGoal.user_id == user_id,
    )
    if task_id is not None:
        query = query.filter(StudySession.task_id == task_id)

    return query.offset(skip).limit(limit).all()


def update_session(db: Session, user_id: int, session_id: int, session_in: StudySessionUpdate) -> StudySession:
    db_session = get_session_or_404(db, user_id, session_id)

    update_data = session_in.model_dump(exclude_unset=True)

    ended_at = update_data.get("ended_at")
    if ended_at is not None:
        if ended_at < db_session.started_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ended_at cannot be earlier than started_at",
            )
        db_session.ended_at = ended_at
        time_diff = ended_at - db_session.started_at
        db_session.duration_minutes = int(time_diff.total_seconds() / 60)

    if "note" in update_data:
        db_session.note = update_data["note"]

    db.commit()
    db.refresh(db_session)

    return db_session


def delete_session(db: Session, user_id: int, session_id: int) -> None:
    db_session = get_session_or_404(db, user_id, session_id)
    db.delete(db_session)
    db.commit()
