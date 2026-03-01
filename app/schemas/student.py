from pydantic import BaseModel
from typing import List, Optional


# =========================
# BASIC ENTITIES
# =========================

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


# =========================
# PROGRESS
# =========================

class SolveResponse(BaseModel):
    message: str
    total_attempts: int
    correct_answers: int


class SectionProgressResponse(BaseModel):
    section_id: int
    total_attempts: int
    correct_answers: int
    success_rate: int


class DashboardResponse(BaseModel):
    total_attempts: int
    total_correct: int
    overall_success_rate: int
    sections_count: int
    strongest_section: Optional[int]
    weakest_section: Optional[int]
