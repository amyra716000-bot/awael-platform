from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.exam_template import ExamType


# =========================
# Create Exam Template
# =========================
class ExamTemplateCreate(BaseModel):
    name: str
    type: ExamType

    stage_id: int
    subject_id: Optional[int] = None
    section_id: Optional[int] = None

    total_questions: int = Field(gt=0)
    duration_minutes: int = Field(gt=0)

    passing_score: int = Field(default=50, ge=0, le=100)

    is_active: bool = True
    end_date: Optional[datetime] = None

    attempt_limit: int = 1
    is_paid: bool = True

    randomize_questions: bool = True
    randomize_options: bool = True

    leaderboard_enabled: bool = True
    show_answers_after_finish: bool = False


# =========================
# Update Exam Template
# =========================
class ExamTemplateUpdate(BaseModel):
    name: Optional[str] = None
    total_questions: Optional[int] = Field(default=None, gt=0)
    duration_minutes: Optional[int] = Field(default=None, gt=0)
    passing_score: Optional[int] = Field(default=None, ge=0, le=100)

    is_active: Optional[bool] = None
    end_date: Optional[datetime] = None

    attempt_limit: Optional[int] = None
    is_paid: Optional[bool] = None

    randomize_questions: Optional[bool] = None
    randomize_options: Optional[bool] = None

    leaderboard_enabled: Optional[bool] = None
    show_answers_after_finish: Optional[bool] = None


# =========================
# Response
# =========================
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
        from_attributes = True
