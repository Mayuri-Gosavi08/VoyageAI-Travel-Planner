from services.weather_service import get_weather

city = input("Enter City: ")

result = get_weather(city)

print(result)