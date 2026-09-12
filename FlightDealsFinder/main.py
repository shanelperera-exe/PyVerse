import socket
import time
import requests_cache
from pprint import pprint
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager
from settings import logo, animate_loading

# Force IPv4 in WSL to prevent intermittent DNS name resolution failures
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    try:
        return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    except socket.gaierror:
        time.sleep(1)
        return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4


# ==================== Conserve requests and preserve your free plan ====================
requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    },
)

# Display Flight Deal Finder ASCII Banner
logo()

# ==================== Setup ====================
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

with animate_loading("Connecting to Google Sheets & retrieving destinations"):
    sheet_data = data_manager.get_destination_data()

# ==================== Retrieve Customer Emails ====================
with animate_loading("Retrieving customer emails from Google Sheets"):
    customer_data = data_manager.get_customer_emails()

# Extract emails, checking for 'email' or the Google Form generated column 'whatIsYourEmailAddress?'
customer_email_list = [
    row.get("email") or row.get("whatIsYourEmailAddress?")
    for row in customer_data
    if (row.get("email") or row.get("whatIsYourEmailAddress?"))
]
print(f"👥 Registered customers to notify: {len(customer_email_list)} ({', '.join(customer_email_list)})")

# ==================== Set the Dates and Origin Airport ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
ORIGIN_CITY_IATA = "LHR"  # London Heathrow

print(f"\n🛫 Departure Airport: {ORIGIN_CITY_IATA}")
print(f"📅 Search Window: {tomorrow.strftime('%Y-%m-%d')} to {six_month_from_today.strftime('%Y-%m-%d')}")

# ==================== Find Cheap Flights ====================

for destination in sheet_data:
    print(f"\n{'='*65}")
    print(f"📍 Checking Destination: {destination['city']} ({destination['iataCode']}) | Sheet Threshold: GBP {destination['lowestPrice']}")
    print(f"{'='*65}")

    with animate_loading(f"🔍 Getting direct flights for {destination['city']}"):
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=tomorrow,
            to_time=six_month_from_today,
            is_direct=True,
        )
    cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))

    if cheapest_flight.price == "N/A":
        print(f"   ℹ️  No direct flight to {destination['city']}. Looking for indirect flights...")
        with animate_loading(f"🔍 Searching indirect flights (with stops) for {destination['city']}"):
            flights = flight_search.check_flights(
                ORIGIN_CITY_IATA,
                destination["iataCode"],
                from_time=tomorrow,
                to_time=six_month_from_today,
                is_direct=False,
            )
        cheapest_flight = find_cheapest_flight(flights, return_date=six_month_from_today.strftime("%Y-%m-%d"))

    if cheapest_flight.price != "N/A":
        stop_info = "direct" if cheapest_flight.stops == 0 else f"{cheapest_flight.stops} stop(s)"
        print(f"🏷️  Cheapest price found: GBP {cheapest_flight.price} ({stop_info})")
    else:
        print("❌ No flights found for this route.")

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        # Customise the message depending on the number of stops
        if cheapest_flight.stops == 0:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly direct " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        else:
            message = f"Low price alert! Only GBP {cheapest_flight.price} to fly " \
                      f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, " \
                      f"with {cheapest_flight.stops} stop(s) " \
                      f"departing on {cheapest_flight.out_date} and returning on {cheapest_flight.return_date}."

        print(f"\n🎉 [DEAL ALERT] Lower price flight found to {destination['city']}!")
        print(f"   💰 New Price: GBP {cheapest_flight.price} < Target: GBP {destination['lowestPrice']}")

        # Update Google Sheet
        with animate_loading("   📝 Updating Google Sheet with new lowest price"):
            data_manager.update_lowest_price(destination["id"], cheapest_flight.price)

        # Telegram notification
        with animate_loading("   📱 Sending instant Telegram deal alert"):
            notification_manager.send_telegram(message_body=message)

        # Send emails to everyone on the list
        with animate_loading(f"   📧 Dispatching deal alert email to {len(customer_email_list)} customer(s)"):
            notification_manager.send_emails(email_list=customer_email_list, email_body=message)

        print("   ✅ All notifications and updates completed successfully!")
    else:
        if cheapest_flight.price != "N/A":
            print(f"   ℹ️  No deal: Price GBP {cheapest_flight.price} is not lower than threshold GBP {destination['lowestPrice']}.")

print(f"\n{'='*65}")
print("✨ Flight search completed for all destinations!")
print(f"{'='*65}\n")

