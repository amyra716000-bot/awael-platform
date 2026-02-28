from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    section_id = Column(Integer, ForeignKey("sections.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    duration_minutes = Column(Integer, default=30)
    total_questions = Column(Integer)

    section = relationship("Section")
