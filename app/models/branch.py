from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)

    # اسم الفرع
    name = Column(String, nullable=False)

    # المرحلة المرتبط بها
    stage_id = Column(Integer, ForeignKey("stages.id"), nullable=False)

    # العلاقة مع Stage
    stage = relationship("Stage", back_populates="branches")

    # العلاقة مع المواد
    subjects = relationship("Subject", back_populates="branch")
