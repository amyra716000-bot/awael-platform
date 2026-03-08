from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    # العلاقات

    branches = relationship(
        "Branch",
        back_populates="stage",
        cascade="all, delete-orphan"
    )

    subjects = relationship(
        "Subject",
        back_populates="stage",
        cascade="all, delete-orphan"
    )

    users = relationship(
        "User",
        back_populates="stage"
    )

    exam_templates = relationship(
        "ExamTemplate",
        back_populates="stage"
    )
