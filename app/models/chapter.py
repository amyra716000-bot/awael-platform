from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.session import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)

    # اسم الفصل
    name = Column(String, nullable=False, index=True)

    # المادة المرتبط بها
    subject_id = Column(
        Integer,
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # ترتيب الفصل
    order = Column(Integer, default=0)

    # حالة الفصل
    is_active = Column(Boolean, default=True)

    # العلاقات
    subject = relationship(
        "Subject",
        back_populates="chapters"
    )

    sections = relationship(
        "Section",
        back_populates="chapter",
        cascade="all, delete"
    )
