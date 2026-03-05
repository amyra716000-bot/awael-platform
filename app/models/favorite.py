from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE")
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE")
    )

    user = relationship(
        "User",
        back_populates="favorites"
    )

    question = relationship(
        "Question",
        back_populates="favorites"
    )

    __table_args__ = (
        UniqueConstraint("user_id", "question_id"),
    )
