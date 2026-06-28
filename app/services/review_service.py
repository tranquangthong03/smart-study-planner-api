from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.review_schedule import ReviewSchedule
from app.models.study_task import StudyTask
from app.models.topic import Topic
from app.models.study_goal import StudyGoal
from app.schemas.review_schedule import ReviewScheduleCreate