from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.question import Question
from app.core.security import get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/{question_id}")
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
