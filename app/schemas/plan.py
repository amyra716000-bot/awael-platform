from pydantic import BaseModel, Field


# =========================
# Create Plan
# =========================
class PlanCreate(BaseModel):
    name: str

    price: int = Field(ge=0)
    duration_days: int = Field(gt=0)

    daily_question_limit: int = Field(ge=0)
    daily_ai_limit: int = Field(ge=0)

    access_exams: bool = True
    access_leaderboard: bool = True
    access_schedule: bool = True
    access_essay: bool = False


# =========================
# Update Plan
# =========================
class PlanUpdate(BaseModel):
    name: str | None = None

    price: int | None = Field(default=None, ge=0)
    duration_days: int | None = Field(default=None, gt=0)

    daily_question_limit: int | None = Field(default=None, ge=0)
    daily_ai_limit: int | None = Field(default=None, ge=0)

    access_exams: bool | None = None
    access_leaderboard: bool | None = None
    access_schedule: bool | None = None
    access_essay: bool | None = None


# =========================
# Response
# =========================
class PlanResponse(BaseModel):
    id: int
    name: str

    price: int
    duration_days: int

    daily_question_limit: int
    daily_ai_limit: int

    access_exams: bool
    access_leaderboard: bool
    access_schedule: bool
    access_essay: bool

    class Config:
        from_attributes = True
