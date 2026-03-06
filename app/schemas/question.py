from pydantic import BaseModel
from typing import Optional, List


class QuestionOptionResponse(BaseModel):
    id: int
    text: str
    is_correct: bool
    order: int

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    content: str
    answer: str
    explanation: Optional[str]

    difficulty: str

    is_important: bool
    is_ministry: bool

    ministry_year: Optional[int]
    ministry_round: Optional[str]

    section_id: int
    type_id: int

    degree: int

    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True
