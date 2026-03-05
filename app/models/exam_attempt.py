from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from enum import Enum


class AttemptStatus(str, Enum):
    started = "started"
    finished = "finished"
    cancelled = "cancelled"


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    template_id = Column(Integer, ForeignKey("exam_templates.id"))

    score = Column(Integer)

    user = relationship(
        "User",
        back_populates="exam_attempts"
    )

    questions = relationship(
        "ExamAttemptQuestion",
        back_populates="attempt",
        cascade="all, delete"
    )
