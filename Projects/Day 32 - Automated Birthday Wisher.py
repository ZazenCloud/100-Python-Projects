import pandas
import smtplib
from email.message import EmailMessage
import datetime as dt
import random
# Download letter_1.txt, letter_2.txt, letter_3.txt and
# users_birthdays.csv (located on this repository)
# then move them to same folder of this file

my_email = "youremail@here.com"
my_password = "yourpassword"
# Current date and time
today = dt.datetime.now()

with open("users_birthdays.csv") as data_file:
    data = pandas.read_csv(data_file)

# Iterate over each row in the data
for index, row in data.iterrows():
    # Check if today is the user's birthday
    if today.day == row.day and today.month == row.month:
        message = EmailMessage()
        # Set the sender's email address
        message['From'] = my_email
        # Set the recipient's email address
        message['To'] = row.email
        # Set the email subject
        message['Subject'] = "Happy Birthday!"

        # Read a random letter template and personalize it with the user's name
        with open(f"letter_{random.randint(1,3)}.txt") as letter_file:
            letter = letter_file.read()
            personalized_letter = letter.replace("[NAME]", row.username)
            # Set the email content
            message.set_content(personalized_letter)

        # Choose the SMTP server of your email service
        # Gmail -> smtp.gmail.com
        # Outlook -> smtp-mail.outlook.com
        # Yahoo -> smtp.mail.yahoo.com
        # iCloud -> smtp.mail.me.com
        with smtplib.SMTP("SMTP server here", port=587) as server:
            # Start a secure TLS connection
            server.starttls()
            # Log in to the email server
            server.login(user=my_email, password=my_password)
            # Send the email message
            server.send_message(message)
