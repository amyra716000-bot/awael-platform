from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    order = Column(Integer)

    selected_option_id = Column(Integer, ForeignKey("question_options.id"), nullable=True)

    is_correct = Column(Boolean, nullable=True)

    attempt = relationship(
        "ExamAttempt",
        back_populates="questions",
        foreign_keys=[attempt_id]
    )

    question = relationship("Question")

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    exam_attempt_id = Column(
        Integer,
        ForeignKey("exam_attempts.id"),
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        index=True
    )

    question_text = Column(String)

    question_type = Column(String)

    options_json = Column(String)

    correct_answer = Column(String)

    selected_answer = Column(String, nullable=True)

    is_correct = Column(Boolean, nullable=True)

    question_degree = Column(Integer, default=1)

    # =========================
    # Relationships
    # =========================

    attempt = relationship(
        "ExamAttempt",
        back_populates="questions"
    )

    question = relationship(
        "Question",
        back_populates="exam_attempt_questions"
    )
