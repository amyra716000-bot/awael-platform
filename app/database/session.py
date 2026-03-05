from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")


# =========================
# Engine
# =========================

engine = create_engine(

    DATABASE_URL,

    # Connection Pool
    pool_size=20,
    max_overflow=40,

    # انتظار الاتصال
    pool_timeout=30,

    # يعيد الاتصال إذا انقطع
    pool_pre_ping=True,

    # إعادة تدوير الاتصال
    pool_recycle=1800,

    # SQLAlchemy 2 compatibility
    future=True
)


# =========================
# Session
# =========================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# =========================
# Base
# =========================

Base = declarative_base()


# =========================
# Dependency
# =========================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
