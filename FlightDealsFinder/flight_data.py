class FlightData:
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops=0):
        """
        Constructor for initializing a new flight data instance with specific travel details.
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data, return_date):
    """
    Parses flight data received from SerpAPI (Google Flights) to find the cheapest flight option.
    """
    # Handle empty or invalid response
    if not data or ("best_flights" not in data and "other_flights" not in data):
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", stops="N/A")

    # Combine best_flights and other_flights to check all available options
    all_flights = data.get("best_flights", []) + data.get("other_flights", [])
    if not all_flights:
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", stops="N/A")

    formatted_return_date = return_date.strftime("%Y-%m-%d") if hasattr(return_date, "strftime") else str(return_date)

    cheapest_flight = None
    lowest_price = float("inf")

    for flight in all_flights:
        try:
            # Handle flights missing the 'price' field
            price = flight.get("price")
            if price is None:
                continue

            price = float(price)
            if price < lowest_price:
                lowest_price = price
                first_flight = flight["flights"][0]
                last_flight = flight["flights"][-1]

                origin = first_flight["departure_airport"]["id"]
                destination = last_flight["arrival_airport"]["id"]
                out_date = first_flight["departure_airport"]["time"].split(" ")[0]
                nr_stops = len(flight["flights"]) - 1

                cheapest_flight = FlightData(
                    price=price,
                    origin_airport=origin,
                    destination_airport=destination,
                    out_date=out_date,
                    return_date=formatted_return_date,
                    stops=nr_stops,
                )
        except (KeyError, IndexError, ValueError, TypeError):
            continue

    if cheapest_flight is None:
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", stops="N/A")

    return cheapest_flight
