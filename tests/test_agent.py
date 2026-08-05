from agents.weather_agent import weather_agent

state = {
    "city": "Mumbai",
    "weather": {},
    "response": "",
    "timestamp": ""
}

result = weather_agent.invoke(state)

print(result)