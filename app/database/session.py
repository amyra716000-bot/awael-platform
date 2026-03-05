from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(
    DATABASE_URL,

    # Connection Pool
    pool_size=40,       # اتصالات ثابتة
    max_overflow=80,    # اتصالات اضافية عند الضغط

    pool_pre_ping=True, # يعيد الاتصال اذا انقطع
    pool_recycle=1800   # يعيد تدوير الاتصال
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
