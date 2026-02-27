from fastapi import APIRouter, Depends, Query
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


# =========================
# GET STAGES
# =========================
@router.get("/stages")
def get_stages(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Stage).all()


# =========================
# GET SUBJECTS BY STAGE
# =========================
@router.get("/subjects/{stage_id}")
def get_subjects(
    stage_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Subject).filter(
        Subject.stage_id == stage_id
    ).all()


# =========================
# GET CHAPTERS BY SUBJECT
# =========================
@router.get("/chapters/{subject_id}")
def get_chapters(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Chapter).filter(
        Chapter.subject_id == subject_id
    ).all()


# =========================
# GET SECTIONS BY CHAPTER
# =========================
@router.get("/sections/{chapter_id}")
def get_sections(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(Section).filter(
        Section.chapter_id == chapter_id
    ).all()


# =========================
# GET QUESTIONS (Protected + Pagination + Filters)
# =========================
@router.get("/questions/{section_id}")
def get_questions(
    section_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    is_ministry: bool | None = Query(None),
    is_important: bool | None = Query(None),
    ministry_year: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # 🔒 فحص الاشتراك
    check_ai_access(db, current_user)

    query = db.query(Question).filter(
        Question.section_id == section_id
    )

    # ===== Filters =====
    if is_ministry is not None:
        query = query.filter(Question.is_ministry == is_ministry)

    if is_important is not None:
        query = query.filter(Question.is_important == is_important)

    if ministry_year is not None:
        query = query.filter(Question.ministry_year == ministry_year)

    total = query.count()

    questions = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": questions
    }
from app.models.progress import StudentProgress


@router.post("/complete/{question_id}")
def mark_question_completed(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # نتأكد السؤال موجود
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        return {"error": "Question not found"}

    # نشوف إذا مسجل سابقاً
    existing = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.question_id == question_id
    ).first()

    if existing:
        return {"message": "Already completed"}

    progress = StudentProgress(
        user_id=current_user.id,
        question_id=question_id,
        is_completed=True
    )

    db.add(progress)
    db.commit()

    return {"message": "Question marked as completed"}
