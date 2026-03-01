from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section
from app.models.question import Question
from app.models.progress import StudentProgress
from app.models.favorite import Favorite

router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# GET STAGES
# =========================
@router.get("/stages")
def get_stages(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return db.query(Stage).all()


# =========================
# GET SUBJECTS
# =========================
@router.get("/subjects/{stage_id}")
def get_subjects(stage_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    return db.query(Subject).filter(
        Subject.stage_id == stage_id
    ).all()


# =========================
# GET CHAPTERS
# =========================
@router.get("/chapters/{subject_id}")
def get_chapters(subject_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    return db.query(Chapter).filter(
        Chapter.subject_id == subject_id
    ).all()


# =========================
# GET SECTIONS
# =========================
@router.get("/sections/{chapter_id}")
def get_sections(chapter_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    return db.query(Section).filter(
        Section.chapter_id == chapter_id
    ).all()


# =========================
# GET QUESTIONS
# =========================
@router.get("/questions/{section_id}")
def get_questions(section_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    return db.query(Question).filter(
        Question.section_id == section_id
    ).all()


# =========================
# SOLVE QUESTION (Progress)
# =========================
@router.post("/solve/{question_id}")
def solve_question(question_id: int,
                   is_correct: bool,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    # نجيب السؤال أولاً
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # نبحث عن تقدم الطالب على مستوى السيكشن
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.section_id == question.section_id
    ).first()

    # إذا ما موجود سجل تقدم
    if not progress:
        progress = StudentProgress(
            user_id=current_user.id,
            section_id=question.section_id,
            is_completed=True,
            correct_answers=1 if is_correct else 0,
            wrong_answers=0 if is_correct else 1
        )
        db.add(progress)
    else:
        # تحديث الإحصائيات
        if is_correct:
            progress.correct_answers += 1
        else:
            progress.wrong_answers += 1

        progress.is_completed = True

    db.commit()

    return {"message": "Progress saved successfully"}
