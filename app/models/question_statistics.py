from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class QuestionStatistics(Base):
    __tablename__ = "question_statistics"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    total_attempts = Column(Integer, default=0)

    correct_attempts = Column(Integer, default=0)

    question = relationship("Question")

    __table_args__ = (

        # منع تكرار الإحصائية لنفس السؤال
        UniqueConstraint(
            "question_id",
            name="unique_question_statistics"
        ),

        # تسريع الاستعلام
        Index(
            "idx_question_statistics_question",
            "question_id"
        ),
    )
