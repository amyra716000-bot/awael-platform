from fastapi import FastAPI
from app.database.session import Base, engine
from app.routes import auth
from app.routes import stage
from app.models import user
from app.models import stage
from app.models import branch
from app.models import subject
from app.models import chapter
from app.models import section
from app.models import question
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Awael Platform")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
