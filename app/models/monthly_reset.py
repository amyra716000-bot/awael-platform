from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from app.database.session import Base


class MonthlyReset(Base):
    __tablename__ = "monthly_resets"

    id = Column(Integer, primary_key=True, index=True)
    last_reset = Column(DateTime, default=datetime.utcnow)
