from datetime import datetime, timedelta

class DateUtils:
    @staticmethod
    def generate_dates(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end - start).days + 1)]
