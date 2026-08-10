from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import Base, engine, SessionLocal
from backend import models
from backend import schemas

from services.gemini_service import generate_response
from agents.master_agent import run_master_agent
from backend.auth import hash_password, verify_password, create_access_token
from backend.dependencies import get_current_user


# Create database tables
Base.metadata.create_all(bind=engine)


# FastAPI App
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
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()


    if existing_user:
        return {
            "message": "Email already registered"
        }


    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message": "User Registered Successfully",
        "user_id": new_user.id
    }




# -----------------------------
# Login User API (Swagger OAuth2)
# -----------------------------
@app.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()


    if db_user and verify_password(
        form_data.password,
        db_user.password
    ):

        token = create_access_token(
            {
                "user_id": db_user.id,
                "email": db_user.email
            }
        )


        return {

            "message": "Login Successful",
            "access_token": token,
            "token_type": "bearer"

        }


    raise HTTPException(
        status_code=401,
        detail="Invalid Email or Password"
    )





# -----------------------------
# Create Trip API
# -----------------------------
@app.post("/trips")
def create_trip(
    trip: schemas.TripCreate,
    db: Session = Depends(get_db)
):

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
def get_all_trips(
    db: Session = Depends(get_db)
):

    trips = db.query(models.Trip).all()

    return trips





# -----------------------------
# Update Trip API
# -----------------------------
@app.put("/trips/{trip_id}")
def update_trip(
    trip_id: int,
    trip: schemas.TripCreate,
    db: Session = Depends(get_db)
):

    db_trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()


    if db_trip is None:

        return {
            "message": "Trip Not Found"
        }


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
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db)
):

    db_trip = db.query(models.Trip).filter(
        models.Trip.id == trip_id
    ).first()


    if db_trip is None:

        return {
            "message": "Trip Not Found"
        }


    db.delete(db_trip)
    db.commit()


    return {

        "message": "Trip Deleted Successfully"

    }





# -----------------------------
# AI Travel Planner API
# -----------------------------
@app.post("/plan-trip")
def plan_trip(
    request: schemas.TravelPlanRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    initial_state = {
        "destination": request.destination,
        "budget": request.budget,
        "days": request.days,

        "weather": {},
        "response": "",

        "budget_response": "",
        "hotel_response": "",
        "restaurant_response": "",
        "itinerary_response": ""
    }

    result = run_master_agent(initial_state)

    new_trip = models.Trip(
        destination=request.destination,
        budget=str(request.budget),
        days=request.days,
        itinerary=str(result),
        user_id=user_id
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return {
        "message": "AI Trip Plan Generated and Saved Successfully",
        "trip_id": new_trip.id,
        "destination": new_trip.destination,
        "itinerary": result
    }
    
    
# -----------------------------
# Logged User Trips
# -----------------------------
@app.get("/my-trips")
def get_my_trips(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):

    trips = db.query(models.Trip).filter(
        models.Trip.user_id == user_id
    ).all()


    return trips