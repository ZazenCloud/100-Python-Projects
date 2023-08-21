import requests
from datetime import datetime
import smtplib
from email.message import EmailMessage
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude
MY_EMAIL = "youremail@here.com"  # Your email
MY_PASSWORD = "yourpassword"  # Your password


def iss_near_me():
    """Fetches the current position of the ISS and checks if it is near you."""
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Return True if your position is within +5 or -5 degrees of the ISS position
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True


def is_night():
    """Checks if it is currently night time on your location, based
    on sunrise/sunset information."""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # Retrieve sunset and sunrise data for your location
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    # Check if it is currently night time based on your location
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    # Loop every minute
    time.sleep(60)
    if iss_near_me and is_night:
        message = EmailMessage()
        # Set the sender's email address
        message['From'] = MY_EMAIL
        # Set the recipient's email address
        message['To'] = MY_EMAIL
        # Set the email subject
        message['Subject'] = "Look up!"
        message.set_content("The ISS is in the sky, above you!")
        # Choose the SMTP server of your email service
        # Gmail -> smtp.gmail.com
        # Outlook -> smtp-mail.outlook.com
        # Yahoo -> smtp.mail.yahoo.com
        # iCloud -> smtp.mail.me.com
        with smtplib.SMTP("SMTP server here", port=587) as server:
            # Start a secure TLS connection
            server.starttls()
            # Log in to the email server
            server.login(user=MY_EMAIL, password=MY_PASSWORD)
            # Send the email message
            server.send_message(message)
