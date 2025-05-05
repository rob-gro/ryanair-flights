from constans import *
from services.chart_service import ChartService
from services.flight_search import FlightSearch
from services.flight_service import FlightService
from services.price_tracker import PriceTracker
from utils.airport_utils import load_airports

# 📅 Parametry wyszukiwania lotów
source_airport = "EDI"
destination_airport = "GDN"  # POZ, GDN, BER
date_from = "2025-04-20"
date_to = "2025-05-30"
return_date_from = "2025-04-01"
return_date_to = "2025-05-31"
currency = "GBP"

load_airports()

flight_search = FlightSearch(currency=currency)
price_tracker = PriceTracker()
flight_service = FlightService(flight_search, price_tracker)

all_outbound_flights, all_inbound_flights = flight_service.find_flights(
    source_airport, destination_airport,
    date_from, date_to,
    return_date_from, return_date_to
)

# 🔹 Wybieramy najtańszą parę lotów
cheapest_option = flight_service.get_cheapest_option(all_outbound_flights, all_inbound_flights)

if cheapest_option:
    cheapest_outbound = cheapest_option['outbound']
    cheapest_inbound = cheapest_option['inbound']
    total_price = cheapest_option['total_price']
    flight_distance = cheapest_option['flight_distance']

    print(f"\n  ✅ **{ORANGE}NAJTAŃSZA OPCJA LOTU W WYBRANYM ZAKRESIE DAT:{RESET}**")
    print(f"   📅 TAM: {BLUE}{date_from}{RESET} ➡️ {BLUE}{date_to}{RESET}")
    print(f"   📅 POWRÓT: {MAGENTA}{return_date_from}{RESET} ➡️ {MAGENTA}{return_date_to}{RESET}")
    print(f"   📏 **Odległość:** {CYAN}{flight_distance:.1f} km{RESET}")
    print("______________________")
    print(
        f"   ✈️ **Wylot:** {GREEN}{cheapest_outbound.origin} ━━➤ {cheapest_outbound.destination}{RESET} | {cheapest_outbound.flight_number}")
    print(f"   📅 **Data:** {BLUE}{cheapest_outbound.departure_time}{RESET}")
    print(f"   💰 **Cena:** {YELLOW}{cheapest_outbound.price:.2f}{RESET} {cheapest_outbound.currency}")
    print("----------------------")
    print(
        f"   ✈️ **Powrót:** {GREEN}{cheapest_inbound.origin} ━━➤ {cheapest_inbound.destination}{RESET} | {cheapest_inbound.flight_number}")
    print(f"   📅 **Data:** {MAGENTA}{cheapest_inbound.departure_time}{RESET}")
    print(f"   💰 **Cena:** {YELLOW}{cheapest_inbound.price:.2f}{RESET} {cheapest_inbound.currency}")
    print("----------------------")
    print(f"   💸 **Łączna cena:** {YELLOW}{total_price:.2f}{RESET} {cheapest_outbound.currency} 🎟️\n")

    # 🔹 **Pokaż 5 kolejnych najtańszych lotów TAM**
    print(f"🛫 ✈️ **{ORANGE}5 NAJTAŃSZYCH LOTÓW TAM (POZA NAJTAŃSZYM):{RESET}**")
    for i, flight in enumerate(all_outbound_flights[1:6], 1):
        print(
            f"   {i}. 📅 {BLUE}{flight.departure_time}{RESET} | 💰 {YELLOW}{flight.price:.2f} {flight.currency}{RESET} | ✈️ {flight.flight_number}")
    print()

    # 🔹 **Pokaż 5 kolejnych najtańszych lotów POWROTNYCH**
    print(f"🛬 ✈️ **{ORANGE}5 NAJTAŃSZYCH LOTÓW POWROTNYCH (POZA NAJTAŃSZYM):{RESET}**")
    for i, flight in enumerate(all_inbound_flights[1:6], 1):
        print(
            f"   {i}. 📅 {MAGENTA}{flight.departure_time}{RESET} | 💰 {YELLOW}{flight.price:.2f} {flight.currency}{RESET} | ✈️ {flight.flight_number}")
    print()

    # Pobierz dane historii cen dla wykresu
    price_history_data = flight_service.get_price_history_data(cheapest_outbound, cheapest_inbound)

    # Wyświetl szczegóły historii cen w konsoli
    print(f"\n--- Filtrowana historia lotów TAM ---")
    for entry in price_history_data['outbound']:
        print(entry)

    print(f"\n--- Filtrowana historia lotów POWRÓT ---")
    for entry in price_history_data['inbound']:
        print(entry)

    # Przygotuj dane dla wykresu
    outbound_flight_info = {
        'flight_number': cheapest_outbound.flight_number,
        'date': cheapest_outbound.departure_time.strftime("%Y-%m-%d")
    }

    inbound_flight_info = {
        'flight_number': cheapest_inbound.flight_number,
        'date': cheapest_inbound.departure_time.strftime("%Y-%m-%d")
    }

    # Generuj wykres
    ChartService.plot_price_history(
        price_history_data['outbound'],
        price_history_data['inbound'],
        outbound_flight_info,
        inbound_flight_info
    )

else:
    print("\n⚠️ ❌ **BRAK DOSTĘPNYCH LOTÓW W PODANYM ZAKRESIE DAT!** 😢")
