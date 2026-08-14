# Agent Prompts

This file contains the prompts used by the AI agents in the VoyageAI Travel Planner.

The prompts send the required project data to Gemini AI and ask it to generate useful travel recommendations.

---

## 1. Weather Agent Prompt

The Weather Agent gets the current weather from the Weather Service and sends it to Gemini.

### Purpose

The prompt asks Gemini to give travel recommendations based on the current weather.

### Information Given to Gemini

- Destination
- Current weather

### Gemini Tasks

Gemini is asked to provide exactly 5 recommendations:

1. What to wear
2. Whether to carry an umbrella
3. Best places to visit in the weather
4. Safety precautions
5. Local travel tips

The response is kept simple and user-friendly.

---

## 2. Budget Agent Prompt

The Budget Agent uses the activity, food and transport CSV datasets.

### Purpose

The prompt asks Gemini to estimate the total travel budget.

### Information Given to Gemini

- Destination
- User budget
- Trip duration
- Activity cost data
- Food cost data
- Transport cost data

### Gemini Tasks

Gemini estimates:

1. Activity cost
2. Food cost
3. Transport cost
4. Total estimated budget
5. Whether the user's budget is sufficient
6. Money-saving tips

The result is returned as a clean travel budget report.

---

## 3. Hotel Agent Prompt

The Hotel Agent searches the Indian and international destination datasets for the selected destination.

### Purpose

The prompt asks Gemini to recommend suitable hotels based on the destination and user's budget.

### Information Given to Gemini

- Destination
- User budget
- Destination information from the CSV datasets

### Gemini Tasks

Gemini recommends 5 hotels.

For each hotel, it provides:

- Hotel name
- Approximate price per night
- Rating
- Nearby attractions
- Reason for recommendation
- Whether it fits the user's budget

Finally, Gemini recommends one best hotel overall.

---

## 4. Restaurant Agent Prompt

The Restaurant Agent filters the restaurant dataset according to the selected destination.

### Purpose

The prompt asks Gemini to recommend restaurants using the filtered restaurant information.

### Information Given to Gemini

- Destination
- User budget
- Restaurant information from the CSV dataset

### Gemini Tasks

Gemini provides:

1. Top 5 restaurants
2. Famous cuisines
3. Approximate cost for two
4. Veg / Non-Veg information
5. Ratings
6. Best restaurant overall
7. Why the restaurant suits the user's budget

The prompt tells Gemini to use only the restaurant information provided by the dataset.

---

## 5. Itinerary Agent Prompt

The Itinerary Agent filters the attractions dataset according to the selected destination.

### Purpose

The prompt asks Gemini to create a complete day-wise travel itinerary.

### Information Given to Gemini

- Destination
- Trip duration
- User budget
- Attraction information from the CSV dataset

### Gemini Tasks

Gemini creates a day-wise itinerary.

For every day, it provides exactly one attraction for:

- Morning
- Afternoon
- Evening

For each attraction, it includes:

- Attraction name
- Category
- Approximate visit duration
- Entry fee
- Short reason for visiting

The itinerary should fit the user's trip duration and budget.

At the end, Gemini provides 3 travel tips.

---

# Prompt Flow

All agents follow a similar basic process:

```text
User Information
       ↓
CSV / API Data
       ↓
Create Prompt
       ↓
Gemini AI
       ↓
Generated Response
       ↓
Save Response in AgentState