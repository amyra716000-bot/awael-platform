from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    subject_id = Column(Integer, ForeignKey("subjects.id"))

    subject = relationship("Subject", backref="chapters")
