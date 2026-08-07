# ==========================================================
#                 VOYAGE AI TRAVEL PLANNER
# ==========================================================
# File : hotel_agent.py
#
# Purpose:
# This agent recommends hotels based on
# destination and user budget.
#
# Workflow:
#
# User Destination
#         │
#         ▼
# Read Destination Dataset
#         │
#         ▼
# Gemini AI
#         │
#         ▼
# Hotel Recommendation
#
# ==========================================================

import pandas as pd

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from services.gemini_service import generate_response


# ==========================================================
#               AGENT STATE
# ==========================================================

class AgentState(TypedDict):

    destination: str

    budget: int

    hotel_response: str


# ==========================================================
#               LOAD DATASET
# ==========================================================

india_df = pd.read_csv("data/india_destinations.csv")

international_df = pd.read_csv("data/international_destinations.csv")


# ==========================================================
#               PROCESS FUNCTION
# ==========================================================

def process(state: AgentState):

    destination = state["destination"]

    budget = state["budget"]


    # ----------------------------------------
    # Search destination in Indian dataset
    # ----------------------------------------

    india_result = india_df[
        india_df.astype(str)
        .apply(lambda col: col.str.lower())
        .apply(lambda col: col.str.contains(destination.lower()))
        .any(axis=1)
    ]


    # ----------------------------------------
    # Search destination in International dataset
    # ----------------------------------------

    international_result = international_df[
        international_df.astype(str)
        .apply(lambda col: col.str.lower())
        .apply(lambda col: col.str.contains(destination.lower()))
        .any(axis=1)
    ]


    destination_data = pd.concat(
    [india_result, international_result]
    )

    if destination_data.empty:
        destination_info = "No destination information found."
    else:
        destination_info = destination_data.iloc[0].to_dict()

    prompt = f"""
        You are an expert travel planner.

        Destination:
        {destination}

        User Budget:
        ₹{budget}

        Destination Information:

        {destination_info}

        Using the destination information above,

        Recommend 5 hotels.

        For each hotel provide:

            • Hotel Name

            • Approximate Price Per Night

            • Rating

            • Nearby Attractions

            • Why it is recommended

            • Whether it fits the user's budget.

        Use the destination's popularity, category, average daily budget,
        description and location while recommending hotels.

    Finally recommend ONE best hotel overall.

    Keep the report clean and professional.
    """


    response = generate_response(prompt)

    state["hotel_response"] = response

    return state


# ==========================================================
#               BUILD GRAPH
# ==========================================================

builder = StateGraph(AgentState)

builder.add_node("process", process)

builder.add_edge(START, "process")

builder.add_edge("process", END)

hotel_agent = builder.compile()