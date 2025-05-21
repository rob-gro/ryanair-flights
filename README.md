## How It Works
The application starts by loading a database of airports and their geographical coordinates. Users specify source and destination airports along with date ranges for both outbound and return flights. The program then:

1. Communicates with the Ryanair API to search for available flights
2. Retrieves and updates pricing information for each flight
3. Sorts flights by price to find the cheapest options
4. Updates the price history database
5. Generates visualizations of price changes over time

## Technical Details
- Built in Python
- Uses the Ryanair API to retrieve flight information
- Implements backoff strategies for API request retries
- Stores price history in CSV format
- Uses matplotlib for chart generation

## Example Usage
The main script allows users to search for flights between specific airport pairs (e.g., Edinburgh to Poznan) and displays:
- The cheapest round-trip option with detailed information
- The next 5 cheapest outbound flight options
- The next 5 cheapest inbound flight options
- A chart visualizing price changes for the selected flights over time

## Future Enhancements
- User interface for easier interaction
- Email notifications for price drops
- Integration with more airlines
- Flight recommendation system based on price history patterns# Ryanair Flight Search Tool

## Project Description
This application is designed to find the cheapest Ryanair flights between selected airports within specified date ranges. The program allows users to monitor flight price changes over time and select the most cost-effective connections.

## Key Features
- Search for round-trip flights between specified airports
- Track flight price history
- Generate price change charts for selected flights
- Display the cheapest flight options
- Calculate distances between airports
- Sort flights by price

## Project Structure

### `models` Package
- `Flight` - class representing a single flight with attributes such as origin airport, destination, departure time, flight number, price, currency
- `Ryanair` - class responsible for communicating with the Ryanair API and retrieving flight information
- `Trip` - class representing a round-trip journey (outbound and inbound flights)

### `services` Package
- `ChartService` - service for generating flight price charts
- `DataManager` - manages data, saves and reads from CSV files
- `FlightSearch` - searches for flights using the Ryanair API
- `FlightService` - main application service, handles flight searches and price management
- `PriceTracker` - tracks flight price history
- `SessionManager` - manages HTTP sessions for communication with the Ryanair API

### `utils` Package
- `airport_utils` - utility functions for loading airport data and calculating distances between airports
- `date_utils` - date handling utilities, including date range generation
- `flight_utils` - functions for updating flight prices based on historical data