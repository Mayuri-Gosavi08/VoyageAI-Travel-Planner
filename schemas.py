from pydantic import BaseModel

# -------------------------
# User Schemas
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------------------------
# Trip Schemas
# -------------------------

class TripCreate(BaseModel):
    destination: str
    budget: float
    days: int
    user_id: int


class TripResponse(BaseModel):
    id: int
    destination: str
    budget: float
    days: int
    user_id: int

    class Config:
        from_attributes = True
        # -------------------------
# Login Schema
# -------------------------

class UserLogin(BaseModel):
    email: str
    password: str