from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    explanation = Column(Text)

    difficulty = Column(String(10), default="medium")

    is_important = Column(Boolean, default=False)

    is_ministry = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)

    ministry_year = Column(Integer)

    ministry_round = Column(String)

    total_attempts = Column(Integer, default=0)

    correct_attempts = Column(Integer, default=0)

    degree = Column(Integer, default=1)

    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE")
    )

    type_id = Column(
        Integer,
        ForeignKey("question_types.id")
    )

    section = relationship(
        "Section",
        back_populates="questions"
    )

    type = relationship(
        "QuestionType",
        back_populates="questions"
    )

    favorites = relationship(
        "Favorite",
        back_populates="question",
        cascade="all, delete-orphan"
    )

    exam_attempt_questions = relationship(
        "ExamAttemptQuestion",
        back_populates="question",
        cascade="all, delete"
    )

    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions"
    )

    # ---------------------------
    # Question Options (NEW)
    # ---------------------------
    options = relationship(
        "QuestionOption",
        back_populates="question",
        cascade="all, delete",
        order_by="QuestionOption.order"
    )
