from fastapi import APIRouter, Depends
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

    # فحص الاشتراك
    subscription, plan = check_ai_access(db, current_user)

    # هنا لاحقاً نربط OpenAI
    ai_answer = f"AI response to: {question}"

    # زيادة العداد
    subscription.ai_used_today += 1
    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": plan.daily_ai_limit - subscription.ai_used_today
    }
