import csv
import os
from datetime import datetime

from models.flight import Flight


class PriceTracker:
    def __init__(self, filename="price_history.csv"):
        self.filename = filename

    @staticmethod
    def detect_delimiter(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
            for delimiter in [',', ';', '\t', '|']:
                if delimiter in first_line:
                    fields = first_line.split(delimiter)
                    if len(fields) > 1:
                        # print(f"Wykryty delimiter: '{delimiter}', pola: {fields}")
                        return delimiter
        return ','  # domyślny delimiter

    def load_price_history(self):
        """Wczytuje całą historię cen z pliku CSV"""
        if not os.path.exists(self.filename):
            return []

        # Wykryj delimiter
        delimiter = self.detect_delimiter(self.filename)

        results = []
        with open(self.filename, mode="r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                return []

            # Ręczne przetwarzanie nagłówków i danych
            headers = [h.strip() for h in lines[0].split(delimiter)]

            for line in lines[1:]:
                if not line.strip():
                    continue  # Pomijamy puste linie

                values = [v.strip() for v in line.split(delimiter)]
                if len(values) != len(headers):
                    print(f"Ostrzeżenie: nieprawidłowa liczba kolumn w linii: {line}")
                    continue

                row = {headers[i]: values[i] for i in range(len(headers))}
                results.append(row)

        return results

    def load_last_price(self, direction: str) -> dict:
        """Wczytuje ostatnią zapisaną cenę dla danego kierunku (TAM/POWRÓT)"""
        data = self.load_price_history()

        # Sprawdzamy różne warianty zapisu kierunku
        possible_directions = [direction, direction.upper(), direction.lower(),
                               direction.strip(), direction.replace("Ó", "O")]

        matching_entries = [entry for entry in data
                            if any(entry.get("Direction", "") == d for d in possible_directions)]

        if matching_entries:
            return matching_entries[-1]
        return {}

    def save_price_history(self, flight: Flight, direction: str):
        """Zapisuje historię cen do pliku CSV tylko jeśli cena się zmieniła"""
        file_exists = os.path.exists(self.filename)

        # Ładujemy całą historię cen
        history = self.load_price_history()

        # Sprawdzamy, czy już mamy taki sam lot z taką samą ceną
        for entry in history:
            if (entry["Direction"] == direction and
                    entry["Flight Number"] == flight.flight_number and
                    entry["Date"] == str(flight.departure_time) and
                    float(entry["Price"]) == flight.price):
                return

        with open(self.filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Timestamp", "Direction", "Date", "Flight Number", "Price", "Currency"])

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                direction,
                flight.departure_time,
                flight.flight_number,
                flight.price,
                flight.currency
            ])

        print(
            f"✅ Zapisano nową cenę dla {direction}: {flight.price:.2f} {flight.currency} dla lotu {flight.departure_time}")
