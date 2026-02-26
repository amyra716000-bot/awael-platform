from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

router = APIRouter(prefix="/setup", tags=["Setup"])

@router.post("/create-admin")
def create_admin(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.role == "admin").first()
    if existing:
        raise HTTPException(status_code=400, detail="Admin already exists")

    admin = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role="admin"
    )

    db.add(admin)
    db.commit()

    return {"message": "Admin created successfully"}
