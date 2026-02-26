from pydantic import BaseModel


class PlanCreate(BaseModel):
    name: str
    price: int
    daily_question_limit: int
    daily_ai_limit: int
    access_exams: bool
    access_leaderboard: bool
    access_schedule: bool
    access_essay: bool


class PlanUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    daily_question_limit: int | None = None
    daily_ai_limit: int | None = None
    access_exams: bool | None = None
    access_leaderboard: bool | None = None
    access_schedule: bool | None = None
    access_essay: bool | None = None


class PlanResponse(BaseModel):
    id: int
    name: str
    price: int
    daily_question_limit: int
    daily_ai_limit: int
    access_exams: bool
    access_leaderboard: bool
    access_schedule: bool
    access_essay: bool

    class Config:
        from_attributes = True
