from agents.itinerary_agent import itinerary_agent

destination = input("Enter Destination : ")
budget = int(input("Enter Budget : "))
days = int(input("Enter Number of Days : "))

initial_state = {
    "destination": destination,
    "budget": budget,
    "days": days,
    "itinerary_response": ""
}

result = itinerary_agent.invoke(initial_state)

print(result["itinerary_response"])