from typing import Dict, List

import matplotlib.pyplot as plt


class ChartService:
    @staticmethod
    def plot_price_history(outbound_history: List[Dict], inbound_history: List[Dict],
                           outbound_flight_info: Dict, inbound_flight_info: Dict):
        """
        Generuje wykres historii cen dla wybranych lotów.

        Args:
            outbound_history: Historia cen lotów TAM
            inbound_history: Historia cen lotów POWRÓT
            outbound_flight_info: Informacje o locie TAM (numer, data)
            inbound_flight_info: Informacje o locie POWRÓT (numer, data)
        """
        if not outbound_history and not inbound_history:
            print("⚠️ Brak danych do wygenerowania wykresu!")
            return

        outbound_flight_number = outbound_flight_info['flight_number']
        outbound_date = outbound_flight_info['date']
        inbound_flight_number = inbound_flight_info['flight_number']
        inbound_date = inbound_flight_info['date']

        outbound_prices = {entry["Timestamp"]: float(entry["Price"]) for entry in outbound_history}
        inbound_prices = {entry["Timestamp"]: float(entry["Price"]) for entry in inbound_history}

        # Krok 2: Zbiera wszystkie unikalne timestampy z obu lotów i sortuje je
        all_timestamps = sorted(set(outbound_prices.keys()) | set(inbound_prices.keys()))

        # Krok 3: Przygotowuje dane do wykresu
        x_values = list(range(len(all_timestamps)))
        outbound_y = []
        inbound_y = []
        last_outbound_price = None
        last_inbound_price = None

        # Krok 4: Wypełnia dane dla obu lotów, przedłużając ostatnią znaną cenę
        for timestamp in all_timestamps:
            if timestamp in outbound_prices:
                last_outbound_price = outbound_prices[timestamp]
            outbound_y.append(last_outbound_price)

            if timestamp in inbound_prices:
                last_inbound_price = inbound_prices[timestamp]
            inbound_y.append(last_inbound_price)

        # Krok 5: Tworzy wykres
        fig, ax = plt.subplots(figsize=(12, 7))

        # Styl wykresu
        plt.style.use('ggplot')

        # Rysowanie danych — tylko dla punktów, które mają wartości
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
                     label=f'Lot TAM ({outbound_flight_number})')

        if inbound_y and any(y is not None for y in inbound_y):
            cleaned_inbound_y = [y if y is not None else inbound_y[i - 1] for i, y in enumerate(inbound_y) if
                                 i == 0 or y is not None or inbound_y[i - 1] is not None]
            plt.plot(x_values, inbound_y, linestyle='-', linewidth=2, color='magenta',
                     label=f'Lot POWRÓT ({inbound_flight_number})')

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
                  f'TAM: {outbound_flight_number} ({outbound_date}) | '
                  f'POWRÓT: {inbound_flight_number} ({inbound_date})',
                  fontsize=14)

        # Formatowanie osi X
        plt.xticks(x_values, all_timestamps, rotation=45, ha='right')

        plt.xlabel('Data sprawdzenia', fontsize=12)
        plt.ylabel('Cena (GBP)', fontsize=12)
        plt.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()

        plt.show()
