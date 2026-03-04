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

    # يعيد الاتصال إذا انقطع
    pool_pre_ping=True,

    # يغلق الاتصال القديم
    pool_recycle=1800
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
