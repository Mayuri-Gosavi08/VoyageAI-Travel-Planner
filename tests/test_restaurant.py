from agents.restaurant_agent import restaurant_agent

destination = input("Enter Destination : ")
budget = int(input("Enter Budget : "))

initial_state = {
    "destination": destination,
    "budget": budget,
    "restaurant_response": ""
}

result = restaurant_agent.invoke(initial_state)

print(result["restaurant_response"])