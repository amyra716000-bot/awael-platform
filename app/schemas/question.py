from pydantic import BaseModel
from typing import Optional, List


class QuestionCreate(BaseModel):
    content: str
    answer: str
    section_id: int
    type_id: int  # 🔥 هذا كان ناقص

    is_ministry: bool = False
    ministry_year: Optional[int] = None
    is_important: bool = False

    category_ids: Optional[List[int]] = []


class QuestionResponse(BaseModel):
    id: int
    content: str
    answer: str
    section_id: int
    type_id: int  # 🔥 أضفناه هنا أيضاً
    is_ministry: bool
    ministry_year: Optional[int]
    is_important: bool

    class Config:
        orm_mode = True
