# =========================
# Load ENV
# =========================

from dotenv import load_dotenv
load_dotenv()

# =========================
# Imports
# =========================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.session import engine, Base

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
# Import Routers
# =========================

from app.routes import auth
from app.routes import question
from app.routes import exam
from app.routes import admin

app.include_router(auth.router)
app.include_router(question.router)
app.include_router(exam.router)
app.include_router(admin.router)

# =========================
# Startup Event
# =========================

@app.on_event("startup")
def startup():

    # إنشاء الجداول
    Base.metadata.create_all(bind=engine)

    # إصلاح قاعدة البيانات (score column)
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                ALTER TABLE exam_attempts
                ADD COLUMN IF NOT EXISTS score INTEGER DEFAULT 0;
            """))
            conn.commit()
    except Exception as e:
        print("Migration skipped:", e)

# =========================
# Health Check
# =========================

@app.get("/health")
def health():
    return {"status": "ok"}
