from pydantic import BaseModel
from typing import Optional


class StageOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SubjectOut(BaseModel):
    id: int
    name: str
    stage_id: int

    class Config:
        from_attributes = True


class ChapterOut(BaseModel):
    id: int
    name: str
    subject_id: int

    class Config:
        from_attributes = True


class SectionOut(BaseModel):
    id: int
    name: str
    chapter_id: int

    class Config:
        from_attributes = True


class QuestionOut(BaseModel):
    id: int
    content: str
    section_id: int

    class Config:
        from_attributes = True
