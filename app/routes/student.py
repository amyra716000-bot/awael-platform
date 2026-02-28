from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import random
import json

from app.database.session import get_db
from app.core.security import get_current_user

from app.models.user import User
from app.models.subscription import Subscription
from app.models.question import Question
from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt, AttemptStatus
from app.models.exam_attempt_question import ExamAttemptQuestion


router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# 🔐 Subscription Check
# =========================

def check_subscription(user: User, db: Session):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id,
        Subscription.is_active == True
    ).first()

    if not subscription:
        raise HTTPException(status_code=403, detail="Active subscription required")


# =========================
# 🚀 Start Exam
# =========================

@router.post("/start-exam/{template_id}")
def start_exam(template_id: int, request: Request,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):

    check_subscription(current_user, db)

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id,
        ExamTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam not found")

    if template.end_date and template.end_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Exam expired")

    existing = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template.id,
        ExamAttempt.status != AttemptStatus.expired
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Exam already taken")

    attempt = ExamAttempt(
        template_id=template.id,
        user_id=current_user.id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    query = db.query(Question).filter(
        Question.stage_id == template.stage_id
    )

    if template.subject_id:
        query = query.filter(Question.subject_id == template.subject_id)

    if template.section_id:
        query = query.filter(Question.section_id == template.section_id)

    questions = query.order_by(func.random()).limit(template.total_questions).all()

    for q in questions:
        options = json.loads(q.options_json) if q.options_json else []
        random.shuffle(options)

        snapshot = ExamAttemptQuestion(
            exam_attempt_id=attempt.id,
            question_text=q.content,
            question_type=q.question_type,
            options_json=json.dumps(options),
            correct_answer=q.answer,
            question_degree=q.degree
        )
        db.add(snapshot)

    db.commit()

    return {
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes,
        "total_questions": template.total_questions
    }


# =========================
# 📝 Submit Answer
# =========================

@router.post("/submit-answer/{attempt_id}/{question_id}")
def submit_answer(attempt_id: int, question_id: int,
                  selected_answer: str,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Invalid attempt")

    template = attempt.template
    end_time = attempt.started_at.timestamp() + (template.duration_minutes * 60)

    if datetime.utcnow().timestamp() > end_time:
        attempt.status = AttemptStatus.expired
        attempt.finished_at = datetime.utcnow()
        db.commit()
        raise HTTPException(status_code=400, detail="Time expired")

    question = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.id == question_id,
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question.selected_answer = selected_answer
    db.commit()

    return {"message": "Answer saved"}


# =========================
# 🏁 Finish Exam
# =========================

@router.post("/finish-exam/{attempt_id}")
def finish_exam(attempt_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.status == AttemptStatus.in_progress
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Invalid attempt")

    template = attempt.template
    end_time = attempt.started_at.timestamp() + (template.duration_minutes * 60)

    if datetime.utcnow().timestamp() > end_time:
        attempt.status = AttemptStatus.expired
    else:
        attempt.status = AttemptStatus.finished

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt.id
    ).all()

    total_degree = 0
    correct = 0
    wrong = 0
    skipped = 0

    for q in questions:
        total_degree += q.question_degree

        if not q.selected_answer:
            skipped += 1
            continue

        if q.selected_answer == q.correct_answer:
            q.is_correct = True
            correct += 1
        else:
            q.is_correct = False
            wrong += 1

    percentage = int((correct / len(questions)) * 100) if questions else 0

    attempt.total_degree = total_degree
    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.skipped_answers = skipped
    attempt.percentage = percentage
    attempt.finished_at = datetime.utcnow()

    db.commit()

    return {
        "percentage": percentage,
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped
                            }
