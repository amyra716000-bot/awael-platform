from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, String, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum


class AttemptStatus(str, enum.Enum):
    in_progress = "in_progress"
    finished = "finished"
    expired = "expired"


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, index=True)

    template_id = Column(Integer, ForeignKey("exam_templates.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    status = Column(Enum(AttemptStatus), default=AttemptStatus.in_progress)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    total_degree = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)
    skipped_answers = Column(Integer, default=0)
    percentage = Column(Integer, default=0)

    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    template = relationship("ExamTemplate")
    user = relationship("User")
anti_cheat_flag = Column(Boolean, default=False)
device_fingerprint = Column(String, nullable=True)

leaderboard_processed = Column(Boolean, default=False)
