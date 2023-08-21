import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
# This project requires an OpenWeatherMap (weather data) and
# Twilio (SMS service) accounts, both have a free tier

ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
# Make sure to set the following environment variables with your own keys
API_KEY = "your_openweathermap_api_key"
ACCOUNT_SID = "your_twilio_account_sid"
AUTH_TOKEN = "your_twilio_auth_token"
MY_NUMBER = "your_phone_number"
TWILIO_NUMBER = "your_twilio_phone_number"
# Make sure to set your latitude and longitude coordinates
MY_LAT = 0
MY_LONG = 0

weather_params = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "exclude": "current,minutely,daily",
    "appid": API_KEY,
}

will_rain = False

# Send the weather API request and retrieve the response
request = requests.get(ENDPOINT, params=weather_params)
request.raise_for_status
weather_data = request.json()

# Extract the hourly weather data for the next 12 hours
weather_slice = weather_data["hourly"][:12]

# Check if any of the hourly weather conditions indicate rain
for hour in weather_slice:
    condition_code = hour["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# If it will rain, send a text message
if will_rain:
    # Configure the Twilio client with proxy settings
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    # Initialize the Twilio client
    client = Client(ACCOUNT_SID, AUTH_TOKEN, http_client=proxy_client)

    # Send the text message
    message = client.messages.create(
        body="It's going to rain today! Remember to bring an umbrella ☂️",
        from_=TWILIO_NUMBER,
        to=MY_NUMBER
    )
    print(message.status)
