from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.session import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)

    # اسم المرحلة
    name = Column(String, nullable=False, unique=True)

    # العلاقة مع الفروع
    branches = relationship("Branch", back_populates="stage")

    # العلاقة مع المواد
    subjects = relationship("Subject", back_populates="stage")
