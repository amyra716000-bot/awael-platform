from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # العلاقة Many-to-Many مع Question
    questions = relationship(
        "Question",
        secondary="question_category_link",
        back_populates="categories"
    )
