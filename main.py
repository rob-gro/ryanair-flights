from datetime import datetime

import matplotlib.pyplot as plt

from constans import DIRECTION_OUTBOUND, DIRECTION_INBOUND
from services.flight_search import FlightSearch
from services.price_tracker import PriceTracker
from utils.date_utils import DateUtils


def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

# 📅 Parametry wyszukiwania lotów
source_airport = "EDI"
destination_airport = "POZ"     #   POZ, GDN
date_from = "2025-03-23"
date_to = "2025-03-30"
return_date_from = "2025-04-05"
return_date_to = "2025-04-30"

# 🔍 Inicjalizacja obiektów
flight_search = FlightSearch()
price_tracker = PriceTracker()


# 🛫 Pobieranie lotów
all_outbound_flights = []
all_outbound_availability = []

for date in DateUtils.generate_dates(date_from, date_to):
    # Pobierz loty
    flights = flight_search.get_flights(source_airport, destination_airport, date, date)
    all_outbound_flights.extend(flights)


# Podobnie dla lotów powrotnych
all_inbound_flights = []
all_inbound_availability = []

for date in DateUtils.generate_dates(return_date_from, return_date_to):
    flights = flight_search.get_flights(destination_airport, source_airport, date, date)
    all_inbound_flights.extend(flights)

# 📊 Zapisywanie cen
for flight in all_outbound_flights:
    price_tracker.save_price_history(flight, DIRECTION_OUTBOUND)

# To samo dla lotów powrotnych
for flight in all_inbound_flights:
    price_tracker.save_price_history(flight, DIRECTION_INBOUND)


# Posortuj loty według ceny i kontynuuj istniejący kod
all_outbound_flights.sort(key=lambda flight: flight.price)
all_inbound_flights.sort(key=lambda flight: flight.price)

# 🔹 Wybieramy **najtańszą parę lotów** (Opcja 1)
if all_outbound_flights and all_inbound_flights:
    cheapest_outbound = all_outbound_flights[0]
    cheapest_inbound = all_inbound_flights[0]
    total_price = cheapest_outbound.price + cheapest_inbound.price

    print("\n  ✅ **NAJTAŃSZA OPCJA LOTU W WYBRANYM ZAKRESIE DAT:**")
    print(f"   📅 TAM: {date_from} ➡️ {date_to}")
    print(f"   📅 POWRÓT: {return_date_from} ➡️ {return_date_to}")
    print("______________________")
    print(f"   ✈️ **Wylot:** {cheapest_outbound.origin} ━━➤ {cheapest_outbound.destination} | {cheapest_outbound.flight_number}")
    print(f"   📅 **Data:** {cheapest_outbound.departure_time}")
    print(f"   💰 **Cena:** {cheapest_outbound.price:.2f} {cheapest_outbound.currency}")
    print("----------------------")
    print(f"   ✈️ **Powrót:** {cheapest_inbound.origin} ━━➤ {cheapest_inbound.destination} | {cheapest_inbound.flight_number}")
    print(f"   📅 **Data:** {cheapest_inbound.departure_time}")
    print(f"   💰 **Cena:** {cheapest_inbound.price:.2f} {cheapest_inbound.currency}")
    print("----------------------")
    print(f"   💸 **Łączna cena:** {total_price:.2f} {cheapest_outbound.currency} 🎟️\n")

    # # 📊 **Zapisz historię cen dla najtańszego lotu TAM**
    price_tracker.save_price_history(cheapest_outbound, DIRECTION_OUTBOUND)
    price_tracker.save_price_history(cheapest_inbound, DIRECTION_INBOUND)

    # Zapisz historię cen dla wszystkich lotów w zakresie dat
    for flight in all_outbound_flights:
        price_tracker.save_price_history(flight, DIRECTION_OUTBOUND)

    for flight in all_inbound_flights:
        price_tracker.save_price_history(flight, DIRECTION_INBOUND)

    # 🔹 **Pokaż 5 kolejnych najtańszych lotów TAM**
    print("🛫 ✈️ **5 NAJTAŃSZYCH LOTÓW TAM (POZA NAJTAŃSZYM):**")
    for i, flight in enumerate(all_outbound_flights[1:6], 1):
        print(f"   {i}. 📅 {flight.departure_time} | 💰 {flight.price:.2f} {flight.currency} | ✈️ {flight.flight_number}")
    print()

    # 🔹 **Pokaż 5 kolejnych najtańszych lotów POWROTNYCH**
    print("🛬 ✈️ **5 NAJTAŃSZYCH LOTÓW POWROTNYCH (POZA NAJTAŃSZYM):**")
    for i, flight in enumerate(all_inbound_flights[1:6], 1):
        print(f"   {i}. 📅 {flight.departure_time} | 💰 {flight.price:.2f} {flight.currency} | ✈️ {flight.flight_number}")
    print()

else:
    print("\n⚠️ ❌ **BRAK DOSTĘPNYCH LOTÓW W PODANYM ZAKRESIE DAT!** 😢")


