from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# Register
# =========================
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role="student"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# =========================
# Login (Access + Refresh)
# =========================
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================
# Refresh Access Token
# =========================
@router.post("/refresh")
def refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        email = payload.get("sub")

        new_access_token = create_access_token({"sub": email})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
