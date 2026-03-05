from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.database.session import get_db
from app.models.question import Question
from app.models.section import Section
from app.models.question_type import QuestionType
from app.schemas.question import QuestionCreate
from app.core.security import get_current_admin, get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


# =========================
# CREATE QUESTION (ADMIN)
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):

    section = db.query(Section).filter(
        Section.id == question.section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    qtype = db.query(QuestionType).filter(
        QuestionType.id == question.type_id
    ).first()

    if not qtype:
        raise HTTPException(
            status_code=404,
            detail="Question type not found"
        )

    new_question = Question(
        content=question.content,
        answer=question.answer,
        section_id=question.section_id,
        type_id=question.type_id,
        is_ministry=question.is_ministry,
        ministry_year=question.ministry_year,
        ministry_round=question.ministry_round,
        is_important=question.is_important,
        difficulty=question.difficulty
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


# =========================
# GET SINGLE QUESTION
# =========================
@router.get("/{question_id}")
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question


# =========================
# GET QUESTIONS BY SECTION
# =========================
@router.get("/section/{section_id}")
def get_questions_by_section(
    section_id: int,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    section = db.query(Section).filter(
        Section.id == section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    questions = (
        db.query(Question)
        .filter(Question.section_id == section_id)
        .limit(limit)
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for this section"
        )

    return questions


# =========================
# RANDOM QUESTIONS
# =========================
@router.get("/random/{section_id}")
def random_questions(
    section_id: int,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    questions = (
        db.query(Question)
        .filter(Question.section_id == section_id)
        .order_by(func.random())
        .limit(limit)
        .all()
    )

    return questions


# =========================
# MINISTRY QUESTIONS
# =========================
@router.get("/ministry/{year}")
def ministry_questions(
    year: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    questions = db.query(Question).filter(
        Question.is_ministry == True,
        Question.ministry_year == year
    ).all()

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No ministry questions found"
        )

    return questions


# =========================
# DAILY QUESTION
# =========================
@router.get("/daily")
def daily_question(
    db: Session = Depends(get_db)
):

    question = (
        db.query(Question)
        .filter(Question.is_ministry == True)
        .order_by(func.random())
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="No ministry questions available"
        )

    return {
        "question_id": question.id,
        "question": question.content,
        "answer": question.answer,
        "year": question.ministry_year,
        "round": question.ministry_round
    }
