from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.database.session import Base, engine
from app.routes import auth, stage, setup
from app.models import user, branch, subject, chapter, section, question

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Awael Platform",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True
    }
)

app.include_router(auth.router)
app.include_router(stage.router)
app.include_router(setup.router)

@app.get("/")
def root():
    return {"message": "Awael Platform API running 🚀"}
