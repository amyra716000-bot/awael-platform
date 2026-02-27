from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # نوع القسم (تعريف / تعليل / مسائل / ...)
    type = Column(String, nullable=False)

    chapter_id = Column(Integer, ForeignKey("chapters.id"))

    chapter = relationship("Chapter", backref="sections")
