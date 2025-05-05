from typing import List, Tuple, Dict, Any

from constans import DIRECTION_OUTBOUND, DIRECTION_INBOUND
from models.flight import Flight
from services.flight_search import FlightSearch
from services.price_tracker import PriceTracker
from utils.airport_utils import get_flight_distance
from utils.date_utils import DateUtils
from utils.flight_utils import update_flights_with_latest_prices


class FlightService:
    def __init__(self, flight_search: FlightSearch, price_tracker: PriceTracker, currency: str = "GBP"):
        self.flight_search = flight_search
        self.price_tracker = price_tracker
        self.currency = currency

    def find_flights(self, source_airport: str, destination_airport: str,
                     date_from: str, date_to: str,
                     return_date_from: str, return_date_to: str) -> Tuple[List[Flight], List[Flight]]:
        """
        Wyszukuje loty w obie strony między podanymi lotniskami w podanych zakresach dat.
        Zwraca dwie listy: lotów TAM i POWRÓT, posortowane wg ceny.
        """
        # Loty TAM
        all_outbound_flights = []
        for date in DateUtils.generate_dates(date_from, date_to):
            flights = self.flight_search.get_flights(source_airport, destination_airport, date, date)
            all_outbound_flights.extend(flights)

        # Loty POWRÓT
        all_inbound_flights = []
        for date in DateUtils.generate_dates(return_date_from, return_date_to):
            flights = self.flight_search.get_flights(destination_airport, source_airport, date, date)
            all_inbound_flights.extend(flights)

        # Zapisywanie historii cen
        for flight in all_outbound_flights:
            self.price_tracker.save_price_history(flight, DIRECTION_OUTBOUND)

        for flight in all_inbound_flights:
            self.price_tracker.save_price_history(flight, DIRECTION_INBOUND)

        # Aktualizacja cen z historii
        price_history = self.price_tracker.load_price_history()
        all_outbound_flights = update_flights_with_latest_prices(all_outbound_flights, price_history)
        all_inbound_flights = update_flights_with_latest_prices(all_inbound_flights, price_history)

        # Sortowanie lotów według ceny
        all_outbound_flights.sort(key=lambda flight: flight.price)
        all_inbound_flights.sort(key=lambda flight: flight.price)

        return all_outbound_flights, all_inbound_flights

    def get_cheapest_option(self, outbound_flights: List[Flight], inbound_flights: List[Flight]) -> Dict[str, Any]:
        """
        Zwraca najtańszą opcję lotu (kombinację lotu TAM i POWRÓT) z podsumowaniem.
        """
        if not outbound_flights or not inbound_flights:
            return None

        cheapest_outbound = outbound_flights[0]
        cheapest_inbound = inbound_flights[0]
        total_price = cheapest_outbound.price + cheapest_inbound.price
        flight_distance = get_flight_distance(cheapest_outbound)

        # Zapis historii cen dla najtańszych lotów (dla przyszłych porównań)
        self.price_tracker.save_price_history(cheapest_outbound, DIRECTION_OUTBOUND)
        self.price_tracker.save_price_history(cheapest_inbound, DIRECTION_INBOUND)

        return {
            'outbound': cheapest_outbound,
            'inbound': cheapest_inbound,
            'total_price': total_price,
            'flight_distance': flight_distance,
            'currency': cheapest_outbound.currency
        }

    def get_price_history_data(self, outbound_flight: Flight, inbound_flight: Flight) -> Dict[str, List]:
        """
        Pobiera dane historii cen dla konkretnych lotów do użycia w wykresie.
        """
        history = self.price_tracker.load_price_history()
        if not history:
            return {'outbound': [], 'inbound': []}

        outbound_flight_number = outbound_flight.flight_number
        outbound_date = outbound_flight.departure_time.strftime("%Y-%m-%d")

        inbound_flight_number = inbound_flight.flight_number
        inbound_date = inbound_flight.departure_time.strftime("%Y-%m-%d")

        # Filtrujemy tylko loty pasujące do obecnie wybranych
        outbound_history = [
            entry for entry in history
            if entry["Direction"] == DIRECTION_OUTBOUND
               and entry["Flight Number"] == outbound_flight_number
               and entry["Date"].startswith(outbound_date)
        ]

        inbound_history = [
            entry for entry in history
            if entry["Direction"] == DIRECTION_INBOUND
               and entry["Flight Number"] == inbound_flight_number
               and entry["Date"].startswith(inbound_date)
        ]

        return {
            'outbound': outbound_history,
            'inbound': inbound_history,
            'all_timestamps': sorted(set(
                entry["Timestamp"] for entry in outbound_history + inbound_history
            ))
        }
