from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    # نص السؤال
    content = Column(Text, nullable=False)

    # الجواب الصحيح
    answer = Column(Text, nullable=False)

    # شرح الجواب
    explanation = Column(Text, nullable=True)

    # صعوبة السؤال
    difficulty = Column(String(10), default="medium", index=True)

    # سؤال مهم
    is_important = Column(Boolean, default=False)

    # =========================
    # الأسئلة الوزارية
    # =========================

    is_ministry = Column(Boolean, default=False, index=True)

    ministry_year = Column(Integer, nullable=True, index=True)

    ministry_round = Column(String(20), nullable=True)

    source = Column(String(100), nullable=True)

    # =========================
    # إحصائيات السؤال
    # =========================

    total_attempts = Column(Integer, default=0, nullable=False)

    correct_attempts = Column(Integer, default=0, nullable=False)

    # =========================
    # إعدادات السؤال
    # =========================

    degree = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    # =========================
    # العلاقات
    # =========================

    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    type_id = Column(
        Integer,
        ForeignKey("question_types.id"),
        nullable=False
    )

    section = relationship(
    "Section",
    back_populates="questions"
    )

    type = relationship(
        "QuestionType",
        back_populates="questions"
    )

    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions"
    )
