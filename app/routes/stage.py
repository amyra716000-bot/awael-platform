from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.stage import Stage
from pydantic import BaseModel

router = APIRouter(prefix="/admin/stages", tags=["Admin - Stages"])


class StageCreate(BaseModel):
    name: str


@router.post("/")
def create_stage(
    stage: StageCreate,
    db: Session = Depends(get_db),
    
):
    new_stage = Stage(name=stage.name)
    db.add(new_stage)
    db.commit()
    db.refresh(new_stage)
    return new_stage
