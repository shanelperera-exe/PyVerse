import os
import time
import requests
from dotenv import load_dotenv
import threading
from settings import animate_dots

load_dotenv()

class DataManager:
    def __init__(self):
        self._user = os.environ.get("SHEETY_USERNAME") or os.environ.get("SHEETY_FLIGHT_USERNAME")
        self._password = os.environ.get("SHEETY_PASSWORD") or os.environ.get("SHEETY_FLIGHT_PASSWORD")
        self.prices_endpoint = os.environ.get("SHEETY_PRICES_ENDPOINT") or os.environ.get("SHEETY_FLIGHT_PRICES_ENDPOINT")
        self.users_endpoint = os.environ.get("SHEETY_USERS_ENDPOINT") or os.environ.get("SHEETY_FLIGHT_USERS_ENDPOINT", "")
        self._authorization = (self._user, self._password)
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        for attempt in range(3):
            try:
                response = requests.get(url=self.prices_endpoint, auth=self._authorization, timeout=10)
                response.raise_for_status()
                data = response.json()
                self.destination_data = data["prices"]
                return self.destination_data
            except Exception as e:
                if attempt == 2:
                    raise e
                time.sleep(1.5)

    def update_destination_codes(self):
        # Start the animation in a separate thread
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=animate_dots, args=(stop_event, "Updating destination codes"))
        animation_thread.start()

        try:
            for city in self.destination_data:
                new_data = {
                    "price": {
                        "iataCode": city["iataCode"]
                    }
                }
                response = requests.put(
                    url=f"{self.prices_endpoint}/{city['id']}",
                    json=new_data,
                    auth=self._authorization
                )
                response.raise_for_status()
        finally:
            # Signal the animation thread to stop
            stop_event.set()
            animation_thread.join()  # Wait for the animation thread to finish


    def update_lowest_price(self, row_id, new_price):
        """
        Updates the lowest price of a specific destination row in the Google Sheet via Sheety.
        """
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        response = requests.put(
            url=f"{self.prices_endpoint}/{row_id}",
            json=new_data,
            auth=self._authorization
        )
        response.raise_for_status()
        return response.json()

    def get_customer_emails(self):
        for attempt in range(3):
            try:
                response = requests.get(url=self.users_endpoint, auth=self._authorization, timeout=10)
                response.raise_for_status()
                self.customer_data = response.json()["users"]
                return self.customer_data
            except Exception as e:
                if attempt == 2:
                    raise e
                time.sleep(1.5)

