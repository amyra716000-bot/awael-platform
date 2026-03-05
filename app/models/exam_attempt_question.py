from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True, index=True)

    # محاولة الامتحان
    exam_attempt_id = Column(
        Integer,
        ForeignKey("exam_attempts.id", ondelete="CASCADE"),
        nullable=False
    )

    # السؤال
    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    # هل الاجابة صحيحة
    is_correct = Column(Boolean, default=False)

    # ======================
    # العلاقات
    # ======================

    exam_attempt = relationship(
        "ExamAttempt",
        back_populates="questions"
    )

    question = relationship(
        "Question",
        back_populates="exam_attempts"
    )
