from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import get_active_subscription

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.question import Question

from app.services.exam_service import start_exam_attempt, finish_exam_attempt
from app.services.ranking_service import update_leaderboard_for_user
from app.services.analytics_service import update_question_stats

router = APIRouter(prefix="/exam", tags=["Exam"])


# ==============================
# START EXAM
# ==============================
@router.post("/start/{template_id}")
def start_exam(
    template_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id,
        ExamTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam not found")

    # فحص مدفوع
    if template.is_paid:
        subscription, plan = get_active_subscription(db, current_user)
        if not subscription:
            raise HTTPException(status_code=403, detail="Paid exam. Please subscribe.")

    # منع الإعادة
    previous_attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id
    ).count()

    if previous_attempts >= template.attempt_limit:
        raise HTTPException(status_code=403, detail="Attempt limit reached")

    attempt = start_exam_attempt(db, current_user.id, template.id)

    return {
        "message": "Exam started",
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes
    }


# ==============================
# GET ATTEMPT QUESTIONS
# ==============================
@router.get("/questions/{attempt_id}")
def get_exam_questions(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).all()

    return questions


# ==============================
# SUBMIT ANSWER
# ==============================
@router.post("/answer/{exam_question_id}")
def submit_answer(
    exam_question_id: int,
    is_correct: bool,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exam_question = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.id == exam_question_id
    ).first()

    if not exam_question:
        raise HTTPException(status_code=404, detail="Question not found")

    exam_question.is_correct = is_correct
    db.commit()

    update_question_stats(db, exam_question.question_id, is_correct)

    return {"message": "Answer recorded"}


# ==============================
# FINISH EXAM
# ==============================
@router.post("/finish/{attempt_id}")
def finish_exam(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.is_completed == False
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found or already finished")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    # فحص الوقت
    time_limit = attempt.started_at + timedelta(minutes=template.duration_minutes)
    if datetime.utcnow() > time_limit:
        attempt.finished_at = datetime.utcnow()

    attempt = finish_exam_attempt(db, attempt)

    # تحديث التصنيف
    if template.leaderboard_enabled:
        update_leaderboard_for_user(db, current_user.id, attempt.score)

    return {
        "score": attempt.score,
        "passed": attempt.score >= template.passing_score,
        "show_answers": template.show_answers_after_finish
  }
