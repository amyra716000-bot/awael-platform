from pydantic import BaseModel, Field
from typing import Optional, List


class QuestionOptionResponse(BaseModel):
    id: int
    text: str
    is_correct: bool
    order: int

    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    content: str = Field(min_length=1)
    answer: str = Field(min_length=1)

    section_id: int
    type_id: int

    difficulty: str = "medium"

    is_ministry: bool = False
    ministry_year: Optional[int] = None
    ministry_round: Optional[str] = None

    is_important: bool = False

    category_ids: List[int] = Field(default_factory=list)


class QuestionResponse(BaseModel):
    id: int
    content: str
    answer: str

    explanation: Optional[str]

    difficulty: str

    section_id: int
    type_id: int

    is_ministry: bool
    ministry_year: Optional[int]
    ministry_round: Optional[str]

    is_important: bool

    degree: int

    options: List[QuestionOptionResponse] = []

    class Config:
        from_attributes = True


class QuestionOptionCreate(BaseModel):
    text: str
    is_correct: bool = False
    order: int = 1
