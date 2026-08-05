from services.gemini_service import generate_response

prompt = "Suggest a 2-day trip itinerary for Goa."

response = generate_response(prompt)

print("Gemini Response:")
print(response)