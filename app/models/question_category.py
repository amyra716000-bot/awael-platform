from sqlalchemy import Column, Integer, String, ForeignKey, Table, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


# ==========================================
# جدول الربط Many-to-Many
# ==========================================
question_category_link = Table(
    "question_category_link",
    Base.metadata,

    Column(
        "question_id",
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "category_id",
        Integer,
        ForeignKey("question_categories.id", ondelete="CASCADE"),
        primary_key=True
    ),

    # تحسين الأداء
    Index("idx_question_category", "question_id", "category_id")
)


class QuestionCategory(Base):
    __tablename__ = "question_categories"

    id = Column(Integer, primary_key=True, index=True)

    # اسم التصنيف
    name = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # العلاقة Many-to-Many مع Question
    questions = relationship(
        "Question",
        secondary=question_category_link,
        back_populates="categories",
        lazy="selectin"
    )
