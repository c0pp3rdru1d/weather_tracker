"""
Tests for Weather Data API
Run with: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from main import app
from database import Base, get_db
from models import WeatherData

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def test_db():
    """Create and clean up test database for each test"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_root_endpoint(test_db):
    """Test root endpoint returns API information"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "1.0.0"

def test_health_check(test_db):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_create_weather_data(test_db):
    """Test creating weather data entry"""
    weather_data = {
        "location": "London",
        "temperature": 15.5,
        "humidity": 70.0,
        "pressure": 1012.0,
        "description": "Cloudy"
    }
    response = client.post("/weather", json=weather_data)
    assert response.status_code == 201
    data = response.json()
    assert data["location"] == "London"
    assert data["temperature"] == 15.5
    assert "id" in data
    assert "timestamp" in data

def test_create_weather_data_validation(test_db):
    """Test validation for invalid weather data"""
    # Invalid temperature
    invalid_data = {
        "location": "Test",
        "temperature": -150.0,  # Too low
        "humidity": 70.0,
        "pressure": 1012.0,
        "description": "Test"
    }
    response = client.post("/weather", json=invalid_data)
    assert response.status_code == 422

def test_get_weather_data(test_db):
    """Test retrieving weather data"""
    # Create test data
    weather_data = {
        "location": "Paris",
        "temperature": 20.0,
        "humidity": 60.0,
        "pressure": 1015.0,
        "description": "Sunny"
    }
    client.post("/weather", json=weather_data)
    
    # Retrieve data
    response = client.get("/weather")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["location"] == "Paris"

def test_get_weather_by_location(test_db):
    """Test filtering weather data by location"""
    # Create multiple entries
    locations = ["Tokyo", "Berlin", "Tokyo"]
    for loc in locations:
        weather_data = {
            "location": loc,
            "temperature": 18.0,
            "humidity": 65.0,
            "pressure": 1013.0,
            "description": "Clear"
        }
        client.post("/weather", json=weather_data)
    
    # Filter by location
    response = client.get("/weather?location=Tokyo")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(d["location"] == "Tokyo" for d in data)

def test_get_weather_by_id(test_db):
    """Test retrieving weather data by ID"""
    # Create entry
    weather_data = {
        "location": "Madrid",
        "temperature": 25.0,
        "humidity": 50.0,
        "pressure": 1018.0,
        "description": "Hot"
    }
    create_response = client.post("/weather", json=weather_data)
    created_id = create_response.json()["id"]
    
    # Get by ID
    response = client.get(f"/weather/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["location"] == "Madrid"

def test_get_weather_by_id_not_found(test_db):
    """Test 404 for non-existent weather data"""
    response = client.get("/weather/9999")
    assert response.status_code == 404

def test_delete_weather_data(test_db):
    """Test deleting weather data"""
    # Create entry
    weather_data = {
        "location": "Rome",
        "temperature": 22.0,
        "humidity": 55.0,
        "pressure": 1014.0,
        "description": "Warm"
    }
    create_response = client.post("/weather", json=weather_data)
    created_id = create_response.json()["id"]
    
    # Delete entry
    response = client.delete(f"/weather/{created_id}")
    assert response.status_code == 204
    
    # Verify deletion
    get_response = client.get(f"/weather/{created_id}")
    assert get_response.status_code == 404

def test_weather_statistics(test_db):
    """Test weather statistics endpoint"""
    # Create multiple entries for same location
    for temp in [18.0, 20.0, 22.0]:
        weather_data = {
            "location": "Amsterdam",
            "temperature": temp,
            "humidity": 70.0,
            "pressure": 1012.0,
            "description": "Variable"
        }
        client.post("/weather", json=weather_data)
    
    # Get statistics
    response = client.get("/analytics/stats?location=Amsterdam&days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "Amsterdam"
    assert data["record_count"] == 3
    assert data["temperature_avg"] == 20.0
    assert data["temperature_min"] == 18.0
    assert data["temperature_max"] == 22.0

def test_statistics_location_not_found(test_db):
    """Test 404 for statistics with no data"""
    response = client.get("/analytics/stats?location=NonExistent&days=7")
    assert response.status_code == 404

def test_available_locations(test_db):
    """Test getting available locations"""
    # Create entries for different locations
    locations = ["Vienna", "Brussels", "Vienna"]
    for loc in locations:
        weather_data = {
            "location": loc,
            "temperature": 17.0,
            "humidity": 68.0,
            "pressure": 1013.0,
            "description": "Mild"
        }
        client.post("/weather", json=weather_data)
    
    # Get locations
    response = client.get("/analytics/locations")
    assert response.status_code == 200
    data = response.json()
    assert "locations" in data
    assert len(data["locations"]) == 2  # Unique locations
    assert "Vienna" in data["locations"]
    assert "Brussels" in data["locations"]

def test_temperature_trends(test_db):
    """Test temperature trends endpoint"""
    # Create entries
    for i in range(3):
        weather_data = {
            "location": "Stockholm",
            "temperature": 15.0 + i,
            "humidity": 65.0,
            "pressure": 1010.0,
            "description": "Cool"
        }
        client.post("/weather", json=weather_data)
    
    # Get trends
    response = client.get("/analytics/trends/Stockholm?days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["location"] == "Stockholm"
    assert "trends" in data
    assert len(data["trends"]) > 0
