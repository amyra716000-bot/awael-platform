from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database.session import Base


question_category_link = Table(
    "question_category_link",
    Base.metadata,
    Column("question_id", Integer, ForeignKey("questions.id")),
    Column("category_id", Integer, ForeignKey("question_categories.id"))
)


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True)

    name = Column(String)

    questions = relationship(
        "Question",
        secondary=question_category_link,
        back_populates="categories"
    )
