from sqlalchemy.orm import relationship
from app.database.session import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, relationship
import enum
from datetime import datetime


class AttemptStatus(str, enum.Enum):
    in_progress = "in_progress"
    finished = "finished"


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    template_id = Column(Integer, ForeignKey("exam_templates.id"))

    status = Column(Enum(AttemptStatus), default=AttemptStatus.in_progress)

    percentage = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime)

    # 🔴 هذا السطر المهم
    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="attempt",
        cascade="all, delete"
    )
