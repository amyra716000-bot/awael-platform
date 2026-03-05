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

    # لا يوجد اشتراك
    if not subscription:
        return None

    # حماية في حال كان end_date فارغ
    if subscription.end_date is None:
        return subscription

    # إذا انتهى الاشتراك
    now = datetime.utcnow()

    if subscription.end_date <= now:
        subscription.is_active = False
        db.commit()
        return None

    return subscription
