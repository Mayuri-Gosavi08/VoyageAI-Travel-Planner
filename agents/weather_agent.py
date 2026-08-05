from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from services.weather_service import get_weather
from services.gemini_service import ask_gemini

class AgentState(TypedDict):
    city: str
    weather: dict
    response: str
    
    
def process(state: AgentState):

    city = state["city"]

    weather = get_weather(city)

    state["weather"] = weather

    prompt = f"""
    You are a travel assistant.

    Weather Information

    {weather}

    Give travelling advice in 5 points.
    """

    answer = ask_gemini(prompt)

    state["response"] = answer

    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
weather_agent = graph.compile()