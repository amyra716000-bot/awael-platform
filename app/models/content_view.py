from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint, Index
from datetime import datetime
from app.database.session import Base


class ContentView(Base):
    __tablename__ = "content_views"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    content_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False
    )

    views_count = Column(Integer, default=0)

    last_viewed_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (

        # منع تكرار نفس السجل
        UniqueConstraint(
            "user_id",
            "content_id",
            name="unique_user_content_view"
        ),

        # تحسين الأداء
        Index(
            "idx_content_views_user",
            "user_id"
        ),
    )
