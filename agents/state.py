from typing import TypedDict

class AgentState(TypedDict):

    # User Inputs
    destination: str
    budget: int
    days: int

    # Weather
    weather: dict
    response: str

    # Budget
    budget_response: str

    # Hotels
    hotel_response: str

    # Restaurants
    restaurant_response: str

    # Itinerary
    itinerary_response: str