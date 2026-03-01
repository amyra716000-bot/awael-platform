from fastapi import APIRouter, Depends, HTTPException
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
    SolveResponse,
    SectionProgressResponse,
    DashboardResponse
)

router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# GET STAGES
# =========================
@router.get("/stages", response_model=List[StageOut])
def get_stages(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return db.query(Stage).all()


# =========================
# GET SUBJECTS
# =========================
@router.get("/subjects/{stage_id}", response_model=List[SubjectOut])
def get_subjects(stage_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return db.query(Subject).filter(
        Subject.stage_id == stage_id
    ).all()


# =========================
# GET CHAPTERS
# =========================
@router.get("/chapters/{subject_id}", response_model=List[ChapterOut])
def get_chapters(subject_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return db.query(Chapter).filter(
        Chapter.subject_id == subject_id
    ).all()


# =========================
# GET SECTIONS
# =========================
@router.get("/sections/{chapter_id}", response_model=List[SectionOut])
def get_sections(chapter_id: int,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return db.query(Section).filter(
        Section.chapter_id == chapter_id
    ).all()


# =========================
# GET QUESTIONS
# =========================
@router.get("/questions/{section_id}", response_model=List[QuestionOut])
def get_questions(section_id: int,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    return db.query(Question).filter(
        Question.section_id == section_id
    ).all()


# =========================
# SOLVE QUESTION
# =========================
@router.post("/solve/{question_id}", response_model=SolveResponse)
def solve_question(question_id: int,
                   is_correct: bool,
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.section_id == question.section_id
    ).first()

    if progress is None:
        progress = StudentProgress(
            user_id=current_user.id,
            section_id=question.section_id,
            correct_answers=1 if is_correct else 0,
            total_attempts=1
        )
        db.add(progress)
    else:
        progress.total_attempts += 1
        if is_correct:
            progress.correct_answers += 1

    db.commit()

    return {
        "message": "Progress saved successfully",
        "total_attempts": progress.total_attempts,
        "correct_answers": progress.correct_answers
    }


# =========================
# SECTION PROGRESS
# =========================
@router.get("/progress/{section_id}", response_model=SectionProgressResponse)
def get_section_progress(section_id: int,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):

    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.section_id == section_id
    ).first()

    if progress is None:
        return {
            "section_id": section_id,
            "total_attempts": 0,
            "correct_answers": 0,
            "success_rate": 0
        }

    success_rate = (
        int((progress.correct_answers / progress.total_attempts) * 100)
        if progress.total_attempts > 0 else 0
    )

    return {
        "section_id": section_id,
        "total_attempts": progress.total_attempts,
        "correct_answers": progress.correct_answers,
        "success_rate": success_rate
    }


# =========================
# DASHBOARD
# =========================
@router.get("/dashboard", response_model=DashboardResponse)
def student_dashboard(db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):

    progresses = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id
    ).all()

    if not progresses:
        return {
            "total_attempts": 0,
            "total_correct": 0,
            "overall_success_rate": 0,
            "sections_count": 0,
            "strongest_section": None,
            "weakest_section": None
        }

    total_attempts = sum(p.total_attempts for p in progresses)
    total_correct = sum(p.correct_answers for p in progresses)

    overall_success_rate = (
        int((total_correct / total_attempts) * 100)
        if total_attempts > 0 else 0
    )

    strongest = max(
        progresses,
        key=lambda p: (p.correct_answers / p.total_attempts)
        if p.total_attempts > 0 else 0
    )

    weakest = min(
        progresses,
        key=lambda p: (p.correct_answers / p.total_attempts)
        if p.total_attempts > 0 else 0
    )

    return {
        "total_attempts": total_attempts,
        "total_correct": total_correct,
        "overall_success_rate": overall_success_rate,
        "sections_count": len(progresses),
        "strongest_section": strongest.section_id,
        "weakest_section": weakest.section_id
    }
