from sqlalchemy.orm import Session
from app.models.leaderboard import Leaderboard
from app.models.user import User


def update_leaderboard_for_user(
    db: Session,
    user_id: int,
    score: int
):

    if score <= 0:
        return

    record = db.query(Leaderboard).filter(
        Leaderboard.user_id == user_id
    ).first()

    if record:
        record.total_score += score
    else:
        record = Leaderboard(
            user_id=user_id,
            total_score=score
        )
        db.add(record)

    # تحديث نقاط المستخدم
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:
        user.xp_points += score

        # نظام مستويات بسيط
        user.level = (user.xp_points // 1000) + 1

    db.commit()

    return record
