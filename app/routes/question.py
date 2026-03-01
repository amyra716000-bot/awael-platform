from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.session import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.core.security import get_current_admin, get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


# =========================
# CREATE QUESTION (Admin Only)
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db)
):
    new_question = Question(
        content=question.content,
        answer=question.answer,
        section_id=question.section_id,
        type_id=question.type_id,
        is_ministry=question.is_ministry,
        ministry_year=question.ministry_year,
        is_important=question.is_important,
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
    current_user = Depends(get_current_user),
):
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


# =========================
# GET QUESTIONS (Advanced Filter + Pagination)
# =========================
@router.get("/")
def get_questions(
    section_id: int | None = None,
    type_id: int | None = None,
    is_important: bool | None = None,
    is_ministry: bool | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):

    query = db.query(Question)

    if section_id is not None:
        query = query.filter(Question.section_id == section_id)

    if type_id is not None:
        query = query.filter(Question.type_id == type_id)

    if is_important is not None:
        query = query.filter(Question.is_important == is_important)

    if is_ministry is not None:
        query = query.filter(Question.is_ministry == is_ministry)

    total = query.count()

    questions = query.order_by(desc(Question.id)) \
                     .offset((page - 1) * limit) \
                     .limit(limit) \
                     .all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": questions
    }
