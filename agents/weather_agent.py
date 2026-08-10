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


def process(state: AgentState):

    destination = state["destination"]

    weather = get_weather(destination)

    state["weather"] = weather

    state["response"] = {
        "message": "Weather information retrieved successfully.",
        "recommendations": [
            f"Check the current weather before going out in {destination}.",
            "Wear clothing suitable for the current temperature.",
            "Carry an umbrella if rain is expected.",
            "Stay hydrated and take normal travel safety precautions.",
            "Plan outdoor activities according to the weather conditions."
        ]
    }

    return state


graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.add_edge(START, "process")
graph.add_edge("process", END)

weather_agent = graph.compile()