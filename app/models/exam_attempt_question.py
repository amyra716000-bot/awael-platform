from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))

    attempt = relationship(
        "ExamAttempt",
        back_populates="questions"
    )
