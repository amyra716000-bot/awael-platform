from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database.session import Base


class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    stage_id = Column(Integer, ForeignKey("stages.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    highest_score = Column(Float, default=0)
    average_score = Column(Float, default=0)
    total_exams = Column(Integer, default=0)

    competitive_score = Column(Float, default=0)

    user = relationship("User")
    stage = relationship("Stage")
    subject = relationship("Subject")
