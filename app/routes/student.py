from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db

from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.favorite import Favorite
from app.models.progress import StudentProgress

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
    check_ai_access(db, current_user)

    query = db.query(Question).filter(
        Question.section_id == section_id
    )

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


# =========================
# MARK QUESTION COMPLETED
# =========================
@router.post("/complete/{question_id}")
def mark_question_completed(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        return {"error": "Question not found"}

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


# =========================
# GET PROGRESS
# =========================
@router.get("/progress/{section_id}")
def get_progress(
    section_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    total_questions = db.query(Question).filter(
        Question.section_id == section_id
    ).count()

    completed = db.query(StudentProgress).join(Question).filter(
        StudentProgress.user_id == current_user.id,
        Question.section_id == section_id
    ).count()

    percentage = 0
    if total_questions > 0:
        percentage = (completed / total_questions) * 100

    return {
        "total_questions": total_questions,
        "completed": completed,
        "progress_percentage": round(percentage, 2)
    }


# =========================
# FAVORITES
# =========================

@router.post("/favorite/{question_id}")
def add_favorite(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()

    if existing:
        return {"message": "Already in favorites"}

    favorite = Favorite(
        user_id=current_user.id,
        question_id=question_id
    )

    db.add(favorite)
    db.commit()

    return {"message": "Added to favorites"}


@router.delete("/favorite/{question_id}")
def remove_favorite(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()

    if not favorite:
        return {"message": "Not in favorites"}

    db.delete(favorite)
    db.commit()

    return {"message": "Removed from favorites"}


@router.get("/favorites")
def get_my_favorites(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    favorites = (
        db.query(Question)
        .join(Favorite, Favorite.question_id == Question.id)
        .filter(Favorite.user_id == current_user.id)
        .all()
    )

    return favorites
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.question import Question
from app.models.progress import StudentProgress
from app.core.security import get_current_user

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/progress/{section_id}")
def get_section_progress(
    section_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # كل اسئلة السكشن
    total_questions = db.query(Question).filter(
        Question.section_id == section_id
    ).count()

    # كل تقدم الطالب بهالسكشن
    progress = db.query(StudentProgress).join(Question).filter(
        StudentProgress.user_id == current_user.id,
        Question.section_id == section_id
    )

    solved_questions = progress.count()

    correct_answers = progress.filter(
        StudentProgress.is_correct == True
    ).count()

    wrong_answers = progress.filter(
        StudentProgress.is_correct == False
    ).count()

    success_rate = 0
    if total_questions > 0:
        success_rate = round((correct_answers / total_questions) * 100, 2)

    return {
        "total_questions": total_questions,
        "solved_questions": solved_questions,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "success_rate": success_rate
