# redeploy force
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.session import engine, Base, SessionLocal

# =========================
# Rate Limiting
# =========================
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

limiter = Limiter(key_func=get_remote_address)

# =========================
# Create App
# =========================
app = FastAPI(
    title="Awael Platform API",
    description="Educational platform API for Iraqi students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# =========================
# CORS
# =========================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Rate Limit
# =========================
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# =========================
# Import Models
# =========================
from app import models

# =========================
# Startup Event
# =========================
@app.on_event("startup")
def startup():

    # إنشاء الجداول إذا لم تكن موجودة
    Base.metadata.create_all(bind=engine)

    # إضافة عمود score إذا لم يكن موجود
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE exam_attempts
                ADD COLUMN IF NOT EXISTS score INTEGER DEFAULT 0;
            """))
            conn.commit()
    except Exception as e:
        print("Migration skipped:", e)
