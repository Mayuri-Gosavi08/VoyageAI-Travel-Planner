"""
===========================================================
                    RESTAURANT AGENT
===========================================================

Purpose:
--------
This agent recommends restaurants based on the user's
destination and budget.

Workflow:
---------
User Input
      ↓
Read Restaurant Dataset
      ↓
Filter Restaurants by Destination
      ↓
Gemini AI
      ↓
Restaurant Recommendations
      ↓
Return Updated State

Input:
------
destination
budget

Output:
-------
restaurant_response

===========================================================
"""

from typing import TypedDict

from langgraph.graph import StateGraph

from services.gemini_service import generate_response

import pandas as pd


# ===========================================================
# Agent State
# Stores all information exchanged between LangGraph nodes.
# ===========================================================

class AgentState(TypedDict):
    destination: str
    budget: int
    restaurant_response: str


# ===========================================================
# Main Processing Function
#
# Steps:
# 1. Read destination and budget.
# 2. Load restaurant dataset.
# 3. Filter matching restaurants.
# 4. Send restaurant data to Gemini.
# 5. Receive recommendations.
# 6. Store response.
# ===========================================================

def process(state: AgentState):

    destination = state["destination"]
    budget = state["budget"]

    # -------------------------------------------------------
    # Load Restaurant Dataset
    # -------------------------------------------------------

    restaurants = pd.read_csv("data/restaurants.csv")

    # -------------------------------------------------------
    # Filter restaurants for selected destination
    # -------------------------------------------------------

    restaurant_data = restaurants[
        (restaurants["city"].str.lower() == destination.lower()) |
        (restaurants["state"].str.lower() == destination.lower())
    ]
    
    

    if restaurant_data.empty:
        restaurant_info = "No restaurant information found."
    else:
        restaurant_info = restaurant_data.to_dict(orient="records")

    # -------------------------------------------------------
    # Prepare Prompt for Gemini AI
    # -------------------------------------------------------

    prompt = f"""
        You are an expert travel planner.

        Destination:
        {destination}

        User Budget:
        ₹{budget}

        Restaurant Information:
        {restaurant_info}

        Using ONLY the restaurant information above,

        Recommend:

            1. Top 5 restaurants.
            2. Famous cuisines.
            3. Approximate cost for two.
            4. Veg / Non-Veg information.
            5. Ratings.
            6. Best restaurant overall. 
            7. Explain why it suits the user's budget.
    """

    # -------------------------------------------------------
    # Generate Restaurant Recommendation
    # -------------------------------------------------------

    response = generate_response(prompt)

    # -------------------------------------------------------
    # Save Response
    # -------------------------------------------------------

    state["restaurant_response"] = response

    return state


# ===========================================================
# LangGraph Workflow
# ===========================================================

builder = StateGraph(AgentState)

# Register processing node
builder.add_node("process", process)

# Define graph starting point
builder.set_entry_point("process")

# Define graph ending point
builder.set_finish_point("process")

# Compile graph
restaurant_agent = builder.compile()