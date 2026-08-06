from agents.weather_agent import weather_agent

initial_state = {
    "city": "Pune",
    "weather": {},
    "response": "",
    "timestamp": ""
}

result = weather_agent.invoke(initial_state)

print(result)