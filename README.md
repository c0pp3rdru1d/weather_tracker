<<<<<<< HEAD
# Weather Data API 🌦️

A professional REST API for weather data collection and analytics, built with FastAPI and SQLAlchemy. This project demonstrates best practices in Python API development, including proper project structure, testing, containerization, and documentation.

## Features

- **RESTful API** with FastAPI
- **Data persistence** with SQLAlchemy and SQLite
- **Comprehensive analytics** endpoints
- **Input validation** with Pydantic
- **Full test coverage** with pytest
- **Docker containerization**
- **Interactive API documentation** (Swagger/ReDoc)
- **Professional code structure** following best practices

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **SQLite**: Lightweight database
- **Pytest**: Testing framework
- **Docker**: Containerization
- **Uvicorn**: ASGI server

## Project Structure

```
weather-data-api/
├── main.py              # FastAPI application and endpoints
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic schemas for validation
├── database.py          # Database configuration
├── test_main.py         # Comprehensive test suite
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker container configuration
├── docker-compose.yml   # Docker Compose setup
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Installation

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd weather-data-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually**
   ```bash
   docker build -t weather-api .
   docker run -p 8000:8000 weather-api
   ```

## API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Weather Data Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint with API information |
| GET | `/health` | Health check endpoint |
| POST | `/weather` | Create new weather data entry |
| GET | `/weather` | Get weather data with optional filtering |
| GET | `/weather/{id}` | Get specific weather data by ID |
| DELETE | `/weather/{id}` | Delete weather data entry |

### Analytics Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/stats` | Get weather statistics for a location |
| GET | `/analytics/locations` | Get list of available locations |
| GET | `/analytics/trends/{location}` | Get temperature trends for a location |

## Usage Examples

### Create Weather Data

```bash
curl -X POST "http://localhost:8000/weather" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York",
    "temperature": 22.5,
    "humidity": 65.0,
    "pressure": 1013.25,
    "description": "Partly cloudy"
  }'
```

### Get Weather Data

```bash
# Get all weather data
curl "http://localhost:8000/weather"

# Filter by location
curl "http://localhost:8000/weather?location=New York"

# Pagination
curl "http://localhost:8000/weather?limit=10&skip=0"
```

### Get Statistics

```bash
curl "http://localhost:8000/analytics/stats?location=New York&days=7"
```

### Get Temperature Trends

```bash
curl "http://localhost:8000/analytics/trends/New York?days=30"
```

## Testing

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

All tests include proper setup and teardown, ensuring isolation between test cases.

## Data Models

### WeatherData

- `id`: Unique identifier (auto-generated)
- `location`: City or location name
- `temperature`: Temperature in Celsius
- `humidity`: Humidity percentage (0-100)
- `pressure`: Atmospheric pressure in hPa
- `description`: Weather description
- `timestamp`: Record timestamp (auto-generated)

### Validation Rules

- Temperature: -100°C to 60°C
- Humidity: 0% to 100%
- Pressure: 800 hPa to 1100 hPa
- Location: 1-100 characters, non-empty
- Description: 1-100 characters

## Development

### Adding New Features

1. Define new models in `models.py`
2. Create Pydantic schemas in `schemas.py`
3. Implement endpoints in `main.py`
4. Write tests in `test_main.py`
5. Update documentation

### Code Quality

This project follows Python best practices:
- Type hints for better code clarity
- Comprehensive docstrings
- Proper error handling
- Input validation
- Database session management
- RESTful API design principles

## Deployment

### Production Considerations

1. **Use PostgreSQL** instead of SQLite:
   ```python
   DATABASE_URL = "postgresql://user:password@localhost/weather_db"
   ```

2. **Set environment variables**:
   ```bash
   export DATABASE_URL="postgresql://..."
   export API_KEY="your-secret-key"
   ```

3. **Enable HTTPS** with a reverse proxy (nginx, Caddy)

4. **Add authentication** for protected endpoints

5. **Implement rate limiting** to prevent abuse

6. **Set up logging** and monitoring

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI and modern Python practices**
=======
# weather_tracker
Another weather tracker dev project
>>>>>>> da1df611219f0cbcb3b0bf9f537083b9c0364b9f
