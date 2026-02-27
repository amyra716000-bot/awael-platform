from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access
from app.models.user import User

router = APIRouter(prefix="/ai", tags=["AI"])

FREE_LIMIT = 5


@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 🔎 فحص الاشتراك أو الوضع المجاني
    subscription, plan = check_ai_access(db, current_user)

    # 🤖 هنا لاحقاً نربط OpenAI
    ai_answer = f"AI response to: {question}"

    # 🔢 تحديث العداد
    if subscription:
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        current_user.free_ai_used += 1
        remaining = FREE_LIMIT - current_user.free_ai_used

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining
    }
