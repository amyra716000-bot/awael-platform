from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base
from app.models.question_category import question_category_link


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    # 🔹 نص السؤال
    content = Column(Text, nullable=False)

    # 🔹 الجواب المختصر
    answer = Column(Text, nullable=False)

    # 🔹 شرح الحل (مهم للطلاب)
    explanation = Column(Text, nullable=True)

    # 🔹 صورة السؤال (للرياضيات / الفيزياء)
    image_url = Column(String, nullable=True)

    # =========================================
    # معلومات الوزاري
    # =========================================

    is_ministry = Column(Boolean, default=False)

    ministry_year = Column(Integer, nullable=True)

    ministry_round = Column(String(20), nullable=True)
    # مثال:
    # first
    # second
    # third

    # =========================================
    # سؤال مهم
    # =========================================

    is_important = Column(Boolean, default=False)

    # =========================================
    # مستوى الصعوبة
    # =========================================

    difficulty = Column(String(10), default="medium")
    # easy
    # medium
    # hard

    # =========================================
    # ترتيب السؤال داخل القسم
    # =========================================

    order = Column(Integer, default=0)

    # =========================================
    # إحصائيات السؤال
    # =========================================

    total_attempts = Column(Integer, default=0)

    correct_attempts = Column(Integer, default=0)

    # =========================================
    # العلاقات
    # =========================================

    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    type_id = Column(Integer, ForeignKey("question_types.id"), nullable=False)

    # 🔹 علاقة مع Section
    section = relationship(
        "Section",
        backref="questions"
    )

    # 🔹 علاقة Many-to-Many مع Category
    categories = relationship(
        "QuestionCategory",
        secondary=question_category_link,
        back_populates="questions"
    )

    # 🔹 علاقة مع QuestionType
    type = relationship(
        "QuestionType",
        back_populates="questions"
    )
