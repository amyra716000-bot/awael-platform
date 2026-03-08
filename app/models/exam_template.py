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

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    # اسم الامتحان
    name = Column(String, nullable=False)

    # نوع الامتحان
    type = Column(Enum(ExamType), nullable=False)

    # =========================
    # المرحلة الدراسية
    # =========================

    stage_id = Column(
        Integer,
        ForeignKey("stages.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # المادة
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    # القسم / الدرس
    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    # =========================
    # إعدادات الامتحان
    # =========================

    # عدد الاسئلة
    total_questions = Column(Integer, nullable=False)

    # مدة الامتحان بالدقائق
    duration_minutes = Column(Integer, nullable=False)

    # نسبة النجاح
    passing_score = Column(Integer, default=50)

    # مستوى الامتحان
    difficulty = Column(String(10), default="medium")

    # ترتيب الامتحان
    display_order = Column(Integer, default=0)

    # حالة الامتحان
    is_active = Column(Boolean, default=True)

    # وقت البداية
    start_date = Column(DateTime, default=datetime.utcnow)

    # وقت النهاية
    end_date = Column(DateTime, nullable=True)

    # عدد المحاولات
    attempt_limit = Column(Integer, default=1)

    # هل الامتحان مدفوع
    is_paid = Column(Boolean, default=True)

    # عشوائية الاسئلة
    randomize_questions = Column(Boolean, default=True)

    # عشوائية الخيارات
    randomize_options = Column(Boolean, default=True)

    # لوحة المتصدرين
    leaderboard_enabled = Column(Boolean, default=True)

    # اظهار الاجوبة بعد الانتهاء
    show_answers_after_finish = Column(Boolean, default=False)

    # =========================
    # الامتحانات الوزارية
    # =========================

    ministry_year = Column(Integer, nullable=True)

    ministry_round = Column(String(20), nullable=True)

    # =========================
    # العلاقات
    # =========================

    stage = relationship(
        "Stage",
        back_populates="exam_templates"
    )

    subject = relationship(
        "Subject",
        back_populates="exam_templates"
    )

    section = relationship(
        "Section",
        back_populates="exam_templates"
    )

    attempts = relationship(
        "ExamAttempt",
        back_populates="template",
        cascade="all, delete"
    )
