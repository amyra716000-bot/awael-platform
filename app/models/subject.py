from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)

    # اسم المادة
    name = Column(String, nullable=False)

    # المرحلة
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)

    # الفرع (اختياري لأن بعض المراحل لا تحتوي فروع)
    branch_id = Column(Integer, ForeignKey("branches.id"), nullable=True)

    # العلاقات
    stage = relationship("Stage", back_populates="subjects")

    branch = relationship("Branch", back_populates="subjects")

    chapters = relationship("Chapter", back_populates="subject")
