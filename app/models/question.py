from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.session import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)      # نص السؤال
    answer = Column(Text, nullable=False)       # الجواب

    is_ministry = Column(Boolean, default=False)    # هل هو وزاري؟
    ministry_year = Column(Integer, nullable=True)  # سنة الامتحان (مثلاً 2023)

    is_important = Column(Boolean, default=False)   # سؤال مهم

    section_id = Column(Integer, ForeignKey("sections.id"))

    section = relationship("Section", backref="questions")
