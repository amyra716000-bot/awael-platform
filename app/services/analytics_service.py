from sqlalchemy.orm import Session
from app.models.question_statistics import QuestionStatistics


def update_question_stats(
    db: Session,
    question_id: int,
    is_correct: bool
):
    stats = db.query(QuestionStatistics).filter(
        QuestionStatistics.question_id == question_id
    ).first()

    if not stats:
        stats = QuestionStatistics(
            question_id=question_id,
            total_attempts=0,
            correct_attempts=0
        )
        db.add(stats)

    stats.total_attempts += 1

    if is_correct:
        stats.correct_attempts += 1

    db.commit()
