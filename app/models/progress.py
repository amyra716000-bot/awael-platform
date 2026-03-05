from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
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

    # احصائيات التقدم
    correct_answers = Column(Integer, default=0)

    total_attempts = Column(Integer, default=0)

    # منع التكرار لنفس المستخدم والقسم
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "section_id",
            name="unique_user_section_progress"
        ),
    )

    # =========================
    # العلاقات
    # =========================

    user = relationship(
        "User",
        back_populates="progress"
    )

    section = relationship(
        "Section"
    )
