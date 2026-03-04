from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    is_ministry = Column(Boolean, default=False)
    ministry_year = Column(Integer, nullable=True)
    is_important = Column(Boolean, default=False)

    difficulty = Column(String(10), default="medium")

    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)

    section = relationship("Section")

    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions"
    )

    type = relationship(
        "QuestionType",
        back_populates="questions"
    )
