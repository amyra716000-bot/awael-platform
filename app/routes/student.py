from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date

from app.database.session import get_db
from app.models.user import User
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.question import Question

from app.models.exam import ExamTemplate, ExamType
from app.models.exam_attempt import ExamAttempt
from app.models.exam_question import ExamAttemptQuestion

from app.core.security import get_current_user


router = APIRouter(prefix="/student", tags=["Student"])


# =========================
# 🚀 Start Exam
# =========================

@router.post("/start-exam/{template_id}")
def start_exam(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id,
        ExamTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Exam template not found")
        # 🚫 منع وجود محاولة غير مكتملة
unfinished_attempt = db.query(ExamAttempt).filter(
    ExamAttempt.user_id == current_user.id,
    ExamAttempt.template_id == template.id,
    ExamAttempt.is_completed == False
).first()

if unfinished_attempt:
    raise HTTPException(
        status_code=400,
        detail="You already have an unfinished exam attempt"
    )

    # 🔒 منع التكرار حسب النوع
    today = date.today()

    existing_attempt = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.template_id == template_id,
        func.date(ExamAttempt.started_at) == today
    ).first()

    if template.exam_type == ExamType.daily and existing_attempt:
        raise HTTPException(status_code=400, detail="Daily exam already taken today")

    if template.exam_type == ExamType.monthly:
        month_attempt = db.query(ExamAttempt).filter(
            ExamAttempt.user_id == current_user.id,
            ExamAttempt.template_id == template_id,
            func.date_trunc('month', ExamAttempt.started_at) == func.date_trunc('month', func.now())
        ).first()
        if month_attempt:
            raise HTTPException(status_code=400, detail="Monthly exam already taken")

    # 🎯 إنشاء محاولة
    attempt = ExamAttempt(
        template_id=template.id,
        user_id=current_user.id,
        total_questions=template.total_questions
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # 📚 اختيار الأسئلة
    query = db.query(Question).filter(
        Question.subject_id == template.subject_id
    )

    if template.chapter_id:
        query = query.filter(Question.chapter_id == template.chapter_id)

    questions = query.order_by(func.random()).limit(template.total_questions).all()

    for q in questions:
        exam_q = ExamAttemptQuestion(
            exam_attempt_id=attempt.id,
            question_id=q.id
        )
        db.add(exam_q)

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
def submit_answer(
    attempt_id: int,
    question_id: int,
    selected_answer: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.is_completed == False
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Exam attempt not found")

    exam_q = db.query(ExamAttemptQuestion).filter(
        ExamAttemptQuestion.exam_attempt_id == attempt_id,
        ExamAttemptQuestion.question_id == question_id
    ).first()

    if not exam_q:
        raise HTTPException(status_code=404, detail="Question not part of this exam")

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    is_correct = question.answer == selected_answer

    exam_q.selected_answer = selected_answer
    exam_q.is_correct = is_correct
    exam_q.answered_at = datetime.utcnow()

    if is_correct:
        attempt.correct_answers += 1

    db.commit()

    return {"is_correct": is_correct}


# =========================
# ✅ Finish Exam
# =========================

@router.post("/finish-exam/{attempt_id}")
def finish_exam(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id
    ).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    if attempt.is_completed:
        raise HTTPException(status_code=400, detail="Exam already finished")

    attempt.is_completed = True
    attempt.finished_at = datetime.utcnow()

    attempt.score = int(
        (attempt.correct_answers / attempt.total_questions) * 100
    )

    db.commit()

    return {
        "score": attempt.score,
        "correct_answers": attempt.correct_answers,
        "total_questions": attempt.total_questions
}
