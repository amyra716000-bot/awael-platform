import os
from fastapi import FastAPI
from sqlalchemy import text

from app.database.session import engine, Base
from fastapi.middleware.cors import CORSMiddleware

# =========================
# Rate Limiting
# =========================
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware


# =========================
# Create Limiter
# =========================
limiter = Limiter(key_func=get_remote_address)


# =========================
# Create App
# =========================
app = FastAPI(
    title="Awael Platform API",
    version="1.0.0",
    docs_url=None if os.getenv("ENV") == "production" else "/docs",
    redoc_url=None if os.getenv("ENV") == "production" else "/redoc",
    openapi_url=None if os.getenv("ENV") == "production" else "/openapi.json",
)
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Add Rate Limit Middleware
# =========================
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {
        "status": "running",
        "platform": "Awael Platform",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# =========================
# Import Models (حتى تنشأ الجداول)
# =========================
from app import models


# =========================
# Create Tables
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# Import Routers
# =========================
from app.routes import (
    auth,
    stage,
    setup,
    plan,
    subscription,
    ai,
    exam,
)

from app.routes.question import router as question_router
from app.routes.subject import router as subject_router
from app.routes.chapter import router as chapter_router
from app.routes.section import router as section_router
from app.routes.student import router as student_router
from app.admin_exam_templates import router as admin_exam_templates_router


# =========================
# Register Routers
# =========================
app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(setup.router)
app.include_router(plan.router)
app.include_router(subscription.router)
app.include_router(ai.router)
app.include_router(exam.router)

app.include_router(question_router)
app.include_router(subject_router)
app.include_router(chapter_router)
app.include_router(section_router)
app.include_router(student_router)
app.include_router(admin_exam_templates_router)

