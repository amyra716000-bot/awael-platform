from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False
    )

    subject = relationship(
        "Subject",
        back_populates="chapters"
    )

    sections = relationship(
        "Section",
        back_populates="chapter",
        cascade="all, delete-orphan"
    )
