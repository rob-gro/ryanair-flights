# Ryanair Flight Search Tool

Ryanair Flight Search Tool is a sophisticated system for finding, tracking, and analyzing flight prices from Ryanair. The application integrates directly with Ryanair's API to provide real-time pricing data and historical price tracking, enabling users to make informed decisions about when to book their flights for the best possible prices.

## 🚀 Features

### ✈️ Flight Search
- **API Integration**: Direct communication with Ryanair's services API to fetch current flight data
- **Flexible Date Ranges**: Search across multiple date ranges for both outbound and return flights
- **Airport Selection**: Easily select source and destination airports
- **Filter Options**: Filter by time of day, maximum price, and specific destinations

### 📊 Price Tracking
- **Historical Data**: Automated recording of flight price changes over time
- **Price Alerts**: Identify price drops and increases for specific routes
- **Visualizations**: Interactive charts showing price trends for selected flights
- **Data Export**: Save price history in CSV format for external analysis

### 💰 Cost Analysis
- **Best Deals**: Automatic identification of the cheapest flight combinations
- **Price Comparison**: Compare current prices with historical averages
- **Distance Calculation**: Calculate the actual distance between airports
- **Price per Kilometer**: Analyze value based on distance traveled

## 🛠 Technologies

- **Language**: Python 3
- **Data Processing**: Pandas for data manipulation
- **API Communication**: Requests with backoff retry mechanism
- **Data Visualization**: Matplotlib for generating price history charts
- **Geospatial Calculations**: Haversine formula for accurate flight distances
- **Data Storage**: CSV-based persistent storage for price history

## 🗂 Project Structure

### Key Modules
- **API Communication**:
  - `ryanair.py` - Core API client for Ryanair services
  - `session_manager.py` - Managing HTTP sessions and cookies

- **Flight Data Processing**:
  - `flight_search.py` - Search functionality for finding available flights
  - `flight_service.py` - Core service coordinating flight searches and price tracking

- **Price Tracking**:
  - `price_tracker.py` - Recording and analyzing price history
  - `chart_service.py` - Generating visual representations of price trends

- **Data Management**:
  - `data_manager.py` - Handling data storage and retrieval operations
  - `date_utils.py` - Date manipulation utilities

- **Airport Information**:
  - `airport_utils.py` - Loading airport data and calculating distances

- **Data Models**:
  - `flight.py` - Core flight data model
  - `types.py` - Data structures representing flights and trips

## 🚀 Usage

The system is designed to be used from the command line:

```bash
python main.py
```

Configuration parameters can be modified directly in the main.py file:
- Source and destination airports
- Date ranges for outbound and return flights
- Currency for price display

## 📊 Output Examples

The application provides rich output including:

- Detailed information about the cheapest flight option including:
  - Flight numbers
  - Departure times
  - Prices in selected currency
  - Distance between airports

- Top 5 alternative options for both outbound and return flights

- Price history visualizations showing trends over time

## 💡 Advanced Features

- **Retry Mechanism**: Built-in exponential backoff strategy for API requests
- **Customizable Search**: Flexible parameters for fine-tuning search criteria
- **Multi-currency Support**: Select your preferred currency for price display
- **Price History Analysis**: Track price changes to identify booking trends

## 🔮 Future Enhancements

- Web interface for easier interaction
- Automated price alerts via email
- Mobile application for on-the-go flight searches
- Expanded airline support beyond Ryanair
- Machine learning for price prediction

---

Ryanair Flight Search Tool represents a modern approach to flight booking, empowering travelers with data-driven insights into airline pricing. Through its integration with Ryanair's API and sophisticated price tracking capabilities, the system provides a comprehensive solution for finding the best flight deals available.