from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class SectionType(str, enum.Enum):
    definitions = "definitions"
    explanations = "explanations"
    problems = "problems"
    multiple_choice = "multiple_choice"
    drawings = "drawings"
    essay = "essay"
    grammar = "grammar"


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)

    # اسم القسم
    name = Column(String, nullable=False)

    # نوع القسم
    type = Column(Enum(SectionType), nullable=False)

    # الفصل المرتبط
    chapter_id = Column(
        Integer,
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False
    )

    # ترتيب الظهور
    order = Column(Integer, default=0)

    # العلاقات
    chapter = relationship(
        "Chapter",
        back_populates="sections"
    )

    questions = relationship(
        "Question",
        back_populates="section",
        cascade="all, delete"
    )
