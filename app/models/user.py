from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=True)

    email = Column(String, unique=True, index=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(String, default="user")

    is_active = Column(Boolean, default=True)

    xp_points = Column(Integer, default=0)

    level = Column(Integer, default=1)

    stage_id = Column(Integer, ForeignKey("stages.id"))

    stage = relationship("Stage")

    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    exam_attempts = relationship(
        "ExamAttempt",
        back_populates="user",
        cascade="all, delete"
    )

    favorites = relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    leaderboards = relationship(
        "Leaderboard",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    progress = relationship(
        "StudentProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )
