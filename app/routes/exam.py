from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pydantic import BaseModel

from app.database.session import get_db
from app.core.security import get_current_user
from app.core.subscription_checker import get_active_subscription

from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt, AttemptStatus
from app.models.exam_attempt_question import ExamAttemptQuestion

from app.services.exam_service import start_exam_attempt, finish_exam_attempt
from app.services.ranking_service import update_leaderboard_for_user

router = APIRouter(prefix="/exam", tags=["Exam"])


# =====================================================
# START EXAM
# =====================================================
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

    # منع وجود امتحان مفتوح
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

    # منع إعادة المحاولة بعد النجاح
    if template.passing_score is not None:
        passed_attempt = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == current_user.id,
            ExamAttempt.template_id == template.id,
            ExamAttempt.percentage >= template.passing_score
        ).first()

        if passed_attempt:
            raise HTTPException(status_code=403, detail="You already passed this exam")

    # فحص attempt limit
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


# =====================================================
# GET QUESTIONS + AUTO FINISH
# =====================================================
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

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    remaining_seconds = None

    if attempt.started_at and attempt.status == AttemptStatus.in_progress:
        if template and template.duration_minutes:
            end_time = attempt.started_at + timedelta(minutes=template.duration_minutes)
            remaining = (end_time - datetime.utcnow()).total_seconds()

            if remaining <= 0:
                attempt.status = AttemptStatus.finished
                attempt.finished_at = datetime.utcnow()
                attempt = finish_exam_attempt(db, attempt)

                if template.leaderboard_enabled:
                    update_leaderboard_for_user(db, current_user.id, attempt.percentage)

                remaining_seconds = 0
            else:
                remaining_seconds = int(remaining)

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).all()

    return {
        "remaining_time_seconds": remaining_seconds,
        "status": attempt.status,
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


# =====================================================
# SUBMIT ANSWER
# =====================================================
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

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == exam_question.exam_attempt_id
    ).first()

    if not attempt or attempt.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if attempt.status != AttemptStatus.in_progress:
        raise HTTPException(status_code=400, detail="Exam already finished")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    if template and template.duration_minutes:
        time_limit = attempt.started_at + timedelta(minutes=template.duration_minutes)
        if datetime.utcnow() > time_limit:
            attempt.status = AttemptStatus.finished
            attempt.finished_at = datetime.utcnow()
            attempt = finish_exam_attempt(db, attempt)
            raise HTTPException(status_code=400, detail="Time is over. Exam finished.")

    exam_question.selected_answer = data.selected_answer
    exam_question.is_correct = (
        data.selected_answer == exam_question.correct_answer
    )

    db.commit()

    return {
        "message": "Answer recorded",
        "is_correct": exam_question.is_correct
    }


# =====================================================
# FINISH EXAM
# =====================================================
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

    attempt = finish_exam_attempt(db, attempt)

    if template and template.leaderboard_enabled:
        update_leaderboard_for_user(db, current_user.id, attempt.percentage)

    return {
        "percentage": attempt.percentage,
        "passed": attempt.percentage >= (template.passing_score or 0),
        "show_answers": template.show_answers_after_finish
    }


# =====================================================
# LEADERBOARD TOP 10
# =====================================================
@router.get("/leaderboard/{template_id}")
def get_leaderboard(template_id: int, db: Session = Depends(get_db)):
    top_users = db.query(ExamAttempt).filter(
        ExamAttempt.template_id == template_id,
        ExamAttempt.status == AttemptStatus.finished
    ).order_by(
        ExamAttempt.percentage.desc()
    ).limit(10).all()

    return [
        {
            "user_id": a.user_id,
            "percentage": a.percentage,
            "correct_answers": a.correct_answers
        }
        for a in top_users
    ]


# =====================================================
# ANALYTICS
# =====================================================
@router.get("/analysis/{attempt_id}")
def exam_analysis(
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

    correct = sum(1 for q in questions if q.is_correct)
    wrong = sum(1 for q in questions if q.is_correct is False)
    skipped = sum(1 for q in questions if q.selected_answer is None)

    accuracy = (correct / len(questions) * 100) if questions else 0

    return {
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped,
        "accuracy": round(accuracy, 2),
        "percentage": attempt.percentage
    }


# =====================================================
# AI ANALYSIS
# =====================================================
@router.get("/ai-analysis/{attempt_id}")
def ai_exam_analysis(
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

    if attempt.percentage >= 90:
        feedback = "Excellent performance. You have strong mastery."
    elif attempt.percentage >= 70:
        feedback = "Good performance. Review weak areas for improvement."
    elif attempt.percentage >= 50:
        feedback = "Average performance. Focus on fundamentals."
    else:
        feedback = "Needs improvement. Consider re-studying the material."

    return {
        "percentage": attempt.percentage,
        "feedback": feedback
    }
