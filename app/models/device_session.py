from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from datetime import datetime
from app.database.session import Base


class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    ip_address = Column(String)
    device_fingerprint = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
