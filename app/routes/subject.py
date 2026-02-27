from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.subject import Subject
from app.schemas.subject import SubjectCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/subjects", tags=["Admin - Subjects"])


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    new_subject = Subject(
        name=subject.name,
        stage_id=subject.stage_id
    )
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject
