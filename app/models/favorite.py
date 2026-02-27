from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database.session import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    user = relationship("User")
    question = relationship("Question")

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="unique_user_question"),
    )
