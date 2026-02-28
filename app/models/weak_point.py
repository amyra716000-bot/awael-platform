from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class WeakPoint(Base):
    __tablename__ = "weak_points"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)

    wrong_answers_count = Column(Integer, default=0)

    user = relationship("User")
    subject = relationship("Subject")
