from fastapi import FastAPI
from app.database.session import Base, engine

# استيراد الروترات
from app.routes import auth, stage, setup, plan, subscription

# استيراد المودلز حتى تنشئ الجداول
from app.models import user, branch, subject, chapter, section, question, subscription

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Awael Platform",
)

# إضافة الروترات
app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(setup.router)
app.include_router(plan.router)
app.include_router(subscription.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
