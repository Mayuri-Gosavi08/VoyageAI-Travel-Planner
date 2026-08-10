# ==========================================================
#                 VOYAGE AI TRAVEL PLANNER
# ==========================================================
# File : budget_agent.py
#
# Purpose:
# This agent estimates the travel budget using
# activity, food and transport datasets.
#
# Workflow:
#
# User Budget
#        │
#        ▼
# Read CSV Files
#        │
#        ▼
# Create Prompt
#        │
#        ▼
# Gemini AI
#        │
#        ▼
# Budget Recommendation
#
# ==========================================================

import pandas as pd

from agents.state import AgentState

from langgraph.graph import StateGraph, END

from services.gemini_service import generate_response


# ==========================================================
#               PROCESS FUNCTION
# ==========================================================
        
def process(state: AgentState):

    # ----------------------------------------
    # Read user information
    # ----------------------------------------

    destination = state["destination"]
    budget = state["budget"]
    days = state["days"]


    # ----------------------------------------
    # Load all required datasets
    # ----------------------------------------

    activity_df = pd.read_csv("data/activity_cost.csv")

    food_df = pd.read_csv("data/food_cost.csv")

    transport_df = pd.read_csv("data/transport_cost.csv")


    # ----------------------------------------
    # Convert datasets into readable text
    # ----------------------------------------

    activity_data = activity_df.to_string(index=False)

    food_data = food_df.to_string(index=False)

    transport_data = transport_df.to_string(index=False)


    # ----------------------------------------
    # Prompt Engineering
    # ----------------------------------------

    prompt = f"""
        You are an AI Travel Budget Planner.

        User Details

        Destination : {destination}

        Budget : ₹{budget}

        Trip Duration : {days} days

        Activity Dataset

        {activity_data}

        Food Dataset

        {food_data}

        Transport Dataset

        {transport_data}

        Using these datasets,

        Estimate:

            1. Activity Cost

            2. Food Cost

            3. Transport Cost

            4. Total Estimated Budget

            5. Whether the user's budget is sufficient

            6. Money Saving Tips

    Return a clean travel budget report.
    """


    # ----------------------------------------
    # Generate Gemini Response
    # ----------------------------------------

    response = generate_response(prompt)


    # ----------------------------------------
    # Save response inside LangGraph State
    # ----------------------------------------

    state["budget_response"] = response

    return state


# ==========================================================
#               BUILD LANGGRAPH
# ==========================================================

graph = StateGraph(AgentState)

graph.add_node("process", process)

graph.set_entry_point("process")

graph.add_edge("process", END)

budget_agent = graph.compile()