from pydantic import BaseModel

class SubmitAnswer(BaseModel):
    answer: str
