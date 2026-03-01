from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.exam_template import ExamType


class ExamTemplateCreate(BaseModel):
    name: str
    type: ExamType

    stage_id: int
    subject_id: Optional[int] = None
    section_id: Optional[int] = None

    total_questions: int
    duration_minutes: int
    passing_score: int = 50

    is_active: bool = True
    end_date: Optional[datetime] = None

    attempt_limit: int = 1
    is_paid: bool = True

    randomize_questions: bool = True
    randomize_options: bool = True

    leaderboard_enabled: bool = True
    show_answers_after_finish: bool = False


class ExamTemplateResponse(BaseModel):
    id: int
    name: str
    type: ExamType

    stage_id: int
    subject_id: Optional[int]
    section_id: Optional[int]

    total_questions: int
    duration_minutes: int
    passing_score: int

    is_active: bool
    start_date: datetime
    end_date: Optional[datetime]

    attempt_limit: int
    is_paid: bool

    randomize_questions: bool
    randomize_options: bool

    leaderboard_enabled: bool
    show_answers_after_finish: bool

    class Config:
        orm_mode = True
