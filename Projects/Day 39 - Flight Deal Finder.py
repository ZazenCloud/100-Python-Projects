from datetime import datetime, timedelta
from flight import DataManager, FlightSearch, NotificationManager
# This project requires a Twilio (SMS service)
# and a TEQUILA API (flight search) account, both have a free tier

# Download flight.py (located on this repository) and move it to same folder of this file

# Clone this spreadsheet
# https://docs.google.com/spreadsheets/d/1YMK-kYDYwuiGZoawQy7zyDjEIU9u8oggCV4H2M9j7os/edit#gid=0

# Log in into https://sheety.co/ with the same Google account that you cloned the spreadsheet
# New Project -> paste the link of your spreadsheet -> Create -> API -> Enable GET and PUT
# Copy the endpoint and paste it as string value for SHEETY_ENDPOINT in the flight.py file

ORIGIN_CITY_IATA = "BCN"  # Change for the IATA code of your origin city

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Get destination data from the Sheety API
sheety_data = data_manager.get_data()
city_names = [row["city"] for row in sheety_data]

# Get destination data from the Sheety API
codes = flight_search.get_destination_codes(city_names)
# Update destination codes in the Sheety API
data_manager.update_destination_codes(codes)
# Get updated destination data from the Sheety API
sheety_data = data_manager.get_data()

tomorrow = datetime.now() + timedelta(1)
six_month_from_today = datetime.now() + timedelta(180)

# Check flights for each destination in the Sheety data
for destination in sheety_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow.strftime("%d/%m/%Y"),
        to_time=six_month_from_today.strftime("%d/%m/%Y"),
    )
    # If the flight price is lower than the lowest price in Sheety data, send a notification
    if flight is not None:
        if flight.price < destination["lowestPrice"]:
            notification_manager.send_sms(
                message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            )