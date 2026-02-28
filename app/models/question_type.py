from sqlalchemy import Column, Integer, String
from app.database.session import Base


class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
