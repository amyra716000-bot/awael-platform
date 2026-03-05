from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.progress import StudentProgress

from app.schemas.student import (
    StageOut,
    SubjectOut,
    ChapterOut,
    SectionOut,
    QuestionOut,
)

router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# GET STAGES
# =========================
@router.get("/stages", response_model=List[StageOut])
def get_stages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Stage).all()


# =========================
# GET SUBJECTS
# =========================
@router.get("/subjects/{stage_id}", response_model=List[SubjectOut])
def get_subjects(
    stage_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Subject).filter(
        Subject.stage_id == stage_id
    ).all()


# =========================
# GET CHAPTERS
# =========================
@router.get("/chapters/{subject_id}", response_model=List[ChapterOut])
def get_chapters(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Chapter).filter(
        Chapter.subject_id == subject_id
    ).all()


# =========================
# GET SECTIONS
# =========================
@router.get("/sections/{chapter_id}", response_model=List[SectionOut])
def get_sections(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Section).filter(
        Section.chapter_id == chapter_id
    ).order_by(Section.order).all()


# =========================
# GET QUESTIONS
# =========================
@router.get("/questions/{section_id}", response_model=List[QuestionOut])
def get_questions(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Question).filter(
        Question.section_id == section_id
    ).all()


# =========================
# GLOBAL LEADERBOARD
# =========================
@router.get("/leaderboard")
def leaderboard(
    db: Session = Depends(get_db)
):

    users = (
        db.query(User)
        .order_by(User.xp_points.desc())
        .limit(20)
        .all()
    )

    data = []

    for i, user in enumerate(users):
        data.append({
            "rank": i + 1,
            "email": user.email,
            "xp_points": user.xp_points,
            "level": user.level
        })

    return data
