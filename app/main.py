from fastapi import FastAPI
from app.database.session import Base, engine
from app.routes import auth
from app.models import user
from app.models import stage
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Awael Platform")

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
