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

    # فحص وقت الامتحان
    if template.start_date and now < template.start_date:
        raise HTTPException(status_code=400, detail="Exam not started yet")

    if template.end_date and now > template.end_date:
        raise HTTPException(status_code=400, detail="Exam expired")

    # منع وجود امتحان مفتوح
    existing_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user_id,
        ExamAttempt.template_id == template.id,
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if existing_attempt:
        raise HTTPException(status_code=400, detail="You already have an active exam")

    if not template.section_id and not getattr(template, "ministry_year", None):
        raise HTTPException(status_code=400, detail="Exam template has no section assigned")

    # ==========================================
    # جلب الأسئلة
    # ==========================================
    query = db.query(Question)

    # اذا الامتحان وزاري
    if getattr(template, "ministry_year", None):

        query = query.filter(
            Question.is_ministry == True,
            Question.ministry_year == template.ministry_year
        )

        if getattr(template, "ministry_round", None):
            query = query.filter(
                Question.ministry_round == template.ministry_round
            )

    # اذا امتحان عادي
    else:
        query = query.filter(
            Question.section_id == template.section_id
        )

    questions = (
        query
        .order_by(func.random())
        .limit(template.total_questions)
        .all()
    )

    if len(questions) < template.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Not enough questions in this section"
        )

    # ==========================================
    # إنشاء محاولة الامتحان
    # ==========================================
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

    # إنشاء أسئلة الامتحان
    for q in questions:

        degree = getattr(q, "degree", 1)

        exam_question = ExamAttemptQuestion(
            exam_attempt_id=attempt.id,
            question_text=q.content,
            question_type=str(q.type_id),
            options_json=getattr(q, "options_json", None),
            correct_answer=q.answer,
            question_degree=degree,
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

    if attempt.status == AttemptStatus.finished:
        return attempt

    attempt.finished_at = datetime.utcnow()
    attempt.status = AttemptStatus.finished

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).all()

    correct_answers = 0
    total_degree = 0
    correct_degree = 0
    wrong_answers = 0
    skipped_answers = 0

    for q in questions:

        total_degree += q.question_degree

        if q.selected_answer is None:
            skipped_answers += 1
            continue

        if q.is_correct:
            correct_answers += 1
            correct_degree += q.question_degree
        else:
            wrong_answers += 1

    attempt.correct_answers = correct_answers
    attempt.wrong_answers = wrong_answers
    attempt.skipped_answers = skipped_answers
    attempt.total_degree = total_degree

    if total_degree > 0:
        attempt.percentage = int((correct_degree / total_degree) * 100)
    else:
        attempt.percentage = 0

    db.commit()
    db.refresh(attempt)

    return attempt
