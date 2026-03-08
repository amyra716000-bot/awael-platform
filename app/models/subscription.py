from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    # المستخدم
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # الخطة
    plan_id = Column(
        Integer,
        ForeignKey("plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # مدة الاشتراك
    # =========================

    start_date = Column(DateTime, default=datetime.utcnow)

    end_date = Column(DateTime, nullable=False)

    # =========================
    # AI Usage Tracking
    # =========================

    ai_used_today = Column(Integer, default=0)

    last_reset_date = Column(DateTime, default=datetime.utcnow)

    questions_used_today = Column(Integer, default=0)

    # =========================
    # حالة الاشتراك
    # =========================

    is_active = Column(Boolean, default=True)

    payment_status = Column(String(20), default="paid")

    auto_renew = Column(Boolean, default=False)

    cancelled_at = Column(DateTime, nullable=True)

    # =========================
    # Relationships
    # =========================

    user = relationship(
        "User",
        back_populates="subscriptions"
    )

    plan = relationship(
        "Plan",
        back_populates="subscriptions"
    )
