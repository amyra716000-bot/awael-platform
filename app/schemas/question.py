from pydantic import BaseModel
from typing import Optional


class QuestionCreate(BaseModel):
    content: str
    answer: str
    section_id: int

    is_ministry: bool = False
    ministry_year: Optional[int] = None
    is_important: bool = False


class QuestionResponse(BaseModel):
    id: int
    content: str
    answer: str
    section_id: int
    is_ministry: bool
    ministry_year: Optional[int]
    is_important: bool

    class Config:
        orm_mode = True
