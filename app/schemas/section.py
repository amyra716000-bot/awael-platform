from pydantic import BaseModel


class SectionCreate(BaseModel):
    name: str
    type: str
    chapter_id: int
