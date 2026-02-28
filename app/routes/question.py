from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.core.security import get_current_admin, get_current_user

router = APIRouter(prefix="/questions", tags=["Questions"])


# 🔹 إنشاء سؤال (Admin فقط)
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):

    new_question = Question(
        content=question.content,
        answer=question.answer,
        section_id=question.section_id,
        type_id=question.type_id,   # 🔥 هذا كان ناقص
        is_ministry=question.is_ministry,
        ministry_year=question.ministry_year,
        is_important=question.is_important,
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


# 🔹 جلب سؤال
@router.get("/{question_id}")
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    question = db.query(Question).filter(Question.id == question_id).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question
