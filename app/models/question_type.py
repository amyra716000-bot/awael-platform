from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionType(Base):
    __tablename__ = "question_types"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    # اسم نوع السؤال
    name = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    # =========================
    # Relationships
    # =========================

    questions = relationship(
        "Question",
        back_populates="type",
        cascade="all, delete"
    )
