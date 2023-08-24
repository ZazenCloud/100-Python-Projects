import requests
from bs4 import BeautifulSoup
import re
import smtplib

# Set your SMTP server details and email credentials
YOUR_SMTP_ADDRESS = "..."
YOUR_EMAIL = "..."
YOUR_PASSWORD = "..."

# Set the URL of the AliExpress product page and the desired buy price
aliexpress_URL = "..."
buy_price = 0

# Set the headers for the HTTP request
# You can check yours here: https://myhttpheader.com/
headers = {
    "dnt": "...",
    'upgrade-insecure-requests': "...",
    "user-Agent": "...",
    "accept": "...",
    "sec-fetch-site": "...",
    "sec-fetch-mode": "...",
    "sec-fetch-user": "...",
    "sec-fetch-dest": "...",
    "accept-language": "...",
}

# HTTP GET request to the AliExpress product page
response = requests.get(aliexpress_URL, headers=headers)

soup = BeautifulSoup(response.content, "html.parser")
# Info about the product is in a <script> element in the HTML's head
head_scripts = soup.head.script
script_contents = head_scripts.get_text(strip=True)

# Pattern 1 -> price
pattern_1 = (
    r'"defaultInstallmentForm"'
    r'\s*:\s*{[^}]*"formatedAmount"\s*:\s*"R\$([^"]*)"'
)

match = re.search(pattern_1, script_contents)

if match:
    result = match.group(1)
    # Formatting
    parts = result.split(",")
    value_before_comma = parts[0].strip()
    value_after_comma = parts[1].strip()
    # String to float
    price = float(f"{value_before_comma}.{value_after_comma}")

# Pattern 2 -> title
pattern_2 = r'"productInfoComponent"\s*:\s*{[^}]*"subject"\s*:\s*"([^"]*)"'

match = re.search(pattern_2, script_contents)

if match:
    title = match.group(1)

# Check if the price is lower than the desired buy price
if price < buy_price:
    # Compose the email message
    message = f"{title} is now {price}!"

    # Establish an SMTP connection and send the email
    with smtplib.SMTP(YOUR_SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        result = connection.login(YOUR_EMAIL, YOUR_PASSWORD)
        connection.sendmail(
            from_addr=YOUR_EMAIL,
            to_addrs=YOUR_EMAIL,
            msg=(
                f"Subject:AliExpress Price Alert!\n\n{message}"
                f"\n{aliexpress_URL}"
            ).encode("utf-8")
        )
