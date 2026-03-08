from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionOption(Base):
    __tablename__ = "question_options"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    text = Column(String, nullable=False)

    is_correct = Column(Boolean, default=False)

    order = Column(Integer, default=0)

    # =========================
    # Relationships
    # =========================

    question = relationship(
        "Question",
        back_populates="options"
    )
