from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)

    exam_attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    selected_correct = Column(Boolean, nullable=True)

    attempt = relationship("ExamAttempt")
    question = relationship("Question")
