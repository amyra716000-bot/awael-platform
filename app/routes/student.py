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
