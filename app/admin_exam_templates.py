from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.exam_template import ExamTemplate
from app.models.stage import Stage
from app.models.subject import Subject
from app.models.section import Section

from app.schemas.exam_template import ExamTemplateCreate
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/admin/exam-templates",
    tags=["Admin - Exam Templates"],
    dependencies=[Depends(get_current_admin)]
)


# =========================
# CREATE EXAM TEMPLATE
# =========================
@router.post("/")
def create_exam_template(
    template: ExamTemplateCreate,
    db: Session = Depends(get_db)
):

    if template.total_questions <= 0:
        raise HTTPException(
            status_code=400,
            detail="total_questions must be greater than 0"
        )

    # تحقق المرحلة
    stage = db.query(Stage).filter(
        Stage.id == template.stage_id
    ).first()

    if not stage:
        raise HTTPException(
            status_code=404,
            detail="Stage not found"
        )

    # تحقق المادة
    if template.subject_id:
        subject = db.query(Subject).filter(
            Subject.id == template.subject_id
        ).first()

        if not subject:
            raise HTTPException(
                status_code=404,
                detail="Subject not found"
            )

    # تحقق القسم
    if template.section_id:
        section = db.query(Section).filter(
            Section.id == template.section_id
        ).first()

        if not section:
            raise HTTPException(
                status_code=404,
                detail="Section not found"
            )

    new_template = ExamTemplate(**template.dict())

    db.add(new_template)
    db.commit()
    db.refresh(new_template)

    return new_template


# =========================
# GET ALL EXAMS
# =========================
@router.get("/")
def get_exam_templates(
    db: Session = Depends(get_db)
):

    templates = db.query(ExamTemplate).all()

    return templates


# =========================
# DELETE EXAM
# =========================
@router.delete("/{template_id}")
def delete_exam_template(
    template_id: int,
    db: Session = Depends(get_db)
):

    template = db.query(ExamTemplate).filter(
        ExamTemplate.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Exam template not found"
        )

    db.delete(template)
    db.commit()

    return {"message": "Exam template deleted"}
