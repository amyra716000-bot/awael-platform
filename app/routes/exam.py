from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.session import get_db
from app.models.exam_template import ExamTemplate
from app.models.exam_attempt import ExamAttempt
from app.models.exam_attempt_question import ExamAttemptQuestion
from app.models.question import Question
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/exam", tags=["Exam"])


# ===============================
# Start Exam
# ===============================
@router.post("/start/{template_id}")
def start_exam(
    template_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam not found")

    questions = db.query(Question).filter(
        Question.section_id == template.section_id
    ).limit(template.total_questions).all()

    if len(questions) < template.total_questions:
        raise HTTPException(
            status_code=400,
            detail="Not enough questions in bank"
        )

    attempt = ExamAttempt(
        user_id=user.id,
        template_id=template.id,
        started_at=datetime.utcnow(),
        is_finished=False
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    for q in questions:
        exam_q = ExamAttemptQuestion(
            attempt_id=attempt.id,
            question_id=q.id
        )
        db.add(exam_q)

    db.commit()

    return {
        "message": "Exam started",
        "attempt_id": attempt.id,
        "duration_minutes": template.duration_minutes
    }


# ===============================
# Get Exam Questions
# ===============================
@router.get("/questions/{attempt_id}")
def get_exam_questions(
    attempt_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == user["user_id"]
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == attempt.template_id
    ).first()

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.attempt_id == attempt.id
    ).all()

    result = []

    for q in questions:
        question = db.query(Question).filter(
            Question.id == q.question_id
        ).first()

        result.append({
            "exam_question_id": q.id,
            "question_id": question.id,
            "content": question.content,
            "difficulty": question.difficulty
        })

    return {
        "attempt_id": attempt.id,
        "questions": result
    }


# ===============================
# Submit Answer
# ===============================
@router.post("/answer/{exam_question_id}")
def submit_answer(
    exam_question_id: int,
    answer: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    exam_q = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.id == exam_question_id
    ).first()

    if not exam_q:
        raise HTTPException(status_code=404, detail="Question not found")

    question = db.query(Question).filter(
        Question.id == exam_q.question_id
    ).first()

    exam_q.user_answer = answer

    if question.answer == answer:
        exam_q.is_correct = True
    else:
        exam_q.is_correct = False

    db.commit()

    return {
        "correct": exam_q.is_correct
    }


# ===============================
# Finish Exam
# ===============================
@router.post("/finish/{attempt_id}")
def finish_exam(
    attempt_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    questions = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.attempt_id == attempt.id
    ).all()

    score = 0

    for q in questions:
        if q.is_correct:
            score += 1

    attempt.score = score
    attempt.is_finished = True
    attempt.finished_at = datetime.utcnow()

    db.commit()

    return {
        "score": score,
        "total": len(questions)
    }


# ===============================
# Leaderboard
# ===============================
@router.get("/leaderboard/{template_id}")
def leaderboard(
    template_id: int,
    db: Session = Depends(get_db)
):

    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.template_id == template_id,
        ExamAttempt.is_finished == True
    ).order_by(ExamAttempt.score.desc()).limit(20).all()

    result = []

    for a in attempts:
        result.append({
            "user_id": a.user_id,
            "score": a.score
        })

    return {
        "leaderboard": result
    }
