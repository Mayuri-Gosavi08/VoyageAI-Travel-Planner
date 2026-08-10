# ==========================================================
#                MASTER AGENT
# ==========================================================
# This agent acts as the central controller of the
# AI Travel Planner.
#
# Responsibilities:
# 1. Receive user input.
# 2. Send the same state to every specialized agent.
# 3. Collect all responses.
# 4. Return the final state.
# ==========================================================

from agents.state import AgentState

from agents.weather_agent import weather_agent
from agents.budget_agent import budget_agent
from agents.hotel_agent import hotel_agent
from agents.restaurant_agent import restaurant_agent
from agents.itinerary_agent import itinerary_agent


def run_master_agent(state: AgentState):

    # ------------------------------------
    # Step 1 : Weather Agent
    # ------------------------------------
    print("Running Weather Agent...")
    state = weather_agent.invoke(state)

    # ------------------------------------
    # Step 2 : Budget Agent
    # ------------------------------------
    print("Running Budget Agent...")
    state = budget_agent.invoke(state)

    # ------------------------------------
    # Step 3 : Hotel Agent
    # ------------------------------------
    print("Running Hotel Agent...")
    state = hotel_agent.invoke(state)

    # ------------------------------------
    # Step 4 : Restaurant Agent
    # ------------------------------------
    print("Running Restaurant Agent...")
    state = restaurant_agent.invoke(state)

    # ------------------------------------
    # Step 5 : Itinerary Agent
    # ------------------------------------
    print("Running Itinerary Agent...")
    state = itinerary_agent.invoke(state)

    return state