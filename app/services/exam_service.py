from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.question import Question


# ==========================================
# إنشاء محاولة امتحان
# ==========================================
def start_exam_attempt(
    db: Session,
    user_id: int,
    template_id: int
):
    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id
    ).first()

    if not template:
        return None

    # إنشاء المحاولة
    attempt = ExamAttempt(
        user_id=user_id,
        template_id=template.id,
        started_at=datetime.utcnow(),
        is_completed=False,
        score=0
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # جلب أسئلة عشوائية
    questions = (
        db.query(Question)
        .filter(Question.section_id == template.section_id)
        .order_by(func.random())
        .limit(template.total_questions)
        .all()
    )

    for q in questions:
        exam_question = ExamAttemptQuestion(
            exam_attempt_id=attempt.id,
            question_id=q.id,
            is_correct=None
        )
        db.add(exam_question)

    db.commit()

    return attempt


# ==========================================
# إنهاء الامتحان
# ==========================================
def finish_exam_attempt(
    db: Session,
    attempt: ExamAttempt
):
    attempt.finished_at = datetime.utcnow()
    attempt.is_completed = True

    correct_answers = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == True
    ).count()

    attempt.score = correct_answers

    db.commit()
    db.refresh(attempt)

    return attempt
