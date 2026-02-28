from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.question import Question
from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.leaderboard import Leaderboard
from app.models.question_statistics import QuestionStatistics

router = APIRouter(prefix="/exam", tags=["Exam"])

FREE_LIMIT = 3


# =========================
# START EXAM
# =========================
@router.post("/start/{template_id}")
def start_exam(template_id: int,
               request: Request,
               db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id,
        ExamTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam not found")

    # منع تجاوز عدد المحاولات
    attempts_count = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template_id
    ).count()

    if attempts_count >= template.attempt_limit:
        raise HTTPException(status_code=403, detail="Attempt limit reached")

    attempt = ExamAttempt(
        user_id=current_user.id,
        template_id=template.id,
        device_fingerprint=request.headers.get("user-agent"),
        ip_address=request.client.host
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # سحب أسئلة عشوائية
    questions = db.query(Question).filter(
        Question.subject_id == template.subject_id
    ).all()

    if len(questions) < template.total_questions:
        raise HTTPException(status_code=400, detail="Not enough questions")

    selected = random.sample(questions, template.total_questions)

    for q in selected:
        snapshot = ExamAttemptQuestion(
            attempt_id=attempt.id,
            question_id=q.id,
            question_text=q.content,
            correct_answer=q.answer,
            degree=1
        )
        db.add(snapshot)

    db.commit()

    return {
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes
    }


# =========================
# SUBMIT ANSWER
# =========================
@router.post("/submit/{attempt_id}/{question_id}")
def submit_answer(attempt_id: int,
                  question_id: int,
                  answer: str,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.status != "in_progress":
        raise HTTPException(status_code=403, detail="Exam closed")

    template = attempt.template

    # تحقق من الوقت
    if datetime.utcnow() > attempt.started_at + timedelta(minutes=template.duration_minutes):
        attempt.status = "expired"
        db.commit()
        raise HTTPException(status_code=403, detail="Time expired")

    answered_count = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.attempt_id == attempt_id,
        ExamAttemptQuestion.selected_answer != None
    ).count()

    # Free Lock
    if current_user.role == "student" and current_user.subscription is None:
        if answered_count >= FREE_LIMIT:
            attempt.status = "locked"
            db.commit()
            return {"locked": True, "message": "Upgrade to continue"}

    question = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.attempt_id == attempt_id,
        ExamAttemptQuestion.question_id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question.selected_answer = answer
    question.is_correct = (answer == question.correct_answer)

    db.commit()

    return {"submitted": True}


# =========================
# FINISH EXAM
# =========================
@router.post("/finish/{attempt_id}")
def finish_exam(attempt_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.status != "in_progress":
        raise HTTPException(status_code=403, detail="Cannot finish")

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.attempt_id == attempt_id
    ).all()

    correct = 0
    wrong = 0
    skipped = 0
    total_degree = 0

    for q in questions:
        total_degree += q.degree
        if q.selected_answer is None:
            skipped += 1
        elif q.is_correct:
            correct += 1
        else:
            wrong += 1

        # تحديث إحصائيات السؤال
        stats = db.query(QuestionStatistics).filter(
            QuestionStatistics.question_id == q.question_id
        ).first()

        if not stats:
            stats = QuestionStatistics(question_id=q.question_id)
            db.add(stats)

        stats.total_attempts += 1
        if q.is_correct:
            stats.correct_attempts += 1
        else:
            stats.wrong_attempts += 1

        stats.difficulty_score = (
            stats.wrong_attempts / stats.total_attempts
        ) if stats.total_attempts > 0 else 0

    percentage = (correct / len(questions)) * 100 if questions else 0

    attempt.correct = correct
    attempt.wrong = wrong
    attempt.skipped = skipped
    attempt.percentage = percentage
    attempt.total_degree = total_degree
    attempt.status = "finished"
    attempt.finished_at = datetime.utcnow()

    # تحديث Leaderboard
    board = db.query(Leaderboard).filter(
        Leaderboard.user_id == current_user.id,
        Leaderboard.stage_id == attempt.template.stage_id,
        Leaderboard.subject_id == attempt.template.subject_id
    ).first()

    if not board:
        board = Leaderboard(
            user_id=current_user.id,
            stage_id=attempt.template.stage_id,
            subject_id=attempt.template.subject_id
        )
        db.add(board)

    board.total_exams += 1
    board.highest_score = max(board.highest_score, percentage)
    board.average_score = (
        (board.average_score * (board.total_exams - 1) + percentage)
        / board.total_exams
    )

    board.competitive_score = (
        board.highest_score * 0.5 +
        board.average_score * 0.5
    )

    db.commit()

    return {
        "percentage": percentage,
        "correct": correct,
        "wrong": wrong,
        "skipped": skipped
                 }
