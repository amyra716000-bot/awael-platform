from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    # المستخدم
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # الخطة
    plan_id = Column(
        Integer,
        ForeignKey("plans.id", ondelete="CASCADE"),
        nullable=False
    )

    # وقت الاشتراك
    start_date = Column(DateTime, default=datetime.utcnow)

    # وقت انتهاء الاشتراك
    end_date = Column(DateTime, nullable=False)

    # =========================
    # AI Usage Tracking
    # =========================

    ai_used_today = Column(Integer, default=0)

    last_reset_date = Column(DateTime, default=datetime.utcnow)

    # =========================
    # حالة الاشتراك
    # =========================

    is_active = Column(Boolean, default=True)

    # =========================
    # العلاقات
    # =========================

    user = relationship(
        "User",
        back_populates="subscriptions"
    )

    plan = relationship(
        "Plan",
        back_populates="subscriptions"
    )
