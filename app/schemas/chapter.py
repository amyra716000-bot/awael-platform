from pydantic import BaseModel


# =========================
# Create Chapter
# =========================
class ChapterCreate(BaseModel):
    name: str
    subject_id: int


# =========================
# Update Chapter
# =========================
class ChapterUpdate(BaseModel):
    name: str | None = None


# =========================
# Response
# =========================
class ChapterResponse(BaseModel):
    id: int
    name: str
    subject_id: int

    class Config:
        from_attributes = True
