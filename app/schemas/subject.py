from pydantic import BaseModel, Field
from typing import Optional


# =========================
# Create Subject
# =========================
class SubjectCreate(BaseModel):
    name: str = Field(min_length=2)

    stage_id: int
    branch_id: Optional[int] = None


# =========================
# Update Subject
# =========================
class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    branch_id: Optional[int] = None


# =========================
# Response
# =========================
class SubjectResponse(BaseModel):
    id: int
    name: str
    stage_id: int
    branch_id: Optional[int]

    class Config:
        from_attributes = True
