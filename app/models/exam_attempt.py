from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.session import Base


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
    total_degree = Column(Integer, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # 🔴 العلاقة المطلوبة
    user = relationship(
        "User",
        back_populates="exam_attempts"
    )

    template = relationship("ExamTemplate")

    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="attempt",
        cascade="all, delete"
    )
