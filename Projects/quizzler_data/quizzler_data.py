import requests

parameters = {
    "amount": 10,  # Number of questions to retrieve
    "type": "boolean",  # Type of questions (boolean - True/False)
}

response = requests.get("https://opentdb.com/api.php?", params=parameters)
response.raise_for_status()
data = response.json()
question_data = data["results"]
