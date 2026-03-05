from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.stage import Stage
from app.schemas.stage import StageCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/stages", tags=["Admin - Stages"])


# =========================
# CREATE STAGE
# =========================
@router.post("/", dependencies=[Depends(get_current_admin)])
def create_stage(stage: StageCreate, db: Session = Depends(get_db)):

    existing = db.query(Stage).filter(
        Stage.name == stage.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Stage already exists"
        )

    new_stage = Stage(name=stage.name)

    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)

    return new_stage


# =========================
# GET ALL STAGES
# =========================
@router.get("/", dependencies=[Depends(get_current_admin)])
def get_stages(db: Session = Depends(get_db)):

    stages = db.query(Stage).all()

    return stages


# =========================
# DELETE STAGE
# =========================
@router.delete("/{stage_id}", dependencies=[Depends(get_current_admin)])
def delete_stage(stage_id: int, db: Session = Depends(get_db)):

    stage = db.query(Stage).filter(
        Stage.id == stage_id
    ).first()

    if not stage:
        raise HTTPException(
            status_code=404,
            detail="Stage not found"
        )

    db.delete(stage)
    db.commit()

    return {"message": "Stage deleted"}
