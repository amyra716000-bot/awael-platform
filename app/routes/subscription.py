from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.session import get_db
from app.models.subscription import Subscription
from app.models.plan import Plan
from app.core.security import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


# =========================
# SUBSCRIBE
# =========================
@router.post("/subscribe/{plan_id}")
def subscribe(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    plan = db.query(Plan).filter(
        Plan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Plan not found"
        )

    # تحقق من الاشتراك الحالي
    active_subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).first()

    if active_subscription:

        # إذا انتهى الاشتراك نوقفه
        if active_subscription.end_date < datetime.utcnow():
            active_subscription.is_active = False
            db.commit()

        else:
            raise HTTPException(
                status_code=400,
                detail="You already have an active subscription"
            )

    duration = plan.duration_days or 30

    end_date = datetime.utcnow() + timedelta(days=duration)

    new_subscription = Subscription(
        user_id=current_user.id,
        plan_id=plan.id,
        start_date=datetime.utcnow(),
        end_date=end_date,
        ai_used_today=0,
        last_reset_date=datetime.utcnow(),
        is_active=True
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return {
        "message": "Subscription activated",
        "plan": plan.name,
        "expires_at": end_date
    }


# =========================
# GET MY SUBSCRIPTION
# =========================
@router.get("/me")
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription"
        )

    # تحقق من انتهاء الاشتراك
    if subscription.end_date < datetime.utcnow():
        subscription.is_active = False
        db.commit()

        raise HTTPException(
            status_code=404,
            detail="Subscription expired"
        )

    plan = db.query(Plan).filter(
        Plan.id == subscription.plan_id
    ).first()

    remaining_ai = plan.daily_ai_limit - subscription.ai_used_today

    return {
        "plan_name": plan.name,
        "price": plan.price,
        "expires_at": subscription.end_date,

        "daily_ai_limit": plan.daily_ai_limit,
        "ai_used_today": subscription.ai_used_today,
        "ai_remaining_today": remaining_ai,

        "access_exams": plan.access_exams,
        "access_leaderboard": plan.access_leaderboard,
        "access_schedule": plan.access_schedule
    }
