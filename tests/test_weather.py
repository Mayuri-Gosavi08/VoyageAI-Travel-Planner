from agents.weather_agent import weather_agent

city = input("Enter City: ")

initial_state = {
    "city": city,
    "weather": {},
    "response": ""
}

result = weather_agent.invoke(initial_state)

print(result["response"])