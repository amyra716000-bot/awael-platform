from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)

    is_admin = Column(Boolean, default=False)
    subscription_active = Column(Boolean, default=False)
    subscription_expiry = Column(DateTime, default=None)

    created_at = Column(DateTime, default=datetime.utcnow)
