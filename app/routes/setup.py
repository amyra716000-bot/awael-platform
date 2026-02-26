from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.core.security import get_password_hash
from pydantic import BaseModel

router = APIRouter(prefix="/setup", tags=["Setup"])


class AdminCreate(BaseModel):
    email: str
    password: str


@router.post("/create-admin")
def create_admin(data: AdminCreate, db: Session = Depends(get_db)):

    # تحقق هل يوجد أدمن مسبقاً
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    hashed_password = get_password_hash(data.password)

    new_admin = User(
        email=data.email,
        password=hashed_password,
        role="admin"
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "Admin created successfully"}
