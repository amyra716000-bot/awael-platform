from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base


class Favorite(Base):
    __tablename__ = "favorites"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="favorites"
    )

    question = relationship(
        "Question",
        back_populates="favorites"
    )

    # =========================
    # Constraints
    # =========================

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "question_id",
            name="unique_user_favorite_question"
        ),
    )
