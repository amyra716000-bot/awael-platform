from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Leaderboard(Base):
    __tablename__ = "leaderboards"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    score = Column(Integer, default=0)

    rank = Column(Integer)

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="leaderboards"
    )
