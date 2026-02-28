from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
import os

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# LOGIN (OAuth2)
# =========================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =========================
# MAKE ADMIN (Protected)
# =========================
@router.post("/make-admin")
def make_admin(
    email: str,
    x_admin_key: str = Header(None),
    db: Session = Depends(get_db)
):
    secret_key = os.getenv("ADMIN_PROMOTE_KEY")

    if not secret_key:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_PROMOTE_KEY not configured"
        )

    if x_admin_key != secret_key:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = "admin"
    db.commit()

    return {
        "message": f"{email} promoted to admin successfully"
    }
