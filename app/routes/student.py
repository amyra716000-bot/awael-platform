from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/stages")
def get_stages(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Stage).all()


@router.get("/subjects/{stage_id}")
def get_subjects(
    stage_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Subject).filter(Subject.stage_id == stage_id).all()


@router.get("/chapters/{subject_id}")
def get_chapters(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Chapter).filter(Chapter.subject_id == subject_id).all()


@router.get("/sections/{chapter_id}")
def get_sections(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Section).filter(Section.chapter_id == chapter_id).all()


@router.get("/questions/{section_id}")
def get_questions(
    section_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # هنا نفحص الاشتراك
    subscription, plan = check_ai_access(db, current_user)

    return db.query(Question).filter(Question.section_id == section_id).all()
