from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    # 🔹 معلومات إضافية
    is_ministry = Column(Boolean, default=False)
    ministry_year = Column(Integer, nullable=True)
    is_important = Column(Boolean, default=False)

    # 🔹 مستوى الصعوبة (جديد)
    difficulty = Column(String(10), default="medium")

    # 🔹 إحصائيات عامة للسؤال (جديد)
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)

    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)

    # 🔹 علاقة مع Section
    section = relationship("Section", backref="questions")

    # 🔹 علاقة Many-to-Many مع Category
    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions"
    )

    # 🔹 علاقة مع QuestionType
    type = relationship(
        "QuestionType",
        back_populates="questions"
    )
