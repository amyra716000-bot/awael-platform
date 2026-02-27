from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from app.database.session import Base


class ContentView(Base):
    __tablename__ = "content_views"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("questions.id"))  # ← هذا التعديل

    views_count = Column(Integer, default=0)
    last_viewed_at = Column(DateTime, default=datetime.utcnow)
