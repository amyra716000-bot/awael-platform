from sqlalchemy import Column, Integer, ForeignKey, Float
from app.database.session import Base


class QuestionStatistics(Base):
    __tablename__ = "question_statistics"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(Integer, ForeignKey("questions.id"))

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    wrong_attempts = Column(Integer, default=0)

    difficulty_score = Column(Float, default=0)
