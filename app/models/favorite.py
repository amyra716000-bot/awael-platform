from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    # العلاقات
    user = relationship(
        "User",
        back_populates="favorites"
    )

    question = relationship(
        "Question",
        back_populates="favorites"
    )

    # القيود
    __table_args__ = (

        # منع التكرار
        UniqueConstraint(
            "user_id",
            "question_id",
            name="unique_user_question"
        ),

        # تحسين الأداء
        Index(
            "idx_user_favorites",
            "user_id"
        ),
    )
