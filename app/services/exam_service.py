from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt, AttemptStatus
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.question import Question


# ==========================================
# START EXAM ATTEMPT
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

    # إنشاء محاولة جديدة
    attempt = ExamAttempt(
        user_id=user_id,
        template_id=template.id,
        status=AttemptStatus.in_progress,
        started_at=datetime.utcnow(),
        total_degree=0,
        correct_answers=0,
        wrong_answers=0,
        skipped_answers=0,
        percentage=0,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # جلب أسئلة عشوائية حسب القسم
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
# FINISH EXAM ATTEMPT
# ==========================================
def finish_exam_attempt(
    db: Session,
    attempt: ExamAttempt
):
    attempt.finished_at = datetime.utcnow()
    attempt.status = AttemptStatus.finished

    correct_answers = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == True
    ).count()

    total_questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).count()

    attempt.correct_answers = correct_answers
    attempt.total_degree = total_questions

    if total_questions > 0:
        attempt.percentage = int((correct_answers / total_questions) * 100)
    else:
        attempt.percentage = 0

    db.commit()
    db.refresh(attempt)

    return attempt
