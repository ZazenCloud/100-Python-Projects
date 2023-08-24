import requests
import datetime as dt
# Clone this spreadsheet
# https://docs.google.com/spreadsheets/d/1DHL6Y8XAHSC_KhJsa9QMekwP8b4YheWZY_sxlH3i494/edit#gid=0


# Create a free account at Nutritionix API
# (https://www.nutritionix.com/business/api)

# Copy your ID and KEY and paste it below as a
# string value for NUTRITIONIX_ID and NUTRITIONIX_KEY


# Log in into https://sheety.co/ with the same Google account
# that you cloned the spreadsheet

# New Project -> paste the link of your spreadsheet -> Create ->
# API -> Enable GET and POST

# Copy the endpoint and paste it below as a string value for SHEETY_ENDPOINT

# Then go to Authentication -> Type Bearer (Token) ->
# Write a safe token -> Save Changes

# Copy the token and paste it below as a string value for SHEETY_TOKEN

NUTRITIONIX_ID = "..."
NUTRITIONIX_KEY = "..."
NUTRITIONIX_ENDPOINT = "..."
SHEETY_ENDPOINT = "..."
SHEETY_TOKEN = "Bearer ..."
NOW = dt.datetime.now()
DATE = NOW.strftime("%d/%m/%Y")
TIME = NOW.strftime("%H:%M:%S")

nutritionix_header = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_KEY,
    "x-remote-user-id": "0",
}

user_input = input("Tell me what exercises you did: ")

nutritionix_params = {
    "query": user_input,
    "gender": "male",  # Your gender (male OR female)
    "weight_kg": 90.4,  # Your weight (float)
    "height_cm": 180.0,  # Your height (float)
    "age": 30  # Your age (integer)
}

# Send a POST request to the Nutritionix API
# to get exercise data based on user input
response = requests.post(
    NUTRITIONIX_ENDPOINT, json=nutritionix_params, headers=nutritionix_header
)
exercises = response.json()['exercises']

sheety_header = {
    "Authorization": SHEETY_TOKEN,
}

# Loop through each exercise and send a POST request to the Sheety API
# to add the exercise data to the spreadsheet
for exercise in exercises:
    sheety_params = {
        "workout": {
            "date": DATE,
            "time": TIME,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }

    new_row = requests.post(
        SHEETY_ENDPOINT, json=sheety_params, headers=sheety_header
    )
