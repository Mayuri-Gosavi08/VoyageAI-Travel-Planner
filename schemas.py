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
# Login Schema
# -------------------------

class UserLogin(BaseModel):
    email: str
    password: str



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
    itinerary: str | None = None
    user_id: int

    class Config:
        from_attributes = True



# -------------------------
# AI Travel Planner Schema
# -------------------------

class TravelPlanRequest(BaseModel):
    destination: str
    days: int
    budget: str
    interest: str



# -------------------------
# Token Response Schema
# -------------------------

class Token(BaseModel):
    access_token: str
    token_type: str