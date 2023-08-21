import requests
from datetime import datetime
# This project uses the Pixela's API

'''To create your account'''
# Modify the TOKEN and USERNAME string values
# Uncomment the Step 1 block (lines 69-70)
# Run the program

'''To create your graph'''
# Modify the GRAPH_ID and GRAPH_NAME string values
# Comment the Step 1 block (lines 69-70)
# Uncomment the Step 2 block (lines 73-74)
# Run the program

'''Normal usage'''
# Comment the Step 2 block (lines 73-74)
# Uncomment lines 77-78 to create today's info

'''Other usage'''
# Comment lines 77-78
# Uncomment lines 81-82 to update today's info
# OR
# Uncomment lines 85-86 to delete today's info

TOKEN = "..."
USERNAME = "..."
GRAPH_ID = "..."
GRAPH_NAME = "..."
PIXELA_ENDPOINT = "https://pixe.la/v1/users"
GRAPH_ENDPOINT = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"
NEW_PIXEL_ENDPOINT = f"{GRAPH_ENDPOINT}/{GRAPH_ID}"

# Current date (formatted to the Pixela's API specification)
today = datetime.now()
formatted_today = today.strftime("%Y%m%d")

quantity = input("How many kilometers did you walk today?\n")

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

headers = {
    "X-USER-TOKEN": TOKEN
}

graph_params = {
    "id": GRAPH_ID,
    "name": GRAPH_NAME,
    "unit": "Km",
    "type": "float",
    "color": "shibafu",
}

new_pixel_params = {
    "date": formatted_today,
    "quantity": quantity,
}

update_params = {
    "quantity": quantity,
}

''' Step 1 -> Create your account'''
# response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
# print(response.text)

''' Step 2 -> Create your graph'''
# response = requests.post(url=GRAPH_ENDPOINT, json=graph_params, headers=headers)
# print(response.text)

'''Uncomment this block to create today's info'''
# response = requests.post(url=NEW_PIXEL_ENDPOINT, json=new_pixel_params, headers=headers)
# print(response.text)

'''Uncomment this block to update today's info'''
# response = requests.put(url=f"{NEW_PIXEL_ENDPOINT}/{formatted_today}", json=update_params, headers=headers)
# print(response.text)

'''Uncomment this block to delete today's info'''
# response = requests.delete(url=f"{NEW_PIXEL_ENDPOINT}/{formatted_today}", headers=headers)
# print(response.text)
