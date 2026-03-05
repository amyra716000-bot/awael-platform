from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)

    # اسم الفرع
    name = Column(String, nullable=False, index=True)

    # المرحلة المرتبط بها
    stage_id = Column(
        Integer,
        ForeignKey("stages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ترتيب الفرع
    order = Column(Integer, default=0)

    # حالة الفرع
    is_active = Column(Boolean, default=True)

    # العلاقة مع Stage
    stage = relationship(
        "Stage",
        back_populates="branches"
    )

    # العلاقة مع المواد
    subjects = relationship(
        "Subject",
        back_populates="branch",
        cascade="all, delete"
    )
