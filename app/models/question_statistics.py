from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionStatistics(Base):
    __tablename__ = "question_statistics"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    question = relationship("Question")
