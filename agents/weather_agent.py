"""
===========================================================
                WEATHER AGENT
===========================================================

Purpose:
--------
This agent retrieves the current weather of a destination
using the Weather Service and asks Gemini AI to generate
travel recommendations based on the weather conditions.

Workflow:
---------
User Input
     ↓
Weather Service
     ↓
Current Weather Data
     ↓
Gemini AI
     ↓
Travel Advice
     ↓
Return Updated State

Input:
------
city

Output:
-------
weather
response

===========================================================
"""

from agents.state import AgentState

from langgraph.graph import StateGraph, START, END

from services.weather_service import get_weather
from services.gemini_service import generate_response


def process(state: AgentState):

    destination = state["destination"]

    weather = get_weather(destination)


    state["weather"] = weather

    prompt = f"""
    You are an expert travel planner.

    Destination: {destination}

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