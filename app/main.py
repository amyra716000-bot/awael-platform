from fastapi import FastAPI
from app.database.session import Base, engine
from app.routes.chapter import router as chapter_router
from app.routes.section import router as section_router
from app.routes.student import router as student_router
from app.models import progress
from app.models import favorite
from app.routes import progress

# ✅ استيراد الموديلات (حتى تنشأ الجداول)
from app.models import (
    user,
    branch,
    subject as subject_model,
    chapter,
    section,
    question,
    plan as plan_model,
    subscription as subscription_model,
    content_view,
)

# ✅ استيراد الروترات
from app.routes import auth, stage, setup, plan, subscription, ai
from app.routes.question import router as question_router
from app.routes.subject import router as subject_router


# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Awael Platform",
)

# تسجيل الروترات
app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(setup.router)
app.include_router(plan.router)
app.include_router(subscription.router)
app.include_router(ai.router)
app.include_router(question_router)
app.include_router(subject_router)
app.include_router(chapter_router)
app.include_router(section_router)
app.include_router(student_router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
