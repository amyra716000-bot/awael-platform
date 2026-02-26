from pydantic import BaseModel


class StageCreate(BaseModel):
    name: str
