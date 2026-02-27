from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    stage_id: int
