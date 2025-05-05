import csv
import os


class DataManager:
    @staticmethod
    def save_to_csv(data, filename):
        file_exists = os.path.exists(filename)

        with open(filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(data[0].keys())

            for row in data:
                writer.writerow(row.values())

    @staticmethod
    def read_csv(filename):
        if not os.path.exists(filename):
            return []

        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            return list(reader)
