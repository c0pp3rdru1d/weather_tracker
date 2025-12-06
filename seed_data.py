"""
Script to seed the database with sample weather data
Run with: python seed_data.py
"""
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database import SessionLocal, init_db
from models import WeatherData

# Sample cities
CITIES = [
    "New York", "London", "Tokyo", "Paris", "Berlin",
    "Sydney", "Toronto", "Dubai", "Singapore", "Mumbai"
]

# Weather descriptions
DESCRIPTIONS = [
    "Sunny", "Partly cloudy", "Cloudy", "Rainy", "Stormy",
    "Foggy", "Clear", "Overcast", "Drizzle", "Windy"
]

def generate_weather_data(location: str, days_back: int = 30) -> list:
    """Generate realistic weather data for a location"""
    weather_records = []
    base_temp = random.uniform(10, 25)  # Base temperature for the location
    
    for i in range(days_back * 4):  # 4 records per day
        timestamp = datetime.utcnow() - timedelta(hours=6 * i)
        
        # Add some variation to temperature
        temp_variation = random.uniform(-5, 5)
        temperature = round(base_temp + temp_variation, 1)
        
        # Generate realistic humidity and pressure
        humidity = round(random.uniform(40, 90), 1)
        pressure = round(random.uniform(990, 1030), 1)
        
        # Random weather description
        description = random.choice(DESCRIPTIONS)
        
        weather_records.append({
            "location": location,
            "temperature": temperature,
            "humidity": humidity,
            "pressure": pressure,
            "description": description,
            "timestamp": timestamp
        })
    
    return weather_records

def seed_database(num_days: int = 30):
    """Seed the database with sample data"""
    print("Initializing database...")
    init_db()
    
    db: Session = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(WeatherData).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} records.")
            response = input("Do you want to clear existing data? (yes/no): ")
            if response.lower() == 'yes':
                db.query(WeatherData).delete()
                db.commit()
                print("Existing data cleared.")
            else:
                print("Keeping existing data and adding new records.")
        
        print(f"\nGenerating weather data for {len(CITIES)} cities over {num_days} days...")
        
        total_records = 0
        for city in CITIES:
            print(f"  Generating data for {city}...")
            weather_data = generate_weather_data(city, num_days)
            
            for record in weather_data:
                db_weather = WeatherData(**record)
                db.add(db_weather)
            
            total_records += len(weather_data)
        
        db.commit()
        print(f"\n✅ Successfully seeded database with {total_records} weather records!")
        print(f"   Cities: {', '.join(CITIES)}")
        print(f"   Time period: {num_days} days")
        print(f"   Records per city: {num_days * 4}")
        
        # Show some statistics
        print("\n📊 Sample Statistics:")
        for city in CITIES[:3]:  # Show first 3 cities
            records = db.query(WeatherData).filter(WeatherData.location == city).all()
            if records:
                avg_temp = sum(r.temperature for r in records) / len(records)
                print(f"   {city}: {len(records)} records, avg temp: {avg_temp:.1f}°C")
    
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Weather Data API - Database Seeding Script")
    print("=" * 60)
    
    try:
        days = input("\nEnter number of days of data to generate (default: 30): ")
        days = int(days) if days else 30
        seed_database(days)
    except ValueError:
        print("Invalid input. Using default value of 30 days.")
        seed_database(30)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    
    print("\n" + "=" * 60)
    print("You can now start the API with: uvicorn main:app --reload")
    print("Visit http://localhost:8000/docs for interactive documentation")
    print("=" * 60)
