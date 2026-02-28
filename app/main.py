from fastapi import FastAPI
from app.database.session import engine, Base

# ✅ استيراد كل الموديلات حتى تنشأ الجداول
from app import models

# ✅ استيراد كل الروترات
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


# إنشاء التطبيق
app = FastAPI(
    title="Awael Platform API",
    version="1.0.0"
)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)


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


@app.get("/")
def root():
    return {
        "status": "running",
        "platform": "Awael Platform",
        "version": "1.0.0"
    }
