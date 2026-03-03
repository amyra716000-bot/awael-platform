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
    # فحص الاشتراك وحدود الاستخدام
    subscription, plan = check_ai_access(db, current_user)

    # رد تجريبي (Mock)
    ai_answer = f"🤖 AI (Mock Mode): سؤالك كان: {question}"

    # زيادة العداد
    if subscription:
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        # وضع مجاني (اذا عندك مستخدم مجاني)
        if current_user.free_ai_used >= 3:
            raise HTTPException(status_code=403, detail="Free AI limit reached")

        current_user.free_ai_used += 1
        remaining = 3 - current_user.free_ai_used

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining,
        "mode": "mock"
    }
