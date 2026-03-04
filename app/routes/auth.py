from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.security import get_current_admin

router = APIRouter(prefix="/auth", tags=["Auth"])

limiter = Limiter(key_func=get_remote_address)


# =========================
# LOGIN (OAuth2)
# =========================
@router.post("/login")
@limiter.limit("5/minute")
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
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    

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
