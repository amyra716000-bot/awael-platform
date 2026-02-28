from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)

    template_id = Column(Integer, ForeignKey("exam_templates.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    score = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_questions = Column(Integer, nullable=False)

    is_completed = Column(Boolean, default=False)

    template = relationship("ExamTemplate")
    user = relationship("User")
