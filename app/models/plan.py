from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    # اسم الخطة
    name = Column(String, unique=True, nullable=False, index=True)

    # السعر بالدولار
    price = Column(Integer, nullable=False)

    # مدة الاشتراك بالأيام
    duration_days = Column(Integer, nullable=False)

    # =========================
    # حدود الاستخدام
    # =========================

    # عدد الأسئلة اليومية من بنك الأسئلة
    daily_question_limit = Column(Integer, default=0)

    # عدد أسئلة AI اليومية
    daily_ai_limit = Column(Integer, default=0)

    # =========================
    # الصلاحيات
    # =========================

    access_exams = Column(Boolean, default=False)

    access_leaderboard = Column(Boolean, default=False)

    access_schedule = Column(Boolean, default=False)

    access_essay = Column(Boolean, default=False)

    # =========================
    # العلاقة مع الاشتراكات
    # =========================

    subscriptions = relationship(
        "Subscription",
        back_populates="plan"
    )
