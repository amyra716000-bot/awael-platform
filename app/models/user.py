from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # معلومات الحساب
    # =========================

    name = Column(String, nullable=True)

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user",
        index=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    # =========================
    # نظام النقاط
    # =========================

    xp_points = Column(Integer, default=0)

    level = Column(Integer, default=1)

    # =========================
    # المرحلة الدراسية
    # =========================

    stage_id = Column(
        Integer,
        ForeignKey("stages.id"),
        nullable=True
    )

    stage = relationship(
        "Stage"
    )

    # =========================
    # الاشتراكات
    # =========================

    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # =========================
    # محاولات الامتحان
    # =========================

    exam_attempts = relationship(
        "ExamAttempt",
        back_populates="user",
        cascade="all, delete"
    )

    # =========================
    # Leaderboard
    # =========================

    leaderboards = relationship(
        "Leaderboard",
        back_populates="user",
        cascade="all, delete-orphan"
    )
