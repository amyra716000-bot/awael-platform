from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.chapter import Chapter
from app.schemas.chapter import ChapterCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/chapters", tags=["Admin - Chapters"])


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):
    new_chapter = Chapter(
        name=chapter.name,
        subject_id=chapter.subject_id
    )
    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)
    return new_chapter
