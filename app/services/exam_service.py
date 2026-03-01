from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt
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
        raise Exception("Exam template not found")

    # إنشاء محاولة
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

    # جلب كل أسئلة القسم
    all_questions = db.query(Question).filter(
        Question.section_id == template.section_id
    ).all()

    # فحص وجود أسئلة كافية
    if len(all_questions) < template.total_questions:
        raise Exception("Not enough questions in this section")

    # اختيار عشوائي من بايثون (أضمن من func.random)
    selected_questions = random.sample(
        all_questions,
        template.total_questions
    )

    for q in selected_questions:
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
    attempt.is_completed = True

    correct_answers = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == True
    ).count()

    attempt.score = correct_answers

    db.commit()
    db.refresh(attempt)

    return attempt
