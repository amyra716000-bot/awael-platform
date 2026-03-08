from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database.session import Base


class AttemptStatus(str, enum.Enum):
    in_progress = "in_progress"
    finished = "finished"


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    template_id = Column(
        Integer,
        ForeignKey("exam_templates.id"),
        index=True
    )

    status = Column(
        Enum(AttemptStatus),
        default=AttemptStatus.in_progress
    )

    percentage = Column(Integer, default=0)

    correct_answers = Column(Integer, default=0)

    total_degree = Column(Integer, default=0)

    wrong_answers = Column(Integer, default=0)

    skipped_answers = Column(Integer, default=0)

    is_finished = Column(Boolean, default=False)

    started_at = Column(DateTime, default=datetime.utcnow)

    finished_at = Column(DateTime, nullable=True)

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="exam_attempts"
    )

    template = relationship(
        "ExamTemplate",
        back_populates="attempts"
    )

    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="attempt",
        cascade="all, delete"
    )
