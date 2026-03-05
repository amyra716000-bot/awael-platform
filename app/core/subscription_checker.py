from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
import os

FREE_AI_LIMIT = int(os.getenv("FREE_AI_LIMIT", 3))


# ==========================================
# GET ACTIVE SUBSCRIPTION
# ==========================================
def get_active_subscription(db: Session, user: User):

    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user.id,
            Subscription.is_active == True
        )
        .order_by(Subscription.start_date.desc())
        .first()
    )

    if not subscription:
        return None, None

    now = datetime.utcnow()

    # لم يبدأ الاشتراك بعد
    if subscription.start_date and subscription.start_date > now:
        return None, None

    # انتهى الاشتراك
    if subscription.end_date and subscription.end_date < now:
        subscription.is_active = False
        db.commit()
        return None, None

    plan = subscription.plan

    if not plan:
        return None, None

    return subscription, plan


# ==========================================
# CHECK AI ACCESS
# ==========================================
def check_ai_access(db: Session, user: User):

    subscription, plan = get_active_subscription(db, user)

    # ==========================================
    # PAID USER
    # ==========================================
    if subscription and plan:

        today = datetime.utcnow().date()

        if not subscription.last_reset_date:
            subscription.last_reset_date = datetime.utcnow()
            subscription.ai_used_today = 0
            db.commit()

        elif subscription.last_reset_date.date() != today:
            subscription.ai_used_today = 0
            subscription.last_reset_date = datetime.utcnow()
            db.commit()

        if plan.daily_ai_limit <= 0:
            raise HTTPException(
                status_code=403,
                detail="AI not available in this plan"
            )

        if subscription.ai_used_today >= plan.daily_ai_limit:
            raise HTTPException(
                status_code=403,
                detail="Daily AI limit reached"
            )

        remaining = plan.daily_ai_limit - subscription.ai_used_today

        return subscription, plan, remaining

    # ==========================================
    # FREE USER
    # ==========================================
    today = datetime.utcnow().date()

    if not user.free_ai_last_reset:
        user.free_ai_last_reset = datetime.utcnow()
        user.free_ai_used = 0
        db.commit()

    elif user.free_ai_last_reset.date() != today:
        user.free_ai_used = 0
        user.free_ai_last_reset = datetime.utcnow()
        db.commit()

    if user.free_ai_used >= FREE_AI_LIMIT:
        raise HTTPException(
            status_code=403,
            detail="Free AI limit reached. Please subscribe."
        )

    remaining = FREE_AI_LIMIT - user.free_ai_used

    return None, None, remaining
