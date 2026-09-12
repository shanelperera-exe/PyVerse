import os
import requests
from dotenv import load_dotenv

load_dotenv()

FLIGHT_ENDPOINT = "https://serpapi.com/search"


class FlightSearch:
    def __init__(self):
        self._api_key = os.environ["SERPAPI_API_KEY"]

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time, is_direct=True):
        """
        Searches for flight options between two cities using the SerpAPI Google Flights engine.
        """
        outbound_date = from_time.strftime("%Y-%m-%d") if hasattr(from_time, "strftime") else from_time
        return_date = to_time.strftime("%Y-%m-%d") if hasattr(to_time, "strftime") else to_time

        parameters = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "currency": "GBP",
            "type": "1",  # Round trip
            "adults": "1",
            "api_key": self._api_key,
            "stops": "1" if is_direct else "0",
        }

        response = requests.get(url=FLIGHT_ENDPOINT, params=parameters)

        if response.status_code != 200:
            print(f"check_flights() response code: {response.status_code}")
            print(f"There was a problem with the flight search: {response.text}")
            return None

        return response.json()