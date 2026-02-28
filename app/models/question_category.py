from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.session import Base


# 🔗 جدول الربط Many-to-Many
question_category_link = Table(
    "question_category_link",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("question_categories.id"), primary_key=True),
)


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # العلاقة Many-to-Many مع Question
    questions = relationship(
        "Question",
        secondary=question_category_link,
        back_populates="categories"
    )
