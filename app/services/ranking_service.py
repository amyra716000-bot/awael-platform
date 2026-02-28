from sqlalchemy.orm import Session
from app.models.leaderboard import Leaderboard


def update_leaderboard_for_user(
    db: Session,
    user_id: int,
    score: int
):
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

    db.commit()
