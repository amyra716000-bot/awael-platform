from fastapi import FastAPI
from app.database.session import Base, engine

# =========================
# استيراد الموديلات (لإنشاء الجداول)
# =========================
from app.models import (
    user,
    stage,
    branch,
    subject,
    chapter,
    section,
    question,
    plan,
    subscription,
    exam_template,
    exam_attempt,
    exam_attempt_question,
    leaderboard,
    question_statistics,
    favorite,
    content_view,
)

# =========================
# استيراد الروترات
# =========================
from app.routes import (
    auth,
    stage,
    subject,
    chapter,
    section,
    question,
    student,
    plan,
    subscription,
    ai,
    exam,
    leaderboard,
)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Awael Platform API")

# =========================
# تسجيل الروترات
# =========================
app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(subject.router)
app.include_router(chapter.router)
app.include_router(section.router)
app.include_router(question.router)
app.include_router(student.router)
app.include_router(plan.router)
app.include_router(subscription.router)
app.include_router(ai.router)
app.include_router(exam.router)
app.include_router(leaderboard.router)


@app.get("/")
def root():
    return {"message": "Awael Platform Running 🚀"}
