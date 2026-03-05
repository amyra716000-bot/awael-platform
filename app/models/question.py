from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    # =========================
    # محتوى السؤال
    # =========================

    content = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    explanation = Column(Text, nullable=True)

    # =========================
    # خصائص السؤال
    # =========================

    difficulty = Column(
        String(10),
        default="medium",
        index=True
    )

    is_important = Column(
        Boolean,
        default=False,
        index=True
    )

    is_active = Column(
        Boolean,
        default=True,
        index=True
    )

    degree = Column(Integer, default=1)

    # =========================
    # الأسئلة الوزارية
    # =========================

    is_ministry = Column(
        Boolean,
        default=False,
        index=True
    )

    ministry_year = Column(
        Integer,
        nullable=True,
        index=True
    )

    ministry_round = Column(
        String(20),
        nullable=True
    )

    source = Column(
        String(100),
        nullable=True
    )

    # =========================
    # إحصائيات السؤال
    # =========================

    total_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

    correct_attempts = Column(
        Integer,
        default=0,
        nullable=False
    )

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
        nullable=False,
        index=True
    )

    section = relationship(
        "Section",
        back_populates="questions",
        lazy="selectin"
    )

    type = relationship(
        "QuestionType",
        back_populates="questions",
        lazy="selectin"
    )

    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions",
        lazy="selectin"
    )

    # =========================
    # تحسين الأداء
    # =========================

    __table_args__ = (

        Index(
            "idx_question_section_type",
            "section_id",
            "type_id"
        ),

        Index(
            "idx_question_ministry",
            "is_ministry",
            "ministry_year"
        ),

    )
