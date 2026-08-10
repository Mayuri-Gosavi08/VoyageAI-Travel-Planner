from agents.hotel_agent import hotel_agent

destination = input("Enter Destination : ")

budget = int(input("Enter Budget : "))

initial_state = {

    "destination": destination,

    "budget": budget,

    "hotel_response": ""

}

result = hotel_agent.invoke(initial_state)

print(result["hotel_response"])