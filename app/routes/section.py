from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.section import Section
from app.schemas.section import SectionCreate
from app.core.security import get_current_admin

router = APIRouter(
    prefix="/admin/sections",
    tags=["Admin - Sections"]
)


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_section(
    section: SectionCreate,
    db: Session = Depends(get_db)
):
    # إنشاء السكشن مع تمرير type الصحيح 🔥
    new_section = Section(
        name=section.name,
        type=section.type,   # ✅ هذا كان ناقص
        chapter_id=section.chapter_id
    )

    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section
