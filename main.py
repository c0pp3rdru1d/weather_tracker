"""
Weather Data API - Main Application
A professional REST API for weather data collection and analytics
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import statistics

from database import get_db, init_db
from models import WeatherData
from schemas import WeatherDataCreate, WeatherDataResponse, WeatherStats

app = FastAPI(
    title="Weather Data API",
    description="Professional API for weather data collection and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Weather Data API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "weather": "/weather",
            "analytics": "/analytics",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/weather", response_model=WeatherDataResponse, status_code=201, tags=["Weather Data"])
async def create_weather_data(
    weather: WeatherDataCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new weather data entry
    
    - **location**: City or location name
    - **temperature**: Temperature in Celsius
    - **humidity**: Humidity percentage (0-100)
    - **pressure**: Atmospheric pressure in hPa
    - **description**: Weather description (e.g., 'Sunny', 'Cloudy')
    """
    db_weather = WeatherData(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

@app.get("/weather", response_model=List[WeatherDataResponse], tags=["Weather Data"])
async def get_weather_data(
    location: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    skip: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieve weather data with optional filtering
    
    - **location**: Filter by location (optional)
    - **limit**: Maximum number of records to return
    - **skip**: Number of records to skip (pagination)
    """
    query = db.query(WeatherData)
    
    if location:
        query = query.filter(WeatherData.location.ilike(f"%{location}%"))
    
    weather_data = query.order_by(WeatherData.timestamp.desc()).offset(skip).limit(limit).all()
    return weather_data

@app.get("/weather/{weather_id}", response_model=WeatherDataResponse, tags=["Weather Data"])
async def get_weather_by_id(weather_id: int, db: Session = Depends(get_db)):
    """Get a specific weather data entry by ID"""
    weather = db.query(WeatherData).filter(WeatherData.id == weather_id).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    return weather

@app.delete("/weather/{weather_id}", status_code=204, tags=["Weather Data"])
async def delete_weather_data(weather_id: int, db: Session = Depends(get_db)):
    """Delete a weather data entry"""
    weather = db.query(WeatherData).filter(WeatherData.id == weather_id).first()
    if not weather:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    db.delete(weather)
    db.commit()
    return None

@app.get("/analytics/stats", response_model=WeatherStats, tags=["Analytics"])
async def get_weather_statistics(
    location: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get weather statistics for a location over a specified period
    
    - **location**: Location name
    - **days**: Number of days to analyze (default: 7)
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    weather_data = db.query(WeatherData).filter(
        WeatherData.location.ilike(f"%{location}%"),
        WeatherData.timestamp >= start_date
    ).all()
    
    if not weather_data:
        raise HTTPException(
            status_code=404,
            detail=f"No weather data found for location: {location}"
        )
    
    temperatures = [w.temperature for w in weather_data]
    humidities = [w.humidity for w in weather_data]
    pressures = [w.pressure for w in weather_data]
    
    return WeatherStats(
        location=location,
        period_days=days,
        record_count=len(weather_data),
        temperature_avg=round(statistics.mean(temperatures), 2),
        temperature_min=round(min(temperatures), 2),
        temperature_max=round(max(temperatures), 2),
        humidity_avg=round(statistics.mean(humidities), 2),
        pressure_avg=round(statistics.mean(pressures), 2),
        start_date=start_date,
        end_date=datetime.utcnow()
    )

@app.get("/analytics/locations", tags=["Analytics"])
async def get_available_locations(db: Session = Depends(get_db)):
    """Get list of all locations with weather data"""
    locations = db.query(WeatherData.location).distinct().all()
    return {
        "locations": [loc[0] for loc in locations],
        "count": len(locations)
    }

@app.get("/analytics/trends/{location}", tags=["Analytics"])
async def get_temperature_trends(
    location: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Get temperature trends for a location
    
    Returns daily average temperatures for trend analysis
    """
    start_date = datetime.utcnow() - timedelta(days=days)
    
    weather_data = db.query(WeatherData).filter(
        WeatherData.location.ilike(f"%{location}%"),
        WeatherData.timestamp >= start_date
    ).order_by(WeatherData.timestamp).all()
    
    if not weather_data:
        raise HTTPException(
            status_code=404,
            detail=f"No weather data found for location: {location}"
        )
    
    # Group by date and calculate daily averages
    daily_data = {}
    for record in weather_data:
        date_key = record.timestamp.date().isoformat()
        if date_key not in daily_data:
            daily_data[date_key] = []
        daily_data[date_key].append(record.temperature)
    
    trends = [
        {
            "date": date,
            "avg_temperature": round(statistics.mean(temps), 2),
            "min_temperature": round(min(temps), 2),
            "max_temperature": round(max(temps), 2)
        }
        for date, temps in sorted(daily_data.items())
    ]
    
    return {
        "location": location,
        "period_days": days,
        "trends": trends
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
