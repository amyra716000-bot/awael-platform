from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
import os


FREE_AI_LIMIT = int(os.getenv("FREE_AI_LIMIT", 3))


# ==========================================
# فحص الاشتراك العام
# ==========================================
def get_active_subscription(db: Session, user: User):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        return None, None

    # إذا منتهي
    if subscription.end_date < datetime.utcnow():
        subscription.is_active = False
        db.commit()
        return None, None

    plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    if not plan:
        return None, None

    return subscription, plan


# ==========================================
# فحص AI Usage
# ==========================================
def check_ai_access(db: Session, user: User):
    subscription, plan = get_active_subscription(db, user)

    # ====== إذا عنده اشتراك ======
    if subscription and plan:

        # تصفير يومي
        today = datetime.utcnow().date()
        if subscription.last_reset_date.date() != today:
            subscription.ai_used_today = 0
            subscription.last_reset_date = datetime.utcnow()
            db.commit()

        if plan.daily_ai_limit <= 0:
            raise HTTPException(
                status_code=403,
                detail="AI access not allowed in this plan"
            )

        if subscription.ai_used_today >= plan.daily_ai_limit:
            raise HTTPException(
                status_code=403,
                detail="Daily AI limit reached"
            )

        remaining = plan.daily_ai_limit - subscription.ai_used_today
        return subscription, plan, remaining

    # ====== Free Mode ======
    if user.free_ai_used is None:
        user.free_ai_used = 0
        db.commit()

    if user.free_ai_used >= FREE_AI_LIMIT:
        raise HTTPException(
            status_code=403,
            detail="Free limit reached. Please subscribe."
        )

    remaining = FREE_AI_LIMIT - user.free_ai_used
    return None, None, remaining
