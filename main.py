from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models
import schemas

# Create all database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="AI Travel Planner API",
    description="Backend API for AI Travel Planner Project",
    version="1.0"
)

# -----------------------------
# Database Session
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to AI Travel Planner Backend!"
    }


# -----------------------------
# Register User API
# -----------------------------
@app.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully",
        "user_id": new_user.id
    }


# -----------------------------
# Login User API
# -----------------------------
@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.password == user.password
    ).first()

    if db_user:
        return {
            "message": "Login Successful",
            "user_id": db_user.id,
            "name": db_user.name
        }

    return {
        "message": "Invalid Email or Password"
    }
# -----------------------------
# Create Trip API
# -----------------------------
@app.post("/trips")
def create_trip(trip: schemas.TripCreate, db: Session = Depends(get_db)):

    new_trip = models.Trip(
        destination=trip.destination,
        budget=trip.budget,
        days=trip.days,
        user_id=trip.user_id
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {
        "message": "Trip Created Successfully",
        "trip_id": new_trip.id
    }
# -----------------------------
# View All Trips API
# -----------------------------
@app.get("/trips")
def get_all_trips(db: Session = Depends(get_db)):

    trips = db.query(models.Trip).all()

    return trips
# -----------------------------
# Update Trip API
# -----------------------------
@app.put("/trips/{trip_id}")
def update_trip(trip_id: int, trip: schemas.TripCreate, db: Session = Depends(get_db)):

    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()

    if db_trip is None:
        return {"message": "Trip Not Found"}

    db_trip.destination = trip.destination
    db_trip.budget = trip.budget
    db_trip.days = trip.days
    db_trip.user_id = trip.user_id

    db.commit()
    db.refresh(db_trip)

    return {
        "message": "Trip Updated Successfully",
        "trip": db_trip
    }
# -----------------------------
# Delete Trip API
# -----------------------------
@app.delete("/trips/{trip_id}")
def delete_trip(trip_id: int, db: Session = Depends(get_db)):

    db_trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()

    if db_trip is None:
        return {"message": "Trip Not Found"}

    db.delete(db_trip)
    db.commit()

    return {
        "message": "Trip Deleted Successfully"
    }