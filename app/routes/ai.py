from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import check_ai_access
from app.utils.subscription import check_and_update_subscription
from app.models.plan import Plan
from fastapi import HTTPException

router = APIRouter(prefix="/ai", tags=["AI"])


subscription = check_and_update_subscription(db, current_user.id)

if not subscription:
    raise HTTPException(status_code=403, detail="No active subscription")

plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()

if subscription.ai_used_today >= plan.daily_ai_limit:
    
    raise HTTPException(status_code=403, detail="Daily AI limit reached")
@router.post("/ask")
def ask_ai(
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # فحص الاشتراك
    subscription, plan = check_ai_access(db, current_user)

    # رد تجريبي مؤقت
    ai_answer = f"🤖 AI (Mock Mode): سؤالك كان: {question}"

    # زيادة العداد
    if subscription:
        subscription.ai_used_today += 1
        remaining = plan.daily_ai_limit - subscription.ai_used_today
    else:
        current_user.free_ai_used += 1
        remaining = 5 - current_user.free_ai_used

    db.commit()

    return {
        "question": question,
        "answer": ai_answer,
        "remaining_today": remaining,
        "mode": "mock"
    }
