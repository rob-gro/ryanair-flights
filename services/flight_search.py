from ryanair.ryanair import Ryanair
from models.flight import Flight

class FlightSearch:
    def __init__(self, currency="GBP"):
        self.ryanair = Ryanair(currency=currency)

    def get_flights(self, source, destination, date_from, date_to):
        flights = self.ryanair.get_cheapest_flights(
            airport=source,
            date_from=date_from,
            date_to=date_to,
            destination_airport=destination
        )
        return [Flight(
            origin=f.origin,
            destination=f.destination,
            departure_time=f.departureTime,
            flight_number=f.flightNumber,
            price=f.price,
            currency=f.currency
        ) for f in flights]
