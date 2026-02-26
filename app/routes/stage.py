from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.stage import Stage
from app.core.security import get_current_admin
from pydantic import BaseModel

router = APIRouter(prefix="/admin/stages", tags=["Admin - Stages"])


class StageCreate(BaseModel):
    name: str


@router.post("/")
def create_stage(
    stage: StageCreate,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    new_stage = Stage(name=stage.name)
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    return new_stage
