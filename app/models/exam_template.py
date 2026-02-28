from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum


class ExamType(str, enum.Enum):
    daily = "daily"
    monthly = "monthly"
    final = "final"


class ExamTemplate(Base):
    __tablename__ = "exam_templates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    type = Column(Enum(ExamType), nullable=False)

    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    total_questions = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    passing_score = Column(Integer, default=50)

    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    stage = relationship("Stage")
    subject = relationship("Subject")
    section = relationship("Section")
