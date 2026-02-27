from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.question import Question
from app.models.content_view import ContentView
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

    # تحقق إذا أكو سجل سابق
    view = db.query(ContentView).filter(
        ContentView.user_id == current_user.id,
        ContentView.content_id == question_id
    ).first()

    if not view:
        view = ContentView(
            user_id=current_user.id,
            content_id=question_id,
            views_count=1,
            last_viewed_at=datetime.utcnow()
        )
        db.add(view)
    else:
        view.views_count += 1
        view.last_viewed_at = datetime.utcnow()

    db.commit()

    return question
