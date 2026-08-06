# ==========================================================
#                VOYAGE AI TRAVEL PLANNER
# ==========================================================
# File        : clean_data.py
# Purpose     : Clean all project datasets
# Author      : Team VoyageAI
#
# Cleaning Performed:
#   ✔ Remove duplicate rows
#   ✔ Remove completely empty rows
#   ✔ Fill missing numeric values with column mean
#   ✔ Fill missing text values with "Unknown"
#   ✔ Save cleaned CSV files
# ==========================================================

import os
import pandas as pd


# ==========================================================
#                 CLEANING FUNCTION
# ==========================================================

def clean_csv(file_path):

    print(f"\nCleaning: {file_path}")

    df = pd.read_csv(file_path)

    print("Original Shape :", df.shape)

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Fill missing values
    for column in df.columns:

        # Check if column is numeric
        if pd.api.types.is_numeric_dtype(df[column]):

            df[column] = df[column].fillna(df[column].mean())
        else:

            df[column] = df[column].fillna("Unknown")

    print("Cleaned Shape :", df.shape)

    # Save back to the same file
    df.to_csv(file_path, index=False)

    print("Saved Successfully!")


# ==========================================================
#                ACTIVITY COST DATASET
# ==========================================================

clean_csv(
    "data/activity_cost.csv"
    
)


# ==========================================================
#                ATTRACTIONS DATASET
# ==========================================================

clean_csv(
    "data/attractions.csv"
)


# ==========================================================
#                FOOD COST DATASET
# ==========================================================

clean_csv(
    "data/food_cost.csv"
)


# ==========================================================
#             INDIA DESTINATIONS DATASET
# ==========================================================

clean_csv(
    "data/india_destinations.csv"
)


# ==========================================================
#          INTERNATIONAL DESTINATIONS DATASET
# ==========================================================

clean_csv(
    "data/international_destinations.csv"
)


# ==========================================================
#               RESTAURANTS DATASET
# ==========================================================

clean_csv(
    "data/restaurants.csv"
)


# ==========================================================
#             TRANSPORT COST DATASET
# ==========================================================

clean_csv(
    "data/transport_cost.csv"
)


# ==========================================================
#               WEATHER SAMPLE DATASET
# ==========================================================

clean_csv(
    "data/weather_sample.csv"
)


# ==========================================================
#                  CLEANING COMPLETE
# ==========================================================

print("\n===================================")
print("All datasets cleaned successfully!")
print("===================================")