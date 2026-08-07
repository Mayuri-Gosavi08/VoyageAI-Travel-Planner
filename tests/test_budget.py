from agents.budget_agent import budget_agent

destination = input("Enter Destination: ")
budget = int(input("Enter Budget: "))
days = int(input("Enter Number of Days: "))

initial_state = {
    "destination": destination,
    "budget": budget,
    "days": days,
    "budget_response": ""
}

result = budget_agent.invoke(initial_state)

print(result["budget_response"])