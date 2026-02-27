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
    ministry = "ministry"
    important = "important"


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    type = Column(Enum(SectionType), nullable=False)

    chapter_id = Column(Integer, ForeignKey("chapters.id"))

    chapter = relationship("Chapter", backref="sections")
