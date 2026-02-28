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

    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.question_id == question_id
    ).first()

    if not progress:
        progress = StudentProgress(
            user_id=current_user.id,
            question_id=question_id,
            is_completed=True,
            is_correct=is_correct
        )
        db.add(progress)
    else:
        progress.is_completed = True
        progress.is_correct = is_correct

    db.commit()

    return {"message": "Progress saved successfully"}


# =========================
# GET SECTION PROGRESS
# =========================
@router.get("/progress/{section_id}")
def get_section_progress(section_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):

    questions = db.query(Question).filter(
        Question.section_id == section_id
    ).all()

    total = len(questions)

    if total == 0:
        return {
            "total_questions": 0,
            "solved_questions": 0,
            "correct_answers": 0,
            "wrong_answers": 0,
            "success_rate": 0
        }

    solved = db.query(StudentProgress).join(Question).filter(
        StudentProgress.user_id == current_user.id,
        Question.section_id == section_id
    ).all()

    solved_count = len(solved)
    correct = len([s for s in solved if s.is_correct])
    wrong = solved_count - correct

    success_rate = (correct / solved_count) * 100 if solved_count > 0 else 0

    return {
        "total_questions": total,
        "solved_questions": solved_count,
        "correct_answers": correct,
        "wrong_answers": wrong,
        "success_rate": success_rate
    }


# =========================
# ADD FAVORITE
# =========================
@router.post("/favorite/{question_id}")
def add_favorite(question_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):

    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()

    if existing:
        return {"message": "Already added"}

    favorite = Favorite(
        user_id=current_user.id,
        question_id=question_id
    )

    db.add(favorite)
    db.commit()

    return {"message": "Added to favorites"}


# =========================
# REMOVE FAVORITE
# =========================
@router.delete("/favorite/{question_id}")
def remove_favorite(question_id: int,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):

    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.question_id == question_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(favorite)
    db.commit()

    return {"message": "Removed from favorites"}


# =========================
# GET FAVORITES
# =========================
@router.get("/favorites")
def get_favorites(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    favorites = db.query(Favorite).filter(
        Favorite.user_id == current_user.id
    ).all()

    return favorites
