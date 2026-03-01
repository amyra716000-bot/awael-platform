from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from fastapi import HTTPException

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
    try:
        template = db.query(ExamTemplate).filter(
            ExamTemplate.id == template_id,
            ExamTemplate.is_active == True
        ).first()

        if not template:
            raise HTTPException(status_code=404, detail="Exam template not found")

        now = datetime.utcnow()

        # فحص وقت البداية والنهاية
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

        if not template.section_id:
            raise HTTPException(status_code=400, detail="Exam template has no section assigned")

        # عدد الأسئلة المتوفرة
        question_count = db.query(Question).filter(
            Question.section_id == template.section_id
        ).count()

        if question_count == 0:
            raise HTTPException(status_code=400, detail="No questions available for this section")

        # إنشاء محاولة جديدة
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
        db.flush()  # للحصول على attempt.id بدون commit

        # سحب أسئلة عشوائية
        questions = (
            db.query(Question)
            .filter(Question.section_id == template.section_id)
            .order_by(func.random())
            .limit(min(template.total_questions, question_count))
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
        db.refresh(attempt)

        return attempt

    except HTTPException:
        db.rollback()
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while starting exam")

    except Exception as e:
    db.rollback()
    print("START EXAM REAL ERROR:", repr(e))
    raise


# ==========================================
# FINISH EXAM ATTEMPT
# ==========================================
def finish_exam_attempt(
    db: Session,
    attempt: ExamAttempt
):
    try:
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

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while finishing exam")

    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unexpected error while finishing exam")
