from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class Stage(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True, index=True)

    # اسم المرحلة
    name = Column(String, nullable=False, unique=True, index=True)

    # ترتيب المرحلة
    order = Column(Integer, default=0)

    # حالة المرحلة
    is_active = Column(Boolean, default=True)

    # العلاقة مع الفروع
    branches = relationship(
        "Branch",
        back_populates="stage",
        cascade="all, delete"
    )

    # العلاقة مع المواد
    subjects = relationship(
        "Subject",
        back_populates="stage",
        cascade="all, delete"
    )
