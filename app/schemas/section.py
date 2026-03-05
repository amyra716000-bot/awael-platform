from pydantic import BaseModel, Field
from typing import Optional
from app.models.section import SectionType


# =========================
# Create Section
# =========================
class SectionCreate(BaseModel):
    name: str = Field(min_length=1)
    type: SectionType
    chapter_id: int
    order: int = 0


# =========================
# Update Section
# =========================
class SectionUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[SectionType] = None
    order: Optional[int] = None


# =========================
# Response
# =========================
class SectionResponse(BaseModel):
    id: int
    name: str
    type: SectionType
    chapter_id: int
    order: int

    class Config:
        from_attributes = True
