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

    # الامتحان المرتبط
    template_id = Column(
        Integer,
        ForeignKey("exam_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # المستخدم
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # حالة الامتحان
    status = Column(
        Enum(AttemptStatus),
        default=AttemptStatus.in_progress
    )

    # وقت البدء والانتهاء
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    # مدة الامتحان بالثواني
    duration_seconds = Column(Integer, nullable=True)

    # الإحصائيات
    total_degree = Column(Integer, default=0)

    correct_answers = Column(Integer, default=0)
    wrong_answers = Column(Integer, default=0)
    skipped_answers = Column(Integer, default=0)

    score = Column(Integer, default=0)

    percentage = Column(Integer, default=0)

    # معلومات الأمان
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)

    anti_cheat_flag = Column(Boolean, default=False)

    device_fingerprint = Column(String, nullable=True)

    leaderboard_processed = Column(Boolean, default=False, index=True)

    # العلاقات
    template = relationship(
        "ExamTemplate"
    )

    user = relationship(
        "User",
        back_populates="exam_attempts"
    )

    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="exam_attempt",
        cascade="all, delete"
    )
