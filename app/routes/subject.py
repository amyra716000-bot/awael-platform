from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.subject import Subject
from app.models.stage import Stage
from app.schemas.subject import SubjectCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/subjects", tags=["Admin - Subjects"])


# =========================
# CREATE SUBJECT
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):

    stage = db.query(Stage).filter(
        Stage.id == subject.stage_id
    ).first()

    if not stage:
        raise HTTPException(
            status_code=404,
            detail="Stage not found"
        )

    existing = db.query(Subject).filter(
        Subject.name == subject.name,
        Subject.stage_id == subject.stage_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Subject already exists in this stage"
        )

    new_subject = Subject(
        name=subject.name,
        stage_id=subject.stage_id
    )

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject


# =========================
# GET SUBJECTS BY STAGE
# =========================
@router.get("/{stage_id}", dependencies=[Depends(get_current_admin)])
def get_subjects(stage_id: int, db: Session = Depends(get_db)):

    stage = db.query(Stage).filter(
        Stage.id == stage_id
    ).first()

    if not stage:
        raise HTTPException(
            status_code=404,
            detail="Stage not found"
        )

    subjects = db.query(Subject).filter(
        Subject.stage_id == stage_id
    ).all()

    return subjects


# =========================
# DELETE SUBJECT
# =========================
@router.delete("/{subject_id}", dependencies=[Depends(get_current_admin)])
def delete_subject(subject_id: int, db: Session = Depends(get_db)):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db.delete(subject)
    db.commit()

    return {"message": "Subject deleted"}
