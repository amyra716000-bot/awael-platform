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
            "duration_minutes": template.duration_minutes
        }

    # فحص الاشتراك
    if template.is_paid:
        subscription, plan = get_active_subscription(db, current_user)
        if not subscription:
            raise HTTPException(status_code=403, detail="Subscription required")

    # منع إعادة الامتحان بعد النجاح
    passed_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id,
        ExamAttempt.percentage >= template.passing_score
    ).first()

    if passed_attempt:
        raise HTTPException(status_code=403, detail="You already passed this exam")

    # attempt limit
    attempts_count = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id
    ).count()

    if template.attempt_limit and attempts_count >= template.attempt_limit:
        raise HTTPException(status_code=403, detail="Attempt limit reached")

    attempt = start_exam_attempt(db, current_user.id, template.id)

    return {
        "message": "Exam started",
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes
    }


# =====================================================
# GET QUESTIONS
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

    if template.duration_minutes and not attempt.is_finished:

        end_time = attempt.started_at + timedelta(minutes=template.duration_minutes)
        remaining = (end_time - datetime.utcnow()).total_seconds()

        if remaining <= 0:
            attempt.finished = True
            attempt.finished_at = datetime.utcnow()

            attempt = finish_exam_attempt(db, attempt)

            if template.leaderboard_enabled:
                update_leaderboard_for_user(db, current_user.id, attempt.percentage)

            remaining_seconds = 0
        else:
            remaining_seconds = int(remaining)

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).order_by(ExamAttemptQuestion.id).all()

    return {
        "remaining_time_seconds": remaining_seconds,
        "finished": attempt.finished,
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "options_json": q.options_json,
                "question_degree": q.question_degree,
                "selected_answer": q.selected_answer
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

    if attempt.finished:
        raise HTTPException(status_code=400, detail="Exam already finished")

    # منع تغيير الإجابة
    if exam_question.selected_answer is not None:
        raise HTTPException(status_code=400, detail="Answer already submitted")

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
        ExamAttempt.finished == False
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    attempt = finish_exam_attempt(db, attempt)

    if template.leaderboard_enabled:
        update_leaderboard_for_user(db, current_user.id, attempt.percentage)

    return {
        "percentage": attempt.percentage,
        "passed": attempt.percentage >= template.passing_score,
        "show_answers": template.show_answers_after_finish
    }


# =====================================================
# LEADERBOARD
# =====================================================
@router.get("/leaderboard/{template_id}")
def get_leaderboard(template_id: int, db: Session = Depends(get_db)):

    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.template_id == template_id,
        ExamAttempt.finished == True
    ).order_by(
        ExamAttempt.percentage.desc()
    ).limit(10).all()

    seen_users = set()
    result = []

    for a in attempts:
        if a.user_id in seen_users:
            continue
        seen_users.add(a.user_id)

        result.append({
            "user_id": a.user_id,
            "percentage": a.percentage,
            "correct_answers": a.correct_answers
        })

    return result

