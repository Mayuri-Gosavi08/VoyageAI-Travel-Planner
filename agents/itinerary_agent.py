"""
===========================================================
                    ITINERARY AGENT
===========================================================

Purpose:
--------
This agent creates a day-wise travel itinerary based on
the user's destination, budget and trip duration.

Workflow:
---------
User Input
      ↓
Read Attractions Dataset
      ↓
Filter Destination
      ↓
Gemini AI
      ↓
Generate Day-wise Itinerary
      ↓
Return Updated State

Input:
------
destination
budget
days

Output:
-------
itinerary_response

===========================================================
"""

from agents.state import AgentState

from langgraph.graph import StateGraph

from services.gemini_service import generate_response

import pandas as pd


# ===========================================================
# Main Processing Function
# ===========================================================

def process(state: AgentState):

    destination = state["destination"]
    budget = state["budget"]
    days = state["days"]

    # -------------------------------------------------------
    # Load Attractions Dataset
    # -------------------------------------------------------

    attractions = pd.read_csv("data/attractions.csv")

    # -------------------------------------------------------
    # Filter Attractions
    # -------------------------------------------------------

    attraction_data = attractions[
        (attractions["destination_name"].str.strip().str.lower() == destination.strip().lower()) |
        (attractions["state"].str.strip().str.lower() == destination.strip().lower())
    ]

    if attraction_data.empty:
        attraction_info = "No attraction information found."
    else:
        attraction_info = attraction_data.to_dict(orient="records")

    # -------------------------------------------------------
    # Prompt for Gemini
    # -------------------------------------------------------

    prompt = f"""
        You are an expert travel planner.

        Destination:
        {destination}

        Trip Duration:
        {days} Days

        Budget:
            ₹{budget}

        Attraction Information:

            {attraction_info}

        Using ONLY the attraction information above,

        Create a complete day-wise itinerary.

        For every day include EXACTLY ONE attraction for:

            Morning

            Afternoon

            Evening

        Do NOT place multiple attractions in the same time slot.

        Mention:

            • Attraction Name

            • Category

            • Approximate Visit Duration

            • Entry Fee

            • Short Reason for visiting

        Ensure the itinerary fits within the user's trip duration and budget.

    At the end give 3 travel tips.
    """
    
    
# -------------------------------------------------------
# Generate Itinerary
# -------------------------------------------------------

    response = generate_response(prompt)

    state["itinerary_response"] = response

    return state


# ===========================================================
# LangGraph Workflow
# ===========================================================

builder = StateGraph(AgentState)

builder.add_node("process", process)

builder.set_entry_point("process")

builder.set_finish_point("process")

itinerary_agent = builder.compile()