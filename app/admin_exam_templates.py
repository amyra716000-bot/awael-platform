from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.exam_template import ExamTemplate
from app.schemas.exam_template import ExamTemplateCreate
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/admin/exam-templates",
    tags=["Admin - Exam Templates"],
    dependencies=[Depends(get_current_admin)]
)


@router.post("/")
def create_exam_template(
    template: ExamTemplateCreate,
    db: Session = Depends(get_db)
):
    new_template = ExamTemplate(**template.dict())

    db.add(new_template)
    db.commit()
    db.refresh(new_template)

    return new_template
