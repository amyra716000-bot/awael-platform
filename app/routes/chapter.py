from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.chapter import Chapter
from app.models.subject import Subject
from app.schemas.chapter import ChapterCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/chapters", tags=["Admin - Chapters"])


# =========================
# CREATE CHAPTER
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_chapter(chapter: ChapterCreate, db: Session = Depends(get_db)):

    subject = db.query(Subject).filter(
        Subject.id == chapter.subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    existing = db.query(Chapter).filter(
        Chapter.name == chapter.name,
        Chapter.subject_id == chapter.subject_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Chapter already exists in this subject"
        )

    new_chapter = Chapter(
        name=chapter.name,
        subject_id=chapter.subject_id
    )

    db.add(new_chapter)
    db.commit()
    db.refresh(new_chapter)

    return new_chapter


# =========================
# GET CHAPTERS BY SUBJECT
# =========================
@router.get("/{subject_id}", dependencies=[Depends(get_current_admin)])
def get_chapters(subject_id: int, db: Session = Depends(get_db)):

    subject = db.query(Subject).filter(
        Subject.id == subject_id
    ).first()

    if not subject:
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    chapters = db.query(Chapter).filter(
        Chapter.subject_id == subject_id
    ).all()

    return chapters


# =========================
# DELETE CHAPTER
# =========================
@router.delete("/{chapter_id}", dependencies=[Depends(get_current_admin)])
def delete_chapter(chapter_id: int, db: Session = Depends(get_db)):

    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id
    ).first()

    if not chapter:
        raise HTTPException(
            status_code=404,
            detail="Chapter not found"
        )

    db.delete(chapter)
    db.commit()

    return {"message": "Chapter deleted"}
