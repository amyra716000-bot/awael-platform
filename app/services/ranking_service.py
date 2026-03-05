from sqlalchemy.orm import Session
from app.models.leaderboard import Leaderboard
from app.models.user import User


def update_leaderboard_for_user(
    db: Session,
    user_id: int,
    score: int
):

    # تجاهل النتائج الصفرية
    if score <= 0:
        return

    record = db.query(Leaderboard).filter(
        Leaderboard.user_id == user_id
    ).first()

    if record:

        # تحديث عدد الامتحانات
        record.total_exams += 1

        # تحديث اعلى درجة
        if score > record.highest_score:
            record.highest_score = score

        # تحديث المعدل
        total_score = record.average_score * (record.total_exams - 1)
        total_score += score
        record.average_score = total_score / record.total_exams

        # النقاط التنافسية
        record.competitive_score = (
            record.highest_score * 0.6 +
            record.average_score * 0.4
        )

    else:

        record = Leaderboard(
            user_id=user_id,
            highest_score=score,
            average_score=score,
            total_exams=1,
            competitive_score=score
        )

        db.add(record)

    # =========================
    # تحديث نقاط المستخدم
    # =========================

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user:

        user.xp_points += score

        # نظام مستويات
        user.level = (user.xp_points // 1000) + 1

    db.commit()

    return record
