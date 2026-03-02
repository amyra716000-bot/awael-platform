from datetime import datetime
from sqlalchemy.orm import Session
from app.models.subscription import Subscription


def check_and_update_subscription(db: Session, user_id: int):
    subscription = (
        db.query(Subscription)
        .filter(
            Subscription.user_id == user_id,
            Subscription.is_active == True
        )
        .first()
    )

    if not subscription:
        return None

    # إذا انتهت مدة الاشتراك
    if subscription.end_date < datetime.utcnow():
        subscription.is_active = False
        db.commit()
        return None

    return subscription
