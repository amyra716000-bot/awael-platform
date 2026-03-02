# redeploy trigger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import get_active_subscription

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt, AttemptStatus
from app.models.exam_attempt_question import ExamAttemptQuestion

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

    # 🔒 منع وجود امتحان مفتوح
    existing_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id,
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if existing_attempt:
        return {
            "message": "Exam already started",
            "attempt_id": existing_attempt.id,
            "duration_minutes": template.duration_minutes or 0
        }

    # فحص الاشتراك
    if template.is_paid:
        subscription, plan = get_active_subscription(db, current_user)
        if not subscription:
            raise HTTPException(status_code=403, detail="Paid exam. Please subscribe.")

    previous_attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id
    ).count()

    if template.attempt_limit is not None:
        if previous_attempts >= template.attempt_limit:
            raise HTTPException(status_code=403, detail="Attempt limit reached")

    attempt = start_exam_attempt(db, current_user.id, template.id)

    return {
        "message": "Exam started",
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes or 0
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

    remaining_seconds = None

if attempt.started_at and attempt.status == AttemptStatus.in_progress:
    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    if template and template.duration_minutes:
        end_time = attempt.started_at + timedelta(minutes=template.duration_minutes)
        remaining = (end_time - datetime.utcnow()).total_seconds()
        remaining_seconds = max(int(remaining), 0)

return {
    "remaining_time_seconds": remaining_seconds,
    "questions": [
        {
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "options_json": q.options_json,
            "question_degree": q.question_degree,
            "selected_answer": q.selected_answer,
        }
        for q in questions
    ]
}


# ==============================
# SUBMIT ANSWER
# ==============================

from pydantic import BaseModel

class AnswerRequest(BaseModel):
    selected_answer: str
    
@router.post("/answer/{exam_question_id}")
def submit_answer(
    exam_question_id: int,
    data: AnswerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    exam_question = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.id == exam_question_id
    ).first()

    if not exam_question:
        raise HTTPException(status_code=404, detail="Question not found")

    # =====================================
    # 🔒 تأكد السؤال تابع لهذا المستخدم
    # =====================================
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == exam_question.exam_attempt_id
    ).first()

    if not attempt or attempt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    # =====================================
    # 🔒 منع الإجابة بعد إنهاء الامتحان
    # =====================================
    if attempt.status != AttemptStatus.in_progress:
        raise HTTPException(status_code=400, detail="Exam already finished")

    # =====================================
    # ⏱ فحص انتهاء الوقت
    # =====================================
    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    if template and template.duration_minutes:
        time_limit = attempt.started_at + timedelta(minutes=template.duration_minutes)
        if datetime.utcnow() > time_limit:
            attempt.status = AttemptStatus.finished
            attempt.finished_at = datetime.utcnow()
            db.commit()
            raise HTTPException(status_code=400, detail="Time is over. Exam finished.")

    # =====================================
    # ✅ تخزين الإجابة (الكود القديم كما هو)
    # =====================================
    exam_question.selected_answer = data.selected_answer

    exam_question.is_correct = (
        data.selected_answer == exam_question.correct_answer
    )

    db.commit()

    return {
        "message": "Answer recorded",
        "is_correct": exam_question.is_correct
            }

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
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found or already finished")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # فحص الوقت
    if template.duration_minutes:
        time_limit = attempt.started_at + timedelta(minutes=template.duration_minutes)
        if datetime.utcnow() > time_limit:
            attempt.finished_at = datetime.utcnow()

    attempt = finish_exam_attempt(db, attempt)

    if template.leaderboard_enabled:
        update_leaderboard_for_user(db, current_user.id, attempt.percentage)

    return {
        "percentage": attempt.percentage,
        "passed": attempt.percentage >= (template.passing_score or 0),
        "show_answers": template.show_answers_after_finish
        }
    
# ==============================
# EXAM HISTORY
# ==============================
@router.get("/history")
def exam_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id
    ).order_by(ExamAttempt.started_at.desc()).all()

    return [
        {
            "attempt_id": a.id,
            "template_id": a.template_id,
            "status": a.status,
            "started_at": a.started_at,
            "finished_at": a.finished_at,
            "percentage": a.percentage,
            "correct_answers": a.correct_answers,
            "total_degree": a.total_degree
        }
        for a in attempts
    ]

# ==============================
# REVIEW EXAM (After Finish)
# ==============================
@router.get("/review/{attempt_id}")
def review_exam(
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

    # لازم يكون الامتحان منتهي
    if attempt.status != AttemptStatus.finished:
        raise HTTPException(status_code=400, detail="Exam not finished yet")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    # تحقق هل مسموح عرض الاجوبة
    if not template.show_answers_after_finish:
        raise HTTPException(status_code=403, detail="Review not allowed for this exam")

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).all()

    return [
        {
            "question_id": q.id,
            "question_text": q.question_text,
            "selected_answer": q.selected_answer,
            "correct_answer": q.correct_answer,
            "is_correct": q.is_correct,
            "question_degree": q.question_degree
        }
        for q in questions
    ]
