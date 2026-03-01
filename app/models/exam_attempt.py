from sqlalchemy.orm import Session
from datetime import datetime
import random

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
        raise Exception("Exam template not found")

    # إنشاء محاولة جديدة بالحالة in_progress
    attempt = ExamAttempt(
        user_id=user_id,
        template_id=template.id,
        status=AttemptStatus.in_progress,
        started_at=datetime.utcnow()
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # جلب أسئلة القسم
    all_questions = db.query(Question).filter(
        Question.section_id == template.section_id
    ).all()

    if len(all_questions) < template.total_questions:
        raise Exception("Not enough questions in this section")

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
    attempt.status = AttemptStatus.finished

    # حساب النتائج
    correct = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == True
    ).count()

    wrong = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == False
    ).count()

    skipped = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id,
        ExamAttemptQuestion.is_correct == None
    ).count()

    total_questions = correct + wrong + skipped

    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.skipped_answers = skipped
    attempt.total_degree = correct

    if total_questions > 0:
        attempt.percentage = int((correct / total_questions) * 100)
    else:
        attempt.percentage = 0

    db.commit()
    db.refresh(attempt)

    return attempt
