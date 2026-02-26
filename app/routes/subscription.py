from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.session import get_db
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.post("/subscribe")
def subscribe(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # تأكد ما عنده اشتراك فعال
    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True,
        Subscription.end_date > datetime.utcnow()
    ).first()

    if active_subscription:
        raise HTTPException(status_code=400, detail="You already have an active subscription")

    # جيب الخطة
    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # احسب تاريخ الانتهاء
    end_date = datetime.utcnow() + timedelta(days=plan.duration_days)

    # أنشئ الاشتراك
    new_subscription = Subscription(
        user_id=current_user.id,
        plan_id=plan.id,
        end_date=end_date,
        ai_used_today=0,
        is_active=True
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return {
        "message": "Subscription created successfully",
        "plan": plan.name,
        "expires_at": end_date
  }
