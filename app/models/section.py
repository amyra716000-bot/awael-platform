from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class SectionType(str, enum.Enum):

    # الاقسام العادية (مثل الملزمة)
    definitions = "definitions"
    explanations = "explanations"
    problems = "problems"
    multiple_choice = "multiple_choice"
    drawings = "drawings"
    essay = "essay"
    grammar = "grammar"

    # الاقسام الوزارية
    ministry_definitions = "ministry_definitions"
    ministry_reasons = "ministry_reasons"
    ministry_problems = "ministry_problems"
    ministry_mcq = "ministry_mcq"
    ministry_essay = "ministry_essay"
    ministry_grammar = "ministry_grammar"

class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    type = Column(Enum(SectionType), nullable=False)

    chapter_id = Column(Integer, ForeignKey("chapters.id"))

    order = Column(Integer, default=0)

    chapter = relationship("Chapter", backref="sections")
    questions = relationship("Question")
