from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base
import enum


class ExamType(str, enum.Enum):
    daily = "daily"
    monthly = "monthly"
    final = "final"


class ExamTemplate(Base):
    __tablename__ = "exam_templates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    # نوع الامتحان
    type = Column(Enum(ExamType), nullable=False)

    # المرحلة
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)

    # المادة
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)

    # القسم (اختياري)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)

    # عدد الاسئلة
    total_questions = Column(Integer, nullable=False)

    # مدة الامتحان بالدقائق
    duration_minutes = Column(Integer, nullable=False)

    # نسبة النجاح
    passing_score = Column(Integer, default=50)

    # حالة الامتحان
    is_active = Column(Boolean, default=True)

    # وقت البداية والنهاية
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    # عدد المحاولات
    attempt_limit = Column(Integer, default=1)

    # هل الامتحان مدفوع
    is_paid = Column(Boolean, default=True)

    # عشوائية الاسئلة
    randomize_questions = Column(Boolean, default=True)

    # عشوائية الخيارات
    randomize_options = Column(Boolean, default=True)

    # Leaderboard
    leaderboard_enabled = Column(Boolean, default=True)

    # اظهار الاجوبة بعد الانتهاء
    show_answers_after_finish = Column(Boolean, default=False)

    # العلاقات
    stage = relationship("Stage")
    subject = relationship("Subject")
    section = relationship("Section")
