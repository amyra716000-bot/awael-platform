from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access

router = APIRouter(prefix="/ai", tags=["AI"])


# ==========================================
# ASK AI
# ==========================================
@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    question = question.strip()

    if len(question) < 3:
        raise HTTPException(
            status_code=400,
            detail="Question too short"
        )

    if len(question) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Question too long"
        )

    # ==========================================
    # CHECK SUBSCRIPTION
    # ==========================================
    subscription, plan, remaining = check_ai_access(db, current_user)

    # ==========================================
    # AI RESPONSE (MOCK MODE)
    # ==========================================
    ai_answer = f"🤖 AI (Mock Mode): سؤالك كان: {question}"

    # ==========================================
    # UPDATE USAGE
    # ==========================================
    if subscription:
        subscription.ai_used_today += 1
    else:
        current_user.free_ai_used += 1

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining - 1,
        "mode": "mock"
    }
