from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
import os

router = APIRouter(prefix="/setup", tags=["Setup"])


SETUP_SECRET = os.getenv("SETUP_SECRET", "CHANGE_ME_SETUP_SECRET")


# ==========================================
# CREATE FIRST ADMIN
# ==========================================
@router.post("/create-admin")
def create_admin(
    user: UserCreate,
    setup_secret: str,
    db: Session = Depends(get_db)
):

    # حماية endpoint
    if setup_secret != SETUP_SECRET:
        raise HTTPException(
            status_code=403,
            detail="Invalid setup secret"
        )

    # تحقق إذا يوجد أدمن
    existing_admin = db.query(User).filter(
        User.role == "admin"
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    # تحقق من البريد
    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already used"
        )

    admin = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "message": "Admin created successfully",
        "admin_email": admin.email
    }
