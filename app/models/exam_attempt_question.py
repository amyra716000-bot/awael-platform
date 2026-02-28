from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True, index=True)

    exam_attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))

    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)

    options_json = Column(Text, nullable=True)
    correct_answer = Column(String, nullable=False)

    question_degree = Column(Integer, default=1)

    selected_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)

    attempt = relationship("ExamAttempt")
