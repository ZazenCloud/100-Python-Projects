from datetime import datetime, timedelta
from flight_club import DataManager, FlightSearch, NotificationManager
# This project is an upgraded version of yesterday's project
# (Day 39 - Flight Deal Finder.py)
# It adds support for new members (via console input), email notification
# and alternatives flights with stopover
# (if direct flights for the destination doesn't exist)

# This project requires a Twilio (SMS service)
# and a TEQUILA API (flight search) account, both have a free tier


# Clone this spreadsheet
# https://docs.google.com/spreadsheets/d/1YMK-kYDYwuiGZoawQy7zyDjEIU9u8oggCV4H2M9j7os/edit#gid=0
# Add a new tab and name it "users"
# Create 3 columns ("First Name", "Last Name" and "Email") in the new tab


# Log in into https://sheety.co/ with the same Google account
# that you cloned the spreadsheet

# New Project -> paste the link of your spreadsheet -> Create ->
# API -> Enable GET, POST and PUT for both tabs

# Copy the endpoint and paste it as string value for
# SHEETY_ENDPOINT in the flight_club.py file

ORIGIN_CITY_IATA = "BCN"  # Change for the IATA code of your origin city

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Get new member info (name + email)
print("Welcome to the Flight Club!")
print("Firstly, do not talk about the Flight Club!")
print("Secondly, we find the best flight deals and email them to you.")
member_first_name = input("What is your first name?\n")
member_last_name = input("What is your last name?\n")
member_email = input("What is your email?\n")
confirm_email = input("Type your email again to confirm.\n")
# Confirm email
while member_email != confirm_email:
    print("Emails do not match!")
    member_email = input("What is your email?\n")
    confirm_email = input("Type your email again to confirm.\n")
print("Congratulations, you are in the club!")
# Add info to the Google Sheets file
data_manager.save_member_email(
    member_first_name, member_last_name, member_email
)

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
    # If the flight price is lower than the lowest
    # price in Sheety data, send a notification
    if flight is not None:
        if flight.price < destination["lowestPrice"]:

            users = data_manager.get_customer_emails()
            emails = [row["email"] for row in users]
            names = [row["firstName"] for row in users]

            message = (
                f"Low price alert! Only £{flight.price} to fly from "
                f"{flight.origin_city}-{flight.origin_airport} to "
                f"{flight.destination_city}-{flight.destination_airport}, from"
                f" {flight.out_date} to {flight.return_date}."
            )

            if flight.stop_overs > 0:
                message += (
                    f"\nFlight has {flight.stop_overs} stop over, "
                    f"via {flight.via_city}."
                )
                print(message)

            notification_manager.send_sms(message)
            notification_manager.send_emails(message)
