import requests
from twilio.rest import Client
# This project requires a Twilio (SMS service), AlphaVantage (stocks info)
# and NewsAPI (news aggregator) accounts, all have a free tier

# Choose your stock/company
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# Make sure to set the following variables with your own keys
STOCK_API_KEY = "..."
NEWS_API_KEY = "..."
TWILIO_SID = "..."
TWILIO_TOKEN = "..."
TWILIO_NUMBER = "..."
MY_NUMBER = "..."

# Stock API endpoint and parameters
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

# News API endpoint and parameters
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_parameters = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "pageSize": 3,  # Number of articles
}

# Get stock data
stock_request = requests.get(STOCK_ENDPOINT, params=stock_parameters)
time_series = stock_request.json()["Time Series (Daily)"]

# Extract data from the last two days
last_two_days = list(time_series.keys())[:2]
evaluation = [float(time_series[day]["4. close"]) for day in last_two_days]

# Calculate percentage difference
percentage_diff = abs((evaluation[1] - evaluation[0]) / evaluation[0]) * 100

# Check if percentage difference exceeds threshold
if percentage_diff >= 2:
    # Get latest news articles
    news_request = requests.get(NEWS_ENDPOINT, params=news_parameters)
    last_news = news_request.json()

    # Determine if stock price increased or decreased
    if evaluation[0] > evaluation[1]:
        up_or_down = "🔼"
    else:
        up_or_down = "🔻"

    # Send notification via Twilio
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    message = client.messages.create(
        body=f"{STOCK}: {up_or_down} {round(percentage_diff, 2)}%\n\n\n"
        f"{last_news['articles'][0]['title']}\n\n"
        f"Brief: {last_news['articles'][0]['description']}\n\n\n"
        f"{last_news['articles'][1]['title']}\n\n"
        f"Brief: {last_news['articles'][1]['description']}\n\n\n"
        f"{last_news['articles'][2]['title']}\n\n"
        f"Brief: {last_news['articles'][2]['description']}",
        from_=TWILIO_NUMBER,
        to=MY_NUMBER,
    )
