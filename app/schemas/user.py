from pydantic import BaseModel, EmailStr, Field


# =========================
# CREATE USER
# =========================
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


# =========================
# LOGIN
# =========================
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# =========================
# TOKEN RESPONSE
# =========================
class Token(BaseModel):
    access_token: str
    token_type: str


# =========================
# USER RESPONSE
# =========================
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
