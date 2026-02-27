from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.subscription import Subscription
from app.models.plan import Plan


def check_ai_access(db: Session, user):

    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True
    ).first()

    # ما عنده اشتراك
    if not subscription:
        raise HTTPException(status_code=403, detail="No active subscription")

    # انتهى الاشتراك
    if subscription.end_date < datetime.utcnow():
        subscription.is_active = False
        db.commit()
        raise HTTPException(status_code=403, detail="Subscription expired")

    plan = db.query(Plan).filter(Plan.id == subscription.plan_id).first()

    # تجاوز الحد اليومي
    if subscription.ai_used_today >= plan.daily_ai_limit:
        raise HTTPException(status_code=403, detail="Daily AI limit reached")

    return subscription, plan
