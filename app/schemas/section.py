from pydantic import BaseModel
from app.models.section import SectionType


class SectionCreate(BaseModel):
    name: str
    type: SectionType
    chapter_id: int
