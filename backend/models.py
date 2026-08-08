from sqlalchemy import Column, Integer, String, ForeignKey
from backend.database import Base


# -------------------------
# User Table
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)



# -------------------------
# Trip Table
# -------------------------

class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    destination = Column(String(100), nullable=False)

    # Budget can store values like:
    # low / medium / high
    budget = Column(String(50))

    days = Column(Integer)

    # AI generated travel plan
    itinerary = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))