from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.section import Section
from app.models.chapter import Chapter
from app.schemas.section import SectionCreate
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/admin/sections",
    tags=["Admin - Sections"]
)


# =========================
# CREATE SECTION
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db)
):

    chapter = db.query(Chapter).filter(
        Chapter.id == section.chapter_id
    ).first()

    if not chapter:
        raise HTTPException(
            status_code=404,
            detail="Chapter not found"
        )

    existing = db.query(Section).filter(
        Section.name == section.name,
        Section.chapter_id == section.chapter_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Section already exists in this chapter"
        )

    new_section = Section(
        name=section.name,
        type=section.type,
        chapter_id=section.chapter_id
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section


# =========================
# GET SECTIONS BY CHAPTER
# =========================
@router.get("/{chapter_id}", dependencies=[Depends(get_current_admin)])
def get_sections(
    chapter_id: int,
    db: Session = Depends(get_db)
):

    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id
    ).first()

    if not chapter:
        raise HTTPException(
            status_code=404,
            detail="Chapter not found"
        )

    sections = db.query(Section).filter(
        Section.chapter_id == chapter_id
    ).order_by(Section.order).all()

    return sections


# =========================
# DELETE SECTION
# =========================
@router.delete("/{section_id}", dependencies=[Depends(get_current_admin)])
def delete_section(
    section_id: int,
    db: Session = Depends(get_db)
):

    section = db.query(Section).filter(
        Section.id == section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    db.delete(section)
    db.commit()

    return {"message": "Section deleted"}
