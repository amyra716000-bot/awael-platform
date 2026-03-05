from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.session import Base
import enum


class SectionType(str, enum.Enum):

    # =========================
    # الاقسام العادية
    # =========================

    definitions = "definitions"
    explanations = "explanations"
    problems = "problems"
    multiple_choice = "multiple_choice"
    drawings = "drawings"
    essay = "essay"
    grammar = "grammar"

    # =========================
    # الاقسام الوزارية
    # =========================

    ministry_definitions = "ministry_definitions"
    ministry_reasons = "ministry_reasons"
    ministry_problems = "ministry_problems"
    ministry_mcq = "ministry_mcq"
    ministry_essay = "ministry_essay"
    ministry_grammar = "ministry_grammar"


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)

    # اسم القسم
    name = Column(
        String,
        nullable=False,
        index=True
    )

    # نوع القسم
    type = Column(
        Enum(SectionType),
        nullable=False
    )

    # الفصل المرتبط
    chapter_id = Column(
        Integer,
        ForeignKey("chapters.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ترتيب القسم داخل الفصل
    order = Column(
        Integer,
        default=0
    )

    # =========================
    # العلاقات
    # =========================

    chapter = relationship(
        "Chapter",
        chapter = relationship(
    "Chapter",
    back_populates="sections"
        )
        lazy="selectin"
    )

    questions = relationship(
        "Question",
        back_populates="section",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # =========================
    # Debug
    # =========================

    def __repr__(self):
        return f"<Section id={self.id} name={self.name} type={self.type}>"
