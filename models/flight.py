from dataclasses import dataclass
from datetime import datetime

@dataclass
class Flight:
    origin: str
    destination: str
    departure_time: datetime
    flight_number: str
    price: float
    currency: str
