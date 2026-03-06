from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    text = Column(String, nullable=False)

    is_correct = Column(Boolean, default=False)

    order = Column(Integer, default=0)

    question = relationship(
        "Question",
        back_populates="options"
    )
