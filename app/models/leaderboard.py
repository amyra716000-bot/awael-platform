from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    score = Column(Integer)

    rank = Column(Integer)

    user = relationship(
        "User",
        back_populates="leaderboards"
    )
