from pydantic import BaseModel


# -------------------------
# User Registration
# -------------------------

class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    department: str | None = None


# -------------------------
# User Response
# -------------------------

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    department: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


# -------------------------
# Login Token
# -------------------------

class Token(BaseModel):
    access_token: str
    token_type: str