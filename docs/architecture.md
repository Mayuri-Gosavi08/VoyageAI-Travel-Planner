# System Architecture

## Overview

VoyageAI Travel Planner is built using a frontend-backend architecture.

The frontend provides the user interface, while the FastAPI backend handles authentication, database operations, trip management, and communication with the AI agent system.

## Architecture Flow

```text
User
  ↓
Streamlit Frontend
  ↓
FastAPI Backend
  ↓
Authentication + Database
  ↓
Master Agent
  ↓
Specialized Agents
  ↓
Final Travel Plan
  ↓
Database
  ↓
Frontend

Frontend

The frontend is developed using Streamlit.

It allows users to:

Register and log in.
Select a travel destination.
Select travel dates/duration.
Enter a travel budget.
Enter their interests.
Generate an AI-based travel plan.
View their saved trips.

The main frontend file is:
frontend/app3.py

Backend

The backend is developed using FastAPI.

The main backend file is:

backend/main.py

The backend provides APIs for:

User registration
User login
Trip creation
Viewing trips
Updating trips
Deleting trips
Generating AI travel plans
Viewing the logged-in user's trips
Authentication

The application uses authentication to protect user-specific travel data.

During registration, the user's password is hashed before it is stored.

During login, the entered password is verified and an access token is generated.

The application uses:

Password hashing
Password verification
Access tokens
Bearer authentication
Database

The project uses SQLAlchemy for database operations.

The backend creates the required database tables using:

Base.metadata.create_all(bind=engine)

Trip information is stored in the database, including:

Destination
Budget
Number of days
User ID
Generated itinerary
AI Agent Integration

The /plan-trip API creates the initial travel-planning state and sends it to the Master Agent.

The Master Agent then runs the specialized agents sequentially:

Master Agent
     ↓
Weather Agent
     ↓
Budget Agent
     ↓
Hotel Agent
     ↓
Restaurant Agent
     ↓
Itinerary Agent

The final result is saved as a trip in the database and returned to the frontend.

Main API Endpoints
Method	Endpoint	Purpose
GET	/	Backend welcome message
POST	/register	Register a new user
POST	/login	Authenticate a user
POST	/trips	Create a trip
GET	/trips	View all trips
PUT	/trips/{trip_id}	Update a trip
DELETE	/trips/{trip_id}	Delete a trip
POST	/plan-trip	Generate an AI travel plan
GET	/my-trips	View trips of the logged-in user
Technologies Used
Python
Streamlit
FastAPI
SQLAlchemy
SQLite
LangGraph
Gemini API
Pandas