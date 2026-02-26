from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.stage import Stage
from app.schemas.stage import StageCreate
from app.core.security import get_current_admin

router = APIRouter(prefix="/admin/stages", tags=["Admin - Stages"])


@router.post("/", dependencies=[Depends(get_current_admin)])
def create_stage(stage: StageCreate, db: Session = Depends(get_db)):
    new_stage = Stage(name=stage.name)
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    return new_stage
