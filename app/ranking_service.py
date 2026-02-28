from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models.exam_attempt import ExamAttempt
from app.models.leaderboard import LeaderboardEntry


def calculate_competitive_score(highest, average, total_exams):
    consistency = min(total_exams / 10, 1)  # max factor = 1
    return (highest * 0.5) + (average * 0.3) + (consistency * 100 * 0.2)


def update_leaderboard_for_user(db: Session, user_id: int):

    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user_id,
        ExamAttempt.status == "finished"
    ).all()

    if not attempts:
        return

    highest = max(a.percentage for a in attempts)
    average = sum(a.percentage for a in attempts) / len(attempts)
    total = len(attempts)

    competitive_score = calculate_competitive_score(highest, average, total)

    entry = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.user_id == user_id,
        LeaderboardEntry.scope_type == "global"
    ).first()

    if not entry:
        entry = LeaderboardEntry(
            user_id=user_id,
            stage_id=attempts[0].template.stage_id,
            scope_type="global"
        )
        db.add(entry)

    entry.highest_score = highest
    entry.average_score = average
    entry.total_exams = total
    entry.competitive_score = competitive_score
    entry.last_updated = datetime.utcnow()

    db.commit()

    # إعادة حساب الترتيب
    all_entries = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.scope_type == "global"
    ).order_by(LeaderboardEntry.competitive_score.desc()).all()

    for index, e in enumerate(all_entries, start=1):
        e.rank_position = index

    db.commit()
