from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.session import Base


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    stage_id = Column(Integer, ForeignKey("stages.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    template_id = Column(Integer, ForeignKey("exam_templates.id"), nullable=True)

    scope_type = Column(String, nullable=False)
    # exam / subject / stage / global

    highest_score = Column(Float, default=0)
    average_score = Column(Float, default=0)
    total_exams = Column(Integer, default=0)

    competitive_score = Column(Float, default=0)
    rank_position = Column(Integer, nullable=True)

    last_updated = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
