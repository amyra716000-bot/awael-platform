from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)

    # اسم الفصل
    name = Column(String, nullable=False)

    # المادة المرتبط بها
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    # العلاقات
    subject = relationship("Subject", back_populates="chapters")

    sections = relationship("Section", back_populates="chapter")
