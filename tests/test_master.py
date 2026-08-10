from agents.master_agent import run_master_agent

state = {

    # User Inputs
    "destination": input("Destination : "),
    "budget": int(input("Budget : ")),
    "days": int(input("Days : ")),

    # Weather
    "weather": {},
    "response": "",

    # Budget
    "budget_response": "",

    # Hotel
    "hotel_response": "",

    # Restaurant
    "restaurant_response": "",

    # Itinerary
    "itinerary_response": ""
}

result = run_master_agent(state)

print("\n")
print("="*80)
print("WEATHER")
print("="*80)
print(result["response"])

print("\n")
print("="*80)
print("BUDGET")
print("="*80)
print(result["budget_response"])

print("\n")
print("="*80)
print("HOTELS")
print("="*80)
print(result["hotel_response"])

print("\n")
print("="*80)
print("RESTAURANTS")
print("="*80)
print(result["restaurant_response"])

print("\n")
print("="*80)
print("ITINERARY")
print("="*80)
print(result["itinerary_response"])