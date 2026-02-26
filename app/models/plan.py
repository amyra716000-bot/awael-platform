from sqlalchemy import Column, Integer, String, Boolean
from app.database.session import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)

    daily_question_limit = Column(Integer, default=0)
    daily_ai_limit = Column(Integer, default=0)

    access_exams = Column(Boolean, default=False)
    access_leaderboard = Column(Boolean, default=False)
    access_schedule = Column(Boolean, default=False)
    access_essay = Column(Boolean, default=False)
