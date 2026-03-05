from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    explanation = Column(Text, nullable=True)

    difficulty = Column(String(10), default="medium")

    is_important = Column(Boolean, default=False)

    is_ministry = Column(Boolean, default=False)

    ministry_year = Column(Integer, nullable=True)

    ministry_round = Column(String(20), nullable=True)

    total_attempts = Column(Integer, default=0)

    correct_attempts = Column(Integer, default=0)

    degree = Column(Integer, default=1)

    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False
    )

    type_id = Column(
        Integer,
        ForeignKey("question_types.id"),
        nullable=False
    )

    section = relationship(
        "Section",
        back_populates="questions"
    )

    type = relationship(
        "QuestionType",
        back_populates="questions"
    )
