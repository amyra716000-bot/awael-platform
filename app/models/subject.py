from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Subject(Base):
    __tablename__ = "subjects"

    # =========================
    # Columns
    # =========================

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    stage_id = Column(
        Integer,
        ForeignKey("stages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # Relationships
    # =========================

    stage = relationship(
        "Stage",
        back_populates="subjects"
    )

    chapters = relationship(
        "Chapter",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

    exam_templates = relationship(
        "ExamTemplate",
        back_populates="subject"
    )

    questions = relationship(
        "Question",
        back_populates="subject"
    )
