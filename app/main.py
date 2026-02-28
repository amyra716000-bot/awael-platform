from fastapi import FastAPI
from app.database.session import Base, engine

# إنشاء التطبيق
app = FastAPI(
    title="Awael Platform",
)

# ----------------------
# استيراد جميع الموديلات
# ----------------------
from app.models import (
    user,
    branch,
    stage,
    subject,
    chapter,
    section,
    question,
    question_category,
    question_type,
    question_statistics,
    weak_point,
    exam_template,
    exam_attempt,
    exam_attempt_question,
    leaderboard,
    subscription,
    plan,
    favorite,
    device_session,
    content_view,
)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# ----------------------
# استيراد الروترات
# ----------------------
from app.routes import auth, stage as stage_route, setup
from app.routes import plan as plan_route, subscription as subscription_route
from app.routes import ai
from app.routes.question import router as question_router
from app.routes.subject import router as subject_router
from app.routes.chapter import router as chapter_router
from app.routes.section import router as section_router
from app.routes.student import router as student_router
from app.routes.exam import router as exam_router
from app.routes.leaderboard import router as leaderboard_router
from app.routes.analytics import router as analytics_router

# تسجيل الروترات
app.include_router(auth.router)
app.include_router(stage_route.router)
app.include_router(setup.router)
app.include_router(plan_route.router)
app.include_router(subscription_route.router)
app.include_router(ai.router)
app.include_router(question_router)
app.include_router(subject_router)
app.include_router(chapter_router)
app.include_router(section_router)
app.include_router(student_router)
app.include_router(exam_router)
app.include_router(leaderboard_router)
app.include_router(analytics_router)


@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
