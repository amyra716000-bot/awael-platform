from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # معلومات الحساب
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="student")

    xp_points = Column(Integer, default=0)
level = Column(Integer, default=1)

streak_days = Column(Integer, default=0)
last_streak_date = Column(DateTime, nullable=True)

    # =========================
    # المرحلة الدراسية (مهم)
    # =========================
    stage_id = Column(
        Integer,
        ForeignKey("stages.id"),
        nullable=True
    )

    branch_id = Column(
        Integer,
        ForeignKey("branches.id"),
        nullable=True
    )

    stage = relationship("Stage")
    branch = relationship("Branch")

    # =========================
    # AI FREE LIMIT
    # =========================
    free_ai_used = Column(Integer, default=0)

    free_ai_last_reset = Column(DateTime, default=datetime.utcnow)

    # =========================
    # حماية الحساب
    # =========================
    is_active = Column(Boolean, default=True)

    device_limit = Column(Integer, default=1)

    # =========================
    # وقت إنشاء الحساب
    # =========================
    created_at = Column(DateTime, default=datetime.utcnow)

    # =========================
    # الاشتراك
    # =========================
    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete"
    )

    # =========================
    # محاولات الامتحان
    # =========================
    exam_attempts = relationship(
        "ExamAttempt",
        back_populates="user",
        cascade="all, delete"
    )
