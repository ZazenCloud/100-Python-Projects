import requests
from twilio.rest import Client

SHEETY_ENDPOINT = "..."
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
# Make sure to set the following variables with your own keys
TEQUILA_KEY = "..."
TWILIO_ID = "..."
TWILIO_TOKEN = "..."
TWILIO_NUMBER = "..."
MY_NUMBER = "..."


class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_data(self):
        # Get data from Google Sheets (city names, codes, prices)
        response = requests.get(url=SHEETY_ENDPOINT)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self, codes):
        # Update destination codes
        id = 2
        for code in codes:
            new_data = {
                "price": {
                    "iataCode": code
                }
            }
            requests.put(
                url=f"{SHEETY_ENDPOINT}/{id}",
                json=new_data
            )
            id += 1


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_ID, TWILIO_TOKEN)

    def send_sms(self, message):
        # Send an SMS notification using Twilio
        message = self.client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=MY_NUMBER,
        )


class FlightData:

    def __init__(self, price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date):
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date


class FlightSearch:

    def get_destination_codes(self, city_names):
        # Get the destination code for a given city name
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_KEY}
        codes = []
        for city in city_names:
            query = {"term": city, "location_types": "city"}
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            results = response.json()["locations"]
            code = results[0]["code"]
            codes.append(code)
        return codes

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        # Check flights prices from origin to destination within a given time range
        headers = {"apikey": TEQUILA_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time,
            "date_to": to_time,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
        }

        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        return flight_data
