from fastapi import FastAPI
from app.database.session import Base, engine

# routers
from app.routes import auth, stage, setup, plan, subscription, ai

# models (فقط لإنشاء الجداول)
from app.models import user, branch, subject, chapter, section, question

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Awael Platform",
)

app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(setup.router)
app.include_router(plan.router)
app.include_router(subscription.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
