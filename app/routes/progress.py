from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import get_current_user
from app.models.progress import StudentProgress
from app.models.question import Question
from app.models.user import User

router = APIRouter(prefix="/student", tags=["Student - Progress"])


@router.post("/solve/{question_id}")
def solve_question(
    question_id: int,
    is_correct: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # نتأكد السؤال موجود
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # نشوف إذا الطالب حل السؤال سابقاً
    existing = db.query(StudentProgress).filter(
        StudentProgress.user_id == current_user.id,
        StudentProgress.question_id == question_id
    ).first()

    if existing:
        # إذا موجود نحدثه
        existing.is_correct = is_correct
        db.commit()
        return {"message": "Progress updated"}

    # إذا ما موجود ننشئ سجل جديد
    progress = StudentProgress(
        user_id=current_user.id,
        question_id=question_id,
        is_completed=True,
        is_correct=is_correct
    )

    db.add(progress)
    db.commit()

    return {"message": "Progress saved successfully"}
