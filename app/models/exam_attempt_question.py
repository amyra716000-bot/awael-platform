from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True)

    exam_attempt_id = Column(
        Integer,
        ForeignKey("exam_attempts.id")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id")
    )

    is_correct = Column(Boolean, nullable=True)

    attempt = relationship("ExamAttempt")

    question = relationship("Question")
