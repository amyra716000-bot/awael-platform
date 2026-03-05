from pydantic import BaseModel, Field
from typing import Optional


# =========================
# Create Stage
# =========================
class StageCreate(BaseModel):
    name: str = Field(min_length=2)


# =========================
# Update Stage
# =========================
class StageUpdate(BaseModel):
    name: Optional[str] = None


# =========================
# Response
# =========================
class StageResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
