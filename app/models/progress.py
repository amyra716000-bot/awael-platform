from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.database.session import Base


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)

    # المستخدم
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # القسم
    section_id = Column(
        Integer,
        ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False
    )

    # إحصائيات التقدم
    correct_answers = Column(Integer, default=0)
    total_attempts = Column(Integer, default=0)

    # القيود
    __table_args__ = (

        # منع تكرار سجل التقدم
        UniqueConstraint(
            "user_id",
            "section_id",
            name="unique_user_section_progress"
        ),

        # تحسين الأداء
        Index(
            "idx_user_progress",
            "user_id",
            "section_id"
        ),
    )

    # العلاقات
    user = relationship(
        "User",
        back_populates="progress",
        lazy="selectin"
    )

    section = relationship(
        "Section",
        lazy="selectin"
    )
