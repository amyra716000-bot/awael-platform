from pydantic import BaseModel, Field
from typing import Optional, List


# =========================
# Create Question
# =========================
class QuestionCreate(BaseModel):
    content: str = Field(min_length=1)
    answer: str = Field(min_length=1)

    section_id: int
    type_id: int

    is_ministry: bool = False
    ministry_year: Optional[int] = None

    is_important: bool = False

    category_ids: List[int] = Field(default_factory=list)


# =========================
# Response
# =========================
class QuestionResponse(BaseModel):
    id: int
    content: str
    answer: str

    section_id: int
    type_id: int

    is_ministry: bool
    ministry_year: Optional[int]

    is_important: bool

    class Config:
        from_attributes = True
