from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.session import Base


class ExamTemplate(Base):
    __tablename__ = "exam_templates"

    id = Column(Integer, primary_key=True)
    stage_id = Column(Integer)
    subject_id = Column(Integer)
    chapter_id = Column(Integer)
    section_id = Column(Integer)

    name = Column(Integer)

    total_questions = Column(Integer)
    duration_minutes = Column(Integer)

    passing_score = Column(Integer)

    is_active = Column(Boolean, default=True)


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    template_id = Column(Integer, ForeignKey("exam_templates.id"))

    score = Column(Integer, default=0)

    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)

    is_finished = Column(Boolean, default=False)


class ExamAttemptQuestion(Base):
    __tablename__ = "exam_attempt_questions"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(Integer, ForeignKey("exam_attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    user_answer = Column(Integer, nullable=True)

    is_correct = Column(Boolean, default=False)
