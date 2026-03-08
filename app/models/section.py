from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class SectionType(str, enum.Enum):

    # =========================
    # أنواع الأقسام العادية
    # =========================

    definitions = "definitions"
    explanations = "explanations"
    problems = "problems"
    multiple_choice = "multiple_choice"
    drawings = "drawings"
    essay = "essay"
    grammar = "grammar"

    # =========================
    # الأقسام الوزارية
    # =========================

    ministry_definitions = "ministry_definitions"
    ministry_reasons = "ministry_reasons"
    ministry_problems = "ministry_problems"
    ministry_mcq = "ministry_mcq"
    ministry_essay = "ministry_essay"
    ministry_grammar = "ministry_grammar"


class Section(Base):
    __tablename__ = "sections"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    type = Column(Enum(SectionType), nullable=False)

    chapter_id = Column(
        Integer,
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    order = Column(Integer, default=0)

    # =========================
    # Relationships
    # =========================

    chapter = relationship(
        "Chapter",
        back_populates="sections"
    )

    questions = relationship(
        "Question",
        back_populates="section",
        cascade="all, delete-orphan"
    )

    exam_templates = relationship(
        "ExamTemplate",
        back_populates="section"
    )
