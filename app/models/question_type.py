from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionType(Base):
    __tablename__ = "question_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    questions = relationship(
        "Question",
        back_populates="type"
    )
