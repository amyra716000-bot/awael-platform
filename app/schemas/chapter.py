from pydantic import BaseModel


class ChapterCreate(BaseModel):
    name: str
    subject_id: int
