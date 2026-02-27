from sqlalchemy import Column, Integer, String
from app.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="student")

    # 🆕 عداد الأسئلة المجانية
    free_ai_used = Column(Integer, default=0)
