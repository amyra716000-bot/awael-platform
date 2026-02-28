import enum
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class ExamType(str, enum.Enum):
    daily = "daily"
    monthly = "monthly"
    final = "final"


class ExamTemplate(Base):
    __tablename__ = "exam_templates"

    id = Column(Integer, primary_key=True, index=True)

    exam_type = Column(Enum(ExamType), nullable=False)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True)

    total_questions = Column(Integer, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subject = relationship("Subject")
    chapter = relationship("Chapter")
