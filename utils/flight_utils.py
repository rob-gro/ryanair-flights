import copy
from datetime import datetime


def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")


def update_flights_with_latest_prices(flights, price_history):
    """
    Aktualizuje ceny lotów na podstawie najnowszych danych z historii cen.
    Args:
        flights: Lista obiektów Flight do zaktualizowania
        price_history: Historia cen z bazy danych/pliku CSV
    Returns:
        Lista zaktualizowanych obiektów Flight
    """
    # Grupuje dane historyczne według numeru lotu i daty
    flight_price_history = {}
    for entry in price_history:
        key = (entry["Flight Number"], entry["Date"].split()[0])
        if key not in flight_price_history or parse_timestamp(entry["Timestamp"]) > parse_timestamp(
                flight_price_history[key]["Timestamp"]):
            flight_price_history[key] = entry

    # Aktualizuje ceny lotów
    updated_flights = []
    for flight in flights:
        flight_copy = copy.deepcopy(flight)
        flight_date = flight.departure_time.strftime("%Y-%m-%d")
        key = (flight.flight_number, flight_date)

        if key in flight_price_history:
            latest_entry = flight_price_history[key]

            flight_copy.price = float(latest_entry["Price"])
            flight_copy.price_source = "history"

        updated_flights.append(flight_copy)

    return updated_flights
