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
    result = check_ai_access(db, current_user)

    # إذا رجعت None أو False
    if not result:
        raise HTTPException(status_code=403, detail="No AI access")

    # إذا رجعت tuple (اشتراك + خطة)
    if isinstance(result, tuple):
        subscription, plan = result
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        # وضع مجاني (3 اسئلة مثلاً)
        current_user.free_ai_used += 1
        remaining = 3 - current_user.free_ai_used

    db.commit()

    ai_answer = f"🤖 AI (Mock Mode): سؤالك كان: {question}"

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining,
        "mode": "mock"
    }