def plot_price_history(cheapest_outbound, cheapest_inbound):
    history = price_tracker.load_price_history()
    if not history:
        print("⚠️ Brak danych do wygenerowania wykresu!")
        return

    # Filtrowanie lotów o tym samym numerze i tej samej dacie co najtańsze loty
    outbound_flight_number = cheapest_outbound.flight_number
    outbound_date = cheapest_outbound.departure_time.strftime("%Y-%m-%d")

    inbound_flight_number = cheapest_inbound.flight_number
    inbound_date = cheapest_inbound.departure_time.strftime("%Y-%m-%d")

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

    print(f"\n--- Filtrowana historia lotów TAM ---")
    for entry in outbound_history:
        print(entry)

    print(f"\n--- Filtrowana historia lotów POWRÓT ---")
    for entry in inbound_history:
        print(entry)

    # Krok 1: Przygotuj słowniki dla wszystkich cen na podstawie timestampów
    outbound_prices = {entry["Timestamp"]: float(entry["Price"]) for entry in outbound_history}
    inbound_prices = {entry["Timestamp"]: float(entry["Price"]) for entry in inbound_history}

    # Krok 2: Zbierz wszystkie unikalne timestampy z obu lotów i posortuj je
    all_timestamps = sorted(set(outbound_prices.keys()) | set(inbound_prices.keys()))

    # Krok 3: Przygotuj dane do wykresu
    x_values = list(range(len(all_timestamps)))
    outbound_y = []
    inbound_y = []
    last_outbound_price = None
    last_inbound_price = None

    # Krok 4: Wypełnij dane dla obu lotów, przedłużając ostatnią znaną cenę
    for timestamp in all_timestamps:
        if timestamp in outbound_prices:
            last_outbound_price = outbound_prices[timestamp]
        outbound_y.append(last_outbound_price)

        if timestamp in inbound_prices:
            last_inbound_price = inbound_prices[timestamp]
        inbound_y.append(last_inbound_price)

    # Krok 5: Stwórz wykres
    fig, ax = plt.subplots(figsize=(12, 7))

    # Styl wykresu
    plt.style.use('ggplot')

    # Rysowanie danych - tylko dla punktów, które mają wartości
    outbound_points_x = []
    outbound_points_y = []
    inbound_points_x = []
    inbound_points_y = []

    for i, timestamp in enumerate(all_timestamps):
        if timestamp in outbound_prices:
            outbound_points_x.append(i)
            outbound_points_y.append(outbound_prices[timestamp])

        if timestamp in inbound_prices:
            inbound_points_x.append(i)
            inbound_points_y.append(inbound_prices[timestamp])

    # Rysowanie linii z ostatnią znaną ceną (przedłużenie)
    if outbound_y and any(y is not None for y in outbound_y):
        cleaned_outbound_y = [y if y is not None else outbound_y[i - 1] for i, y in enumerate(outbound_y) if
                              i == 0 or y is not None or outbound_y[i - 1] is not None]
        plt.plot(x_values, outbound_y, linestyle='-', linewidth=2, color='blue',
                 label=f'Lot {DIRECTION_OUTBOUND} ({outbound_flight_number})')

    if inbound_y and any(y is not None for y in inbound_y):
        cleaned_inbound_y = [y if y is not None else inbound_y[i - 1] for i, y in enumerate(inbound_y) if
                             i == 0 or y is not None or inbound_y[i - 1] is not None]
        plt.plot(x_values, inbound_y, linestyle='-', linewidth=2, color='magenta',
                 label=f'Lot {DIRECTION_INBOUND} ({inbound_flight_number})')

    # Punkty danych (tylko rzeczywiste punkty)
    if outbound_points_x:
        plt.plot(outbound_points_x, outbound_points_y, 'o', markersize=8, color='blue')
        # Dodanie etykiet z cenami
        for i, price in enumerate(outbound_points_y):
            plt.annotate(f'£{price:.2f}',
                         (outbound_points_x[i], outbound_points_y[i]),
                         xytext=(0, 10),
                         textcoords='offset points',
                         fontsize=9,
                         ha='center')

    if inbound_points_x:
        plt.plot(inbound_points_x, inbound_points_y, 's', markersize=8, color='magenta')
        # Dodanie etykiet z cenami
        for i, price in enumerate(inbound_points_y):
            plt.annotate(f'£{price:.2f}',
                         (inbound_points_x[i], inbound_points_y[i]),
                         xytext=(0, -15),
                         textcoords='offset points',
                         fontsize=9,
                         ha='center')

    # Dodanie tytułu zawierającego informacje o konkretnych lotach
    plt.title(f'Zmiana cen konkretnych lotów w czasie\n'
              f'{DIRECTION_OUTBOUND}: {outbound_flight_number} ({outbound_date}) | '
              f'{DIRECTION_INBOUND}: {inbound_flight_number} ({inbound_date})',
              fontsize=14)

    # Formatowanie osi X
    plt.xticks(x_values, all_timestamps, rotation=45, ha='right')

    plt.xlabel('Data sprawdzenia', fontsize=12)
    plt.ylabel('Cena (GBP)', fontsize=12)
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plt.show()

# Wywołanie funkcji z parametrami
if all_outbound_flights and all_inbound_flights:
    plot_price_history(cheapest_outbound, cheapest_inbound)
else:
    print("⚠️ Nie można wygenerować wykresu - brak lotów.")