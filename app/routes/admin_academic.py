from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.core.security import get_current_admin

from app.models.stage import Stage
from app.models.branch import Branch
from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.section import Section, SectionType

router = APIRouter(
    prefix="/admin/academic",
    tags=["Admin Academic"],
    dependencies=[Depends(get_current_admin)]
)

# =====================================================
# STAGES
# =====================================================

@router.post("/stage")
def create_stage(name: str, db: Session = Depends(get_db)):

    existing = db.query(Stage).filter(Stage.name == name).first()
    if existing:
        raise HTTPException(400, "Stage already exists")

    stage = Stage(name=name)

    db.add(stage)
    db.commit()
    db.refresh(stage)

    return stage


@router.get("/stages")
def list_stages(db: Session = Depends(get_db)):
    return db.query(Stage).all()


# =====================================================
# BRANCHES
# =====================================================

@router.post("/branch")
def create_branch(
    name: str,
    stage_id: int,
    db: Session = Depends(get_db)
):

    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(404, "Stage not found")

    branch = Branch(
        name=name,
        stage_id=stage_id
    )

    db.add(branch)
    db.commit()
    db.refresh(branch)

    return branch


@router.get("/branches/{stage_id}")
def get_branches(stage_id: int, db: Session = Depends(get_db)):
    return db.query(Branch).filter(Branch.stage_id == stage_id).all()


# =====================================================
# SUBJECTS
# =====================================================

@router.post("/subject")
def create_subject(
    name: str,
    stage_id: int,
    branch_id: int | None = None,
    db: Session = Depends(get_db)
):

    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(404, "Stage not found")

    if branch_id:
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise HTTPException(404, "Branch not found")

    subject = Subject(
        name=name,
        stage_id=stage_id,
        branch_id=branch_id
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    return subject


@router.get("/subjects/{stage_id}")
def get_subjects(stage_id: int, db: Session = Depends(get_db)):
    return db.query(Subject).filter(Subject.stage_id == stage_id).all()


# =====================================================
# CHAPTERS
# =====================================================

@router.post("/chapter")
def create_chapter(
    name: str,
    subject_id: int,
    db: Session = Depends(get_db)
):

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(404, "Subject not found")

    chapter = Chapter(
        name=name,
        subject_id=subject_id
    )

    db.add(chapter)
    db.commit()
    db.refresh(chapter)

    return chapter


@router.get("/chapters/{subject_id}")
def get_chapters(subject_id: int, db: Session = Depends(get_db)):
    return db.query(Chapter).filter(Chapter.subject_id == subject_id).all()


# =====================================================
# SECTIONS
# =====================================================

@router.post("/section")
def create_section(
    name: str,
    type: SectionType,
    chapter_id: int,
    order: int = 0,
    db: Session = Depends(get_db)
):

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(404, "Chapter not found")

    section = Section(
        name=name,
        type=type,
        chapter_id=chapter_id,
        order=order
    )

    db.add(section)
    db.commit()
    db.refresh(section)

    return section


@router.get("/sections/{chapter_id}")
def get_sections(chapter_id: int, db: Session = Depends(get_db)):

    return (
        db.query(Section)
        .filter(Section.chapter_id == chapter_id)
        .order_by(Section.order)
        .all()
  )
