from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.question import Question
from app.models.progress import StudentProgress


router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# SOLVE QUESTION (Progress)
# =========================
@router.post("/solve/{question_id}")
def solve_question(
    question_id: int,
    is_correct: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ التأكد من وجود السؤال
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    # 2️⃣ البحث عن تقدم الطالب في هذا السيكشن
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.section_id == question.section_id
    ).first()

    # 3️⃣ إذا أول محاولة
    if progress is None:
        progress = StudentProgress(
            user_id=current_user.id,
            section_id=question.section_id,
            correct_answers=1 if is_correct else 0,
            total_attempts=1
        )
        db.add(progress)

    # 4️⃣ إذا موجود مسبقاً
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
# GET SECTION PROGRESS
# =========================
@router.get("/progress/{section_id}")
def get_section_progress(
    section_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

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

    success_rate = 0
    if progress.total_attempts > 0:
        success_rate = int(
            (progress.correct_answers / progress.total_attempts) * 100
        )

    return {
        "section_id": section_id,
        "total_attempts": progress.total_attempts,
        "correct_answers": progress.correct_answers,
        "success_rate": success_rate
    }
# =========================
# STUDENT DASHBOARD
# =========================
@router.get("/dashboard")
def student_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

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
