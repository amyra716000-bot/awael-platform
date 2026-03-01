from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime
from fastapi import HTTPException

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt, AttemptStatus
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.question import Question


# ==========================================
# START EXAM ATTEMPT
# ==========================================
def start_exam_attempt(db: Session, user_id: int, template_id: int):

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id,
        ExamTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam template not found")

    now = datetime.utcnow()

    if template.start_date and now < template.start_date:
        raise HTTPException(status_code=400, detail="Exam not started yet")

    if template.end_date and now > template.end_date:
        raise HTTPException(status_code=400, detail="Exam expired")

    existing_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user_id,
        ExamAttempt.template_id == template.id,
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if existing_attempt:
        raise HTTPException(status_code=400, detail="You already have an active exam")

    if not template.section_id:
        raise HTTPException(status_code=400, detail="Exam template has no section assigned")

    questions = (
        db.query(Question)
        .filter(Question.section_id == template.section_id)
        .order_by(func.random())
        .limit(template.total_questions)
        .all()
    )

    if not questions:
        raise HTTPException(status_code=400, detail="No questions available")

    attempt = ExamAttempt(
        user_id=user_id,
        template_id=template.id,
        status=AttemptStatus.in_progress,
        started_at=now,
        total_degree=0,
        correct_answers=0,
        wrong_answers=0,
        skipped_answers=0,
        percentage=0,
    )

    db.add(attempt)
    db.flush()

    for q in questions:
        exam_question = ExamAttemptQuestion(
            exam_attempt_id=attempt.id,
            question_text=q.content,
            question_type=str(q.type_id),
            options_json=getattr(q, "options_json", None),
            correct_answer=q.answer,
            question_degree=1,
            selected_answer=None,
            is_correct=None
        )
        db.add(exam_question)

    db.commit()
    db.refresh(attempt)

    return attempt


# ==========================================
# FINISH EXAM ATTEMPT
# ==========================================
def finish_exam_attempt(db: Session, attempt: ExamAttempt):

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
