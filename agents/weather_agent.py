from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from services.weather_service import get_weather
from services.gemini_service import generate_response

class AgentState(TypedDict):
    city: str
    weather: dict
    response: str
    
    
def process(state: AgentState):

    city = state["city"]

    weather = get_weather(city)

    state["weather"] = weather

    prompt = f"""
    You are an expert travel planner.

    City: {city}

    Current Weather:
    {weather}

    Give exactly 5 travel recommendations.

    Include:
    - What to wear
    - Whether to carry an umbrella
    - Best places to visit in this weather
    - Safety precautions
    - Local travel tips

    Keep the response simple and user-friendly.
    """
    
    response = generate_response(prompt)

    state["response"] = response

    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
weather_agent = graph.compile()