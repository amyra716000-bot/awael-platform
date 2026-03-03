from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # 👇 نستقبل 3 قيم
    subscription, plan, remaining = check_ai_access(db, current_user)

    # جواب تجريبي
    ai_answer = f"🤖 AI (Mock Mode): سؤالك كان: {question}"

    # ===== إذا عنده اشتراك =====
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
