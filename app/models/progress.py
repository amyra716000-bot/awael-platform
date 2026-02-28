from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base
from datetime import datetime


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    is_completed = Column(Boolean, default=True)
    is_correct = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    question = relationship("Question")

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="unique_user_question"),
    )
